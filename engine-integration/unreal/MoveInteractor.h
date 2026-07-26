// MoveInteractor.h — Unreal Learning Agents "Interactor": what the agent SENSES and DOES
// --------------------------------------------------------------------------------------
// ILLUSTRATIVE SKELETON. Learning Agents is experimental; method signatures vary by UE
// version — treat this as the SHAPE, not copy-paste-compileable code. See the Learning
// Agents docs for your engine version.
//
// The Interactor is the Unreal counterpart of Unity's CollectObservations() +
// OnActionReceived(): one class defines the observation schema (what the policy reads)
// and the action schema (what the policy outputs), plus how to gather/apply them.

#pragma once

#include "LearningAgentsInteractor.h"
#include "MoveInteractor.generated.h"

UCLASS()
class UMoveInteractor : public ULearningAgentsInteractor
{
    GENERATED_BODY()

public:
    // ---- OBSERVATIONS: describe, then fill, the state vector ----------------------

    // Declare the structure of what the agent senses (once).
    virtual void SpecifyAgentObservation_Implementation(
        FLearningAgentsObservationSchemaElement& OutObservation,
        ULearningAgentsObservationSchema* Schema) override;

    // Fill it in for a specific agent, every step (its location + the goal's location).
    virtual void GatherAgentObservation_Implementation(
        FLearningAgentsObservationObjectElement& OutObservation,
        ULearningAgentsObservationObject* Object,
        const int32 AgentId) override;

    // ---- ACTIONS: describe, then apply, the action vector -------------------------

    // Declare the structure of what the agent can do (e.g. a 2D move direction).
    virtual void SpecifyAgentAction_Implementation(
        FLearningAgentsActionSchemaElement& OutAction,
        ULearningAgentsActionSchema* Schema) override;

    // Apply the policy's chosen action to the pawn, every step.
    virtual void PerformAgentAction_Implementation(
        const ULearningAgentsActionObject* Object,
        const FLearningAgentsActionObjectElement& Action,
        const int32 AgentId) override;
};
