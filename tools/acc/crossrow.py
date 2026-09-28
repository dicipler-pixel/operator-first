"""Cross-row lookup with mirror twins.

Every state on every known path (to (x,y)) goes in an index with its remaining path. For each AC row,
states within RADIUS moves of its start are looked up under all 16 mirror transforms (signed
permutations of the letters x,y, optionally switching the two words). A mirror maps each official
move to another official move exactly. When the mirror moves the finish (e.g. to (y,x)), a short
fix path found by BFS is appended. Every candidate is replayed with the official verifier kernel
(verifier.core.verify) before it is reported.

usage: crossrow.py SAIR LIVE_AC.txt OUT.json PATHFILE... [--radius 2] [--train training_424.json]
PATHFILE: jsonl with {"id","ac"} (or {"id","path"}), or text with "ac-NNNNN: [..]" lines."""
import argparse, itertools, json, re, sys

ap = argparse.ArgumentParser(); ap.add_argument('sair'); ap.add_argument('live'); ap.add_argument('out')
ap.add_argument('files', nargs='+'); ap.add_argument('--radius', type=int, default=2)
ap.add_argument('--iradius', type=int, default=0, help='also index states this many moves off each known path')
ap.add_argument('--kmax', type=int, default=0, help='only rows held by <= kmax teams (0 = all)')
ap.add_argument('--train', help='SAIR examples/training_424.json: index its known paths too')
A = ap.parse_args()
sys.path.insert(0, A.sair + '/competition/tools'); from verifier import core
man = json.load(open(A.sair + '/competition/tools/verifier/data/manifest.json'))
C = {c['challenge_id']: c for c in man['challenges']}
live = {l.split()[0]: int(l.split()[1]) for l in open(A.live)}
kt = {l.split()[0]: int(l.split()[2]) for l in open(A.live) if len(l.split()) > 2}
GOAL = ((1,), (2,)); GENS = core.GENS

# ---- 16 mirrors: letter map (signed permutation of 1,2) + optional word switch ----
T = []
for perm in ((1, 2), (2, 1)):
    for s1, s2 in itertools.product((1, -1), repeat=2):
        lm = {1: s1 * perm[0], 2: s2 * perm[1]}; lm.update({-a: -b for a, b in list(lm.items())})
        for sw in (False, True): T.append((lm, sw))
def tstate(t, s):
    lm, sw = t; a = tuple(lm[x] for x in s[0]); b = tuple(lm[x] for x in s[1])
    return (b, a) if sw else (a, b)
def tmove(t, m):
    lm, sw = t
    if m in (0, 1): return (1 - m) if sw else m
    if 2 <= m <= 5: return {2: 4, 3: 5, 4: 2, 5: 3}[m] if sw else m
    base, g = (6, GENS[m - 6]) if m <= 9 else (10, GENS[m - 10])
    if sw: base = 16 - base
    return base + GENS.index(lm[g])
def inverse(t):
    probe = ((1, 2, -1), (2, 2, 1))
    for u in T:
        if tstate(u, tstate(t, probe)) == probe: return u
def fixpath(start, depth=8):  # BFS from start to GOAL
    if start == GOAL: return []
    prev = {start: None}; fr = [start]
    for _ in range(depth):
        nf = []
        for s in fr:
            for m in range(14):
                y = core.apply_move(s, m)
                if y in prev: continue
                prev[y] = (s, m); nf.append(y)
                if y == GOAL:
                    out = []; z = y
                    while prev[z]: z, mv = prev[z][0], prev[z][1]; out.append(mv)
                    return out[::-1]
        fr = nf
    return None
TI = [inverse(t) for t in T]; FIX = [fixpath(tstate(ti, GOAL)) for ti in TI]

# ---- load paths ----
paths = {}
def add(i, p):
    if i in C and isinstance(p, list) and p and (i not in paths or len(p) < len(paths[i])): paths[i] = p
for f in A.files:
    for l in open(f, errors='ignore'):
        l = l.strip()
        if l.startswith('{'):
            try: r = json.loads(l)
            except Exception: continue
            add(r.get('id'), r.get('ac') or r.get('path'))
        else:
            m = re.match(r'^(ac-\d{5}):\s*(\[[\d,\s]*\])', l)
            if m:
                try: add(m.group(1), json.loads(m.group(2)))
                except Exception: pass
idx = {}
for i, p in paths.items():
    s = tuple(map(tuple, C[i]['initial_relators'])); st = [s]
    for mv in p: s = core.apply_move(s, mv); st.append(s)
    if st[-1] != GOAL: continue
    for t, x in enumerate(st):
        rem = len(p) - t
        if x not in idx or idx[x][2] > rem: idx[x] = (i, t, rem, ())
if A.train:  # training instances are not scored rows; their states can still carry a finish
    for t in json.load(open(A.train))['instances']:
        k = 'T:' + t['training_id']; s = tuple(map(tuple, t['initial_relators'])); st = [s]; p = t['moves']
        for mv in p: s = core.apply_move(s, mv); st.append(s)
        if st[-1] != GOAL: continue
        paths[k] = p
        for u, x in enumerate(st):
            if x not in idx or idx[x][2] > len(p) - u: idx[x] = (k, u, len(p) - u, ())
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)  # each official move's inverse
for _ in range(A.iradius):
    add_ = {}
    for x, (i, t, rem, back) in idx.items():
        for m in range(14):
            y = core.apply_move(x, m)
            if y in idx or (y in add_ and add_[y][2] <= rem + 1): continue
            add_[y] = (i, t, rem + 1, (INV[m],) + back)
    idx.update(add_)
print('paths', len(paths), 'indexed states', len(idx), flush=True)

# ---- lookup ----
best = {}
for j, c in C.items():
    if not j.startswith('ac-'): continue
    if A.kmax and not (0 < kt.get(j, 0) <= A.kmax): continue
    s0 = tuple(map(tuple, c['initial_relators'])); front = {s0: []}; seen = {s0}
    for d in range(A.radius + 1):
        for x, pre in front.items():
            for k, t in enumerate(T):
                hit = idx.get(tstate(t, x))
                if not hit or FIX[k] is None: continue
                i, t0, rem, back = hit
                if len(pre) + rem + len(FIX[k]) >= best.get(j, (10 ** 9,))[0]: continue
                cand = pre + [tmove(TI[k], m) for m in list(back) + paths[i][t0:]] + FIX[k]
                if core.verify(c, cand, 'ac-r2-v1', man['limits'])['ok']:
                    best[j] = (len(cand), cand, i, k, len(pre))
        if d == A.radius: break
        nf = {}
        for x, pre in front.items():
            for m in range(14):
                y = core.apply_move(x, m)
                if y not in seen: seen.add(y); nf[y] = pre + [m]
        front = nf
res = []
for j, (n, cand, src, k, pre) in best.items():
    own = len(paths[j]) if j in paths else None
    res.append({'id': j, 'len': n, 'live': live.get(j, 0), 'own': own, 'src': src, 'mirror': k, 'pre': pre, 'ac': cand})
res.sort(key=lambda r: (r['len'] - r['live'] if r['live'] else -999))
json.dump(res, open(A.out, 'w'))
better = [r for r in res if r['own'] is None or r['len'] < r['own']]
print('rows with a verified borrowed path:', len(res), '| shorter than our own path or new:', len(better))
for r in res[:20]:
    print(r['id'], r['len'], 'live', r['live'], 'own', r['own'], 'via', r['src'], 'mirror', r['mirror'], 'pre', r['pre'])
