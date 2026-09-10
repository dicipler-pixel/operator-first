#!/usr/bin/env python3
"""Bounded structural complement census, separate from planar-pair discovery.

Every candidate H is triangle-free, degree<=8 and alpha<=8. A fixed induced
five-cycle partitions vertices with two cycle-neighbors into five classes.
Others are exceptions with zero or one cycle-neighbor. The exact deficit
identity bounds their count by 150-2|E(H)|. This enumerates those finite cases.
UNSAT requires saved CNF, checked forbidden-independent-set cuts, and RUP proof.
"""
from __future__ import annotations
import argparse,itertools,json,time,subprocess,hashlib,math
from pathlib import Path
from pysat.solvers import Solver
from pysat.formula import IDPool,CNF
from pysat.card import CardEnc,EncType
N=19
ALL=list(itertools.combinations(range(N),2))

def compositions(s,k,minval=0):
 if k==1:
  if s>=minval:yield (s,)
 else:
  for a in range(minval,s-minval*(k-1)+1):
   for b in compositions(s-a,k-1,minval):yield (a,)+b

def canonical(a,b):
 return min(tuple(a[(shift+sgn*i)%5] for i in range(5))+tuple(b[(shift+sgn*i)%5] for i in range(5)) for shift in range(5) for sgn in [-1,1])

def cases(threshold):
 D=150-2*threshold;seen=set();out=[]
 for zero in range(D//2+1):
  for one in range(D-2*zero+1):
   r=zero+one
   for a in compositions(19-r,5,1):
    if max(a)>8:continue
    if any(a[(i-1)%5]+a[(i+1)%5]>8 for i in range(5)):continue
    for b in compositions(one,5):
     if any(a[(i-1)%5]+a[(i+1)%5]+b[i]>8 for i in range(5)):continue
     key=(zero,canonical(a,b))
     if key in seen:continue
     seen.add(key);out.append({'zero':zero,'sizes':list(a),'single_counts':list(b),'defect':2*zero+one})
 return out

def instance(case,threshold):
 a,b=case['sizes'],case['single_counts'];groups=[[i] for i in range(5)];label=5
 for i in range(5):groups[i]+=list(range(label,label+a[i]-1));label+=a[i]-1
 typ={v:i for i,g in enumerate(groups)for v in g};bad=[]
 for i in range(5):
  for _ in range(b[i]):bad.append((label,i));label+=1
 for _ in range(case['zero']):bad.append((label,None));label+=1
 assert label==19
 nb=[set()for _ in range(19)]
 for i,g in enumerate(groups):
  for v in g:nb[v]={(i-1)%5,(i+1)%5}
 for v,c in bad:nb[v]=set()if c is None else{c}
 forced=set();options=set()
 for u,v in ALL:
  if u<5 or v<5:
   if u<5 and u in nb[v]:forced.add((u,v))
  elif nb[u]&nb[v]:continue
  elif u in typ and v in typ:
   if (typ[u]-typ[v])%5 in (1,4):options.add((u,v))
  else:options.add((u,v))
 pool=IDPool();ev={e:pool.id(e)for e in sorted(options)};cs=[]
 potential=forced|options
 for t in itertools.combinations(range(19),3):
  es=list(itertools.combinations(t,2))
  if all(e in potential for e in es):cs.append([-ev[e]for e in es if e in ev])
 for v in range(19):
  f=sum(v in e for e in forced);xs=[x for e,x in ev.items()if v in e]
  if f>8:cs.append([])
  elif len(xs)>8-f:cs+=CardEnc.atmost(xs,8-f,vpool=pool,encoding=EncType.seqcounter).clauses
 if threshold>len(potential):cs.append([])
 elif threshold>len(forced):cs+=CardEnc.atleast(list(ev.values()),threshold-len(forced),vpool=pool,encoding=EncType.seqcounter).clauses
 return cs,ev,forced,groups,bad

def independent9(es):
 adj=[0]*19
 for a,b in es:adj[a]|=1<<b;adj[b]|=1<<a
 def dfs(mask,chosen):
  if len(chosen)==9:return chosen
  if mask.bit_count()<9-len(chosen):return None
  if not mask:return None
  vs=[v for v in range(19)if mask>>v&1];v=max(vs,key=lambda w:(adj[w]&mask).bit_count())
  a=dfs(mask&~((1<<v)|adj[v]),chosen+[v])
  return a if a is not None else dfs(mask&~(1<<v),chosen)
 return dfs((1<<19)-1,[])

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--edges',type=int,choices=[72,73,74,75],default=74);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=float,default=300);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 C=cases(a.edges);(a.out/'cases.json').write_text(json.dumps(C,indent=2));rows=[];start=time.monotonic();status='UNSAT_ALL_CASES';rup=Path(__file__).with_name('rup_check')
 for j,case in enumerate(C):
  if time.monotonic()-start>a.seconds:status='UNKNOWN_LIMIT';break
  cs,ev,forced,groups,bad=instance(case,a.edges);cuts=[];models=0;found=None
  with Solver(name='g4',bootstrap_with=cs)as s:
   while s.solve():
    models+=1;mo=set(s.get_model());es=forced|{e for e,x in ev.items()if x in mo}
    assert len(es)>=a.edges and max(sum(v in e for e in es)for v in range(19))<=8
    assert all(not all(e in es for e in itertools.combinations(t,2))for t in itertools.combinations(range(19),3))
    ind=independent9(es)
    if ind is None:found=es;break
    assert len(ind)==9 and all(e not in es for e in itertools.combinations(sorted(ind),2))
    cut=[ev[e]for e in itertools.combinations(sorted(ind),2)if e in ev]
    cs.append(cut);s.add_clause(cut);cuts.append(sorted(ind))
  dest=a.out/f'case_{j:05d}';dest.mkdir()
  (dest/'case.json').write_text(json.dumps({'case':case,'groups':groups,'bad':bad,'independent9_cuts':cuts,'models':models},indent=2))
  CNF(from_clauses=cs).to_file(str(dest/'formula.cnf'))
  if found is not None:
   (dest/'H.json').write_text(json.dumps({'edges':sorted(found),'n':19,'edge_count':len(found)},indent=2));status='SAT_NECESSARY_GRAPH';rows.append({'case':j,'status':status,'edges':len(found)});print('SAT',case,len(found),flush=True);break
  with Solver(name='g4',bootstrap_with=cs,with_proof=True)as ss:
   assert ss.solve()is False;pr=ss.get_proof();(dest/'proof.drup').write_text('\n'.join(pr)+'\n')
  q=subprocess.run([str(rup),str(dest/'formula.cnf'),str(dest/'proof.drup')],capture_output=True,text=True,timeout=60);(dest/'rup.log').write_text(q.stdout+q.stderr)
  if q.returncode:raise AssertionError('RUP rejection '+str(j)+q.stderr)
  rows.append({'case':j,'status':'UNSAT_RUP_CHECKED','models':models,'cuts':len(cuts),'proof_lines':len(pr)})
  if j%20==0:print('case',j,'of',len(C),'seconds',time.monotonic()-start,flush=True)
 (a.out/'report.json').write_text(json.dumps({'status':status,'edge_threshold':a.edges,'cases_total':len(C),'cases_processed':len(rows),'rows':rows,'seconds':time.monotonic()-start,'scope':'necessary complement conditions with induced C5, max degree8, no independent9; no thickness assumption in SAT','proof_checker':'independent C++ RUP'},indent=2))
 print('DONE',status,len(rows),'/',len(C),'seconds',time.monotonic()-start)
if __name__=='__main__':main()
