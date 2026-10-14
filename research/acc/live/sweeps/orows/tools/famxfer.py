"""Family transfer with exact alignment: for target row T, step i on our road, and donor row U whose class meets T's road,
BFS (depth R, all 14 moves) from s_i to ANY exact image g(u_j) (16 symmetries) of the first J states u_j of U's held roads
(ending at (x,y) or (y,x)), then relabel U's remaining road by g and finish to (x,y) and to (y,x) by BFS (<= 6).
Candidates are replayed on the official cores.  usage: python3 famxfer.py R T:i:U[,U..] ..."""
import json, gzip, sys, time
from collections import deque
sys.path.insert(0, '/home/user/operator-first/tools/acc/upgh')
import twin_lookup as T, symmetry_recog as SR
from verifier import stable_core
core = T.core
XY = ((1,), (2,)); YX = ((2,), (1,))
S = '/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/orows'
A = json.load(open(S + '/all_ac_roads.json')); SA = json.load(open(S + '/all_sac_lines.json'))
Rr = int(sys.argv[1]); specs = sys.argv[2:]
need = set()
for sp in specs:
    need |= set(sp.split(':')[2].split(','))
roads = {}
for cid, mv in SR.load_roads():
    if cid[-5:] not in need: continue
    s = T.REL[cid]
    try:
        for m in mv: s = core.apply_move(s, m)
    except Exception: continue
    if s in (XY, YX): roads.setdefault(cid[-5:], set()).add(tuple(mv))
_f = {}
def fin(state, goal, limit=6):
    k = (state, goal)
    if k in _f: return _f[k]
    seen = {state: []}; q = deque([state]); r = None
    while q:
        s = q.popleft()
        if s == goal: r = seen[s]; break
        if len(seen[s]) < limit:
            for m in range(14):
                t = core.apply_move(s, m)
                if t not in seen and sum(map(len, t)) <= 10: seen[t] = seen[s] + [m]; q.append(t)
    _f[k] = r; return r
for sp in specs:
    tn, i, us = sp.split(':'); i = int(i); t0 = time.time()
    cid = 'ac-' + tn; sid = 'sac-' + tn
    mine = A.get(cid, [])[:3] + [l[:-2] for l in SA.get(sid, [])[:3] if all(m <= 13 for m in l[:-2])]
    targets = {}
    for un in us.split(','):
        for p in sorted(roads.get(un, []), key=len)[:8]:
            u = T.REL['ac-' + un]
            for j in range(min(12, len(p))):
                for g in T.SYMS:
                    gi = T.apply_g(g, u)
                    rem = len(p) - j
                    if gi not in targets or rem < targets[gi][0]: targets[gi] = (rem, un, g, list(p), j)
                u = core.apply_move(u, p[j])
    bestA = (min((len(p) for p in A.get(cid, [])), default=999), None); bestS = (min([len(l) for l in SA.get(sid, [])] + [bestA[0] + 2]), None)
    for road in mine:
        s = T.REL[cid]
        for m in road[:i]: s = core.apply_move(s, m)
        seen = {s: []}; fr = [s]
        for d in range(Rr + 1):
            for st in fr:
                if st in targets:
                    rem, un, g, p, j = targets[st]
                    body = [T.mmap(g, m) for m in p[j:]]
                    e = st
                    for m in body: e = core.apply_move(e, m)
                    base = list(road[:i]) + seen[st] + body
                    fx, fy = fin(e, XY), fin(e, YX)
                    if fx is not None:
                        c = base + fx
                        if len(c) < bestA[0] and core.verify(T.CH[cid], c, 'ac-r2-v1', T.man['limits'])['ok']: bestA = (len(c), c, un)
                        if len(c) + 2 < bestS[0] and stable_core.verify(T.CH[sid], c + [16, 15], 'sac-r8-v1', T.man['limits'])['ok']: bestS = (len(c) + 2, c + [16, 15], un)
                    if fy is not None:
                        c = base + fy + [15, 15]
                        if len(c) < bestS[0] and stable_core.verify(T.CH[sid], c, 'sac-r8-v1', T.man['limits'])['ok']: bestS = (len(c), c, un)
            if d == Rr: break
            nf = []
            for st in fr:
                for m in range(14):
                    y = core.apply_move(st, m)
                    if y not in seen: seen[y] = seen[st] + [m]; nf.append(y)
            fr = nf
    print(json.dumps({'T': tn, 'i': i, 'U': us, 'R': Rr, 'AC': bestA[0], 'AC_via': bestA[2] if len(bestA) > 2 else None, 'SAC': bestS[0],
                      'SAC_via': bestS[2] if len(bestS) > 2 else None, 'secs': round(time.time() - t0)}), flush=True)
    for nm, b in (('ac-' + tn, bestA), ('sac-' + tn, bestS)):
        if len(b) > 2: print('NEW', nm, b[0], json.dumps(b[1]), flush=True)
