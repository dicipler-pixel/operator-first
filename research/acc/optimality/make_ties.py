"""Build ACC_TIES_<date>.txt from ties.jsonl (only official-verified paths of exactly the record length)
and replay it with the official CLI."""
import json, sys, subprocess, pathlib
jl, rowsjson, sair, out = sys.argv[1:5]
rows = {r['row']: r for r in json.load(open(rowsjson))}
lines, total = [], 0.0
for l in open(jl):
    r = json.loads(l); x = rows[r['row']]
    if r.get('official_core_verify', {}).get('ok') and len(r['path']) == x['R']:
        lines.append(f"{r['row']}: {json.dumps(r['path']).replace(' ', '')}  # ties record {x['R']}, k={x['k']} (2026-09-14 snapshot), value 2^-{x['k']}")
        total += 2 ** -x['k']
pathlib.Path(out.replace('.txt', '_annotated.txt')).write_text("\n".join(lines) + "\n")
pathlib.Path(out).write_text("".join(l.split('  #')[0] + "\n" for l in lines))
print(f"{len(lines)} tie lines, value if k unchanged: {total:.4f}")
p = subprocess.run([sys.executable, '-m', 'verifier', '--manifest', 'competition/tools/verifier/data/manifest.json', '--submission', str(pathlib.Path(out).resolve()), '--pretty'],
                   cwd=sair, env={'PYTHONPATH': 'competition/tools', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
pathlib.Path(out + '.verify.json').write_text(p.stdout + p.stderr)
print(p.stdout[:1500], p.stderr[-800:])
