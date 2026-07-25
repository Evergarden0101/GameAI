"""
Mario Kart Item & Catch-Up AI  ·  马里奥卡丁车道具与追赶 AI
=========================================================

Arcade kart racers hide a lot of AI in the *item system*, not the driving.  Two
classic mechanisms keep every race close and chaotic — Nintendo's "fun over fair"
philosophy in action:

  1. POSITION-BASED ITEM DISTRIBUTION ("rubber-band items").  The item you roll
     from a box depends on your PLACE, not chance alone.  Front-runners get weak,
     defensive items (bananas, green shells); back-markers get powerful catch-up
     items (mushrooms, stars, bullets, and the infamous blue shell that homes on
     1st place).  This is deliberate dynamic difficulty adjustment.

  2. RUBBER-BANDING SPEED.  Trailing karts get a small top-speed boost and leaders
     are quietly slowed, compressing the pack.

Here 6 AI karts race with both systems.  The AI also DECIDES when to use its item
(hold a shell defensively when someone's behind; fire the blue shell when not in
1st).  Deterministic (seeded).  Standard library only:
    python mario_kart_items.py
"""

import random

rng = random.Random(3)
TRACK_LEN = 1200.0

# Item roulette weighted by race position (1 = leader ... 6 = last).
# Each entry: item -> weight.  Note how power shifts to the back of the pack.
ITEM_TABLE = {
    1: {"banana": 6, "green_shell": 3, "mushroom": 1},
    2: {"banana": 4, "green_shell": 4, "mushroom": 2},
    3: {"green_shell": 3, "mushroom": 4, "red_shell": 3},
    4: {"mushroom": 4, "red_shell": 3, "star": 2, "blue_shell": 1},
    5: {"mushroom": 3, "star": 3, "blue_shell": 2, "bullet": 2},
    6: {"star": 3, "blue_shell": 3, "bullet": 4},
}


def roll_item(place):
    table = ITEM_TABLE[place]
    items, weights = zip(*table.items())
    return rng.choices(items, weights=weights)[0]


class Kart:
    def __init__(self, name):
        self.name = name
        self.pos = 0.0
        self.base_speed = rng.uniform(9.4, 10.2)   # slight skill spread
        self.speed_mod = 1.0                        # transient item effects
        self.item = None
        self.star_ticks = 0
        self.stunned = 0

    def place_boost(self, place, field):
        """Rubber-banding: trailing karts run faster, the leader a touch slower."""
        return 1.0 + 0.02 * (place - 1) - 0.015 * (field - place)


def positions(karts):
    order = sorted(karts, key=lambda k: -k.pos)
    return {k: i + 1 for i, k in enumerate(order)}      # kart -> place (1-based)


def use_item(kart, place, karts, log):
    """Simple item-use policy."""
    if kart.item is None:
        return
    item = kart.item
    behind = [k for k in karts if k is not kart and k.pos < kart.pos]

    if item == "blue_shell" and place != 1:
        leader = max(karts, key=lambda k: k.pos)
        leader.stunned = 3
        log.append(f"    💙 {kart.name} fires a BLUE SHELL at leader {leader.name}!")
        kart.item = None
    elif item in ("banana", "green_shell") and behind:
        # hold defensively until someone is close behind, then drop/fire
        nearest = max(behind, key=lambda k: k.pos)
        if kart.pos - nearest.pos < 25:
            nearest.stunned = 2
            log.append(f"    🍌 {kart.name} drops a {item}; {nearest.name} is hit!")
            kart.item = None
    elif item in ("mushroom", "star", "bullet", "red_shell"):
        if item == "star":
            kart.star_ticks = 12
            log.append(f"    ⭐ {kart.name} goes STAR — invincible & fast!")
        elif item == "bullet":
            kart.speed_mod = 2.2
            log.append(f"    🚀 {kart.name} fires a BULLET BILL and rockets forward!")
        elif item == "mushroom":
            kart.speed_mod = 1.6
            log.append(f"    🍄 {kart.name} uses a mushroom boost.")
        else:  # red_shell
            ahead = [k for k in karts if k.pos > kart.pos]
            if ahead:
                target = min(ahead, key=lambda k: k.pos - kart.pos)
                target.stunned = 2
                log.append(f"    🔴 {kart.name} lands a RED SHELL on {target.name}.")
        kart.item = None


def main():
    names = ["Mario", "Luigi", "Peach", "Bowser", "Yoshi", "Toad"]
    karts = [Kart(n) for n in names]
    field = len(karts)

    print("Mario Kart Item & Catch-Up AI — position-based items + rubber-banding")
    print("=" * 70)
    print("6 karts, 1 lap. Watch back-markers roll power items and close the gap.\n")

    dt = 1.0
    tick = 0
    box_timer = {k: rng.randint(2, 5) for k in karts}

    while max(k.pos for k in karts) < TRACK_LEN and tick < 300:
        tick += 1
        place = positions(karts)
        log = []

        for k in karts:
            # item boxes: grant an item based on current place
            if k.item is None:
                box_timer[k] -= 1
                if box_timer[k] <= 0:
                    k.item = roll_item(place[k])
                    box_timer[k] = rng.randint(4, 8)

            use_item(k, place[k], karts, log)

            # resolve movement
            if k.stunned > 0 and k.star_ticks == 0:
                k.stunned -= 1
                continue
            speed = k.base_speed * k.place_boost(place[k], field) * k.speed_mod
            if k.star_ticks > 0:
                speed *= 1.4
                k.star_ticks -= 1
            k.pos += speed * dt
            k.speed_mod += (1.0 - k.speed_mod) * 0.25       # decay boosts back to 1

        if log or tick % 25 == 0:
            print(f"-- tick {tick:3d} " + "-" * 30)
            order = sorted(karts, key=lambda k: -k.pos)
            standings = "  ".join(f"{i+1}.{k.name}({k.pos:4.0f})"
                                  for i, k in enumerate(order))
            print("   " + standings)
            for line in log:
                print(line)

    order = sorted(karts, key=lambda k: -k.pos)
    print("\n" + "=" * 70)
    print("🏁 FINISH:")
    for i, k in enumerate(order):
        print(f"   {i+1}. {k.name:6s}  ({k.pos:.0f} m)")
    spread = order[0].pos - order[-1].pos
    print(f"\n1st→last spread: {spread:.0f} m over a {TRACK_LEN:.0f} m lap — the item")
    print("AI and rubber-banding kept the pack tight, exactly as arcade racers intend.")


if __name__ == "__main__":
    main()
