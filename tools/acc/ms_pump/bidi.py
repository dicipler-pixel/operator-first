"""Balanced exact bidirectional search for the r1-only pump on MS(n, YXYXyx) rows (UPG-H 21:03Z job; song line
"The echo from the back is still talking to you"). r0 = YXYXyx fixed; r1-only moves {1,4,5,10..13}, invertible under free
reduction. Backward cost B[w] = min_k (k+7 + dist(w -> (xy)^k x)) over KSET (Fable's verified k+7 tail); forward F[w] = depth.
Always expands the smaller frontier. Complete for "total <= BOUND, r1 <= CAP throughout" once df + cb >= BOUND; otherwise stops at
LIMIT states and prints the scope actually covered (df, cb). Usage: KSET=9 LIMIT=40000000 bidi.py ROW CAP BOUND"""
import sys, os, time, json
from common import *
row, CAP, BOUND = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
KSET = [int(x) for x in os.environ.get('KSET', '9').split(',')]; LIMIT = int(os.environ.get('LIMIT', '40000000'))
m = json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in m['challenges']}
if row == 'ms3': st = (R0, (-2,-2,-2,-2,-1,2,2,2,1)); tgt = ((1,),(2,))
else: st = tuple(tuple(r) for r in C[row]['initial_relators']); tgt = tuple(tuple(r) for r in C[row]['target_relators'])
assert st[0] == R0
t = time.time()
enc = lambda w: bytes(g+2 for g in w)
dec = lambda b: tuple(c-2 for c in b)
def bmoves(b):
    for mv, v in moves(dec(b)): yield mv, enc(v)
def log(*a): print(*a, '%.0fs' % (time.time()-t), flush=True)
seeds = {}
for k in KSET:
    if len(xyk(k)) <= CAP: seeds.setdefault(k+7, set()).add(enc(xyk(k)))
S0 = min(seeds); B = {}; cb = S0 - 1; bfront = []; pending = {c: set(v) for c, v in seeds.items()}
F = {enc(st[1]): 0}; df = 0; ffront = [enc(st[1])]; best = None
def meet(w, total):
    global best
    if best is None or total < best[0]: best = (total, w); log('MEET total', total)
def bstep():
    global cb, bfront
    cb += 1; nxt = set(pending.pop(cb, ()))
    for w in bfront:
        for mv, v in bmoves(w):
            if len(v) <= CAP and v not in B: nxt.add(v)
    bfront = [w for w in nxt if w not in B]
    for w in bfront:
        B[w] = cb
        if w in F: meet(w, F[w] + cb)
    log('B cost', cb, 'layer', len(bfront), 'total', len(B))
def fstep():
    global df, ffront
    df += 1; nf = []
    for w in ffront:
        for mv, v in bmoves(w):
            if len(v) <= CAP and v not in F:
                F[v] = df; nf.append(v)
                if v in B: meet(v, df + B[v])
    ffront = nf; log('F depth', df, 'layer', len(ffront), 'total', len(F))
while cb < S0: bstep()   # first seed layer
if enc(st[1]) in B: meet(enc(st[1]), B[enc(st[1])])
while df + cb < BOUND:
    if best and best[0] <= df + cb: break
    if len(F) + len(B) > LIMIT: break
    if not ffront and not bfront: break
    # expand smaller frontier (backward bucket may still have pending seeds even if front empty)
    if (len(ffront) <= len(bfront) and ffront) or not (bfront or any(c > cb for c in pending)): fstep()
    else: bstep()
if best is None or best[0] > BOUND:
    done = df + cb >= BOUND or (not ffront)
    log('RESULT NONE' if done else 'RESULT SCOPED', row, 'cap', CAP, 'KSET', KSET, 'df', df, 'cb', cb, 'bound', BOUND,
        'complete' if done else 'covers totals <= %d only' % (df + cb))
    sys.exit()
w = best[1]; d = F[w]; pre = []
while d > 0:
    for mv, v in bmoves(w):
        if F.get(v) == d-1: pre.append(INVM[mv]); w = v; d -= 1; break
pre.reverse(); w = best[1]; suf = []
while True:
    c = B[w]; k = next((k for k in KSET if enc(xyk(k)) == w and k+7 == c), None)
    if k: suf += tail(k); break
    for mv, v in bmoves(w):
        if B.get(v) == c-1: suf.append(mv); w = v; break
path = pre + suf; s = st
for mv in path: s = core.apply_move(s, mv)
log('RESULT', row, 'len', len(path), 'ok', s == tgt, 'cap', CAP)
print('%s: %s' % (row, json.dumps(path).replace(' ', '')), flush=True)
