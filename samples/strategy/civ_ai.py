"""
4X Empire AI  ·  策略帝国 AI（文明 Civilization 风格）
=====================================================

Turn-based strategy AI (Civilization, Endless Legend, Old World) runs a
UTILITY-based economy every turn: for each city it scores every possible thing it
could build against the empire's current needs and picks the highest.  There is no
search tree — just a bag of hand-tuned scoring functions, which is why Utility AI
(also the brain of *The Sims*) is the workhorse of 4X games.

This sample also demonstrates the open secret of Civ difficulty: on higher levels
the AI is not *smarter*, it just gets **resource bonuses** (extra production and
science, cheaper units).  We run the SAME brain twice — a fair "PRINCE" empire and
a bonus-boosted "DEITY" empire — and watch the handicap, not intelligence, decide
the game.  That is the honest version of "the AI cheats."

Deterministic (shared event stream).  Standard library only:
    python civ_ai.py
"""

# --------------------------------------------------------------------------- #
# Tech tree (priority order) and what each tech unlocks.
# --------------------------------------------------------------------------- #
TECHS = ["Pottery", "Writing", "Bronze Working", "Currency", "Mathematics"]
TECH_COST = {"Pottery": 25, "Writing": 45, "Bronze Working": 70,
             "Currency": 110, "Mathematics": 160}

# Buildings: cost + the empire need they serve.
BUILDINGS = {
    "Granary":  dict(cost=30, needs="Pottery"),        # faster city growth
    "Library":  dict(cost=45, needs="Writing"),        # +science
    "Barracks": dict(cost=35, needs="Bronze Working"), # stronger military
    "Market":   dict(cost=50, needs="Currency"),       # +gold
}
UNITS = {"Settler": 40, "Worker": 20, "Warrior": 15, "Spearman": 25}


class City:
    def __init__(self, name, founded_turn=0):
        self.name = name
        self.pop = 1
        self.food = 0
        self.prod = 0.0            # accumulated production ("hammers")
        self.buildings = set()
        self.building = None       # what we're currently producing
        self.workers = 0

    def yields(self, bonus):
        food = 2 + self.pop + (1 if "Granary" in self.buildings else 0)
        hammers = (1 + self.pop) * bonus
        science = self.pop + (2 if "Library" in self.buildings else 0)
        gold = 1 + (2 if "Market" in self.buildings else 0)
        return food, hammers, science, gold


class Empire:
    def __init__(self, name, prod_bonus=1.0, sci_bonus=1.0):
        self.name = name
        self.prod_bonus = prod_bonus
        self.sci_bonus = sci_bonus
        self.cities = [City("Capital")]
        self.techs = set()
        self.science = 0.0
        self.gold = 0
        self.military = 0          # total combat strength
        self.land = 6              # settle-able city sites remaining

    # ---- utility scoring: what should this city build next? -------------- #
    def choose_build(self, city, threat):
        options = {}

        # EXPAND — settlers are gold early, worthless once land is gone.
        if self.land > 0 and city.pop >= 2:
            options["Settler"] = 10.0 - 1.2 * len(self.cities) + 0.5 * city.pop

        # IMPROVE — workers if the city has unimproved tiles.
        if city.workers < city.pop:
            options["Worker"] = 4.0 + 1.5 * (city.pop - city.workers)

        # DEFEND — military utility scales with the current barbarian threat.
        best_unit = "Spearman" if "Bronze Working" in self.techs else "Warrior"
        options[best_unit] = 3.0 + 2.5 * threat - 0.4 * self.military

        # GROW / TECH / ECONOMY — buildings, gated by tech.
        for b, spec in BUILDINGS.items():
            if b in city.buildings or spec["needs"] not in self.techs:
                continue
            base = {"Granary": 6.5, "Library": 7.5, "Barracks": 5.0, "Market": 6.0}[b]
            options[b] = base - 0.3 * len(city.buildings)

        # pick the highest-utility option
        return max(options, key=options.get), options

    def cost_of(self, item):
        return UNITS.get(item) or BUILDINGS[item]["cost"]

    def complete(self, city, item):
        if item == "Settler" and self.land > 0:
            self.land -= 1
            self.cities.append(City(f"City-{len(self.cities)}"))
        elif item == "Worker":
            city.workers += 1
        elif item in ("Warrior", "Spearman"):
            self.military += 4 if item == "Warrior" else 7
        else:
            city.buildings.add(item)

    def research(self):
        for t in TECHS:
            if t not in self.techs:
                if self.science >= TECH_COST[t]:
                    self.science -= TECH_COST[t]
                    self.techs.add(t)
                    return t
                return None
        return None

    def score(self):
        return (len(self.cities) * 10 + sum(c.pop for c in self.cities) * 3
                + len(self.techs) * 8 + self.military
                + sum(len(c.buildings) for c in self.cities) * 4)

    # ---- one full turn --------------------------------------------------- #
    def take_turn(self, threat, verbose=False):
        newtech = self.research()
        for city in self.cities:
            food, hammers, sci, gold = city.yields(self.prod_bonus)
            self.science += sci * self.sci_bonus
            self.gold += gold

            # growth
            city.food += food
            if city.food >= 10 + city.pop * 2:
                city.food = 0
                city.pop += 1

            # production
            if city.building is None:
                city.building, opts = self.choose_build(city, threat)
                if verbose and city is self.cities[0]:
                    ranked = sorted(opts.items(), key=lambda kv: -kv[1])[:3]
                    picks = ", ".join(f"{k} {v:.1f}" for k, v in ranked)
                    print(f"      · {self.name} {city.name} weighs: {picks}  → {city.building}")
            city.prod += hammers
            if city.prod >= self.cost_of(city.building):
                self.complete(city, city.building)
                city.prod = 0
                city.building = None
        return newtech


def barbarian_stream(turns, seed=1):
    """A deterministic pseudo-random threat level per turn (shared by both AIs)."""
    x = seed
    out = []
    for _ in range(turns):
        x = (1103515245 * x + 12345) & 0x7fffffff       # classic LCG
        out.append((x >> 16) % 3)                        # threat 0,1,2
    return out


def main():
    prince = Empire("PRINCE", prod_bonus=1.0, sci_bonus=1.0)          # fair
    deity = Empire("DEITY ", prod_bonus=1.6, sci_bonus=1.7)           # bonus-boosted

    print("4X Empire AI — Utility-driven cities + the truth about difficulty bonuses")
    print("=" * 74)
    print("Same decision brain in both empires. DEITY only gets +60% production and")
    print("+70% science — no smarter play. Watch the handicap decide the game.\n")

    threats = barbarian_stream(40)
    for turn in range(1, 41):
        threat = threats[turn - 1]
        verbose = turn in (1, 6, 14)
        if verbose:
            print(f"── Turn {turn}  (barbarian threat {threat}) "
                  + "─" * 26)
        t1 = prince.take_turn(threat, verbose)
        t2 = deity.take_turn(threat, verbose)

        # a raid can sack an undefended empire's newest city
        for emp in (prince, deity):
            if threat == 2 and emp.military < 6 and len(emp.cities) > 1:
                lost = emp.cities.pop()             # lose the newest city
                if verbose:
                    print(f"      ! {emp.name} loses {lost.name} to barbarians (undefended)")

        if turn % 8 == 0 or turn == 40:
            print(f"\n  Turn {turn:2d} standings")
            for emp in (prince, deity):
                print(f"    {emp.name}: score {emp.score():3d} | cities {len(emp.cities)} "
                      f"| pop {sum(c.pop for c in emp.cities):2d} | techs {len(emp.techs)} "
                      f"({', '.join(sorted(emp.techs)) or '—'}) | mil {emp.military}")
            print()

    print("=" * 74)
    winner = max((prince, deity), key=lambda e: e.score())
    print(f"🏆  {winner.name.strip()} finishes ahead — score {winner.score()} "
          f"vs {min(prince.score(), deity.score())}.")
    print("Both empires ran the identical utility AI. The gap is pure resource")
    print("bonus — exactly how Civilization scales difficulty. A genuinely *smarter*")
    print("4X AI is very hard to author, so studios reach for the honest cheat instead.")


if __name__ == "__main__":
    main()
