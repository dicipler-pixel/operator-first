#!/usr/bin/env python3
"""Two-layer partition via the three-order criterion (Schnyder; SAT2023 Sec3.2).

This is an eager feasibility encoding, not a new planarity theorem. Optional
previous Kuratowski cuts are semantically rechecked before use. Bounded failure
is UNKNOWN. A SAT witness is independently checked by NetworkX.
"""
from __future__ import annotations
import argparse,itertools,json,threading,time,subprocess
from pathlib import Path
import networkx as nx
from pysat.formula import IDPool,CNF
from pysat.solvers import Solver
import exact_partition as ep
import fixed_layer_sat as fp

def order_formula(n,edges,base=True):
 if base:cs,ev,setup=ep.build(n,edges,True,True);pool=IDPool(start_from=setup['variable_count']+1)
 else:pool=IDPool();ev={e:pool.id(('edge',e)) for e in sorted(edges)};cs=[]
 orders={}
 for side in range(2):
  orders[side]={}
  for i in range(3):
   oo={(a,b):pool.id(('order',side,i,a,b))for a,b in itertools.combinations(range(n),2)};orders[side][i]=oo
   def lt(a,b):return oo[a,b] if a<b else -oo[b,a]
   for a,b,c in itertools.combinations(range(n),3):
    x,y,z=lt(a,b),lt(b,c),lt(a,c);cs.extend([[-x,-y,z],[x,y,-z]])
  for (a,b),e in ev.items():
   for c in range(n):
    if c in (a,b):continue
    witnesses=[]
    for i in range(3):
     oo=orders[side][i];x=oo[a,c] if a<c else -oo[c,a];y=oo[b,c] if b<c else -oo[c,b]
     z=pool.id(('above',side,a,b,c,i));cs.extend([[-z,x],[-z,y],[z,-x,-y]]);witnesses.append(z)
    cs.append(([-e] if side==0 else[e])+witnesses)
 return cs,ev,orders,pool.top

def controls():
 count=0
 # Check criterion directly on many fixed small graphs; color gate pinned true.
 rng=__import__('random').Random(916)
 for n in range(3,8):
  ee=list(itertools.combinations(range(n),2))
  cases=[set(ee),set(ee[:n-1])]
  cases +=[{e for e in ee if rng.random()<p}for p in [.2,.5,.8] for _ in range(10)]
  for E in cases:
   cs,ev,oo,_=order_formula(n,sorted(E),False);cs +=[[x]for x in ev.values()]
   with Solver(name='g4',bootstrap_with=cs)as s:got=s.solve()
   assert got==nx.check_planarity(fp.graph(n,E))[0];count+=1
 return count

def run(input_path,out,seconds,cutfile=None,solver='g4'):
 d=json.loads(input_path.read_text());n=d['n'];E=sorted(map(tuple,d['edges']));cs,ev,oo,top=order_formula(n,E)
 cuts=[]
 if cutfile:
  cuts=json.loads(cutfile.read_text())
  for cut in cuts:
   es=sorted(map(tuple,cut['edges']));assert set(es)<=set(E);assert cut['layer'] in(0,1);fp.kuratowski(es)
   cs.append([-ev[e]if cut['layer']==0 else ev[e]for e in es])
 out.mkdir(parents=True,exist_ok=True);CNF(from_clauses=cs).to_file(str(out/'formula.cnf'));start=time.monotonic();status='UNKNOWN_LIMIT'
 with Solver(name=solver,bootstrap_with=cs,with_proof=True)as s:
  timer=threading.Timer(seconds,s.interrupt);timer.daemon=True;timer.start()
  try:answer=s.solve_limited(expect_interrupt=True)
  finally:timer.cancel()
  stats=s.accum_stats()
  if answer is True:
   mo=set(s.get_model());ls=[{e for e,x in ev.items()if x in mo},{e for e,x in ev.items()if x not in mo}]
   assert all(nx.check_planarity(fp.graph(n,L))[0]for L in ls)
   witness={'n':n,'edges':E,'partition':[sorted(L)for L in ls],'orders':[]}
   for w,L in enumerate(ls):
    table=[]
    for i in range(3):
     def less(a,b):return (oo[w][i][a,b]in mo)if a<b else not(oo[w][i][b,a]in mo)
     ordering=sorted(range(n),key=lambda a:sum(less(b,a)for b in range(n)if b!=a))
     rank={v:j for j,v in enumerate(ordering)}
     assert all(less(a,b)==(rank[a]<rank[b])for a,b in itertools.combinations(range(n),2));table.append(ordering)
    ranks=[{v:j for j,v in enumerate(order)}for order in table]
    assert all(any(r[a]<r[c] and r[b]<r[c] for r in ranks)for a,b in L for c in range(n)if c not in(a,b))
    witness['orders'].append(table)
   (out/'candidate.json').write_text(json.dumps(witness,indent=2)+'\n');status='SAT_PLANAR'
  elif answer is False:
   proof=s.get_proof();(out/'proof.drup').write_text('\n'.join(proof)+'\n');status='UNSAT_PROOF_LOGGED'
   try:
    p=subprocess.run([str(Path(__file__).with_name('rup_check')),str(out/'formula.cnf'),str(out/'proof.drup')],capture_output=True,text=True,timeout=180)
    (out/'rup.log').write_text(p.stdout+p.stderr)
    if p.returncode==0:status='UNSAT_RUP_CHECKED'
   except subprocess.TimeoutExpired:pass
 report={'status':status,'n':n,'edges':len(E),'clauses':len(cs),'variables':top,'previous_cuts_rechecked':len(cuts),'seconds':time.monotonic()-start,'stats':stats,'scope':'the one supplied union graph; independent 3-order witnesses for each edge layer','solver':solver}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=int,default=300);p.add_argument('--cuts',type=Path);p.add_argument('--self-test',action='store_true');p.add_argument('--solver',default='g4');a=p.parse_args()
 if a.self_test:
  n=controls();a.out.mkdir(parents=True,exist_ok=True);(a.out/'controls.json').write_text(json.dumps({'status':'PASS','small_fixed_graphs':n},indent=2)+'\n');print(n)
 else:run(a.input,a.out,a.seconds,a.cuts,a.solver)
