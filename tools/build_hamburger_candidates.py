"""Build attributed public Hamburger candidates from the pulled public notebook assets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
anchor = (ROOT / "research/agents/hamburger_anchor.py").read_text(encoding="utf-8").rstrip()
overlay = (ROOT / "research/agents/hamburger_overlay.py").read_text(encoding="utf-8")
out = ROOT / "research/agents/hamburger_candidates"
out.mkdir(parents=True, exist_ok=True)

specs = {
    "no_cashflow": {"cashflow_mode": "none"},
    "static_slots": {"cashflow_mode": "static_slots"},
    "collision_slots": {"cashflow_mode": "collision_slots"},
    "collision_front": {"cashflow_mode": "collision_front"},
    "relay716": {"terminal_relay": True, "terminal_start": 716},
    "relay717": {"terminal_relay": True, "terminal_start": 717},
    "collision_slots_relay716": {
        "cashflow_mode": "collision_slots",
        "terminal_relay": True,
        "terminal_start": 716,
    },
}

for name, spec in specs.items():
    rendered = (overlay
        .replace("__CASHFLOW_MODE__", repr(spec.get("cashflow_mode", "anchor")))
        .replace("__TERMINAL_RELAY__", repr(bool(spec.get("terminal_relay", False))))
        .replace("__TERMINAL_START__", str(int(spec.get("terminal_start", 716)))))
    # kaggle-environments loads the last newly-registered callable from a file.
    # Redefining an existing `agent` key does not move it to the end of globals,
    # so add a fresh alias after the overlay.
    source = anchor + "\n\n" + rendered + "\n\nsubmission_agent = agent\n"
    path = out / f"{name}.py"
    path.write_text(source, encoding="utf-8")
    compile(source, str(path), "exec")
    print(path)
