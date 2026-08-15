# V39 failure-family state audit

## Scope

This is an analysis-only phase. It does not create a candidate or reopen V28 relay, V29 CARE, V31 extra-hand fertilizer, or V32 animal-mix experiments. The active submission remains 55504047.

## High-supply family

Local replay comparisons used the fixed opponent tapes for `92971175` and `92967433` at seed `27011`, both seats, with `agents/main.py` as the other player.

The high-supply opponent is not a market-only perturbation of v27:

- v27 route: 4 sheep / 9 cow, about 212 WHEAT product purchases, 455 WHEAT sold, and 235 FERTILIZER sold in the replay accounting.
- high-supply route: 8 sheep / 6 cow, about 433–500 WHEAT product purchases, 1,162–1,229 WHEAT sold, and 1,775–1,994 FERTILIZER sold.
- The opponent also uses CARROT and a materially different labor schedule, with far fewer idle PASS turns.

The state snapshots show the divergence is production capacity and working-capital throughput, not an isolated order-slot failure. In one seat pairing the high-supply route has already accumulated 8 sheep by step 288 while v27 has 4; by the end it has roughly 1.8k–2.0k fertilizer throughput versus v27's 235.

## Near-neighbor family

Episode `92994559` is identified in the submission review as an asset/movement near-neighbor of v27, but its replay artifact is not present in the local `research/agents/online` set. V30 already tested fixed-route demand-aware SELL ordering against this class and found no improvement; the local evidence does not justify inventing a new causal explanation.

## Broader failure cluster

Additional downloaded replays confirm the same partition:

- `92995487`: 10 COW, 50.3% movement, 871 WHEAT sold and 1,487 FERTILIZER sold — production/labor expansion.
- `92997365` and `92990803`: near-v27 4/8 assets with 957–966 CARE and materially higher MILK/FERTILIZER output — the already rejected CARE family.
- `92992675`: 12 SHEEP / 6 COW, a third land quadrant, 1,473 WHEAT and 1,748 FERTILIZER sold — the already rejected high-supply relay family.
- `92994559`: near-identical production with a market timing/SELL advantage — the already rejected V30 class.

## Decision

No isolated route-level mechanism is supported by this comparison. The observed losses partition into closed production/labor, CARE, high-supply, and SELL-timing families. Keep 55504047 active, leave `agents/main.py` untouched, and do not submit a new version until a genuinely new mechanism or new evidence appears.
