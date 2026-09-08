"""Guarded finite UPG diagnostics. No atomic or spacetime identification is inferred."""
import numpy as np
from scipy.linalg import expm

def blocked(s): return {'_status':'blocked','reason':s}
def mat(x):
    if isinstance(x,dict): return np.asarray(x['real'],float)+1j*np.asarray(x['imag'],float)
    return np.asarray(x,complex)
def enc(x): return {'real':x.real.tolist(),'imag':x.imag.tolist()}
def square(x): return x.ndim==2 and x.shape[0]==x.shape[1] and len(x)>0 and np.isfinite(x).all()
def herm(x): return square(x) and np.linalg.norm(x-x.conj().T)<1e-9
def orth(p): return herm(p) and np.linalg.norm(p@p-p)<1e-9
def norm(x): return float(np.linalg.norm(x))
def positive(x): return herm(x) and np.linalg.eigvalsh(x).min()>1e-10

def redistribution_memory(i,*_):
    c=i['case'];H=mat(c['H']);P=mat(c['P'])
    if not herm(H) or not orth(P) or H.shape!=P.shape:
        return blocked('This equivalence requires a finite Hermitian H and matching orthogonal P.')
    Q=np.eye(len(P))-P;B=P@H@Q;D=Q@H@Q;F=B+B.conj().T;K0=B@B.conj().T
    times=np.asarray(c.get('times',[0,1,2]),float)
    if times.ndim!=1 or not np.isfinite(times).all() or np.any(times<0):
        return blocked('Finite nonnegative times required.')
    return {'redistribution_norm':norm(F),'commutator_norm':norm(H@P-P@H),
            'K0':enc(K0),'identity_residual':abs(norm(F)**2-2*np.trace(K0).real),
            'K0_min_eigenvalue':float(np.linalg.eigvalsh(K0).min()),
            'feedback_numerically_zero':bool(norm(B)<1e-10),
            'trajectory':[{'time':float(t),'kernel':enc(B@expm(-1j*t*D)@B.conj().T)} for t in times],
            'scope':'H fixed, hbar=1, orthogonal retained/hidden split. K(t)=B exp(-itD) B*. The reduced derivative contains -integral K(t-s)x(s)ds and a separate initial hidden forcing. Nonzero K is elimination memory, not a CP-divisibility witness or extracted work.'}

def spectral_susceptibility(i,*_):
    c=i['case'];H=mat(c['H']);V=mat(c['Hdot']);k=c['rank'];tol=float(c.get('gap_tolerance',1e-8))
    if not herm(H) or not herm(V) or H.shape!=V.shape or not isinstance(k,int) or not 0<k<len(H) or not np.isfinite(tol) or tol<=0:
        return blocked('Matching finite Hermitian H and Hdot, interior integer rank and positive gap tolerance required.')
    e,U=np.linalg.eigh(H);gap=float(e[k]-e[k-1])
    if gap<=tol: return blocked('Selected cluster touches its complement; the projector derivative is not certified here.')
    P=U[:,:k]@U[:,:k].conj().T;v=U.conj().T@V@U;dp=np.zeros_like(v)
    for a in range(k):
        for b in range(k,len(H)):
            dp[a,b]=v[a,b]/(e[a]-e[b]);dp[b,a]=dp[a,b].conjugate()
    dP=U@dp@U.conj().T;Q=np.eye(len(H))-P;F=Q@V@P+P@V@Q
    return {'cluster_gap':gap,'smallest_absolute_eigenvalue':float(abs(e).min()),'projector':enc(P),'projector_derivative':enc(dP),
            'metric_speed':float(np.trace(dP@dP).real/2),'redistribution_norm':norm(F),
            'sylvester_residual':norm(H@dP-dP@H-(P@V-V@P)),
            'scope':'Lowest k eigenvalues of a differentiable Hermitian family. Closing an eigenvalue at zero is different from closing the selected cluster gap. Metric speed is not thermodynamic friction without a response model.'}

def gluing_sign(i,*_):
    c=i['case'];A=mat(c['A']);D=mat(c['D']);B=mat(c['B'])
    if not positive(A) or not positive(D) or B.shape!=(len(A),len(D)) or not np.isfinite(B).all():
        return blocked('Positive definite diagonal blocks and a compatible finite coupling required.')
    M=np.block([[A,B],[B.conj().T,D]]);S=D-B.conj().T@np.linalg.solve(A,B)
    if not positive(S): return blocked('Full Hermitian block is not positive definite; real positive trace-log gluing is inapplicable.')
    ld=lambda x:float(np.log(np.linalg.eigvalsh(x)).sum())
    delta=ld(M)-ld(A)-ld(D);schur=ld(S)-ld(D)
    return {'interface_logdet_correction':delta,'schur_correction':schur,'identity_residual':abs(delta-schur),
            'nonpositive_with_tolerance':bool(delta<=1e-9),
            'scope':'For [[A,B],[B*,D]]>0 the logdet correction is nonpositive, strictly negative when B is nonzero. A positive correction belongs to another functional/sign convention, not this displayed block.'}

def nct_anchor(i,*_):
    c=i['case'];U=mat(c['U']);V=mat(c['V']);tau=float(c.get('branch_tolerance',1e-7))
    if not square(U) or not square(V) or U.shape!=V.shape or not np.isfinite(tau) or tau<=0:
        return blocked('Matching finite square unitaries and positive branch tolerance required.')
    I=np.eye(len(U))
    if max(norm(U.conj().T@U-I),norm(V.conj().T@V-I))>1e-8:
        return blocked('Unitary input required; compressed position operators need a separately validated unitarization.')
    R=U@V@U.conj().T@V.conj().T;lam=np.linalg.eigvals(R);g=float(abs(lam+1).min());delta=norm(R-I)**2/len(U)
    if g<=tau: return blocked('Relator touches the principal-log branch guard; no integer assigned.')
    w=float(np.angle(lam).sum()/(2*np.pi))
    return {'winding':int(round(w)),'integer_residual':abs(w-round(w)),'defect':delta,'branch_guard':g,
            'domain_sum':delta+g*g,'amplitude_bound':len(U)*np.sqrt(delta)/4,
            'scope':'Finite commutator winding/Bott convention of UPG. Not the APS eta invariant, not automatically a measured Chern number; norm and branch guard are explicit.'}

def signature_flow(i,*_):
    c=i['case'];S=mat(c['seifert']);angles=np.asarray(c['angles'],float);tol=float(c.get('wall_tolerance',1e-8))
    if not square(S) or norm(S.imag)>1e-10 or not np.allclose(S.real,np.round(S.real),atol=1e-10,rtol=0) or len(S)%2 or angles.ndim!=1 or not np.isfinite(angles).all() or not np.isfinite(tol) or tol<=0:
        return blocked('Even-dimensional integer Seifert matrix, finite angles and positive tolerance required.')
    if abs(abs(np.linalg.det(S-S.T))-1)>1e-8:
        return blocked('Knot Seifert-form skew part must be unimodular; a diagram-to-matrix certificate is still separate.')
    rows=[]
    for t in angles:
        z=np.exp(1j*t);K=(1-z)*S+(1-z.conjugate())*S.T;e=np.linalg.eigvalsh(K)
        wall=bool(abs(e).min()<=tol)
        rows.append({'angle':float(t),'signature':int((e>tol).sum()-(e< -tol).sum()),'nullity':int((abs(e)<=tol).sum()),
                     'wall_or_basepoint':wall,'regular_plateau':not wall,'alexander_determinant_modulus':float(abs(np.linalg.det(z*S-S.T)))})
    return {'samples':rows,'scope':'Levine-Tristram signature with fixed Seifert convention. Signature at a wall ignores numerically zero modes and is not a regular plateau. Alexander roots permit but need not cause jumps. No eta/CS or colored-Jones identification is made.'}
