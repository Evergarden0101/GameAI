"""
Adversarial Search: Minimax + Alpha-Beta  ·  博弈搜索：极小化极大 + α-β 剪枝
==========================================================================

The classic AI for two-player, perfect-information games (chess, checkers,
Connect Four, tic-tac-toe) is MINIMAX: assume both players play optimally, and
score each move by the value of the position it leads to, where one player
maximizes and the other minimizes.  ALPHA-BETA PRUNING skips branches that
cannot change the decision — the same answer, far fewer nodes explored.  Deep
Blue's win over Kasparov (1997) was alpha-beta minimax on custom hardware.

This sample:
  * plays perfect tic-tac-toe (an unbeatable opponent),
  * shows minimax playing itself to the inevitable DRAW, and
  * counts nodes to show how much work alpha-beta saves.

Runs on the Python standard library only:
    python minimax_tictactoe.py
"""

import random

WINS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),        # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),        # cols
        (0, 4, 8), (2, 4, 6)]                    # diagonals


def winner(b):
    for a, c, d in WINS:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return None


def moves(b):
    return [i for i, v in enumerate(b) if v == " "]


def show(b):
    rows = ["|".join(b[i:i + 3]) for i in range(0, 9, 3)]
    print("\n-+-+-\n".join(rows))


# --------------------------------------------------------------------------- #
# Minimax with alpha-beta pruning.  Returns (score, best_move).
# Score is from X's perspective: +10-depth for an X win, -(10-depth) for O,
# 0 for a draw.  Subtracting depth makes it prefer FAST wins / SLOW losses.
# --------------------------------------------------------------------------- #
def minimax(b, player, depth=0, alpha=-999, beta=999, counter=None, prune=True):
    if counter is not None:
        counter[0] += 1

    w = winner(b)
    if w == "X":
        return 10 - depth, None
    if w == "O":
        return depth - 10, None
    if not moves(b):
        return 0, None

    best_move = None
    if player == "X":                            # maximizing
        best = -999
        for m in moves(b):
            b[m] = "X"
            score, _ = minimax(b, "O", depth + 1, alpha, beta, counter, prune)
            b[m] = " "
            if score > best:
                best, best_move = score, m
            alpha = max(alpha, best)
            if prune and beta <= alpha:
                break                            # β cut-off
        return best, best_move
    else:                                        # minimizing
        best = 999
        for m in moves(b):
            b[m] = "O"
            score, _ = minimax(b, "X", depth + 1, alpha, beta, counter, prune)
            b[m] = " "
            if score < best:
                best, best_move = score, m
            beta = min(beta, best)
            if prune and beta <= alpha:
                break                            # α cut-off
        return best, best_move


def best_move(b, player, prune=True):
    _, m = minimax(b, player, prune=prune)
    return m


# --------------------------------------------------------------------------- #
# Demonstrations
# --------------------------------------------------------------------------- #
def demo_selfplay():
    print("1) Minimax vs Minimax — perfect play always draws")
    print("-" * 58)
    b = [" "] * 9
    player = "X"
    while winner(b) is None and moves(b):
        b[best_move(b, player)] = player
        player = "O" if player == "X" else "X"
    show(b)
    print(f"\nResult: {winner(b) or 'DRAW'}  (as theory predicts)\n")


def demo_pruning():
    print("2) Alpha-beta prunes without changing the answer")
    print("-" * 58)
    b = [" "] * 9
    full, pruned = [0], [0]
    m1 = minimax(b, "X", counter=full, prune=False)[1]
    m2 = minimax(b, "X", counter=pruned, prune=True)[1]
    print(f"Opening move (plain minimax): cell {m1},  nodes visited: {full[0]:,}")
    print(f"Opening move (alpha-beta):    cell {m2},  nodes visited: {pruned[0]:,}")
    print(f"Same move, {100*(1-pruned[0]/full[0]):.0f}% fewer nodes explored.\n")


def demo_vs_random(games=200):
    print(f"3) Perfect AI (X) vs a random player (O) over {games} games")
    print("-" * 58)
    rng = random.Random(0)
    tally = {"X": 0, "O": 0, "DRAW": 0}
    for _ in range(games):
        b = [" "] * 9
        player = "X"
        while winner(b) is None and moves(b):
            if player == "X":
                b[best_move(b, "X")] = "X"
            else:
                b[rng.choice(moves(b))] = "O"
            player = "O" if player == "X" else "X"
        tally[winner(b) or "DRAW"] += 1
    print(f"AI wins: {tally['X']}   draws: {tally['DRAW']}   AI losses: {tally['O']}")
    print("The perfect AI never loses — the whole point of minimax.\n")


def main():
    print("Adversarial Search — Minimax + Alpha-Beta (tic-tac-toe)")
    print("=" * 58 + "\n")
    demo_selfplay()
    demo_pruning()
    demo_vs_random()


if __name__ == "__main__":
    main()
