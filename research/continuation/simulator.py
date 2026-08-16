"""Offline typed continuation trace simulator.

This phase is intentionally descriptive: it can navigate and validate a full
replay trace, but it cannot be used as a Kaggle agent. A future planner will
consume ``ContinuationState`` and emit ``ActionIntent`` only after this trace
layer reproduces complete routes.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .types import ActionIntent, ContinuationState


@dataclass(frozen=True)
class TraceValidation:
    episode_id: str
    seat: int
    action_count: int
    state_count: int
    max_hands: int
    max_animals: int
    max_pastures: int
    unit_counts: tuple[tuple[str, int], ...]
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


class ContinuationSimulator:
    """Typed, read-only view over one complete observable replay route."""

    def __init__(
        self,
        episode_id: str,
        seat: int,
        actions: tuple[ActionIntent, ...],
        states: tuple[ContinuationState, ...],
    ) -> None:
        self.episode_id = episode_id
        self.seat = seat
        self.actions = actions
        self.states = states
        self._states_by_turn = {state.turn: state for state in states}

    @classmethod
    def from_files(
        cls,
        replay_path: str | Path,
        snapshot_path: str | Path = "research/registry/replay_state_snapshots.csv",
        seat: int = 0,
    ) -> "ContinuationSimulator":
        replay_path = Path(replay_path)
        with replay_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        episode_id = str((data.get("info", {}) or {}).get("EpisodeId", replay_path.stem))
        steps = data.get("steps", [])
        actions = tuple(
            ActionIntent.from_raw(step[seat].get("action"))
            for step in steps[1:]
        )
        states = []
        with Path(snapshot_path).open(encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if str(row["episode_id"]) == episode_id and int(row["seat"]) == seat:
                    states.append(ContinuationState.from_registry_row(row))
        states.sort(key=lambda state: state.turn)
        return cls(episode_id, seat, actions, tuple(states))

    def action(self, turn: int) -> ActionIntent:
        return self.actions[turn]

    def state(self, turn: int) -> ContinuationState:
        if turn in self._states_by_turn:
            return self._states_by_turn[turn]
        available = min(self._states_by_turn, key=lambda candidate: abs(candidate - turn))
        return self._states_by_turn[available]

    def profile(self) -> dict[str, Any]:
        units: Counter[str] = Counter()
        market: Counter[str] = Counter()
        for action in self.actions:
            units[action.farmer[0] if action.farmer else "PASS"] += 1
            for order in action.hands:
                units[order[0] if order else "PASS"] += 1
            for order in action.market:
                if order:
                    market[order[0]] += 1
        max_animals = max((sum(count for _, count in state.animals) for state in self.states), default=0)
        return {
            "episode_id": self.episode_id,
            "seat": self.seat,
            "actions": len(self.actions),
            "snapshots": len(self.states),
            "max_hands": max((state.hands for state in self.states), default=0),
            "max_animals": max_animals,
            "max_pastures": max((state.pastures for state in self.states), default=0),
            "unit_counts": dict(sorted(units.items())),
            "market_counts": dict(sorted(market.items())),
        }

    def validate(self) -> TraceValidation:
        errors: list[str] = []
        if len(self.actions) != 719:
            errors.append(f"expected 719 actions, got {len(self.actions)}")
        expected_turns = {0, 24, 96, 192, 288, 384, 480, 576, 719}
        actual_turns = {state.turn for state in self.states}
        if actual_turns != expected_turns:
            errors.append(f"snapshot turns differ: {sorted(actual_turns)}")
        previous_replay_index = -1
        for state in self.states:
            if state.replay_index < previous_replay_index:
                errors.append(f"snapshot replay index regressed at turn {state.turn}")
            previous_replay_index = state.replay_index
            numeric = (state.money, state.wheat_reserve, state.wheat_shed)
            if not all(math.isfinite(value) for value in numeric):
                errors.append(f"non-finite resource state at turn {state.turn}")
            if min(state.hands, state.unlocked_quadrants, state.pastures, state.plants) < 0:
                errors.append(f"negative structural state at turn {state.turn}")
            if state.wheat_reserve < state.wheat_shed:
                errors.append(f"wheat reserve below shed wheat at turn {state.turn}")
        for turn, action in enumerate(self.actions):
            if not action.farmer:
                errors.append(f"empty farmer action at turn {turn}")
            if any(not order for order in action.hands + action.market):
                errors.append(f"empty action order at turn {turn}")
        profile = self.profile()
        return TraceValidation(
            episode_id=self.episode_id,
            seat=self.seat,
            action_count=len(self.actions),
            state_count=len(self.states),
            max_hands=profile["max_hands"],
            max_animals=profile["max_animals"],
            max_pastures=profile["max_pastures"],
            unit_counts=tuple(sorted(profile["unit_counts"].items())),
            errors=tuple(errors),
        )
