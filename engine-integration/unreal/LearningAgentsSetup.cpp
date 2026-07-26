// LearningAgentsSetup.cpp — wire up Learning Agents and drive the per-tick loop
// -----------------------------------------------------------------------------
// ILLUSTRATIVE SKELETON (see MoveInteractor.h caveat). Shows how the pieces connect
// and how one Tick advances either TRAINING or INFERENCE. In a real project this lives
// on a manager actor/component; factory calls and settings structs vary by UE version.

#include "LearningAgentsManager.h"
#include "LearningAgentsPolicy.h"
#include "LearningAgentsCritic.h"
#include "LearningAgentsPPOTrainer.h"
#include "MoveInteractor.h"
#include "MoveTrainer.h"

// Held on your manager actor/component.
struct FBrain
{
    ULearningAgentsManager* Manager;
    UMoveInteractor*        Interactor;
    ULearningAgentsPolicy*  Policy;     // the neural network
    ULearningAgentsCritic*  Critic;     // value function (training only)
    UMoveTrainer*           Trainer;    // reward/completion (training only)
    bool                    bTraining;  // true while learning, false when shipping
};

void SetupBrain(FBrain& B, ULearningAgentsManager* Manager)
{
    B.Manager = Manager;

    // The Interactor defines observations & actions; the Policy is the network that
    // maps one to the other.
    B.Interactor = ULearningAgentsInteractor::MakeInteractor<UMoveInteractor>(Manager);
    B.Policy     = ULearningAgentsPolicy::MakePolicy(Manager, B.Interactor,
                                                     /*PolicySettings*/ {});

    if (B.bTraining)
    {
        // Only needed while learning: the critic + PPO trainer + reward definition.
        B.Critic  = ULearningAgentsCritic::MakeCritic(Manager, B.Policy, {});
        B.Trainer = ULearningAgentsPPOTrainer::MakeTrainer<UMoveTrainer>(
                        Manager, B.Interactor, B.Policy, B.Critic);
    }
}

// Call this every frame from your manager's Tick().
void TickBrain(FBrain& B)
{
    if (B.bTraining)
    {
        // TRAIN: gather obs -> pick actions -> apply -> gather reward/done -> update.
        // Learning Agents batches these; a single call advances one training step.
        B.Trainer->RunTraining(/*TrainerSettings*/ {}, /*PPOSettings*/ {},
                               /*CriticSettings*/ {});
        // Tip: crank the world time dilation and run many agents to train faster.
    }
    else
    {
        // SHIP: no trainer, no critic, no reward — just run the trained network.
        B.Interactor->GatherObservations();   // read the world into observations
        B.Policy->RunInference();              // network: observations -> actions
        // (PerformAgentAction has already applied them to the pawns)
    }
}

// After training, save the Policy's network as an asset and load it in your shipping
// build with bTraining = false. That asset is the "brain" your game runs every tick.
