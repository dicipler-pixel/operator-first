"""Foreign meet v2 (orows): like tools/acc/upgh/foreign_meet.py, but (a) the donor roads may end at (x,y) OR (y,x),
(b) the finish after relabelling goes to (x,y) for AC lines and to (x,y)+[16,15] or (y,x)+[15,15] for Stable lines,
(c) only the given target numbers are scanned, every road we hold for them (not just the best).
Every candidate is replayed on the official pinned cores. 0 API.
usage: python3 fm2.py OUT.json NUM [NUM ...]"""
import json, sys, gzip, time
from collections import deque
sys.path.insert(0, '/home/user/operator-first/tools/acc/upgh')
import twin_lookup as T
import symmetry_recog as SR
from verifier import stable_core
core = T.core
REPO = '/home/user/operator-first'
B = {}
for pfx in ('ac', 'stable_ac'):
    for x in json.load(gzip.open(f'{REPO}/research/acc/live/boards/{pfx}_20261014T0013Z.json.gz'))['data']['items']:
        B[x['challengeId']] = (x.get('currentBestLength'), x.get('kTeams'))
XY = ((1,), (2,)); YX = ((2,), (1,))
NEVER = {'09839', '02257', '09311', '06403', '04718', '05378'}
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
out, nums = sys.argv[1], sys.argv[2:]
t0 = time.time()
roads = {}
for cid, mv in SR.load_roads():
    if cid not in T.REL or cid[-5:] in NEVER or len(mv) > 150: continue
    s = T.REL[cid]
    try:
        for m in mv: s = core.apply_move(s, m)
    except Exception: continue
    if s in (XY, YX): roads.setdefault(cid, {})[tuple(mv)] = s
# index: up to 6 shortest roads per row
index = {}
ns = 0
for cid, rs in roads.items():
    for p in sorted(rs, key=len)[:6]:
        s = T.REL[cid]; seq = [s]
        for m in p: s = core.apply_move(s, m); seq.append(s)
        for j, sj in enumerate(seq[:-1]):
            if sum(map(len, sj)) > 48: continue
            ns += 1; k = T.key(sj); rem = len(p) - j
            lst = index.setdefault(k, [])
            if len(lst) < 4 or rem < max(x[0] for x in lst):
                lst.append((rem, cid, j, p)); lst.sort(key=lambda x: x[0]); del lst[4:]
print('roads rows %d, indexed states %d, keys %d, %.0fs' % (len(roads), ns, len(index), time.time() - t0), flush=True)
res = {}
for n in nums:
    cid = 'ac-' + n; sid = 'sac-' + n
    Ra = B[cid][0]; Rs = B[sid][0]
    mine = sorted(roads.get(cid, {}), key=len)[:40]
    bac = min((len(p) for p in mine if roads[cid][p] == XY), default=999)
    bs = min([len(p) + 2 for p in mine])
    best_ac = (bac, None); best_s = (bs, None)
    for p in mine:
        p = list(p); s = T.REL[cid]
        for i in range(len(p)):
            for rem, fcid, j, fp in index.get(T.key(s), []):
                if fcid == cid and fp == p: continue
                if i + rem >= max(best_ac[0], best_s[0]) + 4: continue
                t = T.REL[fcid]
                for m in fp[:j]: t = core.apply_move(t, m)
                for g in T.SYMS:
                    Tt = T.apply_g(g, t)
                    if tuple(T.ccanon(w) for w in Tt) != tuple(T.ccanon(w) for w in s): continue
                    pre = T.prefix_moves(s, Tt)
                    if pre is None: continue
                    body = [T.mmap(g, m) for m in fp[j:]]
                    e = s
                    for m in pre + body: e = core.apply_move(e, m)
                    base = p[:i] + pre + body
                    if len(base) >= max(best_ac[0], best_s[0]) + 2: continue
                    fx = fin(e, XY); fy = fin(e, YX)
                    if fx is not None:
                        c = base + fx
                        if len(c) < best_ac[0] and core.verify(T.CH[cid], c, 'ac-r2-v1', T.man['limits'])['ok']: best_ac = (len(c), c, fcid)
                        c2 = c + [16, 15]
                        if len(c2) < best_s[0] and stable_core.verify(T.CH[sid], c2, 'sac-r8-v1', T.man['limits'])['ok']: best_s = (len(c2), c2, fcid)
                    if fy is not None:
                        c2 = base + fy + [15, 15]
                        if len(c2) < best_s[0] and stable_core.verify(T.CH[sid], c2, 'sac-r8-v1', T.man['limits'])['ok']: best_s = (len(c2), c2, fcid)
            s = core.apply_move(s, p[i])
    res[n] = {'ac': best_ac, 'sac': best_s}
    print(json.dumps({'row': n, 'AC_rec': Ra, 'AC_have': bac, 'AC_fm': best_ac[0], 'AC_donor': best_ac[2] if len(best_ac) > 2 else None,
                      'SAC_rec': Rs, 'SAC_have': bs, 'SAC_fm': best_s[0], 'SAC_donor': best_s[2] if len(best_s) > 2 else None, 't': round(time.time() - t0)}), flush=True)
json.dump(res, open(out, 'w'))
