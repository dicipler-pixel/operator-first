"""Exact capped sweep over a list of rows: for each row, run acc_capped with rising total-length caps
(start length upward, until the state budget stops a cap before depth MAXD) and depth MAXD = max(AC record - 9, SAC record - 11), so any
AC path <= AC record or SAC path <= SAC record whose first MAXD states stay within the cap is found.
Stops a row early once both AC and SAC reach their records. Paths are saved unchecked.
usage: run_capped_sweep.py MANIFEST BINDIR TFILE WORKDIR targets.json OUT.jsonl [SPAN] [BUDGET]
targets.json: [{"id": "ac-NNNNN", "ac_record": R or null, "sac_record": R or null}, ...]"""
import json, math, os, re, shutil, subprocess, sys, time
MAN, BIN, TF, WORK, TGT, OUT = sys.argv[1:7]
SPAN = int(sys.argv[7]) if len(sys.argv) > 7 else 40
JUMP = int(os.environ.get('CAP_JUMP', '6'))
BUDGET = sys.argv[8] if len(sys.argv) > 8 else '180000000'
PROBE = int(os.environ.get('CAP_PROBE', '10000000'))
C = {c['challenge_id']: c for c in json.load(open(MAN))['challenges']}


def predict_total(stderr, maxd, k=6):
    """'Leader' extrapolation: after the noisy first layers, log(layer growth) decays smoothly as the
    capped region fills. Fit that decay on the last k layers of a cheap probe and extend it to
    depth maxd. Checked on ac-05818: cap 26 predicted 80M (actual 87M); cap 27 predicted 397M
    (actual > 196M)."""
    L = [int(x) for x in re.findall(r'd=\d+ \+(\d+)', stderr)]
    if len(L) < k + 2:
        return None
    lr = [math.log(L[i] / L[i - 1]) for i in range(1, len(L)) if L[i - 1] > 0 and L[i] > 0]
    xs = list(range(len(lr) - k, len(lr))); ys = lr[-k:]
    mx, my = sum(xs) / k, sum(ys) / k
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs); a = my - b * mx
    tot, cur, d = sum(L), L[-1], len(L)
    while d < maxd:
        cur *= math.exp(max(0.0, a + b * (len(lr) + d - len(L)))); tot += cur; d += 1
    return tot
E = {1: 0, -1: 1, 2: 2, -2: 3}
done = {json.loads(l)['id'] for l in open(OUT)} if os.path.exists(OUT) else set()
for t in json.load(open(TGT)):
    cid = t['id']
    if cid in done: continue
    r0, r1 = C[cid]['initial_relators']; start = len(r0) + len(r1)
    ra, rs = t.get('ac_record') or 0, t.get('sac_record') or 0      # 0 = not a target on that board
    maxd = max(ra - 9 if ra else 0, rs - 11 if rs else 0)
    enc = [str(len(r0)), *[str(E[a]) for a in r0], str(len(r1)), *[str(E[a]) for a in r1]]
    rec = {'id': cid, 'start': start, 'ac_record': t.get('ac_record'), 'sac_record': t.get('sac_record'),
           'checked': False, 'caps': []}
    t0 = time.time()
    # Jump ahead: a cap-C search contains every lower cap, so re-running low caps only costs time
    # (2-3.5x on our sweeps). Start at start+JUMP and climb; if that first cap runs out of budget,
    # step down by 2 until one completes.
    def caps():
        c = start + JUMP
        yield c
        if rec['caps'][-1]['complete']:
            while c < start + SPAN:
                c += 1
                yield c
        else:
            while c - 2 >= start:
                c -= 2
                yield c
            if c > start:
                yield start
    for cap in caps():
        wd = os.path.join(WORK, 'cap_' + cid); os.makedirs(wd, exist_ok=True)
        env = {**os.environ, 'MAXD': str(maxd)}
        # probe first (small budget): if it finishes, that's the answer; if its extrapolation doesn't
        # fit the budget, skip this cap instead of burning a whole budget-sized run
        p = subprocess.run([BIN + '/acc_capped', TF, str(cap), str(PROBE), wd, 'c', *enc], capture_output=True,
                           text=True, env={**env, 'INIT_LOG2': '24'})
        shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd, exist_ok=True)
        st0 = re.search(r'cap=\d+ states=(\d+) depth=(\d+) (\w+)', p.stdout)
        probe_done = bool(st0) and (st0.group(3) == 'CLOSED' or int(st0.group(2)) > maxd or ' PATH ' in p.stdout)
        pred = None if probe_done else predict_total(p.stderr, maxd)
        if not probe_done and pred is not None and pred > 0.9 * int(BUDGET):
            info = {'cap': cap, 'states': None, 'depth': None, 'end': 'SKIPPED_PREDICTED', 'predicted': int(pred),
                    'complete': False}
            rec['caps'].append(info); print(json.dumps({'id': cid, **info}), flush=True)
            shutil.rmtree(wd, ignore_errors=True)
            if len(rec['caps']) > 1 and rec['caps'][0]['complete']: break
            continue
        if not probe_done:
            p = subprocess.run([BIN + '/acc_capped', TF, str(cap), BUDGET, wd, 'c', *enc], capture_output=True,
                               text=True, env={**env, 'INIT_LOG2': '27'})
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
        # every AC path is also a Stable AC path: AC + [16, 15] (destabilize y, then x)
        if 'ac' in rec and len(rec['ac']) + 2 < len(rec.get('sac', [0] * 999)):
            rec['sac'] = rec['ac'] + [16, 15]; info['sac_len'] = len(rec['sac']); info['sac_from_ac'] = True
        # complete = every layer through MAXD searched (depth reported as MAXD+1) or a path found
        # CLOSED = no state within the cap is left (the whole capped space was searched)
        info['complete'] = (info['end'] == 'CLOSED' or bool(info['depth'] and info['depth'] > maxd)
                            or 'ac_len' in info or 'sac_len' in info)
        rec['caps'].append(info)
        print(json.dumps({'id': cid, **info}), flush=True)
        if ((not ra or len(rec.get('ac', [0] * 999)) <= ra)
                and (not rs or len(rec.get('sac', [0] * 999)) <= rs)): break
        if len(rec['caps']) > 1:
            going_up = rec['caps'][0]['complete']
            if going_up and not info['complete']: break      # budget reached: higher caps only get bigger
            if not going_up and info['complete']: break      # stepped down to the largest cap that fits
    done_caps = [c['cap'] for c in rec['caps'] if c['complete']]
    rec['proved_cap'] = max(done_caps) if done_caps else None   # no record path within this cap
    rec['ac_len'] = len(rec['ac']) if 'ac' in rec else None
    rec['sac_len'] = len(rec['sac']) if 'sac' in rec else None
    rec['wall_s'] = round(time.time() - t0, 1)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
