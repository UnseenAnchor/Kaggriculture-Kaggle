"""Validate and summarize a complete typed continuation trace."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research.continuation import ContinuationSimulator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("replay", type=Path)
    parser.add_argument("--seat", type=int, default=0)
    parser.add_argument(
        "--snapshots",
        type=Path,
        default=Path("research/registry/replay_state_snapshots.csv"),
    )
    args = parser.parse_args()
    trace = ContinuationSimulator.from_files(args.replay, args.snapshots, args.seat)
    validation = trace.validate()
    result = {"profile": trace.profile(), "validation": {**validation.__dict__, "ok": validation.ok}}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if validation.ok else 1)


if __name__ == "__main__":
    main()
