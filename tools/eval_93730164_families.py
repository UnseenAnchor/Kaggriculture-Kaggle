"""Failure-family gate for bare 93730164 (6cow/12sheep dominant branch): 4 seeds x both seats per family."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
CAND = str((ROOT / 'research/agents/online/episode_93730164_opponent.py').resolve())
FAMILIES = {
    'fail_92967433': str((ROOT / 'research/agents/online/episode_92967433_opponent.py').resolve()),
    'fail_92971175': str((ROOT / 'research/agents/online/episode_92971175_opponent.py').resolve()),
    'fail_92978681': str((ROOT / 'research/agents/online/episode_92978681_opponent.py').resolve()),
}
SEEDS = (27011, 27031, 27101, 27121)


def play(args):
    label, o, seed, seat = args
    from kaggle_environments import make
    agents = [CAND, o] if seat == 0 else [o, CAND]
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    env.run(agents)
    f = env.steps[-1]
    mine = float(f[seat].reward or 0)
    theirs = float(f[1 - seat].reward or 0)
    return label, seed, seat, mine, mine - theirs


def main():
    tasks = [(name, o, s, seat) for name, o in FAMILIES.items() for s in SEEDS for seat in (0, 1)]
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for label in FAMILIES:
        g = [x for x in rows if x[0] == label]
        print(f"{label}: {sum(x[4]>0 for x in g)}W-{sum(x[4]<0 for x in g)}L "
              f"mean_bank={statistics.mean(x[3] for x in g):.0f} "
              f"mean_margin={statistics.mean(x[4] for x in g):.0f} worst={min(x[4] for x in g):.0f}")


if __name__ == '__main__':
    main()
