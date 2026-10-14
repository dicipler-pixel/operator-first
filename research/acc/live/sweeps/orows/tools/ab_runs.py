"""Song idea 2b runs: repo-current acc_beam with the abelian-shadow term (acc_beam_ab), dual-P2 settings, W, depth = SAC record.
Configs per row: control (term off), AB=1 (plain key), ABP=2 (P2 field); target J (ending (y,x)) unless the row's abelian distance prefers I.
Lines are replayed on the official cores; a line <= record goes to orows/HITS.txt at once."""
import json, sys, os, re, subprocess, gzip, time
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools'); from verifier import core, stable_core
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
R = '/home/user/operator-first'; HERE = os.path.dirname(os.path.abspath(__file__))
B = {}
for pfx in ('ac', 'stable_ac'):
    for x in json.load(gzip.open(f'{R}/research/acc/live/boards/{pfx}_20261014T0013Z.json.gz'))['data']['items']: B[x['challengeId']] = (x.get('currentBestLength'), x.get('kTeams'))
E = {1: 0, -1: 1, 2: 2, -2: 3}
W = sys.argv[1]; rows = sys.argv[2:]
BASE = dict(os.environ, BEAM_H='1', BEAM_DIV='0.8', BEAM_P2='2', BEAM_QUOTA='16', BEAM_ELITE='5000', BEAM_DUAL='0.75')
for spec in rows:
    n, tgt = spec.split(':')
    a, b = CH['ac-' + n]['initial_relators']; Ra, ka = B['ac-' + n]; Rs, ks = B['sac-' + n]
    st = [str(len(a)), *[str(E[t]) for t in a], str(len(b)), *[str(E[t]) for t in b]]
    for name, extra in (('ctrl', {}), ('AB1', {'BEAM_AB': '1', 'BEAM_ABT': tgt}), ('ABP2', {'BEAM_ABP': '2', 'BEAM_ABT': tgt})):
        t0 = time.time()
        p = subprocess.run([HERE + '/acc_beam_ab', '/root/.cache/acc_beam_bin/T8.tab', W, str(Rs), *st], capture_output=True, text=True, env=dict(BASE, **extra))
        res = {}
        for k in ('AC', 'SAC'):
            m = re.search(r'^%s \d+ PATH ([\d ]+)' % k, p.stdout, re.M)
            if m:
                line = list(map(int, m.group(1).split()))
                ok = core.verify(CH['ac-' + n], line, 'ac-r2-v1', LIM)['ok'] if k == 'AC' else stable_core.verify(CH['sac-' + n], line, 'sac-r8-v1', LIM)['ok']
                res[k] = len(line) if ok else 'BAD'
                rec, kk, rid = (Ra, ka, 'ac-' + n) if k == 'AC' else (Rs, ks, 'sac-' + n)
                if ok and len(line) <= rec:
                    open(R + '/research/acc/live/sweeps/orows/HITS.txt', 'a').write('# %d vs record %d (k%s), %s, orows song-hour beam (repo dual-P2 engine) config %s W%s; official core ok; method details at 02:55Z\n%s: [%s]\n' % (
                        len(line), rec, kk, 'BEAT' if len(line) < rec else 'TIE', name, W, rid, ', '.join(map(str, line))))
                    res[k + '_hit'] = True
        print(json.dumps({'row': n, 'cfg': name, 'target': tgt, 'W': W, 'AC': res.get('AC'), 'AC_rec': Ra, 'SAC': res.get('SAC'), 'SAC_rec': Rs, 'secs': round(time.time() - t0)}), flush=True)
