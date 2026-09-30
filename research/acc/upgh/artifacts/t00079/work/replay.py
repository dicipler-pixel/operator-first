"""Replay a move list on the pinned official core and print each state as words. usage: replay.py R0 R1 m1 m2 ..."""
import sys, os
sys.path.insert(0, os.environ.get('SAIR', '/root/.cache/upgh/sair') + '/competition/tools')
from verifier import core
E = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}
D = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
W = lambda s: tuple(E[c] for c in s)
S = lambda r: ''.join(D[a] for a in r) or '1'
r0, r1 = sys.argv[1], sys.argv[2]
moves = [int(m) for m in sys.argv[3:]]
s = (W(r0), W(r1))
print(f"{0:3d}  --  {S(s[0]):>30s} | {S(s[1]):<40s} len {len(s[0])+len(s[1])}")
for i, m in enumerate(moves, 1):
    s = core.apply_move(s, m)
    print(f"{i:3d}  {m:2d}  {S(s[0]):>30s} | {S(s[1]):<40s} len {len(s[0])+len(s[1])}")
print("DONE", sorted(map(S, s)) == ['x', 'y'] or S(s[0]) + ' ' + S(s[1]))
