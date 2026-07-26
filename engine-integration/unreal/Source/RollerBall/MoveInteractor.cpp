// MoveInteractor.cpp — see header caveat (experimental API; illustrative shapes).
#include "MoveInteractor.h"
#include "LearningAgentsObservations.h"
#include "LearningAgentsActions.h"
#include "GameFramework/Pawn.h"

void UMoveInteractor::SpecifyAgentObservation_Implementation(
    FLearningAgentsObservationSchemaElement& OutObservation,
    ULearningAgentsObservationSchema* Schema)
{
    // 8 floats: goal(x,y), me(x,y), velocity(x,y) + padding — normalized positions.
    OutObservation = ULearningAgentsObservations::SpecifyFloatArrayObservation(Schema, 6);
}

void UMoveInteractor::GatherAgentObservation_Implementation(
    FLearningAgentsObservationObjectElement& OutObservation,
    ULearningAgentsObservationObject* Object,
    const int32 AgentId)
{
    const APawn* Pawn = Cast<APawn>(GetAgent(AgentId));
    const FVector Me   = Pawn ? Pawn->GetActorLocation() : FVector::ZeroVector;
    const FVector Vel  = Pawn ? Pawn->GetVelocity() : FVector::ZeroVector;
    const FVector Goal = Goals.FindRef(AgentId);
    const float S = 0.001f;   // scale world cm -> small numbers for the network

    TArray<float> Obs = {
        (Goal.X - Me.X) * S, (Goal.Y - Me.Y) * S,   // vector to goal
        Me.X * S,            Me.Y * S,               // where I am
        Vel.X * S,           Vel.Y * S               // how I'm moving
    };
    OutObservation = ULearningAgentsObservations::MakeFloatArrayObservation(Object, Obs);
}

void UMoveInteractor::SpecifyAgentAction_Implementation(
    FLearningAgentsActionSchemaElement& OutAction,
    ULearningAgentsActionSchema* Schema)
{
    // A 2-D move direction, each component in [-1, 1].
    OutAction = ULearningAgentsActions::SpecifyFloatArrayAction(Schema, 2);
}

void UMoveInteractor::PerformAgentAction_Implementation(
    const ULearningAgentsActionObject* Object,
    const FLearningAgentsActionObjectElement& Action,
    const int32 AgentId)
{
    TArray<float> Values;
    ULearningAgentsActions::GetFloatArrayAction(Values, Object, Action);
    if (APawn* Pawn = Cast<APawn>(GetAgent(AgentId)))
    {
        const FVector Dir(Values.IsValidIndex(0) ? Values[0] : 0.f,
                          Values.IsValidIndex(1) ? Values[1] : 0.f, 0.f);
        Pawn->AddMovementInput(Dir, 1.f);       // or add force to a physics ball
    }
}
