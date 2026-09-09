#!/usr/bin/env python3
"""Independent semantic/coverage audit of saved C5-deficit exclusions.

Does not import either census producer. Independently enumerates profile orbits,
reconstructs edges from cycle-neighborhood disjointness, checks every semantic
cut, regenerates the finite CNF, and invokes an independent RUP proof checker.
The cardinality compiler (PySAT sequential counters) is shared, and is declared
as part of the trusted encoding boundary; its small instances are exhaustively
checked here. This is an executable finite certificate, not a Lean theorem.
"""
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,pathlib,subprocess,time,tempfile
from pysat.card import CardEnc,EncType
from pysat.formula import CNF,IDPool
from pysat.solvers import Solver

N=19
PAIRS=list(itertools.combinations(range(N),2))
CYCLE={tuple(sorted((i,(i+1)%5))) for i in range(5)}
AUT=[p for p in itertools.permutations(range(5))
     if {tuple(sorted((p[i],p[j]))) for i,j in CYCLE}==CYCLE]
assert len(AUT)==10

def signature(z,a,b):
    return (z,)+min(tuple(a[p[i]] for i in range(5))+tuple(b[p[i]] for i in range(5)) for p in AUT)

def independent_profiles(q):
    """Bounded degree capacities, not the producer's composition traversal."""
    budget=150-2*q;out=set()
    for a in itertools.product(range(1,8),repeat=5):
        r=N-sum(a)
        if not 0<=r<=min(14,budget):continue
        cap=[8-a[(i-1)%5]-a[(i+1)%5] for i in range(5)]
        if min(cap)<0:continue
        for b in itertools.product(*(range(min(r,c)+1) for c in cap)):
            one=sum(b);z=r-one
            if z<0 or 2*z+one>budget:continue
            out.add(signature(z,a,b))
    return out

def validate_coverage(cases,q):
    got=[]
    for c in cases:
        a,b,z=c['sizes'],c['single_counts'],c['zero']
        assert len(a)==len(b)==5 and all(type(x)is int for x in a+b+[z])
        assert min(a)>=1 and min(b)>=0 and z>=0
        assert sum(a)+sum(b)+z==N
        assert c['defect']==sum(b)+2*z<=150-2*q
        assert all(a[(i-1)%5]+a[(i+1)%5]+b[i]<=8 for i in range(5))
        got.append(signature(z,a,b))
    assert len(got)==len(set(got)), 'Duplicate orbit'
    expected=independent_profiles(q)
    assert set(got)==expected, ('Missing or extra profile orbit',len(set(got)),len(expected))
    return len(expected)

def reconstruct(case,q):
    a,b,z=case['sizes'],case['single_counts'],case['zero']
    groups=[[i] for i in range(5)];nextv=5;neighborhood=[set() for _ in range(N)]
    for i in range(5):
        groups[i]+=list(range(nextv,nextv+a[i]-1));nextv+=a[i]-1
        for v in groups[i]:neighborhood[v]={(i-1)%5,(i+1)%5}
    bad=[]
    for i in range(5):
        for _ in range(b[i]):neighborhood[nextv]={i};bad.append([nextv,i]);nextv+=1
    for _ in range(z):bad.append([nextv,None]);nextv+=1
    assert nextv==N
    forced=set(CYCLE)
    for v in range(5,N):forced|={tuple(sorted((v,c))) for c in neighborhood[v]}
    # A pair sharing a cycle neighbor is forbidden by triangle-freeness.
    # Disjoint 2-neighborhoods on C5 are precisely consecutive regular classes.
    options=[(u,v) for u,v in PAIRS if u>=5 and not(neighborhood[u]&neighborhood[v])]
    pool=IDPool();ev={e:pool.id(e) for e in options};allowed=forced|set(options);clauses=[]
    for i in range(N):
        for j in range(i+1,N):
            for k in range(j+1,N):
                ee=((i,j),(i,k),(j,k))
                if set(ee)<=allowed:clauses.append([-ev[e] for e in ee if e in ev])
    for v in range(N):
        occupied=sum(v in e for e in forced);lits=[ev[e] for e in options if v in e]
        if occupied>8:clauses.append([])
        elif len(lits)>8-occupied:
            clauses+=CardEnc.atmost(lits,8-occupied,vpool=pool,encoding=EncType.seqcounter).clauses
    if q>len(allowed):clauses.append([])
    elif q>len(forced):clauses+=CardEnc.atleast(list(ev.values()),q-len(forced),vpool=pool,encoding=EncType.seqcounter).clauses
    return clauses,ev,forced,groups,bad

def cut_clause(cut,ev,forced):
    vs=cut['vertices'];assert len(vs)==len(set(vs)) and all(type(v)is int and 0<=v<N for v in vs)
    if cut['kind']=='independent9':
        assert len(vs)==9
        ee=list(itertools.combinations(sorted(vs),2))
    elif cut['kind']=='trianglefree_density':
        assert len(vs)>=3
        ee=[tuple(e) for e in cut['edges']]
        assert ee==sorted(set(ee)), 'Unsorted/duplicate edges'
        assert all(len(e)==2 and e[0]<e[1] and set(e)<=set(vs) for e in ee)
        neighbors={v:set() for v in vs}
        for u,v in ee:neighbors[u].add(v);neighbors[v].add(u)
        assert all(not(neighbors[u]&neighbors[v]) for u,v in ee), 'Triangle in witness'
        assert len(ee)>4*len(vs)-8, 'No density violation'
    else:raise AssertionError('Unknown cut type')
    assert not(set(ee)&forced), 'Cut would omit an already true forced edge'
    return [ev[e] for e in ee if e in ev]

def cardinality_controls():
    count=0
    for n in range(0,8):
      for k in range(n+1):
       for lower in [False,True]:
        pool=IDPool(start_from=n+1)
        form=(CardEnc.atleast if lower else CardEnc.atmost)(list(range(1,n+1)),k,vpool=pool,encoding=EncType.seqcounter)
        with Solver(name='g4',bootstrap_with=form.clauses) as s:
         for values in itertools.product([False,True],repeat=n):
          result=s.solve(assumptions=[i+1 if v else -(i+1) for i,v in enumerate(values)])
          assert result==(sum(values)>=k if lower else sum(values)<=k)
          count+=1
    return count

def audit(folder,rup,out):
    start=time.monotonic();q=json.loads((folder/'report.json').read_text())['edge_threshold']
    report=json.loads((folder/'report.json').read_text());cases=json.loads((folder/'cases.json').read_text())
    assert report['status']=='UNSAT_ALL_CASES'
    assert report['cases_total']==report['cases_processed']==len(cases)
    assert [row['case'] for row in report['rows']]==list(range(len(cases)))
    assert all(row['status']=='UNSAT_RUP_CHECKED' for row in report['rows'])
    coverage=validate_coverage(cases,q);cuts=collections.Counter();steps=0;deletions=0;manifest={};models=0;emptyproofs=0
    for j,case in enumerate(cases):
        dest=folder/f'case_{j:05d}';metadata=json.loads((dest/'case.json').read_text())
        assert metadata['case']==case
        formula,ev,forced,groups,bad=reconstruct(case,q)
        assert metadata['groups']==groups and metadata['bad']==bad
        these=metadata.get('cuts')
        if these is None:these=[dict(kind='independent9',vertices=v) for v in metadata['independent9_cuts']]
        for cut in these:formula.append(cut_clause(cut,ev,forced));cuts[cut['kind']]+=1
        actual=CNF(from_file=str(dest/'formula.cnf'))
        assert actual.clauses==formula, ('CNF mismatch',j)
        run=subprocess.run([str(rup),str(dest/'formula.cnf'),str(dest/'proof.drup')],capture_output=True,text=True,timeout=120)
        assert run.returncode==0, (j,run.stderr)
        words=run.stdout.split();assert words[:3]==['VERIFIED','RUP','steps']
        steps+=int(words[3]);deletions+=int(words[5]);emptyproofs+=int(int(words[3])==0)
        models+=metadata['models']
        for name in ['case.json','formula.cnf','proof.drup']:
            p=dest/name;manifest[str(p.relative_to(folder))]=hashlib.sha256(p.read_bytes()).hexdigest()
        if j%500==0:print('audit',q,j,'/',len(cases),'seconds',time.monotonic()-start,flush=True)
    negative=0
    try:validate_coverage(cases[:-1],q)
    except AssertionError:negative+=1
    else:raise AssertionError('Missing profile accepted')
    # Reject insufficient-density and false-independent-set theory certificates.
    test={'kind':'trianglefree_density','vertices':list(range(5)),'edges':sorted(CYCLE)}
    try:cut_clause(test,{},set())
    except AssertionError:negative+=1
    else:raise AssertionError('False density cut accepted')
    test={'kind':'independent9','vertices':list(range(9))}
    try:cut_clause(test,{},CYCLE)
    except AssertionError:negative+=1
    else:raise AssertionError('Forced true edge silently omitted')
    with tempfile.TemporaryDirectory() as td:
        d=pathlib.Path(td);(d/'s.cnf').write_text('p cnf 1 1\n1 0\n');(d/'false.drup').write_text('0\n')
        r=subprocess.run([str(rup),str(d/'s.cnf'),str(d/'false.drup')],capture_output=True,text=True)
        assert r.returncode!=0;negative+=1
    result={'status':'PASS','edge_threshold':q,'profile_orbits_independently_covered':coverage,'all_final_CNF_reconstructions_matched':True,'independent_RUP_checks':len(cases),'verified_RUP_additions':steps,'ignored_deletions':deletions,'root_UP_cases':emptyproofs,'independently_checked_theory_cuts':dict(cuts),'SAT_assignments_rejected':models,'negative_controls_rejected':negative,'seconds':time.monotonic()-start,'new_Lean_compilation':False,'shared_cardinality_compiler':'PySAT seqcounter; separate exhaustive small-instance controls','claim':'No graph satisfying the stated necessary conditions and e(H)>=threshold, subject to the written C5 reduction and standard biplanar/K9 inputs.'}
    out.mkdir(parents=True,exist_ok=True);(out/'AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'CERTIFICATE_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(result,indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=pathlib.Path);p.add_argument('--out',type=pathlib.Path,required=True);p.add_argument('--rup',type=pathlib.Path,default=pathlib.Path(__file__).with_name('rup_check'));a=p.parse_args()
    count=cardinality_controls();print('exhaustive_cardinality_checks',count,flush=True)
    audit(a.folder,a.rup.resolve(),a.out)
    (a.out/'CARDINALITY_CONTROLS.json').write_text(json.dumps({'status':'PASS','exhaustive_checks':count},indent=2)+'\n')
if __name__=='__main__':main()
