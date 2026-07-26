"""
NPC AI: Finite State Machine (+ a tiny Behavior Tree)  ·  NPC 状态机 / 行为树
==========================================================================

Non-Player Characters (NPCs) are most often driven by a Finite State Machine
(FSM) or a Behavior Tree (BT).

* FSM  - the NPC is always in exactly one *state* (Patrol, Investigate, Chase,
         Attack, Flee...). Events (seeing the player, taking damage) trigger
         *transitions* to other states. Simple, predictable, easy to debug.
         Used in countless games for guards and enemies.
* BT   - a tree of behaviors composed with Sequence / Selector nodes. Scales
         to more complex characters than a flat FSM (Halo, most modern AAA).

This file runs a guard NPC through a scripted scenario and prints every state
transition, then shows the same "should I attack?" decision as a Behavior Tree.

Runs on the Python standard library only:  python npc_fsm.py
"""

from dataclasses import dataclass, field


# --------------------------------------------------------------------------- #
# World / perception the guard reacts to each tick
# --------------------------------------------------------------------------- #
@dataclass
class Perception:
    sees_player: bool = False      # player currently in the vision cone
    distance: float = 999.0        # distance to the player (world units)
    heard_noise: bool = False      # a noise this tick (footstep, gunshot)


@dataclass
class Guard:
    health: int = 100
    state: str = "PATROL"
    alert: float = 0.0             # 0..100 suspicion meter
    last_seen_ttl: int = 0         # ticks we keep chasing after losing sight


# --------------------------------------------------------------------------- #
# The FSM.  Each state is a function (guard, perception) -> next_state
# --------------------------------------------------------------------------- #
ATTACK_RANGE = 6.0
SIGHT_RANGE = 30.0
FLEE_HEALTH = 25


def s_patrol(g: Guard, p: Perception) -> str:
    if p.sees_player:
        g.alert = 100.0
        g.last_seen_ttl = 20
        return "CHASE"
    if p.heard_noise:
        g.alert = min(100.0, g.alert + 40.0)
        return "INVESTIGATE" if g.alert >= 60 else "PATROL"
    g.alert = max(0.0, g.alert - 5.0)          # calm down over time
    return "PATROL"


def s_investigate(g: Guard, p: Perception) -> str:
    if p.sees_player:
        g.last_seen_ttl = 20
        return "CHASE"
    g.alert = max(0.0, g.alert - 8.0)
    return "INVESTIGATE" if g.alert > 10 else "PATROL"


def s_chase(g: Guard, p: Perception) -> str:
    if g.health <= FLEE_HEALTH:
        return "FLEE"
    if p.sees_player:
        g.last_seen_ttl = 20
        if p.distance <= ATTACK_RANGE:
            return "ATTACK"
        return "CHASE"
    # lost sight — keep pursuing for a while, then give up
    g.last_seen_ttl -= 1
    return "CHASE" if g.last_seen_ttl > 0 else "INVESTIGATE"


def s_attack(g: Guard, p: Perception) -> str:
    if g.health <= FLEE_HEALTH:
        return "FLEE"
    if not p.sees_player:
        return "CHASE"
    return "ATTACK" if p.distance <= ATTACK_RANGE else "CHASE"


def s_flee(g: Guard, p: Perception) -> str:
    # run until safe (out of sight and some distance away)
    if not p.sees_player and p.distance > SIGHT_RANGE:
        g.alert = 0.0
        return "PATROL"
    return "FLEE"


STATES = {
    "PATROL": s_patrol,
    "INVESTIGATE": s_investigate,
    "CHASE": s_chase,
    "ATTACK": s_attack,
    "FLEE": s_flee,
}


def step(g: Guard, p: Perception) -> str:
    """Run one tick of the FSM; return the (possibly new) state."""
    g.state = STATES[g.state](g, p)
    return g.state


# --------------------------------------------------------------------------- #
# A tiny Behavior Tree for the "engage the player" decision.
# Selector = try children until one succeeds. Sequence = all must succeed.
# --------------------------------------------------------------------------- #
def bt_should_attack(g: Guard, p: Perception) -> bool:
    def sequence(*conds):   return all(c() for c in conds)
    def selector(*opts):    return any(o() for o in opts)

    engage = lambda: sequence(
        lambda: g.health > FLEE_HEALTH,     # healthy enough to fight
        lambda: p.sees_player,              # can see the target
        lambda: p.distance <= ATTACK_RANGE, # in range
    )
    retreat_instead = lambda: g.health <= FLEE_HEALTH
    # Selector: retreat OR engage (retreat wins if hurt).
    return selector(lambda: not retreat_instead() and engage(), lambda: False)


# --------------------------------------------------------------------------- #
# Scripted scenario
# --------------------------------------------------------------------------- #
def main():
    g = Guard()
    print("NPC guard FSM — scripted patrol/chase/attack/flee scenario")
    print("=" * 60)

    # (tick description, perception, optional damage dealt this tick)
    script = [
        ("quiet patrol",        Perception(),                                0),
        ("hears a noise",       Perception(heard_noise=True),                0),
        ("still suspicious",    Perception(),                                0),
        ("spots the player!",   Perception(sees_player=True, distance=22),   0),
        ("closing distance",    Perception(sees_player=True, distance=9),    0),
        ("in attack range",     Perception(sees_player=True, distance=4),   15),
        ("trading blows",       Perception(sees_player=True, distance=4),   40),
        ("badly hurt, flees",   Perception(sees_player=True, distance=8),   30),
        ("breaking line-of-sight", Perception(sees_player=False, distance=18), 0),
        ("escaped, safe",       Perception(sees_player=False, distance=40),  0),
        ("back to patrol",      Perception(),                                0),
    ]

    prev = g.state
    for desc, perc, dmg in script:
        g.health = max(0, g.health - dmg)
        new = step(g, perc)
        arrow = f"{prev:>11s} -> {new:<11s}" if new != prev else f"{'':>11s}    {new:<11s}"
        atk = "  [BT: ATTACK]" if bt_should_attack(g, perc) else ""
        print(f"  {desc:<26s} hp={g.health:3d} alert={g.alert:5.1f}  {arrow}{atk}")
        prev = new

    print("-" * 60)
    print("The guard flowed Patrol -> Investigate -> Chase -> Attack -> Flee "
          "-> Patrol purely from perception + health, with no scripting of the "
          "states themselves.")


if __name__ == "__main__":
    main()
