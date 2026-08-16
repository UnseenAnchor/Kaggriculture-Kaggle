"""Evaluate extracted expansion routes vs Hamburger anchor and the three failure-family tapes."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ['episode_93604505_opponent', 'episode_93587364_opponent', 'episode_93578320_opponent']
OPPONENTS = {
    'hamburger': str((ROOT / 'research/agents/hamburger_anchor.py').resolve()),
    'fail_92967433': str((ROOT / 'research/agents/online/episode_92967433_opponent.py').resolve()),
    'fail_92971175': str((ROOT / 'research/agents/online/episode_92971175_opponent.py').resolve()),
    'fail_92978681': str((ROOT / 'research/agents/online/episode_92978681_opponent.py').resolve()),
}
SEEDS = (27011, 27031)


def play(args):
    c, o, seed, seat = args
    from kaggle_environments import make
    agents = [c, o] if seat == 0 else [o, c]
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    env.run(agents)
    f = env.steps[-1]
    mine = float(f[seat].reward or 0)
    theirs = float(f[1 - seat].reward or 0)
    return c, o, seed, seat, mine, mine - theirs


def main():
    tasks = [(str((ROOT / 'research/agents/online' / f'{r}.py').resolve()), o, s, seat)
             for r in ROUTES for o in OPPONENTS.values() for s in SEEDS for seat in (0, 1)]
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for r in ROUTES:
        c = str((ROOT / 'research/agents/online' / f'{r}.py').resolve())
        g = [x for x in rows if x[0] == c]
        print(f"\n{r}: total {sum(x[5]>0 for x in g)}W-{sum(x[5]<0 for x in g)}L")
        for name, o in OPPONENTS.items():
            sub = [x for x in g if x[1] == o]
            print(f"  vs {name}: {sum(x[5]>0 for x in sub)}W-{sum(x[5]<0 for x in sub)}L "
                  f"mean_bank={statistics.mean(x[4] for x in sub):.0f} "
                  f"mean_margin={statistics.mean(x[5] for x in sub):.0f} worst={min(x[5] for x in sub):.0f}")


if __name__ == '__main__':
    main()
