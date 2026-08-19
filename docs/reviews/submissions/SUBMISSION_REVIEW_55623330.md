# Submission Review 55623330 (V50 re-draw)

## Purpose
TOP700 goal: V50 artifact historically reached 2093.4 live > current TOP700 cutoff 2052.6, but the previous active (55600926, identical code) had drifted to 1857.9 (~rank 1010). Since every strength candidate (v66-v69) was rejected with local gates and the live rating is matchmaking-dominated (±200 on identical bytes), the evidence-backed path was a fresh matchmaking sample of the SAME best artifact.

## Submission
- ref: **55623330**
- file: `submission/main.py` (SHA 3dbcc2a4..., byte-identical to `research/agents/v50_adaptive_replay_policy.py`)
- message: V50 re-draw, TOP700-capable re-sample
- status on upload: PENDING → first Public score **600.0** (fresh-rating reset start, like V50's original 616)
- initial reset confirms: resubmitting resets the rating to ~600; it must climb with wins (V50 climbed 616→1992→2093 historically over 57-187 games).

## Watching
- Background watch: `research/v50_55623330_watch.log` (polls `kaggle competitions submissions` every 2 min).
- Success criterion: rating climbs toward/above **2052.6** (TOP700 line).

## Decision
- Submitted at user's explicit choice (Path A). This is NOT a "new candidate" — it is the same proven V50 artifact re-drawn for favorable matchmaking.
- Rejected candidates unchanged: v66 / v67 / v68 / v69 (see ITERATION_V66_V67_V68_AND_V60_RECONFIRM.md).
