"""Stable AC via the swapped finish. For row s with exact AC distance R (proved), test whether
(y,x) is reachable in <= R-1 AC moves, using T_9 around (x,y) and the generator swap sigma (x<->y):
d(s,(y,x)) = d(sigma s,(x,y)). A path P for sigma s maps to pi(P) for s (pi swaps conjugation
moves 6<->8, 7<->9, 10<->12, 11<->13); then [15,15] destabilizes (y,x) -> (x) -> ().
Every SAC path is replayed by the official stable verifier.
usage: run_sac_swap.py BIN SAIR TFILE WORK OUT rowsjson"""
import json, subprocess, sys, re, time, os
BIN, SAIR, TFILE, WORK, OUT, ROWS = sys.argv[1:7]
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import stable_core, core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}
ENC = {1: 0, -1: 1, 2: 2, -2: 3}; SW = {1: 2, -1: -2, 2: 1, -2: -1}
PI = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}
rows = sorted(json.load(open(ROWS)), key=lambda r: (r['R'], r['k']))
for x in rows:
    row, R = x['row'], x['R']; a = R - 10
    r0, r1 = CH[row]['initial_relators']; s0, s1 = [SW[t] for t in r0], [SW[t] for t in r1]
    for f in os.listdir(WORK):
        if f.startswith(row + '_layer'): os.remove(os.path.join(WORK, f))
    args = [BIN, 'meet', TFILE, '9', str(a), '160000000', WORK, row,
            str(len(s0)), *[str(ENC[t]) for t in s0], str(len(s1)), *[str(ENC[t]) for t in s1]]
    t0 = time.time(); p = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ, STORE_LAST='0' if a >= 9 else '1'))
    rec = {'row': row, 'R_ac': R, 'a': a, 'lmax_yx': a + 9, 'rc': p.returncode, 'wall_s': round(time.time() - t0, 1), 'stdout': p.stdout}
    if 'RESULT NO_MEET' in p.stdout: rec['result'] = f'd(s,(y,x)) >= {R}'
    m = re.search(r'exact_distance=(\d+)', p.stdout); pm = re.search(r'PATH ([\d ]+)', p.stdout)
    if m and pm:
        P = [PI.get(t, t) for t in map(int, pm.group(1).split())]
        sid = 'sac-' + row[3:]
        sac = P + [15, 15]
        rec.update(result='SAC_IMPROVEMENT', d_yx=int(m.group(1)), sac_id=sid, sac_path=sac,
                   sac_verify=stable_core.verify(CH[sid], sac, 'sac-r8-v1', man['limits']))
    print(json.dumps({k: v for k, v in rec.items() if k != 'stdout'}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
