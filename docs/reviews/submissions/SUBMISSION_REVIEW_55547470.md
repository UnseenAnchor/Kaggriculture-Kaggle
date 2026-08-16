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

## Public snapshot: 18 episodes

The first 4 Public episodes were all wins. The next 14 were **12W-2L**, giving V50 an overall **16W-2L-0T** record.

| Block | Record | Mean margin | Worst margin |
|---|:---:|---:|---:|
| Episodes 1–4 | 4W-0L-0T | +51,600 | +38,403 |
| Episodes 5–18 | 12W-2L-0T | +9,626 | -28,578 |
| All 18 | **16W-2L-0T** | **+18,717** | **-28,578** |

The two new losses were:

- `93578320` vs Farmer John: `-28,578`. The opponent ran a 17-SHEEP / high-Yarn route; V50's 4-SHEEP route was overtaken from day 14 onward. This is a route-family mismatch.
- `93585555` vs dupakdungking: `-4,730`. Both sides used nearly the same 8-COW / 4-SHEEP route and ended with the same assets; the small gap appeared from day 7, indicating market/seat timing rather than a broad route failure.

These are different mechanisms. Do not create a local parameter patch or V51 overlay from only these two losses.

Current ratings:

- V50 `55547470`: **2069.5** after 57 Public episodes
- incumbent `55504047`: **1732.9**
- V50 lead: **+336.6**

The downloaded 57 Public replays are **37W-20L-0T**, mean margin **+6,474**, worst **-28,578**. The newest 39-episode block is 21W-18L with mean margin +824, yet the rating still rose from 1993.5 to 2069.5; this confirms the score is opponent-rating-sensitive, not a raw win-rate display.

The newest losses are mostly small same-route market/seat timing gaps. The two clear expansion losses are `93587364` (opponent 6 COW / 8 SHEEP, margin -14,374) and `93604505` (opponent 6 COW / 8 SHEEP, margin -12,781). Do not turn these into a local parameter patch until the family has a causal mechanism across multiple independent controls.

V50 now has enough online evidence to clear the initial sample-size concern. Keep collecting replays, but do not spend another submission or start a new experiment yet.

## Next action

1. Keep `55547470` as the leading challenger and collect the next Public block.
2. Download and analyze new replays, especially the two loss families.
3. Compare V50 and 55504047 on the same episode count when available.
4. Preserve `55504047` as a rollback reference.
