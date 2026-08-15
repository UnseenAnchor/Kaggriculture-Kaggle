# V35 pressure crop route switch

## Hypothesis

The two severe milk/strawberry failure families share an early public signature: at step 192, milk price is at most 190 and the opponent has 9–10 animals. Controls have either no animals (starter) or 14 animals (Hamburger), so the switch can be tested without changing the normal control route.

When the signature appears, switch the remaining strawberry production route to wheat: future `BUY_SEED`, `PLANT`, and existing `SELL` slots for strawberry are rewritten to wheat. This is a single phase transition in product strategy, not a SELL reorder, animal change, CARE overlay, worker change, or relay.

## Gates

- 8 development/unseen seeds × both seats against starter and Hamburger.
- Four fixed seeds × both seats against 92971175, 92978681, and 92967433.
- Required: no base-gate loss, improve both pressure families, and no catastrophic margin.

## Results

- Original route switch (rewriting future strawberry BUY_SEED, PLANT, and SELL slots): starter 16W-0L, Hamburger 16W-0L, but severe score collapse; 92971175 was 5W-3L, 92978681 was 0W-8L, and 92967433 was 3W-5L.
- Reserve-safe correction (rewrite only BUY_SEED and PLANT, preserving strawberry SELL slots): starter 16W-0L and Hamburger 16W-0L, but 92971175 was 9W-7L, 92978681 was 0W-16L, and 92967433 was 4W-12L.
- The crop switch breaks the fixed harvest/seed/action dependencies and does not improve the pressure families.

## Decision

**Reject V35.** Do not tune the pressure threshold or crop substitution further.
