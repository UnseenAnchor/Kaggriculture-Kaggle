"""Lean, conservative Kaggriculture controller.

The farm backbone is a 6-cow/8-sheep expansion route from episode 93604505.  The adaptive
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
    'eNrtXV1vXFdy/CuGnvdBwxkOh3mjpdm1sLQpkFIGG4MwDOwGAYLNg5O3IP89sinO3I/qrqo+547ojyePKXLu+ehzbnd1dfX3'
    '//vq33/86Z//+OnVv3z1/av3Nw8Prx7/9NWr//jxv/7+3z//6Of/+eePP/3nP/7nl//7vz99NfqDrz++u337w6c/+/Dxfp/9'
    '5fevvnn39Bv6p68//u2Hm+/efXtz++rTd725O3z6zwX4l4dv9vv3o3972O/f/vwvh2/2Nx8+fbia/cu3+9u77z59WJ3+6P39'
    '3duPbz4M/277OJvx+3dv/vrx/fCxq9G0v3912D98eJrAd3f3H755+nj64fTTdJ0e9re3wzGs52M4fu/wsXhgo0EMPs42Dg/H'
    '2fBg5qdxPe3garIKn3+VPPf97c2bfbbqeJrHP8PPnsyGjOH570arjsb1y4+/G1jSZCGetzb+XWkv9jfz8Qys6+bD/n5uh7Of'
    'Tu0vOAoXczN8uPs4N0Nk6H/++dBNfjadNdt/uHiTnZgt42Dib26e7fz4i093wHBZCgYwWFA0guMajX5T2l54yvFW4jM2PxLk'
    'ic/7BJd1uFpgj9HvmXv8vEVsecdPAOd7sNBoX0MbX4lXLTxkybXP77bJxPQNwNeett3HwXsL7v1M23q4zM/3G9pRZZ/NhT49'
    '7vTp2SGaf6qs7WCHOjxi7qzhrVjoUcxQuk7r+BXDpy7zBOXTF3/A7G24drz2+T1vv/h6P2F+9/s3xhcf09whI38APKjeY3pz'
    'd3u7f/Phhz/v7z+8u333b9NbqfsyNz7QNrXG551hz45OymCI+Yk9RYGzPwmdl8tH22n+FR4x2zzma7Bphikkx7mPjwZ9YuB+'
    'DyMdcCDqQR70zPCZi2b6+cQUgg8yq/ES8HlLqwtBG9elJ5Fi8FH5ZrJM+KP0zST8MhzvZhAhm0VbOJutvB5IqKeSoS2a3eTR'
    'ZhfoQoUnpe8NMA83WoMh1OC7UVyjXTUIOMujP23E/vc+/awFc+3w/ShcGazz4ONL/uK393fvk+/VLCOP3E6PmP5soYCws28D'
    'ncqNlZNpdYAyrwi9RKb5n9Usk/PpLr6/C9A7+Z5OnQj9+q46S6fnD+/Oqjsgz6Z9wv4CB+mgHi8x5jX08K+Y/1BfNurEZVi3'
    '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'
    'cyiGQP86/ZlnbFl3ElRoj0ZfPZfKWX38f6sF3Ow='
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
