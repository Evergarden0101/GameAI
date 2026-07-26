# Unity ML-Agents — train in the game, run in the game

Unity's [ML-Agents Toolkit](https://github.com/Unity-Technologies/ml-agents) is the
standard way to train reinforcement-learning / imitation agents **inside a Unity
game** and then ship them. It has two halves:

- **C# runtime** (`com.unity.ml-agents`) — lives in your game. You write an `Agent`
  subclass that defines observations, actions, and rewards.
- **Python trainer** (`pip install mlagents`, PyTorch under the hood) — used **only
  while training**. You never write the training loop; you configure it in YAML.

## The training loop (the game *is* the environment)

```
   ┌──────────────────────── Unity (C#) ────────────────────────┐
   │  Agent.CollectObservations()  ── state vector ─┐           │
   │  Agent.OnActionReceived(a)  ◄── actions ──┐     │           │
   │  physics steps · AddReward() ── reward ──┐ │     │           │
   └──────────────────────────────────────────┼─┼─────┼──────────┘
              socket (gRPC)                    │ │     │
   ┌──────────────────────── Python ───────────┼─┼─────┼──────────┐
   │  PPO / SAC (PyTorch):  policy(state) ──────┘ │     │           │
   │  collect (state, action, reward) ────────────┘     │           │
   │  update the neural network ────────────────────────┘           │
   │  ... repeated over MANY parallel envs, millions of steps ...    │
   │  => exports  results/roller01/RollerBall.onnx                   │
   └────────────────────────────────────────────────────────────────┘
```

**Files here:** [`RollerAgent.cs`](RollerAgent.cs) (the agent contract) ·
[`roller_config.yaml`](roller_config.yaml) (PPO hyperparameters).

**Steps:**

```bash
pip install mlagents
mlagents-learn roller_config.yaml --run-id=roller01
# When the console says "Start training by pressing Play", press Play in the Editor.
# Watch it in TensorBoard:  tensorboard --logdir results
```

## Running the trained model in-game (inference)

Two ways — both are **C# only, no Python at runtime**:

1. **Let ML-Agents do it (easiest).** Drag `RollerBall.onnx` onto the agent's
   **Behavior Parameters → Model** slot and set **Behavior Type = Inference Only**.
   The *same* `RollerAgent.cs` now runs — ML-Agents feeds your `CollectObservations`
   into the network (via **Unity Sentis**) and calls `OnActionReceived` with the
   result, every `DecisionRequester` tick.

2. **Run the network yourself.** Load the `.onnx` with **Sentis** and do the forward
   pass in your own code — see [`SentisInference.cs`](SentisInference.cs). This is
   also how you run a model that was **trained in Python** (PyTorch → ONNX) with no
   ML-Agents at all.

> At runtime the "AI" is just a fast matrix multiply on the observation vector. All
> the learning happened offline during training.
