# SCRIPT: SUN-OPEN-02  (v1.3 audit: EP4/5 with radial-continuation tracking; 2D shell onset mechanism; hazard-law arithmetic)
import numpy as np
from scipy.linalg import eigvals

print("=== A: EP census with radial-continuation pair selection (all five points) ===")
N=120; Lx=np.pi
x=np.linspace(0,Lx,N+2)[1:-1]; h=x[1]-x[0]
D2=(np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
D1=(np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
ap=np.cos(x)
Ldyn=lambda a0: np.block([[D2,a0*np.diag(ap)],[D1,D2]])
def newborn_pair(a0, ktop=14):
    w=eigvals(Ldyn(a0)); idx=np.argsort(-w.real)[:ktop]
    cpx=[j for j in idx if w[j].imag>1e-9]
    j=min(cpx,key=lambda j: w[j].imag)          # smallest positive-Im = just-born branch
    lam=w[j]
    jj=min((k for k in idx if k!=j),key=lambda k:abs(w[k]-np.conj(lam)))
    return np.array([lam,w[jj]])
def track(pair, a0c):
    w=eigvals(Ldyn(a0c)); new=[];used=set()
    for lam in pair:
        k=min((kk for kk in range(len(w)) if kk not in used),key=lambda kk:abs(w[kk]-lam))
        used.add(k); new.append(w[k])
    return np.array(new)
for a_ep in [3.8717,5.2802,7.1576,9.0850,11.0320]:
    r=0.12
    pair=newborn_pair(a_ep+0.004)
    for aa in np.linspace(a_ep+0.004,a_ep+r,18)[1:]:  # radial continuation out to loop radius
        pair=track(pair,aa)
    start=pair.copy(); disc=[np.angle((pair[0]-pair[1])**2)]
    for ph in np.linspace(0,2*np.pi,101)[1:]:
        pair=track(pair,a_ep+r*np.exp(1j*ph))
        disc.append(np.angle((pair[0]-pair[1])**2))
    wind=(np.unwrap(disc)[-1]-np.unwrap(disc)[0])/(2*np.pi)
    sw = abs(start[0]-pair[1])<5e-3 and abs(start[1]-pair[0])<5e-3
    print(f"   alpha0* = {a_ep:8.4f}:  winding = {wind:+.4f}   exchange = {sw}")

print()
print("=== B: 2D shell onset mechanism (radial structure) ===")
def shell_onset(Nr, Nx, shear):   # shear: 'lat' = G dA/dx (control), 'rad' = G dA/dr (solar alpha-Omega geometry)
    rr=np.linspace(0.7,1.0,Nr+2)[1:-1]; hr=rr[1]-rr[0]
    xx=np.linspace(0,np.pi,Nx+2)[1:-1]; hx=xx[1]-xx[0]
    D2r=(np.diag(np.ones(Nr-1),1)+np.diag(np.ones(Nr-1),-1)-2*np.eye(Nr))/hr**2
    D2x=(np.diag(np.ones(Nx-1),1)+np.diag(np.ones(Nx-1),-1)-2*np.eye(Nx))/hx**2
    D1r=(np.diag(np.ones(Nr-1),1)-np.diag(np.ones(Nr-1),-1))/(2*hr)
    D1x=(np.diag(np.ones(Nx-1),1)-np.diag(np.ones(Nx-1),-1))/(2*hx)
    Ir,Ix=np.eye(Nr),np.eye(Nx)
    Lap=np.kron(D2r,Ix)+np.kron(Ir,D2x)
    Alpha=np.kron(Ir,np.diag(np.cos(xx)))
    Sh = np.kron(Ir,D1x) if shear=='lat' else np.kron(D1r,Ix)
    def Lsh(a0): return np.block([[Lap,a0*Alpha],[Sh,Lap]])
    def mR(a0): return eigvals(Lsh(a0)).real.max()
    grid=np.linspace(5,240,24); cross=None; prev=mR(grid[0])
    for a0 in grid[1:]:
        cur=mR(a0)
        if prev<0<=cur: cross=a0; break
        prev=cur
    if cross is None: return None
    lo,hi=cross-(grid[1]-grid[0]),cross
    for _ in range(28):
        mid=(lo+hi)/2
        if mR(mid)<0: lo=mid
        else: hi=mid
    w=eigvals(Lsh(hi)); j=np.argmax(w.real)
    return hi, w[j]
for shear in ['lat','rad']:
    res = shell_onset(16,32,shear)
    if res is None: print(f"   shear={shear}: no onset below a0=240"); continue
    ac,s = res
    print(f"   shear={shear} (16x32): a0c = {ac:8.3f}, leading s = {s.real:+.5f} {s.imag:+.4f}i -> {'OSCILLATORY' if abs(s.imag)>1e-5 else 'STEADY'}")
res = shell_onset(22,44,'rad')
if res: 
    ac,s = res
    print(f"   shear=rad  (22x44): a0c = {ac:8.3f}, leading s = {s.real:+.5f} {s.imag:+.4f}i -> {'OSCILLATORY' if abs(s.imag)>1e-5 else 'STEADY'}  (resolution check)")

print()
print("=== C: hazard-law arithmetic and sensitivity ===")
for beta in [-0.8,-0.9,-1.0]:
    if beta==-1.0: print(f"   beta={beta:+.1f}: exponent -> infinity (logarithmic hazard)"); continue
    print(f"   beta={beta:+.1f}: WTD tail exponent 3+beta = {3+beta:.1f};  hazard lambda ~ Phi^(1/(1+beta)) = Phi^{1/(1+beta):.0f}")
print(f"   steepness at exponent 10: 7.2% stress rise doubles the rate (2**0.1={2**0.1:.4f}); 26% rise -> x{1.26**10:.1f}")
print()
print("=== D: OP5 width-per-tilt table (arithmetic from R(theta)) ===")
for th,Rr in [(0,3.49),(10,3.93),(20,4.49),(30,6.28)]:
    print(f"   theta={th:2d}: width for 60 km spacing = {60/Rr:.1f} km; for 100 km = {100/Rr:.1f} km")
