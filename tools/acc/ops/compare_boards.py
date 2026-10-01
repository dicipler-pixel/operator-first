"""env CB_CLEAN=1: apply the commuting-pair cleanup (commute_clean.py) to every route first.
Song 2 (session 2): 'a second body started ticking against mine ... we compared'.
Every route the team holds (UPG-H ledger, repo pool/queue/sweeps/inbox, all scratch *.jsonl) against both live boards, all k:
AC route P scores on AC if len(P) <= AC record; on Stable if len(P)+2 <= Stable record (P + [16,15]).
Stable lines (sac key) score if len <= Stable record. Skips rows we already hold at/below the record."""
import json, gzip, glob, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from commute_clean import clean
CLEAN = os.environ.get('CB_CLEAN') == '1'
S = '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad'
st = sorted(glob.glob('research/acc/live/boards/ac_*.json.gz'))[-1].split('ac_')[-1][:-8]
B = {}
for p in ('ac', 'stable_ac'):
    for x in json.load(gzip.open(f'research/acc/live/boards/{p}_{st}.json.gz'))['data']['items']: B[x['challengeId']] = (x.get('currentBestLength'), x.get('kTeams'))
mine = {}
for fn in glob.glob('research/acc/live/mine_2*.json') + ['research/acc/live/mine_recent.json']:
    for it in json.load(open(fn)).get('items', []):
        for r in it.get('results') or []:
            if r.get('ok'): mine[r['challenge_id']] = min(mine.get(r['challenge_id'], 1 << 30), r['length'])
for l in open('research/acc/live/submit_log.jsonl'):
    try: x = json.loads(l)
    except ValueError: continue
    for r in x.get('results') or []:
        if r.get('ok') and r.get('length'): mine[r['challenge_id']] = min(mine.get(r['challenge_id'], 1 << 30), r['length'])
AC = {}; SAC = {}
def put(D, k, p, src):
    if not (isinstance(p, list) and p and all(isinstance(m, int) for m in p)): return
    if CLEAN: p = clean(p)
    if k not in D or len(p) < len(D[k][0]): D[k] = (p, src)
for l in open('research/acc/upgh/ledger.jsonl'):
    try: x = json.loads(l)
    except ValueError: continue
    d = x.get('data') or {}
    if (x.get('kind') or x.get('event')) == 'path.best' and d.get('cid') and d.get('moves'):
        put(AC if d['cid'].startswith('ac-') else SAC, d['cid'], d['moves'], 'ledger')
line_re = re.compile(r'^(s?ac-\d{5}):\s*(\[[\d,\s]*\])', re.M)
for fn in glob.glob('research/acc/live/**/*.txt', recursive=True) + glob.glob('*.txt'):
    try: t = open(fn).read()
    except (OSError, UnicodeDecodeError): continue
    for cid, arr in line_re.findall(t):
        try: put(AC if cid.startswith('ac-') else SAC, cid, json.loads(arr), fn)
        except ValueError: pass
files = [f for f in glob.glob(f'{S}/**/*.jsonl', recursive=True) if '/swapS' not in f and '/swapW' not in f] + glob.glob('research/acc/live/**/*.jsonl', recursive=True)
for fn in files:
    try:
        for l in open(fn):
            if '"id"' not in l: continue
            try: x = json.loads(l)
            except ValueError: continue
            i = x.get('id')
            if not isinstance(i, str) or not i.startswith('ac-'): continue
            put(AC, i, x.get('ac'), fn); put(SAC, 's' + i, x.get('sac'), fn)
    except (OSError, UnicodeDecodeError): pass
NEVER = {'09839', '02257', '09311', '06403', '04718', '05378'}
wins = []
for cid, (p, src) in AC.items():
    n = cid[3:]
    if n in NEVER: continue
    ar, ak = B.get(cid, (None, None)); sr, sk = B.get('sac-' + n, (None, None))
    if ar and len(p) <= ar and mine.get(cid, 1 << 30) > ar: wins.append((cid, len(p), ar, ak, 'AC', src, p))
    if sr and len(p) + 2 <= sr and mine.get('sac-' + n, 1 << 30) > sr: wins.append(('sac-' + n, len(p) + 2, sr, sk, 'AC+[16,15]', src, p + [16, 15]))
for cid, (p, src) in SAC.items():
    n = cid[4:]
    if n in NEVER: continue
    sr, sk = B.get(cid, (None, None))
    if sr and len(p) <= sr and mine.get(cid, 1 << 30) > sr: wins.append((cid, len(p), sr, sk, 'Stable line', src, p))
best = {}
for w in wins:
    if w[0] not in best or w[1] < best[w[0]][1]: best[w[0]] = w
print(json.dumps({'board': st, 'ac_routes': len(AC), 'sac_routes': len(SAC), 'files': len(files), 'wins': len(best)}))
for w in sorted(best.values(), key=lambda w: (w[1] - w[2], w[3] or 99)):
    print(json.dumps({'row': w[0], 'len': w[1], 'record': w[2], 'k': w[3], 'how': w[4], 'src': os.path.relpath(w[5], S) if w[5].startswith(S) else w[5]}))
json.dump([{'row': w[0], 'len': w[1], 'record': w[2], 'k': w[3], 'how': w[4], 'path': w[6]} for w in best.values()], open(f'{S}/work/compare_wins.json', 'w'))
