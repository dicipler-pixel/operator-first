# SCRIPT: BH-LEDGER-01 -- the Dunford trace-log ledger, computed on the audited operator
# at the coplanar wall's Jordan point. His tip made precise:
# rank-one (eigenvector) data DIVERGES ~ 1/gap approaching the Jordan point;
# contour (Dunford/Riesz) data stays EXACT, including AT the defective point.
# Audited shape block (four-body audit, FOURBODY-AUDIT scripts):
# A11 = (t1+t2) - (t1-t2)(w1-w2); A22 = 2 t3 + w3 (t1+t2-2t3)
# A12 = [ (t1-t2) - (t1+t2-2t3)(w1-w2) ] / sqrt(3); A21 = sqrt(3) (t1-t2) w3
# Shear block diagonal: t1+t2, t1+t3, t2+t3 (separated spectators).
# Jordan condition at w3=0: S = a (w1-w2), S = t1+t2-2t3, a = t1-t2.
import mpmath as mp
mp.mp.dps = 30
import numpy as np

t1,t2,t3 = 2.0, 1.0, 1.3 # a = 1, S = 0.4
dw = 0.4 # w1 - w2 = S/a -> Jordan at w3 = 0
lamstar = 2*t3 # = A11 = A22 at the Jordan point = 2.6

def block(eps):
    w1 = 0.7 - eps/2; w2 = 0.3 - eps/2; w3 = eps
    A11 = (t1+t2) - (t1-t2)*(w1-w2)
    A22 = 2*t3 + w3*(t1+t2-2*t3)
    A12 = ((t1-t2) - (t1+t2-2*t3)*(w1-w2))/np.sqrt(3)
    A21 = np.sqrt(3)*(t1-t2)*w3
    return np.array([[A11,A12],[A21,A22]])

def riesz(A, z0, r, npts=4000, f=None):
    # (1/2pii) contour-int f(lambda) (lambdaI - A)^{-1} dlambda over circle center z0 radius r
    n = A.shape[0]
    acc = np.zeros((n,n), dtype=complex)
    for k in range(npts):
        th = 2*np.pi*k/npts
        lam = z0 + r*np.exp(1j*th)
        R = np.linalg.inv(lam*np.eye(n) - A)
        w = (f(lam) if f else 1.0)
        acc += w * R * (1j*r*np.exp(1j*th)) * (2*np.pi/npts)
    return acc/(2j*np.pi)

print("=== approach along w3 -> 0+ : rank-one data vs contour data ===")
print(f"{'eps':>8} {'gap':>12} {'||P1|| rank-one':>16} {'Tr Pi (contour)':>18} {'||Pi_blk||':>12} {'ledger - 2 log(lam*)':>20}")
for eps in [1e-1,1e-2,1e-3,1e-4,1e-6,0.0]:
    A = block(eps)
    ev, V = np.linalg.eig(A)
    gap = abs(ev[0]-ev[1])
    if gap > 1e-14:
        Vi = np.linalg.inv(V)
        P1 = np.outer(V[:,0], Vi[0,:])
        p1n = np.linalg.norm(P1)
    else:
        p1n = float('inf')
    z0 = np.trace(A)/2
    Pi = riesz(A, z0, 0.15)
    led = riesz(A, z0, 0.15, f=lambda z: np.log(z))
    ledger = np.trace(led).real
    target = 2*np.log(np.trace(A).real/2)
    print(f"{eps:>8.0e} {gap:>12.3e} {p1n:>16.4e} {np.trace(Pi).real:>18.12f} {np.linalg.norm(Pi):>12.6f} {ledger-target:>20.3e}")

print("\n[GATE L1] rank-one projector norm diverges ~ 1/gap: compare ||P1||*gap:")
for eps in [1e-2,1e-3,1e-4]:
    A = block(eps); ev,V = np.linalg.eig(A)
    gap = abs(ev[0]-ev[1]); Vi = np.linalg.inv(V)
    P1 = np.outer(V[:,0],Vi[0,:])
    print(f" eps={eps:.0e}: ||P1||*gap = {np.linalg.norm(P1)*gap:.6f}")
A0 = block(0.0)
print(f"\n[GATE L2] AT the Jordan point (eps=0): A = {A0.tolist()}")
print(f" off-diagonal A12 = {A0[0,1]:.6f} (nonzero -> genuinely defective), A21 = {A0[1,0]:.1f}")
Pi0 = riesz(A0, lamstar, 0.15)
led0 = riesz(A0, lamstar, 0.15, f=lambda z: np.log(z))
print(f" Tr Pi (contour) = {np.trace(Pi0).real:.12f} (exact: 2)")
print(f" ||Pi_blk|| = {np.linalg.norm(Pi0):.6f} (bounded; = ||I2|| + nilpotent part)")
print(f" trace-log ledger = {np.trace(led0).real:.12f} vs 2 log(lam*) = {2*np.log(lamstar):.12f}")
print(f"[GATE L3] ledger exact at the defective point: {abs(np.trace(led0).real-2*np.log(lamstar)) < 1e-9}")
