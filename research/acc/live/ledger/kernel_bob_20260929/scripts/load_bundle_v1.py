# SCRIPT: BOB-LOAD-BUNDLE-01
# Parse BOB_blocks_bundle_compact_20260928.txt, rebuild the 1,619-block library by the
# header recipe, replay every NEAR path (and REC path) with the official core.
import sys, json
from collections import Counter
sys.path.insert(0, '/home/claude/sair/competition/tools')
from verifier.core import apply_move, free_reduce
L = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}
def rel(s): return tuple(L[c] for c in s)
def hexp(s): return [int(c, 16) for c in s]
near, rec = [], []
for line in open('/home/claude/bob_splice/bundle_compact.txt'):
    t = line.split()
    if not t: continue
    if t[0] == 'NEAR':
        near.append(dict(id=t[1], record=int(t[2]), teams=int(t[3]), ours=int(t[4]), rel=[rel(t[5]), rel(t[6])], path=hexp(t[7])))
    elif t[0] == 'REC':
        rec.append(dict(id=t[1], path=hexp(t[2])))
c = Counter()
for r in rec:
    p = r['path']
    for k in range(3, 11):
        for i in range(len(p) - k + 1): c[tuple(p[i:i + k])] += 1
lib = [b for b, n in c.items() if n >= 3]
def replay(R, p):
    s = (free_reduce(R[0]), free_reduce(R[1]))
    for m in p: s = apply_move(s, m)
    return s == ((1,), (2,))
if __name__ == '__main__':
    print('library blocks', len(lib))
    bad = [n['id'] for n in near if not replay(n['rel'], n['path']) or len(n['path']) != n['ours']]
    print('near misses', len(near), 'bad replays/lengths', bad)
