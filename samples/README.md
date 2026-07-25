# Game AI Samples · 游戏 AI 示例代码

Fifteen runnable, self-contained programs — the hands-on companion to the
[Game AI book](../docs/game-ai-book.en.md) and the bilingual guides
([EN](../docs/game-ai-guide.en.md) · [中文](../docs/game-ai-guide.zh.md)).

十五个可独立运行的示例程序，是[《游戏 AI》教程书](../docs/game-ai-book.en.md)与
双语指南的动手实践部分。

## Requirements · 环境要求

- **Python 3.8+**. **Every sample except the generative NPC uses only the
  standard library** — nothing to install.
  除生成式 NPC 外，所有示例仅用 Python 标准库，无需安装依赖。
- The generative NPC optionally uses the Anthropic SDK; without it, it runs an
  **offline mock** automatically.
  生成式 NPC 可选安装 Anthropic SDK；未安装时自动使用离线模拟。

```bash
# optional, only for the live LLM NPC:
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...      # or run: ant auth login
```

## Tier 1 — Classic toolbox · 经典技术工具箱

| Genre / Technique · 类型 / 技术 | File | Run |
|---|---|---|
| NPC state machine + behavior tree · 状态机 + 行为树 | [`npc/npc_fsm.py`](npc/npc_fsm.py) | `python npc/npc_fsm.py` |
| Pac-Man ghost AI (4 personalities) · 吃豆人幽灵 AI（四性格） | [`classic/pacman_ghosts.py`](classic/pacman_ghosts.py) | `python classic/pacman_ghosts.py` |
| Cluster / swarm enemies — Boids · 集群敌人 | [`flocking/flocking.py`](flocking/flocking.py) | `python flocking/flocking.py` |
| Follow / chase — A\* pathfinding · 追踪寻路 | [`follow/pathfinding_astar.py`](follow/pathfinding_astar.py) | `python follow/pathfinding_astar.py` |
| GOAP planner (F.E.A.R.-style) · 目标导向规划 | [`classic/goap_planner.py`](classic/goap_planner.py) | `python classic/goap_planner.py` |
| Minimax + alpha-beta (unbeatable) · 极小化极大 + 剪枝 | [`classic/minimax_tictactoe.py`](classic/minimax_tictactoe.py) | `python classic/minimax_tictactoe.py` |
| Monte-Carlo Tree Search · 蒙特卡洛树搜索 | [`classic/mcts_connect_four.py`](classic/mcts_connect_four.py) | `python classic/mcts_connect_four.py` |

## Tier 2 — Genre deep-dives · 类型深入

| Genre · 类型 | File | Run |
|---|---|---|
| 🏎️ Car racing AI (waypoints/PID/rubber-band) · 赛车 AI | [`racing/racing_ai.py`](racing/racing_ai.py) | `python racing/racing_ai.py` |
| 🏁 Mario Kart items + catch-up · 马里奥卡丁车道具 | [`racing/mario_kart_items.py`](racing/mario_kart_items.py) | `python racing/mario_kart_items.py` |
| 🔫 FPS tactical squad (LOS / cover / suppress / flank) · 射击战术 | [`fps/tactical_fps.py`](fps/tactical_fps.py) | `python fps/tactical_fps.py` |
| ⚙️ RTS skirmish (C&C / Red Alert) · 即时战略 | [`rts/command_conquer_ai.py`](rts/command_conquer_ai.py) | `python rts/command_conquer_ai.py` |
| 🏛️ 4X empire (Civilization + difficulty bonuses) · 策略帝国 | [`strategy/civ_ai.py`](strategy/civ_ai.py) | `python strategy/civ_ai.py` |

## Tier 3 — Modern / learned AI · 现代 / 学习式 AI

| Genre · 类型 | File | Run |
|---|---|---|
| 🧠 RL agent — Q-learning maze · 强化学习（迷宫） | [`rl/q_learning.py`](rl/q_learning.py) | `python rl/q_learning.py` |
| 🏎️ RL racer — Sophy-style speed control · 学习竞速 | [`rl/sophy_racing_qlearn.py`](rl/sophy_racing_qlearn.py) | `python rl/sophy_racing_qlearn.py` |
| 💬 Generative LLM NPC + tool use · 生成式 NPC | [`generative/generative_npc.py`](generative/generative_npc.py) | `python generative/generative_npc.py` |

## Run them all · 一次运行全部

```bash
for f in npc/npc_fsm.py classic/pacman_ghosts.py flocking/flocking.py \
         follow/pathfinding_astar.py classic/goap_planner.py \
         classic/minimax_tictactoe.py classic/mcts_connect_four.py \
         racing/racing_ai.py racing/mario_kart_items.py fps/tactical_fps.py \
         rts/command_conquer_ai.py strategy/civ_ai.py \
         rl/q_learning.py rl/sophy_racing_qlearn.py generative/generative_npc.py; do
  echo "=== $f ==="; python "$f"; echo
done
```

## Notes · 说明

- Each file is **independent** (no shared modules) so you can copy one out on its own.
  每个文件相互独立，可单独复制使用。
- The code favors **clarity over performance** — it is meant to be read and learned from.
  代码以清晰易懂为先，便于学习，而非追求性能。
- Every simulation is **deterministic** (seeded) so runs are reproducible.
  每个模拟都是确定性的（固定随机种子），结果可复现。
- These are **classical teaching implementations**. Production engines add spatial
  hashing, nav-meshes, steering blends, neural networks, GPU search, etc. — see the
  [book](../docs/game-ai-book.en.md) for how each scales up.
  这些是经典教学实现；实际引擎会加入空间哈希、导航网格、神经网络等，详见教程书。
