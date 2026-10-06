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
sys.exit(subprocess.run([sys.executable, R + '/tools/acc/plan_offline.py', '--sair', a.sair, '--out', a.out + '/plan.json', lines], cwd=R).returncode)
