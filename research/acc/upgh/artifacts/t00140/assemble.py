"""Verify every `ac-XXXXX: [...]` line in the given raw files with the pinned core; write lines.txt with the
shortest verified path per row that is <= RECORD[row] (plus sac twin = moves + [16, 15]); print all verdicts.
usage: assemble.py OUT_LINES RAW1 [RAW2 ...]"""
import json, re, sys
SAIR = '/root/.cache/upgh/sair'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
RECORD = {'ac-01432': 41, 'ac-06752': 41, 'ac-00183': 44}
out = sys.argv[1]; best = {}; seen = set()
for fn in sys.argv[2:]:
    try: lines = open(fn).read().splitlines()
    except FileNotFoundError: continue
    for ln in lines:
        m = re.match(r'^(ac-\d{5}): (\[.*\])\s*$', ln)
        if not m: continue
        row, p = m.group(1), json.loads(m.group(2)); key = (row, tuple(p))
        if key in seen: continue
        seen.add(key)
        v = core.verify(CH[row], p, 'ac-r2-v1', man['limits'])
        print(fn, row, len(p), 'record', RECORD.get(row), 'verify:', json.dumps({k: v[k] for k in v if k != 'certificate_hash'}))
        if v['ok'] and (row not in best or len(p) < len(best[row])): best[row] = p
with open(out, 'w') as f:
    for row, p in sorted(best.items()):
        if len(p) <= RECORD.get(row, 10**9):
            f.write(f"{row}: {json.dumps(p).replace(' ', '')}\n")
            f.write(f"sac-{row[3:]}: {json.dumps(p + [16, 15]).replace(' ', '')}\n")
print("best verified per row:", {r: len(p) for r, p in best.items()})
