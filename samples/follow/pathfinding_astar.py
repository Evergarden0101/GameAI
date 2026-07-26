"""
Follow / Chase Enemy AI: A* Pathfinding  ·  追踪敌人 AI（A* 寻路）
================================================================

A "follow enemy" needs to navigate *around obstacles* to reach a moving target
(the player). The workhorse algorithm is **A\\*** ("A-star"): a best-first graph
search that expands the node minimising  f = g + h  where

    g = cost from the start to this node,
    h = heuristic estimate from this node to the goal (Manhattan distance here).

A* is optimal and complete when the heuristic never overestimates. Every game
with grid or nav-mesh movement (Pac-Man ghosts, StarCraft units, tower-defense
creeps) uses A* or a close relative underneath.

This demo builds a grid with walls, runs A*, and then simulates a *chase*: each
tick the enemy re-plans a path to the player and steps one tile along it, while
the player also moves. Watch the enemy route around the wall to cut the player off.

Runs on the Python standard library only:  python pathfinding_astar.py
"""

import heapq

# 0 = floor, 1 = wall.  '#' walls form a barrier the chaser must go around.
GRID = [
    list(row) for row in [
        "0000000000000000",
        "0000011111100000",
        "0000010000100000",
        "0000010000100000",
        "0000010000100000",
        "0000010000000000",
        "0000011111100000",
        "0000000000000000",
        "0001111000011110",
        "0000000000000000",
        "0000000000000000",
    ]
]
ROWS, COLS = len(GRID), len(GRID[0])


def passable(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS and GRID[r][c] == "0"


def neighbors(r, c):
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):   # 4-connected
        nr, nc = r + dr, c + dc
        if passable(nr, nc):
            yield nr, nc


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(start, goal):
    """Return the shortest path [start, ..., goal] or [] if unreachable."""
    open_heap = [(manhattan(start, goal), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}

    while open_heap:
        _, g, current = heapq.heappop(open_heap)
        if current == goal:
            # reconstruct
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        if g > g_score.get(current, 1e9):
            continue
        for nb in neighbors(*current):
            ng = g + 1
            if ng < g_score.get(nb, 1e9):
                g_score[nb] = ng
                came_from[nb] = current
                heapq.heappush(open_heap, (ng + manhattan(nb, goal), ng, nb))
    return []


def render(enemy, player, path=None):
    path = set(path or [])
    out = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            cell = (r, c)
            if cell == enemy:      line.append("E")
            elif cell == player:   line.append("P")
            elif GRID[r][c] == "1": line.append("#")
            elif cell in path:     line.append("*")
            else:                  line.append(".")
        out.append(" ".join(line))
    return "\n".join(out)


def main():
    print("A* pathfinding — a chase enemy (E) routes around walls (#) to the player (P)")
    print("=" * 66)

    enemy = (10, 1)
    goal = (1, 14)
    print("Static A* path from E to a fixed goal:")
    print(render(enemy, goal, astar(enemy, goal)))
    print("  '*' marks the optimal route around the barrier.\n")

    # ----- moving chase ---------------------------------------------------- #
    print("Live chase — enemy re-plans every tick as the player flees:")
    print("-" * 66)
    player = (2, 8)                 # start inside the room
    player_route = [(2, 8), (5, 11), (5, 14), (9, 14), (10, 10),
                    (10, 6), (10, 2), (9, 1), (7, 1)]
    pi = 0

    for tick in range(1, 40):
        # player walks its escape route
        if pi < len(player_route) - 1 and player == player_route[pi]:
            pi += 1
        player = _step_toward(player, player_route[pi])

        # enemy re-plans a fresh A* path to the player's current tile and
        # steps one tile along it (classic "recompute each tick" chaser)
        path = astar(enemy, player)
        if len(path) >= 2:
            enemy = path[1]

        if tick % 6 == 0 or enemy == player:
            print(f"tick {tick:2d}:  enemy={enemy}  player={player}  "
                  f"path_len={len(path)}")
        if enemy == player:
            print("\nCaught the player!")
            print(render(enemy, player))
            break
    else:
        print("\nPlayer still evading after 39 ticks.")
        print(render(enemy, player, astar(enemy, player)))


def _step_toward(cur, tgt):
    """Move one tile toward tgt along a passable cell (greedy)."""
    if cur == tgt:
        return cur
    best = cur
    best_d = manhattan(cur, tgt)
    for nb in neighbors(*cur):
        d = manhattan(nb, tgt)
        if d < best_d:
            best_d, best = d, nb
    return best


if __name__ == "__main__":
    main()
