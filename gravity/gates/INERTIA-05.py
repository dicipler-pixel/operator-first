#!/usr/bin/env python3
# SCRIPT: INERTIA-05   closes the two scope items and adds the control that was missing.
#
# C0  POSITIVE CONTROL, run FIRST and able to void everything after it.  For a
#     self-adjoint generator the block quantum metric is PSD by construction, so the
#     full-space inertia must come back with zero negative directions above roundoff.
#     If it does not, the pipeline is wrong and no result below stands.
# C1  FULL PERTURBATION SPACE.  Potential directions alone span only half the
#     generator; the damping block contributes another 97.  Basis probe operators are
#     rank one in both blocks, so all 194 derivatives come from one solve per node:
#         potential  V_j = -i E_{n+j, j}        damping  V_j = +i E_{n+j, n+j}
# C2  FOUR GENERATOR FAMILIES, so the verdict is not one potential.
import numpy as np

def cheb(N):
    x=np.cos(np.pi*np.arange(N+1)/N)
    c=np.ones(N+1); c[0]=2.; c[-1]=2.; c*=(-1.)**np.arange(N+1)
    X=np.tile(x,(N+1,1)).T
    D=np.outer(c,1./c)/((X-X.T)+np.eye(N+1)); D-=np.diag(D.sum(axis=1))
    return D,x

def generator(N,V0,s,a=0.0):
    D,x=cheb(N); I=np.eye(N+1); Z=0*I
    L1=np.diag(1-x**2)@D@D-2*np.diag(x)@D-V0*I
    L2=-2*np.diag(x)@D-I+a*D
    return 1j*np.block([[Z,I],[L1,s*L2]]),x

def track(N,V0,s,a):
    L,x=generator(N,V0,s,a); ev,_=np.linalg.eig(L)
    root=np.sqrt(complex(V0-0.25)); t0,t1=root-0.5j,root-1.5j
    i0=int(np.argmin(np.abs(ev-t0))); i1=int(np.argmin(np.abs(ev-t1)))
    return L,ev,i0,i1

def metric_rank1(L,pairs,cen,rad,NQ=256):
    # pairs: list of (row_index p, col_index q, coefficient) giving V = coeff * E_{p,q}
    n=L.shape[0]; I=np.eye(n,dtype=complex); k=len(pairs)
    P=np.zeros((n,n),complex); dP=np.zeros((k,n,n),complex)
    for t in range(NQ):
        th=2*np.pi*t/NQ; z=cen+rad*np.exp(1j*th); dz=1j*rad*np.exp(1j*th)*(2*np.pi/NQ)
        Rz=np.linalg.solve(z*I-L,I); P+=Rz*dz
        for idx,(p,q,cf) in enumerate(pairs):
            dP[idx]+=(cf*dz)*np.outer(Rz[:,p],Rz[q,:])
    P/=(2j*np.pi); dP/=(2j*np.pi)
    F=dP.reshape(k,-1); Ft=dP.transpose(0,2,1).reshape(k,-1)
    g=np.real(0.5*(F@Ft.T)); g=0.5*(g+g.T)
    return g,np.real(np.trace(P))

def inert(g,tol=1e-10):
    e=np.linalg.eigvalsh(g); sc=np.max(np.abs(e))
    return int(np.sum(e>tol*sc)),int(np.sum(e<-tol*sc)),e

BAR='='*100
print(BAR); print('INERTIA-05'); print(BAR)

# ---------------- C0 positive control ----------------
print('')
print('C0  POSITIVE CONTROL -- self-adjoint generator, metric must be PSD')
n=97
d=np.arange(n)*0.0
Hh=np.diag(2.0*np.ones(n))+np.diag(-1.0*np.ones(n-1),1)+np.diag(-1.0*np.ones(n-1),-1)
xh=np.linspace(-1,1,n); Hh=Hh+np.diag(3.0*xh**2)
Hh=Hh.astype(complex)
evh=np.linalg.eigvalsh(Hh.real)
cen=0.5*(evh[0]+evh[1]); rad=0.7*abs(evh[0]-evh[1])
pairs=[(j,j,1.0) for j in range(n)]
gh,trh=metric_rank1(Hh,pairs,cen,rad)
p,ng,e=inert(gh)
print('    Tr P = %.9f   inertia (%d,%d,%d)'%(trh,p,ng,n-p-ng))
print('    most negative eigenvalue %+.3e   most positive %+.3e   ratio %.2e'
      %(e[0],e[-1],abs(e[0])/e[-1]))
if ng>0:
    print('    CONTROL FAILED -- everything below is void'); raise SystemExit
print('    control passes: no negative direction above 1e-10 of the top')

# ---------------- C1/C2 full perturbation space ----------------
N=96; m=N+1; nn=2*m
pairs_pot=[(m+j,j,-1j) for j in range(m)]
pairs_dmp=[(m+j,m+j,+1j) for j in range(m)]
print('')
print('C1/C2  FULL PERTURBATION SPACE (%d potential + %d damping = %d directions)'
      %(m,m,nn))
print('    %5s %5s %6s | %-16s | %-16s'%('V0','s','a','potential only','potential+damping'))
for (V0,s) in [(1.40,0.50),(2.00,0.50),(0.80,0.50),(1.40,0.60)]:
    for a in [0.0,0.40]:
        L,ev,i0,i1=track(N,V0,s,a)
        cen=0.5*(ev[i0]+ev[i1]); gp=abs(ev[i0]-ev[i1])
        g1,tr1=metric_rank1(L,pairs_pot,cen,0.70*gp)
        p1,n1,_=inert(g1)
        g2,tr2=metric_rank1(L,pairs_pot+pairs_dmp,cen,0.70*gp)
        p2,n2,e2=inert(g2)
        print('    %5.2f %5.2f %6.3f | (%3d,%3d,%3d)    | (%3d,%3d,%3d)   TrP %.6f'
              %(V0,s,a,p1,n1,m-p1-n1,p2,n2,nn-p2-n2,tr2))

print('')
print('TOLERANCE LADDER on the full 194-direction metric, V0=1.40 s=0.50 a=0')
L,ev,i0,i1=track(N,1.40,0.50,0.0)
cen=0.5*(ev[i0]+ev[i1]); gp=abs(ev[i0]-ev[i1])
gF,trF=metric_rank1(L,pairs_pot+pairs_dmp,cen,0.70*gp)
line=[]
for tol in [1e-6,1e-8,1e-10,1e-12,1e-14]:
    p,q,_=inert(gF,tol); line.append('%.0e:(%d,%d)'%(tol,p,q))
print('    '+'   '.join(line))
e=np.linalg.eigvalsh(gF)
print('    most negative: '+'  '.join('%+.3e'%v for v in e[:4]))
print('    most positive: '+'  '.join('%+.3e'%v for v in e[-4:]))

print('')
print('RESTRICTION CENSUS on the full space')
rng=np.random.default_rng(11)
p,q,_=inert(gF)
print('    full-space inertia (%d,%d,%d)'%(p,q,nn-p-q))
for k in [2,3,5,10]:
    T=400; dfi=0
    for _ in range(T):
        Q=rng.standard_normal((nn,k)); gr=Q.T@gF@Q
        er=np.linalg.eigvalsh(0.5*(gr+gr.T))
        if np.all(er>0) or np.all(er<0): dfi+=1
    print('    k = %2d : %5.1f%% of random k-planes read as DEFINITE'%(k,100.0*dfi/T))
print(BAR)
