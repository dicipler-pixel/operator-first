# SCRIPT: DIO-VERIFY-01
# Independent confirmation of the DIO-TWIST-01 spike:  surface z^2+y^2 z+x^3+x+1=0,
# i.e.  w^2 = y^4 - 4(x^3+x+1),  branch points y = -3/2, +3/2, twist class c = -1.
#
# WHY THIS PROVES WHAT IT CLAIMS.  DIO-TWIST-01 read the cover's rank through the identity
# N_phi(p) = N(p) + chi_c(p) T1(p); a bug there would show up as an isolated spike exactly
# like this one.  Here the cover is built EXPLICITLY and its rank measured from scratch with
# the same detector that read +1.000 on the rank-1 control:
#     the degree-2 cover branched at +-3/2 with twist c is the conic  s^2 = c(y^2 - 9/4).
#     At c = -1 this is s^2 = 9/4 - y^2, which HAS rational points, so the cover is a rational
#     curve and can be parametrised:  y = (3/2)(1-u^2)/(1+u^2).
#     Pull the surface back and measure  rank ~ mean_p (1/p) sum_u sum_x chi(f_{y(u)}(x)).
# CONTROLS, decided before the run:
#   (a) the same cover on the eight other surfaces  -- is c=-1, +-3/2 special to THIS equation?
#   (b) other rational covers of the same surface: branch +-1/2, +-1, +-2, +-5/2 at c=-1
#   (c) the flat cover y = u (degree 1) -- must return the base rank 0 already measured
# KILL: if the direct measurement does not reproduce a score near +1, the spike was an artefact.
import numpy as np
from sympy import primerange
EQS={'H22 x3-2':(0,0,-2),'H23 x3-x-1':(0,-1,-1),'H23 x3+x-1':(0,1,-1),'H23 x3+x+1':(0,1,1),
     'H23 x3-3':(0,0,-3),'H23 x3+3':(0,0,3),'H24 x3-x-2':(0,-1,-2),'H24 x3-x+2':(0,-1,2),'H24 -z x3+2':(-1,0,2)}
primes=list(primerange(401,1500))
def leg(p):
    chi=np.full(p,-1,dtype=np.int8); r=(np.arange(p,dtype=np.int64)**2)%p; chi[r]=1; chi[0]=0; return chi
CHI={p:leg(p) for p in primes}
def rank_on_cover(a,b,c0,h=None):
    """h = None: base (y=u).  h = Fraction r: cover y = r(1-u^2)/(1+u^2), branch +-r, c=-1."""
    vals=[]
    for p in primes:
        chi=CHI[p]; x=np.arange(p,dtype=np.int64); u=np.arange(p,dtype=np.int64)
        if h is None: y=u.copy(); ok=np.ones(p,bool)
        else:
            den=(1+u*u)%p; ok=den!=0
            num=(h[0]*pow(h[1],-1,p))%p
            y=np.zeros(p,dtype=np.int64)
            y[ok]=(num*((1-u[ok]*u[ok])%p)*np.array([pow(int(d),-1,p) for d in den[ok]]))%p
        F=(((y[:,None]*y[:,None]+a)%p)**2 - 4*(x[None,:]**3+b*x[None,:]+c0))%p
        s=chi[F].sum(axis=1)
        vals.append(s[ok].sum()/p)
    v=np.array(vals); return v.mean(), v.std()/np.sqrt(len(v))
print('DIO-VERIFY-01   direct measurement of the cover, no twist identity')
print('primes',primes[0],'..',primes[-1],'(',len(primes),')\n')
a,b,c0=EQS['H23 x3+x+1']
m,e=rank_on_cover(a,b,c0,None); print(f'  control (c): base y=u, x3+x+1                 {m:+.3f} +- {e:.3f}   (must be ~0)')
m,e=rank_on_cover(a,b,c0,(3,2)); print(f'  THE SPIKE  : cover branch +-3/2, c=-1        {m:+.3f} +- {e:.3f}')
print('\n  control (b): other rational covers of the same surface')
for num,den in ((1,2),(1,1),(2,1),(5,2),(3,1),(7,2)):
    m,e=rank_on_cover(a,b,c0,(num,den)); print(f'      branch +-{num}/{den:<2d} c=-1                     {m:+.3f} +- {e:.3f}')
print('\n  control (a): the same cover (+-3/2, c=-1) on the other eight surfaces')
for name,(A,B,C) in EQS.items():
    if name=='H23 x3+x+1': continue
    m,e=rank_on_cover(A,B,C,(3,2)); print(f'      {name:14s}                       {m:+.3f} +- {e:.3f}')
