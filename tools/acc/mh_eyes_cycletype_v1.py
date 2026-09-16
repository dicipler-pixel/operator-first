"""CYCLE_TYPE eye — from paper_v2 Theorem 8 (displacement Gram = cycle Laplacian).

    Gram(v_i, v_j) with v_i = (e_{pi(i)} - e_i)/sqrt(2)  equals  (1/2) L,
    L the graph Laplacian of the permutation's cycle graph; its spectrum is
    {2 sin^2(pi j / l)} over cycles of length l, so the spectrum reads the
    cycle type.

AC application: SL2(F_p) acts on the projective line P^1(F_p), which has p+1
points, so rho(r0) and rho(r1) ARE permutations of p+1 points. Cycle type is
a CONJUGACY INVARIANT, therefore invariant under all eight conjugation moves
6-13 -- half the move set. No other eye here has that property.

Additive; mh_eyes_v1.py and mh_eyes_master_v1.py unchanged.
Status labels per the RTOE Master Index.

CALIBRATION — PASSED, and it is the first new eye this session that does
-------------------------------------------------------------------------
INVARIANCE [PROVED + V]: cycle type is a conjugacy invariant and
rho(g r g^-1) = rho(g) rho(r) rho(g)^-1, so all eight conjugation moves 6-13
preserve it. Verified empirically: 24 conjugation moves across G6, R6, R7,
zero signature changes.

SEPARATION at step 0 [COMPUTED]: Gordon reads r0 = (5,1) at p=5 and (7,1) at
p=7; R6/R7 read r0 = (1,1,1,1,1,1) and (1,1,1,1,1,1,1,1), the identity
permutation. This is NOT new -- it restates the donor-kernel lemma, since
rho(r0) = I for the R family, and the plain kernel test is conjugation-
invariant too. Do not claim it as a separate discriminator.

REFINEMENT along a path [MEASURED] -- this is the new content. On the
verified Gordon q=6 path the binary kernel test fires ZERO times, because
rho(r0) is never the identity there, so it is constant-False for all 17
steps and carries no information. The cycle type fires SEVEN times:

    r0: (5,1) -> (2,2,1,1) at step 12 -> (5,1) at 15 -> (3,3) at 17
    r1: (5,1) -> (2,2,1,1) at step 5  -> (5,1) at 7  -> (3,3) at 14 -> (5,1) at 16

So the conjugacy class is strictly finer than in-or-out of the kernel, and
the extra transitions are exactly where the path does structural work.

CAVEAT [MEASURED]: the r1 reading is periodic in q. X has order 6 in
SL2(F_5), so r1's class depends on q mod 6 -- q=6,9 give (5,1) while
q=7,8,10 give (3,3). That is arithmetic of the representation, not
difficulty, and must not be read as a hardness signal.
"""
import sys
from collections import Counter
sys.path.insert(0,'/home/user/saircompetition/andrews-curtis/competition/tools')
from verifier import core

def sl2_mul(A,B,p): return ((A[0]*B[0]+A[1]*B[2])%p,(A[0]*B[1]+A[1]*B[3])%p,
                            (A[2]*B[0]+A[3]*B[2])%p,(A[2]*B[1]+A[3]*B[3])%p)
def sl2_inv(A,p):
    d=(A[0]*A[3]-A[1]*A[2])%p; di=pow(d,-1,p)
    return ((A[3]*di)%p,(-A[1]*di)%p,(-A[2]*di)%p,(A[0]*di)%p)

def projective_line(p):
    """P^1(F_p) as p+1 normalised points."""
    return [(1,0)]+[(t,1) for t in range(p)]

def act(A,pt,p):
    x,y=pt; nx=(A[0]*x+A[1]*y)%p; ny=(A[2]*x+A[3]*y)%p
    if ny==0: return (1,0)
    return ((nx*pow(ny,-1,p))%p, 1)

def perm_of(A,p):
    P=projective_line(p); idx={q:i for i,q in enumerate(P)}
    return tuple(idx[act(A,q,p)] for q in P)

def cycle_type(perm):
    n=len(perm); seen=[False]*n; cyc=[]
    for i in range(n):
        if seen[i]: continue
        l=0; j=i
        while not seen[j]: seen[j]=True; j=perm[j]; l+=1
        cyc.append(l)
    return tuple(sorted(cyc,reverse=True))

def word_image(w,p,X,Y):
    M=(1,0,0,1)
    Xi,Yi=sl2_inv(X,p),sl2_inv(Y,p)
    for c in w:
        M=sl2_mul(M,{1:X,-1:Xi,2:Y,-2:Yi}[c],p)
    return M

def eye_cycle_type(state,p=5,
                   X=(0,-1,1,1),Y=(-1,0,1,-1)):
    """CYCLE_TYPE  [COMPUTED]

    Cycle type of each relator's image permutation on P^1(F_p).
    One question: what is the conjugacy class of each relator's image.
    Invariant under moves 6-13 by construction.
    """
    Xp=tuple(c%p for c in X); Yp=tuple(c%p for c in Y)
    out=[]
    for w in state:
        M=word_image(list(w),p,Xp,Yp)
        out.append(cycle_type(perm_of(M,p)))
    return {"status":"COMPUTED","p":p,"r0":out[0],"r1":out[1],
            "signature":tuple(sorted(out))}
