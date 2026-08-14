"""Extract one player's public action sequence from a Kaggriculture replay."""
from pathlib import Path
import json
import pprint
import sys

replay_path = Path(sys.argv[1])
agent_index = int(sys.argv[2])
out_path = Path(sys.argv[3])
data = json.loads(replay_path.read_text(encoding="utf-8"))
actions = [(step[agent_index].get("action") or {"farmer": ["PASS"], "hands": [], "market": []})
           for step in data["steps"]]
info = data.get("info", {})
header = f'''"""Public observable action tape.

Source episode: {info.get("EpisodeId")}
Observed team: {info.get("TeamNames", [None, None])[agent_index]}
Observed seat: {agent_index}
This is replay behavior, not recovered private source code.
"""\n\n'''
source = header + "TRACE_ACTIONS = " + pprint.pformat(actions, width=140, compact=True) + "\n\n"
source += '''def agent(obs, config=None):
    # Replay steps store the action that produced that step; obs.step=0 maps to replay step 1.
    step = min(int(obs.step) + 1, len(TRACE_ACTIONS) - 1)
    return TRACE_ACTIONS[step]
'''
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(source, encoding="utf-8")
print(f"wrote {len(actions)} actions to {out_path}")
