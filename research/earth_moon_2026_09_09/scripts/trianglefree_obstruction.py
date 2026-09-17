#!/usr/bin/env python3
"""Exact test for a triangle-free subgraph exceeding the two-planar Euler bound.

For each vertex support size k, choose exactly k vertices and at least 4k-7
edges of the supplied graph, forbid every triangle, and require selected edge
endpoints. If every case is independently RUP-checked UNSAT, this one graph
passes this necessary obstruction for all vertex subsets. That is not biplanarity.
"""
from __future__ import annotations
import argparse,itertools,json,time,threading,subprocess,math
from pathlib import Path
from pysat.solvers import Solver
from pysat.formula import IDPool,CNF
from pysat.card import CardEnc,EncType

def build(n,edges,k):
 pool=IDPool();ev={e:pool.id(('edge',e))for e in sorted(edges)};vv={v:pool.id(('vertex',v))for v in range(n)}
 clauses=[]
 for (u,v),x in ev.items():clauses.extend([[-x,vv[u]],[-x,vv[v]]])
 for t in itertools.combinations(range(n),3):
  pairs=list(itertools.combinations(t,2))
  if all(e in ev for e in pairs):clauses.append([-ev[e]for e in pairs])
 clauses+=CardEnc.equals(list(vv.values()),k,vpool=pool,encoding=EncType.seqcounter).clauses
 wanted=4*k-7
 if wanted>len(ev):clauses.append([])
 else:clauses+=CardEnc.atleast(list(ev.values()),wanted,vpool=pool,encoding=EncType.seqcounter).clauses
 return clauses,ev,vv

def run(n,edges,out,seconds=60):
 out.mkdir(parents=True,exist_ok=True);rows=[];E=set(map(tuple,edges));start=time.monotonic()
 for k in range(3,n+1):
  if k*k//4<=4*k-8:
   rows.append({'k':k,'status':'EXCLUDED_BY_MANTEL','maximum_trianglefree_edges':k*k//4,'allowed':4*k-8});continue
  cs,ev,vv=build(n,E,k);dest=out/f'k{k}';dest.mkdir(exist_ok=True);CNF(from_clauses=cs).to_file(str(dest/'formula.cnf'))
  status='UNKNOWN_LIMIT';stats={};ts=time.monotonic()
  with Solver(name='g4',bootstrap_with=cs,with_proof=True)as s:
   timer=threading.Timer(seconds,s.interrupt);timer.daemon=True;timer.start()
   try:result=s.solve_limited(expect_interrupt=True)
   finally:timer.cancel()
   stats=s.accum_stats()
   if result is True:
    mo=set(s.get_model());vs={v for v,x in vv.items()if x in mo};es={e for e,x in ev.items()if x in mo}
    assert len(vs)==k and len(es)>4*k-8 and all(set(e)<=vs for e in es)
    assert all(not(set(itertools.combinations(t,2))<=es)for t in itertools.combinations(sorted(vs),3))
    status='SAT_DENSITY_OBSTRUCTION';(dest/'witness.json').write_text(json.dumps({'vertices':sorted(vs),'edges':sorted(es)},indent=2)+'\n')
   elif result is False:
    proof=s.get_proof();(dest/'proof.drup').write_text('\n'.join(proof)+'\n');status='UNSAT_PROOF_LOGGED'
    try:
     q=subprocess.run([str(Path(__file__).with_name('rup_check')),str(dest/'formula.cnf'),str(dest/'proof.drup')],capture_output=True,text=True,timeout=90);(dest/'rup.log').write_text(q.stdout+q.stderr)
     if q.returncode==0:status='UNSAT_RUP_CHECKED'
    except subprocess.TimeoutExpired:pass
  rows.append({'k':k,'status':status,'seconds':time.monotonic()-ts,'stats':stats});print(k,status,time.monotonic()-ts,flush=True)
  if status=='SAT_DENSITY_OBSTRUCTION':break
 result={'n':n,'edges':len(E),'rows':rows,'seconds':time.monotonic()-start,
  'status':'OBSTRUCTION_FOUND'if any(r['status']=='SAT_DENSITY_OBSTRUCTION'for r in rows)else 'PASSES_ALL_TRIANGLEFREE_SUBGRAPH_BOUNDS'if len(rows)==n-2 and all(r['status']in('EXCLUDED_BY_MANTEL','UNSAT_RUP_CHECKED')for r in rows)else 'UNKNOWN_LIMIT',
  'biplanarity_proved':False}
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True);return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=float,default=60);a=p.parse_args();d=json.loads(a.input.read_text());run(d['n'],d['edges'],a.out,a.seconds)
if __name__=='__main__':main()
