"""
Pac-Man Ghost AI  ·  吃豆人幽灵 AI（四种性格）
==============================================

Pac-Man (1980) is the textbook example of *believable behaviour from trivial
rules*.  Each ghost is a tiny state machine with ONE distinctive targeting rule,
and the four together feel like a coordinated hunting pack even though none of
them can see the others' plans.  Every ghost simply steps toward its own "target
tile" each move (picking the legal turn that most reduces straight-line distance,
never reversing) — the personalities live entirely in how the target is chosen:

  * BLINKY (red)    - targets Pac-Man's tile directly.          (the relentless chaser)
  * PINKY  (pink)   - targets 4 tiles AHEAD of Pac-Man.         (tries to ambush/cut off)
  * INKY   (cyan)   - targets a point reflected through Blinky. (unpredictable pincer)
  * CLYDE  (orange) - chases when far, but flees to his corner
                      when within 8 tiles.                      (the "shy" one)

They also flip between CHASE and SCATTER (retreat to fixed home corners) on a
timer, which is what stops them from perfectly cornering the player.

Deterministic.  Standard library only:
    python pacman_ghosts.py
"""

MAZE = [
    "###############",
    "#......#......#",
    "#.####.#.####.#",
    "#.............#",
    "#.####.#.####.#",
    "#......#......#",
    "#.####.#.####.#",
    "#.............#",
    "#.####.#.####.#",
    "#......P......#",
    "###############",
]

W, H = len(MAZE[0]), len(MAZE)
UP, LEFT, DOWN, RIGHT = (0, -1), (-1, 0), (0, 1), (1, 0)
DIRS = [UP, LEFT, DOWN, RIGHT]                     # Pac-Man's real tie-break order


def is_wall(x, y):
    return not (0 <= x < W and 0 <= y < H) or MAZE[y][x] == "#"


def dist2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def add(p, d, k=1):
    return (p[0] + d[0] * k, p[1] + d[1] * k)


class Ghost:
    def __init__(self, name, glyph, pos, corner):
        self.name, self.glyph = name, glyph
        self.pos, self.dir = pos, UP
        self.corner = corner                       # scatter target

    def target(self, pac, pac_dir, blinky_pos, mode):
        if mode == "SCATTER":
            return self.corner
        if self.name == "BLINKY":
            return pac
        if self.name == "PINKY":
            return add(pac, pac_dir, 4)             # 4 tiles ahead
        if self.name == "INKY":
            pivot = add(pac, pac_dir, 2)            # reflect through Blinky
            return (2 * pivot[0] - blinky_pos[0], 2 * pivot[1] - blinky_pos[1])
        if self.name == "CLYDE":
            return pac if dist2(self.pos, pac) > 64 else self.corner   # 8 tiles
        return pac

    def step(self, target):
        """Move one tile toward `target`, never reversing, ties by DIRS order."""
        reverse = (-self.dir[0], -self.dir[1])
        best, best_d = None, 1e9
        for d in DIRS:                             # DIRS order breaks ties
            if d == reverse:
                continue
            nxt = add(self.pos, d)
            if is_wall(*nxt):
                continue
            dd = dist2(nxt, target)
            if dd < best_d:
                best, best_d = d, dd
        if best is None:                           # dead end: allow reverse
            best = reverse
        self.dir = best
        self.pos = add(self.pos, best)


def pac_start():
    for y, row in enumerate(MAZE):
        x = row.find("P")
        if x >= 0:
            return (x, y)
    return (1, 1)


def pac_move(pac, pac_dir, ghosts):
    """A simple greedy Pac-Man: flee the nearest ghost, else keep exploring."""
    reverse = (-pac_dir[0], -pac_dir[1])
    nearest = min(ghosts, key=lambda g: dist2(g.pos, pac))
    options = []
    for d in DIRS:
        nxt = add(pac, d)
        if is_wall(*nxt):
            continue
        options.append((d, nxt))
    # prefer moves that keep away from the nearest ghost; avoid reversing if we can
    options.sort(key=lambda dn: (-dist2(dn[1], nearest.pos), dn[0] == reverse))
    return options[0]


def render(pac, ghosts, dots, step, mode):
    grid = [list(row) for row in MAZE]
    for y in range(H):
        for x in range(W):
            if grid[y][x] == "P":
                grid[y][x] = "."
    for (x, y) in dots:
        grid[y][x] = "·"
    for g in ghosts:
        grid[g.pos[1]][g.pos[0]] = g.glyph
    grid[pac[1]][pac[0]] = "@"
    print(f"\n[step {step:2d}]  mode={mode}   dots left={len(dots)}")
    print("\n".join("".join(r) for r in grid))


def main():
    pac = pac_start()
    pac_dir = LEFT
    ghosts = [
        Ghost("BLINKY", "B", (7, 3), (W - 2, 1)),        # red   -> top-right
        Ghost("PINKY",  "P", (6, 5), (1, 1)),            # pink  -> top-left
        Ghost("INKY",   "I", (8, 5), (W - 2, H - 2)),    # cyan  -> bottom-right
        Ghost("CLYDE",  "C", (7, 7), (1, H - 2)),        # orange-> bottom-left
    ]
    dots = {(x, y) for y, row in enumerate(MAZE)
            for x, c in enumerate(row) if c in ".P"}

    print("Pac-Man Ghost AI — four personalities, one target-tile rule each")
    print("=" * 60)
    print("@ = Pac-Man   B/P/I/C = the four ghosts   · = dots")

    # CHASE/SCATTER schedule (classic games alternate on a timer)
    def mode_at(step):
        return "SCATTER" if (step // 7) % 3 == 0 else "CHASE"

    blinky = ghosts[0]
    for step in range(1, 41):
        mode = mode_at(step)

        # Pac-Man acts
        pac_dir, pac = pac_move(pac, pac_dir, ghosts)
        dots.discard(pac)

        # Ghosts act (Blinky first so Inky can use his fresh position)
        for g in ghosts:
            tgt = g.target(pac, pac_dir, blinky.pos, mode)
            g.step(tgt)

        caught = [g for g in ghosts if g.pos == pac]
        if step % 5 == 0 or caught or not dots:
            render(pac, ghosts, dots, step, mode)
            if step % 5 == 0 and not caught:
                for g in ghosts:
                    tgt = g.target(pac, pac_dir, blinky.pos, mode)
                    print(f"    {g.name:6s} at {g.pos} heading for {tgt}")

        if caught:
            print("\n" + "=" * 60)
            print(f"Caught by {caught[0].name} on step {step}! The pincer closed.")
            print("Notice how Pinky and Inky cut angles while Blinky chases straight —")
            print("coordinated-looking behaviour from four independent 1-line rules.")
            return
        if not dots:
            print("\nAll dots eaten — Pac-Man cleared the maze!")
            return

    print("\n" + "=" * 60)
    print("Pac-Man survived the run. Each ghost followed only its own target rule;")
    print("the 'teamwork' is emergent, not scripted — the enduring lesson of 1980.")


if __name__ == "__main__":
    main()
