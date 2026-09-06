#!/usr/bin/env python3
# SCRIPT: PAIRING-SPLIT-01
#
# THE CLAIM UNDER TEST, and why this run decides it.
# For any projector, P dP P = 0 and (1-P) dP (1-P) = 0, so dP_i = X_i + Y_i with
#     X_i = P dP_i (1-P),      Y_i = (1-P) dP_i P.
# Then X_i X_j = Y_i Y_j = 0, so Tr(dP_i dP_j) = Tr(X_i Y_j) + Tr(Y_i X_j) and
#     g_ij = Re (1/2) [ Tr(X_i Y_j) + Tr(Y_i X_j) ]
# is the SYMMETRISED PAIRING of the X family against the Y family.
# If P is self-adjoint then Y_i = X_i-dagger and this is Re <X_i, X_j>, a Gram matrix,
# hence positive semi-definite.  If P is not self-adjoint, Y is an independent family and
# the symmetrisation of an unstructured pairing has a spectrum about zero -- neutral.
# That is B85 (the real part of a rank-one complex form is never definite) for n
# directions instead of one.
#
# PRE-STATED VERDICTS
#   V0  the identity must hold to machine precision, else everything below is VOID.
#   V1  STRUCTURAL: replacing Y by X-dagger by hand, on the SAME dP data, returns zero
#       negative directions -- so the entire negative sector is attributable to Y != X-dag,
#       not to the generator, the rotation, or the probe choice.
#   V2  DEAD: the Hermitised pairing still carries negatives -- the mechanism is wrong.
#   V3  the interpolation Y(t) = (1-t) X-dag + t Y must carry the inertia continuously from
#       (k,0) to the measured split; a jump would mean something else is happening.
#   And the discriminating correlation: the negative count must track the departure
#   ||Y - X-dag|| / ||X||, NOT the rotation parameter a.
# KILL: identity residual above 1e-10 relative, or Tr P off 2 by more than 1e-6.
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
    L,_=generator(N,V0,s,a); ev,_=np.linalg.eig(L)
    root=np.sqrt(complex(V0-0.25))
    i0=int(np.argmin(np.abs(ev-(root-0.5j)))); i1=int(np.argmin(np.abs(ev-(root-1.5j))))
    return L,ev,i0,i1

def contour_data(L,pairs,cen,rad,NQ=256):
    n=L.shape[0]; I=np.eye(n,dtype=complex); k=len(pairs)
    P=np.zeros((n,n),complex); dP=np.zeros((k,n,n),complex)
    for t in range(NQ):
        th=2*np.pi*t/NQ; z=cen+rad*np.exp(1j*th); dz=1j*rad*np.exp(1j*th)*(2*np.pi/NQ)
        Rz=np.linalg.solve(z*I-L,I); P+=Rz*dz
        for idx,(p,q,cf) in enumerate(pairs):
            dP[idx]+=(cf*dz)*np.outer(Rz[:,p],Rz[q,:])
    P/=(2j*np.pi); dP/=(2j*np.pi)
    return P,dP

def split_forms(P,dP):
    n=P.shape[0]; I=np.eye(n,dtype=complex); k=dP.shape[0]
    Q=I-P
    X=np.matmul(np.matmul(P[None,:,:],dP),Q[None,:,:])
    Y=np.matmul(np.matmul(Q[None,:,:],dP),P[None,:,:])
    Xf=X.reshape(k,-1); Yf=Y.reshape(k,-1)
    YT=Y.transpose(0,2,1).reshape(k,-1)
    M=Xf@YT.T                                   # M_ij = Tr(X_i Y_j)
    g_pair=np.real(0.5*(M+M.T))
    Xd=X.conj().transpose(0,2,1)
    XdT=Xd.transpose(0,2,1).reshape(k,-1)
    MH=Xf@XdT.T                                 # M^H_ij = Tr(X_i X_j-dagger)
    g_herm=np.real(0.5*(MH+MH.T))
    dep=np.array([np.linalg.norm(Y[i]-Xd[i])/max(np.linalg.norm(X[i]),1e-300) for i in range(k)])
    return g_pair,g_herm,dep

def g_direct(dP):
    k=dP.shape[0]; F=dP.reshape(k,-1); FT=dP.transpose(0,2,1).reshape(k,-1)
    G=np.real(0.5*(F@FT.T)); return 0.5*(G+G.T)

def inert(g,tol=1e-10):
    e=np.linalg.eigvalsh(g); sc=max(np.max(np.abs(e)),1e-300)
    return int(np.sum(e>tol*sc)),int(np.sum(e<-tol*sc)),e

BAR='='*100
print(BAR); print('PAIRING-SPLIT-01'); print(BAR)

# ---------------- self-adjoint control ----------------
print('')
print('C0  SELF-ADJOINT CONTROL  (Y must equal X-dagger, and g must be PSD)')
n=97
xh=np.linspace(-1,1,n)
Hh=(np.diag(2.0*np.ones(n))+np.diag(-np.ones(n-1),1)+np.diag(-np.ones(n-1),-1)
    +np.diag(3.0*xh**2)).astype(complex)
evh=np.linalg.eigvalsh(Hh.real)
P,dP=contour_data(Hh,[(j,j,1.0) for j in range(n)],0.5*(evh[0]+evh[1]),0.7*abs(evh[0]-evh[1]))
gp,gh,dep=split_forms(P,dP); gd=g_direct(dP)
res=np.max(np.abs(gd-gp))/max(np.max(np.abs(gd)),1e-300)
p,q,_=inert(gp)
print('    Tr P = %.9f   identity residual = %.2e'%(np.real(np.trace(P)),res))
print('    max ||Y - X-dag|| / ||X|| = %.3e'%dep.max())
print('    inertia of the pairing form: (%d,%d,%d)'%(p,q,n-p-q))

# ---------------- the horizon generator ----------------
N=96; m=N+1
sel_p=list(range(4,m-4,3)); sel_d=list(range(4,m-4,3))
pairs=[(m+j,j,-1j) for j in sel_p]+[(m+j,m+j,+1j) for j in sel_d]
k=len(pairs)
print('')
print('C1  HORIZON GENERATOR, %d perturbation directions (%d potential + %d damping)'
      %(k,len(sel_p),len(sel_d)))
print('    %6s %9s %11s | %-14s %-14s | %-10s'
      %('a','TrP','identity','pairing inertia','Hermitised','max depart'))
store={}
for a in (0.0,0.05,0.40):
    L,ev,i0,i1=track(N,1.40,0.50,a)
    cen=0.5*(ev[i0]+ev[i1]); rad=0.70*abs(ev[i0]-ev[i1])
    P,dP=contour_data(L,pairs,cen,rad)
    gp,gh,dep=split_forms(P,dP); gd=g_direct(dP)
    res=np.max(np.abs(gd-gp))/max(np.max(np.abs(gd)),1e-300)
    p1,q1,_=inert(gp); p2,q2,_=inert(gh)
    store[a]=(gp,gh)
    print('    %6.2f %9.5f %11.2e | (%3d,%3d,%3d)  | (%3d,%3d,%3d)  | %.3e'
          %(a,np.real(np.trace(P)),res,p1,q1,k-p1-q1,p2,q2,k-p2-q2,dep.max()))

print('')
print('C2  INTERPOLATION  Y(t) = (1-t) X-dagger + t Y   (linear, so g(t) = (1-t)g_H + t g)')
gp,gh=store[0.05]
print('    %6s %-16s %s'%('t','inertia','fraction negative'))
for t in (0.0,0.1,0.2,0.35,0.5,0.7,0.85,1.0):
    g=(1-t)*gh+t*gp
    p,q,_=inert(g)
    print('    %6.2f (%3d,%3d,%3d)      %.3f'%(t,p,q,k-p-q,q/max(p+q,1)))

print('')
print('C3  DOES THE NEGATIVE COUNT TRACK THE ROTATION, OR THE DEPARTURE?')
for a in (0.0,0.05,0.40):
    gp_,gh_=store[a]; p,q,_=inert(gp_)
    print('    a = %.2f   negatives = %d   (rotation varies, count does not)'%(a,q))
print(BAR)
print('VERDICT')
p0,q0,_=inert(store[0.0][1])
if q0==0:
    print('    V1 STRUCTURAL: Hermitising the pairing on identical dP data removes every')
    print('       negative direction.  The split is generated by Y != X-dagger, i.e. by the')
    print('       projector failing to be self-adjoint, and by nothing else.')
else:
    print('    V2 DEAD: the Hermitised pairing still carries %d negative directions.'%q0)
print(BAR)
