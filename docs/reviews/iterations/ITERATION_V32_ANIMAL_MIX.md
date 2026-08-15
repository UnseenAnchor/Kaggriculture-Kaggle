# V32 Animal mix: 6 sheep / 7 cows

## Hypothesis

The recurring losses are supply-capacity failures. Public winners repeatedly use more sheep and sell substantially more Wool/Fertilizer, while v27 is approximately 4 sheep / 9 cows. V32 tests one route-level variable: convert the existing two-cow purchase/place slots at action steps 192, 198, and 204 to sheep, producing approximately 6 sheep / 7 cows. Movement, workers, CARE, feeding, crop schedule, and all other market orders remain unchanged. This is not a relay and not a CARE experiment.

## Gates

- Development seeds: 27011, 27031, 27101, 27121; both seats.
- Unseen seeds: 37011, 37031, 37101, 37121; both seats.
- Compare `starter`, `hamburger_anchor`, and failure tapes 92971175, 92978681, 92967433.
- Stop if starter/Hamburger regresses, if any catastrophic loss appears, or if the animal mix does not improve at least two independent failure families.

## Results

- Unconditional 6 sheep / 7 cow variant: starter 16W-0L, but Hamburger 14W-2L; stopped before failure-family testing.
- Conditional variant (switch only when opponent animal count at step 192 was at least 9): starter 16W-0L, Hamburger 16W-0L, but failure tapes were all 0W-8L: 92971175, 92978681, and 92967433.
- The conditional signal did not preserve the needed cashflow/production balance and did not improve any independent failure family.

## Decision

**Reject the V32 animal-mix branch.** Do not tune sheep/cow ratios or thresholds further. Keep the v27 route unchanged and do not submit V32.
