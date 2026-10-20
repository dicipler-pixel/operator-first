#!/usr/bin/env python3
"""Bob/Cass method on our rows: many same-length reorderings of a road (swap neighbouring moves only where both orders
reach the identical state), then one BFS inside the tube = all states within radius R of any reordered road.
Reports the shortest AC road to (x,y) and the shortest route to (y,x) (+[15,15] for Stable) inside the tube.
usage: reorder_tube.py CID ROAD_JSON_FILE NVAR R"""
import sys, json, random, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core
cid, rf, NV, R = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
road = json.load(open(rf)); ap = core.apply_move; rnd = random.Random(7)
s0 = tuple(tuple(x) for x in SR.CH[cid]["initial_relators"]); XY, YX = ((1,), (2,)), ((2,), (1,))
def states(p):
    st = [s0]
    for m in p: st.append(ap(st[-1], m))
    return st
t0 = time.time(); variants = {tuple(road)}; nodes = set(states(road))
for v in range(NV):
    p = list(rnd.choice(sorted(variants))); st = states(p)
    for _ in range(3 * len(p)):
        i = rnd.randrange(len(p) - 1)
        if p[i] == p[i + 1]: continue
        a = ap(ap(st[i], p[i + 1]), p[i])
        if a == st[i + 2]:
            p[i], p[i + 1] = p[i + 1], p[i]; st[i + 1] = ap(st[i], p[i])
    assert st[-1] == XY
    variants.add(tuple(p)); nodes.update(st)
tube = set()
for s in nodes:
    fr = [s]; tube.add(s)
    for _ in range(R):
        nf = []
        for t in fr:
            for m in range(14):
                u = ap(t, m)
                if u not in tube: tube.add(u); nf.append(u)
        fr = nf
t1 = time.time()
par = {s0: None}; fr = [s0]; d = 0; hit = {}
while fr and len(hit) < 2:
    nf = []
    for t in fr:
        for m in range(14):
            u = ap(t, m)
            if u in tube and u not in par:
                par[u] = (t, m); nf.append(u)
                if u in (XY, YX) and u not in hit: hit[u] = d + 1
    fr = nf; d += 1
def path(u):
    out = []
    while par[u]: t, m = par[u]; out.append(m); u = t
    return out[::-1]
res = {"cid": cid, "road": len(road), "variants": len(variants), "nodes": len(nodes), "tube": len(tube), "secs": round(time.time() - t0)}
if XY in hit:
    p = path(XY); res["AC"] = len(p); res["AC_ok"] = core.verify(SR.CH[cid], p, "ac-r2-v1", SR.LIM)["ok"]; res["AC_road"] = p
if YX in hit:
    p = path(YX) + [15, 15]; res["SAC_yx"] = len(p); res["SAC_ok"] = bool(stable_core.verify(SR.CH["s" + cid], p, "sac-r8-v1", SR.LIM).get("ok")); res["SAC_road"] = p
print(json.dumps(res))
