"""Build compact replay/state registries from local Kaggriculture replays.

The raw replay JSON files are intentionally not committed. This command turns
them into small CSVs for failure-family clustering and continuation research.
It compares each seat's observable action stream with the current v27 legacy
tape, but never changes or executes the active agent.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any

SNAPSHOT_TURNS = (0, 24, 96, 192, 288, 384, 480, 576, 719)
HASH_CUTS = (24, 100, 200, 400, 719)
REGISTRY_FIELDS = [
    "episode_id", "seat", "team", "opponent", "reward", "opponent_reward",
    "outcome", "margin", "shops", "first_diff_step", "first_diff_components",
    "diff_turns", "diff_market_turns", "diff_farmer_turns", "diff_hand_turns",
    "action_hash_24", "action_hash_100", "action_hash_200",
    "action_hash_400", "action_hash_719", "unit_counts", "sell_counts",
    "buy_counts", "hires", "land_buys", "final_assets", "final_shed",
]
SNAPSHOT_FIELDS = [
    "episode_id", "seat", "turn", "replay_index", "day", "money", "hands",
    "hires_today", "unlocked_quadrants", "animals", "pastures", "plants",
    "wheat_reserve", "wheat_shed", "fertilizer_shed", "milk_shed", "wool_shed",
    "wheat_price", "strawberry_price", "melon_price",
]


def _load_legacy_actions(root: Path) -> list[dict[str, Any]]:
    path = root / "agents" / "main.py"
    spec = importlib.util.spec_from_file_location("registry_main", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return list(module._LEGACY_ACTIONS)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _action_hash(actions: list[dict[str, Any]], cut: int) -> str:
    payload = _json(actions[:cut])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _counter_json(counter: Counter) -> str:
    return _json(dict(sorted(counter.items())))


def _action_stats(actions: list[dict[str, Any]]) -> tuple[Counter, Counter, Counter, int, int]:
    units: Counter = Counter()
    sells: Counter = Counter()
    buys: Counter = Counter()
    hires = 0
    land_buys = 0
    for action in actions:
        action = action or {}
        for op in [action.get("farmer", ["PASS"])] + list(action.get("hands", []) or []):
            units[(op or ["PASS"])[0]] += 1
        for order in action.get("market", []) or []:
            if not order:
                continue
            if order[0] == "SELL" and len(order) > 2:
                sells[order[1]] += _number(order[2])
            elif order[0] == "HIRE":
                hires += 1
            elif order[0] == "BUY_LAND":
                land_buys += 1
            elif order[0].startswith("BUY_") and len(order) > 2:
                buys[f"{order[0]}:{order[1]}"] += _number(order[2])
    return units, sells, buys, hires, land_buys


def _number(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _farm_counts(farm: dict[str, Any]) -> tuple[Counter, int, int]:
    assets: Counter = Counter()
    pastures = 0
    plants = 0
    for row in farm.get("tiles", []) or []:
        for tile in row or []:
            if not isinstance(tile, dict):
                continue
            if tile.get("animal"):
                assets[tile["animal"]] += 1
            if tile.get("crop"):
                assets[tile["crop"]] += 1
            if tile.get("kind") == "PASTURE":
                pastures += 1
            elif tile.get("kind") == "PLANT":
                plants += 1
    return assets, pastures, plants


def _state_row(episode_id: str, seat: int, turn: int, replay_index: int, step: dict[str, Any]) -> dict[str, Any]:
    obs = step[seat].get("observation", {}) or {}
    farms = obs.get("farms", []) or []
    farm = farms[seat] if seat < len(farms) else {}
    private = obs.get("private", {}) or {}
    shed = private.get("shed", {}) or {}
    inventories = private.get("inventories", []) or []
    carried_wheat = sum(_number((inv or {}).get("WHEAT", 0)) for inv in inventories)
    assets, pastures, plants = _farm_counts(farm)
    market = obs.get("market", {}) or {}
    prices = market.get("prices", {}) or {}
    return {
        "episode_id": episode_id,
        "seat": seat,
        "turn": turn,
        "replay_index": replay_index,
        "day": obs.get("day", ""),
        "money": round(float(farm.get("money", 0) or 0), 3),
        "hands": len(farm.get("hands", []) or []),
        "hires_today": farm.get("hires_today", ""),
        "unlocked_quadrants": len(farm.get("unlocked_quadrants", []) or []),
        "animals": _json({k: assets[k] for k in assets if k in {"COW", "SHEEP", "GOOSE"}}),
        "pastures": pastures,
        "plants": plants,
        "wheat_reserve": _number(shed.get("WHEAT", 0)) + carried_wheat,
        "wheat_shed": _number(shed.get("WHEAT", 0)),
        "fertilizer_shed": _number(shed.get("FERTILIZER", 0)),
        "milk_shed": _number(shed.get("MILK", 0)),
        "wool_shed": _number(shed.get("WOOL", 0)),
        "wheat_price": prices.get("WHEAT", ""),
        "strawberry_price": prices.get("STRAWBERRY", ""),
        "melon_price": prices.get("MELON", ""),
    }


def _divergence(actions: list[dict[str, Any]], legacy: list[dict[str, Any]]) -> dict[str, Any]:
    diff_turns = 0
    market_turns = 0
    farmer_turns = 0
    hand_turns = 0
    first_step = ""
    first_components: list[str] = []
    for i, (actual, expected) in enumerate(zip(actions, legacy)):
        actual = actual or {}
        expected = expected or {}
        components = []
        if actual.get("market", []) != expected.get("market", []):
            market_turns += 1
            components.append("market")
        if actual.get("farmer", ["PASS"]) != expected.get("farmer", ["PASS"]):
            farmer_turns += 1
            components.append("farmer")
        if actual.get("hands", []) != expected.get("hands", []):
            hand_turns += 1
            components.append("hands")
        if components:
            diff_turns += 1
            if first_step == "":
                first_step = i
                first_components = components
    return {
        "first_diff_step": first_step,
        "first_diff_components": ",".join(first_components),
        "diff_turns": diff_turns,
        "diff_market_turns": market_turns,
        "diff_farmer_turns": farmer_turns,
        "diff_hand_turns": hand_turns,
    }


def _registry_row(data: dict[str, Any], seat: int, legacy: list[dict[str, Any]]) -> dict[str, Any]:
    info = data.get("info", {}) or {}
    episode_id = str(info.get("EpisodeId", ""))
    names = info.get("TeamNames", ["", ""])
    other = 1 - seat
    steps = data.get("steps", [])
    final = steps[-1][seat]
    opponent_final = steps[-1][other]
    actions = [(step[seat].get("action") or {}) for step in steps[1:]]
    units, sells, buys, hires, land_buys = _action_stats(actions)
    reward = float(final.get("reward", 0) or 0)
    opponent_reward = float(opponent_final.get("reward", 0) or 0)
    outcome = "W" if reward > opponent_reward else "L" if reward < opponent_reward else "T"
    farm = (final.get("observation", {}).get("farms", []) or [])[seat]
    assets, _, _ = _farm_counts(farm)
    shed = final.get("observation", {}).get("private", {}).get("shed", {}) or {}
    row = {
        "episode_id": episode_id,
        "seat": seat,
        "team": names[seat] if seat < len(names) else "",
        "opponent": names[other] if other < len(names) else "",
        "reward": reward,
        "opponent_reward": opponent_reward,
        "outcome": outcome,
        "margin": reward - opponent_reward,
        "shops": _json((steps[-1][0].get("observation", {}).get("town", {}) or {}).get("unlocked_shops", [])),
        **_divergence(actions, legacy),
        **{f"action_hash_{cut}": _action_hash(actions, cut) for cut in HASH_CUTS},
        "unit_counts": _counter_json(units),
        "sell_counts": _counter_json(sells),
        "buy_counts": _counter_json(buys),
        "hires": hires,
        "land_buys": land_buys,
        "final_assets": _counter_json(assets),
        "final_shed": _json({k: v for k, v in shed.items() if v}),
    }
    return row


def build(input_dir: Path, output_dir: Path, root: Path) -> tuple[int, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    legacy = _load_legacy_actions(root)
    registry: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = []
    paths = sorted(input_dir.glob("episode-*-replay.json"))
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        episode_id = str((data.get("info", {}) or {}).get("EpisodeId", path.stem))
        for seat in (0, 1):
            registry.append(_registry_row(data, seat, legacy))
            for turn in SNAPSHOT_TURNS:
                replay_index = min(turn + 1, len(data.get("steps", [])) - 1)
                snapshots.append(_state_row(episode_id, seat, turn, replay_index, data["steps"][replay_index]))
    with (output_dir / "replay_registry.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REGISTRY_FIELDS)
        writer.writeheader()
        writer.writerows(registry)
    with (output_dir / "replay_state_snapshots.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=SNAPSHOT_FIELDS)
        writer.writeheader()
        writer.writerows(snapshots)
    return len(paths), len(registry)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("research/replays"))
    parser.add_argument("--output-dir", type=Path, default=Path("research/registry"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    episodes, rows = build(args.input_dir, args.output_dir, root)
    print(f"episodes={episodes} seat_rows={rows} snapshot_rows={episodes * 2 * len(SNAPSHOT_TURNS)}")
    print(f"registry={args.output_dir / 'replay_registry.csv'}")
    print(f"snapshots={args.output_dir / 'replay_state_snapshots.csv'}")


if __name__ == "__main__":
    main()
