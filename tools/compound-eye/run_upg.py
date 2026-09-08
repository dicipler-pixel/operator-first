from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'projects/upg_integration/verify_upg.py'),'--instrument-root',str(root)],check=True)
