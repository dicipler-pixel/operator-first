#!/usr/bin/env python3
"""orows exact capped sweep (song-7 recipe: acc_capped + T8 finish, INIT_LOG2=26, budget per cap). acc_capped checks both
endings: AC (x,y) and Stable via (y,x) + [15,15] (its swap lookup) or AC + [16,15].
Scope of a miss: no AC route <= bestAC-1 / Stable line <= bestSAC-1 whose first MAXD moves keep total length <= CAP
(the last <= 8 moves are uncapped, T8). Every path is replayed on the pinned official core/stable_core; a line <= the record
goes into ../HITS.txt at once.
usage: capped_run.py ROW CAP MAXD BUDGET"""
import gzip, json, os, re, subprocess, sys, time, datetime, shutil
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools')
from verifier import core, stable_core
HERE = os.path.dirname(os.path.abspath(__file__)); R = '/home/user/operator-first'
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
B = {}
for pfx in ('ac', 'stable_ac'):
    for x in json.load(gzip.open(f'{R}/research/acc/live/boards/{pfx}_20261014T0013Z.json.gz'))['data']['items']:
        B[x['challengeId']] = (x.get('currentBestLength'), x.get('kTeams'))
n, cap, maxd, bud = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
E = {1: 0, -1: 1, 2: 2, -2: 3}
a, b = CH['ac-' + n]['initial_relators']
wd = '/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/orows/capwork_%s_%d' % (n, cap)
shutil.rmtree(wd, ignore_errors=True); os.makedirs(wd)
t0 = time.time()
env = dict(os.environ, MAXD=str(maxd), INIT_LOG2='26')
p = subprocess.run(['/root/.cache/acc_beam_bin/acc_capped', '/root/.cache/acc_beam_bin/T8.tab', str(cap), str(bud), wd, 'c', str(len(a)), *[str(E[t]) for t in a],
                    str(len(b)), *[str(E[t]) for t in b]], capture_output=True, text=True, env=env)
shutil.rmtree(wd, ignore_errors=True)
Ra, ka = B['ac-' + n]; Rs, ks = B['sac-' + n]
res = {'row': n, 'cap': cap, 'MAXD': maxd, 'budget': bud, 'secs': round(time.time() - t0)}
m = re.search(r'cap=\d+ states=(\d+) depth=(\d+) (CLOSED|STOPPED)', p.stdout)
if m: res.update(states=int(m.group(1)), depth=int(m.group(2)), status=m.group(3))
res['last_layers'] = p.stderr.strip().splitlines()[-2:]
hits = []
for kind in ('AC', 'SAC'):
    mm = re.search(r'\] %s (\d+) PATH ([\d ]+)' % kind, p.stdout)
    if not mm: res[kind] = None; continue
    path = list(map(int, mm.group(2).split()))
    if kind == 'AC':
        ok = core.verify(CH['ac-' + n], path, 'ac-r2-v1', LIM)['ok']; rec, k = Ra, ka; rid = 'ac-' + n
        if ok and not stable_core.verify(CH['sac-' + n], path + [16, 15], 'sac-r8-v1', LIM)['ok']: pass
    else:
        ok = stable_core.verify(CH['sac-' + n], path, 'sac-r8-v1', LIM)['ok']; rec, k = Rs, ks; rid = 'sac-' + n
    res[kind] = {'len': len(path), 'ok': ok, 'path': path}
    if ok and len(path) <= rec:
        hits.append('# orows exact capped %s cap %d MAXD %d: %s %d vs record %d (k%s) %s\n%s: [%s]\n' % (n, cap, maxd, kind, len(path), rec, k,
                    'BEAT' if len(path) < rec else 'TIE', rid, ', '.join(map(str, path))))
if hits:
    open(os.path.join(HERE, '..', 'HITS.txt'), 'a').write(''.join(hits))
res['hits'] = len(hits); res['utc'] = datetime.datetime.now(datetime.timezone.utc).strftime('%H:%MZ')
open(os.path.join(HERE, 'capped.jsonl'), 'a').write(json.dumps(res) + '\n'); print(json.dumps(res), flush=True)
