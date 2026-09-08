# SCRIPT: FIG-SUNS-02  (figS4: the braid at the dynamo EP -- pair exchange and discriminant winding)
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
N=120; Lx=np.pi
x=np.linspace(0,Lx,N+2)[1:-1]; h=x[1]-x[0]
D2=(np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
D1=(np.diag(np.ones(N-1),1)-np.diag(np.ones(N-1),-1))/(2*h)
ap=np.cos(x)
Ldyn=lambda a0: np.block([[D2,a0*np.diag(ap)],[D1,D2]])
a_ep=3.871725; r=0.15; M=200
phis=np.linspace(0,4*np.pi,2*M+1)
w0=np.linalg.eigvals(Ldyn(a_ep+r)); idx6=np.argsort(-w0.real)[:6]
best=None
for i in range(6):
    for j in range(i+1,6):
        d=abs(w0[idx6[i]]-w0[idx6[j]])
        if best is None or d<best[0]: best=(d,idx6[i],idx6[j])
pair=np.array([w0[best[1]],w0[best[2]]]); start=pair.copy()
tr1=[pair[0]]; tr2=[pair[1]]; disc=[np.angle((pair[0]-pair[1])**2)]
for ph in phis[1:]:
    w=np.linalg.eigvals(Ldyn(a_ep+r*np.exp(1j*ph)))
    new=[];used=set()
    for lam in pair:
        j=min((jj for jj in range(len(w)) if jj not in used),key=lambda jj:abs(w[jj]-lam))
        used.add(j); new.append(w[j])
    pair=np.array(new); tr1.append(pair[0]); tr2.append(pair[1])
    disc.append(np.angle((pair[0]-pair[1])**2))
tr1=np.array(tr1); tr2=np.array(tr2); wind=np.unwrap(disc)
fig,ax=plt.subplots(1,2,figsize=(9,3.6))
ax[0].plot(tr1[:M+1].real,tr1[:M+1].imag,'b-',lw=1.5,label='branch 1, loop 1')
ax[0].plot(tr2[:M+1].real,tr2[:M+1].imag,'r-',lw=1.5,label='branch 2, loop 1')
ax[0].plot(start[0].real,start[0].imag,'bo',ms=8)
ax[0].plot(start[1].real,start[1].imag,'rs',ms=8)
ax[0].plot(tr1[M].real,tr1[M].imag,'b*',ms=13)
ax[0].plot(tr2[M].real,tr2[M].imag,'r*',ms=13)
ax[0].set_xlabel(r'Re $\lambda$'); ax[0].set_ylabel(r'Im $\lambda$')
ax[0].set_title('One loop around the EP: the pair exchanges')
ax[0].legend(fontsize=8)
ax[1].plot(phis/(2*np.pi),(wind-wind[0])/(2*np.pi),'k-')
ax[1].axhline(1,color='gray',ls=':'); ax[1].axhline(2,color='gray',ls=':')
ax[1].set_xlabel('loops around the EP'); ax[1].set_ylabel(r'winding of $\arg(\lambda_1-\lambda_2)^2/2\pi$')
ax[1].set_title('Integer record: winding $+1$ per loop')
plt.tight_layout(); plt.savefig('figS4_braid.pdf'); plt.close()
print("figS4 done: winding one/two loops =", (wind[M]-wind[0])/(2*np.pi), (wind[-1]-wind[0])/(2*np.pi))
