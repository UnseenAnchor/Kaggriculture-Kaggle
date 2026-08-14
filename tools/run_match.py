"""Seeded match runner: reproducible W/L/T + bank stats across seeds and seats."""
import sys, statistics
from kaggle_environments import make

def run(agent_path, opponent="starter", seeds=(27011, 27031, 27101, 27121), verbose=True):
    results = []
    for seed in seeds:
        for seat in (0, 1):
            agents = [agent_path, opponent] if seat == 0 else [opponent, agent_path]
            env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
            env.run(agents)
            final = env.steps[-1]
            mine, theirs = final[seat].reward, final[1 - seat].reward
            outcome = "W" if mine > theirs else ("L" if mine < theirs else "T")
            results.append((seed, seat, mine, theirs, outcome))
            if verbose:
                print(f"seed={seed} seat={seat}: me={mine:7.0f} opp={theirs:7.0f} -> {outcome}")
    wins = sum(1 for r in results if r[4] == "W")
    losses = sum(1 for r in results if r[4] == "L")
    ties = sum(1 for r in results if r[4] == "T")
    banks = [r[2] for r in results]
    print(f"=== vs {opponent}: {wins}W-{losses}L-{ties}T | "
          f"mean {statistics.mean(banks):.0f} (min {min(banks):.0f}, max {max(banks):.0f}) ===")
    return results

if __name__ == "__main__":
    agent = sys.argv[1] if len(sys.argv) > 1 else "agents/main.py"
    opp = sys.argv[2] if len(sys.argv) > 2 else "starter"
    seeds = tuple(int(s) for s in sys.argv[3].split(",")) if len(sys.argv) > 3 else (27011, 27031, 27101, 27121)
    run(agent, opp, seeds)
