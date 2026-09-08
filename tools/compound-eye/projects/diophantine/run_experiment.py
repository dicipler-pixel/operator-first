"""Reproducible discovery/validation split; exact finite-field arithmetic.
Original discovery window: 401..1499. Fixed validation window: 1501..4999.
Selection searches all 780 original branch pairs and all 74 signed twists.
Three overall and three positive-twist candidates per surface are frozen at
the discovery boundary, then evaluated on the disjoint validation primes.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,time
import numpy as np
from sympy import primerange,factorint
from exact_counts import legendre,correlation,direct
HERE=Path(__file__).resolve().parent
EQS=[(0,0,-2),(0,-1,-1),(0,1,-1),(0,1,1),(0,0,-3),(0,0,3),(0,-1,-2),(0,-1,2),(-1,0,2)]
def mod(x,p): return x.numerator*pow(x.denominator,-1,p)%p
def main():
    start=time.time();rats=sorted({F(n,d) for d in range(1,6) for n in range(-5,6)})
    pairs=list(itertools.combinations(rats,2))+[(r,None) for r in rats]
    cs=[c for c in range(-60,61) if c and all(e<2 for e in factorint(abs(c)).values())]
    primes=list(primerange(3,5000));ds=[p for p in primes if 401<=p<1500]
    discovery=np.zeros((9,len(pairs),len(ds)),dtype=np.int64)
    signs=np.array([[int(legendre(p)[c%p]) for p in ds] for c in cs])
    base=[];controls=[];spike=[];chosen=[];validate=[];ntt_checks=0
    for index,p in enumerate(primes):
        chi=legendre(p);y=np.arange(p,dtype=np.int64)
        corr={b:correlation(p,chi,b) for b in [-1,0,1]}
        control0=correlation(p,chi,0,1);control1=correlation(p,chi,1,1)
        # Independent direct point counts: all shifts at small primes; fixed
        # probe shifts at every larger prime, not a floating-point spot check.
        shifts=list(range(p)) if p<50 else [0,1,2,17%p,p//2,p-1]
        for b in [-1,0,1]:
            assert np.array_equal(corr[b][shifts],direct(p,chi,b,shifts));ntt_checks+=len(shifts)
        A=[corr[b][(((y*y+a)%p)**2-4*c)%p] for a,b,c in EQS]
        base.append({'prime':p,'numerators':[int(a.sum()) for a in A]})
        c0=int(control0[(y*y+1)%p].sum());c1=int(control1[(1-y*y%p*y-y)%p].sum())
        assert c0==p*(len([x for x in range(p) if (x*x*x+1)%p==0])-1)
        controls.append({'prime':p,'mislabeled_rank0_numerator':c0,'visible_section_numerator':c1})
        if p>3:
            r=3*pow(2,-1,p)%p;d=(r*r-y*y)%p
            sn=int((chi[d]*A[3]).sum());missing=int(A[3][-r%p])
            spike.append({'prime':p,'twist_numerator':sn,'base_numerator':int(A[3].sum()),
                          'affine_cover_numerator':int(A[3].sum())+sn-missing,'omitted_infinity':missing})
        if p in ds:
            j=ds.index(p)
            for i,(f1,f2) in enumerate(pairs):
                d=(y-mod(f1,p))%p
                if f2 is not None:d=d*(y-mod(f2,p))%p
                for e in range(9):discovery[e,i,j]=int((chi[d]*A[e]).sum())
            if p==ds[-1]:
                for e in range(9):
                    values=discovery[e]/np.array(ds)
                    means=values@signs.T/len(ds)
                    order=sorted(np.ndindex(means.shape),key=lambda ij:(-means[ij],ij))
                    selected=list(dict.fromkeys(order[:3]+[ij for ij in order if cs[ij[1]]>0][:3]))
                    for i,jj in selected:
                        series=(values[i]*signs[jj]).tolist()
                        chosen.append({'equation':e,'abc':EQS[e],'pair':[str(pairs[i][0]),str(pairs[i][1]) if pairs[i][1] is not None else None],
                            'twist':cs[jj],'discovery_mean':float(np.mean(series)),
                            'discovery_descriptive_se':float(np.std(series,ddof=1)/len(series)**.5),
                            'discovery_values':series,'validation_numerators':[]})
                print('Discovery frozen:',len(chosen),'candidates',flush=True)
        elif p>=1500:
            validate.append(p)
            for c in chosen:
                f1,f2=c['pair'];d=(y-mod(F(f1),p))%p
                if f2 is not None:d=d*(y-mod(F(f2),p))%p
                num=int(chi[c['twist']%p])*int((chi[d]*A[c['equation']]).sum())
                c['validation_numerators'].append(num)
        if index%150==0:print('Exact counts through prime',p,'seconds',round(time.time()-start,1),flush=True)
    for c in chosen:
        v=np.array(c['validation_numerators'])/np.array(validate)
        c['validation_mean']=float(v.mean());c['validation_descriptive_se']=float(v.std(ddof=1)/len(v)**.5)
    result={'schema':'diophantine-evolution-v1','equations':EQS,'prime_limit_exclusive':5000,
        'discovery_primes':ds,'validation_primes':validate,'branch_pairs':len(pairs),'twists':cs,
        'hypotheses_per_surface':len(pairs)*len(cs),'base':base,'controls':controls,'spike':spike,
        'selected_candidates':chosen,'independent_direct_sum_checks':ntt_checks,
        'count_engine':'integer NTT mod 998244353; exact signed recovery bound |coefficient|<=p',
        'limits':'Finite prime diagnostics, not exact rank estimates. Selection is correlated; no significance or exclusion certificate.',
        'runtime_seconds':round(time.time()-start,2)}
    (HERE/'evolution.json').write_text(json.dumps(result,indent=2))
    print('Saved',len(primes),'primes;',len(validate),'held-out;',ntt_checks,'direct checks')
    for c in chosen:
        if c['equation']==3:print('Spike surface',c['pair'],c['twist'],c['discovery_mean'],c['validation_mean'])
if __name__=='__main__':main()
