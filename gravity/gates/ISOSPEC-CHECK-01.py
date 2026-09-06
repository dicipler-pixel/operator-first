#!/usr/bin/env python3
# SCRIPT: ISOSPEC-CHECK-01
# WHY THIS IS THE RIGHT CHECK.  Sec 5.3 asserts that the advection L2 -> L2 + a D cannot
# be symmetric under the pairing that makes the undeformed operator symmetric.  The audit
# memo asserts the same thing without measuring it.  A similarity L(a) = S L(0) S^-1
# preserves the spectrum EXACTLY, hence every trace power Tr[L(a)^k].  So:
#   traces MOVE  -> the deformation is not a similarity, and Result 15 is safe.
#   traces FROZEN -> a necessary condition for the gauge reading is satisfied; it does not
#                    prove gauge equivalence, but the paper's assertion is then untested
#                    and must be fenced.
# Trace powers need no eigendecomposition, so this does not depend on the eigenvector
# conditioning the paper itself calls hopeless.
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
    return 1j*np.block([[Z,I],[L1,s*L2]])

N=96; V0,s=1.0,1.0
D,_=cheb(N)
print('Tr of the Chebyshev first-derivative matrix D : %.6e'%np.trace(D))
print('(if this is zero, Tr L is blind to a by construction and carries no information)')
print()
L0=generator(N,V0,s,0.0)
base=[np.trace(np.linalg.matrix_power(L0,k)) for k in (1,2,3,4)]
print('ISOSPEC-CHECK-01   trace powers of the paper rotating generator, V0=1.0 s=1.0')
print('   %8s | %12s %12s %12s %12s'%('a','|dTr L|','|dTr L^2|','|dTr L^3|','|dTr L^4|'))
for a in (1e-4,1e-3,1e-2,1e-1,0.4,0.8):
    La=generator(N,V0,s,a)
    d=[abs(np.trace(np.linalg.matrix_power(La,k))-base[k-1]) for k in (1,2,3,4)]
    rel=[d[k-1]/max(abs(base[k-1]),1e-300) for k in (1,2,3,4)]
    print('   %8.4g | %12.2e %12.2e %12.2e %12.2e'%(a,*d))
print()
print('   relative to the a=0 values: |Tr L^k| = %s'%['%.3e'%abs(b) for b in base])
print()
print('spectrum movement, tracked overtones (closed form w_n = sqrt(V0-1/4) - i(n+1/2))')
root=np.sqrt(complex(V0-0.25))
targets=[root-0.5j*(2*n+1) for n in range(4)]
ev0=np.linalg.eigvals(L0)
seeds=[ev0[int(np.argmin(np.abs(ev0-t)))] for t in targets]
res0=[abs(seeds[n]-targets[n]) for n in range(4)]
print('   overtone   residual at a=0     max |dw| over a in [1e-4, 0.4]')
mx=[0.0]*4
for a in (1e-4,1e-3,1e-2,1e-1,0.2,0.4):
    ev=np.linalg.eigvals(generator(N,V0,s,a))
    for n in range(4):
        w=ev[int(np.argmin(np.abs(ev-seeds[n])))]
        mx[n]=max(mx[n],abs(w-seeds[n]))
for n in range(4):
    print('   n=%d        %.2e            %.2e'%(n,res0[n],mx[n]))
