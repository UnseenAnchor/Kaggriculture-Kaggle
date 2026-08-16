# Submission Review 55547470

## Submission

- Submission ref: **55547470**
- Submitted: **2026-08-16 08:12:26 UTC**
- Description: `V50 adaptive 8-cow/4-sheep replay policy; full local gate and three failure-family improvements`
- Initial status: **PENDING**
- Public score: pending
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

## Post-submit plan

1. Wait for `COMPLETE`; do not infer strength from PENDING.
2. Record rating/rank with timestamp and episode count.
3. Review the first Public replay immediately.
4. Review after 5 Public episodes before any decision.
5. Download all new replays and update the registry.

Keep `55504047` as the incumbent reference until 55547470 has enough Public evidence.
