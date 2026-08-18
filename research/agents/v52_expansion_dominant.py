"""Lean, conservative Kaggriculture controller.

The farm backbone is a 6-cow/12-sheep dominant-branch expansion route from episode 93730164.  The adaptive
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
    'EOhfpz/zjC3r/YGq6dHoq+dSOauP/w/vLLA2'
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
