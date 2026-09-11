#!/usr/bin/env python3
"""Finite reconstruction controls for QG archive sections 38-69.

These checks validate algebraic consequences and information-retention warnings.
They do not prove the historical physical interpretations or external literature claims.
Standard-library only.
"""
from __future__ import annotations
from pathlib import Path
import itertools,json,math
HERE=Path(__file__).resolve().parent
checks=[]
def req(x,msg):
    if not x: raise AssertionError(msg)
    checks.append(msg)
def frob(A): return math.sqrt(sum(x*x for r in A for x in r))
def sub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def mm(A,B):
    BT=list(zip(*B));return [[sum(x*y for x,y in zip(r,c)) for c in BT] for r in A]
def inv2(S):
    d=S[0][0]*S[1][1]-S[0][1]*S[1][0]
    return [[S[1][1]/d,-S[0][1]/d],[-S[1][0]/d,S[0][0]/d]]
def trans(A): return [list(x) for x in zip(*A)]
def eta_exp(T):
    n=len(T);return sum(T[i][j]-T[j][i] for i in range(n) for j in range(i+1,n))
def permute(T,p): return [[T[p[i]][p[j]] for j in range(len(p))] for i in range(len(p))]
def current(T): return [[T[i][j]-T[j][i] for j in range(len(T))] for i in range(len(T))]

def main():
    # 40: old ±1 irrep taxonomy is not exhaustive: finite witness of distinct characters t -> z.
    zs=[1,2,-1,1j,2+1j]
    req(len({str(z) for z in zs})==5 and all(z!=0 for z in zs),'multiple distinct Z characters')

    # 41: Frobenius spectral-matrix distance needs controlled identification.
    A=[[1.,0.],[0.,0.]];B=[[0.,0.],[0.,1.]];th=.37;c=math.cos(th);s=math.sin(th);Q=[[c,-s],[s,c]]
    d0=frob(sub(A,B));d_orth=frob(sub(mm(mm(Q,A),trans(Q)),mm(mm(Q,B),trans(Q))))
    req(abs(d0-d_orth)<1e-12,'Frobenius distance preserved by common orthogonal conjugation')
    S=[[2.,1.],[0.,1.]];Si=inv2(S);d_sim=frob(sub(mm(mm(S,A),Si),mm(mm(S,B),Si)))
    req(abs(d_sim-d0)>1e-6,'Frobenius distance changes under arbitrary similarity')

    # 43: positive pairwise obstruction over a positive fraction can scale quadratically.
    pair_counts={}
    for N in (5,10,20):
        pc=sum(1 for i in range(N) for j in range(i+1,N));pair_counts[N]=pc
        req(pc==N*(N-1)//2,'quadratic pair count N='+str(N))

    # 45: integrality alone makes the ambient admissible set non-convex.
    midpoint=[[.5,.5],[.5,.5]]
    req(any(x!=round(x) for r in midpoint for x in r),'integer structure midpoint leaves integral set')

    # 55: old eta_exp scalar depends on arbitrary cluster numbering.
    T=[[0,3,0],[1,0,4],[2,0,0]]
    relabel={str(p):eta_exp(permute(T,p)) for p in itertools.permutations(range(3))}
    req(set(relabel.values())=={-4,0,4},'eta_exp changes under relabeling')
    J=current(T);p=(0,2,1);Jp=current(permute(T,p));Jcov=permute(J,p)
    req(Jp==Jcov,'antisymmetric current matrix transforms covariantly')

    # 60: local factor exponent n/2 vs integrated distance exponent 1+n/2.
    exponent_rows=[]
    for n in (1,2,3,4):
        local=n/2;integrated=1+n/2;exponent_rows.append({'n':n,'local':local,'integrated':integrated})
        req(integrated-local==1,'integrated exponent differs by one for n='+str(n))
    for n in (1,2):
        x=.07;exact=x**(1+n/2)/(1+n/2);N=200000;h=x/N;total=0.0
        for k in range(N+1):
            xx=k*h;w=.5 if k in (0,N) else 1.0;total+=w*xx**(n/2)
        numeric=h*total
        req(abs(numeric-exact)<2e-8,'numerical arc-length integral n='+str(n))

    # 61: simple PSD zero vs indefinite sign-changing zero toy models.
    for x in (-.2,.2): req(x*x>=0,'PSD toy determinant nonnegative')
    req((-0.2)*(0.2)<0,'indefinite simple-zero toy determinant changes sign')

    # 62: preserve observation, not physical horizon identification.
    observed=[1.9868,.9934,1.0308,.5154];targets=[2,1,1,.5];errs=[abs(a-b) for a,b in zip(observed,targets)]
    req(max(errs)<.031,'reported exponents numerically near proposed 2,1,1,1/2 values')

    out={
      'status':'PASS','campaign':'QG-ARCHIVE-RECOVERY-38-69-01','checks':len(checks),
      'key_results':{
        'distinct_Z_character_witnesses':[str(z) for z in zs],
        'frobenius_distance':{'canonical':d0,'orthogonal_common_frame':d_orth,'arbitrary_similarity':d_sim},
        'pair_counts':pair_counts,
        'eta_exp_under_relabeling':relabel,
        'quantum_metric_exponents':exponent_rows,
        'reported_exponent_absolute_errors':errs,
      },
      'scope':'Finite algebraic/retention controls only. External experimental/literature statements and physical interpretations are not certified by this script.'
    }
    (HERE/'qg_archive_recovery_38_69_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
