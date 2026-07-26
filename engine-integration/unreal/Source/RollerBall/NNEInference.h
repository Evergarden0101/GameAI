// NNEInference.h — run a trained ONNX model at runtime with Unreal's Neural Network Engine
// -----------------------------------------------------------------------------------------
// ⚠️ Illustrative — NNE API details vary by UE version. This is Unreal's analog of Unity's
// SentisInference.cs: load a network (e.g. trained in PyTorch, exported to ONNX) and run
// forward passes in the game — no Python at runtime.

#pragma once

#include "CoreMinimal.h"
#include "NNERuntimeCPU.h"

class UNNEModelData;

class ROLLERBALL_API FBrain
{
public:
    // Create from an imported .onnx asset (UNNEModelData).
    bool Load(UNNEModelData* ModelData);

    // observations in -> actions out (one forward pass).
    void Decide(const TArray<float>& Observations, TArray<float>& OutActions);

private:
    TSharedPtr<UE::NNE::IModelInstanceCPU> ModelInstance;
};
