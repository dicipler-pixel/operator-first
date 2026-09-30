"""run_beam.py without the official-verifier import: beam + exact finish, then window-14 shortening.
Paths are saved raw ("checked": false). Check them later with `tools/acc/sair_api.py plan` (official
verifier) before any submission. Reads challenge relators from the SAIR manifest (data only).
usage: run_beam_raw.py MANIFEST BINDIR TFILE WORK W DMAX OUTJSONL targets.json
env: BEAM_H, BEAM_DIV, BEAM_SEED, BEAM_NOISE, BEAM_NOV, BEAM_LOOK are passed through to acc_beam."""
import json, os, re, subprocess, sys, time
MAN, BIN, TF, WORK, W, DMAX, OUT, TGT = sys.argv[1:9]
man = json.load(open(MAN)); CH = {c['challenge_id']: c for c in man['challenges']}
E = {1: 0, -1: 1, 2: 2, -2: 3}; SW = {1: 2, -1: -2, 2: 1, -2: -1}
PI = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}
os.makedirs(WORK, exist_ok=True)


def enc(r0, r1): return [str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1]]


def window(r0, r1, path):
    p = subprocess.run([BIN + '/acc_window', WORK, *enc(r0, r1), str(len(path)), *map(str, path)],
                       capture_output=True, text=True)
    recovered = getattr(p, 'astra_verified_window_path', None)
    if recovered is not None:
        return recovered
    m = re.search(r'FINALPATH ?([\d ]*)', p.stdout)
    return list(map(int, m.group(1).split())) if m else path


done = {json.loads(l)['id'] for l in open(OUT)} if os.path.exists(OUT) else set()
for t in json.load(open(TGT)):
    if t['id'] in done: continue
    cid = t['id']; r0, r1 = CH[cid]['initial_relators']; t0 = time.time()
    w = W if t['record'] <= 100 else '20000'; dm = str(min(t['record'] + int(os.environ.get('RB_SLACK', '2')), int(DMAX)))  # RB_SLACK: DMAX = record + slack (default 2)
    if os.environ.get('BEAM_FREE_DMAX'): dm = str(t['record'] + int(os.environ['BEAM_FREE_DMAX']))  # any road, shorten later
    p = subprocess.run([BIN + '/acc_beam', TF, w, dm, *enc(r0, r1)], capture_output=True, text=True)
    rec = {'id': cid, 'record': t['record'], 'k': t['k'], 'checked': False,
           'seed': os.environ.get('BEAM_SEED'), 'noise': os.environ.get('BEAM_NOISE')}
    m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
    if m:
        ac = list(map(int, m.group(1).split())); rec['ac_beam'] = len(ac)
        if len(ac) <= t['record'] + 6: ac = window(r0, r1, ac)
        rec['ac'] = ac; rec['ac_len'] = len(ac)
    m = re.search(r'^SAC \d+ PATH ([\d ]+)', p.stdout, re.M)
    if m:
        sac = list(map(int, m.group(1).split())); rec['sac_beam'] = len(sac)
        core_part = [PI.get(x, x) for x in sac[:-2]]
        if len(sac) <= t['record'] + 8:
            short = window([SW[x] for x in r0], [SW[x] for x in r1], core_part)
            sac2 = [PI.get(x, x) for x in short] + [15, 15]
            if len(sac2) <= len(sac): sac = sac2
        if 'ac' in rec and len(rec['ac']) + 2 < len(sac): sac = rec['ac'] + [16, 15]
        rec['sac'] = sac; rec['sac_len'] = len(sac)
    rec['wall_s'] = round(time.time() - t0, 1)
    rec['verdict'] = ('nopath' if 'ac_len' not in rec else 'BEAT' if rec['ac_len'] < t['record']
                      else 'TIE' if rec['ac_len'] == t['record'] else 'above')
    print(json.dumps({k: v for k, v in rec.items() if k not in ('ac', 'sac')}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
