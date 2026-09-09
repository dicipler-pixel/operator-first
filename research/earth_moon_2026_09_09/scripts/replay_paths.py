#!/usr/bin/env python3
"""Replay saved flip/permutation/stellar paths using the independent Python core.

C++ cached statistics and face indices are not trusted. Rebuild the closed
sphere after each relocation and periodically after flips. Every flip is
checked against the actual two incident triangles. Full final states and proper
colorings are emitted. This verifier never counts a near miss as a solution.
"""
from __future__ import annotations
import argparse,collections,itertools,json,hashlib,time
from pathlib import Path
import graph_core as e

ALL_FACES=list(itertools.combinations(range(19),3))

def relocate(fs,v,root,into):
 fs=set(fs);star={f for f in fs if v in f};boundary=collections.defaultdict(set)
 for f in star:
  u,w=[x for x in f if x!=v];boundary[u].add(w);boundary[w].add(u)
 assert 3<=len(star)<=10 and len(boundary)==len(star)
 assert root in boundary and all(len(n)==2 for n in boundary.values())
 cyc=[root];prev=None;cur=root
 for _ in range(len(star)):
  choices=boundary[cur]-({prev}if prev is not None else set());nxt=min(choices)
  if nxt==root:break
  assert nxt not in cyc;cyc.append(nxt);prev,cur=cur,nxt
 assert len(cyc)==len(star) and root in boundary[cyc[-1]]
 exterior=fs-star;exterior_edges={uv for f in exterior for uv in itertools.combinations(f,2)}
 assert all(tuple(sorted((root,cyc[j])))not in exterior_edges for j in range(2,len(cyc)-1))
 fan={tuple(sorted((root,cyc[j],cyc[j+1])))for j in range(1,len(cyc)-1)}
 assert fan.isdisjoint(exterior)
 remaining=exterior|fan;assert len(remaining)==32 and into in remaining and v not in into
 result=(remaining-{into})|{tuple(sorted((v,)+uv))for uv in itertools.combinations(into,2)}
 t=e.Triangulation(19,list(sorted(result)));e.verify_layer(19,t.as_dict())
 return t

def nine_coloring(ts,union):
 H=e.complement(19,union)
 for triple in ts:
  keep=[v for v in range(19)if v not in triple];ids={v:i for i,v in enumerate(keep)}
  h=[sum(1<<ids[w]for w in keep if H[v]>>w&1)for v in keep]
  matching=e.maximum_matching_dp(h)
  if len(matching)==8:
   classes=[list(triple)]+[[keep[a],keep[b]]for a,b in matching]
   assert sorted(x for c in classes for x in c)==list(range(19))
   assert all(tuple(sorted(x))not in union for c in classes for x in itertools.combinations(c,2))
   return classes
 return None

def run(input_path,saved_path,out):
 start=time.monotonic();raw=input_path.read_text().split();assert len(raw)==204
 faces=[tuple(sorted(map(int,raw[i:i+3])))for i in range(0,204,3)]
 layers=[e.Triangulation(19,faces[:34]),e.Triangulation(19,faces[34:])]
 for t in layers:e.verify_layer(19,t.as_dict())
 data=json.loads(saved_path.read_text());counts=collections.Counter();audits=0
 for k,move in enumerate(data['path']):
  assert len(move)==6;kind,w,a,b,c,d=move;assert w in (0,1);t=layers[w];counts[kind]+=1
  if kind==0:
   old=tuple(sorted((a,b)));assert old in t.inc;rec=t.proposal(t.edge_list.index(old))
   assert rec and rec[2]==tuple(sorted((c,d)));t.apply(rec)
  elif kind==1:
   assert a!=b and 0<=a<19 and 0<=b<19
   fs=[tuple(sorted(b if x==a else a if x==b else x for x in f))for f in t.faces]
   layers[w]=e.Triangulation(19,fs)
  elif kind==2:
   assert d==0 and 0<=c<len(ALL_FACES);layers[w]=relocate(t.faces,a,b,ALL_FACES[c])
  else:raise ValueError('Unknown move type')
  if k%1000==0:
   for t in layers:e.verify_layer(19,t.as_dict())
   audits+=2
 expected=sorted(tuple(sorted(tuple(sorted(f))for f in fs))for fs in data['faces'])
 got=sorted(tuple(sorted(t.faces))for t in layers);assert got==expected
 snap=e.snapshot(layers,{'replayed_from':saved_path.name,'moves':len(data['path'])});verified=e.verify(snap)
 assert all(snap[k]==data[k]for k in ('independent_triples','overlap','union_edges'))
 union=set(layers[0].inc)|set(layers[1].inc);color=nine_coloring(snap['remaining_triples'],union)
 out.mkdir(parents=True,exist_ok=True)
 (out/'checkpoint.json').write_text(json.dumps(snap,indent=2)+'\n')
 result={'status':'PASS','source_input_sha256':hashlib.sha256(input_path.read_bytes()).hexdigest(),'saved_path_sha256':hashlib.sha256(saved_path.read_bytes()).hexdigest(),'moves':len(data['path']),'move_counts':dict(counts),'periodic_sphere_checks':audits,'verified':verified,'nine_coloring':color,'seconds':time.monotonic()-start}
 (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(saved_path.name,len(data['path']),snap['independent_triples'],snap['overlap'],'color9',color is not None,flush=True);return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--saved',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.input,a.saved,a.out)
