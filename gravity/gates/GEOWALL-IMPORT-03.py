#!/usr/bin/env python3
# SCRIPT: GEOWALL-IMPORT-03
# Two imports, measured here rather than cited.
# (A) The ledger at an EXACTLY defective point, and its single-valuedness around a loop
#     enclosing the coalescence.  This is the strongest form of the paper's claim: not a
#     near-degeneracy but a true Jordan block, where eigenvector arithmetic does not exist.
# (B) The pairing dependence of a non-normality verdict.  Theorem 7 says the transport
#     operator of the N=d+1 ladder is B-symmetric with B = diag(t/g).  A verdict of
#     "non-normal" is therefore a statement about a FORM: the same operator is grossly
#     asymmetric in the trace pairing and exactly symmetric in its own pairing.
import numpy as np

def riesz(M, c, r, eta=0.0, NQ=2048):
    th = 2*np.pi*np.arange(NQ)/NQ
    z = c + r*np.exp(1j*th); dz = 1j*r*np.exp(1j*th)*(2*np.pi/NQ)
    n = M.shape[0]; I = np.eye(n, dtype=complex)
    P = np.zeros((n, n), complex); N = 0j; Z = 0j
    for zi, dzi in zip(z, dz):
        R = np.linalg.solve(zi*I - M, I)
        P += R*dzi; tr = np.trace(R); N += tr*dzi; Z += np.log(zi+eta)*tr*dzi
    f = 1/(2j*np.pi); return P*f, (N*f).real, Z*f

print("="*78)
print("GEOWALL-IMPORT-03   (A) the ledger at an exact defect")
print("="*78)
lam = 2.5
J = np.array([[lam, 1.0, 0, 0],
              [0.0, lam, 0, 0],
              [0, 0, 7.0, 0],
              [0, 0, 0, 11.0]], complex)
w, V = np.linalg.eig(J[:2, :2])
print(f"  the 2x2 block is exactly defective: eigenvalues {np.round(w,12)},")
print(f"  eigenvector matrix condition number = {np.linalg.cond(V):.3e}  (diverges)")
print(f"\n  {'eta':>8} {'Tr Pi':>22} {'||Pi||':>12} {'Z':>22} {'2 log(lam+eta)':>18}")
for eta in [0.0, 1e-6, 1e-3, 1.0]:
    P, N, Z = riesz(J, lam, 1.2, eta)
    exact = 2*np.log(lam+eta)
    print(f"  {eta:>8.0e} {N:>22.12f} {np.linalg.norm(P,2):>12.6f} {Z.real:>22.12f} {exact:>18.12f}")
P, N, Z = riesz(J, lam, 1.2, 0.0)
print(f"\n  Tr Pi = {N:.12f} at every regularisation INCLUDING zero;  ||Pi|| = {np.linalg.norm(P,2):.6f}")
print(f"  |Z - 2 log lambda| = {abs(Z.real-2*np.log(lam)):.2e}   idempotency {np.linalg.norm(P@P-P):.2e}")

print("\n  single-valuedness: encircle the coalescence in a complexified parameter")
def Jt(t):
    d = 0.35*np.exp(1j*t)          # a loop around the branch point d = 0
    # eigenvalues lam +- sqrt(d): a genuine square-root exceptional point at d = 0
    A = np.array([[lam, 1.0],[d, lam]], complex)
    return np.block([[A, np.zeros((2,2))],
                     [np.zeros((2,2)), np.diag([7.0+0j, 11.0+0j])]])
Ns, Zs, evs = [], [], []
prev = None
for t in np.linspace(0, 2*np.pi, 961):
    P, N, Z = riesz(Jt(t), lam, 1.2, 1.0)
    e = np.linalg.eigvals(Jt(t)[:2, :2])
    if prev is not None:                       # continuous tracking, never sorted
        if abs(e[0]-prev[0]) + abs(e[1]-prev[1]) > abs(e[1]-prev[0]) + abs(e[0]-prev[1]):
            e = e[::-1]
    prev = e
    Ns.append(N); Zs.append(Z); evs.append(e.copy())
print(f"    count around the loop: {min(Ns):.12f} .. {max(Ns):.12f}")
print(f"    |Z(2pi) - Z(0)| = {abs(Zs[-1]-Zs[0]):.3e}   -> the ledger is single-valued")
print(f"    eigenvalues EXCHANGE: |ev(2pi)-ev(0)| = {np.max(np.abs(evs[-1]-evs[0])):.3e} "
      f"unswapped vs {np.max(np.abs(evs[-1]-evs[0][::-1])):.2e} swapped")

print()
print("="*78)
print("GEOWALL-IMPORT-03   (B) a non-normality verdict is a statement about a FORM")
print("="*78)
rng = np.random.default_rng(5)
print(f"  {'d':>3} {'||A - A^T||  (trace pairing)':>30} {'||A^T B - B A||  (own pairing)':>32}")
worst_t, worst_b = 0.0, 0.0
for d in [4, 6, 8, 12]:
    g = rng.uniform(0.3, 2.0, d); t = rng.uniform(0.3, 2.0, d)
    A = np.diag(t) - np.outer(g, t)
    B = np.diag(t/g)
    a1 = np.linalg.norm(A - A.T); a2 = np.linalg.norm(A.T@B - B@A)
    worst_t = max(worst_t, a1); worst_b = max(worst_b, a2)
    print(f"  {d:>3} {a1:>30.6f} {a2:>32.2e}")
print(f"\n  the same operator, two pairings: asymmetry {worst_t:.2f} against {worst_b:.1e}")
print(f"  a separation of {worst_t/max(worst_b,1e-300):.1e} -- and the spectrum is real in both")
print( "  readings.  'Non-normal' is not a property of the operator alone.")
print("="*78)