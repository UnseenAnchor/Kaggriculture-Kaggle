# V33 Yarn-demand animal adapter

## Hypothesis

92971175 and 92978681 both expose `YARN_STORE` by step 192 and both winners use materially more sheep. Hamburger controls do not expose Yarn at that checkpoint. Therefore, conditionally converting the existing two-cow purchase/place slots to sheep only when early Yarn demand is visible may address the sheep/wool pressure family without damaging ordinary markets. No relay, extra worker, or CARE change.

## Gates

- 8 development/unseen seeds × both seats against starter and Hamburger.
- Four fixed failure seeds × both seats against 92971175, 92978681, and 92967433.
- Stop on any base-gate regression or failure to improve both Yarn-linked families.

## Results

- starter: 16W-0L.
- Hamburger: 16W-0L.
- 92971175: 5W-3L.
- 92978681: 0W-8L.
- 92967433: 3W-5L.
- The Yarn signal did not activate a useful improvement; results match the v27 failure-family baseline. It did not improve either Yarn-linked family or the CARE family.

## Decision

**Reject V33.** The demand-conditioned animal-mix branch is closed. Do not tune the Yarn trigger or sheep/cow ratio further, and do not submit.
