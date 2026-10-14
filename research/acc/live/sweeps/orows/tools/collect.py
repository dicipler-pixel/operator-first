"""Collect every road we hold for the orows target numbers (ac- and sac- lines), verify on the official cores, write best per row."""
import json, sys, glob
from pathlib import Path
REPO = Path('/home/user/operator-first')
sys.path.insert(0, str(REPO / 'tools/acc/upgh'))
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools')
from verifier import core, stable_core
from harvest import extract
OUT = Path('/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/orows')
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
T = json.load(open(REPO / 'research/acc/live/sweeps/orows/targets.json'))
NUMS = {t['row'].split('-')[1] for t in T}
roads = {}  # cid -> {tuple(moves): src}
def put(cid, moves, src):
    if not isinstance(moves, (list, tuple)) or not moves: return
    if cid.split('-')[-1] not in NUMS: return
    roads.setdefault(cid, {}).setdefault(tuple(moves), src)
for line in open(REPO / 'research/acc/upgh/ledger.jsonl', encoding='utf-8'):
    if '"path.best"' not in line: continue
    try: d = json.loads(line)['data']
    except Exception: continue
    put(d.get('cid', ''), d.get('moves'), 'ledger')
files = [f for f in (REPO / 'research/acc/live').rglob('*') if f.suffix in ('.txt', '.jsonl', '.json') and f.stat().st_size < 60_000_000]
files += list(REPO.glob('ACC_*.txt'))
for f in files:
    try:
        for cid, moves, _ in extract(f):
            put(cid, moves, f.relative_to(REPO).as_posix())
    except Exception as e:
        pass
best = {}
for cid, rs in roads.items():
    for p, src in rs.items():
        p = list(p)
        n = cid.split('-')[-1]
        if cid.startswith('ac-'):
            ok = core.verify(CH[cid], p, 'ac-r2-v1', LIM)['ok']
            if not ok: continue
            for key, line in (('ac-' + n, p), ('sac-' + n, p + [16, 15])):
                if key not in best or len(line) < len(best[key][0]): best[key] = (line, src + (' (AC+[16,15])' if key.startswith('sac') else ''), p)
        elif cid.startswith('sac-'):
            ok = stable_core.verify(CH[cid], p, 'sac-r8-v1', LIM)['ok']
            if not ok: continue
            if cid not in best or len(p) < len(best[cid][0]): best[cid] = (p, src, None)
res = {}
for t in T:
    r = t['row']; b = best.get(r)
    n = r.split('-')[1]
    ac = best.get('ac-' + n)
    print(r, 'listed', t['our_best'], 'record', t['record'], 'k', t['k'], '| rebuilt', len(b[0]) if b else None, b[1] if b else '', '| best AC road', len(ac[0]) if ac else None)
    res[r] = {'line': b[0] if b else None, 'src': b[1] if b else None, 'ac': ac[0] if ac else None,
              'n_ac_roads': len(roads.get('ac-' + n, {})), 'n_sac_lines': len(roads.get('sac-' + n, {}))}
json.dump(res, open(OUT / 'best_roads.json', 'w'))
# all verified AC roads per number, for later tools
allr = {}
for cid, rs in roads.items():
    if cid.startswith('ac-'):
        allr[cid] = sorted([list(p) for p in rs if core.verify(CH[cid], list(p), 'ac-r2-v1', LIM)['ok']], key=len)[:50]
json.dump(allr, open(OUT / 'all_ac_roads.json', 'w'))
print({k: len(v) for k, v in allr.items()})
alls = {}
for cid, rs in roads.items():
    if cid.startswith('sac-'):
        alls[cid] = sorted([list(p) for p in rs if stable_core.verify(CH[cid], list(p), 'sac-r8-v1', LIM)['ok']], key=len)[:50]
json.dump(alls, open(OUT / 'all_sac_lines.json', 'w'))
print('sac lines', {k: (len(v), len(v[0]) if v else None, v[0][-2:] if v else None) for k, v in alls.items()})
