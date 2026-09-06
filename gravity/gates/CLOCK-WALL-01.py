#!/usr/bin/env python3
# SCRIPT: CLOCK-WALL-01
#
# WHY THIS GATE PROVES WHAT IT CLAIMS
#
# Sec. 9 states that along the softest direction of the metric the line-element cost
# ds/dlambda falls to zero at det g = 0 and becomes imaginary beyond it, and quotes a
# ladder of values together with a square-root exponent. Those are [V] claims and must
# be produced by a gate on the family they are attributed to. This script builds the
# SAME six-dimensional family used in Appendix C -- same seed, same draw order, same
# diagonal, same contour, same finite-difference step -- locates its wall by bisection,
# and measures the line element along the softest eigenvector of g on both sides.
#
# It also fits the exponent: ds/dlambda ~ |kappa - kappa*|^p, with p = 1/2 predicted for
# a simple (crossing) zero of the soft eigenvalue.
#
# KILL CONDITION, STATED IN ADVANCE: if ds/dlambda stays bounded away from zero along the
# softest direction as det g -> 0, or if the fitted exponent is not near 1/2 on a family
# whose determinant demonstrably changes sign, the claim is wrong.
#
# CONTROL: the same quantity along a FIXED coordinate direction, which must show no
# feature at the wall -- otherwise the effect is a coordinate artefact rather than one
# direction losing its clock.

import numpy as np

NQ = 512
CEN, RAD = 2.5 + 0.0j, 1.2
H = 1e-5

rng = np.random.default_rng(20260820)
N_DIM = 6
D0 = np.diag([2.0, 3.0, 20.0, -20.0, 35.0, -35.0]).astype(complex)

def cmat():
    return rng.normal(size=(N_DIM, N_DIM)) + 1j*rng.normal(size=(N_DIM, N_DIM))

# draw order identical to Appendix C
A1 = cmat(); Bh1 = (A1 + A1.conj().T)/2
A2 = cmat(); Bh2 = (A2 + A2.conj().T)/2
Bn1 = cmat()
Bn2 = cmat()
S1 = cmat(); S1 = (S1 - S1.conj().T)/2
S2 = cmat(); S2 = (S2 - S2.conj().T)/2

def make_family(kappa):
    def fam(t1, t2):
        return D0 + t1*(Bh1 + kappa*S1) + t2*(Bh2 + kappa*S2)
    return fam

def riesz(L):
    n = L.shape[0]
    P = np.zeros((n, n), dtype=complex)
    for j in range(NQ):
        th = 2*np.pi*j/NQ
        z = CEN + RAD*np.exp(1j*th)
        dz = 1j*RAD*np.exp(1j*th)*(2*np.pi/NQ)
        P += np.linalg.solve(z*np.eye(n) - L, np.eye(n))*dz
    return P/(2j*np.pi)

def metric(fam, t=(0.0, 0.0), h=H):
    dP = []
    for i in range(2):
        tp = list(t); tm = list(t)
        tp[i] += h; tm[i] -= h
        dP.append((riesz(fam(*tp)) - riesz(fam(*tm)))/(2*h))
    g = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            g[i, j] = np.real(0.5*np.trace(dP[i] @ dP[j]))
    return (g + g.T)/2

def detg(k):
    return np.linalg.det(metric(make_family(k)))

print("="*78)
print("CLOCK-WALL-01   the transport clock on the Sec. 7 family")
print("="*78)

lo, hi = 0.6, 0.8
flo = detg(lo)
for _ in range(45):
    mid = 0.5*(lo + hi)
    fm = detg(mid)
    if fm*flo > 0: lo, flo = mid, fm
    else: hi = mid
kw = 0.5*(lo + hi)
print(f"  wall located at kappa* = {kw:.12f}   det g there = {detg(kw):+.3e}\n")

print("  line element ds/dlambda along the SOFTEST direction, across the wall")
print(f"  {'kappa - k*':>12} {'det g':>13} {'g(soft,soft)':>15} {'ds/dlambda':>14}")
for d in [-2e-1, -1e-1, -3e-2, -1e-2, -1e-3, 0.0, 1e-3, 1e-2, 3e-2]:
    g = metric(make_family(kw + d))
    w, V = np.linalg.eigh(g)
    s = V[:, 0]
    val = float(s @ g @ s)
    txt = f"{np.sqrt(val):.4e}" if val >= 0 else f"{np.sqrt(-val):.3e}i"
    print(f"  {d:>+12.4f} {np.linalg.det(g):>13.3e} {val:>15.3e} {txt:>14}")

print("\n  the same along a FIXED coordinate direction (control: no feature expected)")
fix = np.array([1.0, 0.0])
print(f"  {'kappa - k*':>12} {'g(fix,fix)':>15} {'ds/dlambda':>14}")
for d in [-1e-1, -1e-2, 0.0, 1e-2, 1e-1]:
    g = metric(make_family(kw + d))
    val = float(fix @ g @ fix)
    print(f"  {d:>+12.4f} {val:>15.3e} {np.sqrt(abs(val)):>14.4e}")

dd = [3e-1, 1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4]
ds = []
for d in dd:
    g = metric(make_family(kw - d))
    w, V = np.linalg.eigh(g)
    s = V[:, 0]
    ds.append(np.sqrt(max(float(s @ g @ s), 0.0)))
p = np.polyfit(np.log(dd), np.log(ds), 1)[0]
print("\n  approach to the wall from the definite side")
print(f"  {'|k-k*|':>10} {'ds/dlambda':>14} {'ds/sqrt|k-k*|':>16}")
for d, v in zip(dd, ds):
    print(f"  {d:>10.0e} {v:>14.4e} {v/np.sqrt(d):>16.5f}")
print(f"\n  fitted exponent  ds/dlambda ~ |kappa-kappa*|^{p:.4f}"
      f"   [{'PASS' if abs(p-0.5) < 0.05 else 'FAIL'}]  (square-root law predicted)")
print("="*78)