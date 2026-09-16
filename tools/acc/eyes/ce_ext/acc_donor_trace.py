"""ACC eye: donor-kernel diagnostic (REPORT_ACC section 4).

Over the integers, X=[[0,-1],[1,1]], Z=[[0,-1],[1,0]], Y=XZ=[[-1,0],[1,-1]];
X^3=Z^2=-I. For the family root R_n=(r,s_n) with r=x^2 y x^-1 y we have rho(r)=I,
and trace rho(s_n) = -n(n+1)-2.

Donor-kernel lemma: if the first relator stays in ker rho along an ordinary AC
path, the second relator's trace is constant. A parameter-changing bridge
R_n -> R_m with n != m therefore cannot remain in that restricted lane; it must
leave and re-enter the kernel, costing at least two first-slot multiplications.
The lemma constrains that lane only. It does not bound a full solve ending at (x,y),
and the legal two-move control [2,4] sends trace t -> t^2-2, which refutes reading
it as an unrestricted AC invariant.

Telemetry only.
"""
def _mul(A,B):
    return (A[0]*B[0]+A[1]*B[2],A[0]*B[1]+A[1]*B[3],
            A[2]*B[0]+A[3]*B[2],A[2]*B[1]+A[3]*B[3])
def _inv(A):
    a,b,c,d=A; det=a*d-b*c
    if det not in (1,-1): raise ValueError('Non-unimodular image.')
    s=det
    return (d//s,-b//s,-c//s,a//s)
_X=(0,-1,1,1); _Z=(0,-1,1,0)
_Y=_mul(_X,_Z)
_L=[_X,_inv(_X),_Y,_inv(_Y)]
def _rho(w):
    M=(1,0,0,1)
    for c in w: M=_mul(M,_L[c])
    return M
def run(inputs,context,dependencies,spec,runtime):
    r0=inputs['relator_0']; r1=inputs['relator_1']
    A=_rho(r0); B=_rho(r1)
    I=(1,0,0,1); mI=(-1,0,0,-1)
    in_kernel = A in (I,mI)
    tr=B[0]+B[3]
    n_implied=None
    # trace = -n(n+1)-2  =>  n^2+n+(tr+2)=0
    disc=1-4*(tr+2)
    if disc>=0:
        r=int(round(disc**0.5))
        if r*r==disc and (-1+r)%2==0:
            cand=(-1+r)//2
            if -cand*(cand+1)-2==tr: n_implied=cand
    return {'rho_r0':list(A),'rho_r1':list(B),
            'first_relator_in_donor_kernel':in_kernel,
            'second_trace':tr,
            'implied_family_parameter_n':n_implied,
            'lemma':'if r0 stays in ker rho, second trace is constant; a bridge to a '
                    'different n needs >=2 first-slot multiplications',
            'scope':'restricted lane only; [2,4] sends t -> t^2-2',
            'certifies':None}
