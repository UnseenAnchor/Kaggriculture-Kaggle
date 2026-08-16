# V45 latest public failure audit

## Sample

Downloaded the ten newest completed Public replays for active submission `55504047` (episodes `93405504` through `93458883`) and compared the active seat with the opponent.

The sample result was **0W-8L-2T**, mean margin **-8,058**.

## Failure families

- High-supply family: `93405504`, `93409876`, `93430251`, `93458883`. Opponents use 14–15 pastures, 271–289 hires, and materially higher WHEAT/FERTILIZER throughput. Margins: **-19,737, -9,589, -8,110, -14,639**.
- CARE family: `93433790`. Opponent keeps the compact animal route but uses 955 CARE and wins **+25,224**.
- New marginal near-neighbor: `93426809`, `93443663`, `93454417`. Opponents use 5 SHEEP / 9 COW, 15 pastures, about 259 hires and 958–992 PASS; margins are only **-1,180, -670, -1,428**.
- Two ties: `93418009`, `93433953`.

## Causal assessment

The marginal near-neighbor is not evidence for an isolated one-sheep fix. Across the three games it changes pasture count, animal inventory, hire timing, task movement, CARE, and Wheat purchases together. The high-supply family changes the same capacity bundle at a larger scale, while the CARE family has a different bottleneck despite similar animals.

This new online sample confirms pressure on the active baseline but does not supply a safe single mechanism that covers two independent families. Do not create a candidate or submit on the basis of the near-neighbor alone. Keep `55504047` active until new replay evidence isolates a mechanism.
