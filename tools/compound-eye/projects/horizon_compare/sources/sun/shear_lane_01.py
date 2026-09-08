# SCRIPT: SHEAR-LANE-01  (magnetized shear layer: modal quench, transient growth, Kreiss, Phi-stress vs field tilt)
import numpy as np
from scipy.linalg import expm, cholesky, eigvals, solve
N = 200; Ly = 12.0
y = np.linspace(-Ly, Ly, N+2)[1:-1]; h = y[1]-y[0]
U  = np.tanh(y); Upp = -2*np.tanh(y)/np.cosh(y)**2
D2 = (np.diag(np.ones(N-1),1) + np.diag(np.ones(N-1),-1) - 2*np.eye(N))/h**2
I  = np.eye(N); nu = 2e-3; eta = 2e-3
vA = 1.5

def Lop(k, Bpar):
    K2 = D2 - k**2*I
    K2inv = np.linalg.inv(K2)
    L11 = K2inv @ (-1j*k*(np.diag(U) @ K2) + 1j*k*np.diag(Upp)) + nu*K2
    L12 = 1j*k*Bpar*I
    L21 = 1j*k*Bpar*I
    L22 = -1j*k*np.diag(U) + eta*K2
    return np.block([[L11, L12],[L21, L22]])

def weighted(k):
    P = h*((k**2)*I - D2)                 # SPD energy weight per field
    F = cholesky(np.block([[P, 0*I],[0*I, P]]), lower=False)
    Finv = np.linalg.inv(F)
    return F, Finv

print("=== P1 control: theta=0 pure hydro KH (Michalke: sigma=0.190 at k=0.445, neutral k=1) ===")
ks = np.linspace(0.1, 1.15, 15)
sig0 = []
for k in ks:
    w = eigvals(Lop(k, 0.0))
    sig0.append(w.real.max())
sig0 = np.array(sig0)
i0 = sig0.argmax()
print("  k grid max: sigma=%.4f at k=%.3f ; sigma(k=1.01)=%.4f" % (sig0[i0], ks[i0], sig0[np.argmin(abs(ks-1.01))]))

print()
print("=== main scan: theta = tilt of B from vertical; B_par = vA sin(theta), vA=1.5, k=0.45 ===")
k = 0.45
F, Finv = weighted(k)
ts = [3,6,10,15,22,32,46,65,90,125]
zs = np.logspace(-2.5, 0.3, 10)
print(f"{'theta':>6} {'B_par':>6} {'maxRe':>9} {'Gmax':>10} {'t_peak':>7} {'Kreiss':>9} {'PhiF':>10}")
rows=[]
for th in [0,15,30,35,40,45,50,60,75,90]:
    Bp = vA*np.sin(np.radians(th))
    L = Lop(k, Bp)
    Lt = F @ L @ Finv
    mre = eigvals(Lt).real.max()
    Gm, tp = 0.0, 0.0
    if mre < 5e-3:
        for t in ts:
            g = np.linalg.norm(expm(Lt*t), 2)**2
            if g > Gm: Gm, tp = g, t
    else:
        Gm, tp = float('nan'), float('nan')
    Kr = max(z*np.linalg.norm(np.linalg.inv(z*np.eye(2*N)-Lt), 2) for z in zs) if mre < 5e-3 else float('nan')
    Phi = np.linalg.norm(Lt @ Lt.conj().T - Lt.conj().T @ Lt, 'fro')
    rows.append((th,Bp,mre,Gm,tp,Kr,Phi))
    print(f"{th:6d} {Bp:6.3f} {mre:9.4f} {Gm:10.1f} {tp:7.1f} {Kr:9.2f} {Phi:10.2f}")

print()
print("=== P5: fastest-growing wavelength at theta=0 (spacing/thickness ratio) ===")
kfine = np.linspace(0.25, 0.7, 19)
sf = [eigvals(Lop(kk,0.0)).real.max() for kk in kfine]
km = kfine[int(np.argmax(sf))]
lam = 2*np.pi/km
print(f"  k_max = {km:.3f}  -> spacing lambda = {lam:.1f} d (d = tanh half-width)")
print(f"  DKIST inversion: spacing 60-100 km -> d = {60/lam:.1f}-{100/lam:.1f} km -> full 90%% shear width 4d = {240/lam:.0f}-{400/lam:.0f} km... per-unit: {4*60/lam:.0f}-{4*100/lam:.0f} km")
