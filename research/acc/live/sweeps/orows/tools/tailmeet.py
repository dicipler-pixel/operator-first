"""Tail meet: for every state on every road we hold for a row (AC roads to (x,y) and AC-move prefixes of Stable lines),
take the shortest prefix index p at which we reach it, and compute the EXACT distance to (x,y) and to (y,x)
(the latter via the letter swap x<->y, moves 6<->8, 7<->9, 10<->12, 11<->13) with acc_batch (S_A ∩ T8; exact up to A+8).
AC line  = prefix + route to (x,y);  Stable line = prefix + route to (x,y) + [16,15]  or  prefix + route to (y,x) + [15,15].
Every candidate is replayed on the official pinned cores.
usage: python3 tailmeet.py A ROWNUM [ROWNUM ...]   (ROWNUM like 01784)"""
import json, sys, gzip, subprocess, os, time
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools')
from verifier import core, stable_core
S = os.path.dirname(os.path.abspath(__file__)); REPO = '/home/user/operator-first'
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
B = {}
for pfx in ('ac', 'stable_ac'):
    for x in json.load(gzip.open(f'{REPO}/research/acc/live/boards/{pfx}_20261014T0013Z.json.gz'))['data']['items']:
        B[x['challengeId']] = (x.get('currentBestLength'), x.get('kTeams'))
AC = json.load(open(S + '/all_ac_roads.json')); SAC = json.load(open(S + '/all_sac_lines.json'))
PI = [0, 1, 2, 3, 4, 5, 8, 9, 6, 7, 12, 13, 10, 11]
ENC = {1: 0, -1: 1, 2: 2, -2: 3}
XY = ((1,), (2,)); YX = ((2,), (1,))
def sw(s): return tuple(tuple((3 - abs(t)) * (1 if t > 0 else -1) for t in w) for w in s)
def enc(s): return ' '.join(str(len(w)) + ''.join(' %d' % ENC[t] for t in w) for w in s)
A = int(sys.argv[1]); rows = sys.argv[2:]
for n in rows:
    t0 = time.time()
    Ra, ka = B.get('ac-' + n); Rs, ks = B.get('sac-' + n)
    start = tuple(tuple(w) for w in CH['ac-' + n]['initial_relators'])
    seqs = [p for p in AC.get('ac-' + n, [])]
    for l in SAC.get('sac-' + n, []):
        body = l[:-2]
        if all(0 <= m <= 13 for m in body): seqs.append(body)
    best_p = {}  # state -> (p, prefix moves)
    for p in seqs:
        s = start; pre = []
        for k in range(len(p) + 1):
            if s not in best_p or k < best_p[s][0]: best_p[s] = (k, p[:k])
            if k < len(p): s = core.apply_move(s, p[k])
    lo = min(Ra, Rs - 2) - (A + 8); hi = max(Ra, Rs - 2)
    cand = {s: v for s, v in best_p.items() if lo <= v[0] < hi}
    # current bests from what we hold
    have_ac = min((len(p) for p in AC.get('ac-' + n, [])), default=999)
    have_s = min([len(l) for l in SAC.get('sac-' + n, [])] + [have_ac + 2])
    lines = []; keys = []
    for i, (s, (p, pre)) in enumerate(cand.items()):
        lines.append('x%d %s' % (i, enc(s))); lines.append('y%d %s' % (i, enc(sw(s)))); keys.append(s)
    wd = S + '/work_tm_' + n; os.makedirs(wd, exist_ok=True)
    out = subprocess.run([S + '/bin/acc_batch', '/root/.cache/acc_beam_bin/T8.tab', '8', str(A), wd], input='\n'.join(lines) + '\n',
                         capture_output=True, text=True).stdout
    bac = (have_ac, None); bs = (have_s, None)
    for ln in out.splitlines():
        f = ln.split()
        if 'dist=' not in ln: continue
        tag = f[0]; i = int(tag[1:]); s = keys[i]; p, pre = cand[s]
        d = int([x for x in f if x.startswith('dist=')][0][5:])
        path = list(map(int, f[f.index('path') + 1:])) if 'path' in f else []
        if tag[0] == 'x':
            line = pre + path
            if len(line) < bac[0] and core.verify(CH['ac-' + n], line, 'ac-r2-v1', LIM)['ok']: bac = (len(line), line)
            sl = line + [16, 15]
        else:
            sl = pre + [PI[m] for m in path] + [15, 15]
        if len(sl) < bs[0] and stable_core.verify(CH['sac-' + n], sl, 'sac-r8-v1', LIM)['ok']: bs = (len(sl), sl)
    print(json.dumps({'row': n, 'A': A, 'states': len(cand), 'roads': len(seqs), 'AC_record': Ra, 'AC_k': ka, 'AC_have': have_ac, 'AC_best': bac[0],
                      'SAC_record': Rs, 'SAC_k': ks, 'SAC_have': have_s, 'SAC_best': bs[0], 'secs': round(time.time() - t0, 1)}), flush=True)
    for tag, (L, line) in (('ac-' + n, bac), ('sac-' + n, bs)):
        if line is not None:
            print('NEW %s %d %s' % (tag, L, json.dumps(line)), flush=True)
