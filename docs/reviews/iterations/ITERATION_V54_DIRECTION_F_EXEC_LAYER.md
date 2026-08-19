# Iteration V54 — Direction F: can the execution layer carry a 14-animal mainline?

## Question
V50 (8-COW/4-SHEEP = 12 animals) has confirmed capacity shortfall vs the ≥13-animal meta. The only surviving path was whether a strong 14/13-animal tape mainline could inherit V50's execution-layer advantages (weed repair, sell ranking, terminal liquidation). V52/53 docs claimed this "collapses" (bank ~26k); we re-tested with a corrected loader (the old 3k reading was a relative-path bug) and quantified the real structure.

## Evidence (starter, seeds 27011+27031)

| Candidate | starter mean bank | vs V50 |
|---|---:|---:|
| V50 8/4 execution layer | **153,648** | — |
| bare 6/12 tape (ep 93730164) | ~153,000 | — |
| **6/12 tape + full V50 exec layer** | **25,258** (−84%) | catastrophe |
| **8/6 tape (94155162) + full V50 exec layer** | **54,712** (−64%) | weak |

## Root cause
All five V50 execution wrappers (`_weed_repair_action`, `_opening_feed_first`, `_premium_front_run`, `_rank_sell_slots`, `_terminal_bank`/`_terminal_liquidation`) encode 8/4 mainline rhythm assumptions. Applied to a 6/12 tape they *cancel* the tape's productive actions → bank collapses 153k→25k. This is structural, not a fixable bug (verified with fully-embedded mainline, no path dependency).

## Is the exec layer non-portable? YES — structural.
The wrapper and the mainline are one coupled unit. You cannot bolt the V50 wrapper onto a different-animal tape.

## Next probe
Peel the 5 wrappers individually to find which one(s) destroy the 6/12 tape. If a driver is animal-agnostic (weed repair), a *minimal* adapt layer could reinforce a strong 14-animal tape without the full 8/4-coupled wrapper. If all 5 destroy production, Direction F is closed and V53 (V50) is the final artifact.

## UPDATE — step-alignment bug found; full re-gate

### The "non-portability" was a step-offset bug
The old 26k "collapse" reading came from a step-alignment bug: `extract_trace_agent` aligns `obs.step+1`, but my embedded mainline used `obs.step`. Fixing `+1` restored real production:

| candidate (starter, 27011+27031) | mean bank |
|---|---:|
| 6/12 + exec layer (step-fixed) | **174,919** |
| 6/12 bare (step-fixed) | **175,070** |
| 8/6 + exec layer (step-fixed) | **153,492** |
| V50 8/4 exec layer | **153,648** |

Execution layer adds ~nothing to 6/12 (175,070 → 174,919); the jump came from step fix alone.

### Head-to-head vs V50 (the decisive test)
| candidate | vs V50 |
|---|---:|
| 6/12 + weed exec (V55) | **2W-2L** |
| 6/12 bare (V52-true) | **2W-2L** |
| 8/6 + exec (V54) | **0W-4L** |
| V50 self | 50/50 |

### Final conclusion
No 14-animal tape — bare or with the V50 exec layer — beats V50 head-to-head locally (best is a coin-flip 2W-2L, reproducing the V52 outcome). Online 8/6 dominates, but its local tape is weak (0W-4L), proving the online lead is stateful behavior that no tape reproduces. **Direction F is closed.** V53 (V50) remains the strongest artifact; no candidate clears the gate. Keep V53 active; do not submit.

### Files
- `research/agents/v54_8cow6_exec.py` (8/6 mainline + V50 exec, step-fixed) — WEAK vs V50
- `research/agents/v55_6cow12_exec.py` / `v55_weed.py` / `v55_bare.py` (6/12 family + variants) — TIE vs V50
- `research/agents/online/episode_94155162_trace.py` (8/6 trace)
