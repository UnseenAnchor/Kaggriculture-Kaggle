# Iteration V53 — rollback to V50 stateful execution layer

## Context / discovery

V52 (`55593198`, the bare 6-COW/12-SHEEP dominant-branch tape) was submitted and reached rating 1996.8, but never overtook V50's 2001.7 and its score was unstable (swung 839 → 1290.8 → 1996.8). Live record after scaling: roughly 15W-12L, losing big to a pool of opponents that all buy **8 COW / 6 SHEEP (14 total animals)** — the current online meta mainstream.

## Root-cause analysis

The real online meta is NOT the 6/12 branch we reproduced. V52's losses were nearly all against `COW8/SHEEP6` opponents. When we extracted two of those opponents as tapes and ran them locally:

- V52 (bare 6/12 tape) vs 8/6 tapes: **~11W-9L** (50-50, seed-dependent)
- V50 (8/4 stateful execution layer) vs same 8/6 tapes: **20W-0L** (all seeds, ~12k-25k margins)

The distinction is stateful vs tape. The online 8/6 opponents are stateful agents; reproducing the same branch as a fixed tape is structurally weaker. V50's existing 8/4 execution layer (weed repair, seed/schedule adaptation) dominates the 8/6 tapes locally and held the higher stable rating online.

### Also checked and rejected (no dedicated doc, logged here)
- 94155162 bare 8/6 tape: failed local gate (head-to-head vs V50 0W-2L, fail families 2W-2L)
- 94155162 + V50 execution layer (V53 candidate): **total collapse** (Hamburger 16-0L, mean bank 26k) — execution layer non-portable to non-8/4 tape confirmed universally.

## Decision

**Roll back to V50.** Resubmitted the V50 artifact (`research/agents/v50_adaptive_replay_policy.py`, SHA256 `3dbcc2a4...519a0`) as submission **`55600926`**. V52's unstable rating (currently 1290.8) and losses to stateful 8/6 opponents do not justify keeping the tape as active.

## Action/resource conservation
- V50 is the strongest artifact known (best gate results, highest stable rating, beats 8/6 meta locally).
- No new marker-level candidate created; V53 = restore, not novelty. Kept to "today's submissions" budget (2-3 remaining).
- Rollback path preserved: V52 backup at `submission/main_v52_backup.py`.