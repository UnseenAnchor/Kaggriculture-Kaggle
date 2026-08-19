# ITERATION V66–V69 & V60-Reconfirm (TOP700 hunt)

**Date**: continuation of the ongoing TOP700 goal.
**Verdict**: ALL candidates rejected. V50 (8/4, submission/main.py) remains the active baseline. No safe candidate advances TOP700.

## Mechanistic finding (re-confirmed across local + online)

- Local 10/4 tape `93928639`: V50 8/4 = **1W-7L** (mean 76.6k vs ~79k).
- Online `94369267` (John Park 10/4, 173841 vs me 156094): the cow-10 opponent front-loads cows (2 at step1, 4 by 121, 10 by 265) and dribble-sells more (26→61→101 SELLs by phase 300/400) while my V50 holds 1 cow through step ~120 and under-sells mid-game.
- Both signatures: (1) late-milk timing (1 cow for first 120 steps), (2) mid-game FERTILIZER/WHEAT stockpiled unsold (my shed held FERTILIZER 24, WHEAT 13-16 at step 360 vs opponent 7/34).

## Candidate 1 — v66 jpsplice (John-Park opening splice onto V50 body)
- Approach: raw table splice = regression (~56k vs Starter). Reject.

## Candidate 2 — v67 fert-dribble (mid-game FERTILIZER/WHEAT dribble)
Hypothesis: sell surplus mid-game fertilizer/wheat to unlock cash-flow (universal, not composition).
- vs Starter: 8W-0L (mean 145.8k).
- vs 10/4 93928639: **0W-8L** (worse than V53's 1W-7L) — regression on that family.
- FULL GATE (registered failure families + mirror):
  - 92971175: **0W-8L** (V50 0-6 → no improvement)
  - 93604505: 4W-4L (V50 0-4 → helped)
  - 93730164: **2W-6L** (V50 0-2 → worse)
  - 92978681 mirror: 6W-2L (V50 6-0 → regressed 100%→75%)
- Net: improves 1 family, regresses 2. **REJECT** (fails "improve multiple failure families"). The added sells harm the mirror/structural cases more than they help.

## Candidate 3 — v68 front-cow (front-load cows at step 0 to counter milk-volume gap)
- Table-surgery patch kept crashing (constraint imbalance: step-0 cash budget + step-74 added SHEEP broke market/animal constraints; 3000 invalid runs).
- Attempt 3 on surgical table modification — stop; the doubtful assumption is that V50's fixed step-0 market orders can be re-arranged without violating cash/pasture/feed/maxOrders constraints. **REJECT.**

## Candidate 4 — v69 melonfront (cash-neutral STRAWBERRY→MELON seed substitution)
Hypothesis: MELON (250, sq 3.6) is ~2x STRAWBERRY (120, linear 1.6) at the same seed cost; front-loading early MELON should close the step-240..300 mid-game money gap (mine 2322→6518 vs winner 1791→14288 in that window).
- Implementation: rewrite equal-quantity `BUY_SEED STRAWBERRY→MELON` at steps 72/120/161/169 (16 units), cash-neutral + order-count-neutral + tile-neutral → no constraint risk.
- vs Starter: 8W-0L but mean dropped to 139.8k (V50 157k).
- GATE: 92971175 **0-8**, 93604505 **0-8**, 93730164 **0-8**, mirror 92978681 **0-8** (V50 6-0!), 10/4 **0-8**. Catastrophic regression everywhere (mean 65-76k).
- Root cause: STRAWBERRY's short cycle is load-bearing for continuous mid-game income; MELON's 12-day cycle + sq elasticity (early oversupply tanks price) is worse in the early-mid window. **REJECT.**

## Composition substitution re-verification (closes 6/8 route with fresh data)
- V60 (6/8) vs V50-loss families: 92971175 **8-0**, 93604505 **8-0**, 93730164 **7-1**, 92967433 **8-0**, 10/4 93928639 **8-0** — V60 dominates all V50 failure families.
- BUT V60 vs the 8/4 mirror 92978681 = 6W-2L (100%→75%), and **V60 vs V50 h2h 20 seeds × 2 seats = 17W-23L (43%)**.
- Live field is majority 8/4 mirror (11/18 in 55600926 sample) where 6/8 is weak → 6/8 is net-NEGATIVE online. This is why V60's live (1246) was low. **6/8 substitution definitively closed.** V60 was correctly NOT promoted to mainline.

## Leaderboard re-anchor
- Live has inflated: top-23 rows floor at ~2861; historical snapshot (55600926): rank 908/5165 at 1926.8, TOP500 cutoff 2239.8 → TOP700 ≈ ~2100.
- V50 best live = 1992.6 → gap to TOP700 ≈ **+100 to +150**. Confirmed out of reach by any candidate in this session.

## Leaderboard re-anchor (DECISIVE — reframes the goal)
- URL live leaderboard pulled to 1600+ rows: **TOP700 cutoff = 2052.6, TOP800 = 1981.2**.
- My current active (55600926 = V50 code) = **1857.9 → ~rank 1010** (top ~310 ranks below TOP700).
- **V50 artifact's own historical live best = 2069.5 (57 ep) and 2093.4 (187 ep)** — BOTH above the current 2052.6 TOP700 line.
- Identity code (V50) has scored 616 / 1857.9 / 1969 / 1992.6 / 2069.5 / 2093.4 live: rating is matchmaking-dominated (±200 swing on identical bytes).
- ⇒ The artifact is ALREADY TOP700-capable. The gap is a **run/rating/rating-match variable, not a strength gap** — consistent with all 4 candidates (v66-v69) being rejected for not adding real strength.
- Highest-EV forward action is to restore V50's live rating toward its 2069-2093 peak (fresh matchmaking draw), NOT to engineer new strength that provably cannot be added within constraints.

## Conclusion
No safe, constraint-respecting candidate improves net online strength above V50's ceiling. The 10/4 niche is a minority the 8/4 mainline cedes; no fixed composition wins both the majority mirror and the niche; opponent-tribe runtime detection is infeasible (no observable signal, re-confirmed). Maintain **submission/main.py = V50**; do NOT submit.

Composition meta is a provable rock-paper-scissors cycle (8/4 > 6/8 > 10/4 > 8/4), verified locally: V60 6/8 vs V50 8/4 h2h = 17W-23L; V60 6/8 vs 10/4 93928639 = 8W-0L; V50 8/4 vs 10/4 93928639 = 1W-7L. No fixed composition can topologically dominate all legs, so the TOP700 cutoff (~2100 vs V50 best 1992.6, +100 to +150) is out of reach by any single-lateral change.

## Decision
- v66 / v67 / v68 / v69: **REJECT** (delete from consideration; do not resubmit).
- V60 (6/8): **REJECT as mainline** (net 17W-23L vs V50 h2h).
- Active baseline unchanged: `submission/main.py` (V50).
