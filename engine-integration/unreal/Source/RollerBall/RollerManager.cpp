// RollerManager.cpp — see header caveat (experimental API; illustrative shapes).
#include "RollerManager.h"
#include "MoveInteractor.h"
#include "MoveTrainer.h"
#include "LearningAgentsManager.h"
#include "LearningAgentsPolicy.h"
#include "LearningAgentsCritic.h"
#include "LearningAgentsTrainer.h"
#include "GameFramework/DefaultPawn.h"
#include "GameFramework/PlayerController.h"
#include "Components/InputComponent.h"

ARollerManager::ARollerManager()
{
    PrimaryActorTick.bCanEverTick = true;
    if (!AgentPawnClass) AgentPawnClass = ADefaultPawn::StaticClass();
}

void ARollerManager::BeginPlay()
{
    Super::BeginPlay();

    // 1) Manager holds the agents. Spawn NumAgents pawns and register them.
    Manager = NewObject<ULearningAgentsManager>(this);
    for (int32 i = 0; i < NumAgents; ++i)
    {
        APawn* Pawn = GetWorld()->SpawnActor<APawn>(
            AgentPawnClass, FVector(0, i * 200.f, 50.f), FRotator::ZeroRotator);
        Manager->AddAgent(Pawn);
    }

    // 2) Interactor (observations/actions) + Policy (the neural network).
    Interactor = ULearningAgentsInteractor::MakeInteractor<UMoveInteractor>(Manager);
    Policy     = ULearningAgentsPolicy::MakePolicy(Manager, Interactor, {});

    if (bTraining)
    {
        // 3) Critic + Trainer (reward/completion + in-engine PPO). Share the Goals map.
        Critic  = ULearningAgentsCritic::MakeCritic(Manager, Policy, {});
        Trainer = ULearningAgentsTrainer::MakeTrainer<UMoveTrainer>(
                      Manager, Interactor, Policy, Critic);
        Trainer->Goals = Interactor->Goals;    // shared goal locations
    }

    // 4) Let this actor receive keyboard input for human feedback.
    if (APlayerController* PC = GetWorld()->GetFirstPlayerController())
    {
        EnableInput(PC);
        if (InputComponent)
        {
            InputComponent->BindKey(EKeys::Equals,   IE_Pressed, this, &ARollerManager::RewardPlus);
            InputComponent->BindKey(EKeys::Add,      IE_Pressed, this, &ARollerManager::RewardPlus);
            InputComponent->BindKey(EKeys::Hyphen,   IE_Pressed, this, &ARollerManager::RewardMinus);
            InputComponent->BindKey(EKeys::Subtract, IE_Pressed, this, &ARollerManager::RewardMinus);
        }
    }
}

void ARollerManager::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    if (bTraining && Trainer)
    {
        // One PPO step: gather obs -> act -> gather reward (incl. human) -> update.
        Trainer->RunTraining({}, {}, {});
    }
    else if (Policy)
    {
        // Shipping: no trainer, no reward — just run the trained network each tick.
        Interactor->GatherObservations();
        Policy->RunInference();
    }
}

// ---- HUMAN FEEDBACK: press + / - to reward or punish every agent right now ---------
void ARollerManager::RewardPlus()  { ApplyHumanReward(+HumanRewardAmount); }
void ARollerManager::RewardMinus() { ApplyHumanReward(-HumanRewardAmount); }

void ARollerManager::ApplyHumanReward(float Amount)
{
    if (!Trainer) return;
    for (int32 i = 0; i < NumAgents; ++i)
    {
        float& H = Trainer->HumanReward.FindOrAdd(i);
        H += Amount;               // consumed inside MoveTrainer::GatherAgentReward
    }
    UE_LOG(LogTemp, Display, TEXT("[RollerBall] human feedback %+0.2f"), Amount);
}
