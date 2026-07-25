# Game AI Samples · 游戏 AI 示例代码

Six runnable, self-contained programs — one per genre covered in the
[Game AI guide](../docs/game-ai-guide.en.md) ([中文](../docs/game-ai-guide.zh.md)).

六个可独立运行的示例程序，每个对应指南中的一个 AI 类型。

## Requirements · 环境要求

- **Python 3.8+**. Samples 1–5 use **only the standard library** — nothing to install.
  示例 1–5 仅用标准库，无需安装任何依赖。
- Sample 6 (generative NPC) optionally uses the Anthropic SDK; without it, it
  runs an **offline mock** automatically.
  示例 6 可选安装 Anthropic SDK；未安装时自动使用离线模拟。

```bash
# optional, only for the live LLM NPC:
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...      # or run: ant auth login
```

## The samples · 示例列表

| # | Genre · 类型 | File | Technique · 技术 | Run |
|---|--------------|------|------------------|-----|
| 1 | Car racing AI · 赛车 AI | [`racing/racing_ai.py`](racing/racing_ai.py) | Waypoint following, PID steering, rubber-banding · 路点跟随、PID 转向、橡皮筋难度 | `python racing/racing_ai.py` |
| 2 | NPC · 非玩家角色 | [`npc/npc_fsm.py`](npc/npc_fsm.py) | Finite state machine + behavior tree · 有限状态机 + 行为树 | `python npc/npc_fsm.py` |
| 3 | Cluster / swarm enemy · 集群敌人 | [`flocking/flocking.py`](flocking/flocking.py) | Boids flocking (separation / alignment / cohesion) · Boids 集群 | `python flocking/flocking.py` |
| 4 | Follow / chase enemy · 追踪敌人 | [`follow/pathfinding_astar.py`](follow/pathfinding_astar.py) | A\* pathfinding, re-planned each tick · A\* 寻路，逐帧重规划 | `python follow/pathfinding_astar.py` |
| 5 | RL agent · 强化学习智能体 | [`rl/q_learning.py`](rl/q_learning.py) | Tabular Q-learning grid world · 表格型 Q-learning | `python rl/q_learning.py` |
| 6 | Generative AI agent · 生成式 AI 智能体 | [`generative/generative_npc.py`](generative/generative_npc.py) | LLM-driven NPC with persona, memory & tool use · LLM 驱动的 NPC（人设 / 记忆 / 工具调用） | `python generative/generative_npc.py` |

## Run all at once · 一次运行全部

```bash
for f in racing/racing_ai.py npc/npc_fsm.py flocking/flocking.py \
         follow/pathfinding_astar.py rl/q_learning.py generative/generative_npc.py; do
  echo "=== $f ==="; python "$f"; echo
done
```

## Notes · 说明

- Each file is **independent** (no shared modules) so you can copy one out on its own.
  每个文件相互独立，可单独复制使用。
- The code favors clarity over performance — it is meant to be read and learned from.
  代码以清晰易懂为先，便于学习，而非追求性能。
- These are **classical, deterministic teaching implementations**. Production
  engines add spatial hashing, nav-meshes, steering-behavior blending, neural
  networks, etc. — see the guide for how each scales up.
  这些是经典的教学实现；实际引擎会加入空间哈希、导航网格、神经网络等，详见指南。
