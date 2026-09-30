"""t00091 driver: replay a prefix on the pinned core, run acc_beam from the resulting state, parse AC/SAC paths,
replay prefix+finish on the pinned core (core.verify) and append ok routes to lines.txt.
usage: drive.py ROW W DMAX [--prefix 1,4,...] [--tag TAG]   (env BEAM_* passed through)"""
import sys, os, re, json, subprocess, time
SAIR = os.environ.get('SAIR', '/root/.cache/upgh/sair')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core
MAN = SAIR + '/competition/tools/verifier/data/manifest.json'
BIN = os.path.expanduser('~/.cache/upgh/bin'); TF = os.path.expanduser('~/.cache/upgh/T9.tab')
ART = '/home/user/operator-first/research/acc/upgh/artifacts/t00092'
E = {1: 0, -1: 1, 2: 2, -2: 3}; D = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
S = lambda r: ''.join(D[a] for a in r) or '1'
row, W, DMAX = sys.argv[1], sys.argv[2], sys.argv[3]
pre = []; tag = row
a = sys.argv[4:]
if '--prefix' in a: pre = [int(x) for x in a[a.index('--prefix') + 1].split(',') if x]
if '--tag' in a: tag = a[a.index('--tag') + 1]
ch = {c['challenge_id']: c for c in json.load(open(MAN))['challenges']}[row]
lim = json.load(open(MAN))['limits']
s = (tuple(ch['initial_relators'][0]), tuple(ch['initial_relators'][1]))
for m in pre: s = core.apply_move(s, m)
print(row, 'prefix', len(pre), 'state', S(s[0]), '|', S(s[1]), 'len', len(s[0]) + len(s[1]), flush=True)
enc = [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
t0 = time.time()
p = subprocess.run([BIN + '/acc_beam', TF, W, DMAX, *enc], capture_output=True, text=True)
open(f'{ART}/work/{tag}_W{W}.out', 'w').write(p.stdout + '\n---STDERR---\n' + p.stderr[-3000:])
print('beam wall', round(time.time() - t0, 1), 's; stdout tail:', p.stdout.strip().splitlines()[-3:], flush=True)
found = 0
for kind in ('AC', 'SAC'):
    for m in re.finditer(r'^%s \d+ PATH ([\d ]+)' % kind, p.stdout, re.M):
        fin = list(map(int, m.group(1).split()))
        if kind == 'AC':
            full = pre + fin
            r = core.verify(ch, full, ch['move_spec_version'], lim)
            print(kind, 'finish', len(fin), 'full', len(full), 'verify', r.get('ok'), r.get('code'), flush=True)
            if r.get('ok'):
                found += 1
                with open(f'{ART}/lines.txt', 'a') as f:
                    f.write(f'{row}: {json.dumps(full)}\n'); f.write(f's{row}: {json.dumps(full + [16, 15])}\n')
        else:
            print('SAC raw finish', len(fin), '(SAC path is in stable space; not composed here)', flush=True)
print('ok_routes', found)
