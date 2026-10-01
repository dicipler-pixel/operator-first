"""One frozen team-feed intake; drafts stay disabled and no search is launched."""
import argparse, contextlib, hashlib, io, json, resource, shutil, signal, sys, time, uuid
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT))
from helper_batch import HelperContinuation
from harness import atomic_json, controller_lock
POOL=ROOT/'helpers/kernel_sources/roads_input.json'
OWN=ROOT/'continuation/routes.json'
VALIDATOR=ROOT/'helpers/intake_exact_roads_v1.py'
INPUT=OUT/'intake_input.json'
OWNER=Path('/tmp/acc_manual_intake_20261001T0316Z_owner.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def rel(p):return str(Path(p).relative_to(ROOT))
def prepare(c):
 assert c.cp['active'] is None and not c.cp['stopped'] and not c.cp.get('intake_lease')
 source=read(INPUT)
 key=hashlib.sha256(json.dumps({'source_sha256':sha(INPUT),'pool_sha256':sha(POOL),'own_sha256':sha(OWN),'method':'exact-data-intake-v1'},sort_keys=True).encode()).hexdigest()
 assert key not in c.cp.get('manual_intakes',{}),'Closed intake; do not repeat'
 owner=uuid.uuid4().hex
 lease={'key':key,'owner':owner,'expires_at':time.time()+600,'phase':'reserved','directory':rel(OUT),'source_head':source['head'],'pool_before_sha256':sha(POOL),'own_before_sha256':sha(OWN),'input_sha256':sha(INPUT),'validator_sha256':sha(VALIDATOR),'controller_sha256':sha(__file__)}
 shutil.copy2(POOL,OUT/'previous_roads_input.json');shutil.copy2(VALIDATOR,OUT/'executed_intake_exact_roads_v1.py')
 atomic_json(OWNER,{'owner':owner,'key':key});c.cp['intake_lease']=lease;c.save()
 print(json.dumps({'status':'reserved_intake','lease':lease}))
def run(c,commit):
 lease=c.cp.get('intake_lease')
 assert lease and lease['directory']==rel(OUT) and lease['expires_at']>time.time()
 assert c.cp['active'] is None and not c.cp['stopped']
 assert read(OWNER)=={'owner':lease['owner'],'key':lease['key']},'Foreign lease'
 assert len(commit)==40 and all(x in '0123456789abcdef' for x in commit)
 for p,k in [(POOL,'pool_before_sha256'),(OWN,'own_before_sha256'),(INPUT,'input_sha256'),(VALIDATOR,'validator_sha256'),(Path(__file__),'controller_sha256')]:assert sha(p)==lease[k]
 assert not (OUT/'validation/result.json').exists() and not (OUT/'interrupted.json').exists()
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
 def expired(*_):raise TimeoutError('180-second intake cap; incomplete, not a miss')
 signal.signal(signal.SIGALRM,expired);signal.alarm(180)
 try:
  from helpers import intake_exact_roads_v1 as validator
  sys.argv=['intake_exact_roads_v1.py','--input',str(INPUT),'--output',str(OUT/'validation')]
  with contextlib.redirect_stdout(io.StringIO()):validator.main()
  result=read(OUT/'validation/result.json');accepted=read(OUT/'validation/accepted_routes.json')['routes']
  current=read(c.path)
  assert current['active'] is None and not current['stopped'] and current.get('intake_lease')==lease
  assert sha(POOL)==lease['pool_before_sha256'] and sha(OWN)==lease['own_before_sha256']
  assert result['source_sha256']==lease['input_sha256'] and result['previous_pool_sha256']==lease['pool_before_sha256']
  pool=read(POOL);assert len(pool['routes'])+len(accepted)<=6000
  changed=result['added_directed_edges']>0
  receipt={'key':lease['key'],'status':'verified_new_graph' if changed else 'verified_no_new_graph','reservation_commit':commit,'source_head':lease['source_head'],'accepted_routes':len(accepted),'added_vertices':result['added_vertices'],'added_directed_edges':result['added_directed_edges'],'validation':rel(OUT/'validation/result.json'),'validation_sha256':sha(OUT/'validation/result.json'),'pool_before_sha256':lease['pool_before_sha256'],'model_workers':0,'limits':result['limits']}
  if changed:
   for r in accepted:pool['routes'].append({'row_id':r['row_id'],'moves':r['moves'],'sources':[{'path':r['source'],'line':r['line'],'head':lease['source_head'],'receipt':rel(OUT/'validation/verifier_receipts.json')}]})
   pool.setdefault('append_only_imports',[]).append({'head':lease['source_head'],'review':rel(OUT/'validation/result.json'),'routes':len(accepted),'exact_graph_new_directed_edges':result['added_directed_edges']})
   atomic_json(OUT/'proposed_pool.json',pool);receipt['pool_after_sha256']=sha(OUT/'proposed_pool.json')
  else:receipt['pool_after_sha256']=lease['pool_before_sha256']
  atomic_json(OUT/'receipt.json',receipt)
  if changed:atomic_json(POOL,pool)
  assert sha(POOL)==receipt['pool_after_sha256']
  current.setdefault('manual_intakes',{})[lease['key']]={'status':receipt['status'],'receipt':rel(OUT/'receipt.json')}
  current.pop('intake_lease');c.cp=current;c.save();c.h.store.event('data.intake.completed',receipt)
  print(json.dumps(receipt))
 except Exception as e:
  failure={'key':lease['key'],'status':'interrupted','error':type(e).__name__+': '+str(e),'reservation_commit':commit}
  atomic_json(OUT/'interrupted.json',failure);current=read(c.path)
  if sha(POOL)==lease['pool_before_sha256'] and current.get('intake_lease')==lease:
   current.setdefault('manual_intakes',{})[lease['key']]={'status':'interrupted','receipt':rel(OUT/'interrupted.json')};current.pop('intake_lease');c.cp=current;c.save()
  raise
 finally:signal.alarm(0)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','run']);p.add_argument('--reservation-commit');a=p.parse_args();c=HelperContinuation(ROOT)
 with controller_lock(c.h.state):
  if a.action=='prepare':prepare(c)
  else:run(c,a.reservation_commit)
