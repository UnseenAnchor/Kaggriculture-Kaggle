# V42 production/labor capacity scheduler

## Fixed direction

This was the only direction pursued in this phase: increase effective production/labor throughput. No second market, Yarn, animal-mix, fixed-relay, or CARE-specific candidate was made.

## Replay/state evidence

The high-supply and CARE failure families both convert more turns into output than v27. Public replay `92971175` uses 277 hires, 684 PASS, 1,229 WHEAT and 1,775 FERTILIZER sold; v27 uses 262 hires, 995 PASS, 455 WHEAT and 235 FERTILIZER. Replay `92978681` keeps the v27-sized animal route but uses a fifth opening hand and much higher CARE/MILK/FERTILIZER throughput.

The candidate hypothesis was that the smallest shared capacity intervention is a working-capital-funded fifth hand: reproduce the observed opening Wheat float, add one HIRE at step 0, and dispatch only that additional hand to unmet CARE, fertilizer collection, harvest, and watering jobs. The original four-hand route remains delegated to `agents/main.py`.

## Candidate and validation

Candidate: `research/agents/v42_capacity_hand_scheduler.py`.

A first single-seed smoke exposed an overlay bookkeeping bug: when the fifth HIRE was not accepted, the last baseline hand was incorrectly rewritten. The candidate was corrected to dispatch only when the observed hand count exceeded the original tape's planned count. The corrected candidate restored the baseline control result before the formal gate.

Formal smoke gate:

- starter, 8 seeds × both seats: **16W-0L-0T**, mean reward **152,059**, minimum **100,529**.
- Hamburger, 8 seeds × both seats: **16W-0L-0T**, mean margin **+93,969**, worst **+25,838**.
- `92971175`, 4 seeds × both seats: **5W-3L-0T**, mean reward **88,844**; no improvement.
- `92978681`, 4 seeds × both seats: **0W-8L-0T**, mean reward **80,339**; no improvement.
- `92967433`, 4 seeds × both seats: **3W-5L-0T**, mean reward **94,815**; no improvement.

Known `universal_poker` / `repeated_poker` OpenSpiel messages appeared during the runner but matches completed normally and emitted complete result rows.

## Decision

**Reject V42.** The capacity mechanism preserves starter/Hamburger controls but improves zero independent failure families. Do not tune its hand dispatch, HIRE timing, or Wheat quantity. Do not submit V42 or modify `agents/main.py`; keep submission `55504047` active.
