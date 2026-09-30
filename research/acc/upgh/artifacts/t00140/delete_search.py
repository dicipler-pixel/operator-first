"""Conceptual transfer by deletion: replay every sibling (n=4) route on the n=3 start with 0..K moves deleted
(any positions), keep any path that reaches (x,y). Also tries the same with the deleted moves replaced by
nothing but also single-insertion of one move at any position (K=1). Exact, core replay.
usage: delete_search.py ROW_N3 ROUTES_JSON K OUT.txt"""
import itertools, json, sys, time
SAIR = '/root/.cache/upgh/sair'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
row, routes, K, out = sys.argv[1], json.loads(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
ch = CH[row]; st0 = tuple(tuple(r) for r in ch['initial_relators']); TGT = ((1,), (2,))
def run(p):
    s = st0
    for m in p:
        s = core.apply_move(s, m)
        if len(s[0]) + len(s[1]) > 400: return None
    return s
found = []
t0 = time.time()
for route in routes:
    n = len(route)
    for k in range(0, K + 1):
        cnt = 0
        for dele in itertools.combinations(range(n), k):
            d = set(dele); p = [m for i, m in enumerate(route) if i not in d]; cnt += 1
            if run(p) == TGT:
                v = core.verify(ch, p, 'ac-r2-v1', man['limits'])
                if v['ok']:
                    found.append(p); print(f"HIT len={len(p)} del={dele} route_len={n}", flush=True)
                    with open(out, 'a') as f: f.write(f"{row}: {json.dumps(p).replace(' ', '')}\n")
        print(f"route len {n}: k={k} tried {cnt} ({time.time()-t0:.1f}s)", flush=True)
    # single insertion at any position of any move (k=+1)
    cnt = 0
    for i in range(n + 1):
        for m in range(14):
            p = route[:i] + [m] + route[i:]; cnt += 1
            if run(p) == TGT:
                found.append(p); print(f"HIT len={len(p)} ins=({i},{m})", flush=True)
                with open(out, 'a') as f: f.write(f"{row}: {json.dumps(p).replace(' ', '')}\n")
    print(f"route len {n}: +1 insertion tried {cnt}", flush=True)
    # one deletion + one insertion (substitution / move)
    cnt = 0
    for dpos in range(n):
        base = route[:dpos] + route[dpos + 1:]
        for i in range(len(base) + 1):
            for m in range(14):
                p = base[:i] + [m] + base[i:]; cnt += 1
                if run(p) == TGT:
                    found.append(p); print(f"HIT len={len(p)} del={dpos} ins=({i},{m})", flush=True)
                    with open(out, 'a') as f: f.write(f"{row}: {json.dumps(p).replace(' ', '')}\n")
    print(f"route len {n}: del+ins tried {cnt} ({time.time()-t0:.1f}s)", flush=True)
print("DONE", row, "found", len(found), "best", min((len(p) for p in found), default=None))
