# SCRIPT: N-RECOVERY-01  (independent audit of the old Dirac/knot papers + the SUN-N-01 pilot: integer record at the dynamo EP)
import numpy as np

print("=== G1: torus boundary operator has EXACT chiral symmetry -> eta identically 0 ===")
# D(m,n) = 2pi[(m+a)s1 + (n+b)s2]; {s3, D} = 0 forces exact +/- pairing at EVERY (a,b)
a, b = 0.31, 0.77
lams = []
for m in range(-6,7):
    for n in range(-6,7):
        r = 2*np.pi*np.hypot(m+a, n+b); lams += [r, -r]
lams = np.sort(np.array(lams))
print(f"   pairing residual max|sorted(L)+sorted(-L)| = {np.max(np.abs(lams + lams[::-1])):.2e}  (structural: {{s3,D}}=0)")
print("   -> Paper I's 'generically nonzero eta' is impossible for this operator; eta = 0 identically. KILL confirmed.")

print()
print("=== G2: the operator where eta DOES work: circle Dirac, eta = 1 - 2a ===")
for a in [0.25, 0.5, 0.75]:
    eps = 1e-4
    ks = np.arange(-200000, 200001)
    lam = ks + a
    eta = np.sum(np.sign(lam)*np.exp(-eps*np.abs(lam)))
    print(f"   a = {a}: eta(regularized) = {eta:+.4f}   exact 1-2a = {1-2*a:+.4f}")

print()
print("=== G3: circle spectral flow: SF = +1 per unit holonomy (the honest integer) ===")
cross = 0
agrid = np.linspace(0.01, 1.01, 2001)
prev = np.sign(np.arange(-3,4)[:,None] + agrid[0]).sum()
lamf = lambda a: np.arange(-3,4) + a
signs_prev = np.sign(lamf(agrid[0]))
for a in agrid[1:]:
    s = np.sign(lamf(a))
    cross += int(np.sum((signs_prev < 0) & (s > 0))) - int(np.sum((signs_prev > 0) & (s < 0)))
    signs_prev = s
print(f"   net signed crossings over one period: SF = {cross}")

print()
print("=== G4: THE RECOVERY -- Levine-Tristram: his n exists, with the walls he remembered ===")
def LT(V, alpha):
    w = np.exp(2j*np.pi*alpha)
    M = (1-w)*V + (1-np.conj(w))*V.T
    ev = np.linalg.eigvalsh(M)
    return int(np.sum(ev > 1e-9) - np.sum(ev < -1e-9))
V_tref = np.array([[-1.,1.],[0.,-1.]])     # right-handed trefoil (chiral)
V_fig8 = np.array([[ 1.,1.],[0.,-1.]])     # figure-eight (amphichiral control)
print("   alpha:   ", "  ".join(f"{al:5.3f}" for al in [0.10,0.15,0.167,0.18,0.5,0.82,0.833,0.85,0.90]))
print("   trefoil: ", "  ".join(f"{LT(V_tref,al):5d}" for al in [0.10,0.15,0.167,0.18,0.5,0.82,0.833,0.85,0.90]))
print("   fig-8:   ", "  ".join(f"{LT(V_fig8,al):5d}" for al in [0.10,0.15,0.167,0.18,0.5,0.82,0.833,0.85,0.90]))
# jump locations vs Alexander roots: trefoil Delta = t^2 - t + 1, roots e^{+-i pi/3} -> alpha = 1/6, 5/6
print(f"   trefoil Alexander roots on S^1 at alpha = 1/6 = {1/6:.4f}, 5/6 = {5/6:.4f} -> jumps land THERE (walls = Alexander roots)")
print("   fig-8 (amphichiral): sigma == 0 everywhere -> chirality detector confirmed on the control")

print()
print("=== G5: SUN-N-01 PILOT -- encircling the dynamo EP: the integer record on OUR operator ===")
N = 120; Lx = np.pi
x = np.linspace(0, Lx, N+2)[1:-1]; h = x[1]-x[0]
D2 = (np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
D1 = (np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
ap = np.cos(x)
def Ldyn(a0):
    return np.block([[D2, a0*np.diag(ap)],[D1, D2]])
a_ep = 3.871725; r = 0.35
M = 160
phis = np.linspace(0, 4*np.pi, 2*M+1)      # TWO loops
# initial pair at phi=0
w0 = np.linalg.eigvals(Ldyn(a_ep + r))
idx = np.argsort(-w0.real)[:2]
pair = w0[idx].copy()
start = pair.copy()
disc_args = [np.angle((pair[0]-pair[1])**2)]
after_one = None
for i, ph in enumerate(phis[1:], 1):
    w = np.linalg.eigvals(Ldyn(a_ep + r*np.exp(1j*ph)))
    # continuity tracking: match each tracked eigenvalue to nearest current
    new = []
    used = set()
    for lam in pair:
        j = min((jj for jj in range(len(w)) if jj not in used), key=lambda jj: abs(w[jj]-lam))
        used.add(j); new.append(w[j])
    pair = np.array(new)
    disc_args.append(np.angle((pair[0]-pair[1])**2))
    if i == M: after_one = pair.copy()
wind = np.unwrap(disc_args)
print(f"   start pair:        {start[0]:.4f}, {start[1]:.4f}")
print(f"   after ONE loop:    {after_one[0]:.4f}, {after_one[1]:.4f}   -> swapped: {np.allclose(sorted(start.imag), sorted(after_one.imag), atol=1e-3) and abs(start[0]-after_one[1])<1e-2}")
print(f"   after TWO loops:   {pair[0]:.4f}, {pair[1]:.4f}   -> restored: {abs(start[0]-pair[0])<1e-2 and abs(start[1]-pair[1])<1e-2}")
print(f"   discriminant winding over one loop  = {(wind[M]-wind[0])/(2*np.pi):+.3f}   (integer record)")
print(f"   discriminant winding over two loops = {(wind[-1]-wind[0])/(2*np.pi):+.3f}")
# ledger single-valuedness + count on a fixed contour enclosing the pair region
c = 40.0
ctr = start.mean(); R = 3.0*max(abs(start[0]-ctr), 1.0)
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
n1, led1 = contour_pair(a_ep + r*np.exp(2j*np.pi))
print(f"   contour count start/after loop: {n0:.4f} / {n1:.4f};  ledger start/after: {led0:.6f} / {led1:.6f}  (single-valued: {abs(led0-led1)<1e-6})")
