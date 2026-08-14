"""Build self-contained one-switch route relay candidates."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V27 = ROOT / "research/agents/kaito_v27_midgame_reset.py"
TRACE = ROOT / "research/agents/online/episode_92971175_opponent.py"
OUT = ROOT / "research/agents/route_hybrids"

v27 = V27.read_text(encoding="utf-8").rstrip()
trace = TRACE.read_text(encoding="utf-8").rstrip()
common = v27 + "\n\n_V27_AGENT = agent\n\n" + trace + "\n\n_TRACE_AGENT = agent\n\n"

relay = common + '''def trace_open_v27_agent(obs, configuration=None):
    """Use the 8-sheep/6-cow opening once, then execute the v27 route."""
    if int(getattr(obs, "step", 0) or 0) == 0:
        return _TRACE_AGENT(obs, configuration)
    return _V27_AGENT(obs, configuration)

submission_agent = trace_open_v27_agent
'''

OUT.mkdir(parents=True, exist_ok=True)
path = OUT / "trace_open_v27_after1.py"
path.write_text(relay, encoding="utf-8")
print(path)
