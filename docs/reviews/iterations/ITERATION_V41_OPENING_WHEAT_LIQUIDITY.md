# V41 opening Wheat liquidity cycle

## Mechanism hypothesis

Episode `92994559` showed a near-v27 route buying 14 WHEAT at step 0, selling 9 at step 1, then buying 3 MELON and 2 WHEAT seeds. The hypothesis was that this two-turn working-capital cycle changes early cash availability and market inventory without changing farmer, hand, animal, CARE, or long-term route actions.

This is deliberately one candidate, not a quantity/threshold sweep. The candidate is `research/agents/v41_opening_wheat_liquidity.py`; `agents/main.py` was not modified.

## Candidate behavior

- Step 0: replace the baseline opening market list with the observed order: BUY_PRODUCT WHEAT 14, HIRE×4, animals, MELON seeds, WHEAT seeds.
- Step 1: add SELL WHEAT 9, BUY_SEED MELON 3, BUY_SEED WHEAT 2.
- All later actions delegate to the active baseline.

## Smoke gate

Command form:

```bash
D:/ke/python.exe tools/run_match.py research/agents/v41_opening_wheat_liquidity.py <opponent> <seeds>
```

Controls, 8 seeds × both seats:

- starter, seeds `27011,27031,27101,27121,37011,37031,37101,37121`: **16W-0L-0T**, mean reward **152,054**, min **100,524**.
- Hamburger anchor, same seeds: **16W-0L-0T**, mean margin **+93,974**, worst **+25,838**.

Fixed failure families, 4 seeds × both seats:

- `92971175`: **5W-3L-0T**, mean reward **88,839**; no improvement.
- `92978681`: **0W-8L-0T**, mean reward **80,339**; no improvement.
- `92967433`: **3W-5L-0T**, mean reward **94,810**; no improvement and slightly below the recorded baseline of about **94,816**.

The recurring `universal_poker` / `repeated_poker` OpenSpiel messages are the known environment dependency noise; Kaggriculture matches still completed and produced normal result rows.

## Decision

**Reject V41.** It preserves starter/Hamburger gates but improves zero independent failure families, so the stop rule applies. Do not run unseen/full regression, do not modify `agents/main.py`, and do not submit a new Kaggle version. Keep submission `55504047` active.
