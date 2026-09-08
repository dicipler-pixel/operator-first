# SCRIPT: BH-DYNAMO-01b  (fix pass: true onset, energy norm ladder, exact-pair ledger with count gate, Parker-Yoshimura on the wave branch)
import numpy as np
from scipy.linalg import expm, eig, eigvals, cholesky
N = 120; Lx = np.pi
x = np.linspace(0, Lx, N+2)[1:-1]; h = x[1]-x[0]
D2 = (np.diag(np.ones(N-1),1) + np.diag(np.ones(N-1),-1) - 2*np.eye(N))/h**2
D1 = (np.diag(np.ones(N-1),1) - np.diag(np.ones(N-1),-1))/(2*h)
ap = np.cos(x); I = np.eye(N)
def Lop(a0, G=1.0):
    return np.block([[D2, a0*np.diag(ap)],[G*D1, D2]])

print("=== PD1 (fix): true onset, alpha0 up to 80 ===")
def maxRe(a0):
    return eigvals(Lop(a0)).real.max()
a_lo, a_hi = 1.0, 80.0
grid = np.linspace(a_lo, a_hi, 40)
cross = None; prev = maxRe(grid[0])
for a0 in grid[1:]:
    cur = maxRe(a0)
    if prev < 0 <= cur: cross = a0; break
    prev = cur
assert cross is not None, "no onset below 80"
lo, hi = cross - (grid[1]-grid[0]), cross
for _ in range(45):
    mid = (lo+hi)/2
    if maxRe(mid) < 0: lo = mid
    else: hi = mid
a_c = hi
w = eigvals(Lop(a_c)); j = np.argmax(w.real)
print(f"  alpha0_c = {a_c:.4f}  (D_c = {a_c*np.pi**3:.0f});  leading s = {w[j].real:+.5f} {w[j].imag:+.4f}i  -> {'OSCILLATORY' if abs(w[j].imag)>1e-6 else 'STEADY'} onset; period = {2*np.pi/abs(w[j].imag) if abs(w[j].imag)>1e-9 else float('inf'):.2f}")

print()
print("=== PD2 (fix): hair ladder at 0.9*alpha0_c in the energy norm E = int(|A_x|^2 + |B|^2) ===")
a0 = 0.9*a_c
Ld = Lop(a0)
P = h*(-D2); Wt = np.block([[P, 0*I],[0*I, h*I]])
F = cholesky(Wt, lower=False); Fi = np.linalg.inv(F)
Lt = F @ Ld @ Fi
wl = eigvals(Lt); jj = np.argmax(wl.real)
slow = wl.real[jj]; per = 2*np.pi/abs(wl[jj].imag) if abs(wl[jj].imag)>1e-9 else np.inf
om = np.linalg.eigvalsh((Lt+Lt.conj().T)/2).max()
Gm, tp = 0.0, 0.0
for t in [0.01,0.02,0.04,0.08,0.15,0.3,0.5,0.9,1.5,2.5,4.0,6.0]:
    g = np.linalg.norm(expm(Lt*t),2)**2
    if g > Gm: Gm, tp = g, t
Phi = np.linalg.norm(Lt@Lt.conj().T - Lt.conj().T@Lt, 'fro')/np.linalg.norm(Lt,'fro')**2
print(f"  SLOW: max Re s = {slow:+.4f}, wave period = {per:.2f}")
print(f"  FAST: G_max = {Gm:.1f} at t = {tp}   (t_peak/period = {tp/per if np.isfinite(per) else 0:.3f})")
print(f"  HYPER: numerical abscissa = {om:+.2f}  (vs slow {slow:+.4f})")
print(f"  normalized Phi-stress = {Phi:.4f}")

print()
print("=== PD4 (fix): ledger with exact-pair contour + enclosed-count gate ===")
a_ep = 3.871725
c = 40.0
for tag, aa in [("at EP", a_ep), ("near EP", a_ep-0.003)]:
    Lm = Lop(aa)
    wv = eigvals(Lm)
    # the colliding pair = two eigenvalues closest to each other among the 6 least-damped
    idx6 = np.argsort(-wv.real)[:6]
    best = None
    for ii in range(6):
        for kk in range(ii+1,6):
            dd = abs(wv[idx6[ii]]-wv[idx6[kk]])
            if best is None or dd < best[0]: best = (dd, idx6[ii], idx6[kk])
    pair = np.array([wv[best[1]], wv[best[2]]])
    ctr = pair.mean()
    others = np.delete(wv, [best[1], best[2]])
    gap = min(abs(others - ctr))
    r = 0.45*gap
    M = 800; th = np.linspace(0,2*np.pi,M,endpoint=False)
    Scount = 0.0+0j; Sled = 0.0+0j
    Iden = np.eye(2*N)
    for t in th:
        z = ctr + r*np.exp(1j*t)
        TrR = np.trace(np.linalg.inv(z*Iden - Lm))
        Scount += TrR*(1j*r*np.exp(1j*t))
        Sled   += np.log(c+z)*TrR*(1j*r*np.exp(1j*t))
    Scount *= (2*np.pi/M)/(2j*np.pi); Sled *= (2*np.pi/M)/(2j*np.pi)
    direct = np.sum(np.log(c+pair))
    print(f"  {tag}: enclosed count = {Scount.real:.6f}; ledger = {Sled.real:.10f}; direct = {direct.real:.10f}; diff = {abs(Sled-direct):.2e}")

print()
print("=== PD5 (fix): Parker-Yoshimura on the WAVE branch (least-damped complex mode), G=+-1 ===")
for G in [+1.0, -1.0]:
    Lm = Lop(0.95*a_c, G)
    wv, vr = np.linalg.eig(Lm)
    cand = [j for j in range(len(wv)) if wv[j].imag > 1e-6]
    j = cand[int(np.argmax(wv.real[cand]))]
    B = vr[N:, j]
    seg = slice(N//4, 3*N//4)
    ph = np.unwrap(np.angle(B[seg]))
    slope = np.polyfit(x[seg], ph, 1)[0]
    print(f"  G = {G:+.0f}: wave s = {wv[j]:.4f}, phase slope d(arg B)/dx = {slope:+.3f}")
