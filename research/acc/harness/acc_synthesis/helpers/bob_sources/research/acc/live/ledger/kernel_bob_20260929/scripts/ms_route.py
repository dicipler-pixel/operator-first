# SCRIPT: KERNEL-MS-ROUTE-01
# Search in Miller-Schupp coordinates and pull the path back.
# psi = automorphism with psi(row) = MS-form state S0. A move sequence on S pulls back to
# the row: inversions/multiplications unchanged; conjugation by generator g becomes
# conjugation by the word psi^-1(g), i.e. single-letter conjugations applied last letter
# first. End state ((1,),(2,)) in S pulls back to (psi^-1(x), psi^-1(y)); a BFS finisher
# on the row side then reaches ((1,),(2,)). Official core replays the final line.
import json, sys, itertools
from collections import deque
sys.path.insert(0, '/home/claude/sair/competition/tools')
from verifier.core import apply_move, free_reduce
from ms_detect import red, inv, sub, words
from drive import solve, run
T = ((1,), (2,))
def inverse_auto(a, b):
    img = {1: a, 2: b}
    cand = [w for L in range(1, 5) for w in itertools.product([1, -1, 2, -2], repeat=L) if red(list(w)) == list(w)]
    u = next(list(w) for w in cand if sub(list(w), img) == [1])
    v = next(list(w) for w in cand if sub(list(w), img) == [2])
    return u, v
CONJ = {(0, 1): 6, (0, -1): 7, (0, 2): 8, (0, -2): 9, (1, 1): 10, (1, -1): 11, (1, 2): 12, (1, -2): 13}
GEN = {6: 1, 7: -1, 8: 2, 9: -2, 10: 1, 11: -1, 12: 2, 13: -2}
def pull_back(path, pinv):
    out = []
    for m in path:
        if m < 6: out.append(m); continue
        rel = 0 if m <= 9 else 1
        g = GEN[m]
        word = pinv[abs(g)] if g > 0 else inv(pinv[abs(g)])
        for letter in reversed(word): out.append(CONJ[(rel, letter)])
    return out
def finish_bfs(s, maxd=10, cap=6):
    q = deque([(s, [])]); seen = {s}
    while q:
        u, p = q.popleft()
        if u == T: return p
        if len(p) >= maxd: continue
        for m in range(14):
            v = apply_move(u, m)
            if len(v[0]) + len(v[1]) <= cap and v not in seen:
                seen.add(v); q.append((v, p + [m]))
    return None
def route(row, auto, W, D, L, mode, timeout):
    a, b = auto
    img = {1: a, 2: b}
    S0 = [sub(row['rel'][0], img), sub(row['rel'][1], img)]
    pS, st, sec = solve(S0, W, D, L, 1, mode, timeout)   # pS ends at ((1,),(2,)) in S coords
    if pS is None: return None, st, sec
    u, v = inverse_auto(a, b)
    pR = pull_back(pS, {1: u, 2: v})
    s0 = (free_reduce(tuple(row['rel'][0])), free_reduce(tuple(row['rel'][1])))
    e = run(s0, pR)
    f = finish_bfs(e, maxd=12, cap=2 + len(u) + len(v) + 2)
    if f is None: return None, 'nofinish %s' % (e,), sec
    return pR + f, 'ok', sec
if __name__ == '__main__':
    rows = {r['id']: r for r in json.load(open('rows_101_213.json'))}
    det = {d['id']: d for d in json.load(open('ms_detect.json'))}
    for cid in sys.argv[1:]:
        p, st, sec = route(rows[cid], det[cid]['auto'], 20000, 300, 80, 0, 900)
        ok = p is not None and run((free_reduce(tuple(rows[cid]['rel'][0])), free_reduce(tuple(rows[cid]['rel'][1]))), p) == T
        print(cid, st, round(sec, 1), len(p) if p else None, 'VERIFIED' if ok else '', p if ok else '')
