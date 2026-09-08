# SCRIPT: N-RECOVERY-01b  (fixes: SF off-grid; EP loop tracking the actual colliding pair, tight radius, clean contour)
import numpy as np

print("=== G3 (fix): circle spectral flow, crossing off-grid ===")
ks = np.arange(-3,4)
agrid = np.linspace(0.013, 1.013, 2000)
signs_prev = np.sign(ks + agrid[0]); cross = 0
for a in agrid[1:]:
    s = np.sign(ks + a)
    cross += int(np.sum((signs_prev < 0) & (s > 0))) - int(np.sum((signs_prev > 0) & (s < 0)))
    signs_prev = s
print(f"   SF over one period = {cross}")

print()
print("=== G5 (fix): encircling the dynamo EP with the COLLIDING pair, r = 0.15 ===")
N = 120; Lx = np.pi
x = np.linspace(0, Lx, N+2)[1:-1]; h = x[1]-x[0]
D2 = (np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
D1 = (np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
ap = np.cos(x)
def Ldyn(a0): return np.block([[D2, a0*np.diag(ap)],[D1, D2]])
a_ep = 3.871725; r = 0.15; M = 200
phis = np.linspace(0, 4*np.pi, 2*M+1)
w0 = np.linalg.eigvals(Ldyn(a_ep + r))
idx6 = np.argsort(-w0.real)[:6]
best = None
for i in range(6):
    for j in range(i+1,6):
        d = abs(w0[idx6[i]]-w0[idx6[j]])
        if best is None or d < best[0]: best = (d, idx6[i], idx6[j])
pair = np.array([w0[best[1]], w0[best[2]]]); start = pair.copy()
disc = [np.angle((pair[0]-pair[1])**2)]
after_one = None
for i, ph in enumerate(phis[1:], 1):
    w = np.linalg.eigvals(Ldyn(a_ep + r*np.exp(1j*ph)))
    new = []; used = set()
    for lam in pair:
        j = min((jj for jj in range(len(w)) if jj not in used), key=lambda jj: abs(w[jj]-lam))
        used.add(j); new.append(w[j])
    pair = np.array(new)
    disc.append(np.angle((pair[0]-pair[1])**2))
    if i == M: after_one = pair.copy()
wind = np.unwrap(disc)
swapped = abs(start[0]-after_one[1]) < 1e-3 and abs(start[1]-after_one[0]) < 1e-3
restored = abs(start[0]-pair[0]) < 1e-3 and abs(start[1]-pair[1]) < 1e-3
print(f"   start pair:      {start[0]:.4f}, {start[1]:.4f}")
print(f"   after ONE loop:  {after_one[0]:.4f}, {after_one[1]:.4f}   swapped = {swapped}")
print(f"   after TWO loops: {pair[0]:.4f}, {pair[1]:.4f}   restored = {restored}")
print(f"   discriminant winding: one loop = {(wind[M]-wind[0])/(2*np.pi):+.4f}, two loops = {(wind[-1]-wind[0])/(2*np.pi):+.4f}")
c = 40.0
ctr = start.mean(); R = 4*abs(start[0]-start[1]) + 0.6
def contour_pair(a0c):
    Lm = Ldyn(a0c); th = np.linspace(0,2*np.pi,500,endpoint=False)
    Cn = 0j; Ld = 0j; Iden = np.eye(2*N)
    for t in th:
        z = ctr + R*np.exp(1j*t)
        TrR = np.trace(np.linalg.inv(z*Iden - Lm))
        Cn += TrR*(1j*R*np.exp(1j*t)); Ld += np.log(c+z)*TrR*(1j*R*np.exp(1j*t))
    f = (2*np.pi/500)/(2j*np.pi)
    return (Cn*f).real, (Ld*f).real
n0, led0 = contour_pair(a_ep + r)
nh, ledh = contour_pair(a_ep + r*np.exp(1j*np.pi))
n1, led1 = contour_pair(a_ep + r*np.exp(2j*np.pi))
print(f"   contour count at phi=0, pi, 2pi: {n0:.4f}, {nh:.4f}, {n1:.4f}")
print(f"   ledger at phi=0 vs 2pi: {led0:.8f} vs {led1:.8f}  single-valued = {abs(led0-led1)<1e-7}")
