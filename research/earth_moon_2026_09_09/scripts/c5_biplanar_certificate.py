#!/usr/bin/env python3
"""C5-defect census with certified triangle-free subgraph cuts for biplanarity.

The SAT domain uses necessary conditions only. A survivor is NOT biplanar unless
separately partitioned. Every exclusion is justified by a validated independent9
or triangle-free-density witness and an independently checked Boolean proof.
"""
from pathlib import Path
import itertools,json,time,argparse,subprocess,threading
from pysat.solvers import Solver
from pysat.formula import CNF
import c5_defect_certificate as base

def density_witness(es,groups,bad):
 G=set(base.ALL)-es;typ={v:i for i,g in enumerate(groups)for v in g};best=None
 for labels in itertools.product(range(5),repeat=len(bad)):
  tt=typ.copy();tt.update({b[0]:t for b,t in zip(bad,labels)})
  edges={e for e in G if (tt[e[0]]-tt[e[1]])%5 in (2,3)};vs=set(range(19))
  while len(vs)>3:
   degrees={v:sum(v in e for e in edges)for v in vs};v=min(vs,key=degrees.get)
   if degrees[v]>=4:break
   vs.remove(v);edges={e for e in edges if v not in e}
  if len(edges)>4*len(vs)-8:
   assert all(not all(e in edges for e in itertools.combinations(t,2))for t in itertools.combinations(sorted(vs),3))
   return sorted(vs),sorted(edges)
 return None

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--edges',type=int,choices=[71,72,73,74],default=73);ap.add_argument('--seconds',type=float,default=240);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--model-limit',type=int,default=10000);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);C=base.cases(a.edges);(a.out/'cases.json').write_text(json.dumps(C,indent=2))
 start=time.monotonic();rows=[];overall='UNSAT_ALL_CASES';rup=Path(__file__).with_name('rup_check')
 for j,case in enumerate(C):
  remain=a.seconds-(time.monotonic()-start)
  if remain<=0:overall='UNKNOWN_LIMIT';break
  dest=a.out/f'case_{j:05d}';dest.mkdir();cs,ev,forced,groups,bad=base.instance(case,a.edges);cuts=[];models=0;found=None;status='UNKNOWN_LIMIT'
  # Guaranteed regular-part join obstruction is checked before calling SAT.
  poss=forced|set(ev);fixedw=density_witness(poss,groups,[]) if not bad else None
  if fixedw:
   vs,ee=fixedw;cs.append([ev[e]for e in ee if e in ev]);cuts.append({'kind':'trianglefree_density','vertices':vs,'edges':ee})
  with Solver(name='g4',bootstrap_with=cs)as s:
   timer=threading.Timer(remain,s.interrupt);timer.daemon=True;timer.start()
   try:
    while models<a.model_limit:
     sat=s.solve_limited(expect_interrupt=True)
     if sat is None:break
     if sat is False:status='UNSAT';break
     models+=1;mo=set(s.get_model());es=forced|{e for e,x in ev.items()if x in mo}
     assert len(es)>=a.edges and max(sum(v in e for e in es)for v in range(19))<=8
     assert all(not all(e in es for e in itertools.combinations(t,2))for t in itertools.combinations(range(19),3))
     ind=base.independent9(es)
     if ind is not None:
      pairs=list(itertools.combinations(sorted(ind),2));assert not(set(pairs)&es);cut=[ev[e]for e in pairs if e in ev];record={'kind':'independent9','vertices':sorted(ind)}
     else:
      w=density_witness(es,groups,bad)
      if w is None:found=es;status='SURVIVING_NECESSARY_GRAPH';break
      vs,ee=w;assert set(ee).isdisjoint(es);cut=[ev[e]for e in ee if e in ev];record={'kind':'trianglefree_density','vertices':vs,'edges':ee}
     cs.append(cut);s.add_clause(cut);cuts.append(record)
   finally:timer.cancel()
  CNF(from_clauses=cs).to_file(str(dest/'formula.cnf'));(dest/'case.json').write_text(json.dumps({'case':case,'groups':groups,'bad':bad,'cuts':cuts,'models':models},indent=2))
  if found is not None:
   (dest/'H.json').write_text(json.dumps({'n':19,'edges':sorted(found),'edge_count':len(found)},indent=2));overall=status;rows.append({'case':j,'status':status,'models':models,'cuts':len(cuts)});print('SURVIVOR',j,case,len(found),flush=True);break
  if status=='UNSAT':
   with Solver(name='g4',bootstrap_with=cs,with_proof=True)as ss:
    assert ss.solve()is False;pr=ss.get_proof();(dest/'proof.drup').write_text('\n'.join(pr)+'\n')
   q=subprocess.run([str(rup),str(dest/'formula.cnf'),str(dest/'proof.drup')],capture_output=True,text=True,timeout=90);(dest/'rup.log').write_text(q.stdout+q.stderr)
   if q.returncode:raise AssertionError('RUP rejected '+str(j)+q.stderr)
   status='UNSAT_RUP_CHECKED'
  else:overall='UNKNOWN_LIMIT'
  rows.append({'case':j,'status':status,'models':models,'cuts':len(cuts)})
  if j%20==0:print('case',j,'/',len(C),'seconds',time.monotonic()-start,flush=True)
  if overall=='UNKNOWN_LIMIT':break
 (a.out/'report.json').write_text(json.dumps({'status':overall,'edge_threshold':a.edges,'cases_total':len(C),'cases_processed':len(rows),'rows':rows,'seconds':time.monotonic()-start,'scope':'complement C5 defect family with necessary max-degree8, no-independent9 and triangle-free G-subgraph bounds; survivor not a biplanar claim'},indent=2));print('DONE',overall,len(rows),'/',len(C),'seconds',time.monotonic()-start)
if __name__=='__main__':main()
