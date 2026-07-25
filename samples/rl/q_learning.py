"""
Reinforcement Learning Agent: Tabular Q-Learning  ·  强化学习智能体（Q-Learning）
==============================================================================

Modern game AI increasingly *learns* behaviour instead of having it scripted.
The classic entry point is **Q-learning**: the agent learns a table Q(state,
action) estimating the long-term reward of each action, by trial and error:

    Q(s,a) <- Q(s,a) + alpha * ( r + gamma * max_a' Q(s',a') - Q(s,a) )

Same idea scales up (Deep Q-Networks, PPO, self-play) to the systems behind
Gran Turismo Sophy (Sony, beat human racers), AlphaStar (StarCraft II) and
OpenAI Five (Dota 2).

Here an agent learns to navigate a grid maze from Start (S) to Goal (G) while
avoiding a Pit (P). We print the learned policy and a greedy rollout.

USAGE (what RL is good for):    hard-to-script, reactive, self-improving agents;
                                super-human play; emergent strategies.
LIMITATIONS (see docs):         needs many samples, a reward function, and a
                                simulator; behaviour can be unpredictable /
                                hard to debug; training is expensive.

Runs on the Python standard library only:  python q_learning.py
"""

import random

# --------------------------------------------------------------------------- #
# Environment: a small grid world.  S=start  G=goal(+1)  P=pit(-1)  #=wall
# --------------------------------------------------------------------------- #
MAP = [
    "S....",
    ".##..",
    ".#P..",
    ".#.#.",
    "....G",
]
ROWS, COLS = len(MAP), len(MAP[0])
ACTIONS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
ACTION_LIST = list(ACTIONS)


def find(ch):
    for r, row in enumerate(MAP):
        c = row.find(ch)
        if c != -1:
            return (r, c)
    raise ValueError(ch)


START, GOAL, PIT = find("S"), find("G"), find("P")


def is_wall(r, c):
    return not (0 <= r < ROWS and 0 <= c < COLS) or MAP[r][c] == "#"


def step(state, action):
    """Return (next_state, reward, done)."""
    dr, dc = ACTIONS[action]
    nr, nc = state[0] + dr, state[1] + dc
    if is_wall(nr, nc):
        nr, nc = state                       # bump into wall -> stay put
    nxt = (nr, nc)
    if nxt == GOAL:
        return nxt, 1.0, True
    if nxt == PIT:
        return nxt, -1.0, True
    return nxt, -0.02, False                  # small step cost => prefer short paths


# --------------------------------------------------------------------------- #
# Q-learning
# --------------------------------------------------------------------------- #
def train(episodes=4000, alpha=0.4, gamma=0.95, eps_start=0.9, eps_end=0.05):
    Q = {(r, c): {a: 0.0 for a in ACTION_LIST}
         for r in range(ROWS) for c in range(COLS)}
    returns = []

    for ep in range(episodes):
        eps = eps_start + (eps_end - eps_start) * (ep / episodes)   # decay
        s = START
        total = 0.0
        for _ in range(100):                 # step cap per episode
            # epsilon-greedy action selection (explore vs exploit)
            if random.random() < eps:
                a = random.choice(ACTION_LIST)
            else:
                a = max(Q[s], key=Q[s].get)

            s2, r, done = step(s, a)
            best_next = max(Q[s2].values())
            # the Q-learning update rule
            Q[s][a] += alpha * (r + gamma * best_next - Q[s][a])
            s = s2
            total += r
            if done:
                break
        returns.append(total)

    return Q, returns


def render_policy(Q):
    out = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            if (r, c) == GOAL:   row.append("G")
            elif (r, c) == PIT:  row.append("P")
            elif MAP[r][c] == "#": row.append("#")
            else:
                best = max(Q[(r, c)], key=Q[(r, c)].get)
                row.append("S" if (r, c) == START else best)
        out.append(" ".join(row))
    return "\n".join(out)


def greedy_rollout(Q):
    s, path = START, [START]
    for _ in range(50):
        a = max(Q[s], key=Q[s].get)
        s, _, done = step(s, a)
        path.append(s)
        if done:
            break
    return path


def main():
    random.seed(0)
    print("Q-learning — agent learns to reach G while avoiding P")
    print("=" * 52)
    print("Maze (S=start  G=goal +1  P=pit -1  #=wall):")
    print("\n".join("  " + " ".join(row) for row in MAP))
    print()

    Q, returns = train()

    # learning progress (average return per 500-episode block)
    print("Learning curve (avg return per 500 episodes):")
    block = 500
    for i in range(0, len(returns), block):
        avg = sum(returns[i:i + block]) / block
        bar = "#" * int((avg + 2) * 8)        # shift so negative values show
        print(f"  ep {i:4d}-{i+block:4d}: {avg:+5.2f}  {bar}")

    print("\nLearned policy (arrow = best action per tile):")
    print("\n".join("  " + line for line in render_policy(Q).split("\n")))

    path = greedy_rollout(Q)
    reached = "reached G" if path[-1] == GOAL else "did NOT reach G"
    print(f"\nGreedy rollout: {' -> '.join(map(str, path))}")
    print(f"Result: {reached} in {len(path)-1} steps.")
    print("-" * 52)
    print("The agent was never told the route — it discovered the optimal "
          "policy purely from reward feedback.")


if __name__ == "__main__":
    main()
