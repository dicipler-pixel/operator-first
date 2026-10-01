"""Read-only exact overlay of new t00312 roads on the saved graph."""
import hashlib,json,resource,signal,sys,time
from collections import deque
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('overlay interrupted, not a miss')));signal.alarm(180)
start=time.monotonic();records=0
def tick(n=1):
 global records
 records+=n
 if records>600000:raise RuntimeError('overlay record cap; incomplete, not a miss')
 if time.monotonic()-start>180:raise TimeoutError('overlay wall cap; incomplete, not a miss')
 cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
 if cp['stopped'] or cp['active'] is not None or cp.get('intake_lease'):raise RuntimeError('stop or competing lease')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(ROOT/'helpers/kernel_sources/roads_input.json')=='f10748695d7a8cf906df7cda342e8d4d9d82bbae04f60ffe8a63241b2bde063c'
assert sha(ROOT/'continuation/routes.json')=='ff93a9ecbba27401dc2b5ca21aac85f52038d994b4e5681b85b9263936a506a9'
input_path=ROOT/'continuation/proof_audit_20261001T0540Z/input.json';assert sha(input_path)=='3369d2dd3a960529a6e08921651c7d3dae1eba3e1c82ad54e443a0d7b46526ff'
prior=json.loads((ROOT/'continuation/intake/20261001T0336Z/validation/result.json').read_text())
pool=json.loads((ROOT/'helpers/kernel_sources/roads_input.json').read_text());own=json.loads((ROOT/'continuation/routes.json').read_text());new=json.loads(input_path.read_text())['routes']
core,specs,pins,selected=load_kernel();challenges=dict(pool['challenges']);graph={}
def state(s):return tuple(tuple(w) for w in s)
def add(ch,moves):
 s=state(ch['initial_relators'])
 for m in moves:
  tick();u=core.apply_move(s,m);graph.setdefault(s,set()).add((u,m));graph.setdefault(u,set()).add((s,core.INVERSE_MOVE[m]));s=u
 return s
for r in pool['routes']:add(challenges[r['row_id']],r['moves'])
for r in own['routes']:add(selected[r['row_id']],r['moves'])
old_vertices=len(graph);old_edges=sum(map(len,graph.values()));added=[]
for r in new:
 ch=challenges[r['id']];tick(len(r['ac']));v=core.verify(ch,r['ac'],ch['move_spec_version'],pool['limits']);assert v['ok']
 before_v=len(graph);before_e=sum(map(len,graph.values()));assert add(ch,r['ac'])==((1,),(2,))
 added.append({'row':r['id'],'length':r['len'],'new_vertices':len(graph)-before_v,'new_directed_edges':sum(map(len,graph.values()))-before_e,'receipt':v})
goal=((1,),(2,));q=deque([goal]);dist={goal:0}
while q:
 s=q.popleft();tick()
 for u,m in graph.get(s,()):
  tick()
  if u not in dist:dist[u]=dist[s]+1;q.append(u)
old={x['row']:x['merged_graph_distance'] for x in prior['selected_rows']};rows=[]
for row,ch in selected.items():
 newdist=dist.get(state(ch['initial_relators']));rows.append({'row':row,'prior_distance':old[row],'overlay_distance':newdist,'improvement':None if newdist is None or old[row] is None else old[row]-newdist})
result={'kind':'completed_read_only_exact_donor_overlay','source_head':json.loads(input_path.read_text())['source_head'],'source_blob':json.loads(input_path.read_text())['source_git_blob'],'pool_sha256':sha(ROOT/'helpers/kernel_sources/roads_input.json'),'input_sha256':sha(input_path),'new_routes':len(new),'old_vertices':old_vertices,'overlay_vertices':len(graph),'added_vertices':len(graph)-old_vertices,'old_directed_edges':old_edges,'overlay_directed_edges':sum(map(len,graph.values())),'added_directed_edges':sum(map(len,graph.values()))-old_edges,'route_additions':added,'selected_rows':rows,'selected_improvements':[x for x in rows if (x['improvement'] or 0)>0],'records':records,'elapsed_seconds':time.monotonic()-start,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'model_workers':0,'row_searches':0,'pool_mutated':False,'limits':{'seconds':180,'memory_mib':1024,'records':600000},'scope':'Exact finite graph overlay only; no global shortest-path or live scoring claim.'}
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');signal.alarm(0)
print(json.dumps({k:v for k,v in result.items() if k not in ('route_additions','selected_rows')}));print(json.dumps(rows))
