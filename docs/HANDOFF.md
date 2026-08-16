# Session Handoff

Updated: 2026-08-16 16:20 UTC

## Goal

Make the active Kaggriculture submission reach TOP500 through public research, deterministic local gates, online replay postmortems, and Git-gated experiments. Do not spend another submission without a reviewed candidate that passes all registered gates.

## Repository and environment

- Working directory: `E:\AI-Coding\09-Kaggriculture`
- GitHub: https://github.com/UnseenAnchor/Kaggriculture-Kaggle
- Python: `D:/ke/python.exe`
- Kaggle CLI: `D:/ke/Scripts/kaggle.exe`
- Kaggle account: `unseenanch`; team: `道海孤舟`
- Active agent: `agents/main.py`
- Submitted artifact: `submission/main.py`
- Workflow: `docs/WORKFLOW.md`
- Review index: `docs/reviews/README.md`
- Long-term strategy: `docs/STRATEGY_LONG_TERM.md`

## Active submission

- Submission ID: **55504047**
- Description: `v27 public Top30 route - TOP500 push`
- Submitted: 2026-08-14 11:15:55 UTC
- Source artifact SHA256: `6fecd21fd0bf933f8c85c7288aa22f4de3a62447e771959063d3136b25b3c6ec`
- Public source/attribution: `kaitofukami/25-27-strict-future-v27-midgame-meta-reset`
- Exact extracted public source: `research/agents/kaito_v27_midgame_reset.py`
- Submission review: `docs/reviews/submissions/SUBMISSION_REVIEW_55504047.md`
- Remaining submissions reported after submit: 2

## Current challenger

- Submission ref: **55547470**
- Candidate: `research/agents/v50_adaptive_replay_policy.py`
- SHA256: `3dbcc2a4e02fb9ba2ab2211f80354ab93d5f11b90768ca5da079d486a34519a0`
- Evidence: `docs/reviews/iterations/ITERATION_V50_ADAPTIVE_REPLAY_POLICY.md`
- Status: **COMPLETE**, Public score **1028.4** after 4 episodes; record **4W-0L-0T**.
- First four margins: +68,281, +55,976, +43,739, +38,403.
- At the same 4-episode checkpoint V27 was approximately 1013.0; do not compare directly with V27's later 45-episode score 1733.1.

## Latest live snapshot

At 2026-08-14 14:04 UTC:

- Public episodes: **45**
- Rating: **1774.6**
- Rank: **996 / 4421** — TOP1000 reached
- TOP1000 threshold: 1771.0
- TOP500 threshold: **2435.3**

The last fully downloaded/reviewed checkpoint is 30 episodes:

- 27W-3L, 90% win rate
- Rating 1728.6, rank 1040/4410
- Mean margin +17,468; median +12,744; worst -29,636
- Losses: episodes 92967433, 92971175, 92978681

The latest sampled block of ten completed Public replays (`93405504` through `93458883`) was downloaded and reviewed: **0W-8L-2T**, mean margin **-8,058**. This sample is not a replacement for the earlier 45-episode rating snapshot. It contains high-supply, CARE, and a new 5-sheep/9-cow near-neighbor family; none currently yields an isolated mechanism.

## Submission trajectory

- v4 submission 55501712: heuristic baseline; latest dynamic score later fell near 616.
- v5-A submission 55501952: Yarn scaling; 1W-1L first review; dynamic score later fell near 562.
- v27 submission 55504047:
  - 4 episodes: 4W-0L, rating 1013, rank 1710
  - 10 episodes: 8W-2L, rating 1288.6, rank 1414
  - 30 episodes: 27W-3L, rating 1728.6, rank 1040
  - 45 episodes: rating 1774.6, rank 996; W/L pending replay review

## Pre-submit evidence for v27

- 6 real online opponent tapes × both seats: 12W-0L, worst +75,207
- 6 public control families: 24W-0L, worst +21,118
- 8 seeds × both seats vs Hamburger anchor: 16W-0L
- 8 seeds × both seats vs collision_front: 16W-0L
- Self mirror: 3W-3L-10T

Full audit: `docs/reviews/iterations/ITERATION_TOP500_V27_PUBLIC_ROUTE.md`.

## Failed online families and exact gates

### 8-sheep / 6-cow family

- Episodes: 92967433, 92971175
- Exact seeds: 2103638568, 847064548
- Active v27: 0W-4L on the two tapes, worst about -30k
- Public opponent tapes:
  - `research/agents/online/episode_92967433_opponent.py`
  - `research/agents/online/episode_92971175_opponent.py`

The 92971175 public route scored 17W-1L on the later 9-tape league and 24W-0L against public controls, but only 7W-9L head-to-head against active v27 across 8 seeds × both seats. It was rejected as a direct replacement.

A step-1 route relay was also rejected: 0W-16L, final bank 19. The routes diverge at step 0 and their worker/assets states are incompatible. See `ITERATION_V28_STRONG_ROUTE_RELAY.md`.

### v27-like CARE/cashflow family

- Episode: 92978681
- Exact seed: 453608024
- Active v27: 0W-2L, 73,569 vs 89,045
- Tape: `research/agents/online/episode_92978681_opponent.py`

Hand PASS→CARE and all-actor PASS→CARE both produced exactly the same 73,569 and remained 0W-2L. CARE-only causality was rejected. The opponent also uses HIRE×5, a WHEAT buy/sell cashflow opening, extra seeds, and a different state trajectory. Its full route was 14W-2L-2T and still lost twice to the 8-sheep/6-cow family. See `ITERATION_V29_CARE_REPAIR.md`.

## Important decisions

1. Keep submission 55504047 active; it has reached TOP1000 and is still collecting episodes.
2. Do not submit the 92971175 route, route relay, CARE overlays, or 92978681 route; all were explicitly rejected.
3. Do not modify the fixed v27 tape based on action-count correlation alone.
4. Any fourth submission must solve multiple independent failure families and preserve the existing online wins.
5. Rating/rank are dynamic; always record timestamp, episode count, W/L/T, margins, and replay evidence.
6. Long-term development is now champion/challenger plus typed continuation policies; do not create another local overlay without a new state cluster and a two-family causal chain.

## Exact next action

1. Wait for Public episode 5 for `55547470`.
2. Record rating/rank with the episode count.
3. Download and analyze any new replay; registry now contains 67 episodes.
4. Review after 5 Public episodes before any replacement decision.
5. Do not spend another submission or start a new experiment yet; keep `55504047` as incumbent reference.

Useful commands:

```bash
cd "E:/AI-Coding/09-Kaggriculture"
D:/ke/Scripts/kaggle.exe competitions submissions kaggriculture -v
D:/ke/Scripts/kaggle.exe competitions episodes 55504047 -v
D:/ke/Scripts/kaggle.exe competitions replay <EPISODE_ID> -p research/replays -q
D:/ke/python.exe tools/analyze_replay.py research/replays/episode-<EPISODE_ID>-replay.json
```

## Git state

Before adding this handoff, the working tree was clean. Most recent research commits:

- `2071a6e` experiment: reject idle CARE repair hypothesis
- `3a0e1b5` docs: review submission 55504047 after thirty episodes
- `e2ed359` experiment: reject incompatible strong-route relay
- `21cd0cb` docs: review submission 55504047 after ten public episodes
- `f707b46` docs: review submission 55504047 after four wins

## New-session bootstrap prompt

```text
切换到 E:\AI-Coding\09-Kaggriculture。先读取 AGENTS.md、docs/HANDOFF.md、docs/WORKFLOW.md 和 docs/reviews/iterations/ITERATION_V50_ADAPTIVE_REPLAY_POLICY.md。V50 已达到可提交状态但尚未上传；不要自动提交，不要修改 active 55504047，除非用户明确批准。
```
