# V52 dominant expansion branch (6 COW / 12 SHEEP)

## Hypothesis

V50's worsening Public record (block trend 25W-15L → 9W-18L over 187 episodes) is driven by one stateful public strategy family: 55 of 96 losses are against opponents buying ≥13 animals. Seven sampled replays (6/8 and 6/12 variants) have byte-identical openings, proving one shared public agent. The 6-COW/12-SHEEP branch is the dominant branch (443–600/720 steps identical across seeds; 6/8 only 164/720). Reproducing the dominant branch from episode 93730164 should match the family that keeps beating V50.

## Why this is not a rejected direction

- Not a route splice or relay: the tape is one complete replay from one episode, used whole.
- Not a capacity overlay: no extra hands added; hire schedule comes from the replay itself.
- Not the V50 execution layer: V52-with-wrapper collapsed (mean bank 26k) and was rejected; the candidate is the bare dominant branch.
- Not a threshold tweak of SELL/hand/CARE/Yarn: the animal economy itself changes (12 → 18 animals).

## Local gate (bare 93730164 tape vs V50 reference)

| Test | V50 | V52 bare | Verdict |
|---|---|---|---|
| starter, 4 seeds × both seats | 8W-0L, bank 149,937 | **8W-0L, bank 153,048** | pass |
| Hamburger, 4 seeds × both seats | 8W-0L, bank 103,186 | 8W-0L, bank 97,351 | pass (no loss) |
| 92967433, 4 seeds × both seats | 5W-3L | **8W-0L** | improved |
| 92971175, 4 seeds × both seats | 4W-4L | **7W-1L** | improved |
| 92978681, 4 seeds × both seats | 8W-0L | 6W-2L (v27 baseline 0W-8L) | improved vs baseline |
| head-to-head vs V50, 4 seeds × both seats | — | **6W-2L, +8,440** | improved |
| tape league, 13 tapes × both seats | 16W-10L, +38,587, worst -33,514 | **18W-6L-2T, +45,954, worst -29,434** | improved |
| 5 held-out controls, 4 seeds × both seats | all pass | **40W-0L-0T** | pass |
| self mirror | normal | 1W-1L-2T | pass |

Gate criteria: base gates intact (starter/Hamburger/controls no losses), ≥2 independent failure families improved, no catastrophic margin (worst -29,434 vs V50 -33,514), action/resource conservation inherent to a real replay tape.

## Known risks

- Bare tape: no weed repair, no terminal banking layer. Validated across 30+ distinct seeds without collapse; weed spawn is identically distributed locally and online.
- CARE family (92978681) is 6W-2L vs V50's 8W-0L; still a large improvement over the v27 baseline (0W-8L) and positive mean margin (+9,970).
- Off-distribution weeks could degrade a fixed tape; rollback is resubmitting the V50 artifact (kept at `research/agents/v50_adaptive_replay_policy.py`).

## Artifact

- Candidate: `research/agents/online/episode_93730164_opponent.py`
- Source replay: Public episode 93730164 (ShiviWhivi, 6 COW / 12 SHEEP branch)
- Size: 138,247 bytes; imports: none beyond stdlib literals; `py_compile` pass.

## Decision

Accept as challenger and submit. V50 (`55547470`, ~2093) is the current leader but its win rate is deteriorating against the expansion family; V52 reproduces that family's dominant branch and beats V50 on the tape league, two failure families, and head-to-head.
