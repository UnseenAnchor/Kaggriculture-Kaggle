# V48 opponent capacity response

## Hypothesis

Some losses reveal a large-capacity opening after the first observable turns: five hands plus a larger COW/SHEEP opening. Only after detecting that public profile, add one extra daily hire and schedule the extra hand from live state. Normal v27-like openings should remain unchanged.

## Results

Four-seed, dual-seat smoke:

- vs `agents/main.py`: `2W-2L-4T`; this is consistent with the existing self-mirror asymmetry, not an improvement claim.
- vs high-supply replay `92971175`: `0W-8L`, mean bank about 10,608 after activation.
- vs CARE/cashflow replay `92978681`: `0W-8L`, unchanged from baseline family failure.
- vs starter: `8W-0L`.
- vs Hamburger: `8W-0L`.

## Root cause

The response is still the rejected capacity overlay in a delayed form. The extra daily hire costs cash before its local job scheduler produces enough output; it does not repair the full production/market route.

## Decision

Reject and freeze. No further fifth-hand, hire-ramp, or extra-hand scheduler variants. Keep `55504047` active and do not submit V48.
