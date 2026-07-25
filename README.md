# GameAI

A bilingual (English / 中文) **book and code lab** on **Game AI** — the classic
and modern techniques that make game characters move, fight, chase, race, plan,
talk, and learn — with a **runnable code sample for every technique**.

游戏 AI 的中英双语**教程书 + 代码实验室**：让游戏角色移动、战斗、追击、竞速、
决策、对话与学习的经典与现代技术，**每种技术都配有可直接运行的示例代码**。

---

## 📖 The book · 教程书

A full, illustrated textbook — **[Game AI: From Pac-Man to GT Sophy](docs/game-ai-book.en.md)** —
takes you from foundations through the classic toolbox, genre deep-dives, and
modern learned AI, with exercises and a glossary.

一本完整的图文教程书，从基础、经典工具箱、类型深入到现代学习式 AI，附练习与术语表。

| Format · 格式 | Link · 链接 |
|---|---|
| 📘 **Book (Markdown)** · 教程书 | [`docs/game-ai-book.en.md`](docs/game-ai-book.en.md) |
| 📄 **Book (Word / .docx)** · Word 版 | [`docs/game-ai-book.docx`](docs/game-ai-book.docx) |
| 📗 Concise guide (English) · 简明指南 | [`docs/game-ai-guide.en.md`](docs/game-ai-guide.en.md) |
| 📗 简明指南（中文） | [`docs/game-ai-guide.zh.md`](docs/game-ai-guide.zh.md) |

**What it covers:** what game AI really is (fun over optimal) · FSMs & behavior
trees · utility AI & GOAP · steering & flocking · A\* pathfinding · minimax,
alpha-beta & MCTS · influence maps & PCG · **racing (Mario Kart, Gran Turismo
Sophy)** · **shooters (Doom, F.E.A.R., Rainbow Six, Apex)** · **strategy
(Civilization, Command & Conquer / Red Alert, StarCraft)** · reinforcement
learning · imitation learning · generative (LLM) agents.

## 🕹️ Interactive lab · 交互式实验室

A self-contained web page — [`web/gameai-lab.html`](web/gameai-lab.html) — with
**three live, interactive debug viewports**: Pac-Man ghost personalities, an FPS
suppress-and-flank squad, and a playable **unbeatable minimax** board. Open it in
any browser (no build, no dependencies), or view it as an
[Artifact](https://claude.ai/code/artifact/4d503b43-4225-4339-9777-3c8058a60c02).

一个自包含网页——内含三个可交互的调试视图：吃豆人幽灵性格、FPS 压制包抄小队，
以及可对弈的“不可战胜”井字棋。用浏览器直接打开即可，无需构建或依赖。

## 💻 The samples · 示例代码

Fifteen self-contained programs in [`samples/`](samples). **Fourteen run on the
Python standard library alone**; the generative NPC optionally uses the Anthropic
SDK and otherwise falls back to an offline mock.

[`samples/`](samples) 中有十五个自包含程序，**其中十四个仅用 Python 标准库**；
生成式 NPC 可选使用 Anthropic SDK，否则回退到离线模拟。

**Classic toolbox** — NPC state machine + behavior tree · Pac-Man ghost AI ·
Boids flocking · A\* pathfinding · GOAP planner · minimax + alpha-beta · MCTS.

**Genre deep-dives** — car racing AI · Mario Kart items & catch-up · FPS tactical
squad (line-of-sight / cover / suppression / flanking) · RTS skirmish
(C&C / Red Alert) · 4X empire AI (Civilization + difficulty bonuses).

**Modern / learned** — Q-learning · a Sophy-style RL racer · generative LLM NPC.

See [`samples/README.md`](samples/README.md) for the full table and run commands.
完整列表与运行命令见 [`samples/README.md`](samples/README.md)。

### Quick start · 快速开始

```bash
# Everything but the LLM NPC needs nothing but Python 3.8+
python samples/classic/pacman_ghosts.py       # the four ghost personalities
python samples/fps/tactical_fps.py            # suppress-and-flank squad AI
python samples/strategy/civ_ai.py             # 4X utility AI + difficulty bonuses
python samples/rts/command_conquer_ai.py      # rush vs. economy RTS doctrines
python samples/classic/mcts_connect_four.py   # Monte-Carlo Tree Search
python samples/rl/sophy_racing_qlearn.py      # RL learns to brake for corners

# Generative NPC: runs an offline mock as-is, or connect a live LLM:
pip install -r samples/requirements.txt
export ANTHROPIC_API_KEY=sk-...
python samples/generative/generative_npc.py
```

## 🗂️ Repository layout · 目录结构

```
GameAI/
├── README.md                       ← you are here · 你在这里
├── docs/
│   ├── game-ai-book.en.md          ← the full textbook (English)
│   ├── game-ai-book.docx           ← the textbook as a Word document
│   ├── game-ai-guide.en.md         ← concise guide (English)
│   └── game-ai-guide.zh.md         ← 简明指南（中文）
├── scripts/
│   └── md_to_docx.py               ← rebuilds the .docx from the Markdown
└── samples/
    ├── classic/                    # pacman_ghosts, minimax, mcts, goap
    ├── npc/                        # state machine + behavior tree
    ├── flocking/  follow/          # boids · A* pathfinding
    ├── racing/                     # racing_ai · mario_kart_items
    ├── fps/                        # tactical_fps (squad tactics)
    ├── rts/                        # command_conquer_ai
    ├── strategy/                   # civ_ai (4X)
    ├── rl/                         # q_learning · sophy_racing_qlearn
    └── generative/                 # generative_npc (LLM + tools)
```

## Rebuilding the Word document · 重新生成 Word 文档

The `.docx` is generated from the Markdown book (requires `python-docx`):

```bash
pip install python-docx
python scripts/md_to_docx.py docs/game-ai-book.en.md
```

## License · 许可

Provided as educational sample code. Use freely.
仅作教学示例代码，可自由使用。
