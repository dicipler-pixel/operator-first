# SCRIPT: DIRAC-SPINE-01 (the graphene Dirac ladder on published parameters;
# the chiral-ensemble ledger)
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

print("=== B: graphene -- the measured Dirac spectrum through the framework ===")
Nl = 60
a = np.diag(np.sqrt(np.arange(1, Nl)), 1)
H = np.block([[np.zeros((Nl, Nl)), a], [a.T, np.zeros((Nl, Nl))]])
ev = np.sort(np.linalg.eigvalsh(H))
pos = ev[ev > 1e-12][:8]
print("  ladder E_n / E_1  vs  sqrt(n): " +
      "  ".join(f"{pos[n]/pos[0]:.6f}/{np.sqrt(n+1):.6f}" for n in range(4)))
nz = int(np.sum(np.abs(ev) < 1e-12))
print(f"  zero modes: {nz}")

th = np.linspace(0, 2*np.pi, 2001)
ph = 0.0
for i in range(len(th) - 1):
    k1, k2 = th[i], th[i+1]
    u1 = np.array([-np.exp(-1j*k1), 1])/np.sqrt(2)
    u2 = np.array([-np.exp(-1j*k2), 1])/np.sqrt(2)
    ph += np.angle(np.vdot(u1, u2))
print(f"  Berry phase around the Dirac point = {ph:.6f}   (pi = {np.pi:.6f})")

hbar, e = 1.0546e-34, 1.602e-19
vF, B = 1.10e6, 10.0
E1 = vF*np.sqrt(2*hbar*e*B)/e*1000
print(f"  with published v_F = 1.10e6 m/s: E_1(10 T) = {E1:.1f} meV")
print()

print("=== C: the chiral-ensemble ledger on the Dirac random-matrix class ===")
rng = np.random.default_rng(3)
M = 1200
X = (rng.normal(size=(M, M)) + 1j*rng.normal(size=(M, M)))/np.sqrt(2*M)
s = np.linalg.svd(X, compute_uv=False)
Z_sample = np.mean(0.5*np.log(1 + s**2))
rho = lambda t: np.sqrt(np.maximum(4 - t**2, 0))/np.pi
Z_MP, _ = quad(lambda t: rho(t)*0.5*np.log(1 + t**2), 0, 2)
print(f"  chGUE sample (M=1200): Z/M = {Z_sample:.6f}   MP integral: {Z_MP:.6f}")

target = np.pi**2/12
f = lambda aa: quad(lambda t: rho(t)*0.5*np.log(1 + (aa*t)**2), 0, 2)[0] - target
a_mp = brentq(f, 0.1, 10)
a_hc = np.exp(target) - 1
print(f"  pi^2/12 realized at a* = {a_mp:.6f} (chGUE/MP) and a* = {a_hc:.6f} (half-Cauchy)")
print(f"  check: ln(1+a_hc) = {np.log(1+a_hc):.10f}   vs   pi^2/12 = {target:.10f}")
