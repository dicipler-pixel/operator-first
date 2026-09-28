"""Stable AC fast peel: finish (x, y X^m) -> empty presentation in about 2k + 3m/k moves instead of m + 2.

Rank-2 AC must peel y X^m one x per move. Stable AC can add a generator g (relator g), turn it into
g X^k with k moves (x is already a relator), then swap each X^k block of r1 for one G:
  r1 <- r1 * (g X^k)^-1   (removes X^k, appends G)      then   conjugate r1 by G (moves the G to the front).
After the blocks: peel the rest of the x's, reduce r2 back to g, peel the G's, destabilize everything.
All moves are official sac-r8-v1 ids; every step is replayed with the official stable_core.
usage: python3 sac_fast_peel.py M [K]   (self-test on the state (x, y X^M))"""
import os, sys
sys.path.insert(0, os.environ.get('SAIR', 'SAIR') + '/competition/tools')
from verifier import stable_core as sc

ID = {}
for r in sc.MOVE_TABLE:
    c = r['category']
    if c == 'multiplication': ID[('mul', r['relator'], r['other'], r['invert_other'])] = r['id']
    elif c == 'conjugation': ID[('conj', r['relator'], r['conjugator'])] = r['id']
    elif c == 'inversion': ID[('inv', r['relator'])] = r['id']
    elif c == 'destabilize': ID[('destab', r['relator'])] = r['id']
    elif c == 'stabilize': ID[('stab',)] = r['id']

def best_k(m):
    return min(range(1, m + 1), key=lambda k: 2 * k + 3 * (m // k) + m % k) if m else 1

def tail(m, k=None):
    """Moves from the rank-2 state (x, y X^m) to the empty presentation."""
    if m <= 0: return [ID[('destab', 0)], ID[('destab', 0)]]
    k = k or best_k(m); q, rem = divmod(m, k)
    if 2 * k + 3 * q + rem + 5 >= m + 2:           # no gain: plain rank-2 peel
        return [ID[('mul', 1, 0, False)]] * m + [ID[('destab', 0)], ID[('destab', 0)]]
    mv = [ID[('stab',)]]                          # (x, y X^m, g)
    mv += [ID[('mul', 2, 0, True)]] * k           # r2 = g X^k
    for _ in range(q):                            # r1 = G^q y X^rem
        mv += [ID[('mul', 1, 2, True)], ID[('conj', 1, -3)]]
    mv += [ID[('mul', 1, 0, False)]] * rem        # r1 = G^q y
    mv += [ID[('mul', 2, 0, False)]] * k          # r2 = g
    mv += [ID[('conj', 1, 2)]]                    # r1 = y G^q
    mv += [ID[('mul', 1, 2, False)]] * q          # r1 = y
    mv += [ID[('destab', 2)], ID[('destab', 0)], ID[('destab', 0)]]
    return mv

def replay(state, moves):
    for i, m in enumerate(moves):
        state, why = sc.apply_move(state, m)
        if state is None: raise SystemExit(f'move {i} ({m}) not applicable: {why}')
    return state

if __name__ == '__main__':
    m = int(sys.argv[1]); k = int(sys.argv[2]) if len(sys.argv) > 2 else None
    mv = tail(m, k)
    end = replay(((1,), (2,) + (-1,) * m), mv)
    print(f'm={m} k={k or best_k(m)} fast tail {len(mv)} moves vs plain {m + 2}; ends at {end!r}')
