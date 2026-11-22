#!/usr/bin/env python3
"""Gap test: our C beam (standard config) on rows Bluepug holds alone. Prints our AC and rank-2 Stable lengths
next to their records. usage: gap.py OUT.json W [N_PER_BIN]"""
import json, gzip, os, sys, subprocess, random, time
from multiprocessing import Pool
S = '/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad'
sys.path.insert(0, '/home/user/operator-first/tools/acc/upgh')
import symmetry_recog as SR
from verifier import core, stable_core
OUT = sys.argv[1]; W = sys.argv[2]; NB = int(sys.argv[3]) if len(sys.argv) > 3 else 6
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
bp = json.load(gzip.open('/home/user/operator-first/research/acc/live/teams/bluepug_20261122T1509Z.json.gz'))['problems']
RA, RS = bp['ac']['rows'], bp['stable_ac']['rows']
E = {1: 0, -1: 1, 2: 2, -2: 3}
random.seed(7)
rows = []
for lo, hi in ((80, 110), (110, 160), (160, 260)):
    pool = sorted(c for c, v in RA.items() if v[1] == 1 and lo <= v[0] < hi and c.split('-')[1] not in NO)
    rows += random.sample(pool, NB)
def run(cid):
    num = cid.split('-')[1]; a, b = SR.CH[cid]['initial_relators']; rec = RA[cid][0]
    srec = RS.get('sac-' + num, [None])[0]
    env = dict(os.environ, BEAM_H='1', BEAM_DIV='0.8', BEAM_QUOTA='16', BEAM_ELITE='5000', BEAM_DUAL='0.75')
    t0 = time.time()
    try:
        p = subprocess.run([S + '/cstd/bin/acc_beam', S + '/cstd/bin/T8.tab', W, str(min(700, 2 * rec)), str(len(a)), *[str(E[x]) for x in a],
                            str(len(b)), *[str(E[x]) for x in b]], capture_output=True, text=True, env=env, timeout=2400)
        out = p.stdout
    except subprocess.TimeoutExpired:
        out = ''
    r = {}
    for l in out.splitlines():
        f = l.split()
        if f and f[0] in ('AC', 'SAC') and f[1] != 'NONE': r[f[0]] = [int(x) for x in f[3:]]
    ac = r.get('AC'); sac = r.get('SAC')
    okac = bool(ac) and core.verify(SR.CH[cid], ac, 'ac-r2-v1', SR.LIM)['ok']
    oks = bool(sac) and stable_core.verify(SR.CH['sac-' + num], sac, 'sac-r8-v1', SR.LIM).get('ok')
    return dict(cid=cid, rec=rec, srec=srec, ours=len(ac) if okac else None, sours=len(sac) if oks else None,
                path=ac if okac else None, spath=sac if oks else None, sec=round(time.time() - t0))
if __name__ == '__main__':
    print('rows', len(rows), 'W', W, flush=True); res = []
    with Pool(4) as P:
        for r in P.imap_unordered(run, rows):
            res.append(r); json.dump(res, open(OUT, 'w'))
            print(f"{r['cid']}  AC record {r['rec']:4}  ours {r['ours']}   Stable record {r['srec']}  ours(rank 2) {r['sours']}  {r['sec']}s", flush=True)
