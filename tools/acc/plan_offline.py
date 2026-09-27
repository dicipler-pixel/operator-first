"""Offline version of `sair_api.py plan` for a session with no SAIR network access.
Uses the newest pulled boards and mine_*.json in research/acc/live, plus the official verifier.
usage: plan_offline.py FILE... --sair DIR --out OUT"""
import argparse, glob, gzip, json, os, re, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument('files', nargs='+'); ap.add_argument('--sair', required=True); ap.add_argument('--out', required=True)
A = ap.parse_args(); L = 'research/acc/live'
board = {}
for p in ('ac', 'stable_ac'):
    f = sorted(glob.glob(f'{L}/boards/{p}_*.json.gz'))[-1]
    for x in json.load(gzip.open(f))['data']['items']: board[x['challengeId']] = (x['currentBestLength'], x['kTeams'])
mine = {}
for it in json.load(open(sorted(glob.glob(f'{L}/mine_*.json'))[-1]))['items']:
    for r in it.get('results') or []:
        if r.get('ok'): mine[r['challenge_id']] = min(mine.get(r['challenge_id'], 1 << 30), r['length'])
lines = {}
for fn in A.files:
    for l in open(fn):
        m = re.match(r'^(s?ac-\d{5}):\s*(\[.*\])\s*$', l.strip())
        if m:
            p = json.loads(m.group(2))
            if m.group(1) not in lines or len(p) < len(lines[m.group(1)]): lines[m.group(1)] = p
ok = set(); items = list(lines.items())
for c in range(0, len(items), 400):  # the verifier accepts at most 500 solutions per file
    tmp = A.out + '.chunk'; open(tmp, 'w').write(''.join(f'{i}: {json.dumps(p).replace(" ", "")}\n' for i, p in items[c:c + 400]))
    r = json.loads(subprocess.run([sys.executable, '-m', 'verifier', '--manifest', 'competition/tools/verifier/data/manifest.json', '--submission', os.path.abspath(tmp)],
                                  cwd=A.sair, env=dict(os.environ, PYTHONPATH='competition/tools'), capture_output=True, text=True).stdout)
    if not r.get('results'): print('verifier batch error:', {k: r.get(k) for k in ('code', 'detail')})
    ok |= {x['challenge_id'] for x in r.get('results', []) if x.get('ok')}
    os.remove(tmp)
keep = []
for i, p in lines.items():
    rec, k = board.get(i, (None, 0)); n = len(p); ours = mine.get(i)
    if i not in ok: v = 'REJECTED'
    elif ours is not None and ours <= n: v = f'already sent ({ours})'
    elif rec is None: v = 'UNSOLVED'
    elif n < rec: v = 'BEAT'
    elif n == rec: v = 'TIE'
    else: v = f'+{n - rec}'
    print(f'{i:10} {n:4} live {rec}/k{k}  -> {v}')
    if v in ('UNSOLVED', 'BEAT', 'TIE'): keep.append((0 if v != 'TIE' else 1, k, i, p))
keep.sort(); open(A.out, 'w').write(''.join(f'{i}: {json.dumps(p).replace(" ", "")}\n' for _, _, i, p in keep))
print(f'wrote {A.out}: {len(keep)} scoring lines')
