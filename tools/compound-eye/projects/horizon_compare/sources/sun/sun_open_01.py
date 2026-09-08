# SCRIPT: SUN-OPEN-01  (closing open problems 1,2,3,8: hemispheric Parker-Yoshimura, onset character, k-optimized envelope, EP/braid census)
import numpy as np
from scipy.linalg import expm, eigvals, cholesky

# ---------- hemispheric Parker model: x in [0, pi/2], pole Dirichlet, equator dipole parity ----------
N = 120; Lx = np.pi/2
x = np.linspace(0, Lx, N+1)[1:]           # interior + last node adjacent to equator ghost
h = x[1]-x[0]
def ops_dirichlet():
    D2 = (np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
    D1 = (np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
    return D2, D1
# B: Dirichlet pole and equator. A: Dirichlet pole, Neumann equator (dipole parity)
D2B, D1B = ops_dirichlet()
D2A = D2B.copy(); D1A = D1B.copy()
D2A[-1,-1] = -1/h**2          # ghost A_{N+1}=A_N
D1A[-1,-1] =  1/(2*h)         # (A_N - A_{N-1})/2h at last row
ap = np.cos(x)
def Lhemi(a0, G=1.0):
    return np.block([[D2A, a0*np.diag(ap)],[G*D1A, D2B]])

print("=== OP2: onset character of the hemispheric (dipole-parity) model ===")
def maxRe(a0, G=1.0):
    return eigvals(Lhemi(a0,G)).real.max()
grid = np.linspace(0.5, 60, 60); cross=None; prev=maxRe(grid[0])
for a0 in grid[1:]:
    cur = maxRe(a0)
    if prev < 0 <= cur: cross=a0; break
    prev=cur
lo, hi = cross-1.0, cross
for _ in range(40):
    mid=(lo+hi)/2
    if maxRe(mid)<0: lo=mid
    else: hi=mid
a_c = hi
w = eigvals(Lhemi(a_c)); j=np.argmax(w.real)
osc = abs(w[j].imag) > 1e-6
print(f"   alpha0_c(hemi) = {a_c:.4f};  leading s = {w[j].real:+.5f} {w[j].imag:+.4f}i  -> {'OSCILLATORY' if osc else 'STEADY'} onset"
      + (f", cycle period {2*np.pi/abs(w[j].imag):.2f}" if osc else ""))

print()
print("=== OP1: Parker-Yoshimura flip in the hemispheric model ===")
for G in [+1.0, -1.0]:
    a0 = 0.98*a_c
    wv, vr = np.linalg.eig(Lhemi(a0, G))
    cand = [k for k in range(len(wv)) if wv[k].imag > 1e-6]
    j = cand[int(np.argmax(wv.real[cand]))]
    B = vr[N:, j]
    seg = slice(N//5, 4*N//5)
    ph = np.unwrap(np.angle(B[seg]))
    slope = np.polyfit(x[seg], ph, 1)[0]
    print(f"   G = {G:+.0f}: wave s = {wv[j]:.4f}, phase slope d(arg B)/dx = {slope:+.3f}")

# butterfly data for the figure (G=+1 wave mode)
a0 = 0.98*a_c
wv, vr = np.linalg.eig(Lhemi(a0, +1.0))
cand = [k for k in range(len(wv)) if wv[k].imag > 1e-6]
j = cand[int(np.argmax(wv.real[cand]))]
np.save('butterfly_mode.npy', np.array([wv[j].real, wv[j].imag]))
np.save('butterfly_B.npy', vr[N:, j]); np.save('butterfly_x.npy', x)

print()
print("=== OP8: EP/braid census along alpha0 (full-domain model) ===")
Nd=120; Lxx=np.pi
xd=np.linspace(0,Lxx,Nd+2)[1:-1]; hd=xd[1]-xd[0]
D2d=(np.diag(np.ones(Nd-1),1)+np.diag(np.ones(Nd-1),-1)-2*np.eye(Nd))/hd**2
D1d=(np.diag(np.ones(Nd-1),1)-np.diag(np.ones(Nd-1),-1))/(2*hd)
apd=np.cos(xd)
Ldyn=lambda a0: np.block([[D2d, a0*np.diag(apd)],[D1d, D2d]])
def n_complex_top(a0, k=10):
    w = eigvals(Ldyn(a0)); idx = np.argsort(-w.real)[:k]
    return int(np.sum(w[idx].imag > 1e-7))
eps_list=[]
agrid = np.linspace(0.2, 13.0, 129)
prev = n_complex_top(agrid[0])
for a0 in agrid[1:]:
    cur = n_complex_top(a0)
    if cur > prev:
        lo, hi = a0-0.1, a0
        for _ in range(35):
            mid=(lo+hi)/2
            if n_complex_top(mid) <= prev: lo=mid
            else: hi=mid
        eps_list.append((hi, cur-prev))
    prev = max(prev, cur)
print(f"   pair-birth events found: {[(round(a,4)) for a,_ in eps_list]}")
def winding_at(aep, r=0.10, M=80):
    w0 = eigvals(Ldyn(aep + r)); idx6 = np.argsort(-w0.real)[:8]
    best=None
    for i in range(8):
        for jj in range(i+1,8):
            d=abs(w0[idx6[i]]-w0[idx6[jj]])
            if best is None or d<best[0]: best=(d,idx6[i],idx6[jj])
    pair=np.array([w0[best[1]],w0[best[2]]]); start=pair.copy()
    disc=[np.angle((pair[0]-pair[1])**2)]
    for ph in np.linspace(0,2*np.pi,M+1)[1:]:
        w=eigvals(Ldyn(aep + r*np.exp(1j*ph)))
        new=[];used=set()
        for lam in pair:
            k2=min((kk for kk in range(len(w)) if kk not in used),key=lambda kk:abs(w[kk]-lam))
            used.add(k2); new.append(w[k2])
        pair=np.array(new); disc.append(np.angle((pair[0]-pair[1])**2))
    wind=np.unwrap(disc)
    swapped = abs(start[0]-pair[1])<5e-3 and abs(start[1]-pair[0])<5e-3
    return (wind[-1]-wind[0])/(2*np.pi), swapped
print("   census (alpha0*, winding per loop, pair exchanged):")
for aep,_ in eps_list[:4]:
    wnd, sw = winding_at(aep)
    print(f"     alpha0* = {aep:8.4f}   winding = {wnd:+.3f}   exchange = {sw}")

print()
print("=== OP3 (2D part): k-optimized transient envelope of the shear lane ===")
Ns=200; Ly=12.0
y=np.linspace(-Ly,Ly,Ns+2)[1:-1]; hs=y[1]-y[0]
U=np.tanh(y); Upp=-2*np.tanh(y)/np.cosh(y)**2
D2s=(np.diag(np.ones(Ns-1),1)+np.diag(np.ones(Ns-1),-1)-2*np.eye(Ns))/hs**2
Is=np.eye(Ns); nu=eta=2e-3; vA=1.5
def Gmax_lane(th_deg, k):
    K2=D2s-k**2*Is; K2i=np.linalg.inv(K2)
    Bp=vA*np.sin(np.radians(th_deg))
    L11=K2i@(-1j*k*(np.diag(U)@K2)+1j*k*np.diag(Upp))+nu*K2
    L=np.block([[L11,1j*k*Bp*Is],[1j*k*Bp*Is,-1j*k*np.diag(U)+eta*K2]])
    P=hs*((k**2)*Is-D2s)
    F=cholesky(np.block([[P,0*Is],[0*Is,P]]),lower=False); Fi=np.linalg.inv(F)
    Lt=F@L@Fi
    if eigvals(Lt).real.max() > 5e-3: return np.nan
    return max(np.linalg.norm(expm(Lt*t),2)**2 for t in [5,10,18,30,50,80])
for th in [35, 45, 60]:
    best=(0,0)
    for k in [0.15,0.25,0.35,0.45,0.6,0.8]:
        g=Gmax_lane(th,k)
        if not np.isnan(g) and g>best[0]: best=(g,k)
    print(f"   theta={th}: G_max over k = {best[0]:.1f} at k={best[1]}   (fixed-k value at 0.45 was {Gmax_lane(th,0.45):.1f})")

print()
print("=== OP5 (theory side): spacing/width ratio vs tilt in the unstable band ===")
for th in [0, 10, 20, 30]:
    Bp=vA*np.sin(np.radians(th))
    ks=np.linspace(0.2,0.8,13); sig=[]
    for k in ks:
        K2=D2s-k**2*Is; K2i=np.linalg.inv(K2)
        L11=K2i@(-1j*k*(np.diag(U)@K2)+1j*k*np.diag(Upp))+nu*K2
        L=np.block([[L11,1j*k*Bp*Is],[1j*k*Bp*Is,-1j*k*np.diag(U)+eta*K2]])
        sig.append(eigvals(L).real.max())
    km=ks[int(np.argmax(sig))]
    print(f"   theta={th}: k_max={km:.3f} -> spacing = {2*np.pi/km:.1f} half-widths (spacing/full-width = {2*np.pi/km/4:.2f})")
