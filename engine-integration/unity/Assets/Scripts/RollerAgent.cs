// RollerAgent.cs — the ML-Agents agent contract (used for training AND inference)
// -------------------------------------------------------------------------------
// A ball learns to roll to a target without falling off a platform. This one class
// defines the whole agent contract that training (external Python/PyTorch) and
// in-game inference (Unity Sentis) both drive:
//   OnEpisodeBegin()      -> RESET the world for a new episode
//   CollectObservations() -> OBSERVATION: what the agent senses (8 numbers)
//   OnActionReceived()    -> ACTION: apply the policy's choice, then give REWARD
//   Heuristic()           -> let a human drive with WASD (to test / record demos)
//
// The environment (camera, floor, this agent, its components, the target) is built
// automatically at Play by EnvironmentBuilder — you do not need to wire a scene.

using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine;

public class RollerAgent : Agent
{
    [HideInInspector] public Transform target;   // assigned by EnvironmentBuilder
    Rigidbody rb;

    public override void Initialize()
    {
        rb = GetComponent<Rigidbody>();
    }

    public override void OnEpisodeBegin()
    {
        if (transform.localPosition.y < 0f)       // we fell off — reset position
        {
            rb.angularVelocity = Vector3.zero;
            rb.velocity = Vector3.zero;
            transform.localPosition = new Vector3(0f, 0.5f, 0f);
        }
        // New random goal each episode so the policy must generalize.
        target.localPosition = new Vector3(Random.value * 8f - 4f, 0.5f,
                                           Random.value * 8f - 4f);
    }

    public override void CollectObservations(VectorSensor sensor)
    {
        sensor.AddObservation(target.localPosition);      // 3
        sensor.AddObservation(transform.localPosition);   // 3
        sensor.AddObservation(rb.velocity.x);             // 1
        sensor.AddObservation(rb.velocity.z);             // 1  -> 8 total
    }

    public override void OnActionReceived(ActionBuffers actions)
    {
        Vector3 force = new Vector3(actions.ContinuousActions[0], 0f,
                                    actions.ContinuousActions[1]);
        rb.AddForce(force * 10f);

        float dist = Vector3.Distance(transform.localPosition, target.localPosition);
        if (dist < 1.42f) { AddReward(1.0f); EndEpisode(); }          // reached goal
        else if (transform.localPosition.y < 0f) { EndEpisode(); }    // fell off
        else { AddReward(-0.001f); }                                  // be quick
    }

    // Keyboard control: used with Behavior Type = "Heuristic Only" to test the scene
    // and to RECORD HUMAN DEMONSTRATIONS for imitation learning (see README).
    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var c = actionsOut.ContinuousActions;
        c[0] = Input.GetAxis("Horizontal");
        c[1] = Input.GetAxis("Vertical");
    }
}
