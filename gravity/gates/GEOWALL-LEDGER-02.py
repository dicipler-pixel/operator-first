# SCRIPT: GEOWALL-LEDGER-02
# The decisive test: does the contour-level record degrade where the metric does?
#
# WHY THIS OPERATOR IS ALLOWED, stated first.  The ledger depends only on the
# geometry of the resolvent set: a rectifiable contour enclosing a cluster, with a
# gap.  It does not depend on definiteness, self-adjointness, or any pairing.  Its
# dependence is therefore strictly COARSER than the metric layer's, so the test may
# be run on ANY generator carrying a det g sign change.  It does not need a rotating
# horizon generator.  That is the whole reason this gate is cheap.
#
# WHAT IS MEASURED along a path in a two-parameter family L(t1,t2):
#   metric layer   g_ij = Re[ (1/2) Tr(d_i Pi  d_j Pi) ],  det g
#                  Omega = -i Tr( Pi [d_1 Pi, d_2 Pi] )      (curvature)
#                  persistence  C(D) = Re Tr[ Pi(t) Pi(t+D) ]   (cap is k = 2)
#   ledger layer   N = (1/2pi i) contour-int Tr R dl          (must stay 2)
#                  Z = (1/2pi i) contour-int log(l) Tr R dl   (vs sum of logs)
#
# PREDICTIONS, written before the run:
#   P1  Hermitian control: det g >= 0 everywhere, Re C <= 2, ledger exact.
#   P2  non-normal family: det g crosses zero and CHANGES SIGN.
#   P3  at that crossing N stays 2 and |Z - Z_direct| stays at its floor, with no
#       feature of any kind at the crossing.               <-- the decisive one
#   P4  the metric-curvature radicand goes negative while Omega stays finite and
#       nonzero: the licence expires with something real still to say.
#   P5  open question, allowed to fail: does Re C > 2 begin exactly where
#       det g < 0 begins?  The claim that the cap and the licence are one statement
#       in two registers predicts they coincide.

import numpy as np

np.set_printoptions(suppress=True)
rng = np.random.default_rng(20260820)

N_DIM = 6
NQ = 512                      # contour quadrature points
CEN, RAD = 2.5 + 0.0j, 1.2    # contour: encloses the cluster near 2 and 3
H = 1e-5                      # finite-difference step for dPi


def resolvent_trace(L, z):
    return np.trace(np.linalg.solve(z*np.eye(L.shape[0]) - L, np.eye(L.shape[0])))


def riesz(L):
    """Riesz projector for the cluster inside the contour, by trapezoid rule."""
    n = L.shape[0]
    P = np.zeros((n, n), dtype=complex)
    for j in range(NQ):
        th = 2*np.pi*j/NQ
        z = CEN + RAD*np.exp(1j*th)
        dz = 1j*RAD*np.exp(1j*th)*(2*np.pi/NQ)
        P += np.linalg.solve(z*np.eye(n) - L, np.eye(n))*dz
    return P/(2j*np.pi)


def ledger(L):
    """Contour count and contour trace-log."""
    n = L.shape[0]
    Nc = 0.0 + 0j
    Z = 0.0 + 0j
    for j in range(NQ):
        th = 2*np.pi*j/NQ
        z = CEN + RAD*np.exp(1j*th)
        dz = 1j*RAD*np.exp(1j*th)*(2*np.pi/NQ)
        tr = resolvent_trace(L, z)
        Nc += tr*dz
        Z += np.log(z)*tr*dz
    return Nc/(2j*np.pi), Z/(2j*np.pi)


def direct_ledger(L):
    ev = np.linalg.eigvals(L)
    inside = ev[np.abs(ev - CEN) < RAD]
    return len(inside), np.sum(np.log(inside)), ev


def geometry(fam, t, h=H):
    """Metric, curvature and det g at parameter point t = (t1,t2)."""
    P0 = riesz(fam(t[0], t[1]))
    dP = []
    for i in range(2):
        tp = list(t); tm = list(t)
        tp[i] += h; tm[i] -= h
        dP.append((riesz(fam(*tp)) - riesz(fam(*tm)))/(2*h))
    g = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            g[i, j] = np.real(0.5*np.trace(dP[i] @ dP[j]))
    Om = np.real(-1j*np.trace(P0 @ (dP[0] @ dP[1] - dP[1] @ dP[0])))
    return P0, g, np.linalg.det(g), Om


def persistence_excess(fam, t, deltas=(0.02, 0.05, 0.10)):
    """max over probe displacements of Re Tr[Pi(t) Pi(t+D)] - k."""
    P0 = riesz(fam(t[0], t[1]))
    best = -np.inf
    for D in deltas:
        for u in ((1, 0), (0, 1), (0.7071, 0.7071), (0.7071, -0.7071)):
            P1 = riesz(fam(t[0] + D*u[0], t[1] + D*u[1]))
            best = max(best, np.real(np.trace(P0 @ P1)) - 2.0)
    return best


# ----------------------------------------------------------------- the families
D0 = np.diag([2.0, 3.0, 20.0, -20.0, 35.0, -35.0]).astype(complex)

def cmat():
    return rng.normal(size=(N_DIM, N_DIM)) + 1j*rng.normal(size=(N_DIM, N_DIM))

A1 = cmat(); Bh1 = (A1 + A1.conj().T)/2
A2 = cmat(); Bh2 = (A2 + A2.conj().T)/2
Bn1 = cmat()
Bn2 = cmat()


def fam_herm(t1, t2):
    return D0 + t1*Bh1 + t2*Bh2


S1 = cmat(); S1 = (S1 - S1.conj().T)/2     # anti-Hermitian
S2 = cmat(); S2 = (S2 - S2.conj().T)/2


def make_family(kappa):
    """Two-parameter family whose non-Hermiticity dial is kappa.
    At kappa = 0 both tangent directions are Hermitian and the metric is a metric;
    increasing kappa tilts them until the pairing loses definiteness."""
    def fam(t1, t2):
        return D0 + t1*(Bh1 + kappa*S1) + t2*(Bh2 + kappa*S2)
    return fam


def row(fam, t, tag):
    P0, g, dg, Om = geometry(fam, t)
    Nc, Z = ledger(fam(t[0], t[1]))
    nin, Zd, ev = direct_ledger(fam(t[0], t[1]))
    gapin = np.min(np.abs(np.abs(ev - CEN) - RAD))
    idem = np.linalg.norm(P0 @ P0 - P0)
    exc = persistence_excess(fam, t) if abs(Nc - 2) < 1e-6 else float('nan')
    rad = 4*dg - Om**2
    ok = "OK " if abs(Nc-2) < 1e-6 else "BAD"
    print(f"  {tag:>9} [{ok}] det g={dg:+.6e}  Om={Om:+.5f}  4detg-Om^2={rad:+.4e}"
          f"  |N-2|={abs(Nc-2):.2e}  |Z-Zd|={abs(Z-Zd):.2e}"
          f"  gap={gapin:.3f}  |PP-P|={idem:.1e}  ReC-2={exc:+.3e}")
    return dg, exc


print("="*128)
print("P1  HERMITIAN CONTROL: det g >= 0, Re C <= 2, ledger exact")
print("="*128)
for s in [0.00, 0.05, 0.10, 0.15, 0.20]:
    row(fam_herm, (s, 0.6*s), f"s={s:.2f}")

print()
print("="*128)
print("P2  NON-NORMAL FAMILY: locate a sign change of det g on a straight path")
print("="*128)
ks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 2.0]
dvals = []
for k in ks:
    _, _, dg, _ = geometry(make_family(k), (0.0, 0.0))
    dvals.append(dg)
    print(f"  kappa = {k:4.2f}   det g = {dg:+.6e}")
cross = [i for i in range(len(ks)-1) if dvals[i]*dvals[i+1] < 0]
print(f"  sign changes between kappa = "
      f"{[(ks[i], ks[i+1]) for i in cross]}")

if not cross:
    print("  NO CROSSING on this path -- widen the scan before drawing any conclusion")
else:
    lo, hi = ks[cross[0]], ks[cross[0]+1]
    for _ in range(45):
        mid = 0.5*(lo+hi)
        _, _, dgm, _ = geometry(make_family(mid), (0.0, 0.0))
        if dgm*dvals[cross[0]] > 0:
            lo = mid
        else:
            hi = mid
    k_star = 0.5*(lo+hi)
    print(f"  wall located at kappa* = {k_star:.12f}")

    print()
    print("="*128)
    print("P3/P4/P5  CROSSING THE WALL: metric layer vs ledger layer, same operator")
    print("="*128)
    offs = [-2e-1, -5e-2, -1e-2, -1e-3, -1e-5, 0.0, +1e-5, +1e-3, +1e-2, +5e-2, +2e-1]
    excs = []
    dgs = []
    for o in offs:
        tag = f"k*{o:+.0e}" if o else "k*"
        dg, exc = row(make_family(k_star + o), (0.0, 0.0), tag)
        dgs.append(dg); excs.append(exc)

    print()
    print("  P5 verdict, the falsifiable one:")
    neg = [o for o, d in zip(offs, dgs) if d < 0]
    sup = [o for o, e in zip(offs, excs) if (e == e and e > 0)]
    print(f"    offsets with det g < 0 : {neg}")
    print(f"    offsets with Re C > 2  : {sup}")
    if set(neg) == set(sup):
        print("    the cap and the licence expire together -- one statement, two registers")
    else:
        print("    they do NOT coincide -- the cap and the licence are separate statements")