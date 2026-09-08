from pathlib import Path
import subprocess,sys,json,hashlib
p=Path(__file__).resolve().parent
for script in [p/'run_qhe.py',p/'projects/peeling_cascade/run_cascade.py',p/'run_upg.py',p/'run_diophantine.py']:
 subprocess.run([sys.executable,str(script)],cwd=p,check=True)
import machine
r=machine.Registry(p)
for ref,s in r.eyes.items():r.validate(s)
summary={'qhe':json.loads((p/'runs/qhe/summary.json').read_text()),'peeling':json.loads((p/'projects/peeling_cascade/verification.json').read_text()),'upg':json.loads((p/'projects/upg_integration/verification.json').read_text())['summary'],'registry_and_implementation_hashes_valid':True,'scope':'Focused QHE, peeling and UPG suites, not every historical research computation.'}
summary['diophantine']=json.loads((p/'projects/diophantine/verification.json').read_text())['summary']
summary['scope']='Focused QHE, peeling, UPG, and Diophantine suites; not every historical research computation.'
(p/'runs/universal_verification.json').write_text(json.dumps(summary,indent=2));print('Universal focused suite PASS')
