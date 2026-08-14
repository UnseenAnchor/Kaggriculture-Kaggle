"""Tournament public Hamburger candidates against anchor + public control families."""
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (27011, 27031)


def play(task):
    candidate, opponent, seed, seat = task
    from kaggle_environments import make
    agents = [candidate, opponent] if seat == 0 else [opponent, candidate]
    env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
    env.run(agents)
    final = env.steps[-1]
    mine = float(final[seat].reward or 0)
    theirs = float(final[1-seat].reward or 0)
    return candidate, opponent, seed, seat, mine, theirs, mine - theirs


def main():
    candidates = [
        str((ROOT / "research/agents/online/episode_92971175_opponent.py").resolve()),
        str((ROOT / "research/agents/online/episode_92967433_opponent.py").resolve()),
        str((ROOT / "research/agents/kaito_v27_midgame_reset.py").resolve()),
        str((ROOT / "research/agents/hamburger_anchor.py").resolve()),
    ]
    candidates += [str(p.resolve()) for p in sorted((ROOT / "research/agents/hamburger_candidates").glob("*.py"))]
    opponents = [str((ROOT / "research/agents/hamburger_anchor.py").resolve())]
    opponents += [str(p.resolve()) for p in sorted((ROOT / "research/agents/hamburger_controls").glob("*.py"))]
    tasks = [(c, o, seed, seat) for c in candidates for o in opponents for seed in SEEDS for seat in (0, 1)]
    rows = []
    with ProcessPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(play, t) for t in tasks]
        for f in as_completed(futures): rows.append(f.result())
    for candidate in candidates:
        group = [r for r in rows if r[0] == candidate]
        wins = sum(r[6] > 0 for r in group); losses = sum(r[6] < 0 for r in group)
        margins = [r[6] for r in group]
        print(f"{Path(candidate).stem}: {wins}W-{losses}L-{len(group)-wins-losses}T | "
              f"mean={statistics.mean(margins):.0f} | worst={min(margins):.0f}")
        for opponent in opponents:
            sub = [r[6] for r in group if r[1] == opponent]
            print(f"  vs {Path(opponent).stem}: {sum(x>0 for x in sub)}W-{sum(x<0 for x in sub)}L | "
                  f"mean={statistics.mean(sub):.0f} | worst={min(sub):.0f}")


if __name__ == "__main__":
    main()
