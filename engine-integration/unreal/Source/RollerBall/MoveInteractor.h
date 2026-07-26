// MoveInteractor.h — Learning Agents Interactor: the agent's OBSERVATIONS and ACTIONS
// -----------------------------------------------------------------------------------
// ⚠️ Learning Agents is EXPERIMENTAL; exact signatures/helpers vary by UE version.
// Treat this as the shape. The Interactor is the Unreal analog of Unity's
// CollectObservations() + OnActionReceived().

#pragma once

#include "CoreMinimal.h"
#include "LearningAgentsInteractor.h"
#include "MoveInteractor.generated.h"

UCLASS()
class ROLLERBALL_API UMoveInteractor : public ULearningAgentsInteractor
{
    GENERATED_BODY()

public:
    // Declare the observation vector (agent location + velocity + goal location).
    virtual void SpecifyAgentObservation_Implementation(
        FLearningAgentsObservationSchemaElement& OutObservation,
        ULearningAgentsObservationSchema* Schema) override;

    // Fill the observation for one agent each step.
    virtual void GatherAgentObservation_Implementation(
        FLearningAgentsObservationObjectElement& OutObservation,
        ULearningAgentsObservationObject* Object,
        const int32 AgentId) override;

    // Declare a 2-D continuous move action.
    virtual void SpecifyAgentAction_Implementation(
        FLearningAgentsActionSchemaElement& OutAction,
        ULearningAgentsActionSchema* Schema) override;

    // Apply the chosen action to the agent pawn each step.
    virtual void PerformAgentAction_Implementation(
        const ULearningAgentsActionObject* Object,
        const FLearningAgentsActionObjectElement& Action,
        const int32 AgentId) override;

    // The goal each agent is trying to reach (set by RollerManager).
    UPROPERTY() TMap<int32, FVector> Goals;

    // RECORD MODE: when true, PerformAgentAction applies the human's action
    // (from RollerManager's WASD input) instead of the policy's, so the recorder
    // captures human demonstrations.
    UPROPERTY() bool bUseHumanActions = false;
    UPROPERTY() TMap<int32, FVector2D> HumanActions;
};
