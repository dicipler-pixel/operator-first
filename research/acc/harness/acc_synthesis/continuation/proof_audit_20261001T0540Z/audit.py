"""Independent finite audit of UPGH's new paid identities and frozen route data."""
import hashlib,json,resource,signal,sys,time
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('audit interrupted, not a miss')))
signal.alarm(180)
started=time.monotonic();count=0
def tick(n=1):
 global count
 count+=n
 if count>600000:raise RuntimeError('finite audit record cap')
 if time.monotonic()-started>180:raise TimeoutError('finite audit wall cap')
 cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
 if cp['stopped'] or cp['active'] is not None or cp.get('intake_lease'):raise RuntimeError('stop/conflicting lease')
core,specs,pins,selected=load_kernel()
input_path=OUT/'input.json';doc=json.loads(input_path.read_text())
manifest=ROOT.parent/'manifest/unpacked/manifest.json'
assert hashlib.sha256(manifest.read_bytes()).hexdigest()==pins['source_manifest_sha256']
man=json.loads(manifest.read_text());challenges={c['challenge_id']:c for c in man['challenges']}
pool=json.loads((ROOT/'helpers/kernel_sources/roads_input.json').read_text())
receipts=[]
for r in doc['routes']:
 ch=challenges[r['id']];tick(len(r['ac']))
 v=core.verify(ch,r['ac'],ch['move_spec_version'],man['limits']);assert v['ok'] and v['length']==r['len']
 old=min((len(z['moves']) for z in pool['routes'] if z['row_id']==r['id']),default=None)
 receipts.append({'row':r['id'],'new':r['len'],'saved_pool_best':old,'improves_pool_best':old is None or r['len']<old,'official_receipt':v,'selected_row':r['id'] in selected})
def apply(s,moves):
 for mv in moves:tick();s=core.apply_move(s,mv)
 return s
rho=(-1,2,1,1,-2);rho2=(2,1,1,-2,-1)
cases=0;transitions=0
for a in range(1,17):
 for b in range(2,7):
  for c in range(2,7):
   s1=((1,)*(a-1)+(2,)*b+(-1,)+(-2,)*c+(1,),rho)
   p1=apply(s1,[z for _ in range(a-1) for z in (2,7)]+[2])
   assert p1==((2,)*b+(-1,)+(-2,)*(c-1)+(1,)*(2*a)+(-2,),rho)
   t1=apply(p1,[0,9,6,10])
   assert t1==((-1,)*(2*a-1)+(2,)*(c-1)+(1,)+(-2,)*(b-1)+(-1,),rho2)
   s2=((-1,)*(a-1)+(2,)*c+(1,)+(-2,)*b+(-1,),rho2)
   p2=apply(s2,[z for _ in range(a-1) for z in (3,6)]+[3])
   assert p2==((2,)*c+(1,)+(-2,)*(b-1)+(-1,)*(2*a)+(-2,),rho2)
   t2=apply(p2,[0,9,7,11])
   assert t2==((1,)*(2*a-1)+(2,)*(b-1)+(-1,)+(-2,)*(c-1)+(1,),rho)
   cases+=2;transitions+=2
load_kernel();signal.alarm(0)
result={'kind':'completed_new_source_finite_audit','source':{k:doc[k] for k in ('source_head','source_path','source_git_blob','drive_id')},'input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),'checker_commit':pins['source_commit'],'manifest_sha256':pins['source_manifest_sha256'],'route_receipts':receipts,'finite_pass_cases':cases,'finite_four_move_transitions':transitions,'domain':{'a':[1,16],'b':[2,6],'c':[2,6]},'records':count,'elapsed_seconds':time.monotonic()-started,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'model_workers':0,'row_searches':0,'limits':doc['bounds'],'proof_scope':'Finite grid supports identities; no Lean-backed all-parameter proof, globally optimal route, or current scoring claim.'}
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='route_receipts'}));print(json.dumps(receipts))
