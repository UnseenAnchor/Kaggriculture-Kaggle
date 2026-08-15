# V44 full job-scheduler reference audit

## Question

After V42 failed as a fifth-hand overlay and V43 found that feed reserves could not be isolated from expansion, test whether the complete public Rancher Rita scheduler is a viable production/labor direction.

## Evidence

Rancher Rita uses the documented full capacity route: 8 hands, 2 extra quadrants, 16 pastures, 10 cows / 6 sheep, 16 feed-float days, sell-before-buy market planning, and a multi-unit priority scheduler.

Local seeded control:

- Rita vs starter, seeds `27011,27031,27101,27121`, both seats: **8W-0L-0T**, mean reward **47,259**, minimum **38,210**.
- Rita vs `agents/main.py`, same seeds and seats: **0W-8L-0T**, mean reward **25,526**, minimum **2,934**.

The scheduler is therefore a valid public reference implementation but not a competitive replacement for the v27 active route. Its reserve logic cannot be transplanted independently without also importing its land, animal, crop, movement, and job-allocation policy.

## Decision

**Close the full-scheduler transplant direction.** Do not create V44 code, do not submit, and keep `55504047` / `agents/main.py` unchanged. A future capacity experiment would require a new external mechanism or new replay evidence, not another partial Rita transplant.
