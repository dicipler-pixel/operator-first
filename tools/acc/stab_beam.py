#!/usr/bin/env python3
"""Stable beam with optional extra generators (stabilize up to rank RMAX). Compares rank 2 only vs rank <= RMAX
on the same row, same width. Every road is replayed on the official stable verifier.
usage: stab_beam.py CID W DMAX RMAX [LAMR]   (LAMR: priority cost per extra generator, default 0)"""
import sys, json, time
sys.path.insert(0, '/home/user/operator-first/tools/acc/upgh')
import symmetry_recog as SR
from verifier import stable_core as SC
CID = sys.argv[1]; W = int(sys.argv[2]); DMAX = int(sys.argv[3]); RMAX = int(sys.argv[4])
LAMR = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
ID = {}
for r in SC.MOVE_TABLE:
    c = r['category']
    if c == 'inversion': ID[('inv', r['relator'])] = r['id']
    elif c == 'multiplication': ID[('mul', r['relator'], r['other'], r['invert_other'])] = r['id']
    elif c == 'conjugation': ID[('conj', r['relator'], r['conjugator'])] = r['id']
    elif c == 'destabilize': ID[('des', r['relator'])] = r['id']
    elif c == 'stabilize': ID[('stab',)] = r['id']
# ac-r2-v1 ids 0..13 for rank-0/1 relators
ID[('inv', 0)] = 0; ID[('inv', 1)] = 1
ID[('mul', 0, 1, False)] = 2; ID[('mul', 0, 1, True)] = 3; ID[('mul', 1, 0, False)] = 4; ID[('mul', 1, 0, True)] = 5
for k in (0, 1):
    for j, g in enumerate((1, -1, 2, -2)): ID[('conj', k, g)] = 6 + 4 * k + j
def inv(w): return tuple(-c for c in reversed(w))
def mul(a, b):
    k = 0; la, lb = len(a), len(b)
    while k < la and k < lb and a[la - 1 - k] == -b[k]: k += 1
    return a[:la - k] + b[k:]
def conj(w, g): return mul(mul((g,), w), (-g,))
def children(s):
    k = len(s)
    for i in range(k):
        yield ID[('inv', i)], s[:i] + (inv(s[i]),) + s[i + 1:]
        for j in range(k):
            if j == i: continue
            for f in (False, True):
                yield ID[('mul', i, j, f)], s[:i] + (mul(s[i], inv(s[j]) if f else s[j]),) + s[i + 1:]
        for g in range(1, k + 1):
            for c in (g, -g):
                yield ID[('conj', i, c)], s[:i] + (conj(s[i], c),) + s[i + 1:]
        w = s[i]
        if len(w) == 1 and w[0] > 0 and not any(abs(a) == w[0] for j, o in enumerate(s) if j != i for a in o):
            gg = w[0]
            yield ID[('des', i)], tuple(tuple(a - 1 if a > gg else (a + 1 if a < -gg else a) for a in o) for j, o in enumerate(s) if j != i)
    if k < RMAX: yield ID[('stab',)], s + ((k + 1,),)
def prio(s): return sum(len(w) for w in s) + LAMR * max(0, len(s) - 2)
def run():
    s0 = tuple(tuple(w) for w in SR.CH[CID]['initial_relators'])
    nodes = [(-1, -1)]; cur = [(s0, 0)]; seen = {s0}; t0 = time.time(); maxr = 2
    for d in range(1, DMAX + 1):
        nxt = {}
        for s, nid in cur:
            for m, t in children(s):
                if t in seen or t in nxt: continue
                nxt[t] = (nid, m)
        if not nxt: break
        if () in nxt:
            pid, m = nxt[()]; path = [m]
            while pid > 0: pp, mm = nodes[pid]; path.append(mm); pid = pp
            return path[::-1], d, time.time() - t0, maxr
        items = sorted(nxt.items(), key=lambda kv: (prio(kv[0]), hash(kv[0])))[:W]
        cur = []
        for t, (pid, m) in items:
            seen.add(t); nodes.append((pid, m)); cur.append((t, len(nodes) - 1)); maxr = max(maxr, len(t))
        if d % 20 == 0:
            ls = [prio(t) for t, _ in items]; rk = sum(1 for t, _ in items if len(t) > 2)
            print(f'  d={d} len[{min(ls):.0f}..{max(ls):.0f}] states with extra generator {rk}/{len(items)} {time.time()-t0:.0f}s', file=sys.stderr, flush=True)
    return None, None, time.time() - t0, maxr
path, d, sec, maxr = run()
ok = bool(path) and SC.verify(SR.CH['s' + CID], path, 'sac-r8-v1', SR.LIM).get('ok')
print(json.dumps(dict(cid=CID, W=W, rmax=RMAX, lamr=LAMR, len=len(path) if ok else None, ok=ok, uses_stab=bool(path) and 14 in path,
                      sec=round(sec), path=path if ok else None)))
