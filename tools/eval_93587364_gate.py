"""Full local gate for bare 93587364 expansion route: starter, Hamburger, failure families, and V50 head-to-head."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
CAND = str((ROOT / 'research/agents/online/episode_93587364_opponent.py').resolve())
V50 = str((ROOT / 'research/agents/v50_adaptive_replay_policy.py').resolve())
OPPONENTS = {
    'starter': 'starter',
    'hamburger': str((ROOT / 'research/agents/hamburger_anchor.py').resolve()),
    'fail_92967433': (str((ROOT / 'research/agents/online/episode_92967433_opponent.py').resolve()), 2103638568),
    'fail_92971175': (str((ROOT / 'research/agents/online/episode_92971175_opponent.py').resolve()), 847064548),
    'fail_92978681': (str((ROOT / 'research/agents/online/episode_92978681_opponent.py').resolve()), 453608024),
}
SEEDS = (27011, 27031, 27101, 27121)


def play(args):
    label, c, o, seed, seat = args
    from kaggle_environments import make
    agents = [c, o] if seat == 0 else [o, c]
    env = make('kaggriculture', configuration={'episodeSteps': 720, 'seed': seed}, debug=False)
    env.run(agents)
    f = env.steps[-1]
    mine = float(f[seat].reward or 0)
    theirs = float(f[1 - seat].reward or 0)
    return label, seed, seat, mine, mine - theirs


def main():
    tasks = []
    for s in SEEDS:
        for seat in (0, 1):
            tasks.append(('starter', CAND, 'starter', s, seat))
            tasks.append(('hamburger', CAND, OPPONENTS['hamburger'], s, seat))
            tasks.append(('head2head_v50', CAND, V50, s, seat))
    for name in ('fail_92967433', 'fail_92971175', 'fail_92978681'):
        o, seed = OPPONENTS[name]
        for seat in (0, 1):
            tasks.append((name, CAND, o, seed, seat))
    with ProcessPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(play, tasks))
    for label in ('starter', 'hamburger', 'fail_92967433', 'fail_92971175', 'fail_92978681', 'head2head_v50'):
        g = [x for x in rows if x[0] == label]
        print(f"{label}: {sum(x[4]>0 for x in g)}W-{sum(x[4]<0 for x in g)}L "
              f"mean_bank={statistics.mean(x[3] for x in g):.0f} "
              f"mean_margin={statistics.mean(x[4] for x in g):.0f} "
              f"worst_margin={min(x[4] for x in g):.0f} min_bank={min(x[3] for x in g):.0f}")


if __name__ == '__main__':
    main()
