#!/usr/bin/env python3
# SCRIPT: GEOWALL-ROT-01
#
# WHY THIS GATE PROVES WHAT IT CLAIMS
#
# The reciprocity theorem says a generator complex-symmetric under a bilinear pairing,
# probed by operators symmetric under the same pairing, has M proportional to N: the
# round-trip form is a perfect square, so the gauge-invariant rank measure W vanishes
# and det g = -(Im conj(u) v)^2 <= 0 degenerates to zero whenever the probe amplitudes
# are phase-aligned.  On the spherically symmetric Poschl-Teller generator that is what
# is measured: W at the instrument floor, |det g| at 1e-16.
#
# The obstruction is therefore a statement about a SYMMETRY, not about openness, and it
# predicts its own removal.  Rotation supplies a mixed time-angle term in the wave
# equation; in this first-order hyperboloidal system the minimal deformation with that
# structure is a first-order advection added to the damping block,
#
#       L2  ->  L2 + a * D ,
#
# an odd-order derivative, which reverses sign under transpose and so cannot be
# symmetric under the pairing that makes the undeformed operator symmetric.  The
# parameter a plays the role of the rotation parameter.  This is a toy carrying the
# structure of frame dragging, not a Kerr calculation, and is used only to test whether
# the obstruction lifts when the symmetry is broken in that way.
#
# PREDICTIONS, STATED BEFORE THE RUN (from the companion paper's open problem 1):
#   P1  W departs from the instrument floor as the rotation is turned on, and does so
#       in proportion to a: a log-log slope of 1.00 +- 0.15 over the small-a decades.
#   P2  |det g| becomes nonzero, rising far above the 1e-16 it holds at a = 0.
#   P3  det g takes BOTH SIGNS somewhere in the (V0, a) plane, so the vanishing set is
#       a curve in two parameters -- the codimension-one geometric wall -- rather than
#       an identically-zero function.
#   P4  the instrument is unchanged: biorthonormality residual stays below 1e-6, and
#       at a = 0 every number reproduces GEOWALL-RECIP-01.
# Any of these can fail.  If W stays at the floor for all a, the obstruction is not
# about this symmetry and the paper's reading of it is wrong.

import numpy as np

def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.ones(N + 1); c[0] = 2.; c[-1] = 2.; c *= (-1.) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    D = np.outer(c, 1. / c) / ((X - X.T) + np.eye(N + 1))
    D -= np.diag(D.sum(axis=1))
    return D, x

def generator(N, V0, s, a=0.0):
    D, x = cheb(N); I = np.eye(N + 1); Z = 0 * I
    L1 = np.diag(1 - x**2) @ D @ D - 2 * np.diag(x) @ D - V0 * I
    L2 = -2 * np.diag(x) @ D - I + a * D          # <-- the rotation term
    return 1j * np.block([[Z, I], [L1, s * L2]]), x

def potential_probe(x, centre, width):
    n = len(x); Z = np.zeros((n, n)); dV = np.exp(-((x - centre) / width) ** 2)
    return 1j * np.block([[Z, Z], [-np.diag(dV), Z]])

def pair_form(N, V0, s, probes, a=0.0, seed=None):
    L, x = generator(N, V0, s, a)
    ev, R = np.linalg.eig(L)
    evL, Lw = np.linalg.eig(L.conj().T)
    root = np.sqrt(complex(V0 - 0.25))
    t0, t1 = (root - 0.5j, root - 1.5j) if seed is None else seed
    i0 = int(np.argmin(np.abs(ev - t0))); i1 = int(np.argmin(np.abs(ev - t1)))
    if i0 == i1: return None
    ladder = abs(ev[i0] - t0) + abs(ev[i1] - t1)
    j0 = int(np.argmin(np.abs(evL.conj() - ev[i0])))
    j1 = int(np.argmin(np.abs(evL.conj() - ev[i1])))
    R0, R1 = R[:, i0], R[:, i1]
    L0, L1v = Lw[:, j0].copy(), Lw[:, j1].copy()
    L0 /= np.vdot(L0, R0).conjugate(); L1v /= np.vdot(L1v, R1).conjugate()
    bio = max(abs(np.vdot(L0, R0) - 1), abs(np.vdot(L1v, R1) - 1),
              abs(np.vdot(L0, R1)), abs(np.vdot(L1v, R0)))
    gap2 = (ev[i0] - ev[i1]) ** 2
    Va, Vb = probes
    Ma = np.vdot(L0, Va @ R1); Mb = np.vdot(L0, Vb @ R1)
    Na = np.vdot(L1v, Va @ R0); Nb = np.vdot(L1v, Vb @ R0)
    W = abs(Ma*Nb - Mb*Na) / (np.hypot(abs(Ma),abs(Mb)) * np.hypot(abs(Na),abs(Nb)))
    A = Ma*Na/gap2; C = Mb*Nb/gap2; B = 0.5*(Ma*Nb + Mb*Na)/gap2
    u, v = Ma/(ev[i0]-ev[i1]), Mb/(ev[i0]-ev[i1])
    return dict(w=(ev[i0], ev[i1]), ladder=ladder, bio=bio, W=W,
                detg=A.real*C.real - B.real**2, align=(np.conj(u)*v).imag)

N = 96
print("=" * 78)
print("GEOWALL-ROT-01   does broken reciprocity lift the obstruction?")
print("=" * 78)
_, xg = generator(N, 1.0, 1.0)
probes = (potential_probe(xg, -0.5, 0.3), potential_probe(xg, +0.5, 0.3))

r0 = pair_form(N, 1.0, 1.0, probes, a=0.0)
print(f"\nP4  a = 0 reproduces the spherically symmetric gate")
print(f"    ladder residual {r0['ladder']:.2e}   biorthonormality {r0['bio']:.2e}")
print(f"    W = {r0['W']:.3e}    |det g| = {abs(r0['detg']):.3e}")

print(f"\nP1/P2  rotation scan at V0 = 1.00, s = 1.00")
print(f"    {'a':>10} {'W':>13} {'|det g|':>13} {'det g sign':>11} {'bio':>10}")
aa = [0.0, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1, 2e-1]
Ws = []; Ds = []; seed = (r0['w'][0], r0['w'][1])
for a in aa:
    r = pair_form(N, 1.0, 1.0, probes, a=a, seed=seed)
    seed = r['w']
    Ws.append(r['W']); Ds.append(r['detg'])
    print(f"    {a:>10.1e} {r['W']:>13.3e} {abs(r['detg']):>13.3e}"
          f" {'+' if r['detg']>0 else '-':>11} {r['bio']:>10.1e}")

sel = [(a, w) for a, w in zip(aa, Ws) if 0 < a <= 1e-2]
la = np.log(np.array([p[0] for p in sel])); lw = np.log(np.array([p[1] for p in sel]))
slope = np.polyfit(la, lw, 1)[0]
print(f"\n    log-log slope of W vs a over the small-a decades : {slope:.3f}"
      f"   [{'PASS' if abs(slope-1) < 0.15 else 'FAIL'}]  (P1 predicted 1.00 +- 0.15)")
print(f"    W lift from a=0 to a=0.1                         : "
      f"{Ws[aa.index(1e-1)]/max(Ws[0],1e-300):.2e} x")
print(f"    |det g| lift from a=0 to a=0.1                   : "
      f"{abs(Ds[aa.index(1e-1)])/max(abs(Ds[0]),1e-300):.2e} x   "
      f"[{'PASS' if abs(Ds[aa.index(1e-1)]) > 1e4*abs(Ds[0]) else 'FAIL'}]  (P2)")

print(f"\nP3  sign of det g over the (V0, a) plane")
V0s = [0.30, 0.60, 1.00, 1.60, 2.40]
print(f"    {'V0 \\ a':>8}" + "".join(f"{a:>11.0e}" for a in [1e-2, 3e-2, 1e-1, 2e-1]))
signs = set()
for V0 in V0s:
    row = f"    {V0:>8.2f}"
    seed = None
    base = pair_form(N, V0, 1.0, probes, a=0.0)
    seed = base['w']
    for a in [1e-2, 3e-2, 1e-1, 2e-1]:
        r = pair_form(N, V0, 1.0, probes, a=a, seed=seed)
        seed = r['w']
        sg = '+' if r['detg'] > 0 else '-'
        signs.add(sg); row += f"{sg:>11}"
    print(row)
print(f"\n    signs present: {sorted(signs)}   "
      f"[{'PASS' if len(signs) == 2 else 'FAIL'}]  (P3: a sign change means the"
      f" vanishing set is a curve)")
print("=" * 78)