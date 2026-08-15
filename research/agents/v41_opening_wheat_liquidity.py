"""V41 candidate: replay-derived opening Wheat working-capital cycle.

Mechanism hypothesis:
The same production route lost value when it could not front-load a small
Wheat purchase and liquidate it one turn later.  Reproducing that two-turn
cash cycle may preserve the opening HIRE/animal/seed route while changing
only early liquidity and market inventory.

Evidence: episode 92994559 seat 1 bought 14 WHEAT at step 0, sold 9 at step 1,
and then bought 3 MELON + 2 WHEAT seeds; the v27 near-neighbor bought only
5 WHEAT at step 0 and made no step-1 market orders.
"""
import copy

# Local research overlay only. Kaggle's runner executes this file from the
# project root, so the active baseline remains loaded without copying it.
_base_namespace = {}
with open("agents/main.py", "r", encoding="utf-8") as _base_file:
    exec(compile(_base_file.read(), "agents/main.py", "exec"), _base_namespace)


def _opening_liquidity(action, step):
    action = copy.deepcopy(action or {})
    market = [list(order) for order in action.get("market", [])]
    if step == 0:
        # Match the observed working-capital cycle: buy 14 Wheat before the
        # fixed opening purchases, leaving 9 units to sell on step 1.
        opening = [
            ["BUY_PRODUCT", "WHEAT", 14],
            ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
            ["BUY_ANIMAL", "COW", 1],
            ["BUY_ANIMAL", "SHEEP", 4],
            ["BUY_SEED", "MELON", 5],
            ["BUY_SEED", "WHEAT", 5],
        ]
        action["market"] = opening
    elif step == 1:
        action["market"] = [
            ["SELL", "WHEAT", 9],
            ["BUY_SEED", "MELON", 3],
            ["BUY_SEED", "WHEAT", 2],
        ]
    else:
        action["market"] = market
    return action


def agent(obs, configuration=None):
    action = _base_namespace["agent"](obs, configuration)
    step = int(obs.get("step", 0) or 0)
    return _opening_liquidity(action, step)
