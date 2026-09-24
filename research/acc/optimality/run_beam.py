"""For each target row: beam+exact finish (AC and Stable AC via (y,x)), official verify, then exact
window-14 shortening of the AC path; the swap-finish SAC path is shortened too by shortening its
swapped AC counterpart. usage: run_beam.py SAIR BINDIR TFILE WORK W DMAX OUTJSONL targets.json"""
import json, subprocess, sys, re, time
SAIR, BIN, TF, WORK, W, DMAX, OUT, TGT = sys.argv[1:9]
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core, stable_core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
E = {1: 0, -1: 1, 2: 2, -2: 3}; SW = {1: 2, -1: -2, 2: 1, -2: -1}; PI = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}
def enc(r0, r1): return [str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1]]
def window(r0, r1, path):
    p = subprocess.run([BIN + '/acc_window', WORK, *enc(r0, r1), str(len(path)), *map(str, path)], capture_output=True, text=True)
    m = re.search(r'FINALPATH ?([\d ]*)', p.stdout); return list(map(int, m.group(1).split())) if m else path
done = set()
import os
if os.path.exists(OUT): done = {json.loads(l)['id'] for l in open(OUT)}
for t in json.load(open(TGT)):
    if t['id'] in done: continue
    cid = t['id']; sid = 'sac-' + cid[3:]; r0, r1 = CH[cid]['initial_relators']; t0 = time.time()
    w = W if t['record'] <= 100 else '20000'; dm = str(min(t['record'] + 2, int(DMAX)))
    p = subprocess.run([BIN + '/acc_beam', TF, w, dm, *enc(r0, r1)], capture_output=True, text=True)
    rec = {'id': cid, 'record': t['record'], 'k': t['k']}
    m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
    if m:
        ac = list(map(int, m.group(1).split())); assert core.verify(CH[cid], ac, 'ac-r2-v1', man['limits'])['ok']
        rec['ac_beam'] = len(ac)
        if len(ac) <= t['record'] + 6: ac = window(r0, r1, ac)
        assert core.verify(CH[cid], ac, 'ac-r2-v1', man['limits'])['ok']
        rec['ac'] = ac; rec['ac_len'] = len(ac)
    m = re.search(r'^SAC \d+ PATH ([\d ]+)', p.stdout, re.M)
    if m:
        sac = list(map(int, m.group(1).split())); assert stable_core.verify(CH[sid], sac, 'sac-r8-v1', man['limits'])['ok']
        rec['sac_beam'] = len(sac)
        # shorten the AC part in swapped coordinates: path to (y,x) for s == path to (x,y) for swap(s)
        core_part = [PI.get(x, x) for x in sac[:-2]]
        s0, s1 = [SW[x] for x in r0], [SW[x] for x in r1]
        short = window(s0, s1, core_part) if len(sac) <= t['record'] + 8 else core_part; sac2 = [PI.get(x, x) for x in short] + [15, 15]
        if stable_core.verify(CH[sid], sac2, 'sac-r8-v1', man['limits'])['ok'] and len(sac2) <= len(sac): sac = sac2
        if 'ac' in rec and len(rec['ac']) + 2 < len(sac): sac = rec['ac'] + [16, 15]
        rec['sac'] = sac; rec['sac_len'] = len(sac)
    rec['wall_s'] = round(time.time() - t0, 1)
    verdict = ('BEAT' if rec.get('ac_len', 999) < t['record'] else 'TIE' if rec.get('ac_len', 999) == t['record'] else 'above')
    rec['verdict'] = verdict
    print(json.dumps({k: v for k, v in rec.items() if k not in ('ac', 'sac')}), flush=True)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
