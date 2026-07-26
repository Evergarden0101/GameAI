// EnvironmentBuilder.cs — builds the whole scene from code at Play (no manual wiring)
// -----------------------------------------------------------------------------------
// This is what makes the project "just press Play": a [RuntimeInitializeOnLoadMethod]
// runs automatically when the game starts (in ANY scene, even an empty one) and
// constructs the camera, light, floor, target, and the agent with all its ML-Agents
// components already configured. So you never have to build a scene by hand.
//
// Targets Unity 6 (6000.x) + com.unity.ml-agents 3.0 (which pulls in Unity Sentis).
// On older setups (2022.3 + Barracuda) change ModelAsset -> NNModel below.

using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Policies;
using UnityEngine;

public static class EnvironmentBuilder
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void Build()
    {
        // Don't rebuild if a scene already contains an agent (e.g. you made your own).
        if (Object.FindObjectOfType<RollerAgent>() != null) return;

        // ---- camera ----
        var camGO = new GameObject("Main Camera");
        var cam = camGO.AddComponent<Camera>();
        camGO.tag = "MainCamera";
        cam.clearFlags = CameraClearFlags.SolidColor;
        cam.backgroundColor = new Color(0.05f, 0.07f, 0.10f);
        camGO.transform.SetPositionAndRotation(new Vector3(0f, 13f, -13f),
                                               Quaternion.Euler(45f, 0f, 0f));

        // ---- light ----
        var lightGO = new GameObject("Directional Light");
        var light = lightGO.AddComponent<Light>();
        light.type = LightType.Directional;
        lightGO.transform.rotation = Quaternion.Euler(50f, -30f, 0f);

        // ---- floor (Plane is 10x10 units, top at y=0) ----
        var floor = GameObject.CreatePrimitive(PrimitiveType.Plane);
        floor.name = "Floor";
        Tint(floor, new Color(0.12f, 0.16f, 0.22f));

        // ---- target ----
        var target = GameObject.CreatePrimitive(PrimitiveType.Cube);
        target.name = "Target";
        target.transform.localPosition = new Vector3(3f, 0.5f, 3f);
        Object.Destroy(target.GetComponent<Collider>());     // purely visual
        Tint(target, new Color(0.20f, 0.85f, 0.45f));

        // ---- agent ----
        var agentGO = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        agentGO.name = "RollerAgent";
        agentGO.transform.localPosition = new Vector3(0f, 0.5f, 0f);
        Tint(agentGO, new Color(0.22f, 0.60f, 1f));
        agentGO.AddComponent<Rigidbody>();

        // ML-Agents "brain wiring", normally done on the Behavior Parameters inspector:
        var bp = agentGO.AddComponent<BehaviorParameters>();
        bp.BehaviorName = "RollerBall";                      // must match config + demos
        bp.BrainParameters.VectorObservationSize = 8;
        bp.BrainParameters.ActionSpec = ActionSpec.MakeContinuous(2);

        // INFERENCE: if a trained model is dropped in Assets/Resources/RollerBall.onnx,
        // load it and switch to inference-only (no Python). Otherwise stays "Default"
        // so it connects to the trainer, or falls back to Heuristic.
        var model = Resources.Load<Unity.Sentis.ModelAsset>("RollerBall");
        if (model != null)
        {
            bp.Model = model;
            bp.BehaviorType = BehaviorType.InferenceOnly;
            Debug.Log("[RollerBall] Loaded trained model — running inference.");
        }

        var agent = agentGO.AddComponent<RollerAgent>();
        agent.target = target.transform;

        var dr = agentGO.AddComponent<DecisionRequester>();
        dr.DecisionPeriod = 5;

        // HUMAN FEEDBACK during training (see HumanFeedback.cs).
        agentGO.AddComponent<HumanFeedback>().agent = agent;
    }

    static void Tint(GameObject go, Color c)
    {
        var r = go.GetComponent<Renderer>();
        if (r != null) r.material.color = c;
    }
}
