"""Build path memory: one quick BEAM_H beam per AC row (no depth cap tied to the record), keep every
path that reaches (x,y), even if longer than the record. The states on these paths are what the
cross-row lookup (crossrow.py) uses: a row whose start is within a few moves of any stored state
borrows the rest of that path.
usage: path_memory.py SAIR BIN TFILE OUT.jsonl [--width 2000] [--dmax 120] [--workers 1]"""
import argparse, json, os, re, subprocess
from concurrent.futures import ThreadPoolExecutor
ap = argparse.ArgumentParser()
for a in ('sair', 'bin', 'tfile', 'out'): ap.add_argument(a)
ap.add_argument('--width', default='2000'); ap.add_argument('--dmax', default='120'); ap.add_argument('--workers', type=int, default=1); ap.add_argument('--maxrec', type=int, default=60); ap.add_argument('--live')
A = ap.parse_args()
man = json.load(open(A.sair + '/competition/tools/verifier/data/manifest.json'))
rows = [c for c in man['challenges'] if c['challenge_id'].startswith('ac-')]
if A.live:
    rec = {l.split()[0]: int(l.split()[1]) for l in open(A.live)}
    rows = sorted([c for c in rows if 0 < rec.get(c['challenge_id'], 0) <= A.maxrec], key=lambda c: rec[c['challenge_id']])
done = set()
if os.path.exists(A.out):
    for l in open(A.out):
        try: done.add(json.loads(l)['id'])
        except Exception: pass
rows = [c for c in rows if c['challenge_id'] not in done]
E = {1: 0, -1: 1, 2: 2, -2: 3}
def run(c):
    r0, r1 = c['initial_relators']
    enc = [str(len(r0))] + [str(E[a]) for a in r0] + [str(len(r1))] + [str(E[a]) for a in r1]
    try:
        p = subprocess.run([A.bin + '/acc_beam', A.tfile, A.width, A.dmax, *enc], capture_output=True, text=True,
                           env=dict(os.environ, BEAM_H='1', BEAM_DIV='1.0'), timeout=600)
        m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
    except subprocess.TimeoutExpired:
        m = None
    return {'id': c['challenge_id'], 'ac': list(map(int, m.group(1).split())) if m else None}
with ThreadPoolExecutor(A.workers) as ex, open(A.out, 'a') as f:
    for n, r in enumerate(ex.map(run, rows), 1):
        f.write(json.dumps(r) + '\n'); f.flush()
        if n % 250 == 0: print('progress', n, len(rows), flush=True)
print('MEMORY_DONE', flush=True)
