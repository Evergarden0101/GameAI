// MoveTrainer.h — Unreal Learning Agents "Trainer": the REWARD and when an episode ENDS
// -------------------------------------------------------------------------------------
// ILLUSTRATIVE SKELETON (see MoveInteractor.h caveat). The Trainer is the Unreal
// counterpart of Unity's AddReward() + EndEpisode(): it defines the reward signal that
// shapes learning and the "completion" that resets an agent's episode. The PPO update
// itself runs in-engine — you don't implement it.

#pragma once

#include "LearningAgentsTrainer.h"
#include "MoveTrainer.generated.h"

UCLASS()
class UMoveTrainer : public ULearningAgentsTrainer
{
    GENERATED_BODY()

public:
    // REWARD: +1 for reaching the goal, small time penalty otherwise. This is the
    // exact analog of RollerAgent.OnActionReceived()'s AddReward() calls in Unity.
    virtual void GatherAgentReward_Implementation(
        float& OutReward, const int32 AgentId) override;

    // COMPLETION: end (and reset) the episode when the goal is reached or the agent
    // falls off / times out — the analog of Unity's EndEpisode().
    virtual void GatherAgentCompletion_Implementation(
        ELearningAgentsCompletion& OutCompletion, const int32 AgentId) override;

    // RESET: place the agent and goal for a fresh episode (analog of OnEpisodeBegin()).
    virtual void ResetAgentEpisode_Implementation(const int32 AgentId) override;
};
