#!/usr/bin/env python3
"""Deterministic, leased intake of a frozen, explicitly allowed team road feed."""
import argparse, contextlib, gzip, hashlib, io, json, os, re, resource, signal, sys, time, uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
CP=ROOT/'continuation/checkpoint.json'
POOL=ROOT/'helpers/kernel_sources/roads_input.json'
POLICY=ROOT/'helpers/auto_intake_policy.json'
OWNER=Path('/tmp/acc_intake_owner.json')
def read(p):return json.loads(Path(p).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(x,indent=2)+'\n');os.replace(t,p)
def relative(p):return str(p.relative_to(ROOT))
def emit(x):print(json.dumps(x));return x
def prepare(feed_path):
 c=read(CP); policy=read(POLICY)
 if not policy.get('enabled',False):return emit({'status':'intake_disabled_draft'})
 if c['stopped'] or c['active']:return emit({'status':'blocked_existing_stop_or_search'})
 if c.get('intake_lease'):return emit({'status':'blocked_intake_lease','lease':c['intake_lease']})
 feed=read(feed_path);pool=read(POOL)
 if not re.fullmatch('[0-9a-f]{40}',feed.get('head','')):raise ValueError('Exact source commit required')
 if {f['path'] for f in feed['files']}!=set(policy['source_paths']):raise ValueError('Source allowlist mismatch')
 if sum(len(f['content'].encode()) for f in feed['files'])>policy['max_source_bytes']:raise ValueError('Source byte cap exceeded')
 known={(r['row_id'],tuple(r['moves'])) for r in pool['routes']}
 routes=[];unknown=[];rejected=[];duplicates=0
 for f in feed['files']:
  for line_number,line in enumerate(f['content'].splitlines(),1):
   if not line.strip() or line.lstrip().startswith('#'):continue
   m=re.fullmatch(r'(ac-\d{5}):\s*(\[.*\])\s*',line)
   if not m:
    rejected.append({'source':f['path'],'line':line_number,'reason':'Unsupported line syntax; no coercion'});continue
   try:moves=json.loads(m[2])
   except ValueError:
    rejected.append({'source':f['path'],'line':line_number,'reason':'Invalid JSON'});continue
   item={'row_id':m[1],'moves':moves,'source':f['path'],'line':line_number}
   if not isinstance(moves,list) or len(moves)>pool['limits']['max_path_length'] or any(type(x)!=int or x<0 or x>13 for x in moves):
    rejected.append({'source':f['path'],'line':line_number,'reason':'Not a primitive AC move array'});continue
   key=(m[1],tuple(moves))
   if key in known:duplicates+=1;continue
   known.add(key)
   if m[1] not in pool['challenges']:unknown.append(item);continue
   if len(pool['routes'])+len(routes)>=policy['max_pool_routes']:
    item['reason']='Existing pool cap; not imported';unknown.append(item);continue
   routes.append(item)
 semantic=digest(canonical({'routes':sorted((r['row_id'],r['moves']) for r in routes),'starts':pool['challenges']}))
 seen=c.get('automatic_intake',{}).get('attempts',{})
 if routes and semantic in seen:return emit({'status':'closed_intake_key','key':semantic,'previous':seen[semantic]})
 source_hash=digest(canonical(feed))
 out=ROOT/'continuation/automatic_intake'/(source_hash[:16]+'_'+digest(POOL.read_bytes())[:12]);out.mkdir(parents=True,exist_ok=True)
 # Exact source snapshot, never retyped by a model.
 (out/'source_snapshot.json.gz').write_bytes(gzip.compress(canonical(feed),mtime=0))
 save(out/'input.json',{'head':feed['head'],'routes':routes,'unknown':unknown,'crashes':[]})
 save(out/'parse_receipt.json',{'source_sha256':source_hash,'key':semantic,'new_known_routes':len(routes),'deferred_routes':len(unknown),'duplicates':duplicates,'rejected_lines':rejected,'policy_sha256':digest(POLICY.read_bytes())})
 state=c.setdefault('automatic_intake',{});state['last_source_head']=feed['head'];state['last_parse']=relative(out/'parse_receipt.json')
 if not routes:
  state['last_status']='no_new_known_routes';save(CP,c)
  return emit({'status':'no_new_known_routes','duplicates':duplicates,'deferred':len(unknown),'receipt':state['last_parse']})
 owner=uuid.uuid4().hex;save(OWNER,{'owner':owner,'key':semantic})
 c['intake_lease']={'key':semantic,'owner':owner,'expires_at':time.time()+600,'phase':'reserved','directory':relative(out),'source_head':feed['head'],'pool_before_sha256':digest(POOL.read_bytes()),'script_sha256':digest(Path(__file__).read_bytes()),'validator_sha256':digest((ROOT/'helpers/intake_exact_roads_v1.py').read_bytes()),'policy_sha256':digest(POLICY.read_bytes())}
 save(CP,c);return emit({'status':'reserved_intake','lease':c['intake_lease']})
def run(key,commit):
 c=read(CP);lease=c.get('intake_lease');policy=read(POLICY)
 assert policy.get('enabled',False),'Draft intake is disabled pending validation'
 assert not c['stopped'] and c['active'] is None
 assert lease and lease['key']==key and lease['expires_at']>time.time()
 assert read(OWNER)=={'owner':lease['owner'],'key':key},'Foreign intake reservation cannot be adopted'
 assert re.fullmatch('[0-9a-f]{40}',commit),'Committed reservation required'
 assert lease['pool_before_sha256']==digest(POOL.read_bytes())
 assert lease['script_sha256']==digest(Path(__file__).read_bytes())
 assert lease['validator_sha256']==digest((ROOT/'helpers/intake_exact_roads_v1.py').read_bytes())
 assert lease['policy_sha256']==digest(POLICY.read_bytes())
 out=ROOT/lease['directory'];pool=read(POOL)
 resource.setrlimit(resource.RLIMIT_AS,(policy['memory_mib']*1024**2,)*2)
 def expired(*_):raise TimeoutError('Intake wall bound; interrupted, not a search miss')
 signal.signal(signal.SIGALRM,expired);signal.alarm(policy['seconds'])
 before=time.monotonic()
 try:
  from helpers import intake_exact_roads_v1 as validator
  sys.argv=['intake_exact_roads_v1.py','--input',str(out/'input.json'),'--output',str(out/'validation')]
  with contextlib.redirect_stdout(io.StringIO()):validator.main()
  result=read(out/'validation/result.json');accepted=read(out/'validation/accepted_routes.json')['routes']
  current=read(CP);assert not current['stopped'] and current['active'] is None and current.get('intake_lease')==lease
  assert lease['pool_before_sha256']==digest(POOL.read_bytes()),'Pool changed during validation'
  changed=result['added_directed_edges']>0
  if changed:
   for r in accepted:pool['routes'].append({'row_id':r['row_id'],'moves':r['moves'],'sources':[{'path':r['source'],'line':r['line'],'head':lease['source_head'],'receipt':relative(out/'validation/verifier_receipts.json')}]})
   pool.setdefault('append_only_imports',[]).append({'head':lease['source_head'],'review':relative(out/'validation/result.json'),'routes':len(accepted),'exact_graph_new_directed_edges':result['added_directed_edges']})
  receipt={'key':key,'status':'verified_new_graph' if changed else 'verified_no_new_graph','reservation_commit':commit,'source_head':lease['source_head'],'pool_before_sha256':lease['pool_before_sha256'],'accepted_routes':len(accepted),'added_directed_edges':result['added_directed_edges'],'validation':relative(out/'validation/result.json'),'elapsed_seconds':time.monotonic()-before,'model_workers':0}
  if changed:save(out/'proposed_pool.json',pool);receipt['pool_after_sha256']=digest((out/'proposed_pool.json').read_bytes())
  else:receipt['pool_after_sha256']=lease['pool_before_sha256']
  save(out/'receipt.json',receipt)
  if changed:save(POOL,pool)
  current.setdefault('automatic_intake',{}).setdefault('attempts',{})[key]={'status':receipt['status'],'receipt':relative(out/'receipt.json')}
  current['automatic_intake']['last_status']=receipt['status'];current.pop('intake_lease');save(CP,current)
  emit(receipt)
 except Exception as error:
  failure={'key':key,'status':'interrupted','error':type(error).__name__+': '+str(error),'elapsed_seconds':time.monotonic()-before,'reservation_commit':commit}
  save(out/'interrupted.json',failure)
  # A partial pool publication needs explicit reconciliation, not a silent reset.
  current=read(CP)
  if digest(POOL.read_bytes())==lease['pool_before_sha256'] and current.get('intake_lease')==lease:
   current.setdefault('automatic_intake',{}).setdefault('attempts',{})[key]={'status':'interrupted','receipt':relative(out/'interrupted.json')};current.pop('intake_lease');save(CP,current)
  emit(failure);raise
 finally:signal.alarm(0)
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='action',required=True)
 q=sub.add_parser('prepare');q.add_argument('--feed',required=True)
 q=sub.add_parser('run');q.add_argument('--key',required=True);q.add_argument('--reservation-commit',required=True)
 a=p.parse_args();return prepare(a.feed) if a.action=='prepare' else run(a.key,a.reservation_commit)
if __name__=='__main__':main()
