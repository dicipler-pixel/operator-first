"""Run the combined-paper supplement without editing any code."""
from pathlib import Path
import argparse,json,hashlib,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--include-elemental',action='store_true',help='Also replay the prior Au/Ag/Cu/Pt and Maxwell-film studies');args=ap.parse_args()
for f in ['run_experiments.py','run_source_controls.py','build_figures.py']:
 subprocess.run([sys.executable,str(P/f)],cwd=ROOT,check=True)
for f in ['verify_compound_eye_release.py','validate_catalog.py']:
 if (ROOT/'scripts'/f).is_file():subprocess.run([sys.executable,str(ROOT/'scripts'/f)],cwd=ROOT,check=True)
if args.include_elemental:
 E=ROOT/'tools/compound-eye/projects/elemental_peel'
 for f in ['run_study.py','extend_observations.py']:subprocess.run([sys.executable,str(E/f)],cwd=E,check=True)
print('Combined-paper reproduction completed. Formal and physical status remain as described in PROOF_STATUS.md.')
