"""ACC eye: exact finite-image distance lower bound.

rho: x -> X=[[0,-1],[1,1]], y -> Y=XZ=[[-1,0],[1,-1]], reduced mod p.
The fourteen ordinary AC moves act on the image pair exactly as on words, because
rho is a homomorphism. A word path therefore projects to an image path of the SAME
length, so distance-to-goal in the finite pair graph is an exact LOWER BOUND on the
remaining ordinary moves. Take the maximum over primes, never the sum.

Telemetry only. This never prunes a search and never certifies anything.
Reproduces the audited state counts of REPORT_ACC section 5:
p=5 -> 14,396 ; p=7 -> 112,892 ; p=11 -> 1,742,396 ; total 1,869,684.
"""
from collections import deque
_CACHE={}

def _mul(A,B,p):
    return ((A[0]*B[0]+A[1]*B[2])%p,(A[0]*B[1]+A[1]*B[3])%p,
            (A[2]*B[0]+A[3]*B[2])%p,(A[2]*B[1]+A[3]*B[3])%p)

def _inv(A,p):
    a,b,c,d=A; det=(a*d-b*c)%p; di=pow(det,p-2,p)
    return ((d*di)%p,(-b*di)%p,(-c*di)%p,(a*di)%p)

def _letters(p):
    X=(0,-1%p,1,1); Z=(0,-1%p,1,0); Y=_mul(X,Z,p)
    return [X,_inv(X,p),Y,_inv(Y,p)],X,Y

_INVM=[0,1,3,2,5,4,7,6,9,8,11,10,13,12]

def _step(st,m,p,L):
    A,B=st
    if m==0: return (_inv(A,p),B)
    if m==1: return (A,_inv(B,p))
    if m==2: return (_mul(A,B,p),B)
    if m==3: return (_mul(A,_inv(B,p),p),B)
    if m==4: return (A,_mul(B,A,p))
    if m==5: return (A,_mul(B,_inv(A,p),p))
    if 6<=m<=9:
        g=L[m-6]; return (_mul(_mul(g,A,p),_inv(g,p),p),B)
    g=L[m-10]; return (A,_mul(_mul(g,B,p),_inv(g,p),p))

def _table(p):
    if p in _CACHE: return _CACHE[p]
    L,X,Y=_letters(p); goal=(X,Y)
    dist={goal:0}; q=deque([goal])
    while q:
        s=q.popleft(); d=dist[s]
        for m in range(14):
            t=_step(s,_INVM[m],p,L)
            if t not in dist: dist[t]=d+1; q.append(t)
    _CACHE[p]=(dist,L)
    return _CACHE[p]

def _rho(w,p,L):
    M=(1,0,0,1)
    for c in w: M=_mul(M,L[c],p)
    return M

def run(inputs,context,dependencies,spec,runtime):
    r0=inputs['relator_0']; r1=inputs['relator_1']
    primes=inputs.get('primes',[5,7,11])
    for w in (r0,r1):
        if not isinstance(w,list) or any(c not in (0,1,2,3) for c in w):
            raise ValueError('Relators must be lists of letters 0=x 1=x^-1 2=y 3=y^-1.')
    per={}; best=0; unreachable=[]
    for p in primes:
        dist,L=_table(p)
        st=(_rho(r0,p,L),_rho(r1,p,L))
        v=dist.get(st)
        per[str(p)]=v
        if v is None: unreachable.append(p)
        else: best=max(best,v)
    return {'lower_bound_moves':(None if unreachable else best),
            'per_prime':per,
            'image_unreachable':bool(unreachable),
            'unreachable_mod':unreachable,
            'states_enumerated':{str(p):len(_table(p)[0]) for p in primes},
            'admissible_for':'A* / IDA* as h; NOT a greedy rank (see REPORT_ACC s7)',
            'certifies':None}
