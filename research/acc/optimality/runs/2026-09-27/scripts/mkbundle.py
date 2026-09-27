import base64
src={n:base64.b64encode(open(n,'rb').read()).decode() for n in ['acc_opt.c','acc_beam.c','acc_window.c','run_beam.py']}
body=r'''#!/usr/bin/env python3
"""Mad Hatters ACC search bundle for Colab / any Linux box (self-contained).

  1. clones the official SAIR repo pinned at a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e (verifier + manifest)
  2. writes and compiles our C engine (acc_beam = beam search + exact finish table; acc_window = exact shortening)
  3. builds the exact finish table T_R around (x,y)  (R=8: 24.6M states, 512 MB; R=9: 215M states, 4.5 GB)
  4. runs the beam per target, finishes exactly via T_R, shortens, derives the Stable AC line,
     and replays every path through the OFFICIAL SAIR verifier
  5. prints clean submission lines only for paths the official CLI accepts

Colab:  !python3 colab_acc_search.py --targets ac-00048:98:1,ac-00046:117:1 --width 200000 --radius 8 --div 0.6
  targets are id:record:k  (record 999 for never-solved rows)
"""
import argparse, base64, json, os, subprocess, sys
SRC = __SRC__
ap = argparse.ArgumentParser()
ap.add_argument('--targets', required=True); ap.add_argument('--width', default='200000')
ap.add_argument('--dmax', default='600'); ap.add_argument('--radius', type=int, default=8, choices=[8, 9])
ap.add_argument('--div', default=None); ap.add_argument('--root', default='acc_run')
a = ap.parse_args()
R = os.path.abspath(a.root); os.makedirs(R + '/work', exist_ok=True); os.chdir(R)
def sh(c): print('+', c, flush=True); subprocess.run(c, shell=True, check=True)
if not os.path.isdir('sair'):
    sh('git clone -q https://github.com/SAIRcompetition/Andrews-Curtis sair && cd sair && git checkout -q a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e')
for n, b in SRC.items(): open(n, 'wb').write(base64.b64decode(b))
sh('gcc -O3 -o acc_opt acc_opt.c -lm && gcc -O3 -o acc_beam acc_beam.c -lm && gcc -O3 -o acc_window acc_window.c -lm')
slots = {8: 32000000, 9: 280000000}[a.radius]; T = 'T%d.tab' % a.radius
if not os.path.exists(T): sh('./acc_opt tball %d %d %s work' % (a.radius, slots, T))
tg = []
for x in a.targets.split(','):
    i, rec, k = x.strip().split(':'); tg.append({'id': i, 'record': int(rec), 'k': int(k)})
json.dump(tg, open('targets.json', 'w'))
env = dict(os.environ)
if a.div: env['BEAM_DIV'] = a.div
subprocess.run([sys.executable, 'run_beam.py', R + '/sair', R, R + '/' + T, R + '/work', a.width, a.dmax, R + '/results.jsonl', 'targets.json'], env=env)
lines = []
for l in open('results.jsonl'):
    r = json.loads(l)
    print('RESULT', r['id'], 'record', r['record'], 'AC', r.get('ac_len'), 'SAC', r.get('sac_len'), r.get('verdict'), flush=True)
    for kind in ('ac', 'sac'):
        if r.get(kind): lines.append('%s-%s: %s' % (kind, r['id'][3:], str(r[kind]).replace(' ', '')))
if lines:
    open('submission.txt', 'w').write('\n'.join(lines) + '\n')
    out = subprocess.run('cd sair && PYTHONPATH=competition/tools %s -m verifier --manifest competition/tools/verifier/data/manifest.json --submission %s/submission.txt' % (sys.executable, R), shell=True, capture_output=True, text=True).stdout
    ok = {x['challenge_id'] for x in json.loads(out)['results'] if x['ok']}
    print('\n=== OFFICIAL CLI accepted %d of %d. Clean lines: ===' % (len(ok), len(lines)))
    for l in lines:
        if l.split(':')[0] in ok: print(l)
else:
    print('No paths found for these targets.')
'''
open('/home/user/operator-first/tools/acc/colab_acc_search.py','w').write(body.replace('__SRC__', repr(src)))
