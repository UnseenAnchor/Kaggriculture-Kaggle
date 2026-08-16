# V47 anchored expansion planner

## Hypothesis

Keep v27 through a capital anchor, then switch to a complete Rancher-style continuation planner for pasture, animals, feed, crop and hand scheduling. This was intended to address high-supply throughput without raw tape relay.

## Attempts

- Day-8 anchor, daily hand target 6→8: `0W-8L` vs v27, mean bank about 8,262.
- Day-16 anchor after adding surplus-market liquidation: `0W-8L` vs v27, mean bank about 37,810.
- The day-8 version bankrupted because it hired before selling existing Fertilizer/Wheat; the market fix prevented immediate bankruptcy but did not recover production.

## Root cause

The full scheduler does not preserve v27's productive action/position rhythm after the anchor. Existing animals are not kept on the same feed/CARE/output cadence, and daily hand costs dominate before the new task graph produces revenue. This is a route/state incompatibility, not a missing threshold.

## Decision

Reject and freeze. Do not tune another anchor, hand count, or sell order. `agents/main.py` and submission `55504047` remain unchanged.
