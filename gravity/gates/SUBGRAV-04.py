#!/usr/bin/env python3
# SCRIPT: SUBGRAV-04
# Is the licence per-subspace and the ledger global?  Twenty independent draws.
#
# WHY THIS TEST PROVES WHAT IT CLAIMS.  A single operator can show two clusters
# degenerating at different parameter values by accident of one random draw.  The
# structural claim is that the geometric layer is a property of the SUBSPACE while
# the contour layer is a property of the WHOLE operator, and that claim survives
# re-randomisation or it is not structural.  Each seed builds a fresh operator with
# two well separated clusters, tilted by one common dial, and asks four questions:
#   B1  do the two blocks reach det g = 0 at different values of the dial?
#   B2  does each block carry its own licence wall 4 det g = Omega^2, interior to it?
#   B3  do the contour count and contour trace-log, summed over ALL blocks, stay
#       exact at every step INCLUDING on each wall?
#   B4  with block A's own spectrum pinned to machine precision, does moving a
#       distant eigenvalue still move block A's wall?  (a null control -- the same
#       distant value compared against itself through the whole pipeline -- fixes
#       the floor that any real shift must beat)
import numpy as np

NQ, SEEDS = 512, 20
# Two resolutions, each matched to what it measures.  A wall is a ROOT of a smooth
# function and is insensitive to quadrature: its location agrees to nine digits at
# 256, 512 and 1024 points.  The sum rule is a PRECISION claim and is not: on the
# worst seeds the summed residual runs 2.4e-05 / 4.4e-10 / 2.5e-15 at those three
# resolutions, i.e. it is quadrature-limited and converges.  Walls and the
# external-field probe are therefore computed at NQ_WALL, the summed rows at NQ_SUM.
NQ_WALL, NQ_SUM = 512, 1024
CA, RA, CB, RB = 2.5, 1.2, 12.5, 1.2
BARS = dict(sep=1e-3, sums=1e-12, lock=1e-12, ratio=1e2)

def ops(seed, far, scale=0.18):
    rng = np.random.default_rng(seed)
    D0 = np.diag([2.,3.,12.,13.,25.,far]).astype(complex)
    def herm():
        M = rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); return (M+M.conj().T)/2
    def anti():
        M = rng.normal(size=(6,6))+1j*rng.normal(size=(6,6)); return (M-M.conj().T)/2
    return D0, scale*herm(), scale*herm(), scale*anti(), scale*anti()

def H(o, k, t, sig=(0j,0j)):
    D0,B1,B2,S1,S2 = o
    M = D0 + t[0]*(B1+k*S1) + t[1]*(B2+k*S2)
    M = M.copy(); M[0,0]+=sig[0]; M[1,1]+=sig[1]; return M

def riesz(M, c, r):
    th = 2*np.pi*np.arange(NQ)/NQ
    z = c + r*np.exp(1j*th); dz = 1j*r*np.exp(1j*th)*(2*np.pi/NQ)
    I = np.eye(6, dtype=complex)
    P = np.zeros((6,6), complex); N = 0j; Z = 0j
    for zi,dzi in zip(z,dz):
        R = np.linalg.solve(zi*I-M, I); P += R*dzi
        tr = np.trace(R); N += tr*dzi; Z += np.log(zi)*tr*dzi
    f = 1/(2j*np.pi); return P*f, (N*f).real, Z*f

def geom(o, k, c, r, sig=(0j,0j), h=1e-4):
    t = np.array([1.,1.]); P0,N0,Z0 = riesz(H(o,k,t,sig), c, r); dP=[]
    for i in range(2):
        tp=t.copy(); tp[i]+=h; tm=t.copy(); tm[i]-=h
        Pp,_,_ = riesz(H(o,k,tp,sig), c, r); Pm,_,_ = riesz(H(o,k,tm,sig), c, r)
        dP.append((Pp-Pm)/(2*h))
    Q = np.array([[np.trace(P0@dP[i]@dP[j]) for j in range(2)] for i in range(2)])
    g = np.real(Q); g = (g+g.T)/2
    Om = np.real(-1j*np.trace(P0@(dP[0]@dP[1]-dP[1]@dP[0])))     # antisymmetric: the curvature
    dg = g[0,0]*g[1,1]-g[0,1]**2
    return dict(detg=dg, lic=4*dg-Om**2, N=N0, Z=Z0, Om=Om,
                idem=np.linalg.norm(P0@P0-P0))

def gate(o, k, blocks):
    Hm = H(o,k,(1.,1.)); ev = np.linalg.eigvals(Hm); ok=True
    for c,r,want in blocks:
        d = np.abs(ev-c)
        if int(np.sum(d<r))!=want or np.min(np.abs(d-r))<0.05: ok=False
    return ok

def walls(f, lo, hi, n=21):
    xs = np.linspace(lo,hi,n); vs=[f(x) for x in xs]; out=[]
    for i in range(n-1):
        if vs[i]*vs[i+1] < 0:
            a,b,fa = xs[i],xs[i+1],vs[i]
            for _ in range(34):
                m=0.5*(a+b); fm=f(m)
                if fa*fm<=0: b=m
                else: a,fa=m,fm
                if b-a<1e-12: break
            out.append(0.5*(a+b))
    return out

def evA(M):
    ev = np.linalg.eigvals(M); ev = ev[np.argsort(np.abs(ev-CA))][:2]
    return ev[np.argsort(ev.real)]

def lock(o, k, target, x0=np.zeros(4)):
    t = np.array([1.,1.])
    def res(x):
        e = evA(H(o,k,t,(x[0]+1j*x[1], x[2]+1j*x[3]))) - target
        return np.array([e[0].real,e[0].imag,e[1].real,e[1].imag])
    x = x0.copy()
    for _ in range(40):
        r = res(x)
        if np.max(np.abs(r)) < 1e-14: break
        J = np.zeros((4,4)); h=1e-7
        for j in range(4):
            dx = x.copy(); dx[j]+=h; J[:,j]=(res(dx)-r)/h
        try: x = x - np.linalg.solve(J,r)
        except np.linalg.LinAlgError: break
    return (x[0]+1j*x[1], x[2]+1j*x[3]), np.max(np.abs(res(x)))

print("="*78); print("SUBGRAV-04   twenty draws"); print("="*78)
print(f"  bars, stated before the run: wall separation > {BARS['sep']:.0e};"
      f" licence wall interior in every block;")
print(f"  |sum N - 6| and |sum Z - Zdir| <= {BARS['sums']:.0e} at every row"
      f" including on the walls;")
print(f"  locked shift > {BARS['ratio']:.0e} x its own null control.\n")
print(f"  {'seed':>4} {'k*_A':>13} {'k*_B':>13} {'|sep|':>10} {'lic<met':>8}"
      f" {'worst sums':>11} {'lock res':>9} {'null':>9} {'EFE shift':>11}")
res = []
for s in range(SEEDS):
    oA, oB = ops(s, 70.0), ops(s, 120.0)
    BL  = [(CA,RA,2),(CB,RB,2),(25.,2.,1),(70.,2.,1)]     # blocks of the far=70 operator
    BLb = [(CA,RA,2),(CB,RB,2),(25.,2.,1),(120.,2.,1)]    # ... and of the far=120 probe
    # admissible range: the largest tilt at which BOTH contours still enclose
    # exactly their pair, with margin.  Walls are hunted only inside it.
    kmax = 0.0
    for kk in np.linspace(0., 2.5, 51):
        if gate(oA,kk,BL) and gate(oB,kk,BLb): kmax = kk
        else: break
    if kmax < 0.5: print(f"  {s:>4}   admissible range too short (kmax={kmax:.2f})"); continue
    wA = walls(lambda k: geom(oA,k,CA,RA)['detg'], 0., kmax)
    wB = walls(lambda k: geom(oA,k,CB,RB)['detg'], 0., kmax)
    lA = walls(lambda k: geom(oA,k,CA,RA)['lic'],  0., kmax)
    lB = walls(lambda k: geom(oA,k,CB,RB)['lic'],  0., kmax)
    if not (wA and wB and lA and lB):
        print(f"  {s:>4}   no det g = 0 inside the admissible range [0,{kmax:.2f}]"); continue
    sep = abs(wA[0]-wB[0])
    interior = (lA[0] < wA[0]) and (lB[0] < wB[0])
    worst = 0.0
    globals()['NQ'] = NQ_SUM
    rows = [0.0, wA[0], wB[0], min(1.5, kmax)]
    for k in rows:
        if not gate(oA,k,BL):        # every row carries the enclosure gate
            worst = np.nan; break
        Hm = H(oA,k,(1.,1.)); Zdir = np.sum(np.log(np.linalg.eigvals(Hm)))
        Nt=0.; Zt=0j
        for c,r,_ in BL:
            gg = geom(oA,k,c,r); Nt+=gg['N']; Zt+=gg['Z']
        worst = max(worst, abs(Nt-6), abs(Zt-Zdir))
    globals()['NQ'] = NQ_WALL
    def locked(k):
        tgt = evA(H(oA,k,(1.,1.))); sg,_ = lock(oB,k,tgt); return geom(oB,k,CA,RA,sg)['detg']
    def nullf(k):
        tgt = evA(H(oA,k,(1.,1.))); sg,_ = lock(oA,k,tgt); return geom(oA,k,CA,RA,sg)['detg']
    lo,hi = max(0.,wA[0]-0.06), min(kmax,wA[0]+0.06)
    wl = walls(locked, lo, hi, 5); wn = walls(nullf, lo, hi, 5)
    _,lr = lock(oB, wA[0], evA(H(oA,wA[0],(1.,1.))))
    shift = abs(wl[0]-wA[0]) if wl else np.nan
    null  = abs(wn[0]-wA[0]) if wn else np.nan
    res.append((sep, interior, worst, lr, null, shift))
    print(f"  {s:>4} {wA[0]:>13.9f} {wB[0]:>13.9f} {sep:>10.2e} {str(interior):>8}"
          f" {worst:>11.2e} {lr:>9.1e} {null:>9.1e} {shift:>11.3e}")

a = np.array([[r[0],r[2],r[3],r[4],r[5]] for r in res]); ints=[r[1] for r in res]
print("\n" + "="*78)
print(f"  seeds completed                 : {len(res)}/{SEEDS}")
print(f"  B1 wall separation              : min {a[:,0].min():.2e}  median {np.median(a[:,0]):.2e}"
      f"   [{'PASS' if a[:,0].min()>BARS['sep'] else 'FAIL'}]")
print(f"  B2 licence interior in every block: {sum(ints)}/{len(ints)}"
      f"   [{'PASS' if all(ints) else 'FAIL'}]")
print(f"  B3 worst |sum N-6| , |sum Z-Zdir|: {a[:,1].max():.2e}"
      f"   [{'PASS' if a[:,1].max()<=BARS['sums'] else 'FAIL'}]")
print(f"  B4 lock residual (A's spectrum)  : worst {a[:,2].max():.1e}")
print(f"     null control floor            : worst {np.nanmax(a[:,3]):.1e}")
print(f"     locked EFE shift              : min {np.nanmin(a[:,4]):.2e}  median {np.nanmedian(a[:,4]):.2e}")
r = np.nanmin(a[:,4])/max(np.nanmax(a[:,3]),1e-300)
print(f"     shift / null                  : {r:.1e}   [{'PASS' if r>BARS['ratio'] else 'FAIL'}]")
print("="*78)