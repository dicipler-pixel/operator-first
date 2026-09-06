# SCRIPT: NULLITY-CHECK-01  (probe for the review's divergence objection)
import numpy as np
from scipy.optimize import brentq, minimize_scalar
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)
def H(k,m=1.0,gam=0.0):
    kx,ky=k; return np.sin(kx)*sx+np.sin(ky)*sy+(m+np.cos(kx)+np.cos(ky)+1j*gam)*sz
def spec(k,m,gam):
    w=np.linalg.eigvals(H(k,m,gam)); return abs(w[0]-w[1])
def proj(k,m,gam):
    A=H(k,m,gam); w,R=np.linalg.eig(A); i=int(np.argmax(w.real))
    wl,L=np.linalg.eig(A.conj().T); j=int(np.argmin(np.abs(wl.conj()-w[i])))
    r=R[:,i]; l=L[:,j]; return np.outer(r,l.conj())/(l.conj()@r)
def gmet(k,m=1.0,gam=0.0,h=1e-5):
    P0=proj(k,m,gam); dP=[]
    for i in range(2):
        e=np.zeros(2); e[i]=h
        dP.append((proj(k+e,m,gam)-proj(k-e,m,gam))/(2*h))
    Q=np.array([[np.trace(P0@dP[a]@dP[b]) for b in range(2)] for a in range(2)])
    G=np.real(Q); return (G+G.T)/2
def root_of(k0,u,gam,m=1.0):
    f=lambda t: np.linalg.det(gmet(k0+t*u,m,gam))
    ts=np.linspace(-0.6,0.6,61); vv=[f(t) for t in ts]
    for i in range(len(ts)-1):
        if vv[i]*vv[i+1]<0: return brentq(f,ts[i],ts[i+1],xtol=1e-13)
    r=minimize_scalar(lambda t: abs(f(t)),bounds=(-1.5,1.5),method='bounded',options={'xatol':1e-12})
    return r.x
print("="*88)
print("NULLITY-CHECK-01   does the SOFT eigenvalue vanish, or is the metric diverging?")
print("="*88)
cases=[("Hermitian  (touching) gamma=0.0",np.array([1.2,-1.2]),np.array([1.,1.])/np.sqrt(2),0.0),
       ("non-Herm. (crossing) gamma=0.6",np.array([-2.042,-0.785]),np.array([1.,0.4])/np.linalg.norm([1.,0.4]),0.6)]
for name,k0,u,gam in cases:
    t0=root_of(k0,u,gam)
    print(f"\n {name}   null point at t = {t0:+.9f}")
    print(f"   {'|t-t0|':>9} {'soft eig':>13} {'hard eig':>13} {'tr g':>13} {'ratio h/s':>11} {'spectral gap':>13}")
    for d in (3e-2,1e-2,3e-3,1e-3,3e-4):
        w=np.linalg.eigvalsh(gmet(k0+(t0-d)*u,1.0,gam))
        s,h_=abs(w[0]),abs(w[1])
        print(f"   {d:>9.0e} {s:>13.4e} {h_:>13.4e} {s+h_:>13.4e} {h_/s:>11.2e} {spec(k0+(t0-d)*u,1.0,gam):>13.4f}")
print("\n"+"="*88)