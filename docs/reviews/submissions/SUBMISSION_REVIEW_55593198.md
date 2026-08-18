# Submission Review 55593198

## Submission

- Submission ref: **55593198**
- Submitted: 2026-08-16 (after V50 reached 2093.4 with deteriorating win rate)
- Description: `V52 dominant 6-cow/12-sheep expansion branch (ep 93730164); beats V50 on tape league, 2 failure families, head-to-head 6W-2L`
- Initial status: PENDING; later **COMPLETE**
- Public score: **839.2** after 2 Public episodes (both wins: +55,943 vs Surya Vijjeswarapu, +23,624 vs ayushk_empire)
- Note: low absolute score is early rating calibration, not losses. Pool-wide drift in the same window: V50 2093.4 → 2002.2, 55504047 1732.9 → 1640.2.
- Source: `research/agents/online/episode_93730164_opponent.py`
- Submitted artifact: `submission/main.py`
- SHA256: `41d0398780dd41951e04ef923052c4ae66244ebfcb1c03cf6b9251f6f5e8a5c7`
- Size: 138,247 bytes
- Remaining submissions after upload: 4

## What changed from V50 (55547470)

V52 replaces V50's 8-COW/4-SHEEP route plus execution layer with the bare dominant branch of the public expansion strategy family (6 COW / 12 SHEEP), extracted from Public episode 93730164. Seven sampled opponent replays share a byte-identical opening, proving one shared public agent; its 6/12 branch is the dominant branch across seeds. This family accounts for 55 of V50's 96 Public losses.

## Pre-submit evidence

Full gate in `docs/reviews/iterations/ITERATION_V52_DOMINANT_EXPANSION_BRANCH.md`:

- starter/Hamburger: 16W-0L; 5 held-out controls: 40W-0L
- failure families vs V50: 92967433 8W-0L (V50 5W-3L), 92971175 7W-1L (V50 4W-4L), 92978681 6W-2L (V50 8W-0L; v27 baseline 0W-8L)
- head-to-head vs V50: 6W-2L, +8,440
- tape league (13 tapes × both seats): 18W-6L-2T, +45,954 vs V50 16W-10L, +38,587

## Rollback

If V52 underperforms online, resubmit the V50 artifact at `research/agents/v50_adaptive_replay_policy.py` (SHA256 `3dbcc2a4...4519a0`).

## Post-submit plan

1. Wait for COMPLETE; record rating with episode count.
2. Download first Public replays immediately.
3. Compare against V50's trajectory at equal episode counts.
4. Update registry and review after 5 Public episodes.
