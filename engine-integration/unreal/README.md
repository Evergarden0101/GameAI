# Unreal Engine — Learning Agents (train) & NNE (inference)

Unreal takes a different path from Unity. Its two relevant systems:

- **Learning Agents** (experimental plugin, UE 5.1+; matured through 5.3–5.5) —
  trains RL / imitation agents **inside the engine**. Unlike Unity ML-Agents, there
  is **no external Python trainer**: the PPO implementation runs in C++ inside UE,
  usually with the game sped up and many agents in parallel. You write C++ (or
  Blueprint) subclasses that define observations, actions, rewards, and resets.
- **NNE — Neural Network Engine** (UE 5.x) — the general runtime for loading and
  running a trained network (e.g. an **ONNX** model trained in PyTorch) during the
  game. This is Unreal's analog of Unity Sentis.

> ⚠️ **Version caveat.** Learning Agents is **experimental** and its API has changed
> significantly between UE versions. The code here is an **illustrative skeleton** to
> show the *shape* of the system — the exact class/method signatures depend on your
> UE version. Always check the official
> [Learning Agents docs](https://dev.epicgames.com/community/learning/tutorials/8OWY/unreal-engine-learning-agents-introduction)
> and [NNE docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/neural-network-engine-nne-in-unreal-engine)
> for your engine version.

## The training loop (all inside the UE tick — no Python)

```
   ┌──────────────── Unreal Engine tick (C++) ─────────────────┐
   │  Interactor.GatherObservations()  ── state ─┐             │
   │  Policy (neural net) . RunTraining() ◄───────┘             │
   │  Interactor.PerformActions(actions) ── act on pawns        │
   │  Trainer.GatherRewards() / GatherCompletions() ── r, done  │
   │  Trainer.ProcessExperience() ── PPO update (in-engine)     │
   │  ... run at high sim speed, many agents ...  => network asset
   └────────────────────────────────────────────────────────────┘
```

At inference time you drop the `Trainer` and just run `Interactor + Policy` (the
network) every tick — or load an ONNX model with **NNE** and run it yourself.

## Files here

- [`MoveInteractor.h`](MoveInteractor.h) — defines the agent's **observations** and
  **actions** (what it senses and what it can do).
- [`MoveTrainer.h`](MoveTrainer.h) — defines the **reward** and **episode
  completion** (what "good" means and when a run ends).
- [`LearningAgentsSetup.cpp`](LearningAgentsSetup.cpp) — wires up the Manager,
  Interactor, Policy, and Trainer and drives the per-tick train/inference loop.
- [`NNEInference.cpp`](NNEInference.cpp) — loads and runs an ONNX model at runtime
  with NNE (the "use a Python-trained model in Unreal" path).
