# Replay registry

Generated from local `research/replays/` by:

```bash
D:/ke/python.exe tools/build_replay_registry.py
```

Files:

- `replay_registry.csv`: one row per episode/seat with outcome, margin, action hashes, first divergence, action counts, market totals, and final assets.
- `replay_state_snapshots.csv`: one row per episode/seat at turns 0, 24, 96, 192, 288, 384, 480, 576, and 719.

The raw replay JSON files are not committed. Registry rows are derived artifacts and can be regenerated after downloading new episodes. The `first_diff_*` fields compare each observable seat action stream with the v27 legacy action tape; they are descriptive evidence, not a claim that every replay opponent is a direct v27 variant.
