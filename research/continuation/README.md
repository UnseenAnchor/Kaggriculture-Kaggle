# Typed continuation trace

This package is offline research infrastructure, not a Kaggle agent.

Validate a full replay trace:

```bash
D:/ke/python.exe tools/validate_continuation.py research/replays/episode-92971175-replay.json --seat 1
D:/ke/python.exe tools/validate_continuation.py research/replays/episode-92971175-replay.json --seat 0
```

The current phase navigates complete observable routes as immutable
`ContinuationState` and `ActionIntent` records. It checks action count,
snapshot coverage, finite resource values, structural non-negativity, and
non-empty action orders. It does not generate actions or splice routes.
