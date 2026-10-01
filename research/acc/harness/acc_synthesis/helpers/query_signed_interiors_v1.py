#!/usr/bin/env python3
"""Finite signed-generator queries on witnessed graph interiors; no fresh moves."""
import argparse,gzip,hashlib,json,resource,signal,sys,time
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel,check,render
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def state(x):return tuple(tuple(w) for w in x)
def flip(s,sx,sy):return tuple(tuple(a*(sx if abs(a)==1 else sy) for a in w) for w in s)
def main():
 a=argparse.ArgumentParser();a.add_argument('--graph',required=True);a.add_argument('--out',required=True);args=a.parse_args()
 out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 if (out/'result.json').exists() or (out/'interrupted.json').exists():raise FileExistsError('Exact finite query already recorded; no replay')
 cp=json.loads((ROOT/'continuation/checkpoint.json').read_text());assert not cp['stopped'] and cp['active'] is None and not cp.get('intake_lease')
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));begin=time.monotonic();records=0;last_check=0
 def expired(*_):raise TimeoutError('Query interrupted at 180 seconds; not a miss')
 signal.signal(signal.SIGALRM,expired);signal.alarm(180)
 def tick(n=1):
  nonlocal records,last_check
  records+=n
  if records>600000:raise RuntimeError('Query record cap; interrupted, not a complete negative')
  now=time.monotonic()
  if now-last_check>=.1:
   c=json.loads((ROOT/'continuation/checkpoint.json').read_text())
   if c['stopped'] or c['active'] is not None:raise RuntimeError('Stop or competing search')
   last_check=now
 graph_path=Path(args.graph); graph_sha=sha(graph_path)
 try:
  # Bind source graph to the original immutable worker result, then verify every edge.
  worker=json.loads((graph_path.parent/'worker_result.json').read_text())
  graph_rel=str(graph_path.resolve().relative_to(ROOT))
  assert any(x['path']==graph_rel and x['sha256']==graph_sha for x in worker['evidence'])
  core,spec,doc,selected=load_kernel();g=json.loads(gzip.decompress(graph_path.read_bytes()))
  assert g['cost']=='unit official primitive'
  states=[state(s) for s in g['states']];idx={s:i for i,s in enumerate(states)};tick(len(states))
  assert len(idx)==len(states);reverse=[[] for _ in states]
  for s,m,t in g['edges']:
   tick();assert core.apply_move(states[s],m)==states[t];reverse[t].append((s,m))
  target=((1,),(2,));goal=idx[target];dist={goal:0};step={};queue=deque([goal])
  while queue:
   v=queue.popleft();tick()
   for u,m in reverse[v]:
    tick()
    if u not in dist:dist[u]=dist[v]+1;step[u]=(v,m);queue.append(u)
  own=json.loads((ROOT/'continuation/routes.json').read_text());rows=[];candidates=[]
  rules=spec.get('ac-r2-v1').move_spec_hash.removeprefix('sha256:')
  for row,ch in selected.items():
   start=state(ch['initial_relators']);baseline=min((len(x['moves']) for x in own['routes'] if x['row_id']==row),default=None)
   for sx,sy in ((1,1),(-1,1),(1,-1),(-1,-1)):
    tick();source=flip(start,sx,sy);i=idx.get(source);d=dist.get(i)
    finish=([0] if sx<0 else [])+([1] if sy<0 else [])
    cost=None if d is None else d+len(finish)
    entry={'row':row,'signs':[sx,sy],'source_index':i,'saved_graph_distance':d,'paid_finish':finish,'total_cost':cost,'baseline':baseline,'status':'absent_exact_interior' if i is None else 'unreachable_in_saved_graph' if d is None else 'witnessed_transfer'}
    rows.append(entry)
    if cost is None or (baseline is not None and cost>=baseline):continue
    moves=[];j=i;s=start
    while j!=goal:
     k,m=step[j];expected=flip(states[k],sx,sy)
     if m<6:mm=m
     else:
      base=6 if m<10 else 10;letter=(1,-1,2,-2)[(m-6)%4];letter*=sx if abs(letter)==1 else sy
      mm=base+(1,-1,2,-2).index(letter)
     tick();s=core.apply_move(s,mm);assert s==expected;moves.append(mm);j=k
    for m in finish:tick();s=core.apply_move(s,m);moves.append(m)
    assert s==target and len(moves)==cost
    candidate={'row_id':row,'track':'AC','start':render(start),'moves':moves,'ruleset_sha256':rules,'evidence_grade':'V','family':'signed-exact-interior-transfer'}
    receipt=check(candidate);assert receipt['valid'];candidates.append({'candidate':candidate,'receipt':receipt,'source_index':i,'signs':[sx,sy]})
  key=hashlib.sha256(json.dumps({'method':'signed-exact-interior-queries-v1','graph_sha256':graph_sha,'selected_manifest_sha256':sha(ROOT/'integration/official_selected.json'),'signs':[[1,1],[-1,1],[1,-1],[-1,-1]]},sort_keys=True).encode()).hexdigest()
  result={'kind':'completed_finite_data_query','key':key,'graph_path':graph_rel,'graph_sha256':graph_sha,'source_worker_result_sha256':sha(graph_path.parent/'worker_result.json'),'executed_script_sha256':sha(__file__),'official_commit':doc['source_commit'],'states':len(states),'checked_edges':len(g['edges']),'queries':rows,'candidates':candidates,'records':records,'elapsed_seconds':time.monotonic()-begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'limits':{'seconds':180,'records':600000,'memory_mib':1024},'model_workers':0,'new_neighborhood_expansions':0,'scope':'Only exact signed matches to this captured graph; no cyclic/class normalization, permutation, fresh bridges, or global impossibility claim.'}
  write(out/'result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['queries','candidates']}|{'candidate_count':len(candidates),'matched_queries':sum(x['total_cost'] is not None for x in rows)}))
 except Exception as error:
  write(out/'interrupted.json',{'kind':'interrupted','error':type(error).__name__+': '+str(error),'graph_sha256':graph_sha,'records':records,'elapsed_seconds':time.monotonic()-begin});raise
 finally:signal.alarm(0)
if __name__=='__main__':main()
