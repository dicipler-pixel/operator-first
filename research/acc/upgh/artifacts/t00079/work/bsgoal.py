"""r0-only BFS from (r0, MS(n)) to ANY BS(1,2)-form of r0 in a basis (y, y^p x y^q): cyclic words x y X Y^m X Y and
x Y X y^m X y, their inverses and rotations, |m|<=M.  usage: bsgoal.py N DEPTH CAP M"""
import sys, os
sys.path.insert(0, os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools')
from verifier import core
n, D, cap, M = map(int, sys.argv[1:5]); E = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}; W = lambda s: tuple(E[c] for c in s)
inv = lambda w: tuple(-a for a in reversed(w)); rots = lambda w: {w[i:] + w[:i] for i in range(len(w))}
def red(w):
    o = []
    for a in w:
        if o and o[-1] == -a: o.pop()
        else: o.append(a)
    return tuple(o)
G = set()
for m in range(-M, M + 1):
    for base in (W('xyX') + W('Y' * m if m >= 0 else 'y' * -m) + W('XY'), W('xYX') + W('y' * m if m >= 0 else 'Y' * -m) + W('Xy')):
        b = red(base)
        for w in (b, inv(b)): G |= rots(w)
ms = W('Y' * (n + 1) + 'X' + 'y' * n + 'x'); s0 = (W('YYYXXYx'), ms)
F = {s0: []}; fr = [s0]; MASK = (0, 2, 3, 6, 7, 8, 9)
for d in range(D + 1):
    hit = [F[s] for s in fr if s[0] in G]
    if hit: print(f'n={n} HIT depth {len(hit[0])} moves {hit[0]}'); break
    nf = []
    for s in fr:
        for mv in MASK:
            y = core.apply_move(s, mv)
            if y in F or len(y[0]) + len(y[1]) > cap: continue
            F[y] = F[s] + [mv]; nf.append(y)
    fr = nf
else: print(f'n={n} NONE within {D} (r0-only, cap {cap}, |m|<={M}, states {len(F)})')
