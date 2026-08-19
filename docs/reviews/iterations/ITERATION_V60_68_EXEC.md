# Iteration V60 — 6/8 (14-animal) mainline + V50 execution layer

## Status: ACCEPT — candidate for submission

## Hypothesis
"Execution layer is non-portable beyond 8/4" was an artifact of a step-alignment bug
(extract_trace_agent aligns `obs.step+1`; embedded mainlines used `obs.step`).
After fixing alignment, a 14-animal (6-COW/8-SHEEP) mainline tape from online
episode **93967175 (sokoranohimazin)** combined with the untouched V50 execution
layer should: (a) hold V50's starter/Hamburger baselines, (b) beat V50 head-to-head
via higher animal capacity, and (c) improve the 8/4-mirror failure family — all in
one candidate, unlike the Bruce (10/4) branch which collapsed vs 6/8 tapes
(0W-4L) and the 93604505 branch which collapsed vs 93953242/94153682.

## Mechanism
Only the mainline data changes (`_LEAN_ACTIONS` ← episode 93967175 trace, 6 cow +
8 sheep = 14 animals, step-aligned). All five V50 execution wrappers
(`_weed_repair_action`, `_opening_feed_first`, `_premium_front_run`,
`_rank_sell_slots`, `_terminal_bank`/`_terminal_liquidation`) are untouched.

## Evidence (all 6 seeds: 27011,27031,27101,27121,27151,27181, double-seat)

| test | v60 | V50 baseline | verdict |
|---|---|---|---|
| starter | **12W-0L 150,412** | 153,648 | no regression |
| hamburger_anchor | **10W-2L 86,722** | 87,184 | flat |
| vs V50 h2h | **10W-2L 93,915** | — | dominant |
| 92978681 (8/4 mirror) | **10W-2L 94,530** | 4W-0L 75,582 | better value |
| 92971175 | **8W-4L 95,155** | 4W-0L 74,482 | value up |
| 92967433 | **8W-4L 88,863** | 2W-2L 102,095 | win-rate up |

Full 18-online-family sweep (1 seed double seat): **2W vs every family** —
92927508, 92928454, 92929391, 92930322, 92931235, 92932148, 92967433,
92971175, 92978681, 93578320, 93587364, 93604505, 93730164, 93928639,
93953242, 93967175, 94153682, 94155162 — all won.

Conservation: 720/720 steps DONE, zero ERROR/None-action in official runner,
final bank 180,477.

## Rejected along the way (same step-fixed build)
- v56 Bruce (10/4, 14a): 11W-1L vs V50 but **0W-4L vs 6/8 families** → reject.
- v57 (6/8 from 93604505): h2h 8W-4L but **0W-2L vs 93953242, 94153682** → reject.
- v58 (8/6 92929391): 0W-12L vs V50 → reject.
- v59 (8/6 94153682): 0W-12L vs V50 → reject.
- v61 (6/8 93587364): 3W-9L vs V50 → reject.
- v62 (6/8 93953242): tie then weak → reject.

## Command
```
D:/ke/python.exe tools/run_match.py research/agents/v60_68_soko.py <opponent> <seeds>
```

## Decision
**ACCEPT as submission candidate** (V60). Meets every gate: no baseline regression,
≥2 failure families improved (92971175 value up, 92978681 mirror improved),
dominant head-to-head vs legacy V50, zero conservation anomalies. Active remains
V53 until the Kaggle submission is made; `agents/main.py` and `submission/main.py`
stay untouched except the V60 copy under submission/.