"""
RTS Skirmish AI  ·  即时战略 AI（命令与征服 / 红色警戒 风格）
============================================================

Real-time-strategy AI (Command & Conquer, Red Alert, StarCraft, Age of Empires)
is not one algorithm but a *stack of managers* running every tick, each a simple
authored policy:

  * Economy manager    - harvesters gather ore -> credits; keep power positive
                         (a power deficit causes brownouts that halve harvesting).
  * Build-order / tech - a prioritized "what do I lack most?" policy builds one
                         structure per turn: power, then economy, then tech.
  * Production manager  - each production building makes ONE unit per turn (a real
                         build queue), so armies grow gradually, not instantly.
  * Tactical manager    - attack only when you actually win the fight; each
                         engagement spends the army, so you must mass up again.

Classic RTS AI famously *cheats a little* (map vision, resource bonuses on hard
difficulty) because a fair, fully strategic AI is very hard to author — the honest
strategic version is what learning systems (AlphaStar) finally cracked.

Two doctrines fight: SOVIETS RUSH infantry from a barracks, hoping to crack the
base before the tanks roll; ALLIES turtle behind pillboxes and tech to heavy
tanks that out-scale infantry.  Who wins is a timing question — the central
balance problem of RTS design.  Deterministic.  Standard library only:
    python command_conquer_ai.py
"""

# --------------------------------------------------------------------------- #
# Static game data.
# --------------------------------------------------------------------------- #
BUILDINGS = {
    "Power Plant": dict(cost=300, power=+100),
    "Refinery":    dict(cost=1400, power=-30),      # +1 harvester
    "Barracks":    dict(cost=500, power=-20),       # produces infantry
    "War Factory": dict(cost=1200, power=-30),      # produces tanks
    "Pillbox":     dict(cost=400, power=-10, defense=10),
}
UNITS = {
    "Rifleman": dict(cost=100, strength=4),
    "Tank":     dict(cost=700, strength=22),
}
# What razing hits first: production, then the defensive wall, then economy, then
# the Construction Yard.  Eroding defense early makes engagements snowball.
RAZE_ORDER = ["War Factory", "Barracks", "Pillbox", "Refinery", "Power Plant",
              "Construction Yard"]


class Base:
    def __init__(self, name, doctrine):
        self.name = name
        self.doctrine = doctrine
        self.credits = 2000
        self.harvesters = 2
        self.buildings = {"Construction Yard": 1, "Power Plant": 1, "Refinery": 1}
        self.units = []
        self.alive = True

    def power_balance(self):
        produced = 100 * self.buildings.get("Power Plant", 0)
        consumed = sum(-BUILDINGS.get(b, {}).get("power", 0) * n
                       for b, n in self.buildings.items())
        return produced - consumed

    def income(self):
        return self.harvesters * (100 if self.power_balance() >= 0 else 50)

    def has(self, b):
        return self.buildings.get(b, 0) > 0

    def army(self):
        return sum(UNITS[u]["strength"] for u in self.units)

    def defense(self):
        return self.army() + BUILDINGS["Pillbox"]["defense"] * self.buildings.get("Pillbox", 0)

    # ---- one structure per turn (build order policy) --------------------- #
    def next_building(self):
        c = self.credits
        if self.power_balance() < 30 and c >= 300:
            return "Power Plant"
        if self.doctrine == "rush":
            if not self.has("Barracks") and c >= 500:
                return "Barracks"                    # then just produce infantry
        else:  # economy -> turtle -> tanks
            if self.buildings.get("Pillbox", 0) < 4 and c >= 400 and c < 1800:
                return "Pillbox"                     # wall goes up first
            if self.buildings.get("Refinery", 0) < 2 and c >= 1400:
                return "Refinery"
            if self.buildings.get("Pillbox", 0) < 4 and c >= 400:
                return "Pillbox"
            if not self.has("War Factory") and c >= 1200:
                return "War Factory"
        return None

    # ---- production: one unit per production building per turn ------------ #
    def produce(self):
        if self.doctrine == "rush":
            for _ in range(self.buildings.get("Barracks", 0)):
                if self.credits >= UNITS["Rifleman"]["cost"]:
                    self.credits -= UNITS["Rifleman"]["cost"]
                    self.units.append("Rifleman")
        else:
            for _ in range(self.buildings.get("War Factory", 0)):
                if self.credits >= UNITS["Tank"]["cost"]:
                    self.credits -= UNITS["Tank"]["cost"]
                    self.units.append("Tank")

    def build(self, name):
        self.credits -= BUILDINGS[name]["cost"]
        self.buildings[name] = self.buildings.get(name, 0) + 1
        if name == "Refinery":
            self.harvesters += 1

    def blayout(self):
        return " ".join(f"{n}×{c}" for n, c in self.buildings.items() if c)


def remove_strength(base, amount):
    base.units.sort(key=lambda u: UNITS[u]["strength"])
    while amount > 0 and base.units:
        amount -= UNITS[base.units.pop(0)]["strength"]


def raze(base, overrun, log):
    to_raze = max(1, overrun // 10)
    for b in RAZE_ORDER:
        while base.buildings.get(b, 0) > 0 and to_raze > 0:
            base.buildings[b] -= 1
            if base.buildings[b] == 0:
                del base.buildings[b]
            if b == "Refinery":
                base.harvesters = max(1, base.harvesters - 1)
            to_raze -= 1
            log.append(f"        💥 razes {base.name}'s {b}")
            if b == "Construction Yard":
                base.alive = False
                return


def resolve_attack(atk, dfn, log):
    a, d = atk.army(), dfn.defense()
    log.append(f"    ⚔  {atk.name} attacks ({a}) vs {dfn.name} defense ({d})")
    if a > d:
        remove_strength(atk, d)
        dfn.units.clear()
        overrun = a - d
        log.append(f"        breakthrough! overrun {overrun}")
        raze(dfn, overrun, log)
    else:
        atk.units.clear()
        remove_strength(dfn, a)
        log.append(f"        {dfn.name} repels the assault (attacker army lost)")


def wants_attack(s, enemy):
    if s.doctrine == "rush":
        return s.army() >= 20 and s.army() > enemy.defense()   # strike when winning
    return s.army() >= 60 and s.army() > enemy.defense()       # heavy tank fist


# --------------------------------------------------------------------------- #
# Match loop
# --------------------------------------------------------------------------- #
def main():
    soviets = Base("SOVIETS", "rush")
    allies = Base("ALLIES", "economy")
    sides = [soviets, allies]

    print("RTS Skirmish AI — SOVIETS (infantry rush)  vs  ALLIES (economy → tanks)")
    print("=" * 72)

    for turn in range(1, 61):
        log = []
        for s in sides:
            if not s.alive:
                continue
            s.credits += s.income()
            b = s.next_building()
            if b:
                s.build(b)
            s.produce()

        for s in sides:
            enemy = allies if s is soviets else soviets
            if s.alive and enemy.alive and wants_attack(s, enemy):
                resolve_attack(s, enemy, log)

        if log or turn % 8 == 0 or not all(x.alive for x in sides):
            print(f"\n── Turn {turn} " + "─" * 46)
            for s in sides:
                print(f"  {s.name:8s} ${s.credits:5d} | harv {s.harvesters} | "
                      f"army {s.army():3d} | def {s.defense():3d} | pwr {s.power_balance():+4d}")
                print(f"           {s.blayout()}")
            for line in log:
                print(line)

        if not all(x.alive for x in sides):
            winner = next(x for x in sides if x.alive)
            print("\n" + "=" * 72)
            print(f"🏆  {winner.name} win on turn {turn} — enemy Construction Yard destroyed.")
            print("   " + ("The rush cracked the base before heavy armor could arrive."
                           if winner is soviets else
                           "Pillboxes soaked the rush; massed tanks then out-scaled the "
                           "infantry and\n   rolled the over-extended attacker."))
            print("   Same engine, different doctrines — the winner is a *balance* knob,\n"
                  "   which is why studios spend so long tuning RTS AI.")
            return

    lead = max(sides, key=lambda s: (s.army(), s.credits))
    print("\n" + "=" * 72)
    print(f"Time limit — {lead.name} hold the stronger position (no base destroyed).")


if __name__ == "__main__":
    main()
