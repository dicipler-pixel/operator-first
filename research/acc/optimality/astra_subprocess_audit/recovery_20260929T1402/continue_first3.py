"""Wait for this identified recovery, then resume only the final pilot row."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root=Path.cwd()
pid=739246
start='4590474'
completion=root/'work/astra_recovery_20260929T1402/recovery.json'
print('Waiting for verified 07194 recovery; no beam running in this wrapper.',flush=True)
while True:
    recovered=json.loads(completion.read_text())
    if 'completed_row' in recovered:
        # The recovery has persisted all checks before writing this marker.
        assert recovered['completed_row']['id']=='ac-07194'
        assert all(v['ok'] for v in recovered['completed_row']['official_checks'].values())
        break
    p=Path('/proc')/str(pid)
    args=[s.decode() for s in (p/'cmdline').read_bytes().split(b'\0') if s]
    fields=(p/'stat').read_text().rsplit(')',1)[1].split()
    assert args==['python3','work/astra_recover_07194.py'] and fields[19]==start, 'Recovery process disappeared or identity changed; stop safely'
    time.sleep(5)
for key,want in {'BEAM_H':'1','BEAM_DIV':'0.8','BEAM_P2':'2','BEAM_QUOTA':'16','BEAM_ELITE':'5000','BEAM_DUAL':'0.75'}.items():
    assert os.environ[key]==want
assert not os.environ.get('BEAM_CHAIN')
subprocess.run([sys.executable,'work/astra_recovery_20260929T1402/prelaunch.py'],check=True)
cmd=['python3','research/acc/optimality/run_beam_raw.py',
     'SAIR/competition/tools/verifier/data/manifest.json','bin','work/T8.tab',
     'work/w_astra_wide','200000','200','work/astra_wide_cap.jsonl','work/astra_wide_first3.json']
print('Checks passed: resume only unfinished 05423; first-three file stops before row4.',flush=True)
os.execvpe(cmd[0],cmd,os.environ)
