#!/usr/bin/env python3
# SCRIPT: BIAXIAL-01
# If the unequal-mass shape sphere is the BIAXIAL case of a two-sheet index surface,
# it must carry exactly TWO isolated optic axes (conical intersections), where the
# equal-mass (uniaxial) case has its degeneracy forced by symmetry at the poles.
import numpy as np
exec(open('/home/claude/unequal_check.py').read().split('print("="*78); print("UNEQUAL-CHECK-01')[0])

def scan(mass, na=340, np_=680):
    pts=[]
    A = np.linspace(0.02, 0.998, na); P = np.linspace(0, 2*np.pi, np_, endpoint=False)
    Gm = np.zeros((na, np_))
    for i,a in enumerate(A):
        for j,p in enumerate(P):
            Gm[i,j] = gap(mass, a, p)[0]
    # local minima of the gap on the grid (torus in psi, interval in a)
    for i in range(1, na-1):
        for j in range(np_):
            v = Gm[i,j]
            nb = [Gm[i-1,j],Gm[i+1,j],Gm[i,(j-1)%np_],Gm[i,(j+1)%np_],
                  Gm[i-1,(j-1)%np_],Gm[i-1,(j+1)%np_],Gm[i+1,(j-1)%np_],Gm[i+1,(j+1)%np_]]
            if v < min(nb) and v < 0.05:
                pts.append((v, A[i], P[j]))
    return pts

def refine(mass, a, p):
    from scipy.optimize import minimize
    r = minimize(lambda x: gap(mass, np.clip(x[0],1e-3,0.999), x[1])[0], [a,p],
                 method='Nelder-Mead', options=dict(xatol=1e-13, fatol=1e-15, maxiter=6000))
    g,s = gap(mass, np.clip(r.x[0],1e-3,0.999), r.x[1])
    return g, r.x[0], r.x[1], s

print("="*78); print("BIAXIAL-01   counting the optic axes"); print("="*78)
for mass, tag in [(np.array([1.,1.,1.]), "EQUAL masses  (uniaxial?)"),
                  (np.array([1.,2.,3.]), "m = (1,2,3)   (biaxial?)"),
                  (np.array([1.,1.,2.5]), "m = (1,1,2.5) (one symmetry left)")]:
    pts = scan(mass)
    # cluster
    keep=[]
    for v,a,p in sorted(pts):
        if all(min(abs(p-q)%(2*np.pi), 2*np.pi-abs(p-q)%(2*np.pi)) > 0.15 or abs(a-b) > 0.05
               for _,b,q in keep):
            keep.append((v,a,p))
    print(f"\n  {tag}:  {len(keep)} distinct near-degeneracies on the grid")
    for v,a,p in keep[:6]:
        g,aa,pp,s = refine(mass, a, p)
        print(f"     a={aa:.8f}  psi={pp:.8f}   gap={g:.2e}   svals={np.array2string(s,precision=6)}")
print("="*78)
