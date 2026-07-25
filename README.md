# GameAI

A bilingual (English / 中文) introduction to **Game AI** — the classic and
modern techniques that make game characters move, fight, chase, race, talk, and
learn — with a **runnable code sample for every genre**.

游戏 AI 的中英双语导引：让游戏角色移动、战斗、追击、竞速、对话与学习的经典与现代
技术，**每种类型都配有可直接运行的示例代码**。

---

## 📖 The guide · 指南

| | |
|---|---|
| **English** | [`docs/game-ai-guide.en.md`](docs/game-ai-guide.en.md) |
| **中文** | [`docs/game-ai-guide.zh.md`](docs/game-ai-guide.zh.md) |

The guide covers what game AI really is (and how it differs from academic AI),
then walks the full landscape: **NPCs, cluster/swarm enemies, follow/chase
enemies, car racing AI, reinforcement-learning agents, and generative (LLM)
agents** — each with concrete shipped-game examples, usage, and limitations.

指南先讲清游戏 AI 究竟是什么（以及它与学术 AI 的区别），再纵览全景：**NPC、
集群敌人、追踪敌人、赛车 AI、强化学习智能体、生成式（LLM）智能体**——每一种都
配有真实游戏案例、用途与局限。

## 💻 The samples · 示例代码

Six self-contained programs in [`samples/`](samples) — five run on the Python
standard library alone; the generative NPC optionally uses the Anthropic SDK and
otherwise falls back to an offline mock.

[`samples/`](samples) 中有六个自包含程序——其中五个仅用 Python 标准库即可运行；
生成式 NPC 可选使用 Anthropic SDK，否则回退到离线模拟。

| Genre · 类型 | Technique · 技术 | Sample · 示例 |
|--------------|------------------|---------------|
| 🏎️ Car racing AI · 赛车 AI | Waypoints + PID + rubber-banding · 路点 + PID + 橡皮筋 | [`samples/racing/racing_ai.py`](samples/racing/racing_ai.py) |
| 🛡️ NPC · 非玩家角色 | Finite state machine + behavior tree · 状态机 + 行为树 | [`samples/npc/npc_fsm.py`](samples/npc/npc_fsm.py) |
| 🦇 Cluster enemy · 集群敌人 | Boids flocking · Boids 集群 | [`samples/flocking/flocking.py`](samples/flocking/flocking.py) |
| 👣 Follow enemy · 追踪敌人 | A\* pathfinding · A\* 寻路 | [`samples/follow/pathfinding_astar.py`](samples/follow/pathfinding_astar.py) |
| 🧠 RL agent · 强化学习智能体 | Tabular Q-learning · 表格型 Q-learning | [`samples/rl/q_learning.py`](samples/rl/q_learning.py) |
| 💬 Generative agent · 生成式智能体 | LLM NPC + tool use · LLM NPC + 工具调用 | [`samples/generative/generative_npc.py`](samples/generative/generative_npc.py) |

### Quick start · 快速开始

```bash
# Samples 1–5 need nothing but Python 3.8+  ·  示例 1–5 仅需 Python 3.8+
python samples/racing/racing_ai.py
python samples/npc/npc_fsm.py
python samples/flocking/flocking.py
python samples/follow/pathfinding_astar.py
python samples/rl/q_learning.py

# Generative NPC: runs an offline mock as-is, or connect a live LLM:
# 生成式 NPC：直接运行离线模拟，或接入实时 LLM：
pip install -r samples/requirements.txt
export ANTHROPIC_API_KEY=sk-...      # or: ant auth login
python samples/generative/generative_npc.py
```

See [`samples/README.md`](samples/README.md) for details.
详见 [`samples/README.md`](samples/README.md)。

## 🗂️ Repository layout · 目录结构

```
GameAI/
├── README.md                     ← you are here · 你在这里
├── docs/
│   ├── game-ai-guide.en.md       ← full guide (English)
│   └── game-ai-guide.zh.md       ← 完整指南（中文）
└── samples/
    ├── README.md
    ├── requirements.txt
    ├── racing/racing_ai.py            # car racing AI
    ├── npc/npc_fsm.py                 # NPC state machine + behavior tree
    ├── flocking/flocking.py           # cluster / swarm enemies (Boids)
    ├── follow/pathfinding_astar.py    # follow / chase enemies (A*)
    ├── rl/q_learning.py               # reinforcement-learning agent
    └── generative/generative_npc.py   # generative LLM agent
```

## License · 许可

Provided as educational sample code. Use freely.
仅作教学示例代码，可自由使用。
