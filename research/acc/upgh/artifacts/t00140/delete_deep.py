"""Deletion-only search, k deletions from one route, replay on the n=3 start (exact core). usage: delete_deep.py ROW ROUTE_JSON KMIN KMAX OUT"""
import itertools, json, sys, time
SAIR = '/root/.cache/upgh/sair'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
row, route, KMIN, KMAX, out = sys.argv[1], json.loads(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
ch = CH[row]; st0 = tuple(tuple(r) for r in ch['initial_relators']); TGT = ((1,), (2,)); n = len(route); t0 = time.time()
for k in range(KMIN, KMAX + 1):
    cnt = 0; hits = 0
    for dele in itertools.combinations(range(n), k):
        d = set(dele); s = st0; ok = True; cnt += 1
        for i, m in enumerate(route):
            if i in d: continue
            s = core.apply_move(s, m)
            if len(s[0]) + len(s[1]) > 300: ok = False; break
        if ok and s == TGT:
            p = [m for i, m in enumerate(route) if i not in d]
            if core.verify(ch, p, 'ac-r2-v1', man['limits'])['ok']:
                hits += 1; print("HIT", len(p), dele, flush=True)
                with open(out, 'a') as f: f.write(f"{row}: {json.dumps(p).replace(' ', '')}\n")
    print(f"{row} k={k} tried {cnt} hits {hits} ({time.time()-t0:.0f}s)", flush=True)
