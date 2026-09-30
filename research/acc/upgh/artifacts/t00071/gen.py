"""Generator path(n) for MS(n, YXXyx) = (YXXyx, Y^(n+1) X y^n x), built from Git's W100k n=4 route shape.
Level forms (r0 = BS = YXXyx throughout the pumps):
  F1(k,a) = x^a Y^k X y^(k-1) x          pump P1 = 5 (11 5)^a 12         -> F2(k-1, 2a+1)   (2a+2 moves)
  F2(k,a) = Y^k X y^(k-1) x^(a+1)         pump P2 = 1 (4 10)^a 1 5 12 10  -> F1(k-1, 2a+1)   (2a+5 moves)
Stage A = 5 7 12 5 6 5 12 : MS_n -> F2(n-1, 3)   (checked by replay for each n)
Level 1: F2(1,a) = Y x^a ; collapse 6 1 3 10 4 -> (x Y x^(a-2), X); strip 2^(a-2) 4 1 2.
"""
import os, sys, json
sys.path.insert(0, os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools')
from verifier import core, stable_core as sc

E = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}; L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def W(s): return tuple(E[c] for c in s)
def S(w): return ''.join(L[a] for a in w)
BS = W('YXXyx')
def MS(n): return (BS, W('Y' * (n + 1) + 'X' + 'y' * n + 'x'))
def F1(k, a): return core.free_reduce(W('x' * a + 'Y' * k + 'X' + 'y' * (k - 1) + 'x'))
def F2(k, a): return core.free_reduce(W('Y' * k + 'X' + 'y' * (k - 1) + 'x' * (a + 1)))

def replay(state, moves):
    for m in moves: state = core.apply_move(state, m)
    return state

A = [5, 7, 12, 5, 6, 5, 12]
def P1(a): return [5] + [11, 5] * a + [12]
def P2(a): return [1] + [4, 10] * a + [1, 5, 12, 10]
COLLAPSE = [6, 2, 10, 1, 4]        # Git seed-11 AC collapse: (BS, Y x^a) -> (x Y x^(a-2), X)
COLLAPSE_SAC = [6, 2, 7, 5, 12]    # Git SAC-56 collapse:     (BS, Y x^a) -> (Y x^(a-1), x)

def prefix(n):
    """moves from MS(n) to the level-1 state (BS, Y x^(2^n-1)) = F2(1, 2^n-1); asserts each level form."""
    st = MS(n); mv = list(A); st = replay(st, mv)
    k, a, form = n - 1, 3, 2
    assert st[1] == F2(k, a), (S(st[1]), S(F2(k, a)))
    while k > 1:
        if form == 2: p = P2(a); form = 1
        else: p = P1(a); form = 2
        mv += p; st = replay(st, p); k, a = k - 1, 2 * a + 1
        exp = F1(k, a) if form == 1 else F2(k, a)
        assert st[0] == BS and st[1] == exp, (n, k, a, form, S(st[1]), S(exp))
    if form == 1:            # F1(1,a) = x^a Y ; rotate to F2(1,a) = Y x^a costs... use 12? y x^a Y y = y x^a  no.
        # F1(1,a) = x^a Y. inverse = y X^a. We handle both forms in collapse().
        pass
    return mv, st, form, a

def collapse_strip(st, form, a):
    """from level 1 to (x, y) (AC target). Returns moves, and the index where the strip starts + pre-strip state."""
    if form == 2:   # (BS, Y x^a)
        mv = list(COLLAPSE)
    else:           # (BS, x^a Y): 13 = Y x^a Y y = Y x^a -> F2(1,a), then the same collapse
        mv = [13] + list(COLLAPSE)
    st2 = replay(st, mv)
    r0, r1 = st2
    assert r1 == (-1,) and r0[:2] == (1, -2) and set(r0[2:]) == {1}, (S(r0), S(r1))
    p = len(r0) - 2
    strip = [2] * p + [4, 1, 2]
    return mv, st2, p, strip

def ac_path(n):
    mv, st, form, a = prefix(n)
    cmv, st2, p, strip = collapse_strip(st, form, a)
    full = mv + cmv + strip
    end = replay(MS(n), full)
    assert end == ((1,), (2,)), end
    return full, {'A': len(A), 'prefix_to_level1': len(mv), 'collapse': len(cmv), 'p': p, 'strip': len(strip), 'total': len(full)}

# ---------- Stable AC tail from the pre-strip state (r0 = x Y x^p, r1 = X) ----------
ID = {}
for r in sc.MOVE_TABLE:
    c = r['category']
    if c == 'multiplication': ID[('mul', r['relator'], r['other'], r['invert_other'])] = r['id']
    elif c == 'conjugation': ID[('conj', r['relator'], r['conjugator'])] = r['id']
    elif c == 'inversion': ID[('inv', r['relator'])] = r['id']
    elif c == 'destabilize': ID[('destab', r['relator'])] = r['id']
    elif c == 'stabilize': ID[('stab',)] = r['id']

def fast_tail_prestrip(p, k):
    """(x Y x^p, X) -> () in Stable AC using one extra generator g with r2 = g x^k."""
    q, rem = divmod(p, k)
    mv = [ID[('inv', 1)]]                      # (xYx^p, x)
    mv += [ID[('stab',)]]                      # r2 = g
    mv += [ID[('mul', 2, 1, False)]] * k       # r2 = g x^k
    for _ in range(q):
        mv += [ID[('mul', 0, 2, True)], ID[('conj', 0, -3)]]   # r0 = G^j x Y x^(p-jk)
    mv += [ID[('mul', 0, 1, True)]] * rem      # r0 = G^q x Y
    mv += [ID[('mul', 2, 1, True)]] * k        # r2 = g
    mv += [ID[('inv', 0)]]                     # r0 = y X g^q
    mv += [ID[('mul', 0, 2, True)]] * q        # r0 = y X
    mv += [ID[('mul', 0, 1, False)]]           # r0 = y
    mv += [ID[('destab', 2)], ID[('destab', 0)], ID[('destab', 0)]]
    return mv

def fast_tail_git(p, k):
    """(Y x^p, x) -> () in Stable AC (Git SAC collapse landing state), helper r2 = g x^k."""
    q, rem = divmod(p, k)
    mv = [ID[('stab',)]]                       # r2 = g
    mv += [ID[('mul', 2, 1, False)]] * k       # r2 = g x^k
    for _ in range(q):
        mv += [ID[('mul', 0, 2, True)], ID[('conj', 0, -3)]]   # r0 = G^j Y x^(p-jk)
    mv += [ID[('mul', 0, 1, True)]] * rem      # r0 = G^q Y
    mv += [ID[('mul', 2, 1, True)]] * k        # r2 = g
    mv += [ID[('conj', 0, -2)]]                # r0 = Y G^q
    mv += [ID[('mul', 0, 2, False)]] * q       # r0 = Y
    mv += [ID[('inv', 0)]]                     # r0 = y
    mv += [ID[('destab', 2)], ID[('destab', 0)], ID[('destab', 0)]]
    return mv

def plain_tail_git(p):
    return [3] * p + [0, 15, 15]

def plain_tail_prestrip(p):
    return [2] * p + [4, 1, 2] + [ID[('destab', 0)], ID[('destab', 0)]]

def sreplay(state, moves):
    for i, m in enumerate(moves):
        state, why = sc.apply_move(state, m)
        if state is None: raise SystemExit(f'move {i} ({m}) not applicable: {why}')
    return state

def sac_path(n):
    mv, st, form, a = prefix(n)
    cands = []
    # variant 1: my collapse to (x Y x^p, X), mirrored fast tail
    cmv, st2, p, strip = collapse_strip(st, form, a)
    for k in range(1, p + 1): cands.append(('v1', k, p, cmv + fast_tail_prestrip(p, k)))
    cands.append(('v1plain', 0, p, cmv + plain_tail_prestrip(p)))
    # variant 2: Git SAC collapse to (Y x^(a-1), x), fast tail there
    cmv2 = ([13] if form == 1 else []) + list(COLLAPSE_SAC)
    st3 = replay(st, cmv2); p2 = len(st3[0]) - 1
    assert st3[1] == (1,) and st3[0][0] == -2 and set(st3[0][1:]) == {1}, st3
    for k in range(1, p2 + 1): cands.append(('v2', k, p2, cmv2 + fast_tail_git(p2, k)))
    cands.append(('v2plain', 0, p2, cmv2 + plain_tail_git(p2)))
    best = min(cands, key=lambda c: len(c[3]))
    full = mv + best[3]
    end = sreplay(MS(n), full)
    assert end == (), end
    return full, {'prefix_to_level1': len(mv), 'variant': best[0], 'p': best[2], 'k': best[1], 'collapse+tail': len(best[3]), 'total': len(full)}

if __name__ == '__main__':
    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        ac, info = ac_path(n); sac, sinfo = sac_path(n)
        print(n, 'AC', info, 'SAC', sinfo)
