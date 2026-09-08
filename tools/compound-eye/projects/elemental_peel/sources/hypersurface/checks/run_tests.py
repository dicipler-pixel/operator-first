#!/usr/bin/env python3
"""Independent finite and continuum-model tests of boundary light/electron ideas.

Models are specified in proof_note.md. No experimental data or gravitational field
is fitted. No result of this program is a Lean kernel certificate.
Requires Python 3.10+, numpy, scipy, sympy. Output is written beside this script.
"""
from __future__ import annotations
import json, platform, time
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss
import sympy as sp

OUT=Path(__file__).resolve().parent
RNG=np.random.default_rng(20260905)
REPORT={"seed":20260905,"models_are_not_experiments":True,"lean_certification":False,
        "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
        "sympy":sp.__version__,"checks":[],"sections":{}}

def check(name: str, ok: bool, value=None):
    REPORT["checks"].append({"name":name,"passed":bool(ok),"value":value})
    if not ok:
        write_report()
        raise AssertionError(f"{name}: {value}")

def write_report():
    REPORT['assertions']=len(REPORT['checks'])
    REPORT['passed']=sum(x['passed'] for x in REPORT['checks'])
    (OUT/'results.json').write_text(json.dumps(REPORT,indent=2),encoding='utf-8')

def rel(A,B):
    return float(np.linalg.norm(A-B)/max(1.,np.linalg.norm(B)))

def cmat(n,m):
    return RNG.normal(size=(n,m))+1j*RNG.normal(size=(n,m))

def unitary(n):
    q,r=np.linalg.qr(cmat(n,n)); return q

# 1. Symbolic photon-ray geometry (fixed positive C^3 inner product).
th,ph=sp.symbols('theta phi',real=True)
e_th=sp.Matrix([sp.cos(th)*sp.cos(ph),sp.cos(th)*sp.sin(ph),-sp.sin(th)])
e_ph=sp.Matrix([-sp.sin(ph),sp.cos(ph),0])
photon=[]
for helicity in [-1,1]:
    u=(e_th+sp.I*helicity*e_ph)/sp.sqrt(2)
    P=u*u.conjugate().T
    du=[u.diff(th),u.diff(ph)]
    Q=sp.Matrix(2,2,lambda i,j:sp.trigsimp((du[i].conjugate().T*(sp.eye(3)-P)*du[j])[0]))
    g=Q.applyfunc(lambda q:sp.simplify(sp.re(q)))
    omega=sp.simplify(-2*sp.im(Q[0,1])) # convention +i Tr(P[dP,dP])
    expected=sp.diag(sp.Rational(1,2),sp.sin(th)**2/2)
    check(f'photon_metric_helicity_{helicity}',(g-expected).applyfunc(sp.simplify)==sp.zeros(2))
    check(f'photon_curvature_helicity_{helicity}',sp.simplify(omega+helicity*sp.sin(th))==0)
    check(f'photon_metric_curvature_saturation_{helicity}',sp.simplify(4*g.det()-omega**2)==0)
    photon.append({'helicity':helicity,'metric':str(g),'omega':str(omega)})
# Cyclic overlap product: this sign is the Bargmann-product convention, opposite
# to the convention gamma = i integral <u|du>. Compare complex phases, not arguments.
def polar(theta,phi,h=1):
    et=np.array([np.cos(theta)*np.cos(phi),np.cos(theta)*np.sin(phi),-np.sin(theta)])
    ep=np.array([-np.sin(phi),np.cos(phi),0.])
    return (et+1j*h*ep)/np.sqrt(2)
loop=[]
for n in [32,64,128,256,512]:
    theta=.7; states=np.array([polar(theta,2*np.pi*j/n) for j in range(n)])
    ovs=np.einsum('ij,ij->i',states.conj(),np.roll(states,-1,axis=0))
    hol=np.prod(ovs/abs(ovs))
    target=np.exp(1j*2*np.pi*(1-np.cos(theta)))
    gauges=np.exp(1j*RNG.normal(size=n)*4)
    ug=states*gauges[:,None]
    og=np.einsum('ij,ij->i',ug.conj(),np.roll(ug,-1,axis=0))
    hg=np.prod(og/abs(og))
    check(f'photon_loop_gauge_{n}',abs(hol-hg)<2e-13,float(abs(hol-hg)))
    loop.append({'nodes':n,'phase_product_error':float(abs(hol-target))})
check('photon_loop_converges_order_two',loop[-2]['phase_product_error']/loop[-1]['phase_product_error']>3.9)
REPORT['sections']['photon_geometry']={'symbolic':photon,'holonomy':loop}
print('PHOTON: metric diag(1/2,sin(theta)^2/2), helicity curvature sign, gauge-invariant holonomy PASS')

# 2. Scalar TE slab guide; all lengths in c/omega_ref, k0=omega=1 for this gate.
# Two identical, lossless local electric sheets at x=+-a; gsheet=k0^2 chi_s.
def slab(nout:float, gsheet:float, a:float=.8, ncore:float=1.5, k0:float=1.):
    if not (0<nout<ncore): raise ValueError('Require positive core contrast.')
    qmax=k0*np.sqrt(ncore*ncore-nout*nout)
    if not 0<=gsheet<qmax: raise ValueError('This gate uses the oscillatory-core branch.')
    hi=min(qmax*(1-1e-13),np.pi/(2*a)*(1-1e-13))
    f=lambda q:q*np.tan(q*a)+gsheet-np.sqrt(max(0,qmax*qmax-q*q))
    q=brentq(f,0.,hi,xtol=4e-15)
    beta=np.sqrt(k0*k0*ncore*ncore-q*q)
    kap=np.sqrt(beta*beta-k0*k0*nout*nout)
    cin=np.cos(q*a)
    inside=a+np.sin(2*q*a)/(2*q)
    outside=cin*cin/kap
    norm=inside+outside
    frac=outside/norm
    fb=-beta*(np.tan(q*a)/q+a/np.cos(q*a)**2+1/kap)
    return dict(nout=nout,gsheet=gsheet,beta=float(beta),q=float(q),kappa=float(kap),
                outside_fraction=float(frac),norm=float(norm),
                residual=float(f(q)),db_dn=float(-nout*k0*k0/kap/fb),
                db_dgs=float(-1/fb),a=a,ncore=ncore,k0=k0)

def profile(x,row):
    a=row['a']; q=row['q']; kap=row['kappa']
    return np.where(abs(x)<=a,np.cos(q*x),np.cos(q*a)*np.exp(-kap*(abs(x)-a)))/np.sqrt(row['norm'])

slabrows=[]
for no in [1.,1.2,1.4]:
    for theta in [0.,np.pi/4,np.pi/2]:
        # Delta=2, d=1, Ns/eps0=.3, omega=1 gives chi_s=.4 sin(theta)^2.
        gs=.4*np.sin(theta)**2
        r=slab(no,gs);r['electronic_rotation']=float(theta)
        check(f'slab_match_{no}_{theta}',abs(r['residual'])<1e-12,r['residual'])
        check(f'slab_order_{no}_{theta}',no<r['beta']<1.5)
        delta=2e-5
        der=(slab(no+delta,gs)['beta']-slab(no-delta,gs)['beta'])/(2*delta)
        hf=no/r['beta']*r['outside_fraction']
        check(f'slab_external_sensitivity_{no}_{theta}',abs(der-hf)<2e-8,float(abs(der-hf)))
        check(f'slab_implicit_vs_HF_{no}_{theta}',abs(r['db_dn']-hf)<1e-12)
        r['db_dn_finite_difference']=float(der);r['db_dn_HF']=float(hf)
        slabrows.append(r)
print('\nSLAB: n_core=1.5, halfwidth=.8, k0=1, sheet=.4 sin(theta)^2')
for r in slabrows:
    print(f" n_out={r['nout']:.1f} sheet={r['gsheet']:.3f} beta/k0={r['beta']:.12f} F_out={r['outside_fraction']:.12f}")
# Independent FD eigensolver for the differential problem, not the matching function.
def fd_slab(dx:float,L:float,row):
    n=int(round(2*L/dx)); x=np.linspace(-L,L,n+1)[1:-1]; dx=2*L/n
    a=row['a']; no=row['nout'];nc=row['ncore']; gs=row['gsheet']; k0=row['k0']
    on=np.isclose(abs(x),a,atol=dx*1e-5,rtol=0)
    n2=np.where(abs(x)<a,nc*nc,no*no).astype(float)
    n2[on]=(nc*nc+no*no)/2 # cell average at dielectric jump
    diag=-2/dx**2+k0*k0*n2+gs*on/dx
    off=np.full(len(x)-1,1/dx**2)
    ev,vec=eigh_tridiagonal(diag,off,select='i',select_range=(len(x)-1,len(x)-1),check_finite=False)
    u=vec[:,0]/np.sqrt(dx)
    ua=profile(x,row)
    if np.dot(u,ua)<0:u=-u
    frac=float(dx*(np.sum(u[abs(x)>a+dx/3]**2)+.5*np.sum(u[on]**2)))
    return float(np.sqrt(ev[0])),float(np.sqrt(dx*np.sum((u-ua)**2))),frac
fdrows=[]
for no,gs in [(1.,0.),(1.2,.2),(1.4,.4)]:
    r=slab(no,gs); errs=[]
    for dx in [.04,.02,.01,.005]:
        beta,perr,frac=fd_slab(dx,40.,r)
        err=abs(beta-r['beta']);errs.append(err)
        fdrows.append({'nout':no,'gsheet':gs,'dx':dx,'beta_fd':beta,'beta_error':err,
                       'profile_L2_error':perr,'outside_fraction_fd':frac,
                       'outside_fraction_error':abs(frac-r['outside_fraction'])})
    check(f'FD_second_order_{no}_{gs}',errs[-2]/errs[-1]>3.8,float(errs[-2]/errs[-1]))
    check(f'FD_beta_accuracy_{no}_{gs}',errs[-1]<5e-6,errs[-1])
# Tail/domain check at the weakly bound no=1.4,gs=0 case.
r=slab(1.4,0.)
box=[]
for L in [20.,40.,60.]:
    b,pe,fo=fd_slab(.01,L,r);box.append({'L':L,'beta':b,'error':abs(b-r['beta'])})
check('FD_exterior_truncation_control',abs(box[-1]['beta']-box[-2]['beta'])<1e-7)
# Full-mode overlap (inside PLUS exterior), with independent integral checks.
from scipy.integrate import quad
def mode_overlap(r,s):
    if r['a']!=s['a']:raise ValueError('Common half-width required for this formula.')
    a=r['a'];q1=r['q'];q2=s['q']
    inside=a*np.sinc((q1-q2)*a/np.pi)+a*np.sinc((q1+q2)*a/np.pi)
    outside=2*np.cos(q1*a)*np.cos(q2*a)/(r['kappa']+s['kappa'])
    return float((inside+outside)/np.sqrt(r['norm']*s['norm']))
for j in range(12):
    r=slab(float(RNG.uniform(1,1.35)),float(RNG.uniform(0,.35)))
    s=slab(float(RNG.uniform(1,1.35)),float(RNG.uniform(0,.35)))
    a=r['a']
    core=2*quad(lambda x:float(profile(np.array(x),r)*profile(np.array(x),s)),0,a,epsabs=1e-12)[0]
    tail=2*quad(lambda x:float(profile(np.array(x),r)*profile(np.array(x),s)),a,np.inf,epsabs=1e-12)[0]
    check(f'full_mode_overlap_quadrature_{j}',abs(mode_overlap(r,s)-core-tail)<1e-11)
    check(f'full_mode_overlap_cap_{j}',0<=mode_overlap(r,s)<=1+1e-13)
mode_metrics=[]; base=slab(1.2,.2)
for h in [2e-3,1e-3,5e-4,2.5e-4]:
    plus=[slab(1.2+h,.2),slab(1.2,.2+h)]
    minus=[slab(1.2-h,.2),slab(1.2,.2-h)]
    gm=np.array([[(mode_overlap(plus[i],plus[j])-mode_overlap(plus[i],minus[j])
                   -mode_overlap(minus[i],plus[j])+mode_overlap(minus[i],minus[j]))/(4*h*h)
                  for j in range(2)] for i in range(2)])
    dmean=np.array([(mode_overlap(base,plus[i])-mode_overlap(base,minus[i]))/(2*h) for i in range(2)])
    gm-=np.outer(dmean,dmean)
    check(f'full_mode_metric_positive_{h}',np.linalg.eigvalsh(gm).min()>0.01)
    mode_metrics.append({'h':h,'metric':gm.tolist(),'eigenvalues':np.linalg.eigvalsh(gm).tolist()})
check('full_mode_metric_convergence',np.max(abs(np.array(mode_metrics[-1]['metric'])-np.array(mode_metrics[-2]['metric'])))<1e-6)
REPORT['sections']['slab']={'parameters':'dimensionless toy; two symmetric local sheets; no fitted material data',
                           'rows':slabrows,'finite_difference':fdrows,'domain_control':box,
                           'full_mode_metric':mode_metrics}
print(' SLAB FD: independent differential eigensolve, second-order refinement and exterior-box controls PASS')

# 3. Gapped neutral two-valley tilted Dirac model. BCD only, not total NLHE.
# H_s = s*t*kx I + s*kx sx + ky sy + m sz, |t|<1.
# Berry convention i Tr(P[dP,dP]) gives upper-band curvature -s*m/(2E^3).
def berry_dipole(mu:float,tilt:float,m:float=.6,nphi:int=256,nr:int=64):
    if abs(tilt)>=1: raise ValueError('Require type-I cones.')
    if abs(mu)<m*np.sqrt(1-tilt*tilt): return (0.,0.)
    if mu<=m: raise ValueError('Metal gate uses mu>m for radial domains containing origin.')
    phi=2*np.pi*(np.arange(nphi)+.5)/nphi; c=np.cos(phi)
    xg,wg=leggauss(nr); total_area=0.;total_fs=0.
    for s in [-1,1]:
        rad=(-mu*s*tilt*c+np.sqrt(mu*mu-m*m+m*m*tilt*tilt*c*c))/(1-tilt*tilt*c*c)
        rr=rad[:,None]*(xg[None,:]+1)/2
        kx=rr*c[:,None]; energy=np.sqrt(m*m+rr*rr)
        domega=3*s*m*kx/(2*energy**5)
        integral=(domega*rr*(rad[:,None]/2)*wg).sum(axis=1)
        total_area+=float(integral.mean()/(2*np.pi))
        en=np.sqrt(m*m+rad*rad)
        omega=-s*m/(2*en**3)
        vx=s*tilt+rad*c/en
        vr=s*tilt*c+rad/en
        total_fs+=float(np.mean(rad*omega*vx/abs(vr))/(2*np.pi))
    return total_area,total_fs
bcd=[]
for mu,t in [(0.,.3),(.8,0.),(.8,.15),(.8,.3),(.8,-.3),(1.2,.3)]:
    a,b=berry_dipole(mu,t);aa,bb=berry_dipole(mu,t,nphi=512,nr=128)
    check(f'BCD_area_vs_FS_{mu}_{t}',abs(a-b)<2e-11,float(abs(a-b)))
    check(f'BCD_resolution_{mu}_{t}',abs(a-aa)<2e-11,float(abs(a-aa)))
    bcd.append({'mu':mu,'tilt':t,'D_x':a,'FS_D_x':b,'fine_D_x':aa})
check('BCD_tilt_reversal',abs(bcd[3]['D_x']+bcd[4]['D_x'])<1e-12)
check('BCD_no_tilt_zero',abs(bcd[1]['D_x'])<1e-12)
check('BCD_doped_nonzero',abs(bcd[3]['D_x'])>.001)
# Rebuild the neutral projector metric from eigensolves and finite differences,
# independently of the analytic Bloch-vector formula used for the reference.
sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.diag([1.,-1.])
def dirac_projector(kx,ky,tilt,m=.6,valley=1):
    H=valley*tilt*kx*np.eye(2)+valley*kx*sx+ky*sy+m*sz
    ev,U=np.linalg.eigh(H);u=U[:,0]
    return np.outer(u,u.conj())
metric_checks=[]
for tilt in [-.3,0.,.3]:
    errs=[]
    for h in [1e-3,5e-4,2.5e-4,1.25e-4]:
        dx=(dirac_projector(h,0,tilt)-dirac_projector(-h,0,tilt))/(2*h)
        dy=(dirac_projector(0,h,tilt)-dirac_projector(0,-h,tilt))/(2*h)
        gm=np.array([[np.trace(v@w).real/2 for w in [dx,dy]] for v in [dx,dy]])
        err=float(np.max(abs(gm-np.eye(2)/(4*.6**2))));errs.append(err)
        check(f'neutral_projector_regular_{tilt}_{h}',np.linalg.eigvalsh(gm).min()>.69)
    check(f'neutral_metric_derivative_convergence_{tilt}',errs[-2]/errs[-1]>3.9)
    check(f'neutral_metric_final_error_{tilt}',errs[-1]<4e-8,errs[-1])
    metric_checks.append({'tilt':tilt,'errors':errs,'metric_fd':gm.tolist()})
check('tilt_changes_occupation_not_projector',np.linalg.norm(dirac_projector(.3,.2,.3)-dirac_projector(.3,.2,-.3))<1e-14)
REPORT['sections']['charge_neutrality']={'model':'two TR-related type-I massive cones; BCD channel only',
    'm':.6,'metric_at_k0':[[1/(4*.6**2),0],[0,1/(4*.6**2)]],'metric_checks':metric_checks,'rows':bcd}
print('\nBERRY CURVATURE DIPOLE: dimensionless momenta, m=.6, two valleys')
for r in bcd: print(f" mu={r['mu']:.2f} tilt={r['tilt']:+.2f} D_x={r['D_x']:+.12f}")
print(' Occupied-region integral versus independent Fermi-contour integral PASS')

# 4. Two-sided exact linear / second-harmonic boundary reduction and basis test.
w=.7
errors={k:0. for k in ['linear','second_harmonic','unitary_covariance','cayley','external_derivative']}
wrong=[]
for case in range(36):
    ni,ns,no=3,2,4; n=ni+ns+no
    i=slice(0,ni);s=slice(ni,ni+ns);o=slice(ni+ns,n)
    H=np.zeros((n,n),complex)
    for sl,nn in [(i,ni),(s,ns),(o,no)]:
        q=cmat(nn,nn);H[sl,sl]=q.conj().T@q+4*np.eye(nn)
    bis=.15*cmat(ni,ns);bso=.15*cmat(ns,no)
    H[i,s]=bis;H[s,i]=bis.conj().T;H[s,o]=bso;H[o,s]=bso.conj().T
    R=.15*cmat(n,n); R[i,o]=0;R[o,i]=0
    skew=(R-R.conj().T)/2
    base=H+skew
    Ms=[base-1j*j*w*np.eye(n) for j in [1,2]]
    def reduced(M):
        return M[s,s]-M[s,i]@np.linalg.solve(M[i,i],M[i,s])-M[s,o]@np.linalg.solve(M[o,o],M[o,s])
    K1,K2=[reduced(M) for M in Ms]
    f=cmat(ns,1)[:,0]; ff=np.zeros(n,complex);ff[s]=f
    u=np.linalg.solve(Ms[0],ff);us=np.linalg.solve(K1,f)
    errors['linear']=max(errors['linear'],rel(us,u[s]))
    tensor=.2*cmat(ns,ns*ns).reshape(ns,ns,ns)
    tensor=(tensor+tensor.transpose(0,2,1))/2
    B=lambda x:np.einsum('abc,b,c->a',tensor,x,x)
    f2=np.zeros(n,complex);f2[s]=-B(u[s])
    u2=np.linalg.solve(Ms[1],f2);u2s=-np.linalg.solve(K2,B(us))
    errors['second_harmonic']=max(errors['second_harmonic'],rel(u2s,u2[s]))
    Q=np.zeros((n,n),complex)
    for sl,nn in [(i,ni),(s,ns),(o,no)]:Q[sl,sl]=unitary(nn)
    qb=Q[s,s]
    newMs=[Q.conj().T@M@Q for M in Ms]
    newK1,newK2=[reduced(M) for M in newMs]
    v1=np.linalg.solve(newK1,qb.conj().T@f)
    v2=-np.linalg.solve(newK2,qb.conj().T@B(qb@v1))
    errors['unitary_covariance']=max(errors['unitary_covariance'],rel(qb@v2,u2s),rel(qb@v1,us))
    # Error of ignoring the entire exterior loading term; retain evidence, no fit.
    badK=Ms[0][s,s]-Ms[0][s,i]@np.linalg.solve(Ms[0][i,i],Ms[0][i,s])
    wrong.append(float(np.linalg.norm(np.linalg.solve(badK,f)-us)/np.linalg.norm(us)))
    inv=np.linalg.inv(K1+np.eye(ns)); S=(K1-np.eye(ns))@inv
    herm=(K1+K1.conj().T)/2
    lhs=np.eye(ns)-S.conj().T@S;rhs=4*inv.conj().T@herm@inv
    errors['cayley']=max(errors['cayley'],rel(lhs,rhs))
    check(f'boundary_passivity_{case}',np.linalg.eigvalsh(lhs).min()>-1e-12)
    # Exterior coefficient sensitivity, including both matrix orderings.
    perturb=np.diag(np.linspace(.2,.7,no));h=1e-4
    plus=Ms[0].copy();minus=Ms[0].copy();plus[o,o]+=h*perturb;minus[o,o]-=h*perturb
    pred=Ms[0][s,o]@np.linalg.solve(Ms[0][o,o],perturb@np.linalg.solve(Ms[0][o,o],Ms[0][o,s]))
    obs=(reduced(plus)-reduced(minus))/(2*h)
    errors['external_derivative']=max(errors['external_derivative'],rel(obs,pred))
    check(f'boundary_linear_{case}',rel(us,u[s])<1e-12)
    check(f'boundary_second_harmonic_{case}',rel(u2s,u2[s])<1e-12)
for k,v in errors.items():check(f'boundary_max_{k}',v<(1e-8 if k=='external_derivative' else 1e-12),v)
check('deleting_exterior_changes_response',min(wrong)>1e-6,float(min(wrong)))
# Formal identifiability control: a completely uncoupled interior coordinate cannot
# be recovered by boundary data, even as a function of frequency.
z,e1,e2,g,d=sp.symbols('z e1 e2 g d')
Mint=sp.diag(e1-z,e2-z);couple=sp.Matrix([g,0])
Kdark=d-(couple.T*Mint.inv()*couple)[0]
check('dark_mode_boundary_independence',sp.diff(Kdark,e2)==0)
REPORT['sections']['two_sided_reduction']={'cases':36,'max_errors':errors,
    'wrong_exterior_relative_error_range':[min(wrong),max(wrong)],
    'dark_mode_boundary_formula':str(Kdark),
    'second_harmonic_scope':'arbitrary declared symmetric bilinear surface source; not microscopic NLHE fit'}
print('\nTWO-SIDED REDUCTION: full vs boundary linear and second-harmonic solves PASS')
print(json.dumps(errors,indent=2));print(' Omit exterior relative error range',min(wrong),max(wrong))

# 5. A quasistatic nonlinear Hall law: total work vs differential response.
ex,ey,dx,dy,sig,chi,bias,eps=sp.symbols('ex ey dx dy sigma chi bias epsilon',real=True)
E=sp.Matrix([ex,ey]);rot=sp.Matrix([[0,-1],[1,0]])
J=sig*E+chi*ex*(rot*E) # dipole axis d=(1,0)
work=sp.expand((E.T*J)[0]);check('hall_total_work',sp.expand(work-sig*(ex**2+ey**2))==0)
L=J.jacobian([ex,ey]).subs({ex:bias,ey:0})
Hs=sp.simplify((L+L.T)/2)
check('hall_differential_form',Hs==sp.Matrix([[sig,chi*bias/2],[chi*bias/2,sig]]))
check('hall_differential_determinant',sp.factor(Hs.det()-(sig**2-chi**2*bias**2/4))==0)
delta=sp.Matrix([dx,dy]);E0=sp.Matrix([bias,0]);Hall0=J-sig*E
LH=Hall0.jacobian([ex,ey]).subs({ex:bias,ey:0})
Hall_delta=Hall0.subs({ex:dx,ey:dy})
check('hall_bias_energy_cancellation',sp.expand((delta.T*LH*delta)[0]+(E0.T*Hall_delta)[0])==0)
hallrows=[]
for b in [0.,1.,2.,3.]:
    matrix=np.array([[1.,-b],[2*b,1.]])
    eig=np.linalg.eigvalsh((matrix+matrix.T)/2)
    S=(matrix-np.eye(2))@np.linalg.inv(matrix+np.eye(2))
    hallrows.append({'bias':b,'symmetric_eigenvalues':eig.tolist(),
                     'smith_largest_singular_value':float(np.linalg.svd(S,compute_uv=False)[0])})
    for trial in range(20):
        ee=RNG.normal(size=2);jj=ee+ee[0]*np.array([-ee[1],ee[0]])
        check(f'nonlinear_Hall_total_passivity_{b}_{trial}',abs(ee@jj-ee@ee)<1e-12)
check('nonlinear_Hall_incremental_indefinite',hallrows[-1]['symmetric_eigenvalues'][0]<0)
REPORT['sections']['nonlinear_Hall_bias']={'law':str(J),'differential':str(L),'rows':hallrows,
    'scope':'quasistatic constitutive toy; not the intrinsic projector metric; bias supplies incremental energy'}
print('\nNONLINEAR HALL: E dot J=sigma |E|^2, but biased differential form crosses zero')
for row in hallrows:print(row)

# 6. Reject ONLY the trial choice A_intr=on-shell dispersion residual.
eta=1e-3; rigidity=[]
for row in slabrows:
    rv=1/(row['residual']**2+eta)
    rigidity.append({'nout':row['nout'],'sheet':row['gsheet'],'R_residual':rv,'n_eff_squared':row['beta']**2})
    check(f'on_shell_rigidity_{row["nout"]}_{row["gsheet"]}',abs(rv-1/eta)<1e-8)
check('optical_index_changes_while_residual_rigidity_fixed',max(r['n_eff_squared'] for r in rigidity)-min(r['n_eff_squared'] for r in rigidity)>.4)
REPORT['sections']['rigidity_candidate']={'eta':eta,'candidate_rejected':'A_intr=on-shell wave-matching residual, not the user general definition','rows':rigidity}
print('\nRIGIDITY: on-shell-residual candidate saturates at 1/eta for EVERY guided mode; cannot equal varying n_eff^2')
write_report()
print(f'\n{REPORT["passed"]}/{REPORT["assertions"]} exact/model assertions passed. No Lean certification claimed.')
