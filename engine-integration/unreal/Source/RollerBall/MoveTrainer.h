// MoveTrainer.h — Learning Agents Trainer: REWARD (incl. HUMAN FEEDBACK) + completion
// -----------------------------------------------------------------------------------
// ⚠️ Experimental API — illustrative shapes. The Trainer is the Unreal analog of
// Unity's AddReward() + EndEpisode(). The PPO update itself runs in-engine; you only
// define the reward signal and when an episode ends.
//
// HUMAN-IN-THE-LOOP: GatherAgentReward adds a `HumanReward` term that RollerManager
// fills from your key presses, so your live feedback shapes what the policy learns.

#pragma once

#include "CoreMinimal.h"
#include "LearningAgentsTrainer.h"
#include "MoveTrainer.generated.h"

UCLASS()
class ROLLERBALL_API UMoveTrainer : public ULearningAgentsTrainer
{
    GENERATED_BODY()

public:
    // +1 for reaching the goal, small time penalty, PLUS any human feedback given
    // since the last step (consumed here).
    virtual void GatherAgentReward_Implementation(
        float& OutReward, const int32 AgentId) override;

    // End (and reset) the episode when the goal is reached or the agent falls off.
    virtual void GatherAgentCompletion_Implementation(
        ELearningAgentsCompletion& OutCompletion, const int32 AgentId) override;

    // Place the agent and its goal for a fresh episode.
    virtual void ResetAgentEpisode_Implementation(const int32 AgentId) override;

    // Goal locations (shared with the interactor / manager).
    UPROPERTY() TMap<int32, FVector> Goals;

    // Human feedback accumulated by RollerManager from + / - key presses.
    UPROPERTY() TMap<int32, float> HumanReward;

    float ReachRadius = 150.f;   // cm
};
