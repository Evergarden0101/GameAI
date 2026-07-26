# A Practical Guide to Game AI — Classic & Modern Genres

*English · [中文版本](game-ai-guide.zh.md)*

> Companion runnable code for every genre below lives in [`../samples`](../samples).

> 📖 **Want the full, book-length treatment?** This page is the concise guide.
> The complete illustrated textbook — with genre deep-dives on **Mario Kart &
> Gran Turismo Sophy, Doom / F.E.A.R. / Rainbow Six / Apex, Civilization /
> Red Alert / StarCraft, and open-world GTA (NPC design, streaming, LOD AI & the
> performance budget)**, plus chapters on minimax, MCTS, GOAP, influence maps,
> exercises and a glossary — is **[Game AI: From Pac-Man to GT Sophy](game-ai-book.en.md)**
> ([中文版](game-ai-book.zh.md); also as Word: [EN](game-ai-book.docx) · [中文](game-ai-book.zh.docx)).

---

## Table of Contents

1. [What "Game AI" actually means](#1-what-game-ai-actually-means)
2. [The landscape at a glance](#2-the-landscape-at-a-glance)
3. [Classic Game AI](#3-classic-game-ai)
   - [3.1 NPCs — Finite State Machines & Behavior Trees](#31-npcs--finite-state-machines--behavior-trees)
   - [3.2 Cluster / swarm enemies — Flocking (Boids)](#32-cluster--swarm-enemies--flocking-boids)
   - [3.3 Follow / chase enemies — Pathfinding (A\*)](#33-follow--chase-enemies--pathfinding-a)
   - [3.4 Car racing AI — Waypoints, steering & rubber-banding](#34-car-racing-ai--waypoints-steering--rubber-banding)
   - [3.5 Other classic techniques](#35-other-classic-techniques-goap-utility-ai-mcts-pcg)
4. [Modern Game AI](#4-modern-game-ai)
   - [4.1 Reinforcement-Learning agents](#41-reinforcement-learning-rl-agents)
   - [4.2 Generative AI agents (LLM-driven)](#42-generative-ai-agents-llm-driven)
   - [4.3 Other ML approaches](#43-other-ml-approaches)
5. [Choosing an approach](#5-choosing-an-approach)
6. [Genre → sample code map](#6-genre--sample-code-map)
7. [Further reading](#7-further-reading)

---

## 1. What "Game AI" actually means

Game AI is **not** academic AI. Its goal is rarely to play *optimally* — it is to
make a game **fun, believable, and performant**. A chess engine wants to win; a
stealth-game guard wants to *lose in an interesting way* so the player feels
clever. Three constraints shape almost every decision:

- **Believability over optimality.** Enemies that never miss aren't fun. Much of
  game AI is deliberately *handicapped* intelligence.
- **Real-time performance.** Decisions must fit in a slice of a 16 ms frame
  (60 FPS), often shared across hundreds of agents.
- **Designer control.** Designers must be able to author, tune, and *predict*
  behavior. This is why transparent techniques (state machines, behavior trees)
  dominated for decades and still power most shipping games.

Because of this, "classic" hand-authored techniques never went away. The
"modern" learning-based techniques are additive — powerful for specific
problems, but they trade away the control and predictability designers love.

---

## 2. The landscape at a glance

| Era | Family | Representative techniques | Typical use |
|-----|--------|---------------------------|-------------|
| **Classic** (authored) | Decision logic | Finite State Machines, Behavior Trees, Utility AI, GOAP | NPCs, enemies, companions |
| | Movement | Steering behaviors, Flocking, Pathfinding (A\*, nav-mesh) | Chasing, swarming, patrolling, racing lines |
| | Search | Minimax, Alpha-Beta, Monte-Carlo Tree Search | Board/strategy games |
| | Content | Procedural Content Generation (PCG) | Levels, maps, loot |
| **Modern** (learned) | Reinforcement learning | Q-learning, DQN, PPO, self-play | Super-human/adaptive agents, racing, RTS/MOBA bots |
| | Imitation / supervised ML | Behavior cloning (e.g. Drivatar) | Human-like opponents |
| | Generative AI | LLM-driven NPCs, generative agents, generative PCG | Open-ended dialogue, emergent behavior, content |

The rest of this guide walks each row, focusing on the six genres you'll find in
[`../samples`](../samples): **racing AI, NPCs, cluster enemies, follow enemies,
RL agents, and generative agents.**

---

## 3. Classic Game AI

### 3.1 NPCs — Finite State Machines & Behavior Trees

Non-Player Characters (guards, townsfolk, enemies, companions) are the bread and
butter of game AI. Two authored techniques dominate.

**Finite State Machine (FSM).** The agent is always in exactly one *state*
(`Patrol`, `Investigate`, `Chase`, `Attack`, `Flee`). *Events* — seeing the
player, hearing a noise, taking damage — trigger *transitions*. FSMs are simple,
predictable, and trivial to debug, which is exactly why designers love them.

**Behavior Tree (BT).** As characters get complex, flat FSMs suffer a
"transition explosion" (every state needs an edge to every other). A BT instead
composes small behaviors with **Sequence** (do all, in order) and **Selector**
(try each until one succeeds) nodes into a tree that is re-evaluated every tick.
BTs scale far better and became the AAA standard after *Halo 2* (2004).

**Concrete examples**
- *Pac-Man* (1980): each ghost is a tiny FSM with a distinct personality —
  Blinky chases directly, Pinky aims ahead of you, Inky is erratic, Clyde
  retreats when close. A masterclass in *believable* behavior from trivial rules.
- *F.E.A.R.* (2005): famous for its **GOAP** planner (see §3.5) layered on top of
  state logic, giving soldiers emergent flanking and suppression.
- *Halo* series: behavior trees for grunts/elites with morale and retreat.

**Usage.** The default choice for almost any NPC or enemy: guards, wildlife,
companions, bosses. Cheap, authorable, predictable.

**Limitations.** Purely reactive — no learning, no long-term planning. Large
FSMs become spaghetti; large BTs become deep and hard to reason about. Behavior
is only as good as the designer's foresight, and clever players quickly learn to
exploit fixed patterns.

▶ **Sample:** [`samples/npc/npc_fsm.py`](../samples/npc/npc_fsm.py) — a guard
flows Patrol → Investigate → Chase → Attack → Flee → Patrol from perception and
health alone, plus a compact behavior-tree version of the "should I attack?"
decision.

---

### 3.2 Cluster / swarm enemies — Flocking (Boids)

When many small enemies must move as a coordinated group — bats, rats, zerglings,
a school of fish, a cloud of drones — the classic answer is Craig Reynolds'
**Boids** (1986). Each agent steers using only its *local* neighbours via three
rules:

1. **Separation** — steer away from crowding (avoid collisions).
2. **Alignment** — steer toward the average heading of neighbours.
3. **Cohesion** — steer toward the average position of neighbours (stay together).

Add a fourth **seek** rule toward the player and the swarm *hunts as a group*.
Crucially there is **no central controller**: the flock's coordinated look
*emerges* from many agents following the same local rules — cheap and organic.

**Concrete examples**
- *Half-Life* (1998) used boids for flying creatures; countless RTS games use
  flocking so unit groups move naturally instead of overlapping.
- *Batman: Arkham* games use flocking for swarms of bats.
- Modern engines expose steering-behavior systems (separation, arrival, wander,
  flee) that blend on top of pathfinding.

**Usage.** Groups of cheap enemies or ambient creatures; crowd simulation;
formations. Combines beautifully with a pathfinding "leader" that the group
follows.

**Limitations.** Emergent behavior is hard to author precisely — you tune weights
and *hope*. Naïve implementations are O(n²) (every agent checks every other), so
large flocks need spatial partitioning (grids, quad-trees). Boids don't avoid
walls on their own; they're usually blended with pathfinding or obstacle
avoidance.

▶ **Sample:** [`samples/flocking/flocking.py`](../samples/flocking/flocking.py) —
40 boids self-organize and converge on the player using only local rules.

---

### 3.3 Follow / chase enemies — Pathfinding (A\*)

A "follow enemy" must navigate *around obstacles* to reach a moving target. The
workhorse is **A\*** ("A-star", Hart–Nilsson–Raphael, 1968), a best-first graph
search that expands the node minimising

```
f(n) = g(n) + h(n)
```

where `g` is the known cost from the start and `h` is a *heuristic* estimate to
the goal (e.g. Manhattan or Euclidean distance). If `h` never overestimates
(is *admissible*), A\* is guaranteed to find the shortest path. Games run A\* on
grids, waypoint graphs, or **navigation meshes** (nav-meshes) that describe
walkable polygons.

**Chasing a moving target** is A\* plus a policy for *when to re-plan*: recompute
every tick (simple, costly), on a timer, or only when the target moves far
enough. Hierarchical pathfinding and flow fields scale this to hundreds of units.

**Concrete examples**
- Practically every game with navigation: *StarCraft*, *Age of Empires*, tower
  defense creeps, stealth-game guards returning to post.
- *Pac-Man* ghosts (again) — a beautifully minimal grid chase without full A\*.
- Nav-meshes are standard in Unity (NavMesh) and Unreal (Navigation System).

**Usage.** Any agent that must reach a point through a non-trivial map: pursuers,
patrols, fetch-quest companions, RTS unit orders.

**Limitations.** Cost scales with map size and agent count; naïvely re-planning
every frame for many chasers is expensive. Dynamic obstacles (doors, other
agents) need re-planning or local avoidance. Grid A\* produces "blocky" paths
that usually need smoothing. Long-range planning across huge worlds needs
hierarchical methods.

▶ **Sample:** [`samples/follow/pathfinding_astar.py`](../samples/follow/pathfinding_astar.py)
— an enemy routes around a wall to a fixed goal, then chases a fleeing player by
re-planning an A\* path every tick.

---

### 3.4 Car racing AI — Waypoints, steering & rubber-banding

Racing opponents combine three ideas:

1. **The racing line as waypoints.** The track is annotated with a sequence of
   waypoints (or splines) forming the ideal line. The AI uses a **pure-pursuit /
   look-ahead** controller: always steer toward a point a little further ahead.
2. **Steering & speed control (PID).** A proportional controller turns the wheel
   in proportion to the heading error; braking points and cornering speeds slow
   the car for sharp turns and let it floor it on straights.
3. **Rubber-banding (Dynamic Difficulty Adjustment).** To keep races close, the
   AI's top speed is nudged up when it falls behind and down when it pulls too
   far ahead. This "catch-up" logic is the (sometimes controversial) secret
   behind *Mario Kart* and many arcade racers.

**Concrete examples**
- *Mario Kart* series — overt rubber-banding and catch-up items.
- *Forza Motorsport* **Drivatar** — machine-learned driving profiles that
  imitate *real players'* styles (an early, celebrated use of ML in a shipping
  racing game; see §4.3).
- *Gran Turismo Sophy* (Sony AI, 2022) — a **reinforcement-learning** agent that
  beat top human drivers (see §4.1). Racing is where classic and modern AI meet.

**Usage.** AI opponents, ghost laps, traffic, and "auto-drive" assists in racing
and driving games.

**Limitations.** Pure waypoint AI is only as good as its authored line and can
look robotic or fail on unexpected geometry (spun-out cars, shortcuts).
Rubber-banding, if too aggressive, feels unfair ("the AI cheats"). Realistic
overtaking, blocking, and physics-aware driving are hard to hand-author — which
is exactly why the frontier (Sophy, Drivatar) moved to learning.

▶ **Sample:** [`samples/racing/racing_ai.py`](../samples/racing/racing_ai.py) —
a waypoint-following AI with PID steering and rubber-banding races a steady
"player" and keeps the gap small.

---

### 3.5 Other classic techniques (GOAP, Utility AI, MCTS, PCG)

- **GOAP (Goal-Oriented Action Planning).** Instead of hard-coded transitions,
  the agent is given *goals* and *actions with preconditions/effects*, and a
  planner (A\* over the action space) assembles a plan at runtime. Debuted in
  *F.E.A.R.* (2005); produces flexible, emergent tactics.
- **Utility AI.** Each possible action is scored by a *utility* function of the
  world state; the agent picks the highest (or samples). Excellent for agents
  with many competing needs — famously *The Sims* (2000), where Sims weigh
  hunger, fun, social, hygiene, etc.
- **Search for board/strategy games.** *Minimax* with *alpha-beta pruning* powers
  classic chess engines; *Monte-Carlo Tree Search (MCTS)* powers strong Go/board
  AIs and later fused with deep learning in AlphaGo.
- **Procedural Content Generation (PCG).** Algorithms generate levels, maps,
  dungeons, loot, and terrain: *Rogue* (1980), *Spelunky*, *Minecraft*,
  *No Man's Sky* (18-quintillion planets). Increasingly hybridized with ML
  ("PCGML") and now generative models.

---

## 4. Modern Game AI

Modern approaches **learn** behavior from data or experience instead of having it
authored. They shine where hand-authoring is impractical, but they cost data,
compute, and predictability.

### 4.1 Reinforcement-Learning (RL) agents

In **RL**, an agent learns by trial and error to maximize cumulative **reward**.
It builds a *policy* mapping states to actions, guided by feedback from the
environment. The tabular **Q-learning** update is the classic starting point:

```
Q(s,a) ← Q(s,a) + α · [ r + γ · maxₐ' Q(s',a') − Q(s,a) ]
```

`α` is the learning rate, `γ` discounts future reward. Scale the table up to a
neural network and you get **Deep Q-Networks (DQN)**; policy-gradient methods
like **PPO** and **self-play** (agents training against copies of themselves)
power the headline results:

**Concrete examples**
- **AlphaGo / AlphaZero / MuZero** (DeepMind, 2016–) — RL + MCTS beat world
  champions at Go, then chess and shogi from self-play alone.
- **OpenAI Five** (2019) — five PPO-trained agents beat the world champions at
  *Dota 2*, a long-horizon, partial-information team game.
- **AlphaStar** (DeepMind, 2019) — reached Grandmaster at *StarCraft II*.
- **Gran Turismo Sophy** (Sony AI, *Nature* 2022) — an RL agent that outraced the
  world's best *Gran Turismo* drivers, with human-like racecraft.
- **Unity ML-Agents** — a toolkit that lets studios train RL/imitation agents
  inside their own games.

**Usage.** Super-human or highly adaptive opponents; agents for games too complex
to script (racing physics, RTS/MOBA micro); automated playtesting and balancing;
NPC skill tuning. Best when you have a fast simulator and a clear reward.

**Limitations.**
- **Sample-hungry & expensive.** OpenAI Five trained on centuries of gameplay per
  day; most studios can't afford that compute.
- **Reward design is hard.** Bad reward functions produce *reward hacking* —
  agents exploiting loopholes instead of playing "properly."
- **Unpredictable & hard to debug.** A learned policy is a black box; you can't
  easily guarantee it won't do something absurd, which designers dislike.
- **Often too good.** A super-human bot isn't fun; you must *deliberately weaken*
  it. Poor generalization to unseen situations and content is common.
- **Integration cost.** Needs a training pipeline, a simulator, and careful QA —
  a heavy lift versus a state machine.

▶ **Sample:** [`samples/rl/q_learning.py`](../samples/rl/q_learning.py) — a
tabular Q-learning agent discovers the optimal path through a maze (avoiding a
pit) purely from reward, then prints the learned policy.

---

### 4.2 Generative AI agents (LLM-driven)

The newest genre puts a **Large Language Model (LLM)** at the heart of an NPC or
agent. Instead of a fixed dialogue tree, the character has:

- a **persona** (a system prompt defining who it is),
- **memory** (conversation history, and sometimes long-term memory stores), and
- **tools / function-calling** so its words become real game actions — giving a
  quest, opening the shop, changing its disposition, moving, attacking.

The player can say *anything* and the NPC responds in character and acts on the
world. Give many such agents a shared world and *emergent social behavior*
appears.

**Concrete examples**
- **"Generative Agents"** (Park et al., Stanford, 2023) — 25 LLM agents in a
  sandbox town ("Smallville") formed relationships, spread news, and
  autonomously organized a Valentine's party. The seminal demonstration.
- **NVIDIA ACE**, **Inworld AI**, **Convai** — middleware bringing LLM-driven,
  voiced NPCs into real game engines.
- **AI Dungeon** (2019) — an early GPT-powered open-ended text adventure.
- Generative models are also used for **content**: textures, dialogue, quests,
  and levels (generative PCG).

**Usage.** Open-ended, replayable dialogue; dynamic quests; companions with
personality and memory; rapid prototyping of characters; accessibility (talk to
NPCs naturally). Also powerful as a *design tool* (generating content offline).

**Limitations.**
- **Hallucination & consistency.** LLMs invent facts, break lore, or contradict
  earlier statements — dangerous for canon and narrative.
- **Control & safety.** Free-form output can be off-tone, exploited by players
  ("jailbreaks"), or say things the studio never approved. Guardrails and tool
  constraints are essential; keep the LLM's *authority* bounded by tools.
- **Latency & cost.** A network round-trip per line adds latency, and per-token
  cost adds up at scale; on-device models trade quality for speed.
- **Determinism & testing.** Non-deterministic output is hard to QA and to
  reproduce for bug reports.
- **Grounding.** The LLM must be tied to actual game state (via tools/memory) or
  it's just chatter with no gameplay consequence.

▶ **Sample:**
[`samples/generative/generative_npc.py`](../samples/generative/generative_npc.py)
— an LLM blacksmith (Anthropic's Claude, `claude-opus-5`) improvises in-character
dialogue *and* drives real game state through tool calls (give quest, check
inventory, adjust disposition). Runs a fully offline mock if no API key is set,
so you can study the architecture with zero setup.

---

### 4.3 Other ML approaches

- **Imitation / behavior cloning.** Train a model to copy *human* play from
  recorded data. **Forza's Drivatar** learns individual players' racing styles so
  your friends' "ghosts" race even when they're offline — human-like opponents
  without super-human RL.
- **Supervised ML for perception/animation.** Learned animation controllers
  (motion matching, learned locomotion), difficulty prediction, matchmaking,
  cheat detection, and player-churn models are ML that never touches the "AI
  opponent" but shapes the experience.
- **Hybrid systems** are the practical frontier: a behavior tree for structure,
  utility scoring for decisions, learned sub-policies for hard motor skills, and
  an LLM for dialogue — each technique where it's strongest.

---

## 5. Choosing an approach

| If you need… | Reach for | Why |
|--------------|-----------|-----|
| A guard/enemy with clear, authorable behavior | **FSM / Behavior Tree** | Predictable, cheap, designer-controlled |
| A group that moves organically | **Flocking / steering** | Emergent coordination, no central brain |
| To reach a point through a map | **A\* / nav-mesh** | Optimal, well-understood |
| A believable racing opponent | **Waypoints + PID + rubber-banding** | Close, fun races on authored lines |
| Complex reactive tactics | **GOAP / Utility AI** | Emergent plans from goals/scores |
| Super-human or unscriptable skill | **Reinforcement learning** | Learns what you can't author — at a cost |
| Human-like opponents from data | **Imitation learning** | Copies real players' style |
| Open-ended dialogue & emergent characters | **Generative / LLM agents** | Say/do anything, in character |

**Rule of thumb:** start with the simplest technique that meets the design goal.
Reach for learning-based methods only when authoring is genuinely impractical,
and always bound a generative agent's power with tools and validation.

---

## 6. Genre → sample code map

| Genre | Guide section | Runnable sample |
|-------|---------------|-----------------|
| Car racing AI | [3.4](#34-car-racing-ai--waypoints-steering--rubber-banding) | [`samples/racing/racing_ai.py`](../samples/racing/racing_ai.py) |
| Mario Kart items & catch-up | [book ch.10](game-ai-book.en.md) | [`samples/racing/mario_kart_items.py`](../samples/racing/mario_kart_items.py) |
| NPCs (FSM / BT) | [3.1](#31-npcs--finite-state-machines--behavior-trees) | [`samples/npc/npc_fsm.py`](../samples/npc/npc_fsm.py) |
| Pac-Man ghost AI | [3.1](#31-npcs--finite-state-machines--behavior-trees) | [`samples/classic/pacman_ghosts.py`](../samples/classic/pacman_ghosts.py) |
| Cluster / swarm enemies | [3.2](#32-cluster--swarm-enemies--flocking-boids) | [`samples/flocking/flocking.py`](../samples/flocking/flocking.py) |
| Follow / chase enemies | [3.3](#33-follow--chase-enemies--pathfinding-a) | [`samples/follow/pathfinding_astar.py`](../samples/follow/pathfinding_astar.py) |
| GOAP planner (F.E.A.R.) | [3.5](#35-other-classic-techniques-goap-utility-ai-mcts-pcg) | [`samples/classic/goap_planner.py`](../samples/classic/goap_planner.py) |
| Minimax + alpha-beta | [3.5](#35-other-classic-techniques-goap-utility-ai-mcts-pcg) | [`samples/classic/minimax_tictactoe.py`](../samples/classic/minimax_tictactoe.py) |
| MCTS (Connect Four) | [3.5](#35-other-classic-techniques-goap-utility-ai-mcts-pcg) | [`samples/classic/mcts_connect_four.py`](../samples/classic/mcts_connect_four.py) |
| FPS tactical squad AI | [book ch.11](game-ai-book.en.md) | [`samples/fps/tactical_fps.py`](../samples/fps/tactical_fps.py) |
| RTS skirmish (C&C / Red Alert) | [book ch.12](game-ai-book.en.md) | [`samples/rts/command_conquer_ai.py`](../samples/rts/command_conquer_ai.py) |
| 4X empire AI (Civilization) | [book ch.12](game-ai-book.en.md) | [`samples/strategy/civ_ai.py`](../samples/strategy/civ_ai.py) |
| RL agents | [4.1](#41-reinforcement-learning-rl-agents) | [`samples/rl/q_learning.py`](../samples/rl/q_learning.py) |
| RL racer (Sophy-style) | [4.1](#41-reinforcement-learning-rl-agents) | [`samples/rl/sophy_racing_qlearn.py`](../samples/rl/sophy_racing_qlearn.py) |
| Generative AI agents | [4.2](#42-generative-ai-agents-llm-driven) | [`samples/generative/generative_npc.py`](../samples/generative/generative_npc.py) |

All samples run on the Python standard library (the generative one optionally
uses the Anthropic SDK, with an offline fallback). See
[`../samples/README.md`](../samples/README.md). For deep-dives on the racing,
shooter, and strategy genres above, see the full
**[book](game-ai-book.en.md)**.

---

## 7. Further reading

- Craig Reynolds, *"Flocks, Herds, and Schools: A Distributed Behavioral Model"*
  (SIGGRAPH 1987) — the Boids paper.
- Hart, Nilsson & Raphael, *"A Formal Basis for the Heuristic Determination of
  Minimum Cost Paths"* (1968) — the A\* paper.
- Millington & Funge, *Artificial Intelligence for Games* — the standard text on
  classic techniques (FSMs, steering, pathfinding, decision making).
- Sutton & Barto, *Reinforcement Learning: An Introduction* — the RL reference.
- Vinyals et al., *"Grandmaster level in StarCraft II"* (Nature, 2019) —
  AlphaStar.
- Wurman et al., *"Outracing champion Gran Turismo drivers with deep
  reinforcement learning"* (Nature, 2022) — Sophy.
- Park et al., *"Generative Agents: Interactive Simulacra of Human Behavior"*
  (2023) — Smallville.
- *Game AI Pro* book series (ed. Steve Rabin) — practitioner articles.
- Unity **ML-Agents** and the **GDC AI Summit** talks — hands-on modern practice.
