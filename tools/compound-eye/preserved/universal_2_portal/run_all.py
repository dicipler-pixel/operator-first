from pathlib import Path
import subprocess,sys,json,hashlib
p=Path(__file__).resolve().parent
for script in [p/'run_qhe.py',p/'projects/peeling_cascade/run_cascade.py']:
 subprocess.run([sys.executable,str(script)],cwd=p,check=True)
import machine
r=machine.Registry(p)
for ref,s in r.eyes.items():r.validate(s)
summary={'qhe':json.loads((p/'runs/qhe/summary.json').read_text()),'peeling':json.loads((p/'projects/peeling_cascade/verification.json').read_text()),'registry_and_implementation_hashes_valid':True,'scope':'Focused QHE and peeling suites, not every historical research computation.'}
(p/'runs/universal_verification.json').write_text(json.dumps(summary,indent=2));print('Universal focused suite PASS')
