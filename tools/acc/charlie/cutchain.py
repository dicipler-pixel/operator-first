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

def key(st):
    a, b = st
    v = len(a); v = (v << 6) | len(b)
    for x in a: v = (v << 2) | CODE[x]
    for x in b: v = (v << 2) | CODE[x]
    return v << (2 * (58 - len(a) - len(b)))

class View:
    def __len__(self): return arr.shape[0]
    def __getitem__(self, i): return (int(arr[i, 1]) << 64) | int(arr[i, 0])
V = View()
def in_T16(st):
    if len(st[0]) + len(st[1]) > 16: return False
    k = key(st); i = bisect.bisect_left(V, k); return i < len(V) and V[i] == k

def chain(s0, maxsteps=12):
    st = s0; prefix = []
    for step in range(maxsteps + 1):
        if in_T16(st): return prefix, st
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
        prefix, st = r
        tail = [cr.INV[m] for m in reversed(cr.moves_to(T, cr.sstr(*st)))]
        path = prefix + tail
        v = core.verify(c, path, 'ac-r2-v1', LIM)
        if v.get('ok'):
            out.write('%s: %s\n' % (c['challenge_id'], json.dumps(path))); out.flush(); n += 1
    print('rows', lo, hi, 'verified lines', n)
