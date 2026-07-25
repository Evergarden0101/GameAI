"""
Monte-Carlo Tree Search (MCTS)  ·  蒙特卡洛树搜索
=================================================

When a game tree is far too big to search exhaustively with minimax (Go has more
positions than atoms in the universe), MCTS wins instead by *sampling*.  It grows
a search tree by repeating four steps thousands of times:

  1. SELECT   - from the root, follow the child with the best UCB1 score
                (balancing exploitation of good moves vs. exploration of rare ones),
  2. EXPAND   - add one new child node for an untried move,
  3. SIMULATE - play the rest of the game with RANDOM moves ("rollout"),
  4. BACKPROP - push the win/loss back up, updating every node on the path.

The move with the most visits is chosen.  MCTS needs no hand-crafted evaluation
function — just the rules — and it is the search that, fused with deep neural nets,
became AlphaGo (2016).  Here it plays Connect Four and crushes a random opponent.

Deterministic (seeded).  Standard library only:
    python mcts_connect_four.py
"""

import math
import random

ROWS, COLS, CONNECT = 6, 7, 4
SIMS_PER_MOVE = 500
rng = random.Random(42)


# --------------------------------------------------------------------------- #
# Connect Four state.  Board is COLS stacks; player is 1 or 2.
# --------------------------------------------------------------------------- #
class Board:
    def __init__(self):
        self.cols = [[] for _ in range(COLS)]      # cols[c] = bottom..top discs
        self.player = 1                            # whose turn it is
        self.winner = None                         # None, 1, 2, or 0 for draw

    def clone(self):
        b = Board()
        b.cols = [c[:] for c in self.cols]
        b.player = self.player
        b.winner = self.winner
        return b

    def legal(self):
        return [c for c in range(COLS) if len(self.cols[c]) < ROWS]

    def play(self, c):
        self.cols[c].append(self.player)
        if self._wins(c, len(self.cols[c]) - 1, self.player):
            self.winner = self.player
        elif not self.legal():
            self.winner = 0                        # draw
        self.player = 3 - self.player

    def _at(self, c, r):
        return self.cols[c][r] if 0 <= c < COLS and 0 <= r < len(self.cols[c]) else 0

    def _wins(self, c, r, p):
        for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
            n = 1
            for s in (1, -1):
                cc, rr = c + dc * s, r + dr * s
                while self._at(cc, rr) == p:
                    n += 1
                    cc, rr = cc + dc * s, rr + dr * s
            if n >= CONNECT:
                return True
        return False

    def render(self):
        glyph = {0: " .", 1: " X", 2: " O"}
        lines = []
        for r in range(ROWS - 1, -1, -1):
            lines.append("|" + "".join(glyph[self._at(c, r)] for c in range(COLS)) + " |")
        lines.append(" " + " ".join(str(c) for c in range(COLS)))
        return "\n".join(lines)


# --------------------------------------------------------------------------- #
# MCTS
# --------------------------------------------------------------------------- #
class Node:
    __slots__ = ("state", "parent", "move", "children", "wins", "visits", "untried")

    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move                           # move that led here
        self.children = []
        self.wins = 0.0
        self.visits = 0
        self.untried = state.legal()

    def ucb1(self, c=1.41):
        exploit = self.wins / self.visits
        explore = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploit + explore

    def best_child(self):
        return max(self.children, key=lambda n: n.ucb1())


def mcts(root_state, sims):
    root = Node(root_state.clone())
    for _ in range(sims):
        node = root
        state = root_state.clone()

        # 1. SELECT down fully-expanded interior nodes
        while not node.untried and node.children:
            node = node.best_child()
            state.play(node.move)

        # 2. EXPAND one untried move
        if node.untried:
            m = rng.choice(node.untried)
            node.untried.remove(m)
            state.play(m)
            child = Node(state.clone(), parent=node, move=m)
            node.children.append(child)
            node = child

        # 3. SIMULATE a random rollout to the end
        while state.winner is None:
            state.play(rng.choice(state.legal()))
        result = state.winner                      # 0 draw, 1 or 2 winner

        # 4. BACKPROPAGATE (reward from the perspective of the mover at each node)
        while node is not None:
            node.visits += 1
            mover = 3 - node.state.player          # player who just moved into node
            if result == mover:
                node.wins += 1
            elif result == 0:
                node.wins += 0.5
            node = node.parent

    return root


def best_move(state, sims=SIMS_PER_MOVE, report=False):
    root = mcts(state, sims)
    if report:
        print("  MCTS root statistics (move: win-rate over visits):")
        for ch in sorted(root.children, key=lambda n: -n.visits):
            print(f"    col {ch.move}:  {ch.visits:4d} visits, "
                  f"{100*ch.wins/ch.visits:5.1f}% est. win")
    return max(root.children, key=lambda n: n.visits).move


# --------------------------------------------------------------------------- #
# Demo: MCTS (X) vs random (O)
# --------------------------------------------------------------------------- #
def main():
    print("Monte-Carlo Tree Search — MCTS (X) vs a random player (O), Connect Four")
    print("=" * 70)
    print(f"MCTS runs {SIMS_PER_MOVE} random simulations per move — no evaluation")
    print("function, just the rules.\n")

    board = Board()
    print("MCTS 'thinking' about the opening move:")
    best_move(board.clone(), report=True)          # show the first search
    print()

    move_no = 0
    while board.winner is None:
        if board.player == 1:
            m = best_move(board)
        else:
            m = rng.choice(board.legal())
        board.play(m)
        move_no += 1

    print(board.render())
    print()
    outcome = {1: "MCTS (X) wins", 2: "Random (O) wins", 0: "Draw"}[board.winner]
    print("=" * 70)
    print(f"Result after {move_no} moves: {outcome}.")
    print("MCTS reliably beats random play by concentrating its samples on the")
    print("moves that matter — the same idea that, with neural-net guidance,")
    print("became AlphaGo.")


if __name__ == "__main__":
    main()
