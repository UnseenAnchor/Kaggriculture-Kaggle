"""V47 research candidate: v27 capital anchor followed by full expansion planner.

Hypothesis: v27 wins its opening economy but loses later to routes that keep a
larger production graph alive. Preserve the v27 route through turn 192 (day 8),
then switch only at an observed state boundary to a complete state-driven
planner. This is deliberately not a fifth-hand, CARE, SELL, or raw tape relay.
"""
import copy

_base = {}
with open("agents/main.py", "r", encoding="utf-8") as handle:
    exec(compile(handle.read(), "agents/main.py", "exec"), _base)

_rita = {}
with open("research/agents/components/rancher_rita_scheduler.py", "r", encoding="utf-8") as handle:
    exec(compile(handle.read(), "research/agents/components/rancher_rita_scheduler.py", "exec"), _rita)

_POLICY = copy.deepcopy(_rita["POLICY"])
_POLICY.update({
    "hands": 6,
    "hands_by_day": [(0, 6), (14, 8)],
    "land": 1,
    "land_buffer": 700,
    "build": [{"kind": "PASTURE", "target": 14, "from_day": 16, "until_day": 20}],
    "animals": ["COW", "SHEEP"],
    "animal_target": {"COW": 9, "SHEEP": 4},
    "animal_batch": 2,
    "animal_buffer": 500,
    "animal_floor": 6,
    "land_after_animals": 6,
    "feed_float_days": 10,
    "animals_from_day": 16,
    "feed_days": 3,
    "wheat_batch": 24,
    "max_wheat_price": 60,
    "crops": ["WHEAT", "MELON"],
    "crop_share": {"WHEAT": 0.7, "MELON": 0.3},
    "plant_until": {"WHEAT": 22, "MELON": 18},
    "seed_stock": 8,
    "invest_until_day": 21,
    "plant_until_day": 22,
    "liquidate_from_day": 28,
    "sell_order": ["FERTILIZER", "MILK", "WOOL", "WHEAT", "MELON", "STRAWBERRY"],
    "shed_pressure": 0,
    "price_floor": {"FERTILIZER": 0, "MILK": 0, "WOOL": 0, "WHEAT": 0, "MELON": 0, "STRAWBERRY": 0},
})
_ANCHOR_TURN = 384


def agent(obs, configuration=None):
    step = int(obs.get("step", 0) or 0)
    if step < _ANCHOR_TURN:
        return _base["agent"](obs, configuration)
    try:
        action = _rita["act"](obs, _POLICY)
        farm = (obs.get("farms") or [])[int(obs.get("player", 0) or 0)]
        hands = len(farm.get("hands", []) or [])
        action["hands"] = list(action.get("hands", []) or [])[:hands]
        action["hands"] += [["PASS"] for _ in range(max(0, hands - len(action["hands"])))]
        return action
    except Exception:
        return _base["agent"](obs, configuration)
