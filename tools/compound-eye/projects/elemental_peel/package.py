"""Build a portable focused supplement with original sources and hash inventory."""
from pathlib import Path
import hashlib,json,shutil,sys,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DEST=Path(sys.argv[1]).resolve();DEST.mkdir(parents=True,exist_ok=True)
stage=DEST/'Elemental_Peel_Complete';stage.mkdir(exist_ok=True)
for name in ['machine.py']:
 shutil.copy2(ROOT/name,stage/name)
for name in ['catalog','plugins']:
 shutil.copytree(ROOT/name,stage/name,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copytree(HERE,stage/'projects/elemental_peel',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
(stage/'START_HERE.md').write_text('''# Elemental Peel: complete focused supplement

Open projects/elemental_peel/Elemental_Peel_Observatory.html for live calculations.
Read that folder's README.md, FINDINGS.md, METHODS.md and paper section.
The registry preserves all 191 earlier definitions and adds seven new eyes.
This is a complete elemental supplement, not a replacement for every older
Universal dataset. The master repository retains the wider project.

For another chat: read those four documents, inspect data provenance, and run
the commands in the project README. Keep evaluated atomic data, measured
optical inputs, fitted response and synthetic electronic controls distinct.
''')
inv={str(p.relative_to(stage)):hashlib.sha256(p.read_bytes()).hexdigest() for p in stage.rglob('*') if p.is_file() and p.name!='SHA256.json'}
(stage/'SHA256.json').write_text(json.dumps(inv,indent=2)+'\n')
archive=DEST/'Elemental_Peel_Complete.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(stage.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(DEST))
for name in ['Elemental_Peel_Observatory.html','Elemental_Peel_Findings.png','FINDINGS.md','Elemental_Peel_Paper_Section.md']:
 target='Elemental_Peel_Findings.md' if name=='FINDINGS.md' else name
 shutil.copy2(HERE/name,DEST/target)
print(json.dumps({'zip':str(archive),'bytes':archive.stat().st_size,'hashed_files':len(inv)}))
