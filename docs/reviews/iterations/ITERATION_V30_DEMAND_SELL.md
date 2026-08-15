# V30 Demand-aware SELL ordering

## Hypothesis

在不改变 v27 固定生产路线、HIRE、动物数量、CARE 和 movement 的前提下，增强已有 `_rank_sell_slots` 对 Town 当前需求的权重，可能减少 92994559 一类同构近邻中的现金流损失，并改善高 Wheat/Fertilizer 压力局。该实验不是 v28 relay，也不是 v29 CARE。

## Baseline

- Candidate: `agents/main.py`，冻结副本：`agents/archive/v27_before_v30_demand_sell.py`。
- Online evidence before experiment: submission 55504047, 46 Public episodes; first 45 reviewed as 37W-8L-0T, episode 93001112 is W +32,980.
- Fixed route and all actor actions remain unchanged; only ordering score is under test.

## Local gates

- Development seeds: 27011, 27031, 27101, 27121; both seats.
- Unseen seeds: 37011, 37031, 37101, 37121; both seats.
- Compare against official `starter` and the public `hamburger_anchor`.
- Required before any submission consideration: no loss of baseline on the 16 starter games; no regression against the public control gate; then run the full registered tape/control gates.
- Stop condition: any starter loss, any catastrophic margin below -10,000, or no improvement against the failure-family controls.

## Rejected paths not revisited

- v28 strong-route relay remains rejected (0W-16L).
- v29 CARE overlays remain rejected (0W-2L with unchanged score).

## Results

- Baseline: 16W-0L vs `starter` and 16W-0L vs `hamburger_anchor` on 8 seeds × 2 seats.
- SELL alpha-only variants `0.50`, `1.00`, `2.00`: each 5W-3L vs `episode_92971175_opponent.py`; no improvement over baseline.
- Public-pressure liquidation including Wheat/Fertilizer/Milk/Wool: 0W-8L vs `episode_92971175_opponent.py`; rejected. Root cause: selling Wheat from shed at step 240 removed future feed stock and collapsed the route.
- Milk/Wool-only liquidation: 5W-3L vs `92971175`, 0W-8L vs `92978681`, and 3W-5L vs `92967433`; no cross-family improvement, rejected.

## Decision

**Do not promote V30 and do not submit it.** The fixed v27 route remains the active candidate. V28 relay and V29 CARE are not revisited. The next candidate must change a mechanism that addresses multiple failure families while preserving the 16W-0L starter and 16W-0L Hamburger gates.
