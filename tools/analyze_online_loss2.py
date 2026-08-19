"""Comparative per-player profile from an online replay: hires, plant, animal timing, sells by product/time, end state."""
import json, sys
from collections import Counter

def main(path):
    d = json.load(open(path, encoding='utf8'))
    steps = d['steps']
    names = [a['Name'] for a in d['info']['Agents']]
    print('rewards:', dict(zip(names, d['rewards'])))
    for pid in range(2):
        hi = []   # (step, qty)
        plant = []  # (step, crop)
        animal_buys = []
        sells = []  # (step, product, qty, price)
        buys = []
        last_money = None
        for st in steps:
            slot = st[pid]
            a = slot['action']
            stepno = slot['observation'].get('step', -1)
            if slot['observation'].get('day', 0) == 29 and slot['observation'].get('hour', 0) == 0:
                pass
            fm = a.get('farmer', [])
            if fm and fm[0] == 'PLANT':
                plant.append((stepno, fm[1] if len(fm) > 1 else '?'))
            elif fm and fm[0] == 'BUILD_PASTURE':
                pass
            for h in a.get('hands', []):
                if h and h[0] == 'PLANT':
                    plant.append((stepno, h[1] if len(h) > 1 else '?'))
            for m in a.get('market', []):
                if not isinstance(m, list) or not m:
                    continue
                op = m[0]
                if op == 'HIRE':
                    pass
                elif op == 'BUY_ANIMAL' and len(m) >= 3:
                    animal_buys.append((stepno, m[1], m[2]))
                elif op == 'BUY' and len(m) >= 3:
                    buys.append((stepno, m[1], m[2]))
                elif op == 'SELL' and len(m) >= 3:
                    sells.append((stepno, m[1], m[2]))
            if slot['observation'].get('private'):
                last_money = slot['observation']['private'].get('money', last_money)
        
        # summarize
        by_prod_sell = Counter(p for _, p, _ in sells)
        sell_phases = Counter()
        for step, prod, qty in sells:
            sell_phases[(step // 100) * 100] += 1
        plant_crops = Counter(c for _, c in plant)
        print('=' * 70)
        print(f'PLAYER {pid} = {names[pid]}')
        print('  sells total', len(sells), 'by product:', dict(by_prod_sell))
        print('  sell phases (step//100):', dict(sorted(sell_phases.items())))
        print('  plants:', dict(plant_crops), 'total', len(plant))
        print('  animal buys:', len(animal_buys))
        for s, an, q in animal_buys:
            print(f'    step {s}: {an} x{q}')
        if not animal_buys:
            print('    (no direct animal buys)')

if __name__ == '__main__':
    main(sys.argv[1])