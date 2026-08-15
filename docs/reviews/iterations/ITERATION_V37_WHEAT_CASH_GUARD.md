# V37 opponent-cash wheat slot guard

## Mechanism hypothesis

The public Broker Bea controller uses opponent cash as a market-order signal: when a rival is cash-starved, promoting a WHEAT sale can lower the feed price they need for animal upkeep. V37 keeps the v27 field/hand tape and current official-impact sell ordering, but restores WHEAT to its original sell slot whenever the opponent's public money is below 200 coins. No production, CARE, animal mix, or quantity changes are made.

## Validation

- `py_compile`: passed.
- Starter, 8 seeds × both seats: `16W-0L-0T`, mean reward `152,062`.
- Hamburger, 8 seeds × both seats: `16W-0L-0T`, mean reward `93,976`.
- `92971175`, 4 seeds × both seats: `5W-3L-0T`, mean reward `88,845`.
- `92978681`, 4 seeds × both seats: `0W-8L-0T`, mean reward `82,534`.
- `92967433`, 4 seeds × both seats: `3W-5L-0T`, mean reward `94,816`.

The failure-family W/L records are unchanged from v27. V37 is rejected; `agents/main.py` remains untouched and no submission is made.
