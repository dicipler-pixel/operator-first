"""Fast sweep of every solved AC row against the live board.

For each row: one BEAM_H beam of width W with the depth capped at (live AC record + 2). It only
returns a path when one exists within that cap, so a miss costs ~2 s at W=2000. Rows are ordered
by the value of a tie on AC + AC+[16,15] on Stable AC (fewest teams first). Every AC hit writes
the AC line and the SAC line AC+[16,15] to OUT.jsonl with the live records.
Nothing is verified or sent here: hits go through plan_offline.py and then the inbox.

usage: fast_sweep.py SAIR BIN TFILE OUT.jsonl [--width 2000] [--workers 2] [--kmax 3] [--start 0]
"""
import argparse, glob, gzip, json, os, re, subprocess
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
for a in ('sair', 'bin', 'tfile', 'out'): ap.add_argument(a)
ap.add_argument('--width', default='2000'); ap.add_argument('--workers', type=int, default=2)
ap.add_argument('--kmax', type=int, default=3); ap.add_argument('--start', type=int, default=0)
A = ap.parse_args()
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def board(p):
    f = sorted(glob.glob(f'{REPO}/research/acc/live/boards/{p}_2*.json.gz'))[-1]
    return {x['challengeId']: (x['currentBestLength'], x['kTeams']) for x in json.load(gzip.open(f))['data']['items']}
ac, sac = board('ac'), board('stable_ac')
man = json.load(open(A.sair + '/competition/tools/verifier/data/manifest.json'))
C = {c['challenge_id']: c for c in man['challenges']}
E = {1: 0, -1: 1, 2: 2, -2: 3}
done = set()
if os.path.exists(A.out):
    for l in open(A.out):
        try: done.add(json.loads(l)['id'])
        except Exception: pass
rows = []
for i, (r, k) in ac.items():
    if not r or i in done: continue
    sr, sk = sac['s' + i]
    if min(k, sk) > A.kmax: continue
    val = 2 ** (1 - (k + 1)) + (2 ** (1 - (sk + 1)) if sr and r + 2 <= sr else 0)
    rows.append((-val, r, i))
rows.sort(); rows = rows[A.start:]
print(f'{len(rows)} rows to sweep (kmax {A.kmax}, width {A.width})', flush=True)

def run(item):
    _, r, i = item
    r0, r1 = C[i]['initial_relators']
    enc = [str(len(r0))] + [str(E[a]) for a in r0] + [str(len(r1))] + [str(E[a]) for a in r1]
    env = dict(os.environ, BEAM_H='1', BEAM_DIV='1.0')
    try:
        p = subprocess.run([A.bin + '/acc_beam', A.tfile, A.width, str(r + 2), *enc], capture_output=True, text=True, env=env, timeout=900)
        m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
    except subprocess.TimeoutExpired:
        m = None
    rec = {'id': i, 'live': ac[i][0], 'k': ac[i][1], 'slive': sac['s' + i][0], 'sk': sac['s' + i][1]}
    if m:
        path = list(map(int, m.group(1).split()))
        rec.update(ac=path, sac=path + [16, 15])
    return rec

with ThreadPoolExecutor(A.workers) as ex, open(A.out, 'a') as f:
    for n, rec in enumerate(ex.map(run, rows), 1):
        f.write(json.dumps(rec) + '\n'); f.flush()
        if 'ac' in rec:
            a = len(rec['ac'])
            print(f"HIT {rec['id']} ac {a} (live {rec['live']}/k{rec['k']}) sac {a + 2} (live {rec['slive']}/k{rec['sk']})", flush=True)
        if n % 200 == 0: print(f'progress {n}/{len(rows)}', flush=True)
print('SWEEP_DONE', flush=True)
