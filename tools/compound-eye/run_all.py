"""Run all five integrated scientific suites and the preserved mixer checks."""
from pathlib import Path
import json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'}
for script in ['run_qhe.py','projects/peeling_cascade/run_cascade.py','run_upg.py','run_diophantine.py','run_horizon.py']:
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True,env=env)
node=shutil.which('node')
if not node:raise RuntimeError('Node.js is required for complete mixer verification. Scientific suites completed; install Node and rerun for the full gate.')
for script in ['projects/eye_mixer/test_mixer.js','projects/eye_mixer/test_ui.js']:
    subprocess.run([node,str(ROOT/script)],cwd=ROOT,check=True)
import machine
registry=machine.Registry(ROOT)
summary={'release':'3.2','registry_and_implementation_hashes_valid':True,'eye_versions':len(registry.eyes),'sets':len(registry.sets),'scope':'Five focused scientific suites plus mixer algebra/UI harness; not every historical calculation or new Lean certification.'}
for name,path in [('qhe','runs/qhe/summary.json'),('peeling','projects/peeling_cascade/verification.json'),('upg','projects/upg_integration/verification.json'),('diophantine','projects/diophantine/verification.json'),('horizon','runs/horizon/summary.json'),('mixer_ui','runs/mixer/ui_verification.json')]:
    record=json.loads((ROOT/path).read_text());summary[name]=record.get('summary',record)
(ROOT/'runs/universal_verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Universal 3.2 integrated suite PASS')
