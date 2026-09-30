"""Solve-first lane: supermove class beam (smbeam) -> direct compile to official moves -> official verify. Routes go to
OUT (jsonl) with the raw path; shortening runs separately. usage: sm_lane.py TARGETS OUT W DMAX LCAP TMAX [SEEDS]"""
import json, subprocess, sys, time, os
import os; S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_direct as cd, skel_dp_local as k
tg = json.load(open(sys.argv[1])); OUT = sys.argv[2]; W, DMAX, LCAP, TMAX = sys.argv[3:7]
SEEDS = [int(x) for x in (sys.argv[7] if len(sys.argv) > 7 else '1').split(',')]
done = set()
if os.path.exists(OUT): done = {json.loads(l)['id'] for l in open(OUT)}
for t in tg:
    cid = t['id'] if isinstance(t, dict) else t
    if cid in done: continue
    c = k.T[cid]; r0, r1 = c['initial_relators']
    rec = {'id': cid, 'record': t.get('record') if isinstance(t, dict) else None}
    for sd in SEEDS:
        rf = os.path.join(os.path.dirname(os.path.abspath(OUT)), 'roads', f'{cid}_s{sd}.out'); os.makedirs(os.path.dirname(rf), exist_ok=True)
        t0 = time.time()
        try:
            p = subprocess.run([os.environ.get('SMBEAM', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smbeam')), W, DMAX, LCAP, str(sd), str(len(r0)), *map(str, r0), str(len(r1)), *map(str, r1)],
                               capture_output=True, text=True, timeout=int(TMAX))
            txt = p.stdout
        except subprocess.TimeoutExpired: txt = ''
        rec[f's{sd}_s'] = round(time.time() - t0, 1)
        if 'FOUND' not in txt: continue
        open(rf, 'w').write(txt)
        try:
            out = []; state = tuple(tuple(r) for r in c['initial_relators']); R = []
            for s in cd.parse(rf):
                cl = k.cls(s)
                if not R or R[-1] != cl: R.append(cl)
            for cl in R[1:]: state = cd.step(state, cl, out)
            for i in (0, 1): state = cd.cyc_reduce(state, i, out)
            f = cd.finish(state); out += f
            v = k.core.verify(c, out, 'ac-r2-v1', k.rl.LIMITS)
            if v.get('ok'):
                if 'path' not in rec or len(out) < len(rec['path']): rec.update(road=len(R), raw_len=len(out), path=out, seed=sd)
        except Exception as e: rec[f's{sd}_err'] = str(e)[:120]
    rec['verdict'] = 'route' if 'path' in rec else 'nopath'
    print(json.dumps({x: y for x, y in rec.items() if x != 'path'}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
