// RollerAgent.cs — Unity ML-Agents agent (training AND inference use this same class)
// ---------------------------------------------------------------------------------
// This is the canonical "RollerBall" task: a ball learns to roll to a target on a
// platform without falling off. It shows the FULL agent contract that both training
// (external Python/PyTorch) and in-game inference (Unity Sentis) drive:
//
//   OnEpisodeBegin()      -> reset the world for a new episode
//   CollectObservations() -> what the agent SENSES (the state vector)
//   OnActionReceived()    -> apply the ACTIONS the policy chose, then give REWARD
//   Heuristic()           -> let a human drive with the keyboard (for testing)
//
// The SAME script runs in two modes, chosen on the Behavior Parameters component:
//   * Behavior Type = Default  + no model  -> talks to the Python trainer (LEARN)
//   * Behavior Type = Inference Only + .onnx model -> Sentis runs the net (PLAY)
//
// Requires the "com.unity.ml-agents" package. Attach this to a Rigidbody GameObject,
// add a Behavior Parameters component (Vector Obs = 8, Continuous Actions = 2) and a
// Decision Requester component.

using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine;

public class RollerAgent : Agent
{
    public Transform target;      // assigned in the Inspector
    Rigidbody rb;

    // Called once when the agent is enabled.
    public override void Initialize()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Called at the start of every training/inference episode: reset the scene.
    public override void OnEpisodeBegin()
    {
        // If we fell off, put us back and kill momentum.
        if (transform.localPosition.y < 0f)
        {
            rb.angularVelocity = Vector3.zero;
            rb.velocity = Vector3.zero;
            transform.localPosition = new Vector3(0f, 0.5f, 0f);
        }
        // Move the target to a new random spot so the agent must generalize.
        target.localPosition = new Vector3(Random.value * 8f - 4f, 0.5f,
                                           Random.value * 8f - 4f);
    }

    // The agent's SENSES: everything it is allowed to know, packed into a vector.
    // Keep this to only fair, observable information (8 numbers here).
    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.localPosition);      // 3: where the goal is
        sensor.AddObservation(transform.localPosition);   // 3: where I am
        sensor.AddObservation(rb.velocity.x);             // 1: how fast I'm moving
        sensor.AddObservation(rb.velocity.z);             // 1
    }

    // The policy's DECISION arrives here as an action vector; we apply it, then we
    // shape the REWARD that teaches the policy what "good" means.
    public override void OnActionReceived(ActionBuffers actions)
    {
        // Two continuous actions in [-1, 1] -> a force on the ball.
        Vector3 force = new Vector3(actions.ContinuousActions[0], 0f,
                                    actions.ContinuousActions[1]);
        rb.AddForce(force * 10f);

        float dist = Vector3.Distance(transform.localPosition, target.localPosition);

        if (dist < 1.42f)             // reached the target
        {
            AddReward(1.0f);
            EndEpisode();
        }
        else if (transform.localPosition.y < 0f)   // fell off the platform
        {
            EndEpisode();             // no reward -> learns to avoid this
        }
        else
        {
            AddReward(-0.001f);       // tiny time penalty -> learns to be quick
        }
    }

    // Optional: lets you drive with WASD to test the scene before/without training.
    // In "Heuristic Only" behavior type this replaces the neural network.
    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var c = actionsOut.ContinuousActions;
        c[0] = Input.GetAxis("Horizontal");
        c[1] = Input.GetAxis("Vertical");
    }
}
