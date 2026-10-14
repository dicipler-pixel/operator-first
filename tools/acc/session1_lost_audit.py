"""Lost-submission audit (session 1 method, Moves Manual 2.3). Plain script, no model, no API.
Harvests every `s?ac-NNNNN: [...]` line (and {"id","ac","sac"} jsonl records) under research/acc
plus any extra dirs given, keeps the 3 shortest distinct roads per row, and runs plan_offline.py on
the newest cached boards. Anything it prints as TIE/BEAT/UNSOLVED that is not 'already sent' is a
line nobody turned in.
usage: python3 tools/acc/session1_lost_audit.py --sair SAIR_CHECKOUT [--extra DIR ...] [--out DIR]"""
import argparse, json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ap = argparse.ArgumentParser(); ap.add_argument('--sair', required=True)
ap.add_argument('--extra', nargs='*', default=[]); ap.add_argument('--out', default='/tmp/lost_audit')
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
pat = re.compile(r'(s?ac-\d{5}):\s*(\[[0-9,\s]+\])'); seen = {}
def add(i, q):
    if isinstance(q, str):
        try: q = json.loads(q)
        except Exception: return
    if q: seen.setdefault(i, set()).add(tuple(q))
for root in [R + '/research/acc'] + a.extra:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if not f.endswith(('.txt', '.md', '.jsonl', '.json')): continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 60_000_000: continue
                t = open(p, errors='ignore').read()
            except Exception: continue
            for m in pat.finditer(t): add(m.group(1), m.group(2))
            if f.endswith('.jsonl'):
                for l in t.splitlines():
                    try: d = json.loads(l)
                    except Exception: continue
                    if isinstance(d, dict) and str(d.get('id', '')).startswith('ac-'):
                        if isinstance(d.get('ac'), list): add(d['id'], d['ac'])
                        if isinstance(d.get('sac'), list): add('s' + d['id'], d['sac'])
lines = a.out + '/harvest.txt'
with open(lines, 'w') as f:
    for i, ps in sorted(seen.items()):
        for q in sorted(ps, key=len)[:3]: f.write('%s: %s\n' % (i, json.dumps(list(q)).replace(' ', '')))
print('harvested', sum(min(3, len(v)) for v in seen.values()), 'lines on', len(seen), 'rows ->', lines, file=sys.stderr)
# plan_offline checks only the shortest line per row, so a junk short line (a doc example) would hide a real
# road on the same row. Verify every line first and hand plan_offline only the verified ones.
good = []; items = [l.split(': ', 1) for l in open(lines).read().splitlines()]
for c in range(0, len(items), 400):
    pending = items[c:c + 400]
    while pending:
        ids = set(); batch = []; rest = []
        for i, p in pending: (rest if i in ids else batch).append((i, p)); ids.add(i)
        tmp = a.out + '/chunk.txt'; open(tmp, 'w').write(''.join(f'{i}: {p}\n' for i, p in batch))
        r = json.loads(subprocess.run([sys.executable, '-m', 'verifier', '--manifest', 'competition/tools/verifier/data/manifest.json', '--submission', tmp],
                                      cwd=a.sair, env=dict(os.environ, PYTHONPATH='competition/tools'), capture_output=True, text=True).stdout)
        ok = {x['challenge_id'] for x in r.get('results', []) if x.get('ok')}
        good += [(i, p) for i, p in batch if i in ok]; pending = rest
vf = a.out + '/verified.txt'; open(vf, 'w').write(''.join(f'{i}: {p}\n' for i, p in good))
print('verified', len(good), 'of', len(items), '->', vf, file=sys.stderr)
sys.exit(subprocess.run([sys.executable, R + '/tools/acc/plan_offline.py', '--sair', a.sair, '--out', a.out + '/plan.txt', vf], cwd=R).returncode)
