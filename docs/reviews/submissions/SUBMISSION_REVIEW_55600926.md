# Submission Review 55600926

## Submission
- Submission ref: **55600926**
- Purpose: **Rollback to V50 stateful execution layer** (replaces V52 bare 6/12 tape)
- Description: `V53 restore: V50 adaptive 8-cow/4-sheep stateful execution layer; beats 8-cow/6-sheep meta tapes 20W-0L (V52 tape only ~11W-9L); rollback from V52`
- Artifact: `research/agents/v50_adaptive_replay_policy.py`
- SHA256: `3dbcc2a4e02fb9ba2ab2211f80354ab93d5f11b90768ca5da079d486a34519a0`
- Submitted file: `submission/main.py` (identical bytes to the V50 artifact)
- Status: PENDING

## Why rollback
- V52 (55593198) never exceeded V50's stable rating and is unstable (839 → 1290.8 → 1996.8).
- Live V52 record ~15W-12L with large losses to stateful COW8/SHEEP6 meta opponents.
- Local head-to-head: V50 vs 8/6 tapes **20W-0L**; V52 vs same tapes **~11W-9L**.
- V50 is the strongest known artifact (8/4 stateful execution layer).

## Rollback path
- To restore V52 (not recommended): `submission/main_v52_backup.py`.
- Active 55600926 review after COMPLETE and first Public episodes.

## Convergence (final)

- Watched until convergence (3 consecutive checks |dScore|<=20): **final score 1969.0** after 32 Public episodes.
- Overall: **24W-8L (75%)**. Leaderboard snapshot: **1926.8, rank 908/5165** (TOP500 cutoff 2239.8).
- Opponent mix: cow8-based 18 games (11 cow8/4, 5 cow8/6, 2 cow10/4) — vs cow8-family **11W-5L**.
- The 8 losses are all small/medium margins (-318..-7820) vs cow8/4, cow10/4, cow6/12, cow6/8 — no blowouts.
- Conclusion: V53 (=V50 stateful 8/4) reached equilibrium at its historical level (~1992). It IS the active submission; no resubmission needed (resubmitting resets rating).
- Remaining gap to TOP500: ~310 points. No candidate proven stronger; do not submit again.
