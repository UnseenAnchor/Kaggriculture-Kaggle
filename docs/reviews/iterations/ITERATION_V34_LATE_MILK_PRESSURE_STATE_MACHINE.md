# V34 late milk-pressure state machine

## Hypothesis

The 92971175 and 92978681 failure families diverge from the control route late: by step 361, milk prices have collapsed while the v27 route still buys one final cow at step 361 and places it at step 518. A late state transition can reduce future milk exposure without disturbing the early capital route.

The transition is deliberately narrow and observable: at step 361, require milk price below 130 and a non-control high-pressure opponent animal structure (at least 12 opponent animals, with sheep count different from 6); replace only the existing step-361 cow purchase and step-518 cow placement with sheep. No relay, SELL change, CARE change, extra worker, or early animal-mix change.

## Gates

- 8 development/unseen seeds × both seats against starter and Hamburger.
- Four fixed seeds × both seats against 92971175, 92978681, and 92967433.
- Required: no base-gate loss, improve both milk-pressure families, and no catastrophic margin.

## Results

- starter: 16W-0L.
- Hamburger: 16W-0L.
- 92971175: 5W-3L.
- 92978681: 0W-8L.
- 92967433: 3W-5L.
- The late cow-to-sheep transition changed margins but not the win/loss pattern and improved no failure family.

## Decision

**Reject V34.** One late animal slot is too small to counter the pressure and is not worth further threshold tuning.
