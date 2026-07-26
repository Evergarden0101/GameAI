// RollerManager.h — setup + train/record/imitate/infer Tick + HUMAN FEEDBACK / DEMOS
// ----------------------------------------------------------------------------------
// ⚠️ Experimental API — illustrative. Drop one of these actors in your level and choose
// a Mode. It spawns agents, wires up Learning Agents, and each Tick advances:
//   Train     — in-engine PPO, with your + / - key feedback folded into reward.
//   Record    — YOU drive with WASD; a Recorder captures a demonstration recording.
//   Imitate   — an Imitation Trainer teaches the policy to copy that recording (BC).
//   Inference — run the trained policy, no training.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RollerManager.generated.h"

class ULearningAgentsManager;
class UMoveInteractor;
class ULearningAgentsPolicy;
class ULearningAgentsCritic;
class UMoveTrainer;
class ULearningAgentsRecorder;
class ULearningAgentsRecording;
class ULearningAgentsImitationTrainer;

UENUM(BlueprintType)
enum class ERollerMode : uint8 { Train, Record, Imitate, Inference };

UCLASS()
class ROLLERBALL_API ARollerManager : public AActor
{
    GENERATED_BODY()

public:
    ARollerManager();

    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

    UPROPERTY(EditAnywhere) ERollerMode Mode = ERollerMode::Train;
    UPROPERTY(EditAnywhere) int32 NumAgents = 16;       // forced to 1 in Record mode
    UPROPERTY(EditAnywhere) TSubclassOf<APawn> AgentPawnClass;
    UPROPERTY(EditAnywhere) float HumanRewardAmount = 0.5f;

    // The demonstration recording asset — created in Record, consumed in Imitate.
    UPROPERTY(EditAnywhere) ULearningAgentsRecording* Recording;

private:
    UPROPERTY() ULearningAgentsManager*          Manager;
    UPROPERTY() UMoveInteractor*                 Interactor;
    UPROPERTY() ULearningAgentsPolicy*           Policy;
    UPROPERTY() ULearningAgentsCritic*           Critic;
    UPROPERTY() UMoveTrainer*                    Trainer;
    UPROPERTY() ULearningAgentsRecorder*         Recorder;
    UPROPERTY() ULearningAgentsImitationTrainer* ImitationTrainer;

    FVector2D HumanDrive = FVector2D::ZeroVector;   // current WASD direction
    bool bRecording = false;

    // input handlers
    void RewardPlus();
    void RewardMinus();
    void ApplyHumanReward(float Amount);
    void DriveX(float V);         // A/D
    void DriveY(float V);         // W/S
    void ToggleRecording();       // R — start/stop and save the demo
};
