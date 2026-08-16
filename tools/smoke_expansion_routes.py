"""Quick parallel smoke test for extracted expansion routes vs starter."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
ROUTES = ['episode_93604505_opponent', 'episode_93587364_opponent', 'episode_93578320_opponent']
SEEDS = (27011, 27031)


def play(args):
    c, seed, seat = args
    from kaggle_environments import make
    agents = [c, 'starter'] if seat == 0 else ['starter', c]
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    env.run(agents)
    f = env.steps[-1]
    mine = float(f[seat].reward or 0)
    theirs = float(f[1 - seat].reward or 0)
    return c, seed, seat, mine, mine - theirs


def main():
    tasks = [(str((ROOT / 'research/agents/online' / f'{r}.py').resolve()), s, seat)
             for r in ROUTES for s in SEEDS for seat in (0, 1)]
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for r in ROUTES:
        c = str((ROOT / 'research/agents/online' / f'{r}.py').resolve())
        g = [x for x in rows if x[0] == c]
        print(r, sum(x[4] > 0 for x in g), 'W', sum(x[4] < 0 for x in g), 'L',
              'mean_bank', round(statistics.mean(x[3] for x in g)),
              'min', round(min(x[3] for x in g)))


if __name__ == '__main__':
    main()
