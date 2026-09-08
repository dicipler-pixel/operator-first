#!/usr/bin/env python3
"""Create a complete portable ZIP with a per-file release manifest."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'compound_eye_modular_complete.zip'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def members():
 return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='RELEASE_MANIFEST.json')
def main():
 files=members()
 manifest={'format':'compound-eye-release-manifest-v1','release':'1.0.0','date':'2026-09-07','scope':'All packaged files except this manifest; original snapshots separately mapped by preservation_manifest.json.','files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
 (ROOT/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files+[ROOT/'RELEASE_MANIFEST.json']:z.write(p,'compound_eye_modular/'+p.relative_to(ROOT).as_posix())
 print(json.dumps({'zip':str(OUT),'bytes':OUT.stat().st_size,'files':len(files)+1,'sha256':sha(OUT)},indent=2))
if __name__=='__main__':main()
