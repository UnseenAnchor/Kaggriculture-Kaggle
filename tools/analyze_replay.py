"""Print a compact, reproducible postmortem summary for a Kaggriculture replay."""
from collections import Counter
import json
import sys

path = sys.argv[1]
data = json.load(open(path, encoding="utf-8"))
print(f"Episode: {data.get('info', {}).get('EpisodeId')} | teams={data['info']['TeamNames']}")

for agent_index in (0, 1):
    unit = Counter()
    sell = Counter()
    buys = Counter()
    hires = lands = 0
    for step in data["steps"]:
        action = step[agent_index].get("action") or {}
        for op in [action.get("farmer", ["PASS"])] + action.get("hands", []):
            unit[(op or ["PASS"])[0]] += 1
        for order in action.get("market", []):
            if not order:
                continue
            if order[0] == "SELL":
                sell[order[1]] += order[2]
            elif order[0].startswith("BUY_") and len(order) > 2:
                buys[(order[0], order[1])] += order[2]
            elif order[0] == "HIRE":
                hires += 1
            elif order[0] == "BUY_LAND":
                lands += 1

    final = data["steps"][-1][agent_index]
    obs = final["observation"]
    farm = obs["farms"][agent_index]
    assets = Counter()
    for row in farm["tiles"]:
        for tile in row:
            if isinstance(tile, dict):
                if tile.get("crop"):
                    assets[tile["crop"]] += 1
                if tile.get("animal"):
                    assets[tile["animal"]] += 1
    moves = sum(unit[x] for x in ("NORTH", "SOUTH", "EAST", "WEST"))
    print(f"\n[{agent_index}] {data['info']['TeamNames'][agent_index]} reward={final['reward']}")
    print(f"movement={moves/sum(unit.values()):.1%} pass={unit['PASS']} hires={hires} lands={lands}")
    print(f"unit={dict(unit)}")
    print(f"sell={dict(sell)}")
    print(f"buys={dict(buys)}")
    print(f"final_assets={dict(assets)}")
    print(f"final_shed={dict((k, v) for k, v in obs['private']['shed'].items() if v)}")

print(f"\nshops={data['steps'][-1][0]['observation']['town']['unlocked_shops']}")
print("daily_bank: day,agent0,agent1,margin0")
for day in range(30):
    idx = min(day * 24 + 1, len(data["steps"]) - 1)
    banks = [data["steps"][idx][i]["observation"]["farms"][i]["money"] for i in (0, 1)]
    print(f"{day},{banks[0]:.0f},{banks[1]:.0f},{banks[0]-banks[1]:.0f}")
