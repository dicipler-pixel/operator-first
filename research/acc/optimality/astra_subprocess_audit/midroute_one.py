"""One lead-authorized mid-route restart, gated by the completed wide pilot.

Run with the existing audited subprocess environment. No networking or inbox writes.
Usage: python3 work/astra_midroute_one.py ac-04316 28 [--prepare]
"""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

root=Path.cwd()
cid=sys.argv[1]; cut=int(sys.argv[2]); prepare='--prepare' in sys.argv[3:]
targets=json.loads((root/'work/astra_wide_targets.json').read_text())
t=next(t for t in targets if t['id']==cid)
rows=[json.loads(l) for l in (root/'work/astra_wide_cap.jsonl').read_text().splitlines()]
source=next(r for r in rows if r['id']==cid)
path=source['ac']
assert 0<cut<len(path)-14, 'Do not duplicate a suffix covered by span14'
manifest=json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch={c['challenge_id']:c for c in manifest['challenges']}
sys.path.insert(0,str(root/'SAIR/competition/tools'))
from verifier import core,stable_core
PIN='a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
def verify(board,moves):
    v=core if board=='ac' else stable_core
    result=v.verify(ch[board+'-'+cid.split('-')[1]],moves,'ac-r2-v1' if board=='ac' else 'sac-r8-v1',manifest['limits'])
    assert result['ok'],result
    return result
verify('ac',path)
state=tuple(tuple(w) for w in ch[cid]['initial_relators'])
for move in path[:cut]: state=core.apply_move(state,move)
literal=dict(challenge_id='midroute-literal',move_spec_version='ac-r2-v1',initial_relators=[list(w) for w in state],target_relators=[[1],[2]])
check=core.verify(literal,path[cut:],'ac-r2-v1',manifest['limits']);assert check['ok'],check
E={1:0,-1:1,2:2,-2:3}; SW={1:2,-1:-2,2:1,-2:-1}
PI={6:8,8:6,7:9,9:7,10:12,12:10,11:13,13:11}
def enc(words): return [x for w in words for x in [str(len(w)),*[str(E[x]) for x in w]]]
dm=t['record']-cut
cmd=['bin/acc_beam','work/T8.tab','200000',str(dm),*enc(state)]
source_hash=hashlib.sha256(json.dumps(path,separators=(',',':')).encode()).hexdigest()
job={'id':cid,'cut':cut,'prefix':path[:cut],'source_path':path,'source_path_sha256':source_hash,
     'record':t['record'],'sac_record':t['sac_record'],'width':200000,'DMAX':dm,'command':cmd,
     'state':[list(w) for w in state],'old_suffix_check':check,'sair_pin':PIN}
if prepare:
    print(json.dumps(job));raise SystemExit(0)
assert len(rows)==3 and [r['id'] for r in rows]==[x['id'] for x in targets[:3]], 'Finish and assess the first3 first'
for r in rows:
    target=next(x for x in targets if x['id']==r['id'])
    for board in ('ac','sac'):
        if board in r:
            verify_id=board+'-'+r['id'].split('-')[1]
            result=(core if board=='ac' else stable_core).verify(ch[verify_id],r[board],'ac-r2-v1' if board=='ac' else 'sac-r8-v1',manifest['limits'])
            assert result['ok'],result
            assert len(r[board])-target[board+'_record']>=target['gap_'+board], 'Wide pilot gained; do not switch automatically'
assert subprocess.check_output(['git','-C','SAIR','rev-parse','HEAD'],text=True).strip()==PIN
assert not subprocess.check_output(['git','-C','SAIR','status','--porcelain','--untracked-files=no'],text=True).strip()
ctl=json.loads((root/'work/astra_recovery_20260929T1303/control.json').read_text());assert ctl['passed']
for name,expected in ctl['binary_sha256'].items():assert hashlib.sha256((root/'bin'/name).read_bytes()).hexdigest()==expected
assert (root/'work/T8.tab').stat().st_size==640000000
with (root/'work/T8.tab').open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()=='38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8'
for key,value in {'BEAM_H':'1','BEAM_DIV':'0.8','BEAM_P2':'2','BEAM_QUOTA':'16','BEAM_ELITE':'5000','BEAM_DUAL':'0.75'}.items():assert os.environ[key]==value
assert not os.environ.get('BEAM_CHAIN')
assert os.environ.get('ASTRA_SUBPROCESS_AUDIT_DIR') and os.environ.get('ASTRA_VERIFIED_WINDOW_FALLBACK')=='1'
status=json.loads(subprocess.check_output(['python3','work/astra_recovery_20260929T1303/inspect.py'],text=True))
assert not any(Path(p['command'][0]).name in ('acc_beam','acc_window') or any(Path(a).name=='run_beam_raw.py' for a in p['command'][1:]) for p in status['processes'])
wd=root/'work/astra_midroute'/f'{cid}_cut{cut}_{source_hash[:12]}'
wd.mkdir(parents=True,exist_ok=True)
assert not (wd/'result.json').exists(), 'Already completed: reuse result'
audit=Path(os.environ['ASTRA_SUBPROCESS_AUDIT_DIR'])
receipts=[json.loads(l) for l in (audit/'executions.jsonl').read_text().splitlines()]
old=next((r for r in receipts if r['command']==cmd),None)
if old:
    assert old['returncode']==0
    output=(audit/old['stdout_file']).read_text()
else:
    cp=subprocess.run(cmd,capture_output=True,text=True)
    output=cp.stdout
(wd/'beam.stdout').write_text(output)
def window(board,words,moves):
    wdir=wd/board;wdir.mkdir(exist_ok=True)
    command=[str(root/'bin/acc_window'),str(wdir),*enc(words),str(len(moves)),*map(str,moves)]
    fresh=[json.loads(l) for l in (audit/'executions.jsonl').read_text().splitlines()]
    receipt=next((r for r in fresh if r['command']==command),None)
    if receipt:
        output=(audit/receipt['stdout_file']).read_text();rc=receipt['returncode']
        recovered=receipt.get('verified_input_fallback',{}).get('selected_path')
        assert rc==0 or recovered is not None
    else:
        cp=subprocess.run(command,capture_output=True,text=True)
        recovered=getattr(cp,'astra_verified_window_path',None);output=cp.stdout;rc=cp.returncode
    match=re.search(r'FINALPATH ?([\d ]*)',output)
    job.setdefault('windows',{})[board]={'returncode':rc,'input_length':len(moves)}
    return recovered if recovered is not None else list(map(int,match[1].split())) if match else moves
job['utc']=dt.datetime.now(dt.timezone.utc).isoformat()
job['paths']={};job['raw_paths']={};job['checks']={}
for board in ('ac','sac'):
    match=re.search(r'^'+board.upper()+r' \d+ PATH ([\d ]+)',output,re.M)
    if not match:continue
    full=path[:cut]+list(map(int,match[1].split()))
    verify(board,full);job['raw_paths'][board]=full
    if board=='ac' and len(full)<=t['record']+6:
        full=window(board,ch[cid]['initial_relators'],full)
    elif board=='sac' and len(full)<=t['record']+8:
        assert full[-2:]==[15,15]
        sw=[[SW[x] for x in w] for w in ch[cid]['initial_relators']]
        short=window(board,sw,[PI.get(x,x) for x in full[:-2]])
        candidate=[PI.get(x,x) for x in short]+[15,15]
        verify(board,candidate)
        if len(candidate)<len(full):full=candidate
    job['paths'][board]=full;job['checks'][board]=verify(board,full)
    (wd/'partial.json').write_text(json.dumps(job,indent=2)+'\n')
if 'ac' in job['paths']:
    stable=job['paths']['ac']+[16,15]
    if 'sac' not in job['paths'] or len(stable)<len(job['paths']['sac']):
        job['paths']['sac']=stable;job['checks']['sac']=verify('sac',stable)
job['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
(wd/'result.json').write_text(json.dumps(job,indent=2)+'\n')
print(json.dumps({'id':cid,'cut':cut,'lengths':{b:len(p) for b,p in job['paths'].items()},'result':str(wd/'result.json')}),flush=True)
