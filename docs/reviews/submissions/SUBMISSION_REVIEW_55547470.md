# Submission Review 55547470

## Submission

- Submission ref: **55547470**
- Submitted: **2026-08-16 08:12:26 UTC**
- Description: `V50 adaptive 8-cow/4-sheep replay policy; full local gate and three failure-family improvements`
- Initial status: **PENDING**; later **COMPLETE**
- Public score: **1028.4** after 4 Public episodes
- Remaining submissions after upload: **4**
- Source: `research/agents/v50_adaptive_replay_policy.py`
- Submitted artifact: `submission/main.py`
- SHA256: `3dbcc2a4e02fb9ba2ab2211f80354ab93d5f11b90768ca5da079d486a34519a0`
- Size: 35,360 bytes

## What changed from active 55504047

V50 replaces the v27 fixed route with one complete 8-COW / 4-SHEEP high-throughput route and a bounded execution layer:

- WEED-blocked productive action repair with actor resynchronization;
- one-turn premium-sale front-running only when town demand is absent, with repayment;
- opening feed ordering;
- existing SELL-slot ranking;
- terminal reachable-inventory banking and liquidation.

It does not add hands, switch routes mid-season, splice v27 actions, or use a capacity overlay.

## Pre-submit evidence

- starter, 8 seeds × both seats: **16W-0L-0T**, mean bank 149,937, minimum 79,798;
- Hamburger, 8 seeds × both seats: **16W-0L-0T**, mean bank 103,186, minimum 54,887;
- registered failure family 92971175: **4W-4L** vs v27 0W-8L;
- registered failure family 92967433: **5W-3L** vs v27 0W-8L;
- registered CARE/cashflow family 92978681: **8W-0L** vs v27 0W-8L;
- existing 9-tape league: **16W-2L**, mean margin +65,622, worst -26,078; v27 was 12W-6L;
- latest 934xxxx replay-derived opponents: 20 games **11W-9L**, mean margin +4,054, worst -21,682;
- py_compile and complete 720-turn runs passed.

Full candidate evidence: `docs/reviews/iterations/ITERATION_V50_ADAPTIVE_REPLAY_POLICY.md`.

## Public snapshot: 4 episodes

All four Public episodes were wins:

| Episode | Seat | Opponent | Result | Margin |
|---:|---:|---|:---:|---:|
| 93570324 | 1 | Dipak_ISM | W | +68,281 |
| 93571219 | 0 | Abish Pius | W | +55,976 |
| 93572099 | 0 | Lady and tech | W | +43,739 |
| 93572980 | 1 | Emanuel Lázaro | W | +38,403 |

- Record: **4W-0L-0T**
- Mean margin: **+51,600**
- Worst margin: **+38,403**
- Score: **1028.4**

The score is not yet comparable to V27's 45-episode score of 1733.1. At the same 4-episode checkpoint, V27 was approximately 1013.0, so V50 is currently slightly ahead by rating snapshot. Continue to the 5-episode review before making a replacement decision.

## Next action

1. Keep `55547470` active and collect the fifth Public episode.
2. Record rating/rank with the episode count.
3. Download and analyze all new replays.
4. Do not spend another submission or start a new experiment before the 5-episode review.

`55504047` remains the incumbent reference until V50 has enough Public evidence.
