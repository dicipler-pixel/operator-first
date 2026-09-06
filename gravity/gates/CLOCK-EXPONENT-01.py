#!/usr/bin/env python3
# SCRIPT: CLOCK-EXPONENT-01
# The Bures arc length along the softest direction of the quantum metric vanishes at the
# metric's null set with an exponent fixed by ONE property: whether the metric is positive
# semi-definite.  Hermitian => semi-definite => the null set can only be TOUCHED => the soft
# eigenvalue has a double zero => arc length exponent 1.  The converse is CONDITIONAL, not
# automatic: non-Hermiticity permits an indefinite form but does not force one -- an open
# operating point that stays definite is exhibited in Appendix I -- and WHERE a crossing
# does occur the zero is simple and the exponent is 1/2.
# There is no free parameter and nothing between the two values.
import numpy as np
from scipy.optimize import brentq, minimize_scalar

sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)

def H(k, m=1.0, gam=0.0):
    kx,ky = k
    return np.sin(kx)*sx + np.sin(ky)*sy + (m+np.cos(kx)+np.cos(ky)+1j*gam)*sz

def proj(k, m, gam):
    A=H(k,m,gam); w,R=np.linalg.eig(A); i=int(np.argmax(w.real))
    wl,L=np.linalg.eig(A.conj().T); j=int(np.argmin(np.abs(wl.conj()-w[i])))
    r=R[:,i]; l=L[:,j]
    return np.outer(r,l.conj())/(l.conj()@r)

def gmet(k, m=1.0, gam=0.0, h=1e-5):
    P0=proj(k,m,gam); dP=[]
    for i in range(2):
        e=np.zeros(2); e[i]=h
        dP.append((proj(k+e,m,gam)-proj(k-e,m,gam))/(2*h))
    Q=np.array([[np.trace(P0@dP[a]@dP[b]) for b in range(2)] for a in range(2)])
    G=np.real(Q); return (G+G.T)/2

def scan(gam, N=90, m=1.0):
    v=[]
    for a in np.linspace(-np.pi,np.pi,N):
        for b in np.linspace(-np.pi,np.pi,N):
            try:
                d=np.linalg.det(gmet((a,b),m,gam))
                if np.isfinite(d): v.append(d)
            except Exception: pass
    return np.array(v)

def exponents(k0, u, gam, m=1.0, dd=(3e-2,1e-2,3e-3,1e-3)):
    f=lambda t: np.linalg.det(gmet(k0+t*u,m,gam))
    ts=np.linspace(-0.6,0.6,61); vv=[f(t) for t in ts]; root=None
    for i in range(len(ts)-1):
        if vv[i]*vv[i+1]<0: root=brentq(f,ts[i],ts[i+1],xtol=1e-13); break
    if root is None:                       # no crossing: find the tangency instead
        r=minimize_scalar(lambda t: abs(f(t)), bounds=(-1.5,1.5), method='bounded',
                          options={'xatol':1e-12}); root=r.x
    lam=[]; ds=[]
    for d in dd:
        w=np.linalg.eigvalsh(gmet(k0+(root-d)*u,m,gam))
        lam.append(abs(w[0])); ds.append(np.sqrt(abs(w[0])))
    return (np.polyfit(np.log(dd),np.log(lam),1)[0],
            np.polyfit(np.log(dd),np.log(ds),1)[0], root)

if __name__ == "__main__":
    print("="*74); print("CLOCK-EXPONENT-01"); print("="*74)
    print(f"  {'gamma':>7} {'min det g':>13} {'max det g':>13} {'crosses':>9}")
    for gam in [0.0,0.1,0.3,0.6,1.0]:
        v=scan(gam)
        print(f"  {gam:>7.2f} {v.min():>13.3e} {v.max():>13.3e} "
              f"{str(bool(v.min()<0<v.max())):>9}")
    print("\n  exponents transverse to the null set")
    print(f"  {'case':>26} {'soft eigenvalue':>17} {'arc length':>12} {'class':>11}")
    u=np.array([1.0,1.0])/np.sqrt(2)
    pl,ps,_=exponents(np.array([1.2,-1.2]),u,0.0)
    print(f"  {'Hermitian (touching)':>26} {pl:>17.4f} {ps:>12.4f} {'2, 1':>11}")
    u2=np.array([1.0,0.4]); u2=u2/np.linalg.norm(u2)
    pl2,ps2,_=exponents(np.array([-2.042,-0.785]),u2,0.6)
    print(f"  {'non-Hermitian (crossing)':>26} {pl2:>17.4f} {ps2:>12.4f} {'1, 1/2':>11}")
    print("\n  1   is the extremal Reissner-Nordstrom lapse  (1 - rs/r)")
    print("  1/2 is the Schwarzschild lapse               sqrt(1 - rs/r)")
    print("="*74)