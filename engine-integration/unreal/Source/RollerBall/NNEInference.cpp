// NNEInference.cpp — see header caveat (illustrative; NNE API varies by UE version).
#include "NNEInference.h"
#include "NNE.h"
#include "NNEModelData.h"

bool FBrain::Load(UNNEModelData* ModelData)
{
    TWeakInterfacePtr<INNERuntimeCPU> Runtime =
        UE::NNE::GetRuntime<INNERuntimeCPU>(TEXT("NNERuntimeORTCpu"));
    if (!Runtime.IsValid() || !ModelData) return false;

    TSharedPtr<UE::NNE::IModelCPU> Model = Runtime->CreateModelCPU(ModelData);
    ModelInstance = Model ? Model->CreateModelInstanceCPU() : nullptr;
    return ModelInstance.IsValid();
}

void FBrain::Decide(const TArray<float>& Observations, TArray<float>& OutActions)
{
    if (!ModelInstance.IsValid()) return;

    UE::NNE::FTensorShape InShape =
        UE::NNE::FTensorShape::Make({ 1, (uint32)Observations.Num() });
    ModelInstance->SetInputTensorShapes({ InShape });

    OutActions.SetNumZeroed(2);   // action dimension

    UE::NNE::FTensorBindingCPU In{ (void*)Observations.GetData(),
                                   (uint64)Observations.Num() * sizeof(float) };
    UE::NNE::FTensorBindingCPU Out{ (void*)OutActions.GetData(),
                                    (uint64)OutActions.Num() * sizeof(float) };

    ModelInstance->RunSync({ In }, { Out });   // OutActions now holds the network output
}
