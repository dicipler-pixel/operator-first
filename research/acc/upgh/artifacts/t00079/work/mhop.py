"""Masked exact hop: shortest route between two states using only the moves in MASK (list of ids), meet in the middle,
total-length cap. usage: mhop.py R0 R1 T0 T1 FWD BWD CAP MASK(comma ids)   Goal matched up to nothing (exact state)."""
import sys, os
sys.path.insert(0, os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools')
from verifier import core
E = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}; W = lambda s: tuple(E[c] for c in s)
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
r0, r1, t0, t1 = sys.argv[1:5]; fd, bd, cap = map(int, sys.argv[5:8])
MASK = [int(m) for m in sys.argv[8].split(',')] if len(sys.argv) > 8 else list(range(14))
start = (W(r0), W(r1)); T = (W(t0), W(t1)); ln = lambda s: len(s[0]) + len(s[1])
B = {T: []}; fr = [T]
for d in range(bd):
    nf = []
    for s in fr:
        for m in MASK:
            y = core.apply_move(s, m)
            if y in B or ln(y) > cap: continue
            B[y] = [INV[m]] + B[s]; nf.append(y)
    fr = nf
print('back states', len(B), file=sys.stderr)
F = {start: []}; fr = [start]
for d in range(fd + 1):
    hit = [F[s] + B[s] for s in fr if s in B]
    if hit:
        p = min(hit, key=len); s = start
        for m in p: s = core.apply_move(s, m)
        print('LEN', len(p), p, 'ok', s == T); break
    nf = []
    for s in fr:
        for m in MASK:
            y = core.apply_move(s, m)
            if y in F or ln(y) > cap: continue
            F[y] = F[s] + [m]; nf.append(y)
    fr = nf
    print('fwd depth', d + 1, 'states', len(F), file=sys.stderr)
else: print('NONE within', fd + bd)
