"""Extract per-player action timeline from an online replay for counterfactual analysis.

Usage: python tools/analyze_online_loss.py <replay.json>
Prints: buys/sells/hires/plant/action counts, animal timing, end-state inventories.
"""
import json, sys
from collections import Counter, defaultdict

def main(path):
    d = json.load(open(path, encoding='utf8'))
    steps = d['steps']
    nsteps = len(steps)
    names = [a['Name'] for a in d['info']['Agents']]
    print('rewards:', dict(zip(names, d['rewards'])))
    # per-player action timeline
    for pid in range(2):
        acts = defaultdict(list)  # kind -> list of (step, payload)
        animal_buys = []  # (step, animal, qty)
        sells = []
        hires = []
        actions_total = 0
        for st in steps:
            slot = st[pid]
            a = slot['action']
            stepno = slot['observation'].get('step', -1) if isinstance(slot.get('observation'), dict) else -1
            farmer = a.get('farmer', [])
            if farmer and farmer[0] != 'PASS':
                acts[farmer[0]].append((stepno, farmer))
            for h in a.get('hands', []):
                acts['HAND:' + h[0]].append((stepno, h))
            for m in a.get('market', []):
                if not isinstance(m, list) or not m:
                    continue
                acts['MARKET:' + m[0]].append((stepno, m))
                if m[0] == 'BUY_ANIMAL' and len(m) >= 3:
                    animal_buys.append((stepno, m[1], m[2]))
                if m[0] == 'SELL' and len(m) >= 3:
                    sells.append((stepno, m[1], m[2]))
        print('=' * 70)
        print(f'PLAYER {pid} ({names[pid]})')
        print('total steps', nsteps, 'last reward', d['rewards'][pid])
        print('action counts:', dict(acts))
        # animal buys
        print('BUY_ANIMAL count:', len(animal_buys))
        if animal_buys:
            for s, animal, qty in animal_buys[:25]:
                print(f'  step {s}: {animal} x{qty}')
        # sells
        print('SELL count:', len(sells))

if __name__ == '__main__':
    main(sys.argv[1])