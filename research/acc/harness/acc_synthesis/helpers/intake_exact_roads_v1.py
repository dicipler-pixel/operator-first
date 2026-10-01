#!/usr/bin/env python3
"""Validate fresh team paths and measure exact graph delta; no new move search."""
import argparse,hashlib,json,resource,sys,time
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel

def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def state(x):return tuple(tuple(w) for w in x)

def main():
 a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--output',required=True);args=a.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));begin=time.monotonic();count=0;last_stop_check=0
 def tick(n=1):
  nonlocal count,last_stop_check
  count+=n
  if count>600000 or time.monotonic()-begin>180:raise RuntimeError('Intake interrupted at resource bound; not a miss')
  now=time.monotonic()
  if now-last_stop_check>=0.1:
   current=json.loads((ROOT/'continuation/checkpoint.json').read_text())
   if current['stopped'] or current['active'] is not None:raise RuntimeError('Stop or competing search during intake')
   last_stop_check=now
 cp=json.loads((ROOT/'continuation/checkpoint.json').read_text());assert cp['active'] is None and cp['stopped'] is False
 source=json.loads(Path(args.input).read_text());pool=json.loads((ROOT/'helpers/kernel_sources/roads_input.json').read_text());own=json.loads((ROOT/'continuation/routes.json').read_text())
 core,spec,doc,selected=load_kernel();from verifier.canon import instance_hash
 graph={};accepted=[];rejected=[];receipts=[]
 def add(start,moves):
  s=state(start)
  for m in moves:
   tick();u=core.apply_move(s,m);graph.setdefault(s,set()).add((u,m));graph.setdefault(u,set()).add((s,core.INVERSE_MOVE[m]));s=u
  return s
 for r in pool['routes']:add(pool['challenges'][r['row_id']]['initial_relators'],r['moves'])
 for r in own['routes']:add(selected[r['row_id']]['initial_relators'],r['moves'])
 old_states=set(graph);old_edges={(s,u,m) for s,edges in graph.items() for u,m in edges}
 for r in source['routes']:
  ch=pool['challenges'][r['row_id']]
  h=instance_hash(ch['challenge_id'],ch['generators'],ch['initial_relators'],ch['target_relators'],ch['move_spec_version'],spec.get(ch['move_spec_version']).move_spec_hash)
  assert h==ch['instance_hash'];tick(len(r['moves']))
  v=core.verify(ch,r['moves'],ch['move_spec_version'],pool['limits']);receipts.append({'row':r['row_id'],'source':r['source'],'line':r['line'],'verdict':v,'instance_hash':h})
  if not v['ok']:rejected.append(r);continue
  end=add(ch['initial_relators'],r['moves']);assert end==((1,),(2,));accepted.append(r)
 new_edges={(s,u,m) for s,edges in graph.items() for u,m in edges};delta_edges=new_edges-old_edges
 # Saved-graph distances only; no neighborhood search or new target expansion.
 q=deque([((1,),(2,))]);dist={q[0]:0}
 while q:
  s=q.popleft();tick()
  for u,m in graph.get(s,()):
   tick()
   if u not in dist:dist[u]=dist[s]+1;q.append(u)
 rows=[]
 for row,ch in selected.items():
  seeds=[r for r in own['routes'] if r['row_id']==row];baseline=min((len(r['moves']) for r in seeds),default=None)
  new_own=[r for r in accepted if r['row_id']==row]
  rows.append({'row':row,'baseline':baseline,'merged_graph_distance':dist.get(state(ch['initial_relators'])),'new_own_routes':len(new_own)})
 out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 write(out/'accepted_routes.json',{'head':source['head'],'routes':accepted});write(out/'verifier_receipts.json',receipts)
 write(out/'deferred_routes.json',source['unknown']);write(out/'rejected_routes.json',rejected);write(out/'team_process_failures.json',source['crashes'])
 result={'kind':'completed_exact_data_intake','source_head':source['head'],'source_sha256':sha(args.input),'previous_pool_sha256':sha(ROOT/'helpers/kernel_sources/roads_input.json'),
         'new_valid_routes':len(accepted),'rejected_routes':len(rejected),'deferred_missing_starts':len(source['unknown']),
         'old_graph_vertices':len(old_states),'new_graph_vertices':len(graph),'added_vertices':len(set(graph)-old_states),
         'old_graph_edges':len(old_edges),'new_graph_edges':len(new_edges),'added_directed_edges':len(delta_edges),'selected_rows':rows,
         'primitive_or_graph_records':count,'elapsed_seconds':time.monotonic()-begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
         'official_commit':doc['source_commit'],'model_workers':0,'new_move_searches':0,'limits':{'seconds':180,'memory_mib':1024,'records':600000}}
 write(out/'result.json',result);print(json.dumps(result))
if __name__=='__main__':main()
