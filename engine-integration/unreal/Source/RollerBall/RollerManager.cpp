// RollerManager.cpp — see header caveat (experimental API; illustrative shapes).
#include "RollerManager.h"
#include "MoveInteractor.h"
#include "MoveTrainer.h"
#include "LearningAgentsManager.h"
#include "LearningAgentsPolicy.h"
#include "LearningAgentsCritic.h"
#include "LearningAgentsTrainer.h"
#include "LearningAgentsRecorder.h"
#include "LearningAgentsRecording.h"
#include "LearningAgentsImitationTrainer.h"
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

    const bool bRecordMode = (Mode == ERollerMode::Record);
    const int32 Count = bRecordMode ? 1 : NumAgents;   // one agent when recording

    // 1) Manager + agents.
    Manager = NewObject<ULearningAgentsManager>(this);
    for (int32 i = 0; i < Count; ++i)
    {
        APawn* Pawn = GetWorld()->SpawnActor<APawn>(
            AgentPawnClass, FVector(0, i * 200.f, 50.f), FRotator::ZeroRotator);
        Manager->AddAgent(Pawn);
    }

    // 2) Interactor + Policy (needed in every mode).
    Interactor = ULearningAgentsInteractor::MakeInteractor<UMoveInteractor>(Manager);
    Policy     = ULearningAgentsPolicy::MakePolicy(Manager, Interactor, {});

    switch (Mode)
    {
    case ERollerMode::Train:
        Critic  = ULearningAgentsCritic::MakeCritic(Manager, Policy, {});
        Trainer = ULearningAgentsTrainer::MakeTrainer<UMoveTrainer>(
                      Manager, Interactor, Policy, Critic);
        Trainer->Goals = Interactor->Goals;
        break;

    case ERollerMode::Record:
        // YOU drive; the recorder captures observation/action pairs into `Recording`.
        Interactor->bUseHumanActions = true;
        Recorder = ULearningAgentsRecorder::MakeRecorder(Manager, Interactor, {});
        if (!Recording) Recording = NewObject<ULearningAgentsRecording>(this);
        break;

    case ERollerMode::Imitate:
        // Teach the policy to copy the recorded demonstrations (behavioral cloning).
        ImitationTrainer = ULearningAgentsImitationTrainer::MakeImitationTrainer(
                               Manager, Interactor, Policy);
        break;

    case ERollerMode::Inference:
    default:
        break;   // just run the trained Policy each tick
    }

    // 3) Input: + / - feedback (Train), WASD (Record), R to save the recording.
    if (APlayerController* PC = GetWorld()->GetFirstPlayerController())
    {
        EnableInput(PC);
        if (InputComponent)
        {
            InputComponent->BindKey(EKeys::Equals,   IE_Pressed, this, &ARollerManager::RewardPlus);
            InputComponent->BindKey(EKeys::Add,      IE_Pressed, this, &ARollerManager::RewardPlus);
            InputComponent->BindKey(EKeys::Hyphen,   IE_Pressed, this, &ARollerManager::RewardMinus);
            InputComponent->BindKey(EKeys::Subtract, IE_Pressed, this, &ARollerManager::RewardMinus);
            InputComponent->BindKey(EKeys::R,        IE_Pressed, this, &ARollerManager::ToggleRecording);
            InputComponent->BindAxisKey(EKeys::D, this, &ARollerManager::DriveX);
            InputComponent->BindAxisKey(EKeys::A, this, &ARollerManager::DriveX);   // scale -1 in project input
            InputComponent->BindAxisKey(EKeys::W, this, &ARollerManager::DriveY);
            InputComponent->BindAxisKey(EKeys::S, this, &ARollerManager::DriveY);
        }
    }
}

void ARollerManager::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    switch (Mode)
    {
    case ERollerMode::Train:
        if (Trainer) Trainer->RunTraining({}, {}, {});     // PPO + human feedback
        break;

    case ERollerMode::Record:
        // Feed the human's WASD into the interactor, step, and capture the experience.
        Interactor->HumanActions.Add(0, HumanDrive);
        Interactor->GatherObservations();
        Interactor->PerformActions();                      // applies the human action
        if (bRecording && Recorder) Recorder->AddExperience();
        break;

    case ERollerMode::Imitate:
        if (ImitationTrainer && Recording)
            ImitationTrainer->RunTraining(Recording, {}, {});   // behavioral cloning
        break;

    case ERollerMode::Inference:
    default:
        Interactor->GatherObservations();
        Policy->RunInference();
        break;
    }
}

// ---- Train-mode human feedback: press + / - to reward / punish every agent ---------
void ARollerManager::RewardPlus()  { ApplyHumanReward(+HumanRewardAmount); }
void ARollerManager::RewardMinus() { ApplyHumanReward(-HumanRewardAmount); }
void ARollerManager::ApplyHumanReward(float Amount)
{
    if (!Trainer) return;
    for (int32 i = 0; i < NumAgents; ++i)
        Trainer->HumanReward.FindOrAdd(i) += Amount;       // consumed in GatherAgentReward
    UE_LOG(LogTemp, Display, TEXT("[RollerBall] human feedback %+0.2f"), Amount);
}

// ---- Record-mode driving + saving the demonstration --------------------------------
void ARollerManager::DriveX(float V) { HumanDrive.X = V; }
void ARollerManager::DriveY(float V) { HumanDrive.Y = V; }

void ARollerManager::ToggleRecording()
{
    if (Mode != ERollerMode::Record || !Recorder) return;
    bRecording = !bRecording;
    if (bRecording)
    {
        Recorder->BeginRecording();
        UE_LOG(LogTemp, Display, TEXT("[RollerBall] RECORDING — drive with WASD."));
    }
    else
    {
        Recorder->EndRecording();          // writes into the `Recording` asset
        UE_LOG(LogTemp, Display, TEXT("[RollerBall] saved demonstration. Switch Mode=Imitate to train from it."));
    }
}
