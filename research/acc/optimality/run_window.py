"""Driver for acc_window: run a row's path, replay every PATH/FINALPATH with official core.verify.
usage: run_window.py BIN SAIR WORKDIR OUTJSONL row=[moves]json ..."""
import json, subprocess, sys, time, re
BIN, SAIR, WORK, OUT = sys.argv[1:5]
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}; ENC = {1: 0, -1: 1, 2: 2, -2: 3}
jobs = json.load(open(sys.argv[5]))
for row in (sys.argv[6].split(',') if len(sys.argv) > 6 else jobs):
    path = jobs[row]; c = CH[row]; r0, r1 = c['initial_relators']
    assert core.verify(c, path, 'ac-r2-v1', man['limits'])['ok']
    args = [BIN, WORK, str(len(r0)), *[str(ENC[x]) for x in r0], str(len(r1)), *[str(ENC[x]) for x in r1], str(len(path)), *map(str, path)]
    t0 = time.time(); p = subprocess.run(args, capture_output=True, text=True)
    rec = {'row': row, 'start_len': len(path), 'rc': p.returncode, 'wall_s': round(time.time() - t0, 1), 'log': p.stdout}
    fm = re.search(r'FINALPATH ?([\d ]*)', p.stdout)
    if fm:
        fp = list(map(int, fm.group(1).split())); rec['end_len'] = len(fp); rec['final_path'] = fp
        rec['official_core_verify'] = core.verify(c, fp, 'ac-r2-v1', man['limits'])
    rec['passes'] = re.findall(r'PASS (\d+) done: max \|B7\|=(\d+), ([\d.]+)s', p.stdout)
    print(json.dumps({k: v for k, v in rec.items() if k != 'log'}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
