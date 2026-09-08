# SCRIPT: UPG-PROVE-01a (metric-curvature bound, its saturation, persistence
# identity, rigidity divergence)
import numpy as np
rng = np.random.default_rng(11)

print("=== P1: bound |Omega| <= 2 sqrt(g11 g22 - g12^2), 1000 random trials ===")

def tangent(Pi, N):
    X = rng.normal(size=(N, N)) + 1j*rng.normal(size=(N, N))
    X = (X + X.conj().T)/2
    I = np.eye(N)
    return (I - Pi) @ X @ Pi + Pi @ X @ (I - Pi)

viol = 0
margins = []
for t in range(1000):
    N, k = 8, 3
    Q, _ = np.linalg.qr(rng.normal(size=(N, k)) + 1j*rng.normal(size=(N, k)))
    Pi = Q @ Q.conj().T
    V, W = tangent(Pi, N), tangent(Pi, N)
    g11 = 0.5*np.trace(V @ V).real
    g22 = 0.5*np.trace(W @ W).real
    g12 = 0.5*np.trace(V @ W).real
    Om = (-1j*np.trace(Pi @ (V @ W - W @ V))).real
    bound = 2*np.sqrt(max(g11*g22 - g12**2, 0))
    if abs(Om) > bound + 1e-9:
        viol += 1
    margins.append(bound - abs(Om))
print(f"  violations: {viol}/1000;  min margin = {min(margins):.3e}")
print()

print("=== P2: saturation for the two-band Dirac model (rank-1 on C^2) ===")

def bloch_pi(th, ph):
    n = np.array([np.sin(th)*np.cos(ph), np.sin(th)*np.sin(ph), np.cos(th)])
    sx = np.array([[0, 1], [1, 0]])
    sy = np.array([[0, -1j], [1j, 0]])
    sz = np.array([[1, 0], [0, -1]])
    return 0.5*(np.eye(2) + n[0]*sx + n[1]*sy + n[2]*sz)

th0, ph0, h = 1.1, 0.7, 1e-5
P0 = bloch_pi(th0, ph0)
V = (bloch_pi(th0 + h, ph0) - bloch_pi(th0 - h, ph0))/(2*h)
W = (bloch_pi(th0, ph0 + h) - bloch_pi(th0, ph0 - h))/(2*h)
g11 = 0.5*np.trace(V @ V).real
g22 = 0.5*np.trace(W @ W).real
g12 = 0.5*np.trace(V @ W).real
Om = (-1j*np.trace(P0 @ (V @ W - W @ V))).real
bd = 2*np.sqrt(g11*g22 - g12**2)
print(f"  |Omega| = {abs(Om):.8f}   bound = {bd:.8f}   ratio = {abs(Om)/bd:.8f}")
print()

print("=== P3: persistence identity C(dt) = Tr(Pi Pi') = sum cos^2 theta_i ===")
ok = True
for t in range(200):
    N, k = 8, 4
    Q1, _ = np.linalg.qr(rng.normal(size=(N, k)) + 1j*rng.normal(size=(N, k)))
    Q2, _ = np.linalg.qr(rng.normal(size=(N, k)) + 1j*rng.normal(size=(N, k)))
    P1, P2 = Q1 @ Q1.conj().T, Q2 @ Q2.conj().T
    s = np.linalg.svd(P1 @ P2, compute_uv=False)[:k]
    ok &= abs(np.trace(P1 @ P2).real - np.sum(s**2)) < 1e-9
print(f"  identity holds (200 trials): {ok}")
print()

print("=== P4: rigidity R = 1/(sigma_min^2 + eps) at a synthetic gap closing ===")
eps = 1e-12
for gap in [1.0, 0.1, 0.01, 0.001]:
    A = np.diag([1.0, gap]) @ np.array([[1, 0.3], [0, 1.0]])
    smin = np.linalg.svd(A, compute_uv=False).min()
    print(f"  gap={gap:6.3f}:  sigma_min = {smin:.4e}   R = {1/(smin**2+eps):.3e}")
