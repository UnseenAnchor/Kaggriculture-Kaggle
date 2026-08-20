# ITERATION_V70: T104 (10-cow / 4-sheep) — REJECTED at live (rolled back to V50)

- Status: **REJECTED (live)**. Submitted 55634837 🡒 live-equilibrium 1633 < V50. Rolled back to V50 8/4 (55640613 = 1660-1675 on this draw).
- Outcome: local h2h 18W-0L did NOT transfer; 2nd confirmed case that local tape h2h does not predict live placement (V60 → 1232, v70 → 1633).
- **Lesson locked**: composition/RPS changes have negative expected value live. V50 8/4 artifact is the only live-proven performer.

## Baseline promotion (post-approval)
- User chose option 1 (submit v70).
- Backed up old baseline: `research/agents/archive/submission_V50_8cow4sheep.py.bak`, `research/agents/archive/agents_v27.py.bak`.
- Promoted `research/agents/v70_t104.py` → `submission/main.py` AND `agents/main.py` (SHA 19b1227... all three identical).
- Re-gated the promoted `submission/main.py` vs true live V50 baseline (`submission/main.py` prior): h2h 8W-0L standard seeds + 10W-0L fresh seeds = **18W-0L**. vs starter 8W-0L 150,637. vs V50 backup 8W-0L 95,801.
- Note: the earlier 17W-1L h2h claim was measured vs `agents/main.py` which was v27 (ref), not the live V50; re-measured authoritative h2h vs live V50 = 18W-0L, equally decisive.

## Hypothesis (mechanism)
The online field is cow-majority. The observed 18-game meta sample bins to
11×8/4 + 5×8/6 + 2×10/4, with ZERO sheep-heavy (6/8, 6/10, 5/9). V50 (8/4) is a
member of the cow8 family it must out-score against. The ratio RPS proven in
V66-V69 (8/4 > 6/8 > 10/4 > 8/4) implies a **cow-10 (10/4) profile beats both
8/4 and 8/6**, i.e. beats 16/18 of the observed live field. A 10/4 agent with the
V50 execution layer was **never built nor gated** — V56-62 only ever tested
6/8/8/6/6/12/sheep20.

Two independent facts it explains:
1. V50 loses to the 10/4 tapes (93928639/93978681) locally — because 10/4 out-cows it.
2. V50's failure tapes are all sheep-heavy (6/8, 6/10, 5/9) — the cow8 family is
   weak both to cow-10 AND sheep-heavy; cow-10 rebalances the cow-side weakness.

## Candidate
`research/agents/v70_t104.py` = V60/V50 execution layer (weed-repair, premium
front-run, rank-sell, terminal liquidation) + a **10-cow/4-sheep action table**
spliced from the 93928639 10/4 tape, normalized to the V50 schema (720 steps).
Verified to run 10 COW / 4 SHEEP with the full adaptive wrapper.

## Results

### Head-to-head vs V50 (the active mainline = the meta)
- Standard 4 seeds (27011/27031/27101/27121) × 2 seats: **7W-1L**
- 5 fresh seeds (32345/43456/54567/65678/76789) × 2 seats: **10W-0L**
- **Combined: 17W-1L vs V50** across 9 seeds. Not a fluke.

### Regression floors (must not collapse)
| Opponent | V50 ref | v70 | verdict |
|---|---|---|---|
| starter | 148,302 (8W-0L) | **150,637 (8W-0L)** | no regression |
| hamburger_anchor | 77,222 (8W-0L) | **98,568 (8W-0L)** | better |

### Known regression: sheep-heavy tapes (rare online)
| tape | tribe | V50 ref | v70 | verdict |
|---|---|---|---|---|
| 92971175 | 6/8 | 5W-3L 88,845 | 0W-8L 69,854 | v70 worse |
| 93604505 | 6/10 | 4W-4L 84,205 | 0W-8L 84,635 | v70 worse |
| 93730164 | 5/9 | 6W-2L 89,966 | 0W-8L 71,756 | v70 worse |

## Decision
The RPS cost is fully symmetric to the RPS gain: v70 dominates the cow8-majority
meta (17W-1L vs the current mainline + wins 8/6 + holds hamburger/starter) at the
price of losing the sheep-heavy families that are ~0/18 in the observed live
sample. Combined with the standing evidence that sheep-heavy loses online (V60's
live ~1241), v70 is the highest-EV mainline available.

**RESULT: ACCEPT as candidate.** Requires user approval to change the frozen
`agents/main.py` / `submission/main.py` baseline and to submit (AGENTS.md
"no new-version submission without a qualified candidate + user go-ahead").

## Commands
```
D:/ke/python.exe tools/run_match.py research/agents/v70_t104.py agents/main.py 27011,27031,27101,27121,32345,43456,54567,65678,76789
D:/ke/python.exe tools/run_match.py research/agents/v70_t104.py starter 27011,27031,27101,27121
D:/ke/python.exe tools/run_match.py research/agents/v70_t104.py research/agents/hamburger_anchor.py 27011,27031,27101,27121
```
