"""Driver: run acc_opt meet for rows, parse results, replay any path with the official verifier core.
usage: run_meet.py BIN SAIR TFILE B WORKDIR OUTJSONL row:a [row:a ...]"""
import json, subprocess, sys, time, re, os
BIN, SAIR, TFILE, B, WORK, OUT = sys.argv[1:7]
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}
ENC = {1: 0, -1: 1, 2: 2, -2: 3}
for spec in sys.argv[7:]:
    row, a = spec.split(':'); a = int(a)
    c = CH[row]; r0, r1 = c['initial_relators']
    args = [BIN, 'meet', TFILE, B, str(a), '160000000', WORK, row,
            str(len(r0)), *[str(ENC[x]) for x in r0], str(len(r1)), *[str(ENC[x]) for x in r1]]
    t0 = time.time()
    import os; env = dict(os.environ, STORE_LAST='0' if a >= 9 else '1')
    p = subprocess.run(args, capture_output=True, text=True, env=env)
    for f in os.listdir(WORK):
        if f.startswith(row + '_layer'): os.remove(os.path.join(WORK, f))
    rec = {'row': row, 'a': a, 'b': int(B), 'lmax': a + int(B), 'rc': p.returncode,
           'wall_s': round(time.time() - t0, 1), 'stdout': p.stdout, 'stderr_tail': p.stderr[-3000:]}
    m = re.search(r'SA_STORED=(\d+)', p.stdout); rec['S_stored'] = int(m.group(1)) if m else None
    m = re.search(r'streamed \(edges.*?\): (\d+)', p.stdout); rec['layer_a_streamed_edges'] = int(m.group(1)) if m else None
    m = re.search(r'MEETS=(\d+)', p.stdout); rec['meets'] = int(m.group(1)) if m else None
    if 'RESULT NO_MEET' in p.stdout: rec['result'] = 'NO_MEET'
    m = re.search(r'RESULT MEET exact_distance=(\d+) dS=(\d+) dT=(\d+) rebuild=(-?\d+)', p.stdout)
    if m:
        rec['result'] = 'MEET'; rec['exact_distance'] = int(m.group(1)); rec['dS'] = int(m.group(2)); rec['dT'] = int(m.group(3))
        pm = re.search(r'PATH ([\d ]+)', p.stdout)
        if pm:
            path = list(map(int, pm.group(1).split())); rec['path'] = path
            rec['official_core_verify'] = core.verify(c, path, 'ac-r2-v1', man['limits'])
    print(json.dumps({k: v for k, v in rec.items() if k not in ('stdout', 'stderr_tail')}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
    if rec['rc'] != 0: sys.exit(rec['rc'])
