# SCRIPT: FIG-SUNS-01  (all figures for the suns paper, regenerated from SHEAR-LANE-01 and BH-DYNAMO-01b)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.linalg import expm, eig, eigvals, cholesky

# ---------- shear-lane machinery ----------
N = 200; Ly = 12.0
y = np.linspace(-Ly, Ly, N+2)[1:-1]; h = y[1]-y[0]
U = np.tanh(y); Upp = -2*np.tanh(y)/np.cosh(y)**2
D2 = (np.diag(np.ones(N-1),1)+np.diag(np.ones(N-1),-1)-2*np.eye(N))/h**2
I = np.eye(N); nu = eta = 2e-3; vA = 1.5; k = 0.45
K2 = D2 - k**2*I; K2inv = np.linalg.inv(K2)
P = h*((k**2)*I - D2)
F = cholesky(np.block([[P,0*I],[0*I,P]]), lower=False); Fi = np.linalg.inv(F)
def Llane(Bp):
    L11 = K2inv@(-1j*k*(np.diag(U)@K2) + 1j*k*np.diag(Upp)) + nu*K2
    return np.block([[L11, 1j*k*Bp*I],[1j*k*Bp*I, -1j*k*np.diag(U)+eta*K2]])
ths_all = [0,15,30,35,40,45,50,60,75,90]
Gm, Kr, Ph, MR = [], [], [], []
zs = np.logspace(-2.5,0.3,10); ts = [3,6,10,15,22,32,46,65,90]
for th in ths_all:
    Lt = F @ Llane(vA*np.sin(np.radians(th))) @ Fi
    mre = eigvals(Lt).real.max(); MR.append(mre)
    Ph.append(np.linalg.norm(Lt@Lt.conj().T - Lt.conj().T@Lt,'fro'))
    if mre < 5e-3:
        Gm.append(max(np.linalg.norm(expm(Lt*t),2)**2 for t in ts))
        Kr.append(max(z*np.linalg.norm(np.linalg.inv(z*np.eye(2*N)-Lt),2) for z in zs))
    else:
        Gm.append(np.nan); Kr.append(np.nan)
fig, ax = plt.subplots(1,2, figsize=(9,3.5))
stab = [i for i,t in enumerate(ths_all) if not np.isnan(Gm[i])]
ax[0].plot([ths_all[i] for i in stab],[Gm[i] for i in stab],'bo-',label=r'$G_{\max}$ (energy)')
ax2 = ax[0].twinx()
ax2.plot([ths_all[i] for i in stab],[Kr[i] for i in stab],'rs--',label='Kreiss')
ax[0].axvspan(0,33,color='orange',alpha=0.15)
ax[0].text(6,7.5,'modally\nunstable',fontsize=8)
ax[0].set_xlabel(r'field tilt $\theta$ (deg from vertical)'); ax[0].set_ylabel(r'$G_{\max}$')
ax2.set_ylabel('Kreiss constant')
ax[0].set_title('Directional rigidity: amplification vs tilt')
ax[0].legend(loc='upper right',fontsize=8); ax2.legend(loc='center right',fontsize=8)
ax[1].plot(ths_all, Ph, 'k^-')
ax[1].set_xlabel(r'$\theta$ (deg)'); ax[1].set_ylabel(r'$\|[\tilde L,\tilde L^\dagger]\|_F$')
ax[1].set_title('Stress stored while release falls')
plt.tight_layout(); plt.savefig('figS1_lane.pdf'); plt.close()
print('figS1 done', [f'{g:.1f}' for g in Gm], [f'{p:.2f}' for p in Ph])

# ---------- dynamo machinery ----------
Nd = 120; Lxx = np.pi
xd = np.linspace(0,Lxx,Nd+2)[1:-1]; hd = xd[1]-xd[0]
D2d = (np.diag(np.ones(Nd-1),1)+np.diag(np.ones(Nd-1),-1)-2*np.eye(Nd))/hd**2
D1d = (np.diag(np.ones(Nd-1),1)-np.diag(np.ones(Nd-1),-1))/(2*hd)
apd = np.cos(xd); Id = np.eye(Nd)
def Ldyn(a0): return np.block([[D2d, a0*np.diag(apd)],[D1d, D2d]])
a_ep = 3.871725
avals = np.linspace(3.4, 4.35, 60)
re1, re2, im1 = [], [], []
for a0 in avals:
    w = eigvals(Ldyn(a0))
    idx6 = np.argsort(-w.real)[:6]
    best=None
    for ii in range(6):
        for kk in range(ii+1,6):
            dd=abs(w[idx6[ii]]-w[idx6[kk]])
            if best is None or dd<best[0]: best=(dd,idx6[ii],idx6[kk])
    p=np.array([w[best[1]],w[best[2]]]); p=p[np.argsort(p.real)]
    re1.append(p[0].real); re2.append(p[1].real); im1.append(abs(p[0].imag))
fig, ax = plt.subplots(1,2, figsize=(9,3.5))
ax[0].plot(avals, re1,'b-',label='Re branch 1'); ax[0].plot(avals, re2,'b--',label='Re branch 2')
ax[0].plot(avals, im1,'r-',label='|Im| (wave born)')
ax[0].axvline(a_ep, color='gray', ls=':')
ax[0].set_xlabel(r'$\alpha_0$'); ax[0].set_title(r'EP birth of the dynamo wave at $\alpha_0^*=3.872$')
ax[0].legend(fontsize=8)
ds = [0.2,0.05,0.0125,0.003125]; kaps=[]
for d in ds:
    Lm = Ldyn(a_ep-d)
    w, vl, vr = eig(Lm, left=True, right=True)
    idx = np.argsort(-w.real)[:2]
    kk=[]
    for j in idx:
        kk.append(np.linalg.norm(vl[:,j])*np.linalg.norm(vr[:,j])/abs(vl[:,j].conj()@vr[:,j]))
    kaps.append(max(kk))
ax[1].loglog(ds, kaps, 'ko-', label=r'$\kappa$ measured')
ax[1].loglog(ds, 1.853/np.sqrt(np.array(ds)), 'r--', label=r'$1.853/\sqrt{\delta}$')
ax[1].set_xlabel(r'$\delta = \alpha_0^*-\alpha_0$'); ax[1].set_title(r'Square-root law: $\kappa\sqrt{\delta}=1.853$')
ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig('figS2_ep.pdf'); plt.close()
print('figS2 done', [f'{q:.1f}' for q in kaps])

# ---------- ladder figure ----------
a_c = 12.6961; a0 = 0.9*a_c
Pd = hd*(-D2d); Wt = np.block([[Pd,0*Id],[0*Id,hd*Id]])
Fd = cholesky(Wt, lower=False); Fdi = np.linalg.inv(Fd)
Lt = Fd @ Ldyn(a0) @ Fdi
slow = eigvals(Lt).real.max()
om = np.linalg.eigvalsh((Lt+Lt.conj().T)/2).max()
tgrid = np.linspace(0.01, 6, 40)
Gt = [np.linalg.norm(expm(Lt*t),2)**2 for t in tgrid]
fig, ax = plt.subplots(figsize=(5.6,3.6))
ax.semilogy(tgrid, Gt, 'b-', label=r'$G(t)$ (energy norm)')
ax.semilogy(tgrid, np.exp(2*slow*tgrid), 'g--', label=f'slow: modal $2s={2*slow:.2f}$')
ax.semilogy(tgrid[tgrid<0.5], np.exp(2*om*tgrid[tgrid<0.5]), 'r:', label=f'hyper: $2\\omega={2*om:.1f}$')
ax.set_xlabel('t'); ax.set_ylabel('energy growth')
ax.set_title(r'The hair ladder at $0.9\,\alpha_{0c}$: three computed rates')
ax.legend(fontsize=8); plt.tight_layout(); plt.savefig('figS3_ladder.pdf'); plt.close()
print('figS3 done: slow', f'{slow:.4f}', 'omega', f'{om:.2f}', 'Gmax', f'{max(Gt):.1f}')
