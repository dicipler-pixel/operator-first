"""Offline sanitizer diagnostic of the known positive window control."""
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

root=Path.cwd(); wd=root/'work/astra_window_sanitize_20260929'
control=json.loads((root/'work/astra_recovery_20260929T1303/control.json').read_text())
cmd=control['window_control']['command'].copy()
cmd[0]=str(wd/'acc_window_sanitize');cmd[1]=str(wd/'window')
Path(cmd[1]).mkdir(exist_ok=True)
record={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'command':cmd,'stage':'running','production_unchanged':True}
(wd/'result.json').write_text(json.dumps(record,indent=2)+'\n')
t0=time.monotonic();env=dict(os.environ,ASAN_OPTIONS='detect_leaks=0:abort_on_error=1')
with (wd/'stdout').open('w') as out,(wd/'stderr').open('w') as err:
    result=subprocess.run(cmd,stdout=out,stderr=err,env=env)
record.update(stage='finished',returncode=result.returncode,seconds=time.monotonic()-t0)
sys.path.insert(0,str(root/'SAIR/competition/tools'))
from verifier import core
manifest=json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch=next(c for c in manifest['challenges'] if c['challenge_id']=='ac-04953')
output=(wd/'stdout').read_text();error=(wd/'stderr').read_text()
record['candidate_checks']=[]
for m in re.finditer(r'^(?:PATH|FINALPATH) ?([\d ]*)$',output,re.M):
    path=list(map(int,m[1].split()));record['candidate_checks'].append({'moves':path,'check':core.verify(ch,path,'ac-r2-v1',manifest['limits'])})
record['sanitizer_report']='AddressSanitizer' in error or 'runtime error:' in error
record['stderr_tail']=error[-10000:]
(wd/'result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'returncode':result.returncode,'seconds':record['seconds'],'sanitizer_report':record['sanitizer_report'],'candidates':[(len(x['moves']),x['check']['ok']) for x in record['candidate_checks']]}),flush=True)
