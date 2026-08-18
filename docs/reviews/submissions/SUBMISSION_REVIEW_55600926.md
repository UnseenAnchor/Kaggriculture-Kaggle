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

## Post-submit plan
1. Confirm COMPLETE; record rating.
2. Download first Public episodes; verify V50's restored trajectory.
3. Re-open B-direction research (a stateful candidate that beats V50) only with causal evidence.