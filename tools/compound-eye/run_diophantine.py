from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
project=root/'projects/diophantine'
subprocess.run([sys.executable,str(project/'run_experiment.py')],check=True)
subprocess.run([sys.executable,str(project/'verify_diophantine.py'),'--instrument-root',str(root)],check=True)
