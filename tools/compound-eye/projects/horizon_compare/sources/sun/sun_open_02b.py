# SCRIPT: SUN-OPEN-02b  (shell onset pinned: radial-shear oscillatory onset + latitudinal-shear control + resolution check)
import numpy as np
from scipy.linalg import eigvals
def build(Nr,Nx,shear,r0=0.2):
    rr=np.linspace(r0,1.0,Nr+2)[1:-1]; hr=rr[1]-rr[0]
    xx=np.linspace(0,np.pi,Nx+2)[1:-1]; hx=xx[1]-xx[0]
    D2r=(np.diag(np.ones(Nr-1),1)+np.diag(np.ones(Nr-1),-1)-2*np.eye(Nr))/hr**2
    D2x=(np.diag(np.ones(Nx-1),1)+np.diag(np.ones(Nx-1),-1)-2*np.eye(Nx))/hx**2
    D1r=(np.diag(np.ones(Nr-1),1)-np.diag(np.ones(Nr-1),-1))/(2*hr)
    D1x=(np.diag(np.ones(Nx-1),1)-np.diag(np.ones(Nx-1),-1))/(2*hx)
    Ir,Ix=np.eye(Nr),np.eye(Nx)
    Lap=np.kron(D2r,Ix)+np.kron(Ir,D2x)
    Alpha=np.kron(Ir,np.diag(np.cos(xx)))
    Sh=np.kron(Ir,D1x) if shear=='lat' else np.kron(D1r,Ix)
    return lambda a0: np.block([[Lap,a0*Alpha],[Sh,Lap]])
def mR(L,a0): return eigvals(L(a0)).real.max()
L=build(16,32,'rad')
lo,hi=1500.,2500.
for _ in range(24):
    mid=(lo+hi)/2
    if mR(L,mid)<0: lo=mid
    else: hi=mid
w=eigvals(L(hi)); j=np.argmax(w.real)
print(f"RADIAL shear (16x32): a0c = {hi:.1f}, onset s = {w[j].real:+.4f}{w[j].imag:+.3f}i -> {'OSCILLATORY' if abs(w[j].imag)>1e-4 else 'STEADY'}, cycle = {2*np.pi/abs(w[j].imag):.4f}")
Ll=build(16,32,'lat')
for a0 in [1000,2500,5000]:
    w=eigvals(Ll(a0)); j=np.argmax(w.real)
    print(f"LATITUDINAL shear control: a0={a0}: max Re = {w[j].real:+.3f}, Im = {w[j].imag:+.3f}")
L2=build(22,44,'rad')
w=eigvals(L2(hi)); j=np.argmax(w.real)
print(f"resolution check (22x44) at a0c(16x32): s = {w[j].real:+.3f}{w[j].imag:+.3f}i  ({'oscillatory branch persists' if abs(w[j].imag)>1e-3 else 'steady?!'})")
