"""
Car Racing Game AI  ·  赛车游戏 AI
=================================

Demonstrates the three classic building blocks of a racing-game opponent:

1. Waypoint following  - the AI drives around a racing line made of waypoints,
   always steering toward a point a little further ahead (a "look-ahead" or
   pure-pursuit controller).
2. PID-style steering + speed control - proportional steering on the heading
   error, and cornering speed that slows down for sharp turns.
3. Rubber-banding (dynamic difficulty adjustment) - the AI speeds up when it
   falls behind the player and eases off when it gets too far ahead, so races
   stay close and fun. This is the trick behind Mario Kart's "catch-up".

Runs on the Python standard library only:  python racing_ai.py
"""

import math


# --------------------------------------------------------------------------- #
# Small 2D vector helper (kept tiny so the file is self-contained)
# --------------------------------------------------------------------------- #
class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = float(x), float(y)

    def __add__(self, o):  return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o):  return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, s):  return Vec2(self.x * s, self.y * s)

    def length(self):      return math.hypot(self.x, self.y)

    def normalized(self):
        n = self.length()
        return Vec2(self.x / n, self.y / n) if n else Vec2()


def angle_of(v: Vec2) -> float:
    return math.atan2(v.y, v.x)


def wrap_angle(a: float) -> float:
    """Wrap an angle to the range (-pi, pi]."""
    while a > math.pi:
        a -= 2 * math.pi
    while a <= -math.pi:
        a += 2 * math.pi
    return a


# --------------------------------------------------------------------------- #
# Track: a closed loop of waypoints (an oval here)
# --------------------------------------------------------------------------- #
def oval_track(n=24, rx=60.0, ry=32.0, cx=0.0, cy=0.0):
    pts = []
    for i in range(n):
        t = (i / n) * 2 * math.pi
        pts.append(Vec2(cx + rx * math.cos(t), cy + ry * math.sin(t)))
    return pts


# --------------------------------------------------------------------------- #
# The AI car
# --------------------------------------------------------------------------- #
class RacingCar:
    def __init__(self, name, track, base_top_speed=18.0):
        self.name = name
        self.track = track
        self.pos = Vec2(track[0].x, track[0].y)
        self.heading = angle_of(track[1] - track[0])
        self.speed = 0.0
        self.base_top_speed = base_top_speed
        self.target_idx = 1          # index of the waypoint we are heading to
        self.laps = 0
        self.progress = 0.0          # total distance travelled (for ranking)

    # ---- controller ------------------------------------------------------- #
    def _steer_toward(self, target: Vec2):
        """Proportional controller: turn toward the target waypoint."""
        desired = angle_of(target - self.pos)
        error = wrap_angle(desired - self.heading)
        # Steering gain (the "P" in PID). Clamp so the car can't spin.
        max_turn = math.radians(9.0)
        return max(-max_turn, min(max_turn, 2.5 * error))

    def _corner_speed(self, target: Vec2):
        """Slow down for sharp upcoming corners, speed up on straights."""
        nxt = self.track[(self.target_idx + 1) % len(self.track)]
        turn = abs(wrap_angle(angle_of(nxt - target) - angle_of(target - self.pos)))
        # turn == 0 on a straight, ~pi on a hairpin.
        straightness = max(0.15, 1.0 - turn / math.pi)
        return self.base_top_speed * straightness

    def update(self, dt, top_speed):
        target = self.track[self.target_idx]

        # advance to the next waypoint once we are close enough (look-ahead)
        if (target - self.pos).length() < 6.0:
            self.target_idx = (self.target_idx + 1) % len(self.track)
            if self.target_idx == 1:
                self.laps += 1
            target = self.track[self.target_idx]

        # steering
        self.heading = wrap_angle(self.heading + self._steer_toward(target))

        # throttle / braking toward the target speed for this corner
        goal_speed = min(top_speed, self._corner_speed(target))
        if self.speed < goal_speed:
            self.speed += 12.0 * dt            # acceleration
        else:
            self.speed -= 20.0 * dt            # braking
        self.speed = max(0.0, self.speed)

        # integrate motion
        step = self.speed * dt
        self.pos = self.pos + Vec2(math.cos(self.heading), math.sin(self.heading)) * step
        self.progress += step


# --------------------------------------------------------------------------- #
# Rubber-banding: adjust the AI's top speed based on the gap to the player.
# --------------------------------------------------------------------------- #
def rubber_banded_top_speed(ai: RacingCar, player: RacingCar):
    gap = player.progress - ai.progress          # +ve => AI is behind
    boost = max(-0.10, min(0.35, gap * 0.012))    # up to +35% behind, -10% ahead
    return ai.base_top_speed * (1.0 + boost)


# --------------------------------------------------------------------------- #
# Simulation
# --------------------------------------------------------------------------- #
def main():
    track = oval_track()
    player = RacingCar("PLAYER", track, base_top_speed=17.0)
    ai     = RacingCar("AI",     track, base_top_speed=16.0)  # slightly slower base

    print("Racing AI demo — waypoint following + rubber-banding")
    print("=" * 58)
    dt = 0.1
    for tick in range(1, 1201):
        # A simple "player" that drives at a steady pace.
        player.update(dt, top_speed=player.base_top_speed)

        # The AI uses rubber-banding to keep the race close.
        ai_top = rubber_banded_top_speed(ai, player)
        ai.update(dt, top_speed=ai_top)

        if tick % 150 == 0:
            gap = player.progress - ai.progress
            tag = "AI behind " if gap > 0 else "AI ahead  "
            print(f"t={tick*dt:5.1f}s | "
                  f"player lap {player.laps} ({player.progress:6.1f}m)  "
                  f"ai lap {ai.laps} ({ai.progress:6.1f}m) | "
                  f"{tag} gap={gap:+6.1f}m  ai_top={ai_top:4.1f}")

    print("-" * 58)
    winner = "PLAYER" if player.progress > ai.progress else "AI"
    print(f"Finish: player={player.progress:.1f}m  ai={ai.progress:.1f}m "
          f"-> {winner} leads. Notice the gap stayed small thanks to "
          f"rubber-banding.")


if __name__ == "__main__":
    main()
