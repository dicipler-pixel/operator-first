#!/usr/bin/env python3
"""Validate deferred team paths against pinned official manifest records."""
import argparse,hashlib,json,resource,sys,time
from collections import deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel

MANIFEST_SHA256='dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37'
MANIFEST_BLOB='accdb626ee08a06beea3f88dc7f351514c99eb27'
OFFICIAL_COMMIT='a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def state(x):return tuple(tuple(w) for w in x)

def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--records',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3));begin=time.monotonic();count=0;last=0
 def tick(n=1):
  nonlocal count,last
  count+=n
  if count>600000 or time.monotonic()-begin>180:raise RuntimeError('Manifest intake interrupted at resource bound; not a miss')
  now=time.monotonic()
  if now-last>=0.1:
   cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
   if cp['stopped'] or cp['active'] is not None:raise RuntimeError('Stop or competing row search during intake')
   last=now
 source=json.loads(Path(a.input).read_text());rdoc=json.loads(Path(a.records).read_text())
 assert rdoc['source_manifest_sha256']==MANIFEST_SHA256 and rdoc['source_manifest_git_blob']==MANIFEST_BLOB and rdoc['source_commit']==OFFICIAL_COMMIT
 pool=json.loads((ROOT/'helpers/kernel_sources/roads_input.json').read_text());own=json.loads((ROOT/'continuation/routes.json').read_text())
 core,specs,doc,selected=load_kernel();from verifier.canon import instance_hash
 assert doc['source_commit']==OFFICIAL_COMMIT and doc['source_manifest_sha256']==MANIFEST_SHA256 and doc['source_manifest_git_blob']==MANIFEST_BLOB
 records={c['challenge_id']:c for c in rdoc['records']};assert len(records)==len(rdoc['records'])
 challenges=dict(pool['challenges']);accepted_records=[]
 for row,c in records.items():
  assert row not in challenges and c['move_spec_version']=='ac-r2-v1' and c['generators']==['x','y']
  h=instance_hash(c['challenge_id'],c['generators'],c['initial_relators'],c['target_relators'],c['move_spec_version'],specs.get(c['move_spec_version']).move_spec_hash)
  assert h==c['instance_hash'];challenges[row]=c;accepted_records.append(c);tick()
 assert {r['row_id'] for r in source['routes']}==set(records) and not source['unknown'] and not source['crashes']
 graph={};accepted=[];rejected=[];receipts=[]
 def add(start,moves):
  s=state(start)
  for m in moves:
   tick();u=core.apply_move(s,m);graph.setdefault(s,set()).add((u,m));graph.setdefault(u,set()).add((s,core.INVERSE_MOVE[m]));s=u
  return s
 for r in pool['routes']:add(challenges[r['row_id']]['initial_relators'],r['moves'])
 for r in own['routes']:add(selected[r['row_id']]['initial_relators'],r['moves'])
 old_states=set(graph);old_edges={(s,u,m) for s,es in graph.items() for u,m in es}
 for r in source['routes']:
  ch=challenges[r['row_id']];tick(len(r['moves']))
  v=core.verify(ch,r['moves'],ch['move_spec_version'],pool['limits'])
  receipts.append({'row':r['row_id'],'source':r['source'],'line':r['line'],'verdict':v,'instance_hash':ch['instance_hash'],'manifest_sha256':MANIFEST_SHA256})
  if not v['ok']:rejected.append(r);continue
  assert add(ch['initial_relators'],r['moves'])==((1,),(2,));accepted.append(r)
 new_edges={(s,u,m) for s,es in graph.items() for u,m in es}
 q=deque([((1,),(2,))]);dist={q[0]:0}
 while q:
  s=q.popleft();tick()
  for u,m in graph.get(s,()):
   tick()
   if u not in dist:dist[u]=dist[s]+1;q.append(u)
 rows=[]
 for row,ch in selected.items():
  seeds=[r for r in own['routes'] if r['row_id']==row];baseline=min((len(r['moves']) for r in seeds),default=None)
  rows.append({'row':row,'baseline':baseline,'merged_graph_distance':dist.get(state(ch['initial_relators']))})
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 write(out/'accepted_routes.json',{'head':source['head'],'routes':accepted})
 write(out/'accepted_challenges.json',{'source_commit':OFFICIAL_COMMIT,'manifest_sha256':MANIFEST_SHA256,'challenges':accepted_records})
 write(out/'verifier_receipts.json',receipts);write(out/'rejected_routes.json',rejected)
 result={'kind':'completed_exact_manifest_data_intake','source_head':source['head'],'source_sha256':sha(a.input),'records_sha256':sha(a.records),
  'previous_pool_sha256':sha(ROOT/'helpers/kernel_sources/roads_input.json'),'new_valid_routes':len(accepted),'rejected_routes':len(rejected),
  'new_challenge_records':len(accepted_records),'old_graph_vertices':len(old_states),'new_graph_vertices':len(graph),'added_vertices':len(set(graph)-old_states),
  'old_graph_edges':len(old_edges),'new_graph_edges':len(new_edges),'added_directed_edges':len(new_edges-old_edges),'selected_rows':rows,
  'primitive_or_graph_records':count,'elapsed_seconds':time.monotonic()-begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
  'official_commit':OFFICIAL_COMMIT,'manifest_sha256':MANIFEST_SHA256,'model_workers':0,'new_move_searches':0,
  'limits':{'seconds':180,'memory_mib':1024,'records':600000}}
 write(out/'result.json',result);print(json.dumps(result))
if __name__=='__main__':main()
