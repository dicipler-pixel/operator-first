"""Guarded arithmetic diagnostics. These are not physical spectral measurements.
Integer/rational certificates and finite-prime heuristics have separate outputs.
"""
from fractions import Fraction as F
from math import isqrt, log, sqrt
import sympy as sp

def blocked(reason): return {'_status':'blocked', 'reason':reason}
def ints(xs): return all(type(x) is int for x in xs)
def equation(a,b,c,x,y,z): return z*z+(y*y+a)*z+x*x*x+b*x+c

def integer_witness(inputs,*_):
    c=inputs['case']; abc=c['abc']; points=c['points']
    if not ints(abc) or any(not ints(p) or len(p)!=3 for p in points):
        return blocked('Exact integer coefficients and triples required; floats are not certificates.')
    residuals=[equation(*abc,*p) for p in points]
    bound=c.get('min_abs_x',0)
    return {'residuals':residuals,'all_satisfy':all(r==0 for r in residuals),
            'distinct_x':len(set(p[0] for p in points))==len(points),
            'all_above_bound':all(abs(p[0])>bound for p in points),
            'evidence':'exact integer substitution; finite witnesses do not prove infinitude'}

def discriminant(inputs,*_):
    c=inputs['case']; vals=c['abc']+[c['x'],c['y']]
    if not ints(vals): return blocked('Integer equation and coordinates required.')
    a,b,c0,x,y=vals; d=(y*y+a)**2-4*(x*x*x+b*x+c0)
    w=isqrt(d) if d>=0 else None; square=w is not None and w*w==d
    parity=square and (w-y*y-a)%2==0
    z=sorted(set([(-y*y-a+w)//2,(-y*y-a-w)//2])) if parity else []
    return {'discriminant':d,'square':square,'parity':parity,'z':z,
            'identity':'4F=(2z+y²+a)²-[(y²+a)²-4(x³+bx+c)]'}

def fibre_transfer(inputs,*_):
    c=inputs['case']; p=c['prime']; traces=c['traces']; r=F(c.get('radius','3/2'))
    if type(p) is not int or not sp.isprime(p) or p==2 or r.denominator%p==0 or r.numerator%p==0:
        return blocked('Odd prime with distinct, defined branch points required.')
    if len(traces)!=p or not ints(traces): return blocked('One exact integer character sum per affine base point required.')
    rr=r.numerator*pow(r.denominator,-1,p)%p
    chi=lambda x: 0 if x%p==0 else (1 if pow(x%p,(p-1)//2,p)==1 else -1)
    multiplicity=[0]*p; poles=0
    for u in range(p):
        den=(1+u*u)%p
        if den==0: poles+=1;continue
        y=rr*(1-u*u)*pow(den,-1,p)%p; multiplicity[y]+=1
    # Add the missing domain point u=infinity, mapping to y=-r.
    full=multiplicity.copy();full[-rr%p]+=1
    target=[1+chi(rr*rr-y*y) for y in range(p)]
    actual=sum(m*t for m,t in zip(multiplicity,traces))
    base=sum(traces);twist=sum(chi(rr*rr-y*y)*traces[y] for y in range(p))
    correction=traces[-rr%p]
    return {'multiplicities_match':full==target,'affine_cover_sum':actual,
            'base_sum':base,'twist_sum':twist,'omitted_domain_infinity_sum':correction,
            'identity_residual':actual-(base+twist-correction),'pole_count':poles,
            'evidence':'exact finite-field pushforward on the declared affine base; no rank inference'}

def prime_evolution(inputs,*_):
    c=inputs['case']; ps=c['primes']; nums=c['numerators']
    if len(ps)!=len(nums) or len(ps)<2 or not ints(ps+nums) or ps!=sorted(set(ps)) or any(not sp.isprime(p) for p in ps):
        return blocked('Ordered distinct primes and matching exact integer numerators required.')
    values=[n/p for n,p in zip(nums,ps)]; n=len(ps);mean=sum(values)/n
    se=sqrt(sum((v-mean)**2 for v in values)/(n-1)/n)
    return {'n':n,'prime_range':[ps[0],ps[-1]],'mean':mean,'descriptive_standard_error':se,
            'weighted_sum_over_cutoff':sum(v*log(p) for v,p in zip(values,ps))/ps[-1],
            'weighted_mean':sum(v*log(p) for v,p in zip(values,ps))/sum(map(log,ps)),
            'rank_proven':False,'evidence':'finite-prime diagnostic; standard error is descriptive, not a discovery p-value'}

def twist_selection(inputs,*_):
    c=inputs['case']; rows=c['values']; labels=c['labels']; cut=c['discovery_count']
    if len(rows)!=len(labels) or not rows or not 2<=cut<len(rows[0])-1 or any(len(r)!=len(rows[0]) for r in rows):
        return blocked('Matching candidate series with disjoint discovery and validation blocks required.')
    def stats(v):
        m=sum(v)/len(v);se=sqrt(sum((x-m)**2 for x in v)/(len(v)-1)/len(v));return {'mean':m,'descriptive_se':se}
    ranked=sorted(range(len(rows)),key=lambda i:(-sum(rows[i][:cut])/cut,labels[i]))
    winner=ranked[0]
    return {'selected_on_discovery':labels[winner], 'discovery':stats(rows[winner][:cut]),
            'validation':stats(rows[winner][cut:]),'candidates_tested':len(rows),
            'candidates':[{'label':labels[i],'discovery':stats(rows[i][:cut]),'validation':stats(rows[i][cut:])} for i in ranked],
            'rank_proven':False,'evidence':'candidate selected before validation; correlated candidates preclude naive Gaussian kill rule'}

def polynomial_identity(inputs,*_):
    c=inputs['case']; t=sp.Symbol('t'); abc=c['abc']
    # Coefficients are exact rational strings, ascending powers. No expression evaluation.
    polynomials=[sum(sp.Rational(str(v))*t**i for i,v in enumerate(cs)) for cs in c['coefficients']]
    if len(polynomials)!=3 or len(abc)!=3:return blocked('Three coordinate polynomials and three equation coefficients required.')
    residue=sp.Poly(sp.expand(equation(*abc,*polynomials)),t)
    return {'identically_zero':residue.is_zero,'residual':str(residue.as_expr()),
            'coordinate_degrees':[int(sp.degree(p,t)) if p!=0 else -1 for p in polynomials],
            'integer_coefficients':all(all(v.q==1 for v in sp.Poly(p,t).all_coeffs()) for p in polynomials),
            'evidence':'symbolic exact coefficient identity; infinitude also requires unbounded distinct integer outputs'}

def integral_cover(inputs,*_):
    c=inputs['case']; r=F(c['radius'])
    if r<=0:return blocked('Positive rational circle radius required.')
    lo=-int(r);hi=int(r);ys=[];candidates=[]
    for y in range(lo,hi+1):
        if r+y==0: candidates.append({'y':y,'u':'infinity'});ys.append(y);continue
        square=(r-y)/(r+y);sn=isqrt(square.numerator);sd=isqrt(square.denominator)
        good=sn*sn==square.numerator and sd*sd==square.denominator
        candidates.append({'y':y,'u_squared':str(square),'rational_u':good})
        if good:ys.append(y)
    return {'integer_y_candidates':candidates,'integer_y_reachable':ys,'real_y_interval':[str(-r),str(r)],
            'unbounded_integer_y':False,'evidence':'complete rational-square test for this circle cover; other coordinates still require checks'}

def pell_orbit(inputs,*_):
    c=inputs['case']; A=c['A'];x=c['x'];v=c['v'];r=c['unit_r'];s=c['unit_s'];steps=c.get('steps',3)
    if not ints([A,x,v,r,s,steps]) or A<=0 or isqrt(A)**2==A or steps<1 or steps>100:
        return blocked('Positive nonsquare integer A and a finite integer orbit request required.')
    if r*r-A*s*s!=1 or r<=1 or s<=0:return blocked('A positive norm-one Pell unit must be supplied and verified.')
    invariant=v*v-A*x*x;out=[]
    for k in range(steps):
        out.append({'step':k,'x':x,'v':v,'invariant':v*v-A*x*x})
        x,v=r*x+s*v,A*s*x+r*v
    return {'orbit':out,'invariant':invariant,'preserved':all(z['invariant']==invariant for z in out),
            'evidence':'exact Pell orbit only; target-surface map and denominator congruences must be certified separately'}
