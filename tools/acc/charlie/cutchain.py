# SCRIPT: CHARLIE_CUTCHAIN -- the rotate-and-cut pattern repeated, then a lookup in T16.
# For each pool row: apply the cheapest cut that lowers the total, repeat while it keeps lowering;
# after every step look the exact state up in T16 (the closed component of ((x),(y)) under cap 16,
# 129,247,304 states, sorted on disk). A hit gives a complete path:
#   cut prefix + (moves from the state to the trivial, read back from the T16 layers).
# Every path is replayed by the official verifier; only accepted lines are written.
# Lookups use the same 128-bit key as acc_disk (len0 6b, len1 6b, letters 2b each, left aligned).
import json, os, sys, bisect, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cutfirst, charlie_run as cr
core = cr.core
T = os.path.join(HERE, 'runs', 'T16'); U = os.path.join(T, 'union.bin')
CODE = {1: 0, -1: 1, 2: 2, -2: 3}
arr = np.memmap(U, dtype=np.uint64, mode='r').reshape(-1, 2)   # little endian: [lo, hi]
B = os.path.join(HERE, 'runs', 'B36'); barr = np.memmap(os.path.join(B, 'union9.bin'), dtype=np.uint64, mode='r').reshape(-1, 2)

def key(st):
    a, b = st
    v = len(a); v = (v << 6) | len(b)
    for x in a: v = (v << 2) | CODE[x]
    for x in b: v = (v << 2) | CODE[x]
    return v << (2 * (58 - len(a) - len(b)))

class View:
    def __init__(self, a): self.a = a
    def __len__(self): return self.a.shape[0]
    def __getitem__(self, i): return (int(self.a[i, 1]) << 64) | int(self.a[i, 0])
V = View(arr); VB = View(barr)
def has(view, st):
    k = key(st); i = bisect.bisect_left(view, k); return i < len(view) and view[i] == k
def in_T16(st):
    if len(st[0]) + len(st[1]) <= 16 and has(V, st): return T
    if len(st[0]) + len(st[1]) <= 36 and has(VB, st): return B
    return None

def chain(s0, maxsteps=12):
    st = s0; prefix = []
    for step in range(maxsteps + 1):
        d = in_T16(st)
        if d: return prefix, st, d
        cs = cutfirst.cuts(st)
        if not cs or cs[0][0] >= len(st[0]) + len(st[1]): return None
        t, cost, pre, st = cs[0]; prefix = prefix + pre
    return None

if __name__ == '__main__':
    M = json.load(open(os.path.join(cr.SAIR, 'verifier/data/manifest.json'))); LIM = M['limits']
    rows = [c for c in M['challenges'] if c['challenge_id'].startswith('ac-')]
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    out = open(os.path.join(HERE, 'runs', 'cutchain_lines_%d_%d.txt' % (lo, hi)), 'w'); n = 0
    for c in rows[lo:hi]:
        s0 = tuple(map(tuple, c['initial_relators'])); r = chain(s0)
        if not r: continue
        prefix, st, d = r
        tail = [cr.INV[m] for m in reversed(cr.moves_to(d, cr.sstr(*st)))]
        path = prefix + tail
        v = core.verify(c, path, 'ac-r2-v1', LIM)
        if v.get('ok'):
            out.write('%s: %s\n' % (c['challenge_id'], json.dumps(path))); out.flush(); n += 1
    print('rows', lo, hi, 'verified lines', n)
