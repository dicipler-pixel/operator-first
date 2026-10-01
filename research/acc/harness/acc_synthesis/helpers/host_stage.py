import argparse,base64,datetime,hashlib,json
from pathlib import Path
from acc_synthesis.helper_batch import HelperContinuation
from acc_synthesis.continue_batch import Continuation
r=Path('acc_synthesis');prefix='research/acc/harness/acc_synthesis/'
p=argparse.ArgumentParser();p.add_argument('action',choices=['reserve','pack']);p.add_argument('--head');p.add_argument('--exclude',default='[]');p.add_argument('--mode',choices=['helper','bridge'],default='helper');a=p.parse_args();c=Continuation() if a.mode=='bridge' else HelperContinuation()
if a.action=='reserve':
 plan=c.plan(json.loads(a.exclude))
 if plan['status']!='planned':print(json.dumps(plan));raise SystemExit
 plan=c.reserve(plan['job']['key'],a.head,json.loads(a.exclude));j=plan['active']['job']
 claim=f'''# ACC memory-first harness claims

Updated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}.

Active: {j.get('helper','bridge')} {j['row_id']}, code-only batch. Key {j['key']}. Expires {datetime.datetime.fromtimestamp(plan['active']['expires_at'],datetime.timezone.utc).isoformat()}.

Row checked against current WORKING claims. Previous completed attempts are retained in continuation/checkpoint.json. This batch begins only after its reservation is committed.

Bounds <=180 search seconds / <=600000 records / <=1024 MiB; model-worker dispatch zero. No challenge API calls, submissions, public publishing or old watches. Read research/acc/harness/acc_synthesis/CONTINUATION.md for the procedure.
'''
 Path('/tmp/acc_current_claim.md').write_text(claim);print(json.dumps(plan));raise SystemExit
from acc_synthesis.helpers.audit_artifacts import audit_all
audit_all(r,sync=True)
meta=json.loads(Path('/tmp/acc_work_meta.json').read_text());remote={e['path']:e['sha'] for e in meta['files']};known=set(meta['known'])
progress=json.loads((r/'continuation/progress.json').read_text());progress.update(completed_batches=len(c.cp['attempts']),code_only_batches=sum(x.get('origin') in ['deterministic_code','deterministic_helper_code'] for x in c.cp['attempts']),next=c.plan(),harness_status=c.h.status(),helper_probes=[{'helper':x['job'].get('helper'),'row_id':x['job']['row_id'],'baseline':x['job']['baseline'],'target':x['job']['target'],'kind':x['kind'],'result_path':x.get('result_path'),'limits':x.get('limits')} for x in c.cp['attempts'] if x['job'].get('helper')],new_improved_routes=sum(bool(x.get('gate',{}).get('exact_verified')) for x in c.cp['attempts'] if x.get('gate')))
(r/'continuation/progress.json').write_text(json.dumps(progress,indent=2)+'\n')
v=json.loads((r/'VALIDATION.json').read_text());v['bounded_real_searches']=len(c.cp['attempts']);(r/'VALIDATION.json').write_text(json.dumps(v,indent=2)+'\n')
if c.cp['active'] is None:
 Path('/tmp/acc_current_claim.md').write_text(f'''# ACC memory-first harness claims

Updated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}.

No active claim. Completed {len(c.cp['attempts'])} bounded method probes.

Completed row details and proposed jobs are in the continuation checkpoint and progress files. They are not reservations.

All results and precise limits are preserved in research/acc/harness/acc_synthesis/continuation/checkpoint.json and runs/. Scheduled model-worker dispatch zero. Bounds unchanged: <=180 search seconds / <=600000 records / <=1024 MiB. No submissions, challenge API requests, public publishing or old watches. Scope of a bounded miss is not a nonexistence proof.
''')
paths=set(remote)
if c.cp.get('intake_lease'):
 lease=c.cp['intake_lease']
 Path('/tmp/acc_current_claim.md').write_text(f'''# ACC memory-first harness claims

Active data-intake lease: {lease['key']}. No row search running. Exact team-route verification and pool staging only.
Expires {datetime.datetime.fromtimestamp(lease['expires_at'],datetime.timezone.utc).isoformat()}.
Other continuations of this harness must honor continuation/checkpoint.json intake_lease. Expiry requires an interrupted record, never adoption or silent replay.
Bounds <=180 seconds / <=600000 records / <=1024 MiB; zero model workers. No submissions or challenge API.
''')
for f in r.rglob('*'):
 if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc' and f.relative_to(r).parts[0] in {'helpers','runs','continuation','tests'}:paths.add(f.relative_to(r).as_posix())
paths.discard('SHA256SUMS.txt')
(r/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256((r/f).read_bytes()).hexdigest()+'  '+f+'\n' for f in sorted(paths)))
paths.add('SHA256SUMS.txt');entries=[];blobs=[]
for f in sorted(paths):
 b=(r/f).read_bytes();sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if remote.get(f)==sha:continue
 e={'path':prefix+f,'mode':'100644','type':'blob'}
 if sha in known:e['sha']=sha
 else:
  try:e['content']=b.decode()
  except UnicodeDecodeError:e['sha']=sha;blobs.append({'content':base64.b64encode(b).decode(),'encoding':'base64','expected_sha':sha})
 entries.append(e)
entries.append({'path':'research/acc/live/WORKING_harness.md','mode':'100644','type':'blob','content':Path('/tmp/acc_current_claim.md').read_text()})
files=[]
for path,obj in [('/tmp/acc_work_entries.json',entries)]+[(f'/tmp/acc_work_blob_{i}.json',b) for i,b in enumerate(blobs)]:
 Path(path).write_text(json.dumps(obj));files.append({'path':path,'length':Path(path).stat().st_size})
print(json.dumps({'files':files,'entries':len(entries),'active':c.cp['active'],'attempts':len(c.cp['attempts'])}))
