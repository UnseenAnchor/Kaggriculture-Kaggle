"""
Kaggriculture baseline agent v2
================================
Clean-room implementation of the converged public meta (2026-08), informed by:
  - bovard/kaggriculture-getting-started (official tutorial)
  - cjlcjlcjl "What the Top Farms Do — a Live Meta"
  - raykkretzschmar "Findings from Zero to Top Meta"
  - amerob/kaggriculture (verified price model; supply-constrained finding)
  - monim343 journal (melon = first-mover race; other lines recover in 4-8 days)
  - forum: Balance Changes (shops drawn WITH replacement; engine >= 1.32.6)

Meta decisions baked in:
  1. Opening (day 0, hour 0): HIRE x4; 1 COW + 2 SHEEP; wheat/strawberry/melon seeds.
  2. Land: NE early, SW later; never SE (negative ROI per community testing).
  3. Hands: ~8-10/day inside the fib-cheap region (first 10 hands ~ $143/day).
  4. Metered selling: small batches (<=5/order) for premium lines; never dump.
  5. Melon = first-mover race: perfect watering in the age 6-10 window,
     sell fast once ripe; abort if the opponent crashed the price first.
  6. Fertilizer sidecar: collect daily, sell early (no town demand -> permanent glut).
  7. Feed animals with bought wheat (log glut curve -> wheat never gets expensive).
  8. Shed hygiene: DROP when shed-adjacent; sell before the 100-item cap.
  9. Endgame (step >= 690): liquidate everything; only bank cash counts.
 10. Supply-constrained market: prioritize production uptime over selling tricks.
"""

BOARD = 10
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]
QUADS = {"NW": (0, 0), "NE": (5, 0), "SW": (0, 5), "SE": (5, 5)}

CROPS = {
    "WHEAT":      {"seed": 10,  "base": 25,  "one_shot": True,  "first": 2,  "maxd": 4},
    "CARROT":     {"seed": 20,  "base": 35,  "one_shot": True,  "first": 2,  "maxd": 3},
    "TOMATO":     {"seed": 50,  "base": 60,  "one_shot": False, "first": 8,  "maxd": 11},
    "STRAWBERRY": {"seed": 100, "base": 120, "one_shot": False, "first": 10, "maxd": 16},
    "MELON":      {"seed": 80,  "base": 250, "one_shot": True,  "first": 10, "maxd": 10},
}
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

# ---- strategy knobs (meta-informed) ----
OPENING_HIRES = 4
TARGET_HANDS_EARLY = 6        # days 1-5
TARGET_HANDS_MID = 10         # once economy rolls
HAND_CASH_FLOOR = 300
MELON_PATCH = 6
STRAWBERRY_PLOTS = 6
WHEAT_PLOTS = 2
TARGET_COWS = 6
TARGET_SHEEP = 4
SELL_BATCH = 5
MAX_ORDERS = 10
MELON_ABORT_PRICE = 20        # opponent won the melon race -> hold
SELL_FLOOR_FRAC = 0.45        # hold premium below this fraction of base
ENDGAME_STEP = 690
FEED_BUFFER_DAYS = 2

STRUCT_FOR = {"COW": "PASTURE", "SHEEP": "PASTURE", "GOOSE": "COOP"}
BUILD_OP = {"PASTURE": "BUILD_PASTURE", "COOP": "BUILD_COOP"}


def _step_toward(fx, fy, tx, ty):
    if fx < tx: return "EAST"
    if fx > tx: return "WEST"
    if fy < ty: return "SOUTH"
    if fy > ty: return "NORTH"
    return None


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _quad_of(x, y):
    for q, (ox, oy) in QUADS.items():
        if ox <= x < ox + 5 and oy <= y < oy + 5:
            return q
    return None


def agent(obs, config=None):
    me = obs.farms[obs.player]
    priv = obs.private
    day, hour, step = obs.day, obs.hour, obs.step
    tiles = me.tiles
    shed = dict(priv.shed)
    seeds = priv.seeds
    invs = list(priv.inventories)
    prices = obs.market.prices
    unlocked = set(me.unlocked_quadrants)
    money = me.money

    units = [("farmer", tuple(me.farmer))] + [("hand", tuple(p)) for p in me.hands]
    while len(invs) < len(units):
        invs.append({})

    # ================= MARKET =================
    market = []

    def order(*args):
        if len(market) < MAX_ORDERS:
            market.append(list(args))

    # -- land: NE then SW (never SE) --
    if day == 0:
        pass  # day-0 buys handled above; never BUY_LAND on day 0
    elif "NE" not in unlocked and day >= 2 and money >= 1800:
        order("BUY_LAND"); money -= 1000
    elif "SW" not in unlocked and "NE" in unlocked and day >= 6 and money >= 4000:
        order("BUY_LAND"); money -= 2000

    # -- opening buys: day 0 hour 0 only (animal-first meta: animals need no watering;
    #    crop seeds arrive day 1 once labor is hired) --
    if day == 0 and hour == 0:
        order("BUY_ANIMAL", "COW", 1)
        order("BUY_ANIMAL", "SHEEP", 2)
        order("BUY_SEED", "WHEAT", 4)

    # -- staged herd growth (not on day 0: budget + labor are opening-constrained) --
    cows = sum(1 for row in tiles for t in row
               if isinstance(t, dict) and t.get("animal") == "COW")
    sheep = sum(1 for row in tiles for t in row
                if isinstance(t, dict) and t.get("animal") == "SHEEP")
    animals_count = cows + sheep + sum(1 for row in tiles for t in row
                                       if isinstance(t, dict) and t.get("animal") == "GOOSE")
    if day >= 1 and hour == 0:
        cow_target = min(TARGET_COWS, 1 + day // 4)
        sheep_target = min(TARGET_SHEEP, 2 + day // 5)
        if cows + shed.get("COW", 0) < cow_target and money >= 1200:
            order("BUY_ANIMAL", "COW", 1); money -= 400
        if sheep + shed.get("SHEEP", 0) < sheep_target and money >= 1300:
            order("BUY_ANIMAL", "SHEEP", 1); money -= 500

    # -- feed security --
    feed_need = animals_count * FEED_BUFFER_DAYS
    if animals_count > 0 and shed.get("WHEAT", 0) < feed_need:
        buy_n = min(feed_need * 2 - shed.get("WHEAT", 0), 10)
        if buy_n > 0 and money >= prices["WHEAT"] * buy_n + 50:
            order("BUY_PRODUCT", "WHEAT", buy_n)
            money -= prices["WHEAT"] * buy_n

    # -- crop seeds arrive from day 1, once hands exist to water them --
    if day == 1 and hour == 0 and money >= 80 * MELON_PATCH + 100 * STRAWBERRY_PLOTS + 200:
        order("BUY_SEED", "MELON", MELON_PATCH)
        order("BUY_SEED", "STRAWBERRY", STRAWBERRY_PLOTS)
    elif day >= 2 and hour == 0:
        if seeds.get("STRAWBERRY", 0) == 0 and day < 12 and money >= 100 * STRAWBERRY_PLOTS + 400:
            order("BUY_SEED", "STRAWBERRY", STRAWBERRY_PLOTS)
        if seeds.get("MELON", 0) == 0 and day < 8 and money >= 80 * MELON_PATCH + 400:
            order("BUY_SEED", "MELON", MELON_PATCH)
        if seeds.get("WHEAT", 0) == 0 and day < 8 and money >= 100:
            order("BUY_SEED", "WHEAT", WHEAT_PLOTS)

    # -- hires: fill remaining order slots AFTER buys (10-order cap per turn) --
    if hour == 0:
        if day == 0:
            target = OPENING_HIRES
        elif money > 4000 or day >= 8:
            target = TARGET_HANDS_MID
        else:
            target = TARGET_HANDS_EARLY
        hires = me.hires_today
        while hires < target and money - _fib(hires) >= (0 if day == 0 else 60):
            order("HIRE")
            money -= _fib(hires)
            hires += 1

    # -- selling --
    endgame = step >= ENDGAME_STEP
    melon_crashed = prices["MELON"] <= MELON_ABORT_PRICE

    def sell_line(item, batch, floor_frac):
        n = shed.get(item, 0)
        if n <= 0:
            return
        if endgame or prices[item] >= BASE_PRICE[item] * floor_frac:
            take = min(n, batch)
            order("SELL", item, take)
            shed[item] = n - take

    if endgame:
        for item in ("WHEAT", "EGG", "CARROT", "TOMATO"):
            sell_line(item, 20, 0.0)
        for item in ("STRAWBERRY", "MILK", "WOOL", "FERTILIZER", "MELON"):
            sell_line(item, SELL_BATCH, 0.0)
    else:
        sell_line("FERTILIZER", 10, 0.30)
        sell_line("MILK", SELL_BATCH, SELL_FLOOR_FRAC)
        sell_line("STRAWBERRY", SELL_BATCH, SELL_FLOOR_FRAC)
        sell_line("WOOL", SELL_BATCH, SELL_FLOOR_FRAC)
        if not melon_crashed:
            sell_line("MELON", SELL_BATCH, 0.0)
        surplus = shed.get("WHEAT", 0) - feed_need
        if surplus > 5:
            take = min(surplus, 10)
            order("SELL", "WHEAT", take)
            shed["WHEAT"] = shed.get("WHEAT", 0) - take
        sell_line("EGG", 10, 0.5)
        sell_line("CARROT", 10, 0.5)
        sell_line("TOMATO", 10, 0.5)

    # ================= FIELD =================
    def empty_owned_tiles():
        out = []
        for y in range(BOARD):
            for x in range(BOARD):
                if tiles[y][x] is None and _quad_of(x, y) in unlocked:
                    d = min(abs(x - sx) + abs(y - sy) for sx, sy in SHED_TILES)
                    out.append((d, x, y))
        out.sort()
        return [(x, y) for _, x, y in out]

    # jobs: (priority, kind, x, y, payload)
    jobs = []
    empty_pastures, empty_coops = [], []
    for y in range(BOARD):
        for x in range(BOARD):
            t = tiles[y][x]
            if not isinstance(t, dict):
                continue
            kind = t.get("kind")
            if kind == "PLANT":
                age = day - t.get("planted_day", day)
                crop = t.get("crop")
                c = CROPS.get(crop, {})
                if c.get("one_shot"):
                    ripe = t.get("yield_units", 0) > 0 and age >= c.get("maxd", 99)
                else:
                    ripe = t.get("yield_units", 0) > 0 and age >= c.get("first", 99)
                if ripe:
                    jobs.append((0, "HARVEST", x, y, None))
                if not t.get("watered_today"):
                    urgent = crop == "MELON" and 6 <= age <= 10
                    jobs.append((1 if urgent else 3, "WATER", x, y, None))
            elif kind in ("COOP", "PASTURE"):
                if t.get("animal"):
                    if not t.get("fed_today"):
                        jobs.append((0, "FEED", x, y, None))
                    if t.get("yield_units", 0) > 0:
                        jobs.append((1, "HARVEST", x, y, None))
                    if t.get("fertilizer_available"):
                        jobs.append((3, "COLLECT_FERTILIZER", x, y, None))
                    if not t.get("cared_today"):
                        jobs.append((4, "CARE", x, y, None))
                else:
                    (empty_pastures if kind == "PASTURE" else empty_coops).append((x, y))
            elif kind == "WEED":
                jobs.append((6, "DIG", x, y, None))

    # planting jobs
    plant_plan = []
    if seeds.get("MELON", 0) > 0:
        plant_plan += ["MELON"] * seeds["MELON"]
    if seeds.get("STRAWBERRY", 0) > 0:
        plant_plan += ["STRAWBERRY"] * seeds["STRAWBERRY"]
    if seeds.get("WHEAT", 0) > 0:
        plant_plan += ["WHEAT"] * min(seeds["WHEAT"], WHEAT_PLOTS)
    if plant_plan:
        spots = empty_owned_tiles()
        for crop, (x, y) in zip(plant_plan, spots):
            jobs.append((3, "PLANT", x, y, crop))

    jobs.sort(key=lambda j: j[0])
    feed_jobs_pending = sum(1 for j in jobs if j[1] == "FEED")

    # shed reservations so units don't grab the same item
    reserved = {"COW": 0, "SHEEP": 0, "GOOSE": 0, "WHEAT": 0}

    # ================= ASSIGN UNITS =================
    actions = {"farmer": ["PASS"], "hands": [], "market": market}
    taken = set()

    for ui, (role, (fx, fy)) in enumerate(units):
        inv = invs[ui] if ui < len(invs) else {}
        carrying_animal = next((a for a in ("COW", "SHEEP", "GOOSE") if inv.get(a, 0) > 0), None)
        wheat_held = inv.get("WHEAT", 0)
        carrying_goods = sum(v for k, v in inv.items()
                             if isinstance(v, int) and k not in ("COW", "SHEEP", "GOOSE", "WHEAT"))
        shed_adj = (fx, fy) in SHED_TILES
        tile = tiles[fy][fx]
        act = None

        # --- 0) end-of-day: hands vanish at day end -> haul everything to the shed ---
        if hour >= 21 and (carrying_goods > 0 or wheat_held > 0 or carrying_animal):
            if shed_adj:
                act = ["DROP"]
            else:
                sx, sy = min(SHED_TILES, key=lambda p: abs(fx - p[0]) + abs(fy - p[1]))
                mv = _step_toward(fx, fy, sx, sy)
                act = [mv] if mv else ["DROP"]

        # --- A) animal logistics chain ---
        if carrying_animal:
            need = STRUCT_FOR[carrying_animal]
            if isinstance(tile, dict) and tile.get("kind") == need and not tile.get("animal"):
                act = ["PLACE", carrying_animal]
            else:
                spots = empty_pastures if need == "PASTURE" else empty_coops
                if spots:
                    tx, ty = min(spots, key=lambda p: abs(fx - p[0]) + abs(fy - p[1]))
                    mv = _step_toward(fx, fy, tx, ty)
                    act = [mv] if mv else ["PLACE", carrying_animal]
                elif tile is None and _quad_of(fx, fy) in unlocked:
                    act = [BUILD_OP[need]]
                else:
                    spots2 = empty_owned_tiles()
                    if spots2:
                        tx, ty = spots2[0]
                        mv = _step_toward(fx, fy, tx, ty)
                        act = [mv] if mv else [BUILD_OP[need]]

        # --- B) shed interactions ---
        if act is None and shed_adj:
            if carrying_goods > 0:
                act = ["DROP"]
            elif shed.get("COW", 0) - reserved["COW"] > 0:
                reserved["COW"] += 1
                act = ["PICKUP", "COW", 1]
            elif shed.get("SHEEP", 0) - reserved["SHEEP"] > 0:
                reserved["SHEEP"] += 1
                act = ["PICKUP", "SHEEP", 1]
            elif shed.get("GOOSE", 0) - reserved["GOOSE"] > 0:
                reserved["GOOSE"] += 1
                act = ["PICKUP", "GOOSE", 1]
            elif feed_jobs_pending > 0 and wheat_held == 0 \
                    and shed.get("WHEAT", 0) - reserved["WHEAT"] > 0:
                take = min(feed_jobs_pending, shed["WHEAT"] - reserved["WHEAT"], 4)
                reserved["WHEAT"] += take
                act = ["PICKUP", "WHEAT", take]

        # --- C) act on current tile ---
        if act is None and isinstance(tile, dict):
            k = tile.get("kind")
            if k == "PLANT":
                age = day - tile.get("planted_day", day)
                crop = tile.get("crop")
                c = CROPS.get(crop, {})
                ripe = tile.get("yield_units", 0) > 0 and (
                    age >= (c.get("maxd", 99) if c.get("one_shot") else c.get("first", 99)))
                if ripe:
                    act = ["HARVEST"]
                elif not tile.get("watered_today"):
                    act = ["WATER"]
            elif k in ("COOP", "PASTURE") and tile.get("animal"):
                if not tile.get("fed_today") and wheat_held > 0:
                    act = ["FEED"]
                elif tile.get("yield_units", 0) > 0:
                    act = ["HARVEST"]
                elif tile.get("fertilizer_available"):
                    act = ["COLLECT_FERTILIZER"]
                elif not tile.get("cared_today"):
                    act = ["CARE"]
            elif k == "WEED":
                act = ["DIG"]

        if act is None and tile is None and _quad_of(fx, fy) in unlocked:
            for j in jobs:
                if j[1] == "PLANT" and j[2] == fx and j[3] == fy and ("PLANT", fx, fy) not in taken:
                    if seeds.get(j[4], 0) > 0:
                        act = ["PLANT", j[4]]
                        taken.add(("PLANT", fx, fy))
                    break

        # --- D) move to nearest job ---
        if act is None:
            best = None
            for j in jobs:
                key = (j[1], j[2], j[3])
                if key in taken:
                    continue
                if j[1] == "FEED" and wheat_held == 0:
                    continue
                d = abs(fx - j[2]) + abs(fy - j[3])
                if best is None or d < best[0]:
                    best = (d, j)
            if best is not None:
                _, j = best
                taken.add((j[1], j[2], j[3]))
                mv = _step_toward(fx, fy, j[2], j[3])
                act = [mv] if mv else ["PASS"]

        # --- E) fallback: haul goods home ---
        if act is None:
            if carrying_goods > 0 and not shed_adj:
                sx, sy = min(SHED_TILES, key=lambda p: abs(fx - p[0]) + abs(fy - p[1]))
                mv = _step_toward(fx, fy, sx, sy)
                act = [mv] if mv else ["PASS"]
            else:
                act = ["PASS"]

        if role == "farmer":
            actions["farmer"] = act
        else:
            actions["hands"].append(act)

    return actions
