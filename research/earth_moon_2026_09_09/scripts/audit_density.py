#!/usr/bin/env python3
"""Independently reconstruct and recheck all-support triangle-free obstructions.

Structural clauses are separately reconstructed. The sequential cardinality
compiler is shared (PySAT), and independently controlled on every Boolean input
through seven variables. This is not a Lean certificate.
"""
from __future__ import annotations
import argparse,json,itertools,subprocess,time
from pathlib import Path
from pysat.formula import IDPool,CNF
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver

def cardinality_controls():
 count=0
 for n in range(8):
  for bound in range(n+1):
   pool=IDPool(start_from=n+1);cs=CardEnc.equals(list(range(1,n+1)),bound,vpool=pool,encoding=EncType.seqcounter).clauses
   with Solver(name='g4',bootstrap_with=cs)as s:
    for bits in itertools.product((0,1),repeat=n):
     sat=s.solve(assumptions=[i+1 if bit else -(i+1)for i,bit in enumerate(bits)])
     assert sat==(sum(bits)==bound);count+=1
 return count

def reconstruct(n,es,k):
 es=sorted(map(tuple,es));E=set(es);pool=IDPool();mapping={uv:pool.id(('edge',uv))for uv in es};vs=[pool.id(('vertex',v))for v in range(n)];rows=[]
 for (u,v),x in mapping.items():rows.extend([[-x,vs[u]],[-x,vs[v]]])
 for a in range(n):
  for b in range(a+1,n):
   for c in range(b+1,n):
    tri=[(a,b),(a,c),(b,c)]
    if all(e in E for e in tri):rows.append([-mapping[e]for e in tri])
 rows+=CardEnc.equals(vs,k,vpool=pool,encoding=EncType.seqcounter).clauses
 if 4*k-7>len(E):rows.append([])
 else:rows+=CardEnc.atleast(list(mapping.values()),4*k-7,vpool=pool,encoding=EncType.seqcounter).clauses
 return rows

def run(source,folder,out):
 d=json.loads(source.read_text());n=d['n'];E=set(map(tuple,d['edges']));assert len(E)==len(d['edges'])
 base=json.loads((folder/'report.json').read_text());assert base['status']=='PASSES_ALL_TRIANGLEFREE_SUBGRAPH_BOUNDS' and len(base['rows'])==n-2
 out.mkdir(parents=True,exist_ok=True);records=[];start=time.monotonic()
 for k in range(3,n+1):
  if k*k//4<=4*k-8:continue
  p=folder/f'k{k}';actual=CNF(from_file=str(p/'formula.cnf')).clauses
  assert actual==reconstruct(n,E,k)
  proc=subprocess.run([str(Path(__file__).with_name('rup_check')),str(p/'formula.cnf'),str(p/'proof.drup')],capture_output=True,text=True,timeout=120)
  assert proc.returncode==0,proc.stderr;(out/f'k{k}_rup.log').write_text(proc.stdout+proc.stderr);records.append({'k':k,'RUP':proc.stdout.strip()})
 controls=cardinality_controls()
 (out/'false.cnf').write_text('p cnf 1 1\n1 0\n');(out/'false.drup').write_text('0\n')
 q=subprocess.run([str(Path(__file__).with_name('rup_check')),str(out/'false.cnf'),str(out/'false.drup')],capture_output=True,text=True)
 assert q.returncode!=0
 result={'status':'PASS','n':n,'edges':len(E),'all_supports_covered':list(range(3,n+1)),'CNF_reconstructions_matched':len(records),'proofs':records,'equality_cardinality_truth_tests':controls,'false_empty_proof_rejected':True,'biplanarity_proved':False,'seconds':time.monotonic()-start}
 (out/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--certificates',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.input,a.certificates,a.out)
