# V51 expansion-route replacement attempts

## Hypothesis

V50's repeated Public losses came from animal-expansion routes (6 COW / 8 SHEEP in episodes 93587364 and 93604505, 17 SHEEP in 93578320). Extract those winning routes and test whether one complete expansion route — with or without V50's execution layer — can replace the V50 8-COW / 4-SHEEP route.

## Candidates tested

1. Bare tape `episode_93604505_opponent` (Zhizhou Sha, 6 COW / 8 SHEEP).
2. Bare tape `episode_93587364_opponent` (Aleks Lviv, 6 COW / 8 SHEEP).
3. Bare tape `episode_93578320_opponent` (Farmer John, 17 SHEEP).
4. `v51_expansion_route.py`: 93604505 tape + V50 execution layer (weed repair, premium-sale front-run, sell-slot ranking, terminal liquidation).

## Demand-driven route selection is informationally infeasible

Both 6/8 routes and the V50 route fork at step 1 (day 0) animal purchases — before any town shop is observable (first shop unlocks day 3). A shop-driven opening route selector cannot exist; the deciding information arrives after the fork.

## Results

Starter smoke (2 seeds × both seats): all three bare routes 4W-0L; 93604505 mean bank 178,894, 93587364 mean 157,964, 93578320 mean 137,082.

Full gates (starter/Hamburger 4 seeds × both seats; failure families at native replay seed, both seats):

| Candidate | starter | Hamburger | 92967433 | 92971175 | 92978681 | vs V50 |
|---|---|---|---|---|---|---|
| 93604505 bare | 8W-0L (167,789) | 8W-0L (89,022) | 0W-2L | 0W-2L | 2W-0L | 4W-4L |
| 93587364 bare | 8W-0L (158,236) | 6W-2L | 0W-2L | 0W-2L | 0W-2L | 1W-7L |
| 93578320 bare | — | 0W-4L | 0W-4L | 0W-4L | 0W-4L | — |
| V51 (93604505 + V50 layer) | 8W-0L (26,323) | 0W-8L | 0W-2L | 0W-2L | 0W-2L | 0W-8L |

V50 reference: starter/Hamburger 16W-0L; failure families 4W-4L / 5W-3L / 8W-0L (4 seeds × both seats); native-seed tape league 92967433 WW, 92971175 LL, 92978681 WW.

## Root causes

- The extracted routes won their Public episodes on their native seeds; off-seed they lose route/task/position rhythm (same tape-fragility failure as V28/V47).
- V50's execution layer is not route-agnostic: applied to the 6/8 route it collapses the economy (mean bank 26k vs 178k bare), because the sale/front-run/feed schedule assumptions no longer match the route's inventory rhythm.
- The early coarse screen (2 seeds) showed false 4W-0L results for 93587364; the native-seed gate is decisive.

## Decision

Reject all four variants. V50 / submission `55547470` remains the best candidate: it is already submitted and leads the incumbent 55504047 by roughly +336 rating. No new submission is justified; continue collecting Public episodes and keep 55504047 as rollback reference.
