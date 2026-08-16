"""Typed state/action records for offline continuation research."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionIntent:
    """One seat's complete action at a continuation turn."""

    farmer: tuple[Any, ...]
    hands: tuple[tuple[Any, ...], ...]
    market: tuple[tuple[Any, ...], ...]

    @classmethod
    def from_raw(cls, action: dict[str, Any] | None) -> "ActionIntent":
        action = action or {}
        farmer = tuple(action.get("farmer") or ["PASS"])
        hands = tuple(tuple(order or ["PASS"]) for order in (action.get("hands") or []))
        market = tuple(tuple(order) for order in (action.get("market") or []))
        return cls(farmer=farmer, hands=hands, market=market)


@dataclass(frozen=True)
class ContinuationState:
    episode_id: str
    seat: int
    turn: int
    replay_index: int
    day: int | None
    money: float
    hands: int
    hires_today: int | None
    unlocked_quadrants: int
    animals: tuple[tuple[str, int], ...]
    pastures: int
    plants: int
    wheat_reserve: int
    wheat_shed: int
    fertilizer_shed: int
    milk_shed: int
    wool_shed: int
    wheat_price: float | None
    strawberry_price: float | None
    melon_price: float | None

    @classmethod
    def from_registry_row(cls, row: dict[str, Any]) -> "ContinuationState":
        def integer(name: str, default: int | None = None) -> int | None:
            value = row.get(name, "")
            if value in ("", None):
                return default
            return int(float(value))

        def number(name: str) -> float | None:
            value = row.get(name, "")
            if value in ("", None):
                return None
            return float(value)

        import json

        animals = tuple(sorted((json.loads(row.get("animals", "{}")) or {}).items()))
        return cls(
            episode_id=str(row["episode_id"]),
            seat=int(row["seat"]),
            turn=int(row["turn"]),
            replay_index=int(row["replay_index"]),
            day=integer("day"),
            money=number("money") or 0.0,
            hands=integer("hands", 0) or 0,
            hires_today=integer("hires_today"),
            unlocked_quadrants=integer("unlocked_quadrants", 0) or 0,
            animals=animals,
            pastures=integer("pastures", 0) or 0,
            plants=integer("plants", 0) or 0,
            wheat_reserve=integer("wheat_reserve", 0) or 0,
            wheat_shed=integer("wheat_shed", 0) or 0,
            fertilizer_shed=integer("fertilizer_shed", 0) or 0,
            milk_shed=integer("milk_shed", 0) or 0,
            wool_shed=integer("wool_shed", 0) or 0,
            wheat_price=number("wheat_price"),
            strawberry_price=number("strawberry_price"),
            melon_price=number("melon_price"),
        )
