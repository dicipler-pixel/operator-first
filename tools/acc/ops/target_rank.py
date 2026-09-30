"""One ranked target list for all rows: expected points per unit of search time.
score = value * p(gap) * p(len), where
  value  = 2^-k for the AC tie we do not hold + 2^-k for the SAC tie we do not hold (a beat would be 1.0 each),
  gap    = our best known length - record (AC or SAC; None = no path yet): p = 0.35, 0.18, 0.08, 0.03, 0.01 for gap 1..4+,
           0.25 for 'no path yet' on records <= 30, 0.08 on 31-45, 0.02 beyond,
  tries  = attempts already logged by any lane: x0.7 per extra attempt,
  len    = record: p = 1 (<=30), 0.7 (31-40), 0.45 (41-50), 0.25 (51-70), 0.08 (71+).
Also tags the lane that fits: 'yx' (SAC record = AC+1, SAC not held), 'dual' (AC side), 'family' (MS family row).
Weights come from today's hit data (one-offs converted most); tune as evidence grows.
usage: python3 tools/acc/ops/target_rank.py [N]   -> research/acc/live/TARGETS_RANKED.{json,md}"""
import glob, gzip, json, os, sys
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
def rows(f):
    d = json.load(gzip.open(f))['data']; lst = next(v for v in d.values() if isinstance(v, list))
    return {r['challengeId']: (r['currentBestLength'], r['kTeams']) for r in lst}
A = rows(sorted(glob.glob('research/acc/live/boards/ac_2026*.json.gz'))[-1])
B = rows(sorted(glob.glob('research/acc/live/boards/stable_ac_2026*.json.gz'))[-1])
sent = {}
for l in open('research/acc/live/SENT_ROWS.txt'):
    if l.startswith('#') or not l.strip(): continue
    t = l.split(); sent[t[0]] = int(t[1])
skip = {r if isinstance(r, str) else (r.get('id') or r.get('challenge_id')) for r in json.load(open('research/acc/live/AK3_CLASS_ROWS.json'))['rows']}
best = {}; tries = {}
for f in glob.glob(S + '/work/*_cap.jsonl') + glob.glob('research/acc/live/sweeps/*_cap.jsonl'):
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        c = d.get('id')
        if not isinstance(c, str): continue
        tries[c] = tries.get(c, 0) + 1
        b = best.setdefault(c, [None, None])
        if d.get('ac_len'): b[0] = d['ac_len'] if b[0] is None else min(b[0], d['ac_len'])
        if d.get('sac_len'): b[1] = d['sac_len'] if b[1] is None else min(b[1], d['sac_len'])
fam = {}
if os.path.exists('research/acc/live/ledger/ms_families_by_w_20260928.json'):
    for w, v in json.load(open('research/acc/live/ledger/ms_families_by_w_20260928.json')).items():
        for n, x in v.items(): fam[x[2]] = f'MS({n},{w.split("|")[0]})'
def pgap(g, rec):
    if g is None: return 0.25 if rec <= 30 else (0.08 if rec <= 45 else 0.02)
    return {1: 0.35, 2: 0.18, 3: 0.08, 4: 0.03}.get(g, 0.01) if g > 0 else 0.0
def plen(rec): return 1 if rec <= 30 else 0.7 if rec <= 40 else 0.45 if rec <= 50 else 0.25 if rec <= 70 else 0.08
out = []
for cid, (ra, ka) in A.items():
    if ra is None or cid in skip: continue
    rs, ks = B.get('s' + cid, (None, 0))
    ab, sb = best.get(cid, [None, None])
    va = 2 ** -ka if sent.get(cid, 999) > ra else 0
    vs = 2 ** -ks if rs is not None and sent.get('s' + cid, 999) > rs else 0
    if va + vs == 0: continue
    pen = 0.7 ** max(0, tries.get(cid, 0) - 1)          # each extra failed attempt: x0.7 (rows that keep resisting sink)
    sa = va * pgap(None if ab is None else ab - ra, ra) * plen(ra) * pen
    ss = vs * pgap(None if sb is None else sb - rs, rs) * plen(rs or ra) * pen
    lane = 'yx' if (rs == ra + 1 and vs) else ('family' if cid in fam else 'dual')
    out.append({'id': cid, 'score': round(sa + ss, 5), 'ac_record': ra, 'k': ka, 'ours_ac': ab, 'sac_record': rs, 'k_sac': ks,
                'ours_sac': sb, 'tries': tries.get(cid, 0), 'value': round(va + vs, 4), 'lane': lane, 'family': fam.get(cid, '')})
out.sort(key=lambda r: -r['score'])
json.dump(out[:2000], open('research/acc/live/TARGETS_RANKED.json', 'w'), indent=0)
L = ['# Ranked targets (expected points per unit of search; board ' + sorted(glob.glob('research/acc/live/boards/ac_2026*.json.gz'))[-1][-20:-8] + ')', '',
     'score = value (2^-k per unheld side) x p(gap to record) x p(record length). "ours" = best length any lane has found.', '',
     '| # | Row | Score | AC rec / k / ours | SAC rec / k / ours | Lane | Family |', '|---|---|---|---|---|---|---|']
for i, r in enumerate(out[:N]):
    L.append(f"| {i+1} | {r['id']} | {r['score']:.4f} | {r['ac_record']} / {r['k']} / {r['ours_ac'] or '-'} | "
             f"{r['sac_record']} / {r['k_sac']} / {r['ours_sac'] or '-'} | {r['lane']} | {r['family']} |")
open('research/acc/live/TARGETS_RANKED.md', 'w').write('\n'.join(L) + '\n')
print(len(out), 'rows scored; top', [(r['id'], r['score'], r['lane']) for r in out[:8]])
