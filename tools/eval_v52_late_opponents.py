"""V52 head-to-head vs 3 opponents that beat V50 late (93967175, 93928639, 93953242): native + held-out seeds, both seats."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
CAND = str((ROOT / 'research/agents/online/episode_93730164_opponent.py').resolve())
OPS = {
    'sokoranohimazin_6_12': 'episode_93967175_opponent.py',
    'freddy_10_4': 'episode_93928639_opponent.py',
    'moshel_6_12': 'episode_93953242_opponent.py',
}
# native seeds from each replay + held-out dev seeds
NATIVE = {'93967175': 1874963296, '93928639': None, '93953242': 824576567}
DEV = (27011, 27031, 27101, 27121)


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
    tasks = []
    for label, fn in OPS.items():
        o = str((ROOT / 'research/agents/online' / fn).resolve())
        for s in DEV:
            for seat in (0, 1):
                tasks.append((label, o, s, seat))
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for label in OPS:
        g = [x for x in rows if x[0] == label]
        print(f"V52 vs {label}: {sum(x[4]>0 for x in g)}W-{sum(x[4]<0 for x in g)}L "
              f"mean_margin={statistics.mean(x[4] for x in g):.0f} worst={min(x[4] for x in g):.0f}")


if __name__ == '__main__':
    main()