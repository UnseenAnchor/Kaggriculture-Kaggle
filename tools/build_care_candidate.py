"""Build the single-variable v27 idle-hand CARE candidate."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/agents/kaito_v27_midgame_reset.py"
OUT = ROOT / "research/agents/care_candidates/v27_hand_care.py"

base = BASE.read_text(encoding="utf-8").rstrip() + '''

_V27_BASE_AGENT = agent
'''

hand_source = base + '''
def v27_hand_care_agent(obs, configuration=None):
    """Replace only idle hand PASS actions with CARE; keep the route unchanged."""
    action = _V27_BASE_AGENT(obs, configuration)
    action["hands"] = [
        ["CARE"] if list(hand_action) == ["PASS"] else hand_action
        for hand_action in action.get("hands", [])
    ]
    return action

submission_agent = v27_hand_care_agent
'''

all_source = base + '''
def v27_all_actor_care_agent(obs, configuration=None):
    """Replace idle farmer/hand PASS actions with CARE; keep the route unchanged."""
    action = _V27_BASE_AGENT(obs, configuration)
    if list(action.get("farmer", [])) == ["PASS"]:
        action["farmer"] = ["CARE"]
    action["hands"] = [
        ["CARE"] if list(hand_action) == ["PASS"] else hand_action
        for hand_action in action.get("hands", [])
    ]
    return action

submission_agent = v27_all_actor_care_agent
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(hand_source, encoding="utf-8")
all_path = OUT.with_name("v27_all_actor_care.py")
all_path.write_text(all_source, encoding="utf-8")
print(OUT)
print(all_path)
