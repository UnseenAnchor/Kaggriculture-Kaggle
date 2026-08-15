# V43 feed/animal expansion reserve audit

## Scope

This phase stayed on the fixed production/labor direction. It did not create a candidate or modify `agents/main.py`.

## Replay evidence

The correct high-supply seats are seat 0 of `92971175` and seat 1 of `92967433`. Their common changes versus v27 are coupled rather than a single animal purchase:

- opening market: 5 HIRE, 2 COW + 2 SHEEP, larger WHEAT/MELON seed stock and WHEAT float;
- 14 PASTURE builds rather than v27's 13;
- 5 hands at the opening and sustained active transport/feeding work;
- 9 animals by day 8 and 14 animals by day 12, followed by later land/animal purchases;
- final production path: roughly 1,229 WHEAT / 1,775 FERTILIZER sold in `92971175`, versus v27's 455 / 235.

The high-supply replay uses only about 313 CARE actions, so this is not the CARE family in disguise. Conversely, `92978681` keeps 13 pastures and the v27-sized animal route but replaces idle work with about 957 CARE actions. The two families therefore have different bottlenecks: expansion/transport throughput versus animal-care utilization.

## Reference evidence

Rancher Rita's public reference policy documents the relevant reserve rule:

- hold `feed_float_days = 16` before buying an animal;
- sell before buying so same-turn proceeds fund feed;
- count shed and carried WHEAT in the flock budget;
- delay land/animal expansion until feed and working-capital buffers are satisfied;
- use a complete multi-unit job scheduler to move feed and service animals.

That reserve rule is inseparable from Rita's 8-hand, 16-pasture, 10-cow/6-sheep route and scheduler. V42 already tested the smallest apparent transplant (the opening Wheat float plus a fifth hand with dynamic jobs) and improved none of the three failure families.

## Decision

No safe V43 single mechanism exists under the current constraints. A reserve-only or extra-animal-only overlay would explain the high-supply family but not the independent CARE family; reproducing both requires a full route/scheduler redesign, not an isolated cash gate. Do not create V43, do not submit, and keep `55504047` / `agents/main.py` unchanged.
