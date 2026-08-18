"""Held-out control gate for bare 93730164: public control agents + self mirror, 4 seeds x both seats."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
CAND = str((ROOT / 'research/agents/online/episode_93730164_opponent.py').resolve())
CONTROLS = ['frontier_v12', 'kaito_v21', 'replay_shield_v15', 'scenario_v14', 'soil_v25']
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
    tasks = []
    for c in CONTROLS:
        o = str((ROOT / 'research/agents/hamburger_controls' / f'{c}.py').resolve())
        for s in SEEDS:
            for seat in (0, 1):
                tasks.append((c, o, s, seat))
    for s in SEEDS[:2]:
        for seat in (0, 1):
            tasks.append(('self_mirror', CAND, s, seat))
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for label in CONTROLS + ['self_mirror']:
        g = [x for x in rows if x[0] == label]
        print(f"{label}: {sum(x[4]>0 for x in g)}W-{sum(x[4]<0 for x in g)}L-{sum(x[4]==0 for x in g)}T "
              f"mean_bank={statistics.mean(x[3] for x in g):.0f} "
              f"mean_margin={statistics.mean(x[4] for x in g):.0f} worst={min(x[4] for x in g):.0f}")


if __name__ == '__main__':
    main()
