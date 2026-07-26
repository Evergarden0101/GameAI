// NNEInference.cpp — run a trained ONNX model at runtime with Unreal's Neural Network Engine
// -----------------------------------------------------------------------------------------
// ILLUSTRATIVE SKELETON. This is Unreal's analog of Unity's SentisInference.cs: load a
// neural network (e.g. one TRAINED IN PYTHON with PyTorch and exported to ONNX) and run
// forward passes inside the game — no Python at runtime. API details vary by UE version;
// see the NNE docs.

#include "NNE.h"
#include "NNERuntimeCPU.h"
#include "NNEModelData.h"

// UNNEModelData* ModelData  -> an imported .onnx asset (assigned in the editor).
TSharedPtr<UE::NNE::IModelInstanceCPU> CreateBrain(UNNEModelData* ModelData)
{
    // Pick a runtime backend (ORT CPU here; GPU/DirectML runtimes also exist).
    TWeakInterfacePtr<INNERuntimeCPU> Runtime =
        UE::NNE::GetRuntime<INNERuntimeCPU>(TEXT("NNERuntimeORTCpu"));
    if (!Runtime.IsValid()) return nullptr;

    TSharedPtr<UE::NNE::IModelCPU> Model = Runtime->CreateModelCPU(ModelData);
    return Model ? Model->CreateModelInstanceCPU() : nullptr;
}

// Run one forward pass: observations in -> actions out.
void Decide(UE::NNE::IModelInstanceCPU* Brain,
            const TArray<float>& Observations, TArray<float>& OutActions)
{
    // Describe the input/output tensor shapes ([batch=1, features]).
    UE::NNE::FTensorShape InShape =
        UE::NNE::FTensorShape::Make({ 1, (uint32)Observations.Num() });
    Brain->SetInputTensorShapes({ InShape });

    OutActions.SetNumZeroed(/*your action dim*/ 2);

    // Bind CPU memory for input and output, then run synchronously.
    UE::NNE::FTensorBindingCPU In{ (void*)Observations.GetData(),
                                   Observations.Num() * sizeof(float) };
    UE::NNE::FTensorBindingCPU Out{ (void*)OutActions.GetData(),
                                    OutActions.Num() * sizeof(float) };

    Brain->RunSync({ In }, { Out });   // OutActions now holds the network's output
}

// Usage each tick:
//   TArray<float> Obs = { GoalX, GoalY, MeX, MeY, VelX, VelY };
//   TArray<float> Act;
//   Decide(Brain.Get(), Obs, Act);
//   Pawn->AddMovementInput(FVector(Act[0], Act[1], 0));
//
// Same lesson as everywhere: at runtime the "AI" is a fast forward pass on the
// observation vector. The learning already happened offline.
