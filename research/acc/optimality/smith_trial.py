import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sair_root = Path(os.environ.get('SAIR_ROOT', 'SAIR'))
sys.path.insert(0, str(sair_root / 'competition' / 'tools'))
from verifier import core

manifest = json.loads((sair_root / 'competition' / 'tools' / 'verifier' / 'data' / 'manifest.json').read_text())
challenges = {c['challenge_id']: c for c in manifest['challenges']}
target_ids = ['ac-03305', 'ac-05558']
base_env = dict(os.environ, BEAM_H='1', BEAM_DIV='0.8', BEAM_P2='2',
                BEAM_QUOTA='16', BEAM_ELITE='5000', BEAM_DUAL='0.75')
letters = {1: 0, -1: 1, 2: 2, -2: 3}
out = []
for cid in target_ids:
    c = challenges[cid]
    r0, r1 = c['initial_relators']
    args = [os.environ.get('T8_PATH', 'work/T8.tab'), '20000', '35', str(len(r0)), *[str(letters[x]) for x in r0],
            str(len(r1)), *[str(letters[x]) for x in r1]]
    for name, exe, sf in [('base', 'bin/acc_beam', '0'), ('smith', 'bin/acc_beam_smith', '0.5')]:
        env = dict(base_env, BEAM_SMITH=sf)
        start = time.monotonic()
        p = subprocess.run([exe, *args], env=env, text=True, capture_output=True)
        rec = {'id': cid, 'arm': name, 'smith_fraction_of_second_eye': float(sf),
               'exit_code': p.returncode, 'wall_s': round(time.monotonic()-start, 2)}
        for kind in ('AC', 'SAC'):
            m = re.search(r'^' + kind + r' \d+ PATH ([\d ]+)', p.stdout, re.M)
            if m:
                path = [int(x) for x in m.group(1).split()]
                rec[kind.lower()] = path
                rec[kind.lower()+'_len'] = len(path)
                if kind == 'AC':
                    rec['verified'] = core.verify(c, path, 'ac-r2-v1', manifest['limits'])['ok']
        rec['stderr_tail'] = p.stderr.splitlines()[-3:]
        print({k:v for k,v in rec.items() if k not in ('ac','sac')}, flush=True)
        out.append(rec)
        Path('work/smith_trial.json').write_text(json.dumps(out, indent=2))
