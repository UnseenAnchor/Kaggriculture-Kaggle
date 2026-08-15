"""V42: working-capital-funded fifth-hand capacity scheduler.

One mechanism hypothesis:
The high-supply and CARE failure families both convert more of the farm's
available work into output than v27.  Episode 92978681 exposes the smallest
observable intervention: the same opening Wheat liquidity cycle funds a fifth
hand at step 0.  Keeping that extra hand productive on unmet CARE, fertilizer,
harvest, and water jobs should raise throughput without changing animal mix,
Yarn policy, or the fixed route of the original four hands.

This is a research overlay. It does not modify agents/main.py.
"""
import copy

_base_namespace = {}
with open("agents/main.py", "r", encoding="utf-8") as _base_file:
    exec(compile(_base_file.read(), "agents/main.py", "exec"), _base_namespace)


def _tile_jobs(obs):
    seat = int(obs.get("player", 0) or 0)
    farm = obs.get("farms", [])[seat]
    tiles = farm.get("tiles", [])
    jobs = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            kind = tile.get("kind")
            pos = (x, y)
            if kind == "PASTURE" and tile.get("animal"):
                if not tile.get("cared_today"):
                    jobs.append((0, pos, ["CARE"]))
                elif tile.get("fertilizer_available"):
                    jobs.append((1, pos, ["COLLECT_FERTILIZER"]))
                elif tile.get("yield_units", 0) > 0:
                    jobs.append((2, pos, ["HARVEST"]))
            elif kind == "PLANT":
                if tile.get("yield_units", 0) > 0:
                    jobs.append((3, pos, ["HARVEST"]))
                elif not tile.get("watered_today"):
                    jobs.append((4, pos, ["WATER"]))
    jobs.sort(key=lambda row: (row[0], abs(row[1][0] - 4) + abs(row[1][1] - 4), row[1]))
    return farm, jobs


def _move_toward(position, target):
    x, y = position
    tx, ty = target
    if x < tx:
        return ["EAST"]
    if x > tx:
        return ["WEST"]
    if y < ty:
        return ["SOUTH"]
    if y > ty:
        return ["NORTH"]
    return ["PASS"]


def _extra_hand_action(obs):
    farm, jobs = _tile_jobs(obs)
    hands = list(farm.get("hands", []) or [])
    if not hands or not jobs:
        return ["PASS"]
    position = tuple(hands[-1])
    _, target, operation = jobs[0]
    if position == target:
        return list(operation)
    return _move_toward(position, target)


def _extra_hand_exists(obs, configuration, step):
    seat = int(obs.get("player", 0) or 0)
    farms = obs.get("farms", []) or []
    actual = len((farms[seat] if seat < len(farms) else {}).get("hands", []) or [])
    actions = (
        _base_namespace["_REBALANCE_ACTIONS"]
        if _base_namespace["_regime"](configuration) == "rebalance"
        else _base_namespace["_LEGACY_ACTIONS"]
    )
    planned = len((actions[step] or {}).get("hands", []) or [])
    return actual > planned


def agent(obs, configuration=None):
    action = copy.deepcopy(_base_namespace["agent"](obs, configuration))
    step = int(obs.get("step", 0) or 0)
    if step == 0:
        action["market"] = [
            ["BUY_PRODUCT", "WHEAT", 14],
            ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
            ["BUY_ANIMAL", "COW", 1],
            ["BUY_ANIMAL", "SHEEP", 4],
            ["BUY_SEED", "MELON", 5],
            ["BUY_SEED", "WHEAT", 5],
            ["HIRE"],
        ]
    elif step == 1:
        action["market"] = [
            ["SELL", "WHEAT", 9],
            ["BUY_SEED", "MELON", 3],
            ["BUY_SEED", "WHEAT", 2],
        ]
    if step >= 1 and action.get("hands") and _extra_hand_exists(obs, configuration, step):
        action["hands"][-1] = _extra_hand_action(obs)
    return action
