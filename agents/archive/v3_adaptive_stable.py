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
ENDGAME_STEP = 672            # day 28: leave 48 turns for orderly liquidation
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

    # Count live assets before buying.  Public-meta targets are plot counts,
    # not seed inventory counts; replenishing whenever seeds hit zero caused
    # runaway 16-melon / 17-strawberry monocultures in the previous version.
    crop_counts = {crop: 0 for crop in CROPS}
    for row in tiles:
        for t in row:
            if isinstance(t, dict) and t.get("kind") == "PLANT":
                crop = t.get("crop")
                if crop in crop_counts:
                    crop_counts[crop] += 1

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

    # -- demand-adaptive staged herd growth --
    # Shops are sampled with replacement. Fixed 6C/4S overproduces wool in no-yarn
    # seasons and underproduces milk in ice-cream/smoothie-heavy seasons.
    shops = list(obs.town.unlocked_shops)
    milk_demand = sum(shops.count(s) for s in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"))
    yarn_count = shops.count("YARN_STORE")
    egg_demand = shops.count("BAKERY") + shops.count("BRUNCH_SPOT")
    berry_demand = sum(shops.count(s) for s in
                       ("BRUNCH_SPOT", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP", "FARMERS_MARKET"))
    carrot_demand = 2 * shops.count("PET_CAFE") + shops.count("FARMERS_MARKET")
    tomato_demand = shops.count("PIZZA_SHOP") + shops.count("FARMERS_MARKET")
    cows = sum(1 for row in tiles for t in row
               if isinstance(t, dict) and t.get("animal") == "COW")
    sheep = sum(1 for row in tiles for t in row
                if isinstance(t, dict) and t.get("animal") == "SHEEP")
    geese = sum(1 for row in tiles for t in row
                if isinstance(t, dict) and t.get("animal") == "GOOSE")
    carried_cows = sum(inv.get("COW", 0) for inv in invs)
    carried_sheep = sum(inv.get("SHEEP", 0) for inv in invs)
    carried_geese = sum(inv.get("GOOSE", 0) for inv in invs)
    animals_count = cows + sheep + geese
    if 1 <= day <= 22 and hour == 0:
        demand_cow_target = 3 + min(5, milk_demand)
        demand_sheep_target = 2 + min(4, yarn_count * 2)
        demand_goose_target = min(3, egg_demand)
        cow_target = min(demand_cow_target, 1 + day // 3)
        sheep_target = min(demand_sheep_target, 2 + day // 4)
        goose_target = min(demand_goose_target, max(0, (day - 5) // 3))
        if cows + shed.get("COW", 0) + carried_cows < cow_target and money >= 1200:
            order("BUY_ANIMAL", "COW", 1); money -= 400
        if sheep + shed.get("SHEEP", 0) + carried_sheep < sheep_target and money >= 1300:
            order("BUY_ANIMAL", "SHEEP", 1); money -= 500
        if geese + shed.get("GOOSE", 0) + carried_geese < goose_target and money >= 900:
            order("BUY_ANIMAL", "GOOSE", 1); money -= 300

    # -- feed security --
    feed_need = animals_count * FEED_BUFFER_DAYS
    if animals_count > 0 and shed.get("WHEAT", 0) < feed_need:
        buy_n = min(feed_need * 2 - shed.get("WHEAT", 0), 10)
        if buy_n > 0 and money >= prices["WHEAT"] * buy_n + 50:
            order("BUY_PRODUCT", "WHEAT", buy_n)
            money -= prices["WHEAT"] * buy_n

    # -- crop seeds: cap by live plots + queued seeds, adapt mix to shop demand --
    # Melon is one early IPO only; unlike all other products, no shop drains it.
    berry_target = STRAWBERRY_PLOTS + min(2, berry_demand // 2)
    carrot_target = min(6, carrot_demand)
    tomato_target = min(4, tomato_demand)
    if 1 <= day <= 3 and hour == 0:
        melon_deficit = max(0, MELON_PATCH - crop_counts["MELON"] - seeds.get("MELON", 0))
        berry_deficit = max(0, berry_target - crop_counts["STRAWBERRY"] - seeds.get("STRAWBERRY", 0))
        if melon_deficit and money >= 80 * melon_deficit + 200:
            order("BUY_SEED", "MELON", melon_deficit)
            money -= 80 * melon_deficit
        if berry_deficit and money >= 100 * berry_deficit + 200:
            order("BUY_SEED", "STRAWBERRY", berry_deficit)
            money -= 100 * berry_deficit
    elif day >= 4 and hour == 0:
        deficits = [
            ("STRAWBERRY", max(0, berry_target - crop_counts["STRAWBERRY"] - seeds.get("STRAWBERRY", 0)), 100, 15),
            ("CARROT", max(0, carrot_target - crop_counts["CARROT"] - seeds.get("CARROT", 0)), 20, 24),
            ("TOMATO", max(0, tomato_target - crop_counts["TOMATO"] - seeds.get("TOMATO", 0)), 50, 15),
            ("WHEAT", max(0, WHEAT_PLOTS - crop_counts["WHEAT"] - seeds.get("WHEAT", 0)), 10, 8),
        ]
        for crop, deficit, cost, last_day in deficits:
            if deficit and day < last_day and money >= cost * deficit + 300:
                order("BUY_SEED", crop, deficit)
                money -= cost * deficit

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
    # Waiting 4-8 days is rational for premium lines, but a fixed threshold can
    # strand 50+ units until the $1 terminal floor. Relax as time runs out.
    if day < 15:
        premium_floor = SELL_FLOOR_FRAC
    elif day < 22:
        premium_floor = 0.30
    elif day < 26:
        premium_floor = 0.18
    else:
        premium_floor = 0.05

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
        sell_line("MILK", SELL_BATCH, premium_floor)
        sell_line("STRAWBERRY", SELL_BATCH, premium_floor)
        sell_line("WOOL", SELL_BATCH, premium_floor)
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
    if seeds.get("CARROT", 0) > 0:
        plant_plan += ["CARROT"] * seeds["CARROT"]
    if seeds.get("TOMATO", 0) > 0:
        plant_plan += ["TOMATO"] * seeds["TOMATO"]
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
