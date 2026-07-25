"""
GOAP — Goal-Oriented Action Planning  ·  目标导向的行动规划
=========================================================

Instead of hard-coding an NPC's behaviour with state-machine transitions, GOAP
gives the agent a GOAL and a set of ACTIONS, each with PRECONDITIONS and EFFECTS,
and lets a planner assemble a valid sequence AT RUNTIME.  The planner is just A*
searching through *world states*: the start state is the world now, the goal test
is "are the goal conditions satisfied?", neighbours are actions whose
preconditions hold, and the path cost is the sum of action costs.

GOAP debuted in F.E.A.R. (2005), where it gave soldiers their famously emergent
tactics — flushing the player with grenades, flanking, taking cover — without a
designer scripting each combo.  The same actions re-plan into different plans as
the world changes, which is what makes it feel intelligent.

Runs on the Python standard library only:
    python goap_planner.py
"""

import heapq
from itertools import count


class Action:
    def __init__(self, name, preconditions, effects, cost=1.0):
        self.name = name
        self.pre = preconditions        # dict of required state values
        self.eff = effects              # dict of state values this sets
        self.cost = cost

    def applicable(self, state):
        return all(state.get(k) == v for k, v in self.pre.items())

    def apply(self, state):
        s = dict(state)
        s.update(self.eff)
        return s


# --------------------------------------------------------------------------- #
# A* over world states.
# --------------------------------------------------------------------------- #
def plan(actions, start, goal):
    def satisfied(state):
        return all(state.get(k) == v for k, v in goal.items())

    def heuristic(state):
        # optimistic: number of unmet goal conditions (each needs >=1 action)
        return sum(1 for k, v in goal.items() if state.get(k) != v)

    start_key = frozenset(start.items())
    tiebreak = count()
    frontier = [(heuristic(start), next(tiebreak), 0.0, start, [])]
    best_cost = {start_key: 0.0}

    while frontier:
        _, _, g, state, path = heapq.heappop(frontier)
        if satisfied(state):
            return path, g
        for a in actions:
            if not a.applicable(state):
                continue
            ns = a.apply(state)
            key = frozenset(ns.items())
            ng = g + a.cost
            if ng < best_cost.get(key, 1e9):
                best_cost[key] = ng
                heapq.heappush(frontier,
                               (ng + heuristic(ns), next(tiebreak), ng, ns, path + [a]))
    return None, float("inf")


# --------------------------------------------------------------------------- #
# A F.E.A.R.-style soldier: goal = enemy eliminated.
# --------------------------------------------------------------------------- #
def soldier_actions():
    return [
        Action("MoveToWeapon", {}, {"at_weapon": True}, cost=2),
        Action("PickUpWeapon", {"at_weapon": True}, {"has_weapon": True}, cost=1),
        Action("LoadWeapon", {"has_weapon": True}, {"weapon_loaded": True}, cost=1),
        Action("MoveToCover", {}, {"in_cover": True}, cost=2),
        Action("MoveToEnemy", {}, {"near_enemy": True, "in_cover": False}, cost=3),
        Action("ThrowGrenade", {"near_enemy": True, "has_grenade": True},
               {"enemy_flushed": True}, cost=2),
        Action("Attack",
               {"weapon_loaded": True, "near_enemy": True, "enemy_flushed": True},
               {"enemy_dead": True}, cost=1),
    ]


def show(label, actions, start, goal):
    print(label)
    print("  start:", {k: v for k, v in start.items() if v})
    steps, cost = plan(actions, start, goal)
    if steps is None:
        print("  → no plan found\n")
        return
    print("  plan (total cost {:.0f}):".format(cost))
    for i, a in enumerate(steps, 1):
        print(f"    {i}. {a.name}")
    print()


def main():
    print("GOAP — one goal, one action set, plans built by A* at runtime")
    print("=" * 62)
    goal = {"enemy_dead": True}
    actions = soldier_actions()

    # Scenario 1: unarmed soldier, enemy in the open with a grenade available.
    start1 = dict(has_weapon=False, weapon_loaded=False, at_weapon=False,
                  near_enemy=False, in_cover=False, has_grenade=True,
                  enemy_flushed=False, enemy_dead=False)
    show("Scenario 1 — unarmed, must arm up first:", actions, start1, goal)

    # Scenario 2: already armed & loaded -> the planner produces a SHORTER plan.
    start2 = dict(start1, has_weapon=True, weapon_loaded=True, at_weapon=True)
    show("Scenario 2 — already armed (same goal, world changed):", actions, start2, goal)

    # Scenario 3: no grenade -> Attack's precondition can't be met -> no plan,
    # so the agent would fall back / pick another goal (shown as 'no plan').
    start3 = dict(start1, has_grenade=False)
    show("Scenario 3 — no grenade, enemy can't be flushed:", actions, start3, goal)

    print("Same actions, three worlds, three different outcomes — no branch of this")
    print("was scripted. That runtime re-planning is what made F.E.A.R.'s AI famous.")


if __name__ == "__main__":
    main()
