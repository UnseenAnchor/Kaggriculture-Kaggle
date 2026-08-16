# V46 replay registry and typed continuation trace

## Scope

Infrastructure phase only. No candidate, no active-agent change, and no Kaggle submission.

## Implementation

- `tools/build_replay_registry.py` scans local replay JSON and writes compact CSVs.
- `research/registry/replay_registry.csv`: 126 seat rows from 63 episodes.
- `research/registry/replay_state_snapshots.csv`: 1,134 snapshots at turns 0/24/96/192/288/384/480/576/719.
- `research/continuation/` provides immutable `ContinuationState`, `ActionIntent`, and read-only `ContinuationSimulator` records.
- `tools/validate_continuation.py` validates complete action count, snapshot coverage, finite resources, structural non-negativity, and non-empty action orders.

## Validation

Both seats of episode `92971175` validate successfully:

- v27 active seat 1: `719` actions, max sampled hands `10`, max animals `13`, max pastures `13`.
- high-supply seat 0: `719` actions, max sampled hands `8`, max animals `14`, max pastures `14`.

The trace layer deliberately does not generate actions and does not splice routes. It is the prerequisite for the next phase: a typed planner that can emit a legal, state-compatible continuation.

## Decision

Keep `55504047` and `agents/main.py` unchanged. Do not create V46 agent code or submit. Continue with planner design only after the trace invariants remain stable.
