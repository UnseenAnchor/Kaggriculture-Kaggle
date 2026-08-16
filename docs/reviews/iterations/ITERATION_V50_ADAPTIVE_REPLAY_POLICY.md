# V50 adaptive replay policy

## Hypothesis

Use one complete 8-COW / 4-SHEEP high-throughput route from step 0, with a bounded execution layer that only:

- repairs a productive action blocked by a WEED and resynchronizes its actor;
- moves an already-planned premium sale forward by one turn only when no town demand occurs, then repays the quantity;
- protects opening feed ordering;
- ranks existing SELL slots and banks/liquidates reachable inventory only at the terminal window.

It does not add hands, switch routes mid-season, splice v27 actions, or use a fifth-hand/capacity overlay.

## Local gate

| Opponent | Result | Mean bank | Minimum bank |
|---|---:|---:|---:|
| starter, 8 seeds × both seats | **16W-0L-0T** | 149,937 | 79,798 |
| Hamburger anchor, 8 seeds × both seats | **16W-0L-0T** | 103,186 | 54,887 |
| Frontier v12, 4 seeds × both seats | **8W-0L-0T** | 85,912 | 69,307 |
| Kaito v21, 4 seeds × both seats | **8W-0L-0T** | 108,430 | 82,591 |
| Replay Shield v15, 4 seeds × both seats | **8W-0L-0T** | 87,903 | 69,278 |
| Scenario v14, 4 seeds × both seats | **7W-1L-0T** | 87,909 | 56,173 |
| Soil v25, 4 seeds × both seats | **8W-0L-0T** | 85,890 | 55,155 |
| self mirror, 4 seeds × both seats | **1W-1L-6T** | no disaster | — |

## Failure-family gate

Four fixed seeds × both seats:

| Family | V27 baseline | V50 | Mean V50 bank |
|---|---:|---:|---:|
| 92971175 high supply | 0W-8L | **4W-4L** | 82,755 |
| 92967433 supply/market | 0W-8L | **5W-3L** | 74,853 |
| 92978681 CARE/cashflow | 0W-8L | **8W-0L** | 88,328 |

All three registered failure families improve; no extra hand or capacity patch is involved.

## Existing public tape league

Using the same 9 downloaded online opponent tapes and seeds:

- V27: `12W-6L-0T`, mean margin `+61,334`, worst `-30,245`, mean bank `102,961`.
- V50: **`16W-2L-0T`**, mean margin **`+65,622`**, worst **`-26,078`**, mean bank **`113,589`**.
- 92967433 changes from `LL` to `WW`.
- 92978681 changes from `LL` to `WW`.
- 92971175 remains `LL` and is the remaining hard family.

Evidence: `research/v50_tape_league_results.csv`.

## Latest Public replay check

Against replay-derived opponent actions for episodes `93405504` through `93458883`, V50 completed 20 games at **11W-9L**, mean margin **+4,054**, worst **-21,682**. On the corresponding active-seat orientation it was **5W-5L**, improving on the active submission's latest sampled `0W-8L-2T` block without a new execution failure.

Evidence: `research/v50_latest_934_results.csv`.

## Artifact checks

- Candidate: `research/agents/v50_adaptive_replay_policy.py`
- SHA256: `3dbcc2a4e02fb9ba2ab2211f80354ab93d5f11b90768ca5da079d486a34519a0`
- Size: 35,360 bytes
- Imports: Python standard library only
- `py_compile`: pass
- 720-turn local runs: complete
- `agents/main.py`: unchanged
- `submission/main.py`: unchanged
- Active submission `55504047`: unchanged

## Decision

V50 passed the registered local gates, improves all three failure families, and beats V27 on the existing public tape league. It was uploaded as submission **55547470** on 2026-08-16 08:12:26 UTC. The first four Public episodes are **4W-0L-0T**, with mean margin **+51,600** and score **1028.4**. At the same four-episode checkpoint, V27 was approximately 1013.0; the later V27 score 1733.1 is not yet comparable. Keep `55504047` as the incumbent reference until the fifth-episode review.
