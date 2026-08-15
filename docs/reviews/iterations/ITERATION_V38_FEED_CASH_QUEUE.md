# V38 feed-cash queue scheduler

## Mechanism hypothesis

The fixed v27 route can issue `BUY_PRODUCT WHEAT` after optional seed/animal/hire orders. In the 92978681 replay family, this reaches a cash-debt window: feed buys at steps 178, 182, 183, 195, 197, and 199 fail after earlier purchases consume the working capital. V38 estimates the current market queue cost and, only when projected cash cannot cover feed plus a 50-coin reserve, keeps SELL positions fixed and moves WHEAT purchases ahead of non-SELL optional buys.

## Validation

- `py_compile`: passed.
- `92978681`, 4 seeds × both seats: `0W-8L-0T`, mean reward `80,339` (v27: `0W-8L`, mean `82,534`).
- `92971175`, 4 seeds × both seats: `5W-3L-0T`, mean reward `88,844`.
- `92967433`, 4 seeds × both seats: `3W-5L-0T`, mean reward `94,816`.

The target family remains a clean loss and the other two families do not improve. V38 is rejected without base-gate expansion; `agents/main.py` and submission 55504047 remain active.

## Dependency audit conclusion

A follow-up before/after audit of steps 168–200 shows why queue order is insufficient. In `92978681`, step 193 begins with about 147 coins while the route requests WHEAT seed 5, STRAWBERRY seed 2, and WHEAT product 2. The route needs the strawberry seed for the next planting steps (206 and 209), so deferring that order would break the fixed field dependency; prioritizing it would instead lose feed. The later failed feed buys are therefore a structural cash/supply deficit, not a resolvable order-slot defect. No additional scheduler is justified without reopening the already rejected production, hand, animal, or cash-liquidation mechanisms.
