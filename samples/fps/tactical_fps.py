"""
FPS Tactical Squad AI  ·  第一人称射击战术 AI
=============================================

The combat AI in shooters is a lineage of *classic, authored* techniques stacked
ever higher.  This one sample shows the whole stack cooperating:

  * Line-of-sight (LOS)   - can the soldier actually see the target?  Doom's
                            monsters (1993) were state machines gated on LOS.
  * Cover / concealment   - path so a wall stays between you and the enemy.  The
                            flanker below uses a concealment-weighted search that
                            *prefers hidden cells* over the short exposed route.
  * Suppression           - the ANCHOR keeps LOS and fires to PIN the player.
                            A pinned defender tunnel-visions on the shooter in
                            their face (F.E.A.R., 2005) and stops tracking movers.
  * Squad flanking        - under that cover, the FLANKER maneuvers to a firing
                            position at a *different bearing* and delivers the kill.

Fire-and-maneuver — one element fixes the enemy in place while another moves on
them — is exactly what made F.E.A.R., Killzone, Halo and Rainbow Six Siege bots
feel like real soldiers.  Real engines swap the grid for a navmesh and bake cover
maps offline, but the decision logic is what you see here.

Deterministic.  Runs on the Python standard library only:
    python tactical_fps.py
"""

import heapq
import math

# --------------------------------------------------------------------------- #
# Arena.  '#' is a wall (blocks movement AND line-of-sight = hard cover).
# The player defends a room with two doorways; the squad exploits both.
# --------------------------------------------------------------------------- #
ARENA = [
    "####################",
    "#..................#",
    "#....########......#",
    "#....#......#......#",
    "#....#..P...+......#",   # + = right doorway (flank route leads here)
    "#....#......#......#",
    "#....##+#####......#",   # + = bottom doorway (anchor assaults here)
    "#..................#",
    "#..................#",
    "#..A............B..#",   # A = anchor start, B = flanker start
    "####################",
]

WALL = "#"


def parse_arena(rows):
    grid, player, squad = [], None, {}
    for y, row in enumerate(rows):
        line = []
        for x, c in enumerate(row):
            if c in "PAB.+":
                if c == "P":
                    player = (x, y)
                elif c in "AB":
                    squad[c] = (x, y)
                line.append(".")           # doorways and starts are floor
            else:
                line.append(WALL)
        grid.append(line)
    return grid, player, squad


GRID, PLAYER_START, SQUAD_START = parse_arena(ARENA)
H, W = len(GRID), len(GRID[0])


def is_wall(x, y):
    return not (0 <= x < W and 0 <= y < H) or GRID[y][x] == WALL


def line_of_sight(a, b):
    """Bresenham LOS: True if no wall lies strictly between a and b."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while (x, y) != (x1, y1):
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
        if (x, y) != (x1, y1) and is_wall(x, y):
            return False
    return True


def neighbours(x, y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if not is_wall(nx, ny):
            yield nx, ny


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra_step(start, goal, exposure_penalty=0, player=None):
    """First step of the cheapest path start->goal.

    exposure_penalty > 0 makes entering a cell the player can SEE cost extra, so
    the flanker naturally hugs cover instead of sprinting across open ground.
    """
    if start == goal:
        return start
    dist = {start: 0}
    first = {start: start}
    pq = [(0, start)]
    while pq:
        d, cell = heapq.heappop(pq)
        if cell == goal:
            return first[cell]
        if d > dist.get(cell, 1e9):
            continue
        for n in neighbours(*cell):
            step = 1
            if exposure_penalty and player and line_of_sight(n, player):
                step += exposure_penalty
            nd = d + step
            if nd < dist.get(n, 1e9):
                dist[n] = nd
                first[n] = n if cell == start else first[cell]
                heapq.heappush(pq, (nd, n))
    return start


# --------------------------------------------------------------------------- #
# Tactical position scoring (utility AI over cells).
# --------------------------------------------------------------------------- #
def bearing(frm, to):
    return math.atan2(to[1] - frm[1], to[0] - frm[0])


def nearest_firing_cell(start, player):
    """Closest reachable cell (to `start`) that has LOS to the player."""
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for cell in frontier:
            for n in neighbours(*cell):
                if n in seen:
                    continue
                if line_of_sight(n, player):
                    return n
                seen.add(n)
                nxt.append(n)
        frontier = nxt
    return start


def find_flank(player, anchor):
    """A firing cell whose bearing to the player differs most from the anchor's,
    kept at a little standoff distance so the flanker isn't point-blank."""
    best, best_score = None, -1e9
    ab = bearing(player, anchor)
    for y in range(H):
        for x in range(W):
            if is_wall(x, y) or not line_of_sight((x, y), player):
                continue
            d = manhattan((x, y), player)
            if d < 3:                       # don't suicide into their lap
                continue
            fb = bearing(player, (x, y))
            spread = abs(math.atan2(math.sin(fb - ab), math.cos(fb - ab)))  # 0..pi
            score = spread * 4.0 - 0.2 * d
            if score > best_score:
                best, best_score = (x, y), score
    return best


# --------------------------------------------------------------------------- #
# Agents
# --------------------------------------------------------------------------- #
class Soldier:
    def __init__(self, name, pos, role):
        self.name, self.pos, self.role = name, pos, role
        self.state, self.hp = "ADVANCE", 120

    def alive(self):
        return self.hp > 0


class Player:
    def __init__(self, pos):
        self.pos, self.hp, self.suppressed = pos, 100, False


def render(player, squad, tick):
    grid = [row[:] for row in GRID]
    for s in squad:
        if s.alive():
            grid[s.pos[1]][s.pos[0]] = s.name
    if player.hp > 0:
        grid[player.pos[1]][player.pos[0]] = "P"
    print(f"\n[t={tick:02d}]  player HP {max(0, player.hp):3d}"
          f"{'   << PINNED' if player.suppressed else ''}")
    print("\n".join("".join(r) for r in grid))


# --------------------------------------------------------------------------- #
# Simulation
# --------------------------------------------------------------------------- #
def main():
    player = Player(PLAYER_START)
    anchor = Soldier("A", SQUAD_START["A"], "ANCHOR")
    flanker = Soldier("B", SQUAD_START["B"], "FLANKER")
    squad = [anchor, flanker]

    print("FPS Tactical Squad AI  —  fire-and-maneuver on a dug-in player")
    print("=" * 62)
    print("A = anchor (fixes/suppresses)   B = flanker (maneuvers)   P = player")
    print("+ marks the two doorways into the player's room.")

    flank_goal = find_flank(player.pos, anchor.pos)

    for tick in range(1, 61):
        # ---------- anchor: get LOS, then SUPPRESS to pin the player -------
        if anchor.alive():
            if line_of_sight(anchor.pos, player.pos):
                anchor.state = "SUPPRESS"
                player.suppressed = True
                player.hp -= 4                       # suppressing fire chips slowly
            else:
                anchor.state = "ADVANCE"
                anchor.pos = dijkstra_step(anchor.pos,
                                           nearest_firing_cell(anchor.pos, player.pos))

        # ---------- flanker: maneuver via cover, then FLANK-FIRE -----------
        if flanker.alive():
            if flanker.pos == flank_goal and line_of_sight(flanker.pos, player.pos):
                flanker.state = "FLANK-FIRE"
                flanker.hp = flanker.hp               # holding position
                player.hp -= 26 if player.suppressed else 15
            else:
                flanker.state = "FLANK-MOVE"
                flanker.pos = dijkstra_step(flanker.pos, flank_goal,
                                            exposure_penalty=6, player=player.pos)

        # ---------- player returns fire -----------------------------------
        # A PINNED defender tunnel-visions on the shooter in their face (the
        # anchor) and stops tracking the mover -> that is why the flank works.
        if player.hp > 0:
            if player.suppressed and anchor.alive() and line_of_sight(player.pos, anchor.pos):
                anchor.hp -= 6                        # focuses the suppressor, weakly
            else:
                visible = [s for s in squad if s.alive()
                           and line_of_sight(player.pos, s.pos)]
                if visible:
                    tgt = min(visible, key=lambda s: manhattan(player.pos, s.pos))
                    tgt.hp -= 16

        player.suppressed = anchor.state == "SUPPRESS" and anchor.alive()

        if tick % 3 == 0 or player.hp <= 0:
            render(player, squad, tick)
            for s in squad:
                print(f"    {s.name} ({s.role}) HP {max(0, s.hp):3d}  ->  "
                      f"{'KIA' if not s.alive() else s.state}")

        if player.hp <= 0:
            print("\n" + "=" * 62)
            print(f"Objective neutralized on tick {tick}.")
            print("The ANCHOR pinned the player (who tunnel-visioned on the")
            print("suppressor), while the FLANKER hugged cover to an unguarded")
            print("bearing and delivered the kill — textbook fire-and-maneuver,")
            print("the core loop of modern shooter squad AI.")
            return
        if all(not s.alive() for s in squad):
            print("\nSquad wiped — the defender held. Re-tune cover/suppression weights.")
            return

    print("\nStalemate — suppression held the player but the flank stalled.")


if __name__ == "__main__":
    main()
