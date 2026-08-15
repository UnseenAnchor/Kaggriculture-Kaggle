# V40 replay analysis: 92994559 near-neighbor

## Evidence

Downloaded locally with:

```bash
D:/ke/Scripts/kaggle.exe competitions replay 92994559 -p research/replays -q
D:/ke/python.exe tools/analyze_replay.py research/replays/episode-92994559-replay.json
```

The opponent is structurally near-identical to v27:

- v27: 4 sheep / 9 cow, 42.8% movement, 995 PASS, 57 DROP.
- opponent: 4 sheep / 9 cow, 43.1% movement, 962 PASS, 69 DROP.
- Farmer/hand production counts are otherwise effectively identical.
- Opponent sells 464 WHEAT versus v27's 455; FERTILIZER, WOOL, MILK, MELON and STRAWBERRY totals are the same.
- Opponent buys 221 WHEAT product units versus v27's 212 and 22 MELON seeds versus 19.

Comparing the opponent seat-1 replay action stream with `_LEGACY_ACTIONS` gives 87 differing turns. The important differences are market timing and queue placement: the opponent buys 14 WHEAT at step 0 and sells 9 WHEAT at step 1, sells MILK/FERTILIZER earlier around steps 215–216, adds fertilizer sales before later purchases, and changes late SELL ordering. The production route itself is not the cause.

## Decision

The approximately 17.7k reward gap is evidence for market cash/price timing, not a new non-market route mechanism. SELL/market timing is already explicitly closed by the project constraints and V30 results; recreating this replay as another SELL overlay would violate the experiment rules and is not justified. No V40 candidate is created. Keep `agents/main.py` and submission 55504047 unchanged.
