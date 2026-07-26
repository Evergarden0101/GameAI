# Engine Integration · 引擎集成

How learned AI actually ships in a game: **train a model, then run it in the engine.**
The runnable samples in [`../samples`](../samples) teach the *algorithms* in Python;
this folder shows how the *learned* ones plug into real engines in their own languages.

游戏中的学习式 AI 是如何落地的：**先训练模型，再在引擎里运行它。**
[`../samples`](../samples) 用 Python 讲清*算法*；本目录展示学习式方法如何用引擎各自的
语言接入真实引擎。

> These are **reference snippets**, not runnable programs — they need Unity or Unreal.
> 这些是**参考代码片段**，并非可独立运行的程序——需要 Unity 或 Unreal。

## The core idea: the game is the environment · 核心思想：游戏即环境

Training an agent is a loop between an **agent** and an **environment** (your game):

训练一个智能体，是**智能体**与**环境**（你的游戏）之间的一个循环：

```
        ┌───────────── ENVIRONMENT (your game) ─────────────┐
   ┌───▶│  observation (state)          reward + done       │
   │    └──────────┬─────────────────────────▲──────────────┘
   │               ▼                          │
   │    ┌───────────── AGENT (the policy) ────┴──────────────┐
   └────┤  action = policy(observation)   learn from reward  │
        └───────────────────────────────────────────────────┘
```

The four things you must define — the **agent contract** — are the same in every
framework: **observations** (what it senses), **actions** (what it can do),
**reward** (what "good" means), and **reset** (start a new episode). Training runs
this millions of times; the policy (a neural network) gets better at maximizing
reward. Then you **freeze** the network and run only `observation → action` in the
shipping game.

你必须定义的四件事——**智能体契约**——在每个框架里都一样：**观测**（它感知什么）、
**动作**（它能做什么）、**奖励**（什么算好）、**重置**（开始新回合）。训练会跑上百万次，
策略（一个神经网络）越来越擅长最大化奖励。然后你**冻结**网络，在上线游戏里只运行
`观测 → 动作`。

## Unity vs. Unreal · Unity 与 Unreal 对比

| | **Unity — ML-Agents** | **Unreal — Learning Agents** |
|---|---|---|
| Language you write · 你写的语言 | C# agent + YAML config | C++ / Blueprint |
| Where training runs · 训练在哪 | **External Python** (PyTorch), over a socket | **In-engine** (C++ PPO), no Python |
| You write the training loop? · 要写训练循环吗 | No — configure in YAML | No — call `RunTraining()` |
| Run a model in-game · 游戏内运行模型 | **Sentis** (was Barracuda) | **NNE** (Neural Network Engine) |
| Run a Python-trained ONNX? · 跑 Python 训练的 ONNX | Yes, via Sentis | Yes, via NNE |
| Maturity · 成熟度 | Stable, widely used | Experimental (API changes) |

Both are now **complete projects**, not loose snippets:

- **Unity** → [`unity/`](unity/) — an **importable Unity project** (open in Unity Hub,
  press Play; the scene builds itself). RL agent + **live human feedback** + imitation +
  Sentis inference. See [its README](unity/README.md).
- **Unreal** → [`unreal/`](unreal/) — a **complete UE 5.4 C++ project scaffold**:
  Learning Agents in-engine training with **human feedback** + NNE inference. See
  [its README](unreal/README.md). *(Experimental plugin — needs UE + a compile.)*

## Three situations, all shown · 三种情形，均有示例

1. **Train an AI using a game environment** — the game feeds observations/rewards and
   the trainer improves the policy (Unity: Python over a socket; Unreal: the engine
   in-process). Unity `Assets/Scripts/RollerAgent.cs` + `config/roller_config.yaml`;
   Unreal `MoveInteractor` + `MoveTrainer` + `RollerManager`.
   **用游戏环境训练 AI**——游戏提供观测/奖励，训练器改进策略。

2. **Human feedback during training (human-in-the-loop)** — while it trains, press
   **`+` / `-`** to reward/punish the agent live; those presses fold into the same
   reward PPO optimizes (a TAMER / RLHF-style loop). Unity `HumanFeedback.cs`; Unreal
   `RollerManager` + `MoveTrainer::GatherAgentReward`. Imitation from recorded demos is
   also shown (Unity `roller_imitation_config.yaml`, BC + GAIL).
   **训练中的人类反馈（人在回路）**——训练时按 `+` / `-` 实时奖惩，直接塑造策略；另含从
   人类演示中模仿学习。

3. **Use a trained model during the game (inference in C++/C#)** — freeze the network
   and run fast forward passes each tick, no training, no Python. Unity
   `SentisInference.cs` (or assign the `.onnx` and set *Inference Only*); Unreal
   `NNEInference.cpp`.
   **游戏中使用训练好的模型（C++/C# 推理）**——冻结网络，每帧前向推理，无需训练与 Python。

> See **Appendix A** of the [book](../docs/game-ai-book.en.md)
> ([中文](../docs/game-ai-book.zh.md)) for the narrative version.
> 叙述版见[教程书](../docs/game-ai-book.zh.md)**附录 A**。
