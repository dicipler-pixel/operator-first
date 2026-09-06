# SCRIPT: PAIRING-SPLIT-02   diagnose the jump in C2
# g(t) = (1-t) g_H + t g_pair is linear in t, so if ||g_H|| >> ||g_pair|| the Hermitised
# term dominates until t is within a whisker of 1 and the count appears to jump.  That
# would be a parameterisation artefact, not a discontinuity.  Two things settle it: the
# norm ratio, and the same homotopy run with both endpoints normalised to unit norm.
import numpy as np
exec(open('PAIRING-SPLIT-01.py').read().split("BAR='='*100")[0].split('import numpy as np')[1])

N=96; m=N+1
sel=list(range(4,m-4,3))
pairs=[(m+j,j,-1j) for j in sel]+[(m+j,m+j,+1j) for j in sel]
k=len(pairs)
L,ev,i0,i1=track(N,1.40,0.50,0.05)
cen=0.5*(ev[i0]+ev[i1]); rad=0.70*abs(ev[i0]-ev[i1])
P,dP=contour_data(L,pairs,cen,rad)
gp,gh,dep=split_forms(P,dP)
np.save('gp.npy',gp); np.save('gh.npy',gh)
nh=np.linalg.norm(gh); ng=np.linalg.norm(gp)
print('||g_Hermitised||  = %.6e'%nh)
print('||g_pairing||     = %.6e'%ng)
print('ratio             = %.3e'%(nh/ng))
print('departure ||Y-Xdag||/||X||: min %.3f  median %.3f  max %.3f'
      %(dep.min(),np.median(dep),dep.max()))
print('')
print('A  raw homotopy, fine grid near t = 1')
for t in (0.9,0.99,0.999,0.9999,0.99999,0.999999,1.0):
    g=(1-t)*gh+t*gp; p,q,_=inert(g)
    print('   t = %.6f   (%3d,%3d,%3d)'%(t,p,q,k-p-q))
print('')
print('B  norm-matched homotopy (both endpoints scaled to unit Frobenius norm)')
GH=gh/nh; GP=gp/ng
for t in (0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0):
    g=(1-t)*GH+t*GP; p,q,_=inert(g)
    print('   t = %.2f   (%3d,%3d,%3d)   fraction negative %.3f'%(t,p,q,k-p-q,q/max(p+q,1)))
