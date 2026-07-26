# RollerBall — Unreal Learning Agents project (with human feedback) + NNE inference

A C++ Unreal project that trains an RL agent **in-engine** (no external Python) with
**live human feedback**, and shows how to run a trained ONNX model with **NNE**.

> ⚠️ **Experimental & version-sensitive.** Unreal **Learning Agents** is an experimental
> plugin whose API has changed significantly across UE 5.1–5.5. This project targets
> **UE 5.4** and is a **complete, correctly-structured scaffold** — but unlike the Unity
> project it is *not* "double-click and run": you need UE 5.4+ installed, the plugins
> enabled, and a C++ compile, and some Learning Agents calls may need adjusting to your
> exact engine version. Always cross-check the
> [Learning Agents docs](https://dev.epicgames.com/community/learning/tutorials/8OWY/unreal-engine-learning-agents-introduction)
> and [NNE docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/neural-network-engine-nne-in-unreal-engine).

## What's here

```
unreal/
├── RollerBall.uproject             ← enables the LearningAgents + NNE plugins
├── Config/                         ← DefaultEngine.ini, DefaultGame.ini
└── Source/
    ├── RollerBall.Target.cs · RollerBallEditor.Target.cs
    └── RollerBall/
        ├── RollerBall.Build.cs     ← deps: LearningAgents(+Training), NNE
        ├── RollerBall.h/.cpp        ← module
        ├── MoveInteractor.h/.cpp    ← OBSERVATIONS + ACTIONS
        ├── MoveTrainer.h/.cpp       ← REWARD (incl. human feedback) + completion
        ├── RollerManager.h/.cpp     ← setup, the train/infer Tick, and key input
        └── NNEInference.h/.cpp      ← run a trained ONNX model at runtime
```

## Build & run

1. Install **Unreal Engine 5.4+**. Right-click `RollerBall.uproject` → **Generate
   Visual Studio project files**, then open and **build** (or open the `.uproject` and
   let it compile).
2. In **Edit → Plugins**, confirm **Learning Agents** and **NNE / NNERuntimeORT** are
   enabled (the `.uproject` requests them).
3. Drop an **`ARollerManager`** actor into a level (a simple plane with some spawned
   pawns) and pick a **`Mode`** on it: `Train`, `Record`, `Imitate`, or `Inference`.
   Press **Play**.

## Human feedback during training (`Mode = Train`)

While training runs, press —

| key | effect |
|---|---|
| **`+`** (or numpad `+`) | reward every agent now |
| **`-`** (or numpad `-`) | punish every agent now |

`RollerManager` captures the key and adds to `Trainer->HumanReward`;
`UMoveTrainer::GatherAgentReward` folds that into the reward PPO optimizes and consumes
it — so your feedback directly shapes the learned policy (the same human-in-the-loop
idea as the Unity project).

## Record demonstrations, then imitate (`Mode = Record` → `Mode = Imitate`)

The other way to inject human input — the Unreal counterpart of the Unity demo recorder:

1. **Record.** Set `Mode = Record`, press **Play**. One agent spawns; **drive it with
   WASD**. Press **`R`** to start capturing and **`R`** again to stop — `RollerManager`
   drives the recorder (`BeginRecording` / `AddExperience` each tick / `EndRecording`)
   and stores a **`ULearningAgentsRecording`**. Your WASD becomes the performed action
   via `MoveInteractor.bUseHumanActions`, so the recording is genuinely your play.
2. **Imitate.** Set `Mode = Imitate` (with the recording assigned), press **Play**. A
   **`ULearningAgentsImitationTrainer`** teaches the policy to copy your demonstrations
   (behavioral cloning). Then switch to `Mode = Inference` to run the result.

## Inference (ship the trained brain)

Set `bTraining = false`: the manager drops the trainer and runs just
`Interactor + Policy` each tick. To instead run a model trained elsewhere (PyTorch →
ONNX), use `FBrain` in `NNEInference.cpp` — load the `.onnx` and call `Decide(obs, act)`.
