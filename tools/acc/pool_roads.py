"""Pool every verified AC road we hold into one jsonl ({"id","ac"}), keeping distinct roads per row.
Sources: ac- lines and {"id","ac"} records in tracked repo files, the graph-map archive, route maps, and any
extra jsonl/txt files given. Each road is replayed with the official kernel.
usage: pool_roads.py SAIR OUT.jsonl [EXTRA_FILES...]"""
import glob, gzip, json, os, re, subprocess, sys
sair, out, extra = sys.argv[1], sys.argv[2], sys.argv[3:]
sys.path.insert(0, sair + '/competition/tools'); from verifier import core
man = json.load(open(sair + '/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in man['challenges']}
roads = set()
def add(i, p):
    if i in C and i.startswith('ac-') and isinstance(p, list) and p and all(isinstance(x, int) and 0 <= x < 14 for x in p): roads.add((i, tuple(p)))
pat = re.compile(r'"?(ac-\d{5})"?\s*[:,=]?\s*(?:"(?:path|ac|moves)"\s*:\s*)?(\[[\d,\s]{3,}\])')
def scan_text(s):
    for m in pat.finditer(s):
        try: add(m.group(1), json.loads(m.group(2)))
        except Exception: pass
def scan_jsonl(f):
    for l in open(f, errors='ignore'):
        try: r = json.loads(l)
        except Exception: continue
        if isinstance(r, dict): add(r.get('id'), r.get('ac'))
files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True).stdout.split()
for f in files:
    if f.endswith(('.txt', '.md', '.json', '.jsonl')) and os.path.isfile(f) and os.path.getsize(f) < 200e6:
        s = open(f, errors='ignore').read(); scan_text(s)
        if f.endswith('.jsonl'): scan_jsonl(f)
g = 'research/acc/graphmaps/2026-09-27/route_maps.jsonl.gz'
if os.path.exists(g):
    for l in gzip.open(g, 'rt'):
        r = json.loads(l)
        if r.get('spec') == 'ac-r2-v1': add(r['challenge_id'], r['moves'])
for f in glob.glob('research/acc/optimality/*map*.json'):
    try: d = json.load(open(f)); i = re.search(r'(ac-\d{5})', f).group(1)
    except Exception: continue
    for rt in (d.get('routes', []) if isinstance(d, dict) else []): add(i, rt.get('move_ids') or rt.get('moves'))
for f in extra:
    if f.endswith('.jsonl'): scan_jsonl(f)
    else: scan_text(open(f, errors='ignore').read())
ok = [(i, p) for i, p in roads if core.verify(C[i], list(p), 'ac-r2-v1', man['limits'])['ok']]
with open(out, 'w') as fo:
    for i, p in sorted(ok): fo.write(json.dumps({'id': i, 'ac': list(p)}) + '\n')
print('roads', len(roads), 'verified', len(ok), 'rows', len({i for i, _ in ok}))
