// MoveTrainer.cpp — see header caveat (experimental API; illustrative shapes).
#include "MoveTrainer.h"
#include "GameFramework/Pawn.h"

void UMoveTrainer::GatherAgentReward_Implementation(float& OutReward, const int32 AgentId)
{
    const APawn* Pawn = Cast<APawn>(GetAgent(AgentId));
    const FVector Me   = Pawn ? Pawn->GetActorLocation() : FVector::ZeroVector;
    const FVector Goal = Goals.FindRef(AgentId);

    float Reward = -0.001f;                                   // small time penalty
    if (FVector::Dist2D(Me, Goal) < ReachRadius) Reward += 1.0f;   // reached the goal
    if (Me.Z < 0.f) Reward -= 1.0f;                          // fell off

    // ---- HUMAN FEEDBACK: fold in and consume the operator's live reward -----------
    if (float* H = HumanReward.Find(AgentId))
    {
        Reward += *H;      // your + / - presses directly change PPO's reward
        *H = 0.f;          // consume so each press counts once
    }

    OutReward = Reward;
}

void UMoveTrainer::GatherAgentCompletion_Implementation(
    ELearningAgentsCompletion& OutCompletion, const int32 AgentId)
{
    const APawn* Pawn = Cast<APawn>(GetAgent(AgentId));
    const FVector Me   = Pawn ? Pawn->GetActorLocation() : FVector::ZeroVector;
    const FVector Goal = Goals.FindRef(AgentId);

    const bool bReached = FVector::Dist2D(Me, Goal) < ReachRadius;
    const bool bFell    = Me.Z < 0.f;
    OutCompletion = (bReached || bFell) ? ELearningAgentsCompletion::Termination
                                        : ELearningAgentsCompletion::Running;
}

void UMoveTrainer::ResetAgentEpisode_Implementation(const int32 AgentId)
{
    if (APawn* Pawn = Cast<APawn>(GetAgent(AgentId)))
    {
        Pawn->SetActorLocation(FVector(0.f, 0.f, 50.f));     // back to the start
    }
    // New random goal within the platform.
    Goals.Add(AgentId, FVector(FMath::FRandRange(-400.f, 400.f),
                               FMath::FRandRange(-400.f, 400.f), 50.f));
}
