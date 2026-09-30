"""Every 15 min: (1) junction splice over the whole route pool (junction_splice.py, R=2); (2) yx_mid on every row where we
hold an AC path at the record (or 1 over) and the Stable record = AC record + 1, not yet run and not held.
Hits are written in watch_sweeps format: $ACC_S/work/auto_cap.jsonl + auto_targets.json (so the sweep watcher fires).
usage: python3 tools/acc/ops/auto_splice_loop.py      (runs until killed; env BEAM_* passed to yx_mid)"""
import glob, gzip, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scratch_utils')); from acmoves import run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
W = S + '/work/'; OUT = W + 'auto_cap.jsonl'; TGT = W + 'auto_targets.json'; DONE = W + 'auto_yxm_done.txt'
ENV = dict(os.environ, ACC_S=S, BEAM_H='1', BEAM_DIV='0.8', BEAM_P2='2', BEAM_QUOTA='16', BEAM_ELITE='5000', BEAM_DUAL='0.75')
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
man = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in man['challenges']}
def board(p):
    d = json.load(gzip.open(sorted(glob.glob(f'research/acc/live/boards/{p}_2026*.json.gz'))[-1]))['data']
    return {r['challengeId'].replace('sac-', 'ac-'): (r['currentBestLength'], r['kTeams']) for r in d['items']}
def targets_add(cid, A, B):
    T = {t['id']: t for t in (json.load(open(TGT)) if os.path.exists(TGT) else [])}
    T[cid] = {'id': cid, 'record': A.get(cid, (None, 0))[0], 'k': A.get(cid, (None, 0))[1],
              'ac_record': A.get(cid, (None, 0))[0], 'sac_record': B.get(cid, (None, 0))[0]}
    json.dump(list(T.values()), open(TGT, 'w'))
def emit(rec, A, B):
    targets_add(rec['id'], A, B)
    with open(OUT, 'a') as f: f.write(json.dumps(rec) + '\n')
while True:
    A, B = board('ac'), board('stable_ac')
    # (1) junction splice
    p = subprocess.run(['python3', 'tools/acc/ops/junction_splice.py', '2'], capture_output=True, text=True, env=ENV)
    for l in p.stdout.splitlines():
        try: d = json.loads(l)
        except Exception: continue
        if not d.get('ok') or not d.get('ties_or_beats'): continue
        if d['target'] == 'x,y': emit({'id': d['id'], 'src': 'junction', 'ac_len': len(d['path']), 'ac': d['path'],
                                       'sac_len': len(d['path']) + 2, 'sac': d['path'] + [16, 15]}, A, B)
        else: emit({'id': d['id'], 'src': 'junction', 'sac_len': len(d['path']) + 2, 'sac': d['path'] + [15, 15]}, A, B)
    # (2) yx_mid on AC paths at/near the record where Stable record = AC + 1
    sent = {}
    for l in open('research/acc/live/SENT_ROWS.txt'):
        t = l.split()
        if len(t) >= 2 and not l.startswith('#'): sent[t[0]] = int(t[1])
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    skip = set(open(W + 'yxm_done_manual.txt').read().split()) if os.path.exists(W + 'yxm_done_manual.txt') else set()
    paths = {}
    for f in glob.glob(W + '*_cap.jsonl') + glob.glob('research/acc/live/sweeps/*.jsonl'):
        for l in open(f, errors='ignore'):
            try: d = json.loads(l)
            except Exception: continue
            if isinstance(d, dict) and isinstance(d.get('id'), str) and isinstance(d.get('ac'), list): paths.setdefault(d['id'], []).append(d['ac'])
    for f in glob.glob('research/acc/live/inbox/*.txt') + glob.glob('ACC_QUEUE_*.txt'):
        for l in open(f, errors='ignore'):
            m = re.match(r'^(ac-\d{5}):\s*(\[[\d,\s]*\])', l.strip())
            if m: paths.setdefault(m.group(1), []).append(json.loads(m.group(2)))
    for cid, ps in paths.items():
        if cid in done or cid in skip or cid not in C or cid not in A: continue
        ra, rs = A[cid][0], B.get(cid, (None, 0))[0]
        if ra is None or rs is None or rs != ra + 1 or sent.get('s' + cid, 999) <= rs: continue
        R0 = tuple(''.join(L[i] for i in x) for x in C[cid]['initial_relators'])
        good = [q for q in ps if len(q) <= ra + 1 and all(isinstance(m, int) and 0 <= m < 14 for m in q) and run(R0, q) == ('x', 'y')]
        if not good: continue
        q = min(good, key=len)
        r = subprocess.run(['python3', 'tools/acc/ops/yx_mid.py', cid, str(rs - 2), json.dumps(q), '20000', '1'],
                           capture_output=True, text=True, env=ENV)
        last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '{}'
        try: d = json.loads(last)
        except Exception: d = {}
        if d.get('sac'): emit({'id': cid, 'src': 'yx_mid', 'sac_len': d['sac_len'], 'sac': d['sac']}, A, B)
        with open(DONE, 'a') as f: f.write(cid + '\n')
    time.sleep(900)
