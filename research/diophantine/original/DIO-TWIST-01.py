# SCRIPT: DIO-TWIST-01
# Degree-2 base-change sweep for the nine Epoch small-Diophantine surfaces.
# Surface over the y-line: w^2 = f_y(x) = (y^2+a)^2 - 4(x^3 + b x + c0).   Base rank 0 (DIO-NAGAO-01).
# Cover y = phi(t) of degree 2 with branch points f1, f2 (f2 may be infinity) and twist class c:
#     #phi^{-1}(u) = 1 + chi(c (u-f1)(u-f2))    so   N_phi(p) = N(p) + chi_c(p) T1(p),
#     T1(p) = sum_u chi((u-f1)(u-f2)) A_u(p),   A_u(p) = sum_x chi(f_u(x)).
# rank(cover) = 0 + rank(twist),  rank(twist, c) ~ mean_p chi_c(p) T1(p) / p.
# Shioda-Tate: sum over c of rank(twist,c) <= 2 for branch points off the singular fibres.
# KILL: no (pair, c) with score above the noise ceiling  =>  no positive-rank degree-2 cover of
# height <= HMAX for that surface.
import numpy as np, itertools, time
from fractions import Fraction
from sympy import primerange, factorint
EQS = {'H22 x3-2':(0,0,-2),'H23 x3-x-1':(0,-1,-1),'H23 x3+x-1':(0,1,-1),'H23 x3+x+1':(0,1,1),
       'H23 x3-3':(0,0,-3),'H23 x3+3':(0,0,3),'H24 x3-x-2':(0,-1,-2),'H24 x3-x+2':(0,-1,2),'H24 -z x3+2':(-1,0,2)}
HMAX=5
primes=list(primerange(401,1500))
def leg(p):
    chi=np.full(p,-1,dtype=np.int8); r=(np.arange(p,dtype=np.int64)**2)%p; chi[r]=1; chi[0]=0; return chi
CHI={p:leg(p) for p in primes}
# branch points: rationals of height <= HMAX, up to the y -> -y symmetry take f1 >= 0 ... keep all, cheap
rats=sorted({Fraction(n,d) for d in range(1,HMAX+1) for n in range(-HMAX,HMAX+1) if abs(n)<=HMAX and d<=HMAX})
pairs=[(f1,f2) for f1,f2 in itertools.combinations(rats,2)]+[(f1,None) for f1 in rats]
def modp(fr,p): return (fr.numerator*pow(fr.denominator,-1,p))%p
cs=[c for c in range(-60,61) if c not in (0,) and all(e<2 for e in factorint(abs(c)).values())]
def chic(c,p):
    return int(CHI[p][c%p]) if c%p!=0 else 0
CHIC=np.array([[chic(c,p) for p in primes] for c in cs],dtype=float)   # cs x primes
print('surfaces',len(EQS),'branch pairs',len(pairs),'twist classes',len(cs),'primes',len(primes),flush=True)
t0=time.time()
for name,(a,b,c0) in EQS.items():
    T1=np.zeros((len(pairs),len(primes)))
    for j,p in enumerate(primes):
        chi=CHI[p]; x=np.arange(p,dtype=np.int64); y=np.arange(p,dtype=np.int64)
        F=(((y[:,None]*y[:,None]+a)%p)**2 - 4*(x[None,:]**3 + b*x[None,:] + c0))%p
        A=chi[F].sum(axis=1).astype(float)          # A_u for u = y mod p
        u=np.arange(p,dtype=np.int64)
        for i,(f1,f2) in enumerate(pairs):
            m1=modp(f1,p)
            if f2 is None: d=(u-m1)%p
            else: d=((u-m1)*(u-modp(f2,p)))%p
            T1[i,j]=(chi[d]*A).sum()/p
    S=T1@CHIC.T/len(primes)             # pairs x cs : mean over primes of chi_c T1/p
    sd=T1.std(axis=1)/np.sqrt(len(primes))
    Z=S/np.maximum(sd[:,None],1e-9)
    k=np.unravel_index(np.argmax(S),S.shape)
    exp_noise=np.sqrt(2*np.log(S.size))          # expected max |z| over S.size gaussians
    print(f'{name:12s} best score {S[k]:+.3f} +- {sd[k[0]]:.3f} (z={Z[k]:+.2f}) at branch {pairs[k[0]][0]},{pairs[k[0]][1]} c={cs[k[1]]}   '
          f'max|z| {np.abs(Z).max():.2f} vs noise ceiling ~{exp_noise:.2f}   {round(time.time()-t0)}s',flush=True)
    top=np.argsort(-S.ravel())[:3]
    for tix in top:
        i,jj=np.unravel_index(tix,S.shape); print(f'     {S[i,jj]:+.3f}  branch {pairs[i][0]},{pairs[i][1]}  c={cs[jj]}')
