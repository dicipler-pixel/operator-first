"""Automatic 'opposite approach' on near misses: every lane result that is exactly 1 over a record held by 1-2 teams
(AC or SAC) gets, once each: the mirror-twin beam (AC), and the two (y,x)-aimed beams (SAC: TWIN_MODE=yx, yx2).
Loops forever (poll every 10 min). Results -> $ACC_S/work/esc_cap.jsonl (watch_sweeps sees it via esc_targets.json)."""
import glob, gzip, json, os, subprocess, time
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
W = S + '/work/'; OUT = W + 'esc_cap.jsonl'; TGT = W + 'esc_targets.json'; DONE = W + 'esc_done.txt'
BEAM = dict(os.environ, BEAM_H='1', BEAM_DIV='0.8', BEAM_P2='2', BEAM_QUOTA='16', BEAM_ELITE='5000', BEAM_DUAL='0.75')
def rows(f):
    d = json.load(gzip.open(f))['data']; lst = next(v for v in d.values() if isinstance(v, list))
    return {r['challengeId']: (r['currentBestLength'], r['kTeams']) for r in lst}
while True:
    A = rows(sorted(glob.glob('research/acc/live/boards/ac_2026*.json.gz'))[-1])
    B = rows(sorted(glob.glob('research/acc/live/boards/stable_ac_2026*.json.gz'))[-1])
    sent = {}
    for l in open('research/acc/live/SENT_ROWS.txt'):
        if l.startswith('#') or not l.strip(): continue
        t = l.split(); sent[t[0]] = int(t[1])
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    jobs = []
    for f in glob.glob(W + '*_cap.jsonl'):
        if f.endswith('esc_cap.jsonl'): continue
        for l in open(f):
            try: d = json.loads(l)
            except Exception: continue
            cid = d.get('id')
            if not cid or cid not in A or A[cid][0] is None: continue
            ra, ka = A[cid]; rs, ks = B.get('s' + cid, (None, 9))
            if d.get('ac_len') == ra + 1 and ka <= 2 and sent.get(cid, 999) > ra and ('ac:' + cid) not in done:
                jobs.append(('ac', cid, ra, ka, rs))
            if rs is not None and d.get('sac_len') == rs + 1 and ks <= 2 and sent.get('s' + cid, 999) > rs and ('sac:' + cid) not in done:
                jobs.append(('sac', cid, ra, ks, rs))
    jobs = sorted(set(jobs), key=lambda j: (j[3], j[2]))
    T = {t['id']: t for t in (json.load(open(TGT)) if os.path.exists(TGT) else [])}
    for kind, cid, ra, k, rs in jobs:
        T[cid] = {'id': cid, 'record': ra, 'k': k, 'ac_record': A[cid][0], 'sac_record': rs}
        json.dump(list(T.values()), open(TGT, 'w'))
        modes = [('', ra + 1)] if kind == 'ac' else [('yx', rs - 2), ('yx2', rs - 2)]
        for mode, dmax in modes:
            env = dict(BEAM, TWIN_MODE=mode) if mode else BEAM
            p = subprocess.run(['python3', 'tools/acc/ops/twin_beam.py', cid, '20000', str(dmax)], capture_output=True, text=True, env=env)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else json.dumps({'id': cid, 'verdict': 'error'})
            with open(OUT, 'a') as o: o.write(line + '\n')
        with open(DONE, 'a') as o: o.write(kind + ':' + cid + '\n')
    time.sleep(600)
