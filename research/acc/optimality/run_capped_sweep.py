"""Exact capped sweep over a list of rows: for each row, run acc_capped with rising total-length caps
(start length upward, until the state budget stops a cap before depth MAXD) and depth MAXD = max(AC record - 9, SAC record - 11), so any
AC path <= AC record or SAC path <= SAC record whose first MAXD states stay within the cap is found.
Stops a row early once both AC and SAC reach their records. Paths are saved unchecked.
usage: run_capped_sweep.py MANIFEST BINDIR TFILE WORKDIR targets.json OUT.jsonl [SPAN] [BUDGET]
targets.json: [{"id": "ac-NNNNN", "ac_record": R or null, "sac_record": R or null}, ...]"""
import json, os, re, shutil, subprocess, sys, time
MAN, BIN, TF, WORK, TGT, OUT = sys.argv[1:7]
SPAN = int(sys.argv[7]) if len(sys.argv) > 7 else 40
BUDGET = sys.argv[8] if len(sys.argv) > 8 else '180000000'
C = {c['challenge_id']: c for c in json.load(open(MAN))['challenges']}
E = {1: 0, -1: 1, 2: 2, -2: 3}
done = {json.loads(l)['id'] for l in open(OUT)} if os.path.exists(OUT) else set()
for t in json.load(open(TGT)):
    cid = t['id']
    if cid in done: continue
    r0, r1 = C[cid]['initial_relators']; start = len(r0) + len(r1)
    ra, rs = t.get('ac_record') or 999, t.get('sac_record') or 999
    maxd = max(ra - 9, rs - 11)
    enc = [str(len(r0)), *[str(E[a]) for a in r0], str(len(r1)), *[str(E[a]) for a in r1]]
    rec = {'id': cid, 'start': start, 'ac_record': t.get('ac_record'), 'sac_record': t.get('sac_record'),
           'checked': False, 'caps': []}
    t0 = time.time()
    for cap in range(start, start + SPAN + 1):
        wd = os.path.join(WORK, 'cap_' + cid); os.makedirs(wd, exist_ok=True)
        p = subprocess.run([BIN + '/acc_capped', TF, str(cap), BUDGET, wd, 'c', *enc], capture_output=True,
                           text=True, env={**os.environ, 'MAXD': str(maxd), 'INIT_LOG2': '27'})
        shutil.rmtree(wd, ignore_errors=True)
        st = re.search(r'cap=\d+ states=(\d+) depth=(\d+) (\w+)', p.stdout)
        info = {'cap': cap, 'states': int(st.group(1)) if st else None,
                'depth': int(st.group(2)) if st else None, 'end': st.group(3) if st else p.stdout[-200:]}
        for which in ('AC', 'SAC'):
            m = re.search(r'^\[c\] %s (\d+) PATH ([\d ]+)' % which, p.stdout, re.M)
            if m:
                path = list(map(int, m.group(2).split())); key = which.lower()
                info[key + '_len'] = len(path)
                if len(path) < len(rec.get(key, [0] * 999)): rec[key] = path
        # complete = every layer through MAXD searched (depth reported as MAXD+1) or a path found
        info['complete'] = bool(info['depth'] and info['depth'] > maxd) or 'ac_len' in info or 'sac_len' in info
        rec['caps'].append(info)
        print(json.dumps({'id': cid, **info}), flush=True)
        if len(rec.get('ac', [0] * 999)) <= ra and len(rec.get('sac', [0] * 999)) <= rs: break
        if not info['complete']: break           # budget reached: higher caps only get bigger
    done_caps = [c['cap'] for c in rec['caps'] if c['complete']]
    rec['proved_cap'] = max(done_caps) if done_caps else None   # no record path within this cap
    rec['ac_len'] = len(rec['ac']) if 'ac' in rec else None
    rec['sac_len'] = len(rec['sac']) if 'sac' in rec else None
    rec['wall_s'] = round(time.time() - t0, 1)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
