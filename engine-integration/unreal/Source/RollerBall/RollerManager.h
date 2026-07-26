// RollerManager.h — sets up Learning Agents, drives the tick, and reads HUMAN FEEDBACK
// ------------------------------------------------------------------------------------
// ⚠️ Experimental API — illustrative. Drop one of these actors in your level. It spawns
// agents, wires up the Manager/Interactor/Policy/Trainer, and each Tick advances either
// TRAINING (with your + / - feedback folded into reward) or INFERENCE.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RollerManager.generated.h"

class ULearningAgentsManager;
class UMoveInteractor;
class ULearningAgentsPolicy;
class ULearningAgentsCritic;
class UMoveTrainer;

UCLASS()
class ROLLERBALL_API ARollerManager : public AActor
{
    GENERATED_BODY()

public:
    ARollerManager();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UPROPERTY(EditAnywhere) bool bTraining = true;      // false = run trained brain
    UPROPERTY(EditAnywhere) int32 NumAgents = 16;       // parallel agents speed up RL
    UPROPERTY(EditAnywhere) TSubclassOf<APawn> AgentPawnClass;
    UPROPERTY(EditAnywhere) float HumanRewardAmount = 0.5f;

private:
    UPROPERTY() ULearningAgentsManager* Manager;
    UPROPERTY() UMoveInteractor*        Interactor;
    UPROPERTY() ULearningAgentsPolicy*  Policy;
    UPROPERTY() ULearningAgentsCritic*  Critic;
    UPROPERTY() UMoveTrainer*           Trainer;

    // Input handlers — the human's live feedback during training.
    void RewardPlus();
    void RewardMinus();
    void ApplyHumanReward(float Amount);
};
