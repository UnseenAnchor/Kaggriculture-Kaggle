# SUBMISSION_REVIEW_55634837 — T104 (10-cow/4-sheep) baseline swap

- Submission: 55634837 (main.py at SHA 19b1227 = v70_t104)
- Submitted: 2026-08-20 (user-approved option 1)
- Code: research/agents/v70_t104.py (10cow/4sheep action table + V50 exec layer)

## Local evidence (pre-submission, complete gate)
- h2h vs live V50 baseline (`submission/main.py` prior): 8W-0L (std seeds) + 10W-0L (5 fresh seeds) = **18W-0L**
- vs starter: 8W-0L, mean 150,637 (V50 ref 148,302)
- vs hamburger_anchor: 8W-0L, mean 98,568 (V50 ref 77,222)
- Known regression: sheep-heavy tapes (6/8, 6/10, 5/9) 0W-8L each — rare online (~0/18 observed)

## Decision
- Live re-rating shows v70 plateau at **~1633** (flat 1.5-2h), while V50 redraw at the SAME elapsed time was **1840-1864** (t=9600-13200s) and settled 1770-1781. V53/V50 currently 1857.9.
- **Local h2h (18W-0L vs V50) did NOT transfer to live.** Same failure mode as V60 (local 10W-2L → live 1232).
- **VERDICT: NEGATIVE — v70 underperforms V50 live by ~150-200 pts.** Recommend rollback to V50 baseline and re-submit.

## Final decision
**REJECTED at live.** Submitted 55634837; equilibrium ~1633 < V50 refs (1660-1858). Rolled back to V50 (55640613). Baseline is V50 8/4 again.

## Live score progression (Public rating)
| poll | score |
|---|---|
| initial | 600.0 |
| +5 min | 715.2 |
| +15 min | 940.5 |
| +20 min | 1198.8 |
| ~+30 min | 1099.4 |
| ~+40 min | 1223.6 |
| +60 min | 1366.0 |
| +70 min | 1393.0 |
| +80 min | 1446.1 |
| +90 min | 1474.4 |
| +100 min | 1497.6 |
| +110 min | 1519.7 → 1517.0 |
| +120 min | 1555.9 → 1535.1 |
| ~+2.5h | 1565.4 → 1587.3 → 1616.6 → 1628.3 → 1633.3 |
| ~+3h→+5h | **1633.0 flat (plateau)** |
| V50 redraw ref same time | 1840-1864 (t=3h) |
| V50 redraw final | 1770-1781 (t=16h) |

## Decision
**ROLLBACK RECOMMENDED**: restore V50 (archive `submission_V50_8cow4sheep.py.bak`) as active and re-submit. Local h2h remains non-predictive of live placement (2nd occurrence: V60 + v70).