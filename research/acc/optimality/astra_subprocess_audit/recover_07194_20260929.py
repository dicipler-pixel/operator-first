"""Recover the completed audited beam; no API calls and no beam launch."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root = Path.cwd()
audit = root/'work/astra_resume_20260929T0328/subprocess_audit'
dest = root/'work/astra_recovery_20260929T1402'
dest.mkdir(exist_ok=True)
control = json.loads((root/'work/astra_recovery_20260929T1303/control.json').read_text())
assert control['passed']
for name, expected in control['binary_sha256'].items():
    assert hashlib.sha256((root/'bin'/name).read_bytes()).hexdigest() == expected
assert subprocess.check_output(['git','-C','SAIR','rev-parse','HEAD'], text=True).strip() == control['sair_pin']
assert not subprocess.check_output(['git','-C','SAIR','status','--porcelain','--untracked-files=no'], text=True).strip()
assert (root/'work/T8.tab').stat().st_size == 640000000
with (root/'work/T8.tab').open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest() == '38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8'
status = json.loads(subprocess.check_output(['python3','work/astra_recovery_20260929T1303/inspect.py'],text=True))
assert not status['processes'], status['processes']
receipts = [json.loads(s) for s in (audit/'executions.jsonl').read_text().splitlines()]
receipt = next(r for r in receipts if r['stdout_file'] == '1790689242864254695_acc_beam.stdout')
assert receipt['returncode'] == 0
targets = json.loads((root/'work/astra_wide_targets.json').read_text())
source = json.loads((root/'research/acc/live/targets_astra_wide_20260929T0720Z.json').read_text())
assert targets == source
assert json.loads((root/'work/astra_wide_first3.json').read_text()) == source[:3]
t = targets[1]
assert t['id'] == 'ac-07194'
sys.path.insert(0,str(root/'SAIR/competition/tools'))
from verifier import core, stable_core
manifest = json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch = {c['challenge_id']:c for c in manifest['challenges']}
E={1:0,-1:1,2:2,-2:3}; SW={1:2,-1:-2,2:1,-2:-1}
PI={6:8,8:6,7:9,9:7,10:12,12:10,11:13,13:11}
def enc(words):
    return [v for w in words for v in [str(len(w)),*[str(E[x]) for x in w]]]
assert receipt['command'] == ['bin/acc_beam','work/T8.tab','200000','46',*enc(ch[t['id']]['initial_relators'])]
def verify(board,path):
    result=(core if board=='ac' else stable_core).verify(ch[board+'-07194'],path,'ac-r2-v1' if board=='ac' else 'sac-r8-v1',manifest['limits'])
    assert result['ok'],result
    return result
raw=(audit/receipt['stdout_file']).read_text()
paths={b:list(map(int,re.search(r'^'+b.upper()+r' \d+ PATH ([\d ]+)',raw,re.M)[1].split())) for b in ('ac','sac')}
evidence={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'id':t['id'],'sair_pin':control['sair_pin'],
          'receipt':receipt,'raw_paths':paths,'raw_checks':{b:verify(b,p) for b,p in paths.items()},'windows':{}}
def save():
    (dest/'recovery.json').write_text(json.dumps(evidence,indent=2)+'\n')
save()
print('PIN/HASH/BINARIES PASS; raw AC49/SAC51 official-clean. Recovering windows, no repeated beam.',flush=True)
def window(board,words,path):
    wd=dest/('window_'+board); wd.mkdir(exist_ok=True)
    cmd=[str(root/'bin/acc_window'),str(wd),*enc(words),str(len(path)),*map(str,path)]
    old=next((r for r in receipts if r['command']==cmd),None)
    if old:
        output=(audit/old['stdout_file']).read_text()
        fallback=old.get('verified_input_fallback',{}).get('selected_path')
        rc=old['returncode']
        assert rc==0 or fallback is not None
    else:
        cp=subprocess.run(cmd,capture_output=True,text=True)
        output=cp.stdout; rc=cp.returncode
        fallback=getattr(cp,'astra_verified_window_path',None)
    match=re.search(r'FINALPATH ?([\d ]*)',output)
    result=fallback if fallback is not None else list(map(int,match[1].split())) if match else path
    evidence['windows'][board]={'command':cmd,'returncode':rc,'input_length':len(path),'output_length':len(result),'literal_path':result}
    save()
    return result
ac=window('ac',ch[t['id']]['initial_relators'],paths['ac'])
verify('ac',ac)
swapped=[[SW[x] for x in w] for w in ch[t['id']]['initial_relators']]
sac_core=window('sac',swapped,[PI.get(x,x) for x in paths['sac'][:-2]])
sac=[PI.get(x,x) for x in sac_core]+[15,15]
verify('sac',sac)
if len(paths['sac'])<len(sac): sac=paths['sac']
if len(ac)+2<len(sac): sac=ac+[16,15]
checks={'ac':verify('ac',ac),'sac':verify('sac',sac)}
rec={'id':t['id'],'record':t['record'],'k':t['k'],'checked':True,'seed':None,'noise':None,
     'ac_beam':len(paths['ac']),'sac_beam':len(paths['sac']),'ac':ac,'sac':sac,'ac_len':len(ac),'sac_len':len(sac),
     'wall_s':None,'verdict':'BEAT' if len(ac)<t['record'] else 'TIE' if len(ac)==t['record'] else 'above',
     'recovered_finished_beam_receipt':receipt['stdout_file'],'sair_pin':control['sair_pin'],'official_checks':checks}
out=root/'work/astra_wide_cap.jsonl'
done=[json.loads(l) for l in out.read_text().splitlines()]
previous=next((r for r in done if r['id']==t['id']),None)
if previous:
    assert previous['ac']==ac and previous['sac']==sac
else:
    with out.open('a') as f:
        f.write(json.dumps(rec)+'\n'); f.flush(); os.fsync(f.fileno())
evidence['completed_row']=rec
evidence['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
save()
print(json.dumps({k:v for k,v in rec.items() if k not in ('ac','sac','official_checks')}),flush=True)
