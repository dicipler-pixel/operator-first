#!/usr/bin/env python3
"""Finite paid joins through canonical cyclic words on witnessed interiors.

The quotient is an index only. Every emitted path uses official primitive
moves; canonical normalizer recipes are not claimed to be shortest bridges.
"""
import argparse,gzip,hashlib,json,math,resource,shutil,signal,sys,time
from collections import defaultdict,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import official_checker
from harness import atomic_json
INV=(0,1,3,2,5,4,7,6,9,8,11,10,13,12)
LETTERS=(1,-1,2,-2)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def state(s):return tuple(tuple(w) for w in s)
def inverse_word(w):return tuple(-x for x in reversed(w))
def inverse_path(p):return [INV[m] for m in reversed(p)]
def cancel(p):
 out=[]
 for m in p:
  if out and INV[m]==out[-1]:out.pop()
  else:out.append(m)
 return out
def cyclic_core(w):
 w=tuple(w)
 while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
 return w
def canonical_word(w):
 w=cyclic_core(w)
 if not w:return ()
 return min(v[i:]+v[:i] for v in (w,inverse_word(w)) for i in range(len(v)))
def class_key(s):return tuple(canonical_word(w) for w in s)
def normalizer(w,rel,direction,canonical):
 w=tuple(w);stem=[]
 def conj(g):return 6+4*rel+LETTERS.index(g)
 while len(w)>1 and w[0]==-w[-1]:stem.append(conj(-w[0]));w=w[1:-1]
 paths=[]
 for invert in (False,True):
  v=inverse_word(w) if invert else w
  for j in range(max(1,len(v))):
   if v[j:]+v[:j]!=canonical:continue
   p=stem+([rel] if invert else []);u=v
   if direction=='forward':
    for _ in range(j):p.append(conj(-u[0]));u=u[1:]+u[:1]
   elif direction=='reverse':
    for _ in range((len(v)-j)%max(1,len(v))):p.append(conj(u[-1]));u=u[-1:]+u[:-1]
   else:raise ValueError('Unknown clock direction')
   assert u==canonical;paths.append(cancel(p))
 assert paths
 return min(paths,key=lambda p:(len(p),p))
def recipes(s,t,key):
 table={}
 for rel in (0,1):
  a={d:normalizer(s[rel],rel,d,key[rel]) for d in ('forward','reverse')}
  b={d:normalizer(t[rel],rel,d,key[rel]) for d in ('forward','reverse')}
  table[rel]={(d,e):cancel(a[d]+inverse_path(b[e])) for d in a for e in b}
 return {
  'forward':table[0]['forward','forward']+table[1]['forward','forward'],
  'reverse':table[0]['reverse','reverse']+table[1]['reverse','reverse'],
  'mixed':min(table[0].values(),key=lambda p:(len(p),p))+min(table[1].values(),key=lambda p:(len(p),p))}
class Bound(Exception):pass
def main():
 p=argparse.ArgumentParser();p.add_argument('--row',required=True);p.add_argument('--output-dir',required=True);p.add_argument('--wall-seconds',type=float,default=180);p.add_argument('--node-cap',type=int,default=600000);p.add_argument('--memory-mib',type=int,default=1024);p.add_argument('--target-length',type=int,required=True);a=p.parse_args()
 if not math.isfinite(a.wall_seconds) or not 0<a.wall_seconds<=180 or not 0<a.node_cap<=600000 or not 0<a.memory_mib<=1024 or a.target_length<0:raise ValueError('Invalid limits')
 out=Path(a.output_dir).resolve();out.relative_to(ROOT/'runs');out.mkdir(parents=True,exist_ok=True)
 assert not (out/'worker_result.json').exists(),'Immutable result already exists'
 protocol=json.loads((ROOT/'helpers/paid_phase_protocol.json').read_text());assert a.row in protocol['rows']
 graph_path=ROOT/protocol['graph'];worker_path=graph_path.parent/'worker_result.json'
 assert sha(graph_path)==protocol['graph_sha256'] and sha(worker_path)==protocol['worker_result_sha256']
 worker=json.loads(worker_path.read_text());assert any(e['path']==protocol['graph'] and e['sha256']==protocol['graph_sha256'] for e in worker['evidence'])
 resource.setrlimit(resource.RLIMIT_AS,(a.memory_mib*1024**2,)*2)
 begin=time.monotonic();last_check=0;records=0;coverage={'graph_edges_checked':0,'class_pairs_tested':0,'complete':False,'arm_best':{},'arm_proposals':{'forward':0,'reverse':0,'mixed':0}}
 def tick(n=1):
  nonlocal records,last_check
  if records+n>a.node_cap:raise Bound('record_cap')
  records+=n;now=time.monotonic()
  if now-begin>=a.wall_seconds:raise Bound('wall_seconds')
  if now-last_check>=.1:
   cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
   if cp['stopped']:raise Bound('controller_stop')
   last_check=now
 def expired(*_):raise Bound('wall_seconds')
 signal.signal(signal.SIGALRM,expired);signal.setitimer(signal.ITIMER_REAL,a.wall_seconds)
 core,spec,doc,selected=official_checker.load_kernel();ch=selected[a.row];start=state(ch['initial_relators']);goal=((1,),(2,))
 seeds=sorted({tuple(r['moves']) for r in json.loads((ROOT/'continuation/routes.json').read_text())['routes'] if r['row_id']==a.row})
 assert seeds,'This finite query requires witnessed own paths';baseline=min(map(len,seeds));best=None;best_arm=None;reason='complete'
 atomic_json(out/'input.json',{'row':a.row,'seeds':seeds,'protocol':protocol,'baseline':baseline,'target':a.target_length})
 shutil.copy2(__file__,out/'executed_paid_phase_lane_v1.py');shutil.copy2(ROOT/'helpers/paid_phase_protocol.json',out/'executed_protocol.json')
 try:
  graph=json.loads(gzip.decompress(graph_path.read_bytes()));assert graph['cost']=='unit official primitive'
  states=[state(s) for s in graph['states']];index={s:i for i,s in enumerate(states)};tick(len(states));assert len(index)==len(states)
  back=[[] for s in states]
  for s,m,t in graph['edges']:
   tick();assert core.apply_move(states[s],m)==states[t];back[t].append((s,m));coverage['graph_edges_checked']+=1
  end=index[goal];dist={end:0};step={};q=deque([end])
  while q:
   v=q.popleft();tick()
   for u,m in back[v]:
    tick()
    if u not in dist:dist[u]=dist[v]+1;step[u]=(v,m);q.append(u)
  classes=defaultdict(list)
  for i,s in enumerate(states):
   tick()
   if i in dist:classes[class_key(s)].append(i)
  def suffix(i):
   path=[]
   while i!=end:i,m=step[i];path.append(m)
   return path
  entries={start:[]}
  for moves in seeds:
   s=start;pref=[]
   for m in moves:
    tick();s=core.apply_move(s,m);pref=cancel(pref+[m])
    if s not in entries or len(pref)<len(entries[s]):entries[s]=pref
   assert s==goal
  control=min((len(pref)+dist[index[s]] for s,pref in entries.items() if s in index and index[s] in dist),default=None)
  coverage['exact_control_length']=control;coverage['entry_states']=len(entries);coverage['classes']=len(classes)
  for s,pref in sorted(entries.items(),key=lambda x:(len(x[1]),x[0])):
   key=class_key(s)
   for t in classes.get(key,[]):
    tick();coverage['class_pairs_tested']+=1
    tail=suffix(t)
    for arm,join in recipes(s,states[t],key).items():
     tick();coverage['arm_proposals'][arm]+=1
     moves=cancel(pref+join+tail);length=len(moves)
     old=coverage['arm_best'].get(arm);coverage['arm_best'][arm]=length if old is None else min(old,length)
     if length>=baseline or (best is not None and length>=len(best)):continue
     v=s
     for m in join:tick();v=core.apply_move(v,m)
     assert v==states[t],'Paid alignment recipe did not reach exact donor state'
     v=start
     for m in moves:tick();v=core.apply_move(v,m)
     assert v==goal
     best=moves;best_arm=arm
     atomic_json(out/'best_join.json',{'prefix':pref,'alignment':join,'suffix':tail,'moves':moves,'source_state':s,'donor_index':t,'arm':arm,'length':length})
  coverage['complete']=True
 except Bound as e:reason=str(e)
 finally:signal.setitimer(signal.ITIMER_REAL,0)
 coverage.update({'algorithm':'paid-canonical-interior-joins-v1','row':a.row,'baseline':baseline,'best_length':len(best) if best is not None else baseline,'best_arm':best_arm,'records':records,'termination_reason':reason,'elapsed_seconds':time.monotonic()-begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'limits':{'wall_seconds':a.wall_seconds,'node_cap':a.node_cap,'memory_mib':a.memory_mib},'scope':'Only frozen graph and fixed normalizer recipes; not all conjugators or all routes. Unit-cost clock; no physical time or free symmetries.'})
 atomic_json(out/'coverage.json',coverage)
 evidence=[out/'input.json',out/'executed_paid_phase_lane_v1.py',out/'executed_protocol.json',out/'coverage.json',graph_path,worker_path]
 if best is not None:
  candidate={'row_id':a.row,'track':'AC','start':official_checker.render(start),'moves':best,'ruleset_sha256':spec.get('ac-r2-v1').move_spec_hash.removeprefix('sha256:'),'evidence_grade':'V','family':'paid-canonical-interior-joins'}
  receipt=official_checker.check(candidate);assert receipt['valid'];atomic_json(out/'candidate.json',candidate);atomic_json(out/'receipt.json',receipt);evidence += [out/'best_join.json',out/'candidate.json',out/'receipt.json']
  result={'kind':'candidate','summary':f'Paid interior join improves {baseline} to {len(best)}; no current scoring claim.','candidate':candidate}
 else:
  result={'kind':'bounded_miss' if coverage['complete'] else 'blocked','summary':f'Paid canonical interior recipes: best {baseline}; coverage complete={coverage["complete"]}; {reason}.','limits':coverage['limits'],'actual_coverage':coverage,'termination_reason':reason,'reopen_when':{'event':'new_witnessed_graph_or_entry_states','row_id':a.row}}
 result['evidence']=[{'path':str(x.relative_to(ROOT)),'sha256':sha(x)} for x in evidence];atomic_json(out/'worker_result.json',result)
 print(json.dumps({'result_path':str((out/'worker_result.json').relative_to(ROOT)),'kind':result['kind'],'best_length':coverage['best_length'],'termination_reason':reason}))
if __name__=='__main__':main()
