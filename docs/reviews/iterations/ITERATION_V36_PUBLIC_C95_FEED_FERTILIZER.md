# V36 public C95 feed-first / fertilizer timing

## External evidence

Kaggle notebook `raykkretzschmar/kaggriculture-findings-from-zero-to-top-meta` documents C94/C95 as a market-only response to public losses. Its exact C95 artifact keeps the same field route and adds: (1) move the existing five-unit wheat purchase to market slot 0; (2) move at most five units of an already scheduled next-turn fertilizer sale one turn earlier and subtract the same quantity from the later sale. The notebook reports C95 112-8 against refreshed top-20 medoids and C94 88-14 in an 18-agent tournament; those are external evidence, not acceptance of this local candidate.

The downloaded C95 `_TRACE` matches the current v27 action tape at all 720 turns for farmer and hand actions. This is therefore a market-layer transplant, not the rejected v28 route relay.

## Hypothesis

Early shared-market wheat purchases can deny the fixed route enough feed for one sheep; first-slot feed protection removes that race. Later, one-turn fertilizer preemption can prevent a price/order loss without increasing total liquidation or changing production.

## Gates

- 8 development/unseen seeds × both seats against starter and Hamburger.
- Four fixed seeds × both seats against 92971175, 92978681, and 92967433.
- Required: no base-gate loss, improvement in at least two independent failure families, and no catastrophic margin.
- If passed: full registered tape/control regression and untouched final block before any submission consideration.

## Local validation

The completed transplant also applies the C94/C95 slot-0 five-unit wheat purchase, while preserving the v27 field/hand tape and limiting fertilizer preemption to five units.

- `py_compile`: passed.
- Starter, 8 seeds × both seats: `16W-0L-0T`, mean reward `152,062`.
- Hamburger, 8 seeds × both seats: `16W-0L-0T`, mean reward `93,992`.
- `92971175`, 4 seeds × both seats: `5W-3L-0T`, mean reward `88,849`.
- `92978681`, 4 seeds × both seats: `0W-8L-0T`, mean reward `80,050`.
- `92967433`, 4 seeds × both seats: `3W-5L-0T`, mean reward `94,816`.

The failure-family records are unchanged from v27. The candidate is rejected: it passes the base gates but improves none of the required independent online failure families. `agents/main.py` remains untouched and no submission is made.
