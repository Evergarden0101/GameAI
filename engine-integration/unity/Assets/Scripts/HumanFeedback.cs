// HumanFeedback.cs — HUMAN-IN-THE-LOOP reward shaping DURING training (Situation A)
// ---------------------------------------------------------------------------------
// While training runs, you watch the agent in the Editor and press keys to tell it
// "that was good" or "that was bad". Those key presses add reward to the SAME signal
// PPO is optimizing, so your feedback literally shapes what the policy learns — a
// simple, interactive form of human-in-the-loop RL (the idea behind TAMER / RLHF).
//
//   +  (or  ] )  -> reward the agent      (good behaviour)
//   -  (or  [ )  -> punish the agent      (bad behaviour)
//   H            -> toggle human feedback on/off
//
// Because AddReward() accumulates into the agent's current step, your presses are
// folded into that step's reward and sent to the trainer with everything else.

using Unity.MLAgents;
using UnityEngine;

public class HumanFeedback : MonoBehaviour
{
    [HideInInspector] public Agent agent;         // set by EnvironmentBuilder
    public float rewardAmount = 0.5f;
    public bool active = true;

    float lastPulse;                               // for on-screen flash
    float sessionTotal;                            // total human reward given

    void Update()
    {
        if (agent == null) return;

        if (Input.GetKeyDown(KeyCode.H)) active = !active;
        if (!active) return;

        if (Input.GetKeyDown(KeyCode.Equals) || Input.GetKeyDown(KeyCode.RightBracket)
            || Input.GetKeyDown(KeyCode.KeypadPlus))
            Give(+rewardAmount);

        if (Input.GetKeyDown(KeyCode.Minus) || Input.GetKeyDown(KeyCode.LeftBracket)
            || Input.GetKeyDown(KeyCode.KeypadMinus))
            Give(-rewardAmount);
    }

    void Give(float amount)
    {
        agent.AddReward(amount);                   // <-- folds into PPO's reward signal
        sessionTotal += amount;
        lastPulse = Time.time;
    }

    // Simple in-game HUD so the feedback keys are discoverable while training.
    void OnGUI()
    {
        var style = new GUIStyle(GUI.skin.label) { fontSize = 14 };
        GUI.color = active ? Color.white : Color.gray;
        GUILayout.BeginArea(new Rect(12, 12, 420, 120));
        GUILayout.Label($"HUMAN FEEDBACK  [{(active ? "ON" : "OFF")}]  (H to toggle)", style);
        GUILayout.Label("  +  or  ]   reward good behaviour", style);
        GUILayout.Label("  -  or  [   punish bad behaviour", style);

        // flash the last feedback and show the running total
        if (Time.time - lastPulse < 0.4f)
        {
            GUI.color = sessionTotal >= 0 ? Color.green : Color.red;
            GUILayout.Label(sessionTotal >= 0 ? "  +REWARD" : "  -PENALTY", style);
        }
        GUI.color = Color.white;
        GUILayout.Label($"  session human reward: {sessionTotal:0.0}", style);
        GUILayout.EndArea();
    }
}
