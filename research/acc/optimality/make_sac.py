"""ACC_SAC_<date>.txt: Stable AC lines that improve on what the team already holds.
Sources: swap-finish paths (sac_swap.jsonl, < R+2) and exact-optimal AC paths + [16,15] (ties.jsonl, = R+2).
Also rewrites the AC tie file without rows already held at R. Every line replayed by the official CLI."""
import json, sys, subprocess, pathlib
work, sair, repo = map(pathlib.Path, sys.argv[1:4])
sys.path.insert(0, str(sair / 'competition/tools')); from verifier import stable_core
man = json.load(open(sair / 'competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
held = json.load(open(pathlib.Path(__file__).parent / 'held_from_history.json'))
rows = {r['row']: r for r in json.load(open(work / 'rows.json'))}
best = {}
for fn, kind in (('ties.jsonl', 'ac+2'), ('sac_swap.jsonl', 'swap')):
    f = work / fn
    if not f.exists(): continue
    for l in open(f):
        r = json.loads(l); sid = 'sac-' + r['row'][3:]
        if kind == 'ac+2' and r.get('official_core_verify', {}).get('ok'): p = r['path'] + [16, 15]
        elif kind == 'swap' and r.get('sac_verify', {}).get('ok'): p = r['sac_path']
        else: continue
        assert stable_core.verify(CH[sid], p, 'sac-r8-v1', man['limits'])['ok']
        if sid not in best or len(p) < len(best[sid][0]): best[sid] = (p, kind)
sac_lines = []
for sid, (p, kind) in sorted(best.items(), key=lambda kv: rows['ac-' + kv[0][4:]]['k']):
    h = held['sac'].get(sid)
    if h is None or len(p) < h:
        sac_lines.append(f"{sid}: {json.dumps(p).replace(' ', '')}  # {len(p)} moves via {kind}; team held {h}; AC record {rows['ac-'+sid[4:]]['R']}")
out = repo / 'ACC_SAC_20260924.txt'
out.write_text("# Stable AC lines improving on the team's held lengths (history of 2026-09-24); official stable verifier replayed\n" + "\n".join(sac_lines) + "\n")
# AC tie file minus rows already held at R
ac_lines = [l for l in (repo / 'ACC_TIES_20260924.txt').read_text().splitlines() if l.startswith('ac-')]
new_ac = [l for l in ac_lines if held['ac'].get(l.split(':')[0], 999) > rows[l.split(':')[0]]['R']]
(repo / 'ACC_TIES_NEW_20260924.txt').write_text("# AC tie lines not yet held by the team (per submission history)\n" + "\n".join(new_ac) + "\n")
for fn in ('ACC_SAC_20260924.txt', 'ACC_TIES_NEW_20260924.txt'):
    p = subprocess.run([sys.executable, '-m', 'verifier', '--manifest', 'competition/tools/verifier/data/manifest.json', '--submission', str(repo / fn)],
                       cwd=sair, env={'PYTHONPATH': 'competition/tools', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
    (repo / (fn + '.verify.json')).write_text(p.stdout + p.stderr)
    res = json.loads(p.stdout) if p.stdout.strip().startswith('{') else {}
    print(fn, 'accepted', res.get('accepted'), 'ok', sum(1 for x in res.get('results', []) if x.get('ok')), '/', len(res.get('results', [])))
print(len(sac_lines), 'SAC lines;', len(new_ac), 'new AC tie lines')
