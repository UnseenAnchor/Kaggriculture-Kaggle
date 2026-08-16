"""V48 research candidate: respond to an observed large-capacity opening.

Hypothesis: several current failures reveal themselves after step 0 with a
fifth hand and a larger animal/feed opening. Keep the v27 opening unless the
opponent's public farm proves that profile at step 1; then fund exactly one
additional hand each day and schedule it from the live farm state.

Unlike V42, this does not unconditionally change our opening or buy an animal.
Normal opponents remain byte-identical to v27.
"""
import copy

_base = {}
with open("agents/main.py", "r", encoding="utf-8") as handle:
    exec(compile(handle.read(), "agents/main.py", "exec"), _base)

_MODE = {0: False, 1: False}
_LAST_STEP = {0: -1, 1: -1}


def _farm(obs, seat):
    farms = obs.get("farms", []) or []
    return farms[seat] if seat < len(farms) else {}


def _large_opening(obs):
    player = int(obs.get("player", 0) or 0)
    other = 1 - player
    farm = _farm(obs, other)
    animals = {}
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if isinstance(tile, dict) and tile.get("animal"):
                animals[tile["animal"]] = animals.get(tile["animal"], 0) + 1
    hands = len(farm.get("hands", []) or [])
    # This catches both observed high-supply openings and the CARE/cashflow
    # opening, while starter/Hamburger remain below the capacity threshold.
    return hands >= 5 and animals.get("COW", 0) >= 1 and animals.get("SHEEP", 0) >= 2


def _tile_jobs(obs):
    player = int(obs.get("player", 0) or 0)
    farm = _farm(obs, player)
    jobs = []
    for y, row in enumerate(farm.get("tiles", []) or []):
        for x, tile in enumerate(row or []):
            if not isinstance(tile, dict):
                continue
            pos = (x, y)
            if tile.get("kind") == "PASTURE" and tile.get("animal"):
                if not tile.get("cared_today"):
                    jobs.append((0, pos, ["CARE"]))
                elif tile.get("fertilizer_available"):
                    jobs.append((1, pos, ["COLLECT_FERTILIZER"]))
                elif tile.get("yield_units", 0) > 0:
                    jobs.append((2, pos, ["HARVEST"]))
            elif tile.get("kind") == "PLANT":
                if tile.get("yield_units", 0) > 0:
                    jobs.append((3, pos, ["HARVEST"]))
                elif not tile.get("watered_today"):
                    jobs.append((4, pos, ["WATER"]))
    jobs.sort(key=lambda item: (item[0], item[1][1], item[1][0]))
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
    return list(operation) if position == target else _move_toward(position, target)


def _align(action, obs):
    player = int(obs.get("player", 0) or 0)
    expected = len(_farm(obs, player).get("hands", []) or [])
    hands = list(action.get("hands", []) or [])
    hands = hands[:expected]
    hands += [["PASS"] for _ in range(expected - len(hands))]
    action["hands"] = hands
    return action


def agent(obs, configuration=None):
    player = int(obs.get("player", 0) or 0)
    step = int(obs.get("step", 0) or 0)
    if step == 0 or step <= _LAST_STEP[player]:
        _MODE[player] = False
    _LAST_STEP[player] = step
    if not _MODE[player] and 0 <= step <= 8 and _large_opening(obs):
        _MODE[player] = True

    action = copy.deepcopy(_base["agent"](obs, configuration))
    if not _MODE[player]:
        return action

    farm = _farm(obs, player)
    actual_hands = len(farm.get("hands", []) or [])
    hires_today = int(farm.get("hires_today", 0) or 0)
    market = list(action.get("market", []) or [])
    # Hire one extra daily hand, but never spend beyond the engine's order cap.
    if int(obs.get("hour", 0) or 0) <= 2 and hires_today < 5 and len(market) < 10:
        market.append(["HIRE"])
    action["market"] = market[:10]
    action = _align(action, obs)
    if actual_hands >= 5:
        action["hands"][-1] = _extra_hand_action(obs)
    return action
