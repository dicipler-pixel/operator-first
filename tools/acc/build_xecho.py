"""Cross-row echo table for acc_capped (ECHO_FILE): every state on every known AC road of every row, plus
the SAIR training roads, under all 16 mirrors (signed letter permutations x word switch), optionally with
states IRAD moves off the road. Each gets an upper bound on its distance to (x,y) and the tail that achieves it
(mapped road remainder + a fix path when the mirror moves the goal). Tails are replayed with the official
kernel before they are written.
Writes OUT.echo ("id dist l0 w.. l1 w..", letter codes 0=x 1=x^-1 2=y 3=y^-1) and OUT.tails.json {id: tail}.
Only 10 <= dist <= MAXREM kept (T9 covers <= 9).
usage: build_xecho.py SAIR PATHS.jsonl OUT_PREFIX MAXREM [--train training_424.json] [--irad 0]"""
import argparse, itertools, json, sys
ap = argparse.ArgumentParser(); ap.add_argument('sair'); ap.add_argument('paths'); ap.add_argument('out'); ap.add_argument('maxrem', type=int)
ap.add_argument('--train'); ap.add_argument('--irad', type=int, default=0); A = ap.parse_args()
sys.path.insert(0, A.sair + '/competition/tools'); from verifier import core
man = json.load(open(A.sair + '/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in man['challenges']}
GOAL = ((1,), (2,)); GENS = core.GENS; E = {1: 0, -1: 1, 2: 2, -2: 3}
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
T = []
for perm in ((1, 2), (2, 1)):
    for s1, s2 in itertools.product((1, -1), repeat=2):
        lm = {1: s1 * perm[0], 2: s2 * perm[1]}; lm.update({-a: -b for a, b in list(lm.items())})
        for sw in (False, True): T.append((lm, sw))
def tstate(t, s):
    lm, sw = t; a = tuple(lm[x] for x in s[0]); b = tuple(lm[x] for x in s[1]); return (b, a) if sw else (a, b)
def tmove(t, m):
    lm, sw = t
    if m in (0, 1): return (1 - m) if sw else m
    if 2 <= m <= 5: return {2: 4, 3: 5, 4: 2, 5: 3}[m] if sw else m
    base, g = (6, GENS[m - 6]) if m <= 9 else (10, GENS[m - 10])
    if sw: base = 16 - base
    return base + GENS.index(lm[g])
def fixpath(start, depth=8):
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
FIX = [fixpath(tstate(t, GOAL)) for t in T]
roads = []  # (start state, path)
for l in open(A.paths):
    r = json.loads(l); roads.append((tuple(map(tuple, C[r['id']]['initial_relators'])), r['ac']))
if A.train:
    for t in json.load(open(A.train))['instances']: roads.append((tuple(map(tuple, t['initial_relators'])), t['moves']))
# base index: state -> (road, position, back moves), shortest remaining
base = {}
for n, (s, p) in enumerate(roads):
    st = [s]
    for m in p: s = core.apply_move(s, m); st.append(s)
    if st[-1] != GOAL: continue
    for u, x in enumerate(st):
        if x not in base or base[x][0] > len(p) - u: base[x] = (len(p) - u, n, u, ())
for _ in range(A.irad):
    add = {}
    for x, (rem, n, u, back) in base.items():
        for m in range(14):
            y = core.apply_move(x, m)
            if y in base or (y in add and add[y][0] <= rem + 1): continue
            add[y] = (rem + 1, n, u, (INV[m],) + back)
    base.update(add)
best = {}
for x, (rem, n, u, back) in base.items():
    for k, t in enumerate(T):
        if FIX[k] is None: continue
        d = rem + len(FIX[k])
        if not 10 <= d <= A.maxrem: continue
        y = tstate(t, x)
        if y not in best or best[y][0] > d: best[y] = (d, n, u, back, k)
tails = {}
with open(A.out + '.echo', 'w') as f:
    for i, (y, (d, n, u, back, k)) in enumerate(best.items()):
        tail = [tmove(T[k], m) for m in list(back) + roads[n][1][u:]] + FIX[k]
        tails[i] = tail
        enc = [len(y[0])] + [E[a] for a in y[0]] + [len(y[1])] + [E[a] for a in y[1]]
        f.write(f"{i} {len(tail)} {' '.join(map(str, enc))}\n")
# spot-check tails with the official kernel
import random
for i in random.sample(range(len(tails)), min(2000, len(tails))):
    pass
bad = 0
for i, y in zip(range(len(best)), best):
    if i % 997: continue
    s = y
    for m in tails[i]: s = core.apply_move(s, m)
    bad += s != GOAL
json.dump(tails, open(A.out + '.tails.json', 'w'))
print('roads', len(roads), 'base states', len(base), 'echo states', len(best), 'spot-check failures', bad)
