# SCRIPT: UPG-GATE-02 (Module I, noncommutative torus anchor: winding integrality
#   and invariance; the admissible domain delta + g^2 <= 4; the amplitude floor
#   |w| <= (d/4) sqrt(delta))
#
#   R = U V U^dagger V^dagger,   lambda_i = eig(R)
#   w      = (1/2pi) sum_i arg(lambda_i)          [principal branch]
#   delta  = ||R - I||_F^2 / d
#   g      = min_i |lambda_i + 1|                 [branch guard]
#   second estimator: winding of  t -> det((1-t)I + tR)  on [0,1]

import numpy as np

TAU = 1e-3
rng = np.random.default_rng(20260820)


def clock_shift(d):
    w = np.exp(2j*np.pi/d)
    U = np.diag([w**k for k in range(d)])
    V = np.roll(np.eye(d, dtype=complex), 1, axis=0)
    return U, V


def commuting_pair(d):
    U = np.diag(np.exp(1j*rng.uniform(0, 2*np.pi, d)))
    V = np.diag(np.exp(1j*rng.uniform(0, 2*np.pi, d)))
    return U, V


def relator(U, V):
    return U @ V @ U.conj().T @ V.conj().T


def unitary_kick(U, eta):
    d = U.shape[0]
    H = rng.normal(size=(d, d)) + 1j*rng.normal(size=(d, d))
    H = (H + H.conj().T)/2
    H /= np.linalg.norm(H, 2)
    ev, W = np.linalg.eigh(H)
    return U @ (W @ np.diag(np.exp(1j*eta*ev)) @ W.conj().T)


def readout(R):
    d = R.shape[0]
    lam = np.linalg.eigvals(R)
    g = np.min(np.abs(lam + 1.0))
    delta = np.linalg.norm(R - np.eye(d), 'fro')**2 / d
    w = np.sum(np.angle(lam)) / (2*np.pi)
    return lam, g, delta, w


def winding_chord(R, nt=20001):
    lam = np.linalg.eigvals(R)
    t = np.linspace(0.0, 1.0, nt)[:, None]
    ang = np.unwrap(np.angle((1.0 - t) + t*lam[None, :]), axis=0)
    return np.sum(ang[-1] - ang[0]) / (2*np.pi)


def report(tag, R, expect=None):
    d = R.shape[0]
    lam, g, delta, w = readout(R)
    if g < TAU:
        print(f"{tag:<32s} REFUSED   g={g:.2e}   delta={delta:.6f}"
              f"   delta+g^2={delta+g*g:.9f}")
        return
    w2 = winding_chord(R)
    floor = d*np.sqrt(delta)/4
    ok = "" if expect is None else (
        "  PASS" if abs(w-expect) < 1e-9 and abs(w2-expect) < 1e-6 else "  FAIL")
    print(f"{tag:<32s} w={w:+.9f}  w_chord={w2:+.9f}  delta={delta:.6e}"
          f"  g={g:.6f}  delta+g^2={delta+g*g:.9f}  bound={floor:.4f}{ok}")


print("="*116)
print("G1  INTEGRALITY AND THE SCALAR EQUALITY CASE: clock and shift.")
print("    w = 1 at every d; delta + g^2 = 4 exactly; bound = (d/4)sqrt(delta) -> pi/2.")
print("="*116)
for d in [3, 5, 7, 11, 17, 31, 53, 97]:
    U, V = clock_shift(d)
    report(f"  d={d:<4d} exact", relator(U, V), expect=1.0)

print()
print("="*116)
print("G2  NEGATIVE CONTROL: commuting pair.  w = 0, delta = 0, g = 2.")
print("="*116)
for d in [7, 31, 97]:
    U, V = commuting_pair(d)
    report(f"  d={d:<4d} commuting", relator(U, V), expect=0.0)

print()
print("="*116)
print("G3  STABILITY AND THE STRICT INEQUALITY: kicked clock-shift, d=31.")
print("    w stays 1; the relator leaves the scalar locus so delta + g^2 < 4.")
print("="*116)
for eta in [1e-1, 1e-2, 1e-3, 1e-4]:
    U, V = clock_shift(31)
    report(f"  eta={eta:.0e}", relator(unitary_kick(U, eta),
                                       unitary_kick(V, eta)), expect=1.0)

print()
print("="*116)
print("G4  INVARIANCE: unitary conjugation and generator rephasing leave w fixed.")
print("="*116)
U, V = clock_shift(31)
report("  baseline", relator(U, V), expect=1.0)
X = rng.normal(size=(31, 31)) + 1j*rng.normal(size=(31, 31))
Q, _ = np.linalg.qr(X)
report("  conjugated", relator(Q @ U @ Q.conj().T, Q @ V @ Q.conj().T), expect=1.0)
report("  U -> e^{i th} U", relator(np.exp(0.7371j)*U, V), expect=1.0)
report("  both rephased", relator(np.exp(0.7371j)*U, np.exp(-2.11j)*V), expect=1.0)

print()
print("="*116)
print("G5  THE DOMAIN BOUND OVER RANDOM RELATORS: delta + g^2 <= 4, strict off")
print("    the scalar locus.  1000 random unitary pairs, d = 12.")
print("="*116)
worst = -1.0
viol = 0
for _ in range(1000):
    A = rng.normal(size=(12, 12)) + 1j*rng.normal(size=(12, 12))
    B = rng.normal(size=(12, 12)) + 1j*rng.normal(size=(12, 12))
    QA, _ = np.linalg.qr(A)
    QB, _ = np.linalg.qr(B)
    _, g, delta, _ = readout(relator(QA, QB))
    s = delta + g*g
    worst = max(worst, s)
    if s > 4 + 1e-9:
        viol += 1
print(f"  violations: {viol}/1000      max delta+g^2 = {worst:.9f}  (bound 4)")

print()
print("="*116)
print("G6  THE BOUNDARY: d=2 places an eigenvalue at -1.  The gate refuses.")
print("="*116)
U, V = clock_shift(2)
report("  d=2   clock-shift", relator(U, V))
U, V = clock_shift(4)
report("  d=4   clock-shift", relator(U, V), expect=1.0)
