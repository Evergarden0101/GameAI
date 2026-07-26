"""
Learning to Race — RL Speed Control  ·  学习竞速：强化学习速度控制
=============================================================

Gran Turismo Sophy (Sony AI, *Nature* 2022) beat the world's best GT drivers with
deep reinforcement learning — no hand-authored racing line, just reward for going
fast without crashing.  This sample shows the *idea* at teaching scale with tabular
Q-learning (the same algorithm as the maze demo, applied to driving):

A car runs a lap made of straights and corners.  Each corner has a SAFE SPEED; go
in faster and you spin out (crash).  The agent's state is (track segment, current
speed bucket); its actions are ACCELERATE / HOLD / BRAKE.  It gets a small reward
for speed each tick and a big penalty for crashing.  From nothing, it learns a
speed PROFILE — floor it on straights, brake before corners — beating a naive
"always full throttle" driver that just crashes.

That is Sophy in miniature: no racing line is programmed; the *policy* discovers
one.  Deterministic (seeded).  Standard library only:
    python sophy_racing_qlearn.py
"""

import random

rng = random.Random(0)

# Track = list of segment "safe speeds" (low = tight corner, high = straight).
TRACK = [5, 5, 2, 2, 5, 5, 5, 1, 2, 5, 5, 3, 5, 5, 2, 5]
N_SEG = len(TRACK)
MAX_SPEED = 5
ACTIONS = {"BRAKE": -1, "HOLD": 0, "ACCEL": +1}
ACT_NAMES = list(ACTIONS)


def step(seg, speed, action):
    """Apply an action; return (next_seg, next_speed, reward, crashed)."""
    speed = max(0, min(MAX_SPEED, speed + ACTIONS[action]))
    nxt = (seg + 1) % N_SEG
    # entering the NEXT segment above its safe speed = spin out
    if speed > TRACK[nxt]:
        return nxt, 0, -60, True
    reward = speed                       # reward = distance covered this tick
    return nxt, speed, reward, False


def train(episodes=6000, alpha=0.2, gamma=0.9):
    Q = {}                               # (seg, speed) -> [q per action]

    def q(s):
        return Q.setdefault(s, [0.0, 0.0, 0.0])

    for ep in range(episodes):
        eps = max(0.05, 1.0 - ep / (episodes * 0.7))     # decay exploration
        seg, speed = 0, 1
        for _ in range(N_SEG * 3):
            s = (seg, speed)
            if rng.random() < eps:
                ai = rng.randrange(3)
            else:
                ai = max(range(3), key=lambda i: q(s)[i])
            nseg, nspeed, r, crashed = step(seg, speed, ACT_NAMES[ai])
            ns = (nseg, nspeed)
            target = r + (0 if crashed else gamma * max(q(ns)))
            q(s)[ai] += alpha * (target - q(s)[ai])
            if crashed:
                break
            seg, speed = nseg, nspeed
    return Q


def greedy_lap(Q, verbose=False):
    """Run one lap with the learned policy; return (distance, crashed)."""
    def q(s):
        return Q.get(s, [0.0, 0.0, 0.0])
    seg, speed, dist = 0, 1, 0
    for t in range(N_SEG):
        ai = max(range(3), key=lambda i: q((seg, speed))[i])
        seg, speed, r, crashed = step(seg, speed, ACT_NAMES[ai])
        dist += max(0, r)
        if verbose:
            marker = "  <-- corner" if TRACK[seg] <= 2 else ""
            print(f"    seg {seg:2d} (safe {TRACK[seg]})  {ACT_NAMES[ai]:5s} "
                  f"-> speed {speed}{marker}")
        if crashed:
            return dist, True
    return dist, False


def naive_lap():
    """Always-accelerate baseline — the 'floor it' driver."""
    seg, speed, dist = 0, 1, 0
    for _ in range(N_SEG):
        seg, speed, r, crashed = step(seg, speed, "ACCEL")
        dist += max(0, r)
        if crashed:
            return dist, True
    return dist, False


def main():
    print("Learning to Race — tabular Q-learning discovers a speed profile")
    print("=" * 64)
    print("Track safe-speeds per segment (1=hairpin, 5=straight):")
    print("   " + " ".join(f"{v}" for v in TRACK) + "\n")

    nd, ncrash = naive_lap()
    print(f"Naive 'always full throttle' driver: distance {nd}, "
          f"{'CRASHED' if ncrash else 'clean'} — it can't handle corners.\n")

    print("Training the RL agent (6000 episodes of trial-and-error)...")
    Q = train()
    print("Learned policy lap:")
    dist, crashed = greedy_lap(Q, verbose=True)
    print("=" * 64)
    print(f"Learned driver: distance {dist}, {'CRASHED' if crashed else 'clean lap'}.")
    print("With zero programmed racing line, the agent learned to BRAKE before every")
    print("corner and ACCELERATE on straights — the essence of Sophy, at toy scale.")


if __name__ == "__main__":
    main()
