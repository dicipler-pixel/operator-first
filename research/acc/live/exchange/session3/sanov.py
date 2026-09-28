# SCRIPT: ACC_SANOV_SMITH  faithful per-line Smith eye: x->[[1,2],[0,1]], y->[[1,0],[2,1]] (Sanov, free in SL2(Z))
# distance of line r from its vacuum letter g: arccosh(||rho(g)^-1 rho(r)||^2/2); zero iff r == g as words. Exact ints.
import math
def mul(A,B): return (A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3],-A[1],-A[2],A[0])
X=(1,2,0,1); Y=(1,0,2,1); L={1:X,-1:inv(X),2:Y,-2:inv(Y)}
def rho(w):
    M=(1,0,0,1)
    for c in w: M=mul(M,L[c])
    return M
def sd(w,g):
    M=mul(inv(L[g]),rho(w)); n2=sum(v*v for v in M)
    return math.log(n2) if n2>2 else 0.0   # arccosh(n2/2) ~ log(n2) for large n2; exact 0 at identity
