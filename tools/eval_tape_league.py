"""Evaluate candidate agents against all downloaded public online-opponent tapes."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import csv
import json
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]


def one_game(args):
    candidate, opponent, seed, seat, episode = args
    from kaggle_environments import make
    agents = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run(agents)
    final = env.steps[-1]
    mine = float(final[seat].reward or 0)
    theirs = float(final[1 - seat].reward or 0)
    return {
        "candidate": candidate,
        "episode": episode,
        "seed": seed,
        "seat": seat,
        "mine": mine,
        "theirs": theirs,
        "margin": mine - theirs,
        "outcome": "W" if mine > theirs else ("L" if mine < theirs else "T"),
    }


def main():
    candidates = sys.argv[1:]
    if not candidates:
        candidates = ["agents/main.py", "research/agents/hamburger_anchor.py"]
    tapes = []
    for replay in sorted((ROOT / "research/replays").glob("episode-*-replay.json")):
        data = json.loads(replay.read_text(encoding="utf-8"))
        names = data["info"]["TeamNames"]
        if "道海孤舟" not in names:
            continue
        episode = int(data["info"]["EpisodeId"])
        opponent = ROOT / "research/agents/online" / f"episode_{episode}_opponent.py"
        if opponent.exists():
            tapes.append((episode, int(data["info"]["seed"]), str(opponent)))
    tasks = [(str((ROOT / c).resolve()), opponent, seed, seat, episode)
             for c in candidates for episode, seed, opponent in tapes for seat in (0, 1)]
    rows = []
    with ProcessPoolExecutor(max_workers=min(6, len(tasks))) as pool:
        futures = [pool.submit(one_game, task) for task in tasks]
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda r: (r["candidate"], r["episode"], r["seat"]))
    out = ROOT / "research" / "tape_league_results.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    for candidate in candidates:
        resolved = str((ROOT / candidate).resolve())
        group = [r for r in rows if r["candidate"] == resolved]
        wins = sum(r["outcome"] == "W" for r in group)
        losses = sum(r["outcome"] == "L" for r in group)
        margins = [r["margin"] for r in group]
        print(f"{candidate}: {wins}W-{losses}L-{len(group)-wins-losses}T | "
              f"mean_margin={statistics.mean(margins):.0f} | worst={min(margins):.0f} | "
              f"mean_bank={statistics.mean(r['mine'] for r in group):.0f}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
