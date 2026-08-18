"""Lean, conservative Kaggriculture controller.

The farm backbone is an 8-cow/4-sheep high-throughput route.  The adaptive
layer is deliberately narrow: repair weed-blocked productive actions, move an
already-planned premium-product sale forward by exactly one turn when no town
demand occurs, repay that move on the original turn, and bank/liquidate only at
the very end.  Worker inventories are never treated as directly sellable.
"""
import base64
import copy
import json
import math
import zlib


# Lean 8-cow/4-sheep route selected after comparing the two stronger public
# candidates. The payload is data only; the adaptive wrapper below is ours.
_LEAN_ACTIONS = json.loads(zlib.decompress(base64.b64decode(
    (
    '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'
    )
)).decode("utf-8"))
_LEGACY_ACTIONS = _LEAN_ACTIONS
_REBALANCE_ACTIONS = _LEAN_ACTIONS
del _LEAN_ACTIONS
_PRICE_FLOOR = 1
_DEMAND_ALPHA = 0.25
_MARKET_PARAMS = {
    "WHEAT": (25, 10000, 400, "sqrt", 0.8, "log", 0.2),
    "CARROT": (35, 10000, 450, "log", 0.2, "sqrt", 0.7),
    "TOMATO": (60, 10000, 200, "linear", 0.4, "sqrt", 0.6),
    "STRAWBERRY": (120, 10000, 100, "sqrt", 0.7, "linear", 1.6),
    "MELON": (250, 10000, 300, "log", 0.2, "sq", 3.6),
    "EGG": (50, 10000, 332, "linear", 0.4, "log", 0.2),
    "MILK": (160, 10000, 122, "sqrt", 0.6, "linear", 1.6),
    "WOOL": (200, 10000, 105, "log", 0.2, "sq", 3.2),
    "FERTILIZER": (100, 10000, 200, "linear", 0.4, "linear", 0.4),
}
_SHOP_PRODUCTS = {
    "BAKERY": ("EGG", "WHEAT"),
    "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"),
    "YARN_STORE": ("WOOL",),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"),
    "PET_CAFE": ("CARROT",),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}
_WEED_STATE = {0: {}, 1: {}}
_SALE_STATE = {0: {}, 1: {}}
_WEED_BLOCKED_OPS = {"BUILD_PASTURE", "BUILD_COOP", "PLANT", "PLACE"}
_PREMIUM_ITEMS = ("MELON", "MILK", "STRAWBERRY", "WOOL")
_TERMINAL_ROUTE_TURNS = 1
_TERMINAL_MIN_LOAD_VALUE = 300


def _get(value, key, default=None):
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _regime(configuration):
    interval = int(_get(configuration, "townCenterSellInterval", 12) or 12)
    return "rebalance" if interval >= 24 else "legacy"


def _copy_action(action):
    action = copy.deepcopy(action or {})
    return {
        "farmer": list(action.get("farmer") or ["PASS"]),
        "hands": [list(order or ["PASS"]) for order in (action.get("hands") or [])],
        "market": [list(order) for order in (action.get("market") or [])],
    }


def _seat(obs):
    return 1 if int(_get(obs, "player", 0) or 0) == 1 else 0


def _farm(obs, seat):
    farms = list(_get(obs, "farms", []) or [])
    return farms[seat] if seat < len(farms) else {}


def _align_hands(action, obs):
    action = _copy_action(action)
    expected = len(_get(_farm(obs, _seat(obs)), "hands", []) or [])
    hands = list(action.get("hands") or [])
    if len(hands) < expected:
        hands.extend([["PASS"] for _ in range(expected - len(hands))])
    action["hands"] = [list(order or ["PASS"]) for order in hands[:expected]]
    return action


def _tile_at(farm, position):
    try:
        x, y = int(position[0]), int(position[1])
        return (_get(farm, "tiles", []) or [])[y][x]
    except (IndexError, TypeError, ValueError):
        return "LOCKED"


def _weed_repair_action(obs, action, actions, step):
    action = _align_hands(action, obs)
    seat = _seat(obs)
    game = _WEED_STATE[seat]
    day = _positive_count(_get(obs, "day", step // 24))
    previous_day = game.get("day") if game else None
    if (
        not game
        or step == 0
        or step <= game.get("last_step", -1)
    ):
        game = {"last_step": step, "day": day, "pending": {}}
        _WEED_STATE[seat] = game
    elif day != previous_day:
        # Hired hands disappear at day end, so their actor indices cannot keep
        # delayed actions.  The permanent farmer (index 0) persists and keeps
        # its queue across the boundary.
        farmer_queue = game.get("pending", {}).get(0)
        game["pending"] = {0: farmer_queue} if farmer_queue else {}
    game["last_step"] = step
    game["day"] = day

    # Preserve the last two turns for endgame banking and liquidation.
    if step >= len(actions) - 2:
        return action

    farm = _farm(obs, seat)
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    unit_actions = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    pending = game["pending"]

    for index, (position, intended) in enumerate(zip(positions, unit_actions)):
        intended = list(intended) if isinstance(intended, list) and intended else ["PASS"]
        queue = pending.get(index)
        if queue:
            unit_actions[index] = list(queue.pop(0))
            if intended[0] != "PASS":
                queue.append(intended)
            if queue:
                pending[index] = queue
            else:
                pending.pop(index, None)
            continue
        if intended[0] not in _WEED_BLOCKED_OPS:
            continue
        tile = _tile_at(farm, position)
        if not isinstance(tile, dict) or tile.get("kind") != "WEED":
            continue
        pending[index] = [intended]
        unit_actions[index] = ["DIG"]

    action["farmer"] = unit_actions[0] if unit_actions else ["PASS"]
    action["hands"] = unit_actions[1:]
    return _align_hands(action, obs)


def _shape(name, value):
    value = max(0.0, float(value))
    if name == "linear":
        return value
    if name == "sq":
        return value * value
    if name == "sqrt":
        return math.sqrt(value)
    if name == "log":
        return math.log1p(value)
    if name == "log10":
        return math.log10(1.0 + value)
    raise ValueError(name)


def _market_parameters(item, configuration=None):
    names = (
        "base", "I0", "T", "below_func", "below_target",
        "above_func", "above_target",
    )
    values = list(_MARKET_PARAMS[item])
    configured = _get(configuration, "marketParams", {}) or {}
    override = _get(configured, item, {}) or {}
    for index, name in enumerate(names):
        value = _get(override, name, None)
        if value is not None:
            values[index] = value
    return values


def _market_price(item, inventory, configuration=None):
    base, equilibrium, scale, below_func, below_target, above_func, above_target = (
        _market_parameters(item, configuration)
    )
    base = float(base)
    equilibrium = int(equilibrium)
    scale = max(1.0, float(scale))
    below_target = float(below_target)
    above_target = float(above_target)
    if inventory < equilibrium:
        amplitude = below_target * base / _shape(below_func, scale)
        price = base + amplitude * _shape(below_func, equilibrium - inventory)
    else:
        amplitude = above_target * base / _shape(above_func, scale)
        price = base - amplitude * _shape(above_func, inventory - equilibrium)
    return max(_PRICE_FLOOR, int(round(price)))


def _is_sell(order):
    return (
        isinstance(order, (list, tuple))
        and len(order) >= 3
        and order[0] == "SELL"
        and order[1] in _MARKET_PARAMS
    )


def _impact_score(obs, order, configuration=None):
    if not _is_sell(order):
        return float("-inf")
    item = str(order[1])
    try:
        quantity = max(0, int(order[2]))
    except (TypeError, ValueError):
        return 0.0
    market = _get(obs, "market", {}) or {}
    inventory = _get(market, "inventory", {}) or {}
    prices = _get(market, "prices", {}) or {}
    current_inventory = int(_get(inventory, item, 10000) or 0)
    current_quote = float(
        _get(
            prices,
            item,
            _market_price(item, current_inventory, configuration),
        ) or 0
    )
    later_quote = float(
        _market_price(item, current_inventory + quantity, configuration)
    )
    return float(quantity) * max(0.0, current_quote - later_quote)


def _demand_per_day(obs, configuration, item):
    town = _get(obs, "town", {}) or {}
    shops = list(_get(town, "unlocked_shops", []) or [])
    turns_per_day = int(_get(configuration, "turnsPerDay", 24) or 24)
    shop_interval = max(
        1, int(_get(configuration, "townShopSellInterval", 4) or 4)
    )
    demand = 0.0
    for shop in shops:
        products = _SHOP_PRODUCTS.get(shop, ())
        if item in products:
            demand += (turns_per_day / shop_interval) * (
                2 if len(products) == 1 else 1
            )
    regime = _regime(configuration)
    if item != "FERTILIZER":
        center_default = 24 if regime == "rebalance" else 12
        center_interval = max(
            1,
            int(
                _get(configuration, "townCenterSellInterval", center_default)
                or center_default
            ),
        )
        day = int(_get(obs, "day", int(_get(obs, "step", 0) or 0) // 24) or 0)
        multiplier = (
            1
            if regime == "rebalance"
            else (4 if day >= 20 else 2 if day >= 10 else 1)
        )
        demand += (turns_per_day / center_interval) * multiplier
    return demand


def _order_score(obs, configuration, order):
    score = _impact_score(obs, order, configuration)
    if _regime(configuration) != "rebalance" or score <= 0 or not _is_sell(order):
        return score
    item = str(order[1])
    quantity = max(0, int(order[2]))
    market = _get(obs, "market", {}) or {}
    inventory = _get(market, "inventory", {}) or {}
    current_inventory = int(_get(inventory, item, 10000) or 0)
    demand = max(0.25, _demand_per_day(obs, configuration, item))
    excess = max(0.0, current_inventory + quantity - 10000)
    urgency = min(1.0, (excess / demand) / 10.0)
    return score * (1.0 + _DEMAND_ALPHA * urgency)


def _rank_sell_slots(obs, action, configuration):
    action = _copy_action(action)
    market = list(action.get("market") or [])
    rows = [
        (_order_score(obs, configuration, order), -index, list(order))
        for index, order in enumerate(market)
        if _is_sell(order)
    ]
    if len(rows) < 2:
        return action
    rows.sort(reverse=True)
    ranked = iter(row[2] for row in rows)
    action["market"] = [next(ranked) if _is_sell(order) else order for order in market]
    return action


def _positive_count(value):
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def _isolated_sale_revenue(obs, configuration, order):
    """Exact own-order revenue if no concurrent opponent order hits this item."""
    if not _is_sell(order):
        return 0
    item = str(order[1])
    quantity = _positive_count(order[2])
    market = _get(obs, "market", {}) or {}
    inventories = _get(market, "inventory", {}) or {}
    quotes = _get(market, "prices", {}) or {}
    inventory = _positive_count(_get(inventories, item, 10000))
    revenue = 0
    for unit in range(quantity):
        if unit == 0:
            price = _positive_count(
                _get(
                    quotes,
                    item,
                    _market_price(item, inventory, configuration),
                )
            )
        else:
            price = _market_price(item, inventory, configuration)
        price = max(_PRICE_FLOOR, int(price))
        revenue += price
        # At the price floor, the engine buys the unit without increasing the
        # market inventory.  Future units therefore remain responsive to buys.
        if price > _PRICE_FLOOR:
            inventory += 1
    return revenue


def _shed_products(obs):
    """Return product counts that SELL can actually access this turn."""
    private = _get(obs, "private", {}) or {}
    shed = _get(private, "shed", {}) or {}
    return {
        item: _positive_count(_get(shed, item, 0))
        for item in _MARKET_PARAMS
        if _positive_count(_get(shed, item, 0)) > 0
    }


def _episode_steps(configuration):
    return max(1, _positive_count(_get(configuration, "episodeSteps", 720)) or 720)


def _is_final_action(obs, configuration):
    # Kaggle's episodeSteps includes the initial state, hence the last action is
    # normally numbered episodeSteps - 2 (718 for the standard 720-step game).
    step = _positive_count(_get(obs, "step", 0))
    return step >= max(0, _episode_steps(configuration) - 2)


def _shed_access(farm):
    size = len(_get(farm, "tiles", []) or []) or 10
    half = size // 2
    return {
        (half - 1, half - 1), (half, half - 1),
        (half - 1, half), (half, half),
    }


def _position(value):
    try:
        return int(value[0]), int(value[1])
    except (IndexError, TypeError, ValueError):
        return None


def _inventory_value(obs, inventory):
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    return sum(
        _positive_count(count) * _positive_count(_get(prices, item, 1))
        for item, count in (inventory or {}).items()
        if item in _MARKET_PARAMS
    )


def _route_to_shed(position, sheds, farm):
    """Return one legal Manhattan step toward a shed-access tile."""
    if position is None or not sheds:
        return ["PASS"]
    x, y = position
    target = min(
        sheds,
        key=lambda q: (abs(q[0] - x) + abs(q[1] - y), q[1], q[0]),
    )
    tx, ty = target
    candidates = []
    if tx < x:
        candidates.append(("WEST", (x - 1, y)))
    if tx > x:
        candidates.append(("EAST", (x + 1, y)))
    if ty < y:
        candidates.append(("NORTH", (x, y - 1)))
    if ty > y:
        candidates.append(("SOUTH", (x, y + 1)))
    tiles = _get(farm, "tiles", []) or []
    size = len(tiles)
    for operation, (nx, ny) in candidates:
        if 0 <= nx < size and 0 <= ny < size:
            return [operation]
    return ["PASS"]


def _terminal_bank(obs, action, configuration):
    """Route valuable reachable loads to the shed during the final window."""
    step = _positive_count(_get(obs, "step", 0))
    final_step = max(0, _episode_steps(configuration) - 2)
    first_route_step = max(0, final_step - _TERMINAL_ROUTE_TURNS)
    if step < first_route_step or step >= final_step:
        return action
    action = _align_hands(action, obs)
    farm = _farm(obs, _seat(obs))
    positions = [_get(farm, "farmer"), *list(_get(farm, "hands", []) or [])]
    inventories = list(
        _get(_get(obs, "private", {}) or {}, "inventories", []) or []
    )
    unit_actions = [action["farmer"], *action["hands"]]
    sheds = _shed_access(farm)
    turns_remaining = final_step - step
    for index, position in enumerate(positions):
        inventory = inventories[index] if index < len(inventories) else {}
        load = sum(_positive_count(value) for value in (inventory or {}).values())
        pos = _position(position)
        if load <= 0 or pos is None or index >= len(unit_actions):
            continue
        if pos in sheds:
            unit_actions[index] = ["DROP"]
            continue
        distance = min(
            abs(pos[0] - target[0]) + abs(pos[1] - target[1])
            for target in sheds
        )
        value = _inventory_value(obs, inventory)
        scheduled = unit_actions[index] if unit_actions[index] else ["PASS"]
        safe_override = scheduled[0] == "PASS"
        if distance + 1 <= turns_remaining and (
            value >= _TERMINAL_MIN_LOAD_VALUE or safe_override
        ):
            unit_actions[index] = _route_to_shed(pos, sheds, farm)
    action["farmer"] = unit_actions[0]
    action["hands"] = unit_actions[1:]
    return action


def _terminal_liquidation(obs, action, configuration):
    step = _positive_count(_get(obs, "step", 0))
    final_step = max(0, _episode_steps(configuration) - 2)
    if step < max(0, final_step - _TERMINAL_ROUTE_TURNS):
        return action
    action = _copy_action(action)
    orders = [
        ["SELL", item, quantity]
        for item, quantity in _shed_products(obs).items()
    ]
    orders.sort(
        key=lambda order: (
            _isolated_sale_revenue(obs, configuration, order),
            _order_score(obs, configuration, order),
            order[1],
        ),
        reverse=True,
    )
    limit = _positive_count(
        _get(configuration, "maxMarketOrdersPerTurn", 10)
    ) or 10
    action["market"] = orders[:limit]
    return action


def _opening_feed_first(action, step):
    """Put the opening feed purchase before animals and hires."""
    if step != 0:
        return action
    action = _copy_action(action)
    market = action["market"]
    for index, order in enumerate(market):
        if len(order) >= 3 and order[:2] == ["BUY_PRODUCT", "WHEAT"]:
            action["market"] = [market[index], *market[:index], *market[index + 1:]]
            break
    return action


def _reduce_sale(action, item, quantity):
    """Repay a previous pull-forward without making any count negative."""
    remaining = _positive_count(quantity)
    market = []
    for raw in action.get("market", []) or []:
        order = list(raw)
        if remaining and _is_sell(order) and order[1] == item:
            sold = _positive_count(order[2])
            reduction = min(sold, remaining)
            sold -= reduction
            remaining -= reduction
            if sold == 0:
                continue
            order[2] = sold
        market.append(order)
    action["market"] = market
    return remaining


def _town_demand_now(obs, item, step, configuration):
    """Whether town demand will replenish this item after market actions."""
    turns_per_day = _positive_count(_get(configuration, "turnsPerDay", 24)) or 24
    center_interval = _positive_count(
        _get(configuration, "townCenterSellInterval", turns_per_day)
    ) or turns_per_day
    if item != "FERTILIZER" and step % center_interval == 0:
        return True
    shop_interval = _positive_count(
        _get(configuration, "townShopSellInterval", 4)
    ) or 4
    if step % shop_interval:
        return False
    town = _get(obs, "town", {}) or {}
    for shop in list(_get(town, "unlocked_shops", []) or []):
        if item in _SHOP_PRODUCTS.get(str(shop), ()):
            return True
    return False


def _pickup_reserve(action, item):
    """Stock needed by same-turn worker pickups before farm actions execute."""
    reserve = 0
    orders = [action.get("farmer", ["PASS"]), *list(action.get("hands") or [])]
    for order in orders:
        if (
            isinstance(order, (list, tuple))
            and len(order) >= 2
            and order[0] == "PICKUP"
            and order[1] == item
        ):
            reserve += _positive_count(order[2]) if len(order) >= 3 else 1
    return reserve


def _existing_sell(action, item):
    return sum(
        _positive_count(order[2])
        for order in (action.get("market", []) or [])
        if _is_sell(order) and order[1] == item
    )


def _premium_front_run(obs, action, actions, step, configuration):
    """Move only tomorrow's premium sales to today, then conserve quantity."""
    seat = _seat(obs)
    state = _SALE_STATE[seat]
    if not state or step == 0 or step <= state.get("last_step", -1):
        state = {"last_step": step, "debt": {}}
        _SALE_STATE[seat] = state
    state["last_step"] = step
    debt = state["debt"]
    action = _copy_action(action)

    due = dict(debt.pop(step, {}))
    for item, quantity in due.items():
        unpaid = _reduce_sale(action, item, quantity)
        if unpaid:
            following = debt.setdefault(step + 1, {})
            following[item] = following.get(item, 0) + unpaid

    final_step = max(0, _episode_steps(configuration) - 2)
    future_step = step + 1
    if (
        step >= final_step - 1
        or future_step >= len(actions)
    ):
        return action
    limit = _positive_count(
        _get(configuration, "maxMarketOrdersPerTurn", 10)
    ) or 10
    shed = _shed_products(obs)
    moved = {}
    for item in _PREMIUM_ITEMS:
        if _town_demand_now(obs, item, step, configuration):
            continue
        planned = sum(
            _positive_count(order[2])
            for order in (actions[future_step].get("market", []) or [])
            if _is_sell(order) and order[1] == item
        )
        if planned <= 0:
            continue
        committed = _existing_sell(action, item)
        available = max(
            0,
            shed.get(item, 0) - committed - _pickup_reserve(action, item),
        )
        quantity = min(planned, available)
        if quantity <= 0:
            continue
        existing = next(
            (
                order for order in action["market"]
                if _is_sell(order) and order[1] == item
            ),
            None,
        )
        if existing is not None:
            existing[2] = _positive_count(existing[2]) + quantity
        elif len(action["market"]) < limit:
            action["market"].append(["SELL", item, quantity])
        else:
            continue
        moved[item] = moved.get(item, 0) + quantity
    if moved:
        tomorrow = debt.setdefault(future_step, {})
        for item, quantity in moved.items():
            tomorrow[item] = tomorrow.get(item, 0) + quantity
    return action


def agent(obs, configuration=None):
    try:
        actions = (
            _REBALANCE_ACTIONS
            if _regime(configuration) == "rebalance"
            else _LEGACY_ACTIONS
        )
        step = min(max(0, int(_get(obs, "step", 0) or 0)), len(actions) - 1)
        action = _weed_repair_action(
            obs, _copy_action(actions[step]), actions, step
        )
        action = _opening_feed_first(action, step)
        action = _premium_front_run(
            obs, action, actions, step, configuration
        )
        action = _rank_sell_slots(obs, action, configuration)
        action = _terminal_bank(obs, action, configuration)
        action = _terminal_liquidation(obs, action, configuration)
        return _align_hands(action, obs)
    except Exception:
        farm = _farm(obs, _seat(obs))
        return {
            "farmer": ["PASS"],
            "hands": [["PASS"] for _ in (_get(farm, "hands", []) or [])],
            "market": [],
        }


def _kaggle_submission_entrypoint(obs, configuration=None):
    return agent(obs, configuration)
