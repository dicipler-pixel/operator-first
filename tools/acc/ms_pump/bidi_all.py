"""Exact balanced bidirectional search over ALL 14 moves (each has an inverse: 0,1 self; 2<->3; 4<->5; 6<->7; 8<->9; 10<->11; 12<->13).
State = (r0, r1) freely reduced; cap = total relator length. Forward from START, backward from (x, y).
Complete for "length <= BOUND with total <= CAP throughout" when df + db >= BOUND. Usage: bidi_all.py 'r0;r1' CAP BOUND  (words in xXyY)"""
import sys, time, json, os
from common import core
LIMIT = int(os.environ.get('LIMIT', '40000000'))
M = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}
r0s, r1s = sys.argv[1].split(';'); CAP, BOUND = int(sys.argv[2]), int(sys.argv[3])
st = (tuple(M[c] for c in r0s), tuple(M[c] for c in r1s)); tg = ((1,), (2,))
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
def enc(s): return bytes(g + 2 for g in s[0]) + b'\x09' + bytes(g + 2 for g in s[1])
def dec(b): a, c = b.split(b'\x09'); return (tuple(v - 2 for v in a), tuple(v - 2 for v in c))
t = time.time()
def log(*a): print(*a, '%.0fs' % (time.time() - t), flush=True)
def nbrs(b):
    s = dec(b)
    for m in range(14):
        v = core.apply_move(s, m)
        if len(v[0]) + len(v[1]) <= CAP and v[0] and v[1]: yield m, enc(v)
F = {enc(st): 0}; B = {enc(tg): 0}; ff = [enc(st)]; bf = [enc(tg)]; df = db = 0; best = None
if enc(st) in B: best = (0, enc(st))
while df + db < BOUND and best is None and len(F) + len(B) < LIMIT and ff and bf:
    if len(ff) <= len(bf):
        df += 1; n = []
        for w in ff:
            for m, v in nbrs(w):
                if v not in F:
                    F[v] = df; n.append(v)
                    if v in B and (best is None or df + B[v] < best[0]): best = (df + B[v], v)
        ff = n; log('F', df, len(ff), len(F))
    else:
        db += 1; n = []
        for w in bf:
            for m, v in nbrs(w):
                if v not in B:
                    B[v] = db; n.append(v)
                    if v in F and (best is None or F[v] + db < best[0]): best = (F[v] + db, v)
        bf = n; log('B', db, len(bf), len(B))
if best is None or best[0] > BOUND:
    log('RESULT NONE cap', CAP, 'df', df, 'db', db, 'bound', BOUND, 'complete' if df + db >= BOUND or not ff or not bf else 'SCOPED to %d' % (df + db)); sys.exit()
w = best[1]; d = F[w]; pre = []
while d > 0:
    for m, v in nbrs(w):
        if F.get(v) == d - 1: pre.append(INV[m]); w = v; d -= 1; break
pre.reverse(); w = best[1]; d = B[w]; suf = []
while d > 0:
    for m, v in nbrs(w):
        if B.get(v) == d - 1: suf.append(m); w = v; d -= 1; break
p = pre + suf; s = st
for m in p: s = core.apply_move(s, m)
log('RESULT len', len(p), 'ok', s == tg, 'cap', CAP); print('PATH', json.dumps(p).replace(' ', ''), flush=True)
