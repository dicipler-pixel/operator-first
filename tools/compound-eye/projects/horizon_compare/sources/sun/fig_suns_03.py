# SCRIPT: FIG-SUNS-03  (figS5: hemispheric butterfly diagrams -- Parker-Yoshimura flip)
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
N=120; Lx=np.pi/2
x=np.linspace(0,Lx,N+1)[1:]; h=x[1]-x[0]
D2B=(np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
D1B=(np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
D2A=D2B.copy(); D1A=D1B.copy()
D2A[-1,-1]=-1/h**2; D1A[-1,-1]=1/(2*h)
ap=np.cos(x)
Lh=lambda a0,G: np.block([[D2A,a0*np.diag(ap)],[G*D1A,D2B]])
a0=0.98*12.5264
fig,ax=plt.subplots(1,2,figsize=(9,3.6))
for col,G in enumerate([+1.0,-1.0]):
    wv,vr=np.linalg.eig(Lh(a0,G))
    cand=[k for k in range(len(wv)) if wv[k].imag>1e-6]
    j=cand[int(np.argmax(wv.real[cand]))]
    B=vr[N:,j]; om=wv[j].imag
    T=2*np.pi/om
    t=np.linspace(0,2*T,240)
    lat=90-x*180/np.pi
    F=np.real(np.outer(np.exp(1j*om*t),B))
    F=F/np.max(np.abs(F))
    ax[col].contourf(t/T,lat,F.T,levels=21,cmap='RdBu_r')
    ax[col].set_xlabel('t / cycle'); ax[col].set_ylabel('latitude (deg)')
    ax[col].set_title(f'G={G:+.0f}: '+('poleward' if G>0 else 'equatorward (solar-like)'))
plt.tight_layout(); plt.savefig('figS5_butterfly.pdf'); plt.close()
print("figS5 done")
