# SCRIPT: BH-DYNAMO-01  (Parker alpha-Omega dynamo operator: oscillatory onset, hair ladder, EP birth of the wave, ledger through the EP, Parker-Yoshimura control)
import numpy as np
from scipy.linalg import expm, eig, eigvals
N = 120; L = np.pi
x = np.linspace(0, L, N+2)[1:-1]; h = x[1]-x[0]
D2 = (np.diag(np.ones(N-1),1) + np.diag(np.ones(N-1),-1) - 2*np.eye(N))/h**2
D1 = (np.diag(np.ones(N-1),1) - np.diag(np.ones(N-1),-1))/(2*h)
alpha_prof = np.cos(x)

def Lop(a0, G=1.0):
    return np.block([[D2, a0*np.diag(alpha_prof)],[G*D1, D2]])

print("=== PD1: onset scan (max Re s vs alpha0; oscillatory?) ===")
a_grid = np.linspace(0.5, 12, 24)
prev = None; a_c = None
for a0 in a_grid:
    w = eigvals(Lop(a0))
    i = np.argmax(w.real)
    if prev is not None and prev < 0 <= w.real[i]:
        a_c = a0
    prev = w.real[i]
if a_c is None: a_c = a_grid[-1]
# refine by bisection
lo, hi = a_c-0.5, a_c
for _ in range(40):
    mid = (lo+hi)/2
    if eigvals(Lop(mid)).real.max() < 0: lo = mid
    else: hi = mid
a_c = hi
w = eigvals(Lop(a_c)); i = np.argmax(w.real)
print(f"  alpha0_c = {a_c:.4f}  (D_c = a0*G*L^3 = {a_c*np.pi**3:.1f});  leading s = {w[i]:.4f}  -> Im = {w[i].imag:.4f} ({'OSCILLATORY onset' if abs(w[i].imag)>1e-6 else 'steady onset'})")
period = 2*np.pi/abs(w[i].imag)

print()
print("=== PD2: the hair ladder at 0.9*alpha0_c (all modes damped) ===")
a0 = 0.9*a_c
Ld = Lop(a0)
w = eigvals(Ld); iw = np.argmax(w.real)
slow = w.real[iw]; cyc = 2*np.pi/abs(w[iw].imag) if abs(w[iw].imag)>1e-9 else np.inf
omega_num = np.linalg.eigvalsh((Ld+Ld.T)/2).max()
Gm, tp = 0.0, 0.0
for t in [0.02,0.05,0.1,0.2,0.35,0.6,1.0,1.6,2.5,4.0]:
    g = np.linalg.norm(expm(Ld*t),2)**2
    if g > Gm: Gm, tp = g, t
Phi = np.linalg.norm(Ld@Ld.T - Ld.T@Ld,'fro')
print(f"  SLOW  (modal):   max Re s = {slow:+.4f}, cycle period = {cyc:.2f}")
print(f"  FAST  (transient): G_max = {Gm:.1f} at t = {tp}  (t_peak/period = {tp/cyc:.3f})")
print(f"  HYPER (num. abscissa): omega(L) = {omega_num:+.2f}  ({'positive: instantaneous growth in damped operator' if omega_num>0 else 'negative'})")
print(f"  Phi-stress ||[L,L^T]||_F = {Phi:.1f}")

print()
print("=== PD3: EP hunt -- birth of the wave (real pair -> complex pair) ===")
def top_im(a0):
    w = eigvals(Lop(a0))
    idx = np.argsort(-w.real)[:4]
    return max(abs(w[idx].imag))
lo, hi = 0.05, a_c
assert top_im(lo) < 1e-9 and top_im(hi) > 1e-6
for _ in range(45):
    mid = (lo+hi)/2
    if top_im(mid) < 1e-9: lo = mid
    else: hi = mid
a_ep = (lo+hi)/2
print(f"  EP located: alpha0* = {a_ep:.6f}  (= {a_ep/a_c:.3f} alpha0_c)")
def kappa_pair(a0):
    Lm = Lop(a0)
    w, vl, vr = eig(Lm, left=True, right=True)
    idx = np.argsort(-w.real)[:2]
    ks = []
    for j in idx:
        num = np.linalg.norm(vl[:,j])*np.linalg.norm(vr[:,j])
        den = abs(vl[:,j].conj() @ vr[:,j])
        ks.append(num/den)
    return max(ks), w[idx]
print(f"  {'delta':>9} {'kappa':>12} {'kappa*sqrt(delta)':>18}")
for d in [0.2, 0.05, 0.0125, 0.003125]:
    kap,_ = kappa_pair(a_ep - d)
    print(f"  {d:9.5f} {kap:12.1f} {kap*np.sqrt(d):18.3f}")

print()
print("=== PD4: shifted Dunford ledger through the EP ===")
c = 40.0
for tag, a0 in [("at EP", a_ep), ("near EP", a_ep-0.003)]:
    Lm = Lop(a0)
    w = eigvals(Lm); idx = np.argsort(-w.real)[:2]
    pair = w[idx]
    ctr = pair.real.mean()
    others = np.delete(w, idx)
    r = 0.5*min(abs(others - ctr))
    r = max(r, 2*abs(pair[0]-pair[1]))
    M = 600; th = np.linspace(0, 2*np.pi, M, endpoint=False)
    S = 0.0+0j
    for t in th:
        z = ctr + r*np.exp(1j*t)
        S += np.log(c+z)*np.trace(np.linalg.inv(z*np.eye(2*N)-Lm))*(1j*r*np.exp(1j*t))
    S *= (2*np.pi/M)/(2j*np.pi)
    direct = np.sum(np.log(c+pair))
    print(f"  {tag}: ledger = {S.real:.10f}  direct sum log(c+pair) = {direct.real:.10f}  diff = {abs(S-direct):.2e}")

print()
print("=== PD5: Parker-Yoshimura control (phase-migration flips with sign of G) ===")
for G in [+1.0, -1.0]:
    Lm = Lop(1.05*a_c, G)
    w, vr = np.linalg.eig(Lm)
    j = np.argmax(w.real)
    B = vr[N:,j]
    ph = np.unwrap(np.angle(B[N//4:3*N//4]))
    slope = np.polyfit(x[N//4:3*N//4], ph, 1)[0]
    print(f"  G = {G:+.0f}: leading s = {w[j]:.3f}, mean phase slope d(arg B)/dx = {slope:+.3f}")
