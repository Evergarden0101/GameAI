"""
Cluster / Swarm Enemy AI: Boids Flocking  ·  集群/蜂群敌人 AI（Boids）
====================================================================

"Cluster enemies" - bats, zerg, drones, a school of fish - are usually driven
by Craig Reynolds' **Boids** algorithm (1986). Each agent follows three local
steering rules using only its nearby neighbours:

1. Separation - steer away from crowding (don't collide).
2. Alignment  - steer toward the average heading of neighbours.
3. Cohesion   - steer toward the average position of neighbours (stay a group).

Add a 4th "seek" rule toward the player and you get a menacing swarm that
hunts as a coordinated group while still looking organic. No central brain -
the group behaviour *emerges* from local rules.

Runs on the Python standard library only:  python flocking.py
"""

import math
import random


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = float(x), float(y)

    def __add__(self, o):  return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o):  return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, s):  return Vec2(self.x * s, self.y * s)

    def length(self):
        return math.hypot(self.x, self.y)

    def limit(self, m):
        n = self.length()
        return self * (m / n) if n > m else Vec2(self.x, self.y)

    def normalized(self):
        n = self.length()
        return Vec2(self.x / n, self.y / n) if n else Vec2()


class Boid:
    def __init__(self, x, y):
        self.pos = Vec2(x, y)
        ang = random.uniform(0, 2 * math.pi)
        self.vel = Vec2(math.cos(ang), math.sin(ang))


# --------------------------------------------------------------------------- #
# Tunable weights and radii - the "feel" of the swarm lives here.
# --------------------------------------------------------------------------- #
NEIGHBOR_RADIUS = 12.0
SEPARATION_RADIUS = 4.0
MAX_SPEED = 2.2
MAX_FORCE = 0.20
W_SEP, W_ALI, W_COH, W_SEEK = 1.6, 1.0, 1.0, 0.9
WORLD = 80.0


def steer(boids, me, target):
    sep = Vec2(); ali = Vec2(); coh = Vec2()
    n_ali = n_coh = 0

    for other in boids:
        if other is me:
            continue
        offset = me.pos - other.pos
        d = offset.length()
        if d < SEPARATION_RADIUS and d > 0:
            sep = sep + offset.normalized() * (1.0 / d)   # push harder when closer
        if d < NEIGHBOR_RADIUS:
            ali = ali + other.vel
            coh = coh + other.pos
            n_ali += 1
            n_coh += 1

    acc = Vec2()
    if sep.length() > 0:
        acc = acc + (sep.normalized() * MAX_SPEED - me.vel).limit(MAX_FORCE) * W_SEP
    if n_ali:
        ali = (ali * (1.0 / n_ali)).normalized() * MAX_SPEED
        acc = acc + (ali - me.vel).limit(MAX_FORCE) * W_ALI
    if n_coh:
        center = coh * (1.0 / n_coh)
        desired = (center - me.pos).normalized() * MAX_SPEED
        acc = acc + (desired - me.vel).limit(MAX_FORCE) * W_COH

    # seek the player/target so the swarm hunts as a group
    seek = (target - me.pos).normalized() * MAX_SPEED
    acc = acc + (seek - me.vel).limit(MAX_FORCE) * W_SEEK
    return acc


def update(boids, target):
    for b in boids:
        b.vel = (b.vel + steer(boids, b, target)).limit(MAX_SPEED)
    for b in boids:
        b.pos = b.pos + b.vel
        # wrap around the world edges (toroidal)
        b.pos.x %= WORLD
        b.pos.y %= WORLD


def flock_metrics(boids, target):
    cx = sum(b.pos.x for b in boids) / len(boids)
    cy = sum(b.pos.y for b in boids) / len(boids)
    center = Vec2(cx, cy)
    spread = sum((b.pos - center).length() for b in boids) / len(boids)
    dist_to_target = (center - target).length()
    return spread, dist_to_target


def ascii_snapshot(boids, target, size=24):
    grid = [["." for _ in range(size)] for _ in range(size)]
    def cell(p):
        return (int(p.y / WORLD * size) % size, int(p.x / WORLD * size) % size)
    for b in boids:
        r, c = cell(b.pos)
        grid[r][c] = "o"
    tr, tc = cell(target)
    grid[tr][tc] = "X"                       # the player/target
    return "\n".join(" ".join(row) for row in grid)


def main():
    random.seed(7)
    boids = [Boid(random.uniform(0, 20), random.uniform(0, 20)) for _ in range(40)]
    target = Vec2(60, 60)                     # the player the swarm hunts

    print("Boids swarm — 40 cluster enemies hunting the player (X)")
    print("=" * 56)
    print("Start (scattered, far from player):")
    print(ascii_snapshot(boids, target))
    s0, d0 = flock_metrics(boids, target)
    print(f"  spread={s0:5.1f}  swarm-to-player distance={d0:5.1f}\n")

    for step_i in range(1, 121):
        update(boids, target)
        if step_i == 60:
            print("After 60 steps (grouped up, closing in):")
            print(ascii_snapshot(boids, target))
            s, d = flock_metrics(boids, target)
            print(f"  spread={s:5.1f}  swarm-to-player distance={d:5.1f}\n")

    print("After 120 steps (tight swarm on the player):")
    print(ascii_snapshot(boids, target))
    s, d = flock_metrics(boids, target)
    print(f"  spread={s:5.1f}  swarm-to-player distance={d:5.1f}")
    print("-" * 56)
    print("The group cohesion and hunt emerged from local rules only — "
          "no boid was told where the others are going.")


if __name__ == "__main__":
    main()
