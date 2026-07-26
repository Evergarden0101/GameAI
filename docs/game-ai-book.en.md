# Game AI: From Pac-Man to GT Sophy

### An Illustrated, Hands-On Guide to the Techniques Behind Game Characters

*A companion textbook to the [GameAI](../README.md) repository. Every technique in this book has runnable code in [`../samples`](../samples).*

*English edition. A concise bilingual guide is also available: [English](game-ai-guide.en.md) · [中文](game-ai-guide.zh.md).*

---

## How to use this book

This is a **book for learning**, organized so you can read it front to back or jump to the genre you care about.

- **Part I — Foundations** explains what game AI *is*, how it differs from academic AI, and the sense–think–act loop every agent runs.
- **Part II — The Classic Toolbox** teaches the authored techniques that still power most shipping games: state machines, behavior trees, utility AI, GOAP, steering, pathfinding, and search.
- **Part III — Genre Deep-Dives** shows how *real, named games* build their AI: racing (Mario Kart, Gran Turismo 7 / Sophy), shooters (Doom, F.E.A.R., Rainbow Six Siege, Apex), and strategy (Civilization, Command & Conquer / Red Alert, StarCraft).
- **Part IV — Modern, Learned AI** covers reinforcement learning, imitation learning, and generative (LLM) agents.
- **Part V — Practice** gives a decision guide, exercises, a glossary, and references.

Each technique chapter follows the same rhythm: **the idea → how it works → concrete shipped games → usage → limitations → the runnable sample**. Look for the ▶ marker linking to code you can run immediately with nothing but Python.

> **A note on philosophy.** Throughout, remember the golden rule: **game AI optimizes for fun, not for winning.** This one idea explains almost every design decision that follows.

---

## Table of Contents

**Part I — Foundations**
1. What Game AI Is (and Isn't)
2. A Short History of Game AI
3. The Agent Loop: Sense, Think, Act

**Part II — The Classic Toolbox**
4. Decision-Making I — Finite State Machines & Behavior Trees
5. Decision-Making II — Utility AI & GOAP
6. Movement I — Steering & Flocking
7. Movement II — Pathfinding with A\*
8. Adversarial Search — Minimax, Alpha-Beta & MCTS
9. Spatial Reasoning — Influence Maps & Procedural Content

**Part III — Genre Deep-Dives**
10. Racing AI — Mario Kart to Gran Turismo Sophy
11. Shooter AI — Doom to Rainbow Six & Apex
12. Strategy AI — Civilization, Red Alert & StarCraft
13. Open-World AI — GTA, Streaming & the Performance Budget

**Part IV — Modern, Learned AI**
14. Reinforcement Learning
15. Imitation Learning & Other ML
16. Generative AI Agents (LLMs)

**Part V — Practice**
17. Choosing an Approach
18. Exercises
19. Glossary
20. Further Reading

**Appendix**
- A. Training AI Inside the Engine — Unity ML-Agents & Unreal Learning Agents

---

# Part I — Foundations

## 1. What Game AI Is (and Isn't)

When researchers say "AI," they usually mean building a system that solves a problem as *well* as possible — a chess engine that wins, a classifier that is accurate, a robot that reaches its goal efficiently. **Game AI is different, and the difference is the whole subject.** The goal of the AI in a game is not to win. It is to make the *player* have a good time.

A stealth-game guard that could actually find you every time would end the game in seconds and feel awful. A racing opponent that drove a physically perfect lap would vanish over the horizon and never be seen again. A shooter enemy that shot you the instant you were in its line of sight, with perfect accuracy, at any range, would be simply unfair. In every case the "better" the AI plays, the *worse* the game becomes. So game AI is, more than anything, the art of building **intelligence that is deliberately shaped, bounded, and often handicapped** to produce a specific experience.

Three constraints press on nearly every decision a game-AI programmer makes:

**1. Believability over optimality.** The AI must *look* intelligent, which is not the same as *being* intelligent. Players read intention into behavior: an enemy that takes cover, calls out that it's flanking, and throws a grenade *feels* smart even if, under the hood, it is following a few simple rules. Conversely, an agent doing something genuinely clever that the player can't perceive is wasted computation. Much of the craft is in **telegraphing** — making the AI's reasoning legible through animation, audio barks, and readable movement.

**2. Real-time performance.** A game running at 60 frames per second has about **16 milliseconds** to simulate *everything* in a frame — physics, animation, rendering, audio, and the AI for potentially hundreds or thousands of agents. An RTS may have thousands of units pathfinding at once. This hard budget is why lightweight, predictable techniques dominate and why expensive methods (deep neural networks, large search) are used sparingly, precomputed, or amortized across many frames.

**3. Designer control.** Games are authored experiences. A designer needs to be able to build a specific encounter, tune it, predict it, and debug it when a tester reports "the boss got stuck in the corner." This is the quiet reason that transparent, inspectable techniques — state machines, behavior trees — have dominated for decades and still do. A system you cannot predict is a system you cannot ship with confidence.

Because of these constraints, the "classic," hand-authored techniques never went away. The exciting "modern," learning-based techniques (reinforcement learning, LLM agents) are **additive**: they are powerful for specific problems where authoring is impractical, but they trade away exactly the control and predictability that designers prize. A mature game-AI engineer treats all of it as one toolbox and reaches for the simplest tool that produces the desired feel.

> **Key distinction.** *Academic AI asks "how do I win/solve this?" Game AI asks "how do I make a human enjoy playing against or alongside this?"* Keep this in mind and the field's peculiar choices — enemies that miss on purpose, opponents that rubber-band, bosses with scripted "tells" — all make sense.

## 2. A Short History of Game AI

Understanding where the techniques came from makes them easier to remember. Here is the field in one timeline.

| Year | Game / Milestone | Why it matters |
|------|------------------|----------------|
| 1972 | *Pong* | Enemy paddle tracks the ball — arguably the first game "AI," a one-line rule. |
| 1978 | *Space Invaders* | Fixed patterns that speed up as enemies die — emergent difficulty from a bug that became a feature. |
| 1980 | *Pac-Man* | Four ghosts, each a tiny state machine with a *distinct personality*; the birth of readable, character-driven AI. |
| 1990s | *Warcraft*, *Command & Conquer*, *Age of Empires* | Real-time strategy forces industrial-strength pathfinding and economic AI. |
| 1998 | *Half-Life* | Marines that flank, retreat, and use squad tactics — a leap in perceived intelligence. |
| 1999 | *The Sims* (2000) | Utility AI: characters driven by competing needs (hunger, fun, social). |
| 2004 | *Halo 2* | Popularized **behavior trees** as the AAA standard for character AI. |
| 2005 | *F.E.A.R.* | **GOAP** planning gives soldiers emergent, unscripted tactics — still a benchmark for combat AI. |
| 2008 | *Left 4 Dead* | The **AI Director** dynamically paces tension — AI as a *dramatist*, not an opponent. |
| 2016 | *AlphaGo* (DeepMind) | Deep RL + MCTS beats a Go world champion; the modern era of learned game agents begins. |
| 2019 | *OpenAI Five*, *AlphaStar* | RL agents reach champion level at *Dota 2* and *StarCraft II* — long-horizon, hidden-information team games. |
| 2022 | *Gran Turismo Sophy* (Sony AI) | Deep RL outraces the world's best human drivers *with* good sportsmanship — published in *Nature*. |
| 2023 | *Generative Agents* ("Smallville"), NVIDIA ACE | LLM-driven NPCs with memory and autonomy; the generative era of game characters begins. |

Two things stand out. First, the **classic techniques cluster in the 1980s–2000s** and are still in constant use. Second, the **learned techniques are recent, expensive, and headline-grabbing** — but each solved a problem the classic toolbox genuinely couldn't. The rest of this book follows exactly this arc.

## 3. The Agent Loop: Sense, Think, Act

Almost every game agent, from a Pac-Man ghost to a Sophy racer, runs the same loop every "tick" (update step):

```
        ┌─────────────────────────────────────────┐
        │                                          │
        ▼                                          │
   ┌─────────┐      ┌──────────┐      ┌─────────┐  │
   │  SENSE  │ ───▶ │  THINK   │ ───▶ │   ACT   │ ─┘
   │ gather  │      │ decide   │      │ move,   │
   │ world   │      │ what to  │      │ shoot,  │
   │ state   │      │ do next  │      │ build…  │
   └─────────┘      └──────────┘      └─────────┘
```

- **Sense** — read the parts of the world the agent is allowed to know: the player's position (if visible), nearby cover, its own health, sounds. Crucially, good AI *restricts* its own senses to what's fair — an enemy shouldn't react to a player it cannot see, or the illusion breaks.
- **Think** — run a decision algorithm to choose an action. **This is where the techniques in this book live.** A state machine, a behavior tree, a utility score, an A\* search, a neural network — all are just different ways of implementing "Think."
- **Act** — apply the chosen action to the world: set a movement target, fire a weapon, queue a building. Actions usually take many ticks to complete, so the loop is continuous, not one-shot.

Everything that follows is, in essence, a catalogue of ways to implement the **Think** box — and a guide to which one to pick for which job.

---

# Part II — The Classic Toolbox

The techniques in Part II are **authored**: a human designer specifies the behavior directly. They are cheap, predictable, debuggable, and — decades after their invention — still the backbone of almost every shipping game. Master these and you can build the AI for the majority of games ever made.

## 4. Decision-Making I — Finite State Machines & Behavior Trees

### The idea

The most fundamental question in character AI is: *given the situation, what should I do right now?* The oldest and most transparent answer is the **Finite State Machine (FSM)**.

An FSM says the agent is always in exactly one **state** — `Patrol`, `Investigate`, `Chase`, `Attack`, `Flee` — and that **events** (seeing the player, hearing a noise, taking damage, low health) trigger **transitions** between states. That's it. Each state defines behavior ("in `Patrol`, walk between waypoints") and the transitions define the logic ("if I see the player, go to `Chase`").

```
        see player            in range
 ┌────────┐──────────▶┌────────┐──────────▶┌────────┐
 │ PATROL │           │ CHASE  │           │ ATTACK │
 └────────┘◀──────────└────────┘◀──────────└────────┘
      ▲   lost player       │   out of range      │
      │                     │ low health          │
      │                     ▼                     │
      │                ┌────────┐                 │
      └────────────────│  FLEE  │◀────────────────┘
          safe again   └────────┘   low health
```

FSMs are simple, predictable, and trivial to debug — which is *exactly* why designers love them. You can draw one on a whiteboard, and when a tester says "the guard did something weird," you can point at the exact state and transition responsible.

### The problem FSMs hit, and behavior trees

FSMs have a fatal flaw as characters grow complex: the **transition explosion**. With *n* states, you can need up to *n×(n−1)* transitions — every state potentially needing an edge to every other. At a dozen states this becomes an unmaintainable tangle of spaghetti.

The **Behavior Tree (BT)**, popularized by *Halo 2* (2004), solves this. Instead of a graph of states-and-transitions, a BT is a **tree of behaviors that is re-evaluated from the root every tick.** Its power comes from a few node types:

- **Sequence** (→): run children left to right; succeed only if *all* succeed; stop at the first failure. ("Move to cover **AND** aim **AND** fire.")
- **Selector** (?): try children left to right; succeed at the *first* that succeeds. ("Attack **OR ELSE** chase **OR ELSE** patrol.") This gives natural **fallback/priority** behavior.
- **Leaf** nodes are **actions** (do something) or **conditions** (test something).
- **Decorators** modify a child (invert it, repeat it, add a cooldown).

```
                 [Selector: pick the first that works]
                /                |                    \
        [Sequence: fight]   [Sequence: search]     [Action: patrol]
         /       |     \       /        \
 [see enemy?] [in range?] [fire]  [heard noise?] [go to noise]
```

Because the whole tree re-runs each tick, a higher-priority branch (fight) automatically **preempts** a lower one (patrol) the instant its conditions become true — no explicit transitions required. BTs scale to hundreds of behaviors, are modular (subtrees reuse), and became the AAA standard for character AI.

### Concrete games

- ***Pac-Man*** **(1980)** — the canonical FSM showcase. Each ghost is a minimal state machine with a distinct target-selection *personality*: Blinky chases you directly, Pinky aims ahead of you to cut you off, Inky uses a vector reflected through Blinky for erratic pincers, and Clyde chases only when far and retreats when close. From four one-line rules emerges behavior that *feels* like a coordinated hunting pack. We dissect this in detail in **Chapter 11's cousin**, and there is runnable code below.
- ***Halo*** **series** — behavior trees for Grunts and Elites, including morale (Grunts flee when their leader dies).
- ***F.E.A.R.*** **(2005)** — layered a GOAP planner (Chapter 5) *on top of* state logic for its famous soldiers.

### Usage

The default choice for almost any NPC or enemy: guards, wildlife, companions, bosses, simple enemies. If you're not sure what to use, start here. FSMs for simple agents (a few states); behavior trees once behavior grows or you want reusable, prioritized logic.

### Limitations

Purely **reactive** — there is no lookahead or planning; the agent does what its current state/tree says, nothing more. Large FSMs become spaghetti; large BTs become deep and hard to trace. Most importantly, the behavior is only ever as good as the designer's foresight: clever players quickly learn the fixed patterns and exploit them. For long-term reasoning you need planning (Chapter 5); for adaptation you need learning (Part IV).

### ▶ Run it

- [`samples/npc/npc_fsm.py`](../samples/npc/npc_fsm.py) — a guard that flows Patrol → Investigate → Chase → Attack → Flee → Patrol from perception and health alone, plus a compact behavior-tree version of the "should I attack?" decision.
- [`samples/classic/pacman_ghosts.py`](../samples/classic/pacman_ghosts.py) — the four Pac-Man ghosts, each with its real target-selection rule and the scatter/chase mode timer, hunting a Pac-Man in an ASCII maze.

## 5. Decision-Making II — Utility AI & GOAP

FSMs and BTs *react*. Two more classic techniques let agents **weigh options** and **plan ahead**.

### Utility AI

Instead of hard rules, **Utility AI** scores every possible action with a **utility function** of the current world state, then picks the highest score (or samples proportionally for variety). Each action answers "how appealing am I *right now*?" with a number.

This is ideal for agents juggling **many competing needs**. The canonical example is ***The Sims*** **(2000)**, where each Sim continuously scores actions against its needs — hunger, energy, fun, social, hygiene, bladder — and does whatever currently scores highest. Eat when hungry, sleep when tired, seek company when lonely; the behavior looks lifelike because it *is* a continuous trade-off, exactly like real motivation.

Utility AI shines in strategy games too. In a 4X game like ***Civilization***, a city scores every possible thing it could build — settler, worker, soldier, library, granary — against the empire's current situation (few cities? favor settlers; under threat? favor military; peaceful and growing? favor infrastructure). No decision tree, just a bag of tunable scoring functions. We build exactly this in Chapter 12.

**Strengths:** smoothly handles many factors, produces nuanced "it depends" behavior, easy to add a new option (just write its score). **Weaknesses:** tuning the scoring functions is a dark art — a badly weighted term produces bizarre choices, and because everything blends, it can be hard to guarantee a specific behavior in a specific situation.

### GOAP — Goal-Oriented Action Planning

**GOAP** takes a different leap: instead of authoring *behavior*, you author *goals* and *actions with preconditions and effects*, and let a **planner assemble the behavior at runtime.** It's the AI equivalent of giving someone an objective and a toolbox instead of a script.

- A **goal** is a desired world state, e.g. `enemy_dead = true`.
- Each **action** has **preconditions** (world state required to run it) and **effects** (how it changes the world), plus a **cost**. E.g. `Attack` requires `weapon_loaded ∧ near_enemy` and yields `enemy_dead`.
- The planner runs **A\*** (Chapter 7) *through the space of world states*, chaining actions from the current state to one satisfying the goal, minimizing total cost.

The magic is that **the same actions re-plan into different behavior as the world changes.** Unarmed? The plan becomes *move to weapon → pick up → load → approach → attack*. Already armed? *approach → attack*. No grenade to flush the enemy? *no plan exists*, so the agent falls back to another goal. None of these branches were scripted — they *emerge* from the action definitions.

GOAP debuted in ***F.E.A.R.*** **(2005)** and remains a benchmark: its soldiers flush the player from cover, flank, and coordinate suppressing fire, all from a compact action set plus a planner. Players swore the AI was "cheating" because it was so adaptive; it was just re-planning.

**Usage:** enemies and NPCs whose situations vary too much to script every combination — combat AI, immersive-sim characters, agents that use tools and the environment. **Limitations:** planning costs more CPU than a BT (mitigated by planning infrequently and caching); designing a clean, orthogonal action set is hard; and the emergent behavior, while flexible, is harder to *guarantee* than an authored tree.

### ▶ Run it

- [`samples/classic/goap_planner.py`](../samples/classic/goap_planner.py) — a F.E.A.R.-style soldier whose goal is "enemy eliminated," solved by A\* over world states. Watch it produce a long plan when unarmed, a short plan when already armed, and *no plan* when the world makes the goal unreachable — pure runtime replanning.

## 6. Movement I — Steering & Flocking

Deciding *what* to do is only half the job; the agent must then *move* convincingly. The classic movement toolbox starts with **steering behaviors** (Craig Reynolds) — small, composable rules that each produce a steering force, blended into smooth, organic motion: **seek, flee, arrive, pursue, evade, wander, obstacle-avoidance.**

The most famous steering result is **flocking**, or **Boids** (Reynolds, 1986/87), the standard way to move a *group* of simple agents — bats, rats, fish, birds, zerglings, a cloud of drones. Each agent steers using only its **local** neighbors via three rules:

1. **Separation** — steer away from crowding (don't collide).
2. **Alignment** — steer toward the average heading of neighbors.
3. **Cohesion** — steer toward the average position of neighbors (stay together).

Add a fourth **seek** rule toward the player and the swarm *hunts as a group*. The crucial insight is that there is **no central controller**: the coordinated, lifelike motion of the whole flock **emerges** from many agents each following identical local rules. This is cheap, scalable, and organic — the opposite of scripting every unit.

**Concrete games:** *Half-Life* (1998) used boids for flying creatures; countless RTS games flock unit groups so they move naturally instead of overlapping; the *Batman: Arkham* games swarm bats with flocking; modern engines (Unity, Unreal) ship steering-behavior systems that blend on top of pathfinding.

**Usage:** groups of cheap enemies, ambient wildlife, crowds, formations — usually combined with a pathfinding "leader" the group follows. **Limitations:** emergent behavior is hard to author precisely (you tune weights and hope); naïve implementations are O(n²) because every agent checks every other, so large flocks need spatial partitioning (grids, quad-trees); and boids don't avoid walls on their own — they're blended with obstacle avoidance or pathfinding.

### ▶ Run it

[`samples/flocking/flocking.py`](../samples/flocking/flocking.py) — 40 boids self-organize from separation, alignment, and cohesion, then converge on the player as a coherent swarm, with no central coordinator.

## 7. Movement II — Pathfinding with A\*

A "follow" or "chase" enemy must navigate *around obstacles* to reach a target. The workhorse of game navigation is **A\*** ("A-star"; Hart, Nilsson & Raphael, 1968), a best-first graph search that is both optimal and efficient. A\* expands the node that minimizes

```
f(n) = g(n) + h(n)
```

where **g(n)** is the known cost from the start to *n*, and **h(n)** is a **heuristic** estimate of the remaining cost from *n* to the goal (typically Manhattan distance on a grid, or straight-line distance). If the heuristic never *overestimates* the true remaining cost (it is **admissible**), A\* is guaranteed to find the shortest path — and the closer the heuristic is to the truth, the fewer nodes it explores.

Games run A\* over three kinds of graph:
- **Grids** — simplest; every cell is a node. Produces "blocky" paths that usually need smoothing.
- **Waypoint graphs** — hand- or auto-placed nodes connected by walkable links.
- **Navigation meshes (navmeshes)** — the modern standard: the walkable floor is decomposed into convex polygons, so paths are found over a handful of big regions instead of thousands of tiny cells. Unity's *NavMesh* and Unreal's *Navigation System* are navmesh-based.

**Chasing a moving target** is A\* plus a *re-planning policy*: recompute every tick (simple, costly), on a timer, or only when the target has moved far enough. For hundreds of units, studios use **hierarchical pathfinding** (plan over regions, then within them) and **flow fields** (compute one direction field the whole army follows).

**Concrete games:** essentially every game with navigation — *StarCraft*, *Age of Empires*, tower-defense creeps, stealth-game guards returning to post, open-world companions. **Usage:** any agent that must reach a point through a non-trivial map. **Limitations:** cost scales with map size and agent count; naïvely re-planning every frame for many chasers is expensive; dynamic obstacles (opening doors, other units) require re-planning or local avoidance; and grid paths need smoothing to look natural.

### ▶ Run it

[`samples/follow/pathfinding_astar.py`](../samples/follow/pathfinding_astar.py) — an enemy routes around a wall to a goal, then chases a fleeing player by re-planning an A\* path every tick.

## 8. Adversarial Search — Minimax, Alpha-Beta & MCTS

For **two-player, perfect-information** games — chess, checkers, Connect Four, Go, tic-tac-toe — the classic AI *searches the game tree*: it looks ahead at possible moves, counter-moves, and their consequences.

### Minimax and Alpha-Beta

**Minimax** assumes both players play optimally. One player (MAX) tries to maximize the position's score; the opponent (MIN) tries to minimize it. The algorithm recursively explores moves to some depth, evaluates the resulting positions, and backs the values up the tree — MAX picking the highest, MIN the lowest — to choose the move that leads to the best guaranteed outcome.

The catch is that game trees explode: chess has ~35 legal moves per turn, so looking *d* moves ahead is ~35^d positions. **Alpha-Beta pruning** is the essential optimization: it tracks the best score each player is already assured of (α for MAX, β for MIN) and **prunes** any branch that cannot possibly change the decision. It returns the *identical* answer as plain minimax while often exploring an order of magnitude fewer nodes — in our tic-tac-toe sample, alpha-beta cuts node count by **~96%**. ***Deep Blue***, which beat world chess champion Garry Kasparov in 1997, was alpha-beta minimax with a hand-crafted evaluation function running on custom hardware.

### Monte-Carlo Tree Search (MCTS)

For games too big to search deeply, or where a good evaluation function is hard to write (famously **Go**, with ~250 moves per turn and 10^170 positions), minimax stalls. **MCTS** wins by **sampling** instead of exhaustive search. It grows a lopsided tree by repeating four steps thousands of times:

1. **Select** — from the root, descend to a promising leaf using **UCB1**, a formula that balances *exploitation* (moves that have scored well) against *exploration* (moves tried only rarely).
2. **Expand** — add a new child node for an untried move.
3. **Simulate** — play the rest of the game with *random* moves (a "rollout") to a win/loss/draw.
4. **Backpropagate** — push that result back up the path, updating every node's win/visit statistics.

After the budget is spent, the most-visited move is chosen. MCTS needs **no evaluation function — only the rules** — and naturally concentrates effort on the moves that matter. It was the core of strong Go programs and, fused with deep neural networks that guided selection and replaced random rollouts, became ***AlphaGo*** (2016).

**Usage:** board games, card games, turn-based tactics, and any decision with a simulatable model of outcomes. **Limitations:** minimax needs a good evaluation function and branching-factor discipline; MCTS needs many simulations (compute) and a fast simulator, and in its pure form struggles with very long games or huge branching without neural guidance.

### ▶ Run it

- [`samples/classic/minimax_tictactoe.py`](../samples/classic/minimax_tictactoe.py) — perfect, unbeatable tic-tac-toe; plays itself to the inevitable draw, beats a random player ~199/200, and prints the node counts that show alpha-beta's ~96% saving.
- [`samples/classic/mcts_connect_four.py`](../samples/classic/mcts_connect_four.py) — MCTS plays Connect Four with 500 rollouts per move, prints its per-move visit statistics ("thinking"), and reliably beats a random opponent.

## 9. Spatial Reasoning — Influence Maps & Procedural Content

Two more classic tools round out the toolbox.

### Influence maps

An **influence map** is a grid overlaid on the world where each cell holds a number summarizing "who controls this area." Friendly units stamp positive influence that spreads to nearby cells; enemies stamp negative; you sum them. The result is a cheap, queryable picture of the tactical situation:

- **High-friendly cells** = safe staging areas.
- **Zero-crossings** (where friendly meets enemy influence) = the **front line**.
- **High-enemy cells** = danger; route around them.
- Subtracting a "threat" map from a "goal desirability" map tells a unit *where* to go.

Influence maps power RTS decisions (where to attack, where the front is, which base is weak), FPS tactical positioning (find cover with low enemy influence), and MOBA/strategy target selection. They're a form of spatial utility scoring — cheap to compute, easy to reason about, and used constantly in strategy games.

### Procedural Content Generation (PCG)

**PCG** uses algorithms to *generate* content — levels, maps, dungeons, loot, terrain, quests — rather than hand-placing it. It ranges from the fully random dungeons of ***Rogue*** (1980) and ***Spelunky***, to the noise-based worlds of ***Minecraft***, to the 18-quintillion procedurally-generated planets of ***No Man's Sky*** (2016). Techniques include random layout grammars, Perlin/Simplex noise for terrain, wave-function-collapse for tile maps, and increasingly **PCG via machine learning (PCGML)** and generative models. PCG buys near-infinite content and replayability at the cost of control — the classic tension is generating content that is not just varied but *good*, which is why most shipping PCG mixes generation with hand-authored constraints and set pieces.

---

# Part III — Genre Deep-Dives

Part II gave you the toolbox. Part III shows how real, named games combine those tools into the AI you actually experience. Each genre has evolved its own idioms — and its own place where the classic toolbox handed off to learning.

## 10. Racing AI — Mario Kart to Gran Turismo Sophy

Racing is the perfect genre to see classic and modern AI side by side, because two very different racing games sit at opposite ends of the spectrum: the arcade chaos of *Mario Kart* and the simulation precision of *Gran Turismo*.

### The classic racing stack

Nearly every racing opponent, from arcade to sim, is built from three authored layers:

**1. The racing line as waypoints (or splines).** The track is annotated with a sequence of points forming the ideal line through corners. The AI uses a **pure-pursuit / look-ahead controller**: it always steers toward a point a little further ahead along the line, which produces smooth cornering. (Look too close and it wobbles; too far and it cuts corners.)

**2. Steering and speed control (PID).** A **proportional controller** turns the wheel in proportion to the heading error between "where I'm pointing" and "where the look-ahead point is." Braking points and per-corner target speeds slow the car for tight turns and let it accelerate on straights. More sophisticated AIs add integral and derivative terms (full PID) and a model of grip.

**3. Rubber-banding (Dynamic Difficulty Adjustment).** To keep races exciting, the AI's performance is quietly nudged based on the gap to the player: fall behind and the AI's top speed is boosted; pull ahead and it eases off. This "catch-up logic" keeps the pack tight and the finish photo-worthy.

### Case study: *Mario Kart* — fun over fair

*Mario Kart* is a masterclass in **deliberately unfair AI in service of fun.** Two systems do the heavy lifting, and neither is about driving skill:

- **Rubber-banding speed.** Trailing CPU karts get a real top-speed boost; leaders are slowed. The pack compresses no matter how well or badly you drive, so every race stays tense to the finish line. Pushed too far this feels cheap ("the AI cheats"), which is why the tuning is so delicate.
- **Position-based item distribution.** This is the clever part. The item you roll from a box depends on your **race position**, not pure chance. Front-runners roll weak, defensive items (bananas, single green shells); back-markers roll powerful **catch-up items** (triple mushrooms, stars, Bullet Bills, and the infamous **blue/spiny shell** that homes in on whoever is in 1st place). The item table *is* a dynamic-difficulty system: it hands comebacks to the players who need them and denies runaway leaders the tools to extend their lead.

On top of distribution sits a small **item-use AI**: hold a shell behind you as a shield when someone's close; fire the blue shell when you're *not* in first; save a mushroom boost for a shortcut. The driving AI underneath can be quite simple because the *items* create the drama.

> **The lesson:** in an arcade racer, most of the "AI" isn't in the driving at all — it's in an item economy engineered to manufacture close, chaotic, funny races.

### Case study: *Gran Turismo 7* / **Sophy** — where AI learned to race

At the opposite pole is the sim. For decades, *Gran Turismo*'s built-in opponents were classic waypoint-followers — competent but robotic, and easy for experts to read. Realistic wheel-to-wheel racing — choosing when to brake at the limit of grip, how to defend a line, when to make a passing dive stick without causing a collision — turned out to be extremely hard to hand-author.

So Sony AI trained it instead. **Gran Turismo Sophy** (published in *Nature*, 2022) is a **deep reinforcement-learning** agent (Chapter 14) that learned to drive *Gran Turismo* by trial and error over enormous simulated mileage, rewarded for lap time while penalized for going off-track or colliding. Sophy **beat the world's best human GT drivers** — and, notably, learned not just raw speed but **racecraft and sportsmanship**: tactical overtaking, blocking, and respecting racing etiquette (the reward was carefully shaped to discourage dirty driving). A version was later made playable inside *Gran Turismo 7*, so ordinary players could race a super-human learned opponent.

Sophy is the clearest example in this book of *why* studios reach for learning: the classic waypoint stack had a ceiling that hand-authoring could not break through, and RL broke through it.

### Also notable

- ***Forza Motorsport* Drivatar** — an **imitation-learning** system (Chapter 15) that learns *individual human players'* driving styles from their recorded laps, so your friends' "Drivatars" race in your game even when they're offline. Human-like, not super-human.

### Usage & limitations

The classic stack (waypoints + PID + rubber-banding) is cheap, controllable, and still ships in most racing games; its limits are robotic-looking lines, brittleness on unexpected geometry (a spun-out car, a shortcut), and rubber-banding that feels unfair if overdone. Learned drivers (Sophy) achieve human-plus racecraft but demand a fast simulator, huge training compute, careful reward shaping, and — for a *shipping* opponent — deliberate weakening so they're fun rather than demoralizing to race.

### ▶ Run it

- [`samples/racing/racing_ai.py`](../samples/racing/racing_ai.py) — the classic stack: waypoint following, PID steering, and rubber-banding keeping the gap to a "player" small.
- [`samples/racing/mario_kart_items.py`](../samples/racing/mario_kart_items.py) — six karts race with **position-based item distribution** and rubber-banding; watch back-markers roll blue shells and stars to close the gap, and the pack finish within a few car-lengths.
- [`samples/rl/sophy_racing_qlearn.py`](../samples/rl/sophy_racing_qlearn.py) — a *Sophy-in-miniature*: a reinforcement-learning agent with **no programmed racing line** learns a speed profile — braking before corners, flooring the straights — purely from reward, beating a naive "full throttle" driver that crashes.

## 11. Shooter AI — Doom to Rainbow Six & Apex

The first-person shooter drove decades of combat-AI innovation. Watching it evolve is like watching the classic toolbox get stacked ever higher.

### The lineage

**1993 — *Doom*: the state machine and line-of-sight.** *Doom*'s monsters are pure finite state machines. Each has states like *idle, walking, attacking, pain, dying*, and simple transitions. Two ideas gave them life far beyond their simplicity:
- **Line-of-sight and sound activation** — a monster "wakes" when it can see the player or hears gunfire, so the world feels reactive.
- **Monster infighting** — if one monster accidentally hits another (with a stray fireball), the victim turns on the attacker. This tiny rule produces emergent chaos players still exploit, and it cost almost nothing to implement. *Doom* is the definitive proof that **great feel comes from simple rules plus good telegraphing**, not complex AI. (Movement was crude — monsters largely walked toward the player with basic obstacle handling, no real pathfinding.)

**1998 — *Half-Life*: squads and the illusion of tactics.** *Half-Life*'s marines appeared to flank, retreat, call out, and coordinate. Under the hood it was a schedule/task system with squad slots, but the *perception* of tactical intelligence was a huge leap — and it was driven as much by **audio barks** ("He's flanking! Cover me!") as by the underlying logic. This cemented **telegraphing** as core craft: tell the player what the AI is doing and they'll credit it with more intelligence than it has.

**2001–2004 — *Halo*: behavior trees and the "30 seconds of fun."** Bungie built *Halo*'s enemies on behavior trees with layered behaviors, morale, and vehicles, tuned around repeatable, readable combat encounters. *Halo 2* popularized behavior trees industry-wide.

**2005 — *F.E.A.R.*: GOAP and the high-water mark of combat AI.** Widely regarded as the best combat AI of its era, *F.E.A.R.*'s replica soldiers used **GOAP** (Chapter 5) over a **cover system**. Given the goal "kill the player" and actions with preconditions/effects, the planner produced emergent **fire-and-maneuver**: one soldier **suppresses** (keeps the player pinned behind cover) while others **flank** to a new angle, throw grenades to flush the player out, and retreat when exposed. Crucially, the soldiers *narrated* it ("Flanking!", "Suppressing!"), so players read genuine tactics into what was, mechanically, a planner plus cover-point selection. This suppress-and-flank loop is the core of modern shooter squad AI.

**2015–present — destruction, gadgets, and battle royale.**
- ***Rainbow Six Siege*** is defined by its **fully destructible environment**: walls, floors, and ceilings can be breached, so "cover" and sightlines are dynamic and player-created. The design challenge is AI (in Terrorist Hunt / training modes) and, more importantly, level and gadget systems that must reason about a space that *changes shape* mid-round — reinforced walls, breach charges, drones for reconnaissance, and destructible line-of-sight. It's tactical AI where the map itself is a variable.
- ***Apex Legends*** and battle-royale shooters are primarily player-vs-player, so their notable "AI" is different: **bots for onboarding** new players, plus the systems around aim assist, movement, and matchmaking. (The studio's earlier *Titanfall* games featured "grunt" AI as fodder that made players feel powerful.) The broader battle-royale trend also revives the idea of an **AI Director** — see below.

**2008 — *Left 4 Dead*: the AI Director.** Worth a special mention because it reframes what game AI *is*. Valve's **AI Director** isn't an opponent; it's an invisible **dramatist** that watches the players' stress and dynamically paces the experience — spawning zombie hordes, distributing health and ammo, and orchestrating lulls and crescendos — to keep every playthrough tense but fair. It's dynamic difficulty as *storytelling*, and it influenced the pacing systems of countless later games.

### What actually powers shooter AI

Peel back any of these and you find the same stack from Part II:
- **Line-of-sight** checks (can I see the target?) — the gate on almost every decision.
- **Cover selection** — scoring nearby positions by how well they block enemy sightlines (utility/influence).
- **Suppression** — a soldier that fires to *pin* the target, dropping the target's effectiveness and forcing them to break line-of-sight.
- **Squad coordination** — roles (anchor/suppressor vs. flanker) so the group performs **fire-and-maneuver** rather than clumping.
- **Telegraphing** — animation and voice that make the above legible.

### Usage & limitations

This stack gives readable, tunable, satisfying combat — the default for single-player and co-op shooters. Its limits are the usual ones for authored AI: it's reactive and exploitable once players learn the patterns, cover systems need well-authored cover points (or expensive runtime cover generation), and truly novel tactics require either painstaking authoring or learning. Fully learned FPS combat agents exist in research but are rare in shipping games, partly because super-human aim is trivial for a machine and must be *removed* to stay fun.

### ▶ Run it

[`samples/fps/tactical_fps.py`](../samples/fps/tactical_fps.py) — a two-soldier squad performs **fire-and-maneuver** on a dug-in player: the **anchor** takes a firing position and **suppresses** (pinning the player, who tunnel-visions on the visible threat), while the **flanker** uses a **concealment-weighted path** to reach a different bearing and deliver the kill. Line-of-sight, cover, suppression, and flanking — the whole *Doom → F.E.A.R. → modern* stack — in one runnable file.

## 12. Strategy AI — Civilization, Red Alert & StarCraft

Strategy games demand the broadest AI of any genre: an opponent must manage an **economy**, choose a **build order and tech path**, position an **army**, and make **tactical** decisions in battle — all at once, often across a huge map. There is no single algorithm; there is a **stack of managers**, each a classic technique from Part II.

### Turn-based 4X: *Civilization*

A *Civilization* AI runs, above all, on **Utility AI** (Chapter 5). Every turn, for every city, it scores everything it could build against the empire's needs and picks the best; at the empire level it scores research options, diplomatic moves, and where to settle or attack. Add pathfinding for units, influence maps for the front line, and simple tactical rules for combat, and you have a 4X opponent.

**The open secret of *Civ* difficulty.** Here is something every strategy player should understand. On higher difficulty levels, the *Civilization* AI is **not smarter — it gets bonuses.** Extra starting units, cheaper buildings and units, production and science bonuses, happiness/maintenance discounts, and more aggression. The decision logic is essentially the *same* across difficulties; the higher levels simply hand the AI a **resource handicap** in its favor. This is the honest, pragmatic truth of most strategy-game difficulty: a genuinely *smarter* strategic AI is extremely hard to author (the state space is astronomical and the reasoning is long-horizon), so studios scale challenge with bonuses instead. It works, it's predictable, and it's cheap — even if veterans grumble that "the AI cheats."

### Real-time strategy: *Command & Conquer* / *Red Alert*

Classic RTS AI (*C&C*, *Red Alert*, *Warcraft*, *Age of Empires*) is a set of managers running every tick:

- **Economy manager** — send harvesters to gather resources; keep power positive (a deficit causes brownouts); expand refineries.
- **Build-order / tech manager** — a prioritized policy: "what do I lack most?" Build power, then economy, then the tech buildings that unlock your chosen units.
- **Production manager** — pump out combat units, limited by production capacity (a real build queue), so armies grow gradually.
- **Tactical manager** — mass an army, then commit it in **attack waves** when it's strong enough; each engagement spends the army, so you rebuild and attack again.

And, exactly as in *Civ*, **classic RTS AI famously cheats a little** — on harder difficulties it gets resource bonuses and often **full map vision** (it can "see" your base without scouting), because fair, fog-of-war-respecting strategic play is so hard to author. *Red Alert*'s skirmish AI, the *Age of Empires* computer players, and the *StarCraft* built-in AI all lean on such handicaps.

The interesting design consequence is that RTS AI is a **balance problem**: a rush doctrine (cheap units, early pressure) and an economy doctrine (greedy expansion, tech to powerful units) each beat the other under different tunings. Watching the two collide, and seeing that the winner is a knob-tuning question rather than an intelligence question, is the best way to feel why studios spend so long on it.

### The frontier: *StarCraft II* and AlphaStar

*StarCraft II* is the grand challenge of strategy AI: real-time, hidden information (fog of war), a vast action space, and long-horizon planning where an early economic choice pays off ten minutes later. Hand-authored AI plateaus well below expert human play. In 2019, DeepMind's **AlphaStar** — deep reinforcement learning with imitation-learning bootstrapping and league-style self-play (Chapter 14) — reached **Grandmaster** level, among the top handful of percent of human players. It's the strategy-genre counterpart to Sophy and OpenAI Five: the problem the classic toolbox couldn't fully crack, cracked by learning.

### Usage & limitations

The manager stack is how essentially all shipping strategy games build their AI: it's transparent, tunable, and fast enough for thousands of units. Its limits are real — the tactical AI is often the weak point (mediocre army micro, exploitable attack patterns), long-horizon strategy is shallow, and difficulty leans on bonuses rather than skill. Learned strategy AI (AlphaStar) reaches far higher but is astronomically expensive to train and, like all super-human agents, must be *dialed back* to be an enjoyable opponent.

### ▶ Run it

- [`samples/strategy/civ_ai.py`](../samples/strategy/civ_ai.py) — a 4X empire AI that builds each city by **utility scoring**, researches a tech tree, and expands — and directly demonstrates the difficulty-bonus truth by running the **same brain** as a fair "Prince" empire and a bonus-boosted "Deity" empire, so you watch the *handicap*, not intelligence, decide the game.
- [`samples/rts/command_conquer_ai.py`](../samples/rts/command_conquer_ai.py) — a *Red Alert*-style skirmish where an **infantry rush** doctrine fights an **economy → tanks** doctrine, each a full stack of economy/build-order/production/tactical managers, and the winner comes down to tuning — the RTS balance problem in miniature.

---

## 13. Open-World AI — GTA, Streaming & the Performance Budget

Open-world games — *Grand Theft Auto*, *Red Dead Redemption*, *Cyberpunk 2077*, *Assassin's Creed* — pose a problem no other genre does: they must make a **whole living city** feel real, with hundreds of pedestrians, cars, and animals visible at once, in a seamless map you can drive across for ten minutes without a loading screen. This chapter uses the *GTA* series as the worked example, because it is the definitive open-world AI showcase, and answers four questions: how are the NPCs designed, how do they fit a giant world and a huge crowd into a fixed memory and frame budget, whether generative AI can live there, and how you balance any AI you add against performance.

### How the NPCs are designed

The key realization is that a *GTA* crowd is not hundreds of hand-placed characters. It is a **population system** that continuously **spawns NPCs around the player and despawns them out of sight**, keeping only a bounded number "alive" at any moment. Where they spawn, and what kind, is driven by the zone (a beach, a business district, a slum), time of day, and a **density budget**. Walk down a street and the pedestrians ahead are being created just outside your view and quietly deleted behind you — the city is an illusion maintained in a bubble around you.

Each pedestrian ("ped") and vehicle runs an authored decision architecture built from the techniques in Part II:

- **A hierarchical task system.** Rockstar's RAGE engine drives peds with a tree of **tasks** (wander, cross the road, flee, take cover, enter vehicle) — effectively a behavior-tree/HTN hybrid where a high-level task expands into sub-tasks. This is the FSM/behavior-tree material of Chapter 4, scaled up.
- **Scenarios.** The world is seeded with **scenario points** — annotations that say "a ped here can sit on this bench / lean on this wall / sweep / sunbathe / drink coffee." Ambient NPCs claim a nearby scenario and play its authored behavior, which is why the city looks *purposeful* rather than full of aimless walkers. Scenarios are a form of world-baked utility: cheap, designer-authored, location-specific behavior.
- **Navigation on two graphs.** Peds path over a **navmesh** (Chapter 7); vehicles follow a **road/path-node network** — a graph of lane nodes with speeds, links, and junctions — with car-following, lane changes, and traffic-light obedience layered on top.
- **Perception and an event system.** Peds have senses (sight cones, hearing) and an **event queue**. A gunshot, a car mounting the curb, or a punch generates an event that **interrupts** the current task with a higher-priority reaction — flee, cower, fight back, or call the police. This event-driven interruption is what makes the world feel reactive.
- **The Wanted system.** The police are the game's showcase combat/pursuit AI: response escalates with wanted level, officers pathfind to you, use cover-based combat (Chapter 11), and — when they lose sight of you — switch to a **search** behavior around your **last-known position**, exactly the "when to re-plan / where did they go" problem of Chapter 7.

None of this is one clever algorithm. It is the **classic toolbox, integrated and budgeted** — which is the real lesson of open-world AI.

### Fitting a giant world and a huge crowd into a fixed budget

A console has a fixed amount of memory and ~16 ms per frame. A *GTA* map is far too large to hold in memory and has far too many potential agents to simulate every frame. Four ideas make it possible, and they are the heart of open-world engineering:

1. **Streaming.** The world is cut into cells/blocks, and assets — geometry, textures, collision, audio, and AI data — are **streamed off disk into memory as the player moves**, while cells left behind are evicted. Only a region around the player is ever resident. A dedicated **streaming system** predicts what you'll need next (based on position and velocity) and loads it just in time, which is how the map has no loading screens.
2. **Level of Detail (LOD) — for geometry *and* AI.** Near the player, the city is full-detail and NPCs are fully simulated. Farther out, geometry drops to cheaper **LOD models** and eventually flat imposters; and — crucially — **AI runs at "level of detail" too**. This **LOD AI** is the single most important idea: a distant car isn't a full physics-and-AI vehicle, it's a cheap "dummy" that slides along a path node; a distant crowd is a few animated billboards. Full simulation is spent only where the player can actually perceive it.
3. **Time-slicing.** Even the near NPCs are not all updated every frame. Their AI updates are **spread across frames** — a fraction of the agents "think" each frame on a rotating schedule, and distant ones think less often. This turns an unaffordable "N agents × every frame" into a fixed per-frame cost.
4. **Density caps and culling.** Hard **caps** limit how many peds/vehicles are active at once (tuned per zone and per platform), and spatial partitioning plus occlusion culling keep queries and rendering bounded. The population system spawns up to the cap and no further.

Put together: **stream a bubble of world around the player, simulate at full fidelity only what's close and visible, fake everything else with LOD, and spread the remaining work across frames.** That is how a "living city" fits in a fixed budget.

### Can we use generative (LLM) AI agents in an open world?

Yes — but not the way people first imagine. You **cannot** run an LLM for a whole *GTA* crowd: with hundreds of NPCs spawning and despawning every minute, a network round-trip and per-token cost *per NPC per line* is impossible on both latency and money, and it would break the population/streaming model entirely. The realistic architecture is **tiered and hybrid**:

- **Most NPCs stay classic.** Ambient peds keep their cheap task/scenario AI — they don't need language.
- **A few "hero" NPCs get generative AI.** A mission character, a recurring shopkeeper, a companion — a handful of important characters — can be LLM-driven for open-ended dialogue, exactly the persona + memory + tools pattern of Chapter 16.
- **Use LLMs offline as a content tool.** Generate barks, ambient chatter, and quest text *ahead of time*, review it, and **bake it in** — you get generative *variety* with zero runtime cost or risk.
- **Right-size the model.** A small **on-device** model can serve many nearby NPCs with low latency; a large **cloud** model is reserved for the few characters that justify it. **Cache** aggressively (identical situations reuse responses).
- **Bound the LLM's authority with tools.** As in Chapter 16, let the character *talk* freely but only *act* through a small, validated set of game functions — so it can never break the simulation, the economy, or the rating.

The blockers are the same as anywhere: latency, cost at scale, consistency with canon, determinism for QA, and content safety. Middleware such as **NVIDIA ACE**, **Inworld AI**, and **Convai** exists precisely to make the "a few talkable NPCs" tier practical, and mods have already put GPT-driven NPCs into *GTA V* as proof of concept.

### Balancing performance against the AI you add

Every technique above is really one discipline: **spend the frame budget where the player will notice, and nowhere else.** When you add *any* AI to a game — a smarter enemy, a learned policy, an LLM companion — apply the same playbook:

- **Give AI a frame budget.** Decide up front that AI may use, say, 2–3 ms of the 16 ms frame, and design to it. Profile against it.
- **Tier by importance and distance (LOD AI).** Full brains for on-screen, gameplay-relevant agents; cheap approximations or none for the rest. This one idea buys the most.
- **Time-slice and stagger.** Don't run every agent every frame; amortize expensive decisions (planning, re-pathing, inference) over many frames and across agents.
- **Go async and off the main thread.** Run pathfinding, planning, and model inference on worker threads or a frame or two behind, so a spike never stalls rendering.
- **Cache and precompute.** Bake navmeshes, influence maps, and cover points offline; memoize plans and LLM responses; reuse results across similar agents.
- **For learned models, right-size and batch.** Quantize and run small models on-device; **batch** inference calls; run them at a lower frequency than the render loop. For LLM NPCs specifically: stream tokens so dialogue *starts* fast, cap context length, and prefer many cheap calls to a small model over few calls to a giant one.
- **Degrade gracefully.** When the budget is tight (a huge firefight, a dense crowd), *reduce AI fidelity* — fewer thinking agents, simpler behaviors — rather than dropping frames. Players forgive a slightly duller distant crowd; they don't forgive stutter.

The through-line from *Doom*'s state machines to a hypothetical LLM-driven *GTA* companion is the same: **match the intelligence you pay for to the attention the player can actually give it.**

### ▶ See it

The interactive companion includes an **Open-World AI** viewport that visualizes exactly this: the player at the center of concentric **LOD-AI rings** (full-sim → simplified → streamed-out), NPCs spawning near you and despawning far away against a **density cap**, and a live **frame-budget meter** you can push by widening the full-simulation radius or toggling "LLM hero NPCs" — watch the cost, and the graceful degradation, in real time.

---

# Part IV — Modern, Learned AI

The techniques in Part IV **learn** behavior from experience or data instead of having it authored. They solve problems the classic toolbox genuinely can't — but they cost data, compute, and predictability, which is why they supplement rather than replace the classics.

## 14. Reinforcement Learning

In **reinforcement learning (RL)**, an agent learns by **trial and error** to maximize cumulative **reward**. It builds a **policy** — a mapping from states to actions — guided only by a reward signal from the environment, with no examples of "correct" play. The foundational algorithm is **Q-learning**, which learns a value **Q(s, a)** — the expected long-term reward of taking action *a* in state *s* — via the update:

```
Q(s,a) ← Q(s,a) + α · [ r + γ · maxₐ' Q(s',a') − Q(s,a) ]
```

where **α** is the learning rate and **γ** discounts future reward. Store Q in a table for small problems; replace the table with a **neural network** and you get **Deep Q-Networks (DQN)**. Policy-gradient methods like **PPO**, combined with **self-play** (agents training against copies of themselves), power the headline results:

| System | Year | Game | Method |
|--------|------|------|--------|
| **AlphaGo / AlphaZero / MuZero** | 2016– | Go, chess, shogi | Deep RL + MCTS, self-play |
| **OpenAI Five** | 2019 | *Dota 2* | PPO self-play, 5-agent team |
| **AlphaStar** | 2019 | *StarCraft II* | RL + imitation + league self-play |
| **Gran Turismo Sophy** | 2022 | *Gran Turismo* | Deep RL with shaped reward |

**Usage.** Super-human or highly adaptive opponents; agents for games too complex to script (racing physics, RTS/MOBA micro); automated **playtesting and balancing**; tuning NPC skill. RL works best when you have a **fast simulator** and a **clear reward**.

**Limitations — and they are serious.**
- **Sample-hungry and expensive.** OpenAI Five trained on the equivalent of *centuries* of gameplay per day; almost no studio can afford that compute.
- **Reward design is treacherous.** A poorly specified reward produces **reward hacking** — the agent exploits a loophole instead of playing "properly" (e.g., a boat-racing agent that learned to spin in circles collecting points instead of finishing).
- **Unpredictable and hard to debug.** A learned policy is a black box; you cannot easily guarantee it won't do something absurd in a situation it never saw.
- **Often *too good*.** A super-human bot is not fun. Shipping RL opponents (like Sophy in *GT7*) must be **deliberately weakened and tuned** to be enjoyable.
- **Integration cost.** It needs a training pipeline, a simulator, and heavy QA — a large investment versus a state machine.

### ▶ Run it

- [`samples/rl/q_learning.py`](../samples/rl/q_learning.py) — tabular Q-learning discovers the optimal path through a maze (avoiding a pit) purely from reward, then prints the learned policy.
- [`samples/rl/sophy_racing_qlearn.py`](../samples/rl/sophy_racing_qlearn.py) — the same algorithm applied to *driving*: with no programmed racing line, the agent learns a speed profile that brakes for corners and accelerates on straights — Sophy's core idea at teaching scale.

## 15. Imitation Learning & Other ML

Not all learned AI is reward-driven. **Imitation learning (behavior cloning)** trains a model to *copy human play* from recorded data — no reward function, just examples. The celebrated shipping example is ***Forza*** **Drivatar**: it learns *individual players'* racing styles from their laps, so your friends' AI "ghosts" race with their real habits and quirks even when they're offline. The result is **human-like** opponents (mistakes and all), which is often more fun than the flawless lines of an RL agent.

Other ML quietly shapes games without ever being the "opponent":
- **Learned animation** — motion matching and neural locomotion controllers pick or blend animation from a huge library for natural movement.
- **Player modeling** — churn prediction, matchmaking, skill rating, and dynamic difficulty.
- **Cheat and toxicity detection**, **QA/playtesting bots**, and **PCGML** (machine-learned content generation).

The practical frontier is **hybrid systems**: a behavior tree for structure, utility scoring for decisions, learned sub-policies for hard motor skills (aiming, driving), an influence map for tactics, and an LLM for dialogue — *each technique where it is strongest.* No serious game is "all classic" or "all learned."

## 16. Generative AI Agents (LLMs)

The newest genre of game AI puts a **Large Language Model (LLM)** at the heart of a character or agent. Instead of a fixed dialogue tree, the NPC has:

- a **persona** — a system prompt defining who it is, its knowledge, and its voice;
- **memory** — recent conversation, and sometimes long-term memory stores it can retrieve from;
- **tools / function-calling** — so its words become *real game actions*: give a quest, open the shop, change disposition, move, attack.

The player can now say **anything**, and the NPC responds in character and acts on the world. Give many such agents a shared world and **emergent social behavior** appears. The seminal demonstration is **"Generative Agents"** (Park et al., Stanford, 2023): 25 LLM-driven agents in a sandbox town ("Smallville") formed relationships, spread news, and autonomously organized a Valentine's Day party — none of it scripted. Middleware like **NVIDIA ACE**, **Inworld AI**, and **Convai** now brings voiced, LLM-driven NPCs into real engines.

**Usage.** Open-ended, replayable dialogue; dynamic quests; companions with personality and memory; natural-language interaction for accessibility; and — powerfully — as an *offline design tool* to generate content (barks, quests, lore) that is then reviewed and baked in.

**Limitations.**
- **Hallucination & consistency.** LLMs invent facts, break lore, and contradict themselves — dangerous for canon and narrative.
- **Control & safety.** Free-form output can be off-tone, exploited by players ("jailbreaks"), or say things the studio never approved. The essential discipline is to **bound the LLM's authority with tools**: let it *talk* freely but only *act* through a small, validated set of functions, so it can never do something the game doesn't permit.
- **Latency & cost.** A network round-trip per line adds latency, and per-token cost adds up at scale; on-device models trade quality for speed.
- **Determinism & testing.** Non-deterministic output is hard to QA and to reproduce for bug reports.
- **Grounding.** The LLM must be tied to real game state via tools and memory, or it's just chatter with no gameplay consequence.

### ▶ Run it

[`samples/generative/generative_npc.py`](../samples/generative/generative_npc.py) — an LLM blacksmith that improvises in-character dialogue **and** drives real game state through tool calls (give quest, check inventory, adjust disposition). It uses Anthropic's Claude (`claude-opus-5`) if an API key is present, and otherwise runs a fully **offline mock** through the same code path, so you can study the persona/memory/tools architecture with zero setup.

---

# Part V — Practice

## 17. Choosing an Approach

There is no "best" technique — only the best fit for a specific job under the constraints of Chapter 1. Use this as a starting decision guide:

| If you need… | Reach for | Why |
|--------------|-----------|-----|
| A guard/enemy with clear, authorable behavior | **FSM / Behavior Tree** | Predictable, cheap, designer-controlled |
| An agent juggling many competing needs | **Utility AI** | Smooth trade-offs from tunable scores |
| Complex, adaptive reactive tactics | **GOAP** | Plans emerge from goals + actions |
| A group that moves organically | **Flocking / steering** | Emergent coordination, no central brain |
| To reach a point through a map | **A\* / navmesh** | Optimal, well-understood |
| A strong opponent for a board/turn game | **Minimax + α-β, or MCTS** | Optimal lookahead / sampling search |
| To know "who controls where" | **Influence maps** | Cheap spatial tactical picture |
| A believable arcade racing opponent | **Waypoints + PID + rubber-banding** | Close, fun, controllable races |
| Endless levels/maps/loot | **PCG** | Infinite content, replayability |
| Super-human or unscriptable skill | **Reinforcement learning** | Learns what you can't author — at a cost |
| Human-like opponents from data | **Imitation learning** | Copies real players' style |
| Open-ended dialogue & emergent characters | **Generative / LLM agents** | Say/do anything, in character |

**Rules of thumb.**
1. **Start with the simplest technique that meets the design goal.** A state machine you can ship beats a neural network you can't debug.
2. **Reach for learning only when authoring is genuinely impractical** — super-human skill, unscriptable physics, open-ended language.
3. **Bound every powerful/generative agent** with tools, validation, and the ability to fall back to authored behavior.
4. **Telegraph everything.** The player only credits intelligence they can perceive.
5. **Tune for fun, not for winning.** Always.

## 18. Exercises

Work these against the companion code in [`../samples`](../samples).

**Foundations & classic toolbox**
1. In `npc/npc_fsm.py`, add an `Investigate` timeout so a guard that finds nothing returns to `Patrol` after N ticks. Then add a `Search` state that visits the last-known player position.
2. Convert the FSM's decision logic into a behavior tree. Which is easier to extend with a new "call for backup" behavior?
3. In `pacman_ghosts.py`, add a **Frightened** mode (triggered by a power pellet) in which ghosts flee — target the tile *maximizing* distance from Pac-Man. Does the classic feel return?
4. In `flocking/flocking.py`, add obstacle avoidance so the swarm flows around a wall. Then add a spatial grid so it stays fast with 500 boids.
5. In `pathfinding_astar.py`, switch the heuristic from Manhattan to Euclidean, then to *zero* (making it Dijkstra). Count nodes expanded in each case — what does the heuristic buy you?
6. In `minimax_tictactoe.py`, add **move ordering** (try center and corners first) and measure how many *more* nodes alpha-beta prunes.
7. In `mcts_connect_four.py`, vary `SIMS_PER_MOVE` from 50 to 5000 and plot win rate vs. random. Where are the diminishing returns?
8. In `goap_planner.py`, add a `Reload` action and a `weapon_empty` state, and a second goal (`retreat_to_cover`). Watch the planner switch plans.

**Genres**
9. In `racing/mario_kart_items.py`, redesign the item table so comebacks are *more* aggressive. At what point does it stop feeling fair?
10. In `sophy_racing_qlearn.py`, make one corner much tighter and retrain. Does the agent learn to brake earlier? Add a "tire wear" penalty for hard braking.
11. In `fps/tactical_fps.py`, give the player a second defensive position and a third soldier. Can the squad still coordinate a flank?
12. In `command_conquer_ai.py`, tune the constants until the *rush* wins instead of the economy. Which single number matters most?
13. In `civ_ai.py`, remove the Deity bonuses and instead try to make Deity win by *smarter* play (better utility weights). How far can you get? (This is the whole difficulty of strategy AI.)

**Modern**
14. In `q_learning.py`, add a second pit and a moving reward. Does tabular Q-learning still converge?
15. In `generative_npc.py`, add a new tool (e.g., `start_duel`) and a guardrail that prevents the NPC from giving the same quest twice.

**Open world & scale**
16. Sketch a population system: spawn NPCs around a moving player up to a density cap and despawn them beyond a radius. What's the smallest cap that still feels "alive"?
17. Add **LOD AI**: give each NPC a tier (full / simplified / dummy) based on distance to the player, and **time-slice** so only a fixed number "think" per frame. Measure the cost vs. simulating everyone every frame.
18. Design the tiering for an LLM companion in an open world: which decisions go to the LLM, which stay classic, and where do you cache? Estimate the per-minute cost at 1, 10, and 100 talkable NPCs.

## 19. Glossary

- **A\*** — best-first pathfinding minimizing `f = g + h`; optimal with an admissible heuristic.
- **Admissible heuristic** — a heuristic that never overestimates remaining cost; required for A\* optimality.
- **Behavior Tree (BT)** — a tree of Sequence/Selector/action nodes re-evaluated each tick; the AAA standard for character AI.
- **Boids** — Reynolds' flocking model: separation + alignment + cohesion.
- **Dynamic Difficulty Adjustment (DDA)** — quietly tuning challenge to the player; rubber-banding is one form.
- **Finite State Machine (FSM)** — states + event-driven transitions; the simplest decision technique.
- **Flow field** — a precomputed direction field a whole group follows toward a goal.
- **GOAP** — Goal-Oriented Action Planning; A\* over world states using actions with preconditions/effects.
- **Heuristic** — an estimate guiding search (the `h` in A\*).
- **Influence map** — a grid summarizing spatial control/threat for tactical decisions.
- **Imitation learning** — training a model to copy recorded human behavior (e.g., Drivatar).
- **Line-of-sight (LOS)** — whether one point can "see" another unobstructed; gates most perception.
- **LLM** — Large Language Model; the engine of generative NPCs.
- **LOD AI (level-of-detail AI)** — simulating near/visible agents at full fidelity and distant ones cheaply (or not at all); the key to open-world scale.
- **MCTS** — Monte-Carlo Tree Search; select/expand/simulate/backpropagate using UCB1.
- **Minimax / Alpha-Beta** — optimal adversarial search / its pruning optimization.
- **Navmesh** — navigation mesh; walkable space as convex polygons for efficient pathfinding.
- **PCG / PCGML** — Procedural Content Generation / its machine-learned variant.
- **PID controller** — proportional-integral-derivative control; used for steering/speed.
- **Policy** — a mapping from state to action; what an RL agent learns.
- **Population system** — spawns NPCs around the player up to a density cap and despawns them out of view, creating a "living" crowd within a bounded budget.
- **PPO / DQN** — Proximal Policy Optimization / Deep Q-Network; deep-RL algorithms.
- **Pure pursuit / look-ahead** — steering toward a point ahead on a path.
- **Q-learning** — value-based RL learning `Q(s,a)`.
- **Reward hacking** — an RL agent exploiting a loophole in the reward instead of the intended behavior.
- **Rubber-banding** — DDA in racing: speeding up trailing AI, slowing leaders.
- **Steering behaviors** — small composable forces (seek, flee, arrive, wander…) blended into movement.
- **Streaming** — loading world assets (geometry, AI data) from disk as the player moves and evicting what's left behind, so a huge map fits in fixed memory.
- **Suppression** — pinning a target with fire to reduce its effectiveness and force it into cover.
- **Telegraphing** — making the AI's intent legible via animation/audio so players perceive intelligence.
- **Time-slicing** — spreading agents' AI updates across many frames instead of updating all of them every frame, to bound per-frame cost.
- **UCB1** — the exploration/exploitation formula MCTS uses in selection.
- **Utility AI** — scoring actions by a utility function and picking the best; drives *The Sims* and 4X production.

## 20. Further Reading

**Books**
- Ian Millington & John Funge, *Artificial Intelligence for Games* — the standard text on the classic toolbox.
- Steve Rabin (ed.), *Game AI Pro* series — practitioner articles across every genre.
- Richard Sutton & Andrew Barto, *Reinforcement Learning: An Introduction* — the RL reference.

**Landmark papers**
- Reynolds, "Flocks, Herds, and Schools: A Distributed Behavioral Model" (SIGGRAPH 1987) — Boids.
- Hart, Nilsson & Raphael, "A Formal Basis for the Heuristic Determination of Minimum Cost Paths" (1968) — A\*.
- Orkin, "Three States and a Plan: The A.I. of F.E.A.R." (GDC 2006) — GOAP in practice.
- Silver et al., "Mastering the game of Go…" (*Nature* 2016) — AlphaGo.
- Vinyals et al., "Grandmaster level in StarCraft II…" (*Nature* 2019) — AlphaStar.
- Wurman et al., "Outracing champion Gran Turismo drivers with deep reinforcement learning" (*Nature* 2022) — Sophy.
- Park et al., "Generative Agents: Interactive Simulacra of Human Behavior" (2023) — Smallville.

**Communities & tools**
- The **GDC AI Summit** talks (many free on the GDC Vault / YouTube).
- **Unity ML-Agents** — train RL/imitation agents inside a real engine.
- **AiGameDev**, the **Game AI Pro** website, and the annual **AIIDE** / **CoG** academic conferences.

---

# Appendix A — Training AI Inside the Engine (Unity ML-Agents & Unreal Learning Agents)

The learned techniques in Part IV — reinforcement learning especially — raise an obvious question: the samples train in Python, but games ship in **C#** (Unity) or **C++** (Unreal). How does a model get trained *using a game* and then *run inside* one? This appendix answers that, and reference code lives in [`../engine-integration`](../engine-integration).

### The game is the environment

Training an agent is a loop between an **agent** and an **environment** — and in a game, *the game is the environment*. You must define four things — the **agent contract** — and they are the same in every framework:

- **Observations** — what the agent senses (a state vector: my position, the goal, my velocity…). Keep it to fair, observable information.
- **Actions** — what it can do (e.g. a 2-D move force; discrete button presses).
- **Reward** — the scalar that defines "good" (+1 for reaching the goal, a small time penalty, 0 for falling off).
- **Reset** — how to start a fresh episode (reposition the agent and goal).

Training runs this loop millions of times; a **policy** (a neural network) gradually learns to pick actions that maximize reward. Then you **freeze** the network and, in the shipping game, run only `observation → action` every tick. That final step — inference — is just a fast forward pass; all the learning happened offline.

### Unity — ML-Agents (train in Python, run in C#)

Unity's **ML-Agents Toolkit** has two halves. In-game you write a C# `Agent` subclass overriding `CollectObservations()`, `OnActionReceived()` (where you also call `AddReward()` / `EndEpisode()`), and `OnEpisodeBegin()` — that *is* the agent contract above. Training is driven by an **external Python process** (`mlagents-learn config.yaml`, PPO on PyTorch) that connects to Unity over a socket: it receives observations, returns actions, receives rewards, and updates the network across many parallel copies of the scene. It exports a `.onnx` file.

To **run it in-game** you have two options, both C#-only with no Python at runtime: (1) assign the `.onnx` to the agent's **Behavior Parameters → Model** and set **Inference Only** — the *same* agent script now runs, with **Unity Sentis** (formerly Barracuda) evaluating the network; or (2) load the `.onnx` yourself with Sentis and run the forward pass in your own code (this is also how you run a model trained in plain PyTorch). See `engine-integration/unity/`.

### Unreal — Learning Agents (train in-engine) + NNE (inference)

Unreal's **Learning Agents** plugin takes a different path: training runs **inside the engine** in C++ — there is *no external Python trainer*. You write an **Interactor** (defines observations and actions), a **Trainer** (defines reward and completion), and a **Policy** (the network); each engine tick advances a PPO step, usually with the game sped up and many agents in parallel. At inference time you drop the trainer and run just the Interactor + Policy. Separately, Unreal's **NNE (Neural Network Engine)** loads and runs any **ONNX** model at runtime (the analog of Unity Sentis) — so a model trained in Python can run in an Unreal game too. See `engine-integration/unreal/`. *(Learning Agents is experimental; its API changes between engine versions.)*

### Human feedback during training

Beyond a fixed reward function, you can put a **human in the training loop**: while the agent trains, an operator presses keys to reward or punish it live, and those signals fold into the *same* reward the optimizer maximizes — a simple form of TAMER / RLHF. Both complete projects in [`../engine-integration`](../engine-integration) implement this (`HumanFeedback.cs` in Unity; `RollerManager` + `MoveTrainer` in Unreal), alongside **imitation learning** from recorded human demonstrations (behavioral cloning + GAIL). The Unity example is an importable project that builds its own scene on Play; the Unreal example is a complete C++ project scaffold.

### At a glance

| | Unity ML-Agents | Unreal Learning Agents |
|---|---|---|
| You write | C# agent + YAML | C++ / Blueprint |
| Training runs | External Python (PyTorch) | In-engine (C++ PPO) |
| Run a model in-game | Sentis (ex-Barracuda) | NNE |
| Run a Python-trained ONNX | Yes (Sentis) | Yes (NNE) |
| Maturity | Stable, widely used | Experimental |

The throughline of this whole book returns one last time: the *algorithm* is the real content; the *language* is a delivery choice — Python to learn it, C#/C++ to ship it, and (as in this repo's interactive lab) JavaScript to demo it.

---

*End of book. Runnable algorithm code lives in [`../samples`](../samples); engine integration reference code in [`../engine-integration`](../engine-integration); the concise bilingual guides are [here (EN)](game-ai-guide.en.md) and [here (中文)](game-ai-guide.zh.md). Built as an educational companion to the [GameAI](../README.md) repository.*


