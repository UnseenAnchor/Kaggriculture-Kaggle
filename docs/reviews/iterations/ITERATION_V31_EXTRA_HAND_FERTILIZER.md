# V31 Extra-hand fertilizer support

## Hypothesis

The recurring online losses are capacity/production-pressure losses: stronger opponents use more workers and animals and sell much more Wheat/Fertilizer/Milk/Wool. The previous SELL controls attacked liquidation order, not the root capacity gap. V31 adds exactly one early farm hand and gives only that hand a state-aware patrol over public animal structures to collect available fertilizer. It does not copy an opponent tape, add CARE, or alter the v27 route's existing actors.

## Baseline and gates

- Baseline: `agents/main.py`, frozen at `agents/archive/v27_before_v30_demand_sell.py`.
- Development seeds: 27011, 27031, 27101, 27121; both seats.
- Unseen seeds: 37011, 37031, 37101, 37121; both seats.
- Required controls: official `starter`, `hamburger_anchor`, and failure tapes 92971175, 92978681, 92967433.
- Stop: any regression on starter/Hamburger, any catastrophic loss, or no improvement across at least two failure families.

## Results

- First implementation passed `starter` 16W-0L but failed `hamburger_anchor` 2W-14L. Cause: farm hands reset daily; fixed index 4 eventually replaced a normal v27 route hand.
- Identity-safe repair used the last hand hired on the last available HIRE step of each day and avoided occupied pasture tiles. It passed starter 16W-0L and Hamburger 16W-0L.
- Against failure tapes, identity-safe V31 scored 3W-5L vs `92971175`, 0W-8L vs `92978681`, and 3W-5L vs `92967433`. It did not improve any required family and was worse than the v27 baseline on the 92971175 gate.

## Decision

**Reject V31 and do not submit.** The added worker/fertilizer patrol does not solve the shared online failure mechanism; its remaining effect is either too small or interferes with the fixed production tape. Do not tune this branch further. Keep `agents/main.py` unchanged and retain 55504047 as the active submission.
