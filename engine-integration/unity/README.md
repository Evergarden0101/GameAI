# RollerBall — a complete, importable Unity ML-Agents project

A ball learns (with reinforcement learning) to roll to a target without falling off a
platform — and **you can shape its learning live with keyboard feedback**. The whole
environment builds itself from code on Play, so there is no scene to wire up.

**Targets:** Unity **6 (6000.x)** + `com.unity.ml-agents` **3.0** (which pulls in
Unity **Sentis**). On Unity 2022.3 + Barracuda, change `ModelAsset` → `NNModel` and the
Sentis calls in `SentisInference.cs`/`EnvironmentBuilder.cs`.

## What's here

```
unity/
├── Packages/manifest.json          ← declares the ML-Agents package (auto-resolves)
├── ProjectSettings/ProjectVersion.txt
├── Assets/Scripts/
│   ├── RollerAgent.cs              ← the agent contract (obs / action / reward / reset)
│   ├── EnvironmentBuilder.cs       ← builds camera+floor+agent+target on Play
│   ├── HumanFeedback.cs            ← press + / - to shape learning during training
│   └── SentisInference.cs          ← run a trained .onnx in pure C#
└── config/
    ├── roller_config.yaml          ← PPO (pure RL)
    └── roller_imitation_config.yaml← BC + GAIL (learn from your demonstrations)
```

## 1. Open it

Open this `unity/` folder with **Unity Hub → Add → project**. Unity resolves the
packages on first open (needs internet). If package resolution fails for your version,
open **Window → Package Manager → + → Add package by name → `com.unity.ml-agents`** and
follow the [official install guide](https://unity-technologies.github.io/ml-agents/Installation/).

Press **Play** — `EnvironmentBuilder` constructs the scene and the ball starts moving
(random until trained). No scene setup required.

## 2. Train with reinforcement learning + live human feedback

```bash
python -m venv venv && source venv/bin/activate     # (Windows: venv\Scripts\activate)
pip install mlagents
mlagents-learn config/roller_config.yaml --run-id=roller01
# When it prints "Start training by pressing Play", press Play in the Editor.
```

**Human-in-the-loop (Situation A):** while it trains, watch the ball and press —

| key | effect |
|---|---|
| **`+`** or **`]`** | reward the agent (good behaviour) |
| **`-`** or **`[`** | punish the agent (bad behaviour) |
| **`H`** | toggle human feedback on/off |

Those presses call `AddReward()` on the **same signal PPO optimizes**, so your feedback
directly shapes the learned policy (a simple TAMER / RLHF-style loop). Watch progress in
TensorBoard: `tensorboard --logdir results`.

## 3. Or learn from your demonstrations (imitation)

The other way to inject human input into training:

1. Select the agent at Play-time (or add it in `EnvironmentBuilder`), add a
   **Demonstration Recorder** component, tick **Record**, set a name, set **Behavior
   Type = Heuristic Only**, press Play and drive with **WASD**.
2. It saves `Assets/Demonstrations/RollerBall.demo`.
3. Train with `config/roller_imitation_config.yaml` (adds **Behavioral Cloning + GAIL**):
   `mlagents-learn config/roller_imitation_config.yaml --run-id=roller_imit01`.

## 4. Run the trained model in-game (inference, no Python)

Training writes `results/<run-id>/RollerBall.onnx`. Two ways to use it:

- **Automatic:** drop the `.onnx` into `Assets/Resources/RollerBall.onnx`.
  `EnvironmentBuilder` loads it and switches to **Inference Only** — the same agent now
  runs the network via **Sentis**, no Python.
- **Manual:** load it yourself with `SentisInference.cs` and call `Decide(obs)` — this is
  also how you run a model trained in plain PyTorch (exported to ONNX).
