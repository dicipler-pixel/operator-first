"""ACC eye: small-prime component obstruction.

Idea taken from jackyreaps/X-files: a residual-flux parity that "cannot flip
spontaneously" is a controlled topological charge, a global selection rule
(README: Hol = +-1, mu_n = integral tr(M) ds mod 2).

Applied here: reduce rho mod a small prime. |SL(2,2)|=6 so the pair graph has 36
nodes; mod 3 it has 576. The fourteen AC moves act on it, and its CONNECTED
COMPONENTS are an UNCONDITIONAL invariant -- no cap, no engine, no budget. If a
start pair sits outside the component of (X,Y), no AC path to the trivial
presentation exists at all.

Motivating check: the legal two-move control [2,4] sends trace t -> t^2-2, which
destroys the trace; but t^2-2 = t (mod 2), so trace parity survives a move the
trace does not. That is what suggested looking below p=5.

Measured: 9 of 36 pairs lie outside the goal component mod 2; 64 of 576 mod 3.
Measured on the pool: ZERO of the 10,115 competition rows land outside either.
The obstruction is real and vacuous here -- every row normally generates, so its
image generates. Recorded so the class of 'find a small obstruction' approaches
is closed rather than retried.

Telemetry only; certifies nothing.
"""
from collections import deque
_C={}
def _mul(A,B,p):
    return ((A[0]*B[0]+A[1]*B[2])%p,(A[0]*B[1]+A[1]*B[3])%p,
            (A[2]*B[0]+A[3]*B[2])%p,(A[2]*B[1]+A[3]*B[3])%p)
def _inv(A,p):
    a,b,c,d=A; det=(a*d-b*c)%p; di=pow(det,p-2,p)
    return ((d*di)%p,(-b*di)%p,(-c*di)%p,(a*di)%p)
def _letters(p):
    X=(0,-1%p,1,1); Z=(0,-1%p,1,0); Y=_mul(X,Z,p)
    return [X,_inv(X,p),Y,_inv(Y,p)],X,Y
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
def _goal_component(p):
    if p in _C: return _C[p]
    L,X,Y=_letters(p); goal=(X,Y)
    comp={goal}; q=deque([goal])
    while q:
        s=q.popleft()
        for m in range(14):
            t=_step(s,m,p,L)
            if t not in comp: comp.add(t); q.append(t)
    _C[p]=(comp,L); return _C[p]
def _rho(w,p,L):
    M=(1,0,0,1)
    for c in w: M=_mul(M,L[c],p)
    return M
def run(inputs,context,dependencies,spec,runtime):
    r0=inputs['relator_0']; r1=inputs['relator_1']
    primes=inputs.get('primes',[2,3])
    per={}; blocked=[]
    for p in primes:
        comp,L=_goal_component(p)
        st=(_rho(r0,p,L),_rho(r1,p,L))
        ok=st in comp
        per[str(p)]={'in_goal_component':ok,'goal_component_size':len(comp)}
        if not ok: blocked.append(p)
    return {'per_prime':per,
            'unconditionally_unsolvable':bool(blocked),
            'blocked_mod':blocked,
            'scope':'unconditional: no cap, engine or budget qualifier',
            'pool_result':'zero of 10,115 rows land outside; real but vacuous here',
            'certifies':None}
