# SCRIPT: DIO-NAGAO-01
# Nagao / Rosen-Silverman rank detector for the nine Epoch "small Diophantine" surfaces.
# Each equation z^2 + (y^2+a) z + P(x) = 0 with P(x) = x^3 + b x + c becomes, for fixed y,
#     w^2 = (y^2+a)^2 - 4 P(x)  =: f_y(x)      (elliptic curve in (x,w), point at infinity)
# an elliptic surface over the y-line.  Rosen-Silverman: rank E(Q(y)) = lim avg over p of -A_p,
#     -A_p = (1/p) sum_y sum_x chi_p(f_y(x))            (chi_p = Legendre symbol)
# CALIBRATION, same primes, same code path:
#   rank-0 control: w^2 = x^3 + (y^2 + 1)   (generic twist family, expected ~0)
#   rank-1 control: w^2 = x^3 + x + 1 - y^3 - y  (visible section (x,w) = (y, 1), reads ~+1 in the
#                   Naskrecki work: +1.083 +- 0.121)
# Primes 401..1499.  j = 0 fibres (b = 0) have a_p = 0 at p = 2 mod 3, so those primes carry no
# rank information for the b = 0 equations; they are reported separately.
import numpy as np
from sympy import primerange
EQS = {  # name: (a, b, c)   for z^2 + (y^2+a)z + x^3 + b x + c = 0
 'H22  z2+y2z+x3-2':      (0, 0,-2),
 'H23  z2+y2z+x3-x-1':    (0,-1,-1),
 'H23  z2+y2z+x3+x-1':    (0, 1,-1),
 'H23  z2+y2z+x3+x+1':    (0, 1, 1),
 'H23  z2+y2z+x3-3':      (0, 0,-3),
 'H23  z2+y2z+x3+3':      (0, 0, 3),
 'H24  z2+y2z+x3-x-2':    (0,-1,-2),
 'H24  z2+y2z+x3-x+2':    (0,-1, 2),
 'H24  z2+y2z-z+x3+2':    (-1,0, 2),
}
def legendre_table(p):
    chi=np.full(p,-1,dtype=np.int8); chi[0]=0
    r=(np.arange(p,dtype=np.int64)**2)%p; chi[r]=1; chi[0]=0
    return chi
def score(p,chi,fy):
    x=np.arange(p,dtype=np.int64); y=np.arange(p,dtype=np.int64)
    F=fy(x[None,:],y[:,None],p)
    return chi[F].sum()/p
def surf(a,b,c):
    return lambda x,y,p: (((y*y+a)%p)**2 - 4*(x*x*x + b*x + c))%p
ctrl0=lambda x,y,p: (x*x*x + y*y + 1)%p
ctrl1=lambda x,y,p: (x*x*x + x + 1 - y*y*y - y)%p
primes=list(primerange(401,1500))
print('primes',len(primes),'range',primes[0],'..',primes[-1])
def report(name,fy,split3=False):
    vals=np.array([score(p,legendre_table(p),fy) for p in primes])
    if split3:
        m1=np.array([p%3==1 for p in primes]); v=vals[m1]
        print(f'  {name:26s} all p: {vals.mean():+.3f} +- {vals.std()/np.sqrt(len(vals)):.3f}   p=1 mod 3 only: {v.mean():+.3f} +- {v.std()/np.sqrt(len(v)):.3f}   (p=2 mod 3 mean {vals[~m1].mean():+.3f})')
    else:
        print(f'  {name:26s} {vals.mean():+.3f} +- {vals.std()/np.sqrt(len(vals)):.3f}')
print('controls')
report('rank-0 control',ctrl0,split3=True)
report('rank-1 control',ctrl1)
print('the nine surfaces  (score ~ rank E(Q(y)))')
for name,(a,b,c) in EQS.items():
    report(name,surf(a,b,c),split3=(b==0))
