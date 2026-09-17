#!/usr/bin/env python3
"""Exact thickness-two test for a supplied union graph, not a global search.

Every edge receives one of two layers. Every lazy cut is a checked K5/K3,3
subdivision; symmetry uses only verified graph automorphisms and layer exchange.
Timeouts stay UNKNOWN. Finite UNSAT proof logs are checked by separate C++ RUP.
"""
from __future__ import annotations
import argparse,itertools,json,subprocess,time,threading
from pathlib import Path
import networkx as nx
from pysat.formula import IDPool,CNF
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
import fixed_layer_sat as fp

class Oracle:
 def __init__(self,path):
  self.raw_subdivision_fallbacks=0
  self.proc=subprocess.Popen([str(path)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,bufsize=1)
 def __call__(self,n,es):
  es=sorted(es);self.proc.stdin.write(' '.join(map(str,[n,len(es)]+[v for e in es for v in e]))+'\n');self.proc.stdin.flush();w=self.proc.stdout.readline().split()
  if w==['P']:return True,None
  if not w or w[0]!='C':raise RuntimeError('Oracle protocol failed')
  count=int(w[1]);vals=list(map(int,w[2:]));assert len(vals)==2*count
  witness=sorted(tuple(sorted(vals[i:i+2]))for i in range(0,len(vals),2))
  assert len(set(witness))==len(witness) and set(witness)<=set(es)
  try:fp.kuratowski(witness)
  except ValueError:
   good,cert=nx.check_planarity(fp.graph(n,witness),counterexample=True)
   if good:raise AssertionError('False nonplanarity proposal')
   self.raw_subdivision_fallbacks+=1
   witness=sorted(tuple(sorted(e))for e in cert.edges());fp.kuratowski(witness)
  return False,witness
 def close(self):self.proc.stdin.close();self.proc.wait(timeout=5)

def lex_leader(xs,ys,pool):
 cs=[];prev=None
 for x,y in zip(xs,ys):
  if x==y:continue
  cs.append(([-prev]if prev else[])+[-x,y]);nxt=pool.id()
  cs.append(([-prev]if prev else[])+[x,y,nxt]);cs.append(([-prev]if prev else[])+[-x,-y,nxt])
  cs.extend([[-nxt,-x,y],[-nxt,x,-y]])
  if prev:cs.append([-nxt,prev])
  prev=nxt
 return cs

def build(n,es,symmetry=True,cliques=True):
 es=sorted(es);pool=IDPool();ev={e:pool.id(('edge',e))for e in es};cs=[];v=list(ev.values());bound=3*n-6
 cs+=CardEnc.atmost(v,bound,vpool=pool,encoding=EncType.seqcounter).clauses
 cs+=CardEnc.atmost([-x for x in v],bound,vpool=pool,encoding=EncType.seqcounter).clauses
 # Lex minimum under automorphisms AND color complementation has first bit zero.
 if v:cs.append([-v[0]])
 g=fp.graph(n,es);autos=[];subsets=[];E=set(es)
 if symmetry:
  for a,b in itertools.combinations(range(n),2):
   perm=list(range(n));perm[a],perm[b]=b,a
   if {tuple(sorted((perm[u],perm[w])))for u,w in es}==E:
    ys=[ev[tuple(sorted((perm[u],perm[w])))]for u,w in es]
    cs+=lex_leader(v,ys,pool);autos.append([a,b])
 if cliques:
  subsets+=sorted(tuple(sorted(c))for c in nx.find_cliques(g)if len(c)>=5)
  subsets += [tuple(w for w in range(n)if w!=u)for u in range(n)]
  for subset in subsets:
   ss=set(subset);vv=[ev[e]for e in es if set(e)<=ss];b=3*len(ss)-6
   if len(vv)>b:
    cs+=CardEnc.atmost(vv,b,vpool=pool,encoding=EncType.seqcounter).clauses
    cs+=CardEnc.atmost([-x for x in vv],b,vpool=pool,encoding=EncType.seqcounter).clauses
 small=[]
 for c in itertools.combinations(range(n),5):
  ee=list(itertools.combinations(c,2))
  if set(ee)<=E:
   xs=[ev[e]for e in ee];cs.extend([xs,[-x for x in xs]]);small.append(list(c))
 return cs,ev,{'automorphism_transpositions':autos,'Euler_subsets':subsets,'K5_sets':small,'variable_count':pool.top}

def solve(n,es,out,seconds=120,model_limit=500000,proof_seconds=120,symmetry=True,oracle_path=None):
 out.mkdir(parents=True,exist_ok=True);es=sorted(set(map(tuple,es)));cs,ev,setup=build(n,es,symmetry);base_len=len(cs)
 CNF(from_clauses=cs).to_file(str(out/'initial.cnf'));cuts=[];models=0;status='UNKNOWN_LIMIT';candidate=None;t=time.monotonic();oracle=Oracle(oracle_path)if oracle_path else None
 with Solver(name='g4',bootstrap_with=cs)as s:
  timer=threading.Timer(seconds,s.interrupt);timer.daemon=True;timer.start()
  try:
   while models<model_limit and time.monotonic()-t<seconds:
    sat=s.solve_limited(expect_interrupt=True)
    if sat is None:break
    if sat is False:status='UNSAT_SOLVER';break
    models+=1;model=set(s.get_model());layers=[{e for e,x in ev.items()if x in model},{e for e,x in ev.items()if x not in model}];allgood=True
    for side,L in enumerate(layers):
     if oracle:good,w=oracle(n,L)
     else:
      good,ob=nx.check_planarity(fp.graph(n,L),counterexample=True);w=None if good else sorted(tuple(sorted(e))for e in ob.edges())
     if good:
      assert nx.check_planarity(fp.graph(n,L))[0];continue
     allgood=False;core=fp.kuratowski(w);cut=[-ev[e]if side==0 else ev[e]for e in w]
     s.add_clause(cut);cs.append(cut);cuts.append({'layer':side,'edges':w,'core':core})
    if allgood:
     candidate={'n':n,'edges':es,'partition':[sorted(L)for L in layers],'embeddings':[]}
     for L in layers:
      good,emb=nx.check_planarity(fp.graph(n,L));assert good
      candidate['embeddings'].append({str(v):list(emb.neighbors_cw_order(v))for v in range(n)})
     (out/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n');status='SAT_PLANAR';break
    if models%1000==0:
     print('models',models,'cuts',len(cuts),'seconds',time.monotonic()-t,flush=True)
     (out/'partial.json').write_text(json.dumps({'status':'RUNNING','models':models,'cuts':len(cuts),'seconds':time.monotonic()-t}))
  finally:
   timer.cancel()
   if oracle:oracle.close()
  stats=s.accum_stats()
 CNF(from_clauses=cs).to_file(str(out/'final.cnf'));(out/'cuts.json').write_text(json.dumps(cuts,separators=(',',':'))+'\n');(out/'setup.json').write_text(json.dumps({'n':n,'edges':es,'symmetry':symmetry,**setup},indent=2)+'\n')
 proof_checked=False;proof_lines=0
 if status=='UNSAT_SOLVER':
  with Solver(name='g4',bootstrap_with=cs,with_proof=True)as s:
   timer=threading.Timer(proof_seconds,s.interrupt);timer.daemon=True;timer.start()
   try:result=s.solve_limited(expect_interrupt=True)
   finally:timer.cancel()
   if result is False:
    proof=s.get_proof();(out/'proof.drup').write_text('\n'.join(proof)+'\n');proof_lines=len(proof);status='UNSAT_PROOF_LOGGED'
    try:
     r=subprocess.run([str(Path(__file__).with_name('rup_check')),str(out/'final.cnf'),str(out/'proof.drup')],capture_output=True,text=True,timeout=proof_seconds);(out/'rup.log').write_text(r.stdout+r.stderr);proof_checked=r.returncode==0
     if proof_checked:status='UNSAT_RUP_CHECKED'
    except subprocess.TimeoutExpired:pass
 report={'status':status,'n':n,'edges':len(es),'base_clauses':base_len,'final_clauses':len(cs),'models':models,'checked_Kuratowski_cuts':len(cuts),'raw_witnesses_requiring_minimization':oracle.raw_subdivision_fallbacks if oracle else 0,'proof_checked':proof_checked,'proof_lines':proof_lines,'stats':stats,'seconds':time.monotonic()-t,'scope':'exact two-planar-edge-partition of the one supplied union graph; not all graphs of this order'}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True);return report

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=float,default=120);p.add_argument('--no-symmetry',action='store_true');p.add_argument('--oracle',type=Path,default=Path(__file__).with_name('planarity_oracle'))
 a=p.parse_args();data=json.loads(a.input.read_text());solve(data['n'],data['edges'],a.out,a.seconds,symmetry=not a.no_symmetry,oracle_path=a.oracle.resolve())
if __name__=='__main__':main()
