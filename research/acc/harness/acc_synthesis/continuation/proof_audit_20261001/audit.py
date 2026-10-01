#!/usr/bin/env python3
"""Independent finite diagnostics; no external solver implementation imported."""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import hashlib,json,time,resource
resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
START=time.monotonic(); LIMIT=180; RECORD_CAP=600000
records=0
def charge():
 global records
 records+=1
 if records>RECORD_CAP or time.monotonic()-START>LIMIT: raise RuntimeError("incomplete: resource limit")
def ball(edges,start,r,allowed=None):
 d={start:0};q=deque([start])
 while q:
  u=q.popleft()
  if d[u]==r:continue
  for v in edges[u]:
   if (allowed is None or v in allowed) and v not in d:d[v]=d[u]+1;q.append(v)
 return d
pairs=list(combinations(range(4),2));cases=0
for mask in range(1<<len(pairs)):
 e={i:set() for i in range(4)}
 for j,(u,v) in enumerate(pairs):
  if mask>>j&1:e[u].add(v);e[v].add(u)
 for h in product((0,1),repeat=4):
  allowed={i for i in range(4) if h[i]==0}
  for s in allowed:
   for t in allowed:
    full=ball(e,s,4,allowed);dist=full.get(t)
    for a,b in product(range(3),repeat=2):
     charge();A=ball(e,s,a,allowed);B=ball(e,t,b,allowed)
     assert bool(set(A)&set(B))==(dist is not None and dist<=a+b)
     cases+=1
# A capped backward ball cannot certify the prefix-only claim.
e={0:{1},1:{0,2},2:{1,3},3:{2}};heights=[0,0,2,0];C=0
A=ball(e,0,1,{0,1,3});B=ball(e,3,2,{0,1,3})
assert not set(A)&set(B) and ball(e,0,3)[3]==3
cap_counterexample={"edges":[[0,1],[1,2],[2,3]],"heights":heights,"cap":0,"forward_radius":1,"backward_radius":2,"forward_capped_ball":A,"backward_capped_ball":B,"uncapped_path":[0,1,2,3],"prefix_through_step1_within_cap":True}
partial={"forward_ball":[0,1],"backward_stored":[3,2],"advertised_back_radius":2,"actually_complete_back_radius":1,"missing_vertex":1,"real_path":[0,1,2,3]}
def mul(A,B):
 a,b,c,d=A;e,f,g,h=B
 return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inv(A):
 a,b,c,d=A;det=a*d-b*c;assert abs(det)==1
 return (d//det,-b//det,-c//det,a//det)
I=(1,0,0,1);S0=(0,-1,1,0)
gens=((1,1,0,1),(1,-1,0,1),(1,0,1,1),(1,0,-1,1),(-1,0,0,1),(1,0,0,-1))
maxdepth=9;dist={I:0};q=deque([I]);parents={}
while q:
 u=q.popleft()
 if dist[u]>=maxdepth:continue
 for k,g in enumerate(gens):
  charge();v=mul(g,u)
  if v not in dist:dist[v]=dist[u]+1;parents[v]=(u,k);q.append(v)
def witness(x):
 moves=[]
 while x!=I:
  x,k=parents[x];moves.append(k)
 return list(reversed(moves))
table=[]
for M in range(1,7):
 P=(M,1,1,0)
 assert mul((-1,0,0,1),(1,-M,0,1))==mul(P,inv(S0))
 assert mul(mul(mul((1,0,0,-1),gens[0]),gens[3]),(1,-(M-1),0,1))==inv(P)
 for sign0,sign1 in product((1,-1),repeat=2):
  Q=mul((sign0,0,0,sign1),P);left=mul(Q,inv(S0));right=inv(Q)
  d0=dist.get(left);d1=dist.get(right)
  assert d0 is not None and d1 is not None
  for value in (left,right):
   w=witness(value);out=I
   for k in w:out=mul(gens[k],out)
   assert out==value and len(w)==dist[value]
  table.append({"M":M,"row_signs":[sign0,sign1],"start_to_intermediate":d0,"intermediate_to_identity":d1,"sum":d0+d1,"claimed_sum":2*M+3,"matches":d0+d1==2*M+3})
out={"status":"complete","scope":"finite graph-lemma checks and exact GL2(Z) word distances only; not an ACC route search or a general proof","graph_cases":cases,"matrix_ball_radius":maxdepth,"matrix_ball_states":len(dist),"matrix_generators":gens,"matrix_rows":table,"matrix_claim_all_finite_cases_match":all(x["matches"] for x in table),"capped_backward_prefix_counterexample":cap_counterexample,"partial_ball_counterexample":partial,"records_or_comparisons":records,"limits":{"wall_seconds":LIMIT,"records":RECORD_CAP,"memory_mib":1024},"elapsed_seconds":time.monotonic()-START,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"model_workers":0,"network_calls":0}
Path(__file__).with_name('receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ("status","graph_cases","matrix_ball_states","matrix_claim_all_finite_cases_match","records_or_comparisons","elapsed_seconds","peak_rss_kib")}))

