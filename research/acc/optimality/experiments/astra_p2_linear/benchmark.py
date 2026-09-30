"""Reproduce the isolated Astra least-rotation benchmark; does not alter acc_beam.c.

Run from the repository root, with SAIR and work/T8.tab already built:
  python3 research/acc/optimality/experiments/astra_p2_linear/benchmark.py
Results and isolated binaries are written to work/astra_p2_reproduction/.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
OUT = ROOT / 'work/astra_p2_reproduction'
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / 'research/acc/optimality/acc_beam.c'
original = SOURCE.read_text()
old = 'static int p2_minrot2(const char*d,int n){ int best=0; for(int i=1;i<n;i++){ if(memcmp(d+i,d+best,n)<0) best=i; } return best; }'
new = '''static int p2_minrot2(const char*d,int n){ int i=0,j=1,k=0;
  while(i<n&&j<n&&k<n){ unsigned char a=d[i+k],b=d[j+k]; if(a==b){ k++; continue; }
    if(a>b) i+=k+1; else j+=k+1; if(i==j) j++; k=0; }
  return i<j?i:j; }'''
assert original.count(old) == 1, 'Baseline function changed; inspect before adapting this experiment.'
variant = OUT / 'acc_beam_linear.c'
variant.write_text(original.replace(old, new))

def build(source, output):
    subprocess.run(['gcc', '-O3', '-march=native', '-I', str(SOURCE.parent), '-o', str(output), str(source), '-lm'], check=True)

build(HERE / 'check_minrot.c', OUT / 'check_minrot')
subprocess.run([str(OUT / 'check_minrot')], check=True)
build(SOURCE, OUT / 'base')
build(variant, OUT / 'linear')

sys.path.insert(0, str(ROOT / 'SAIR/competition/tools'))
from verifier import core, stable_core
manifest = json.loads((ROOT / 'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch = {c['challenge_id']: c for c in manifest['challenges']}
enc = {1: 0, -1: 1, 2: 2, -2: 3}
env = {k: v for k, v in os.environ.items() if not k.startswith('BEAM_')}
env.update(BEAM_H='1', BEAM_DIV='0.8', BEAM_P2='2', BEAM_QUOTA='16', BEAM_ELITE='500', BEAM_DUAL='0.75')
rows = []
for rep in range(3):
    for cid, depth in [('ac-01262', 57), ('ac-06403', 24), ('ac-06262', 45)]:
        args = [str(x) for word in ch[cid]['initial_relators'] for x in [len(word)] + [enc[a] for a in word]]
        outputs, logs = {}, {}
        for name in (['base', 'linear'] if rep % 2 == 0 else ['linear', 'base']):
            start = time.monotonic()
            p = subprocess.run([str(OUT / name), 'work/T8.tab', '2000', str(depth), *args], env=env, capture_output=True, text=True, check=True)
            wall = time.monotonic() - start
            prefix = OUT / f'{rep}_{cid}_{name}'
            prefix.with_suffix('.out').write_text(p.stdout)
            prefix.with_suffix('.err').write_text(p.stderr)
            checks = {}
            for kind, version, verifier in [('AC', 'ac-r2-v1', core), ('SAC', 'sac-r8-v1', stable_core)]:
                match = re.search(r'^' + kind + r' (\d+) PATH ([\d ]+)', p.stdout, re.M)
                if match:
                    moves = list(map(int, match.group(2).split()))
                    target = cid if kind == 'AC' else 's' + cid
                    checks[kind] = verifier.verify(ch[target], moves, version, manifest['limits'])
                    assert checks[kind]['ok'], checks[kind]
            outputs[name] = p.stdout
            logs[name] = re.sub(r'\d+\.\d+ s in P2', 'TIME s in P2', p.stderr)
            row = dict(id=cid, rep=rep, variant=name, width=2000, elite=500, depth=depth, wall_s=round(wall, 3), checks=checks)
            rows.append(row)
            print(json.dumps(row), flush=True)
            (OUT / 'results.json').write_text(json.dumps({'source_sha256': hashlib.sha256(original.encode()).hexdigest(), 'runs': rows}, indent=2) + '\n')
        assert outputs['base'] == outputs['linear'], (cid, 'different paths')
        assert logs['base'] == logs['linear'], (cid, 'different frontiers')
        print(cid + ': identical paths/frontiers; elapsed time excluded', flush=True)
