"""Horizon comparison 1.0: scoped views, not a physical identification of models.

Geometrical units G=c=1 are used ONLY by causal_surface. Other calculations
use declared dimensionless finite models. See each manifest and manual.
"""
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad

def stop(s): return {'_status':'blocked','reason':s}
def encode(a): return {'real':np.real(a).tolist(),'imag':np.imag(a).tolist()}
def case(i): return i['case']
def matrix(v):
    a=np.asarray(v,dtype=float)
    if a.ndim!=2 or not np.all(np.isfinite(a)): raise ValueError('Finite real matrix required.')
    return a

def orientation(i,*_):
    p=case(i);X=matrix(p['X'])
    if X.shape!=(3,3):return stop('Three Jacobi vectors in three dimensions required.')
    G=X.T@X;det=float(np.linalg.det(X));Y=np.diag([1,1,-1])@X
    return {'gram':G.tolist(),'gram_rank':int(np.linalg.matrix_rank(G)),
        'det_X':det,'orientation_sign':int(np.sign(det)),
        'reflected_det_X':float(np.linalg.det(Y)),
        'reflected_gram_residual':float(np.linalg.norm(Y.T@Y-G)),
        'scope':'Gram data forget orientation at full rank; near rank loss a signed lift and numerical tolerance must be retained.'}

def wall_path(i,*_):
    p=case(i);a=float(p['a']);q=float(p['q'])
    if not 0<a<1 or not abs(q)<1:return stop('0<a<1 and |q|<1 required for this path.')
    X=np.diag([np.sqrt(a)*np.sqrt(1-q*q),np.sqrt(1-a)*np.sqrt(1-q*q),q])
    dX=np.diag([-np.sqrt(a)*q/np.sqrt(1-q*q),-np.sqrt(1-a)*q/np.sqrt(1-q*q),1])
    gq=1/(1-q*q);length=quad(lambda s:1/np.sqrt(1-s*s),0,abs(q),epsabs=1e-12)[0]
    return {'q':q,'w3':q*q,'lift':X.tolist(),'det_X':float(np.linalg.det(X)),
        'lift_speed_squared':float(np.sum(dX*dX)),'metric_qq':gq,
        'horizontal_residual':float(np.linalg.norm(X@dX.T-dX@X.T)),
        'gram_coordinate_metric_ww':None if q==0 else 1/(4*q*q*(1-q*q)),
        'path_length_to_wall':length,'analytic_path_length':float(np.arcsin(abs(q))),
        'scope':'Finite length along an explicit normalized horizontal path. At q=0, metric_qq is the smooth lifted limit; not a claim of physical horizon escape.'}

def shape_transport(i,*_):
    p=case(i);w=np.asarray(p['w'],float);t=np.asarray(p['t'],float)
    if w.shape!=(3,) or t.shape!=(3,) or not np.all(np.isfinite(t)) or np.any(w<0) or not np.isclose(w.sum(),1,atol=1e-12,rtol=0):return stop('Trace-one nonnegative Gram eigenvalues and three finite principal coefficients required.')
    x,y,z=w;a=t[0]-t[1];S=t[0]+t[1]-2*t[2];d=x-y;q=float(p.get('signed_q',np.sqrt(z)))
    if not np.isclose(q*q,z,atol=1e-14,rtol=1e-10):return stop('Signed lift coordinate must satisfy q^2=w3.')
    A=np.array([[t[0]+t[1]-a*d,(a-S*d)/np.sqrt(3)],[np.sqrt(3)*a*z,2*t[2]+z*S]])
    B=np.array([[A[0,0],-2*q*(a-S*d)],[-a*q/2,A[1,1]]])
    out={'coordinate_operator':A.tolist(),'lifted_operator':B.tolist(),'eigenvalues':encode(np.linalg.eigvals(A)),
        'metric_available':bool(np.all(w>0)),
        'coordinate_jordan_at_wall':bool(z==0 and np.isclose(A[0,0],A[1,1],atol=1e-12,rtol=0) and abs(A[0,1])>1e-12),
        'lifted_nilpotent_residual_at_wall':float(np.linalg.norm(B-np.trace(B)/2*np.eye(2))) if z==0 else None,
        'scope':'The audited principal-frame shape block. The lift is a similarity only for q!=0; its continuous limit supplies a different regular tangent chart.'}
    if np.all(w>0):
        E=np.array([[1,-1,0],[1/np.sqrt(3),1/np.sqrt(3),-2/np.sqrt(3)]])/np.sqrt(2)
        g=(E/(4*w))@E.T;F=np.linalg.cholesky(g).T;Fi=np.linalg.inv(F)
        ev,V=np.linalg.eig(A);gap=abs(ev[0]-ev[1]);J=np.diag([1/np.sqrt(2),-np.sqrt(6)*q])
        out.update(metric=g.tolist(),metric_condition=float(np.linalg.cond(g)),
          metric_selfadjoint_residual=float(np.linalg.norm(g@A-A.T@g)),
          whitened_operator=(F@A@Fi).tolist(),
          lift_similarity_residual=float(np.linalg.norm(A@J-J@B)))
        if gap>1e-12:
            P=np.outer(V[:,0],np.linalg.inv(V)[0]);out.update(gap=float(gap),projector_norm_coordinate=float(np.linalg.norm(P,2)),projector_norm_metric=float(np.linalg.norm(F@P@Fi,2)))
    return out

def oscillator_scaling(i,*_):
    p=case(i);lam=np.asarray(p['lambda'],float);mode=p['normalization']
    if lam.ndim!=1 or np.any(lam<=0) or not np.all(np.isfinite(lam)):return stop('Positive finite oscillator eigenvalues required.')
    omega=np.sqrt(2*lam)
    if mode=='fixed_energy':
        E=float(p['energy'])
        if E<0:return stop('Nonnegative energy required.')
        amp=np.sqrt(2*E)/omega;vamp=np.full_like(omega,np.sqrt(2*E))
    elif mode=='fixed_initial_data':
        q0=float(p['q0']);v0=float(p['v0']);amp=np.hypot(q0,v0/omega);vamp=omega*amp
    else:return stop('Declare fixed energy or fixed initial data; no universal amplitude law without normalization.')
    return {'frequencies':omega.tolist(),'displacement_amplitudes':amp.tolist(),'velocity_amplitudes':vamp.tolist(),
        'energies':(.5*vamp*vamp).tolist(),'scope':'q_ddot+2 lambda q=0, unit mass. Phase convention and initial data matter; displacement suppression does not imply velocity suppression.'}

def causal_surface(i,*_):
    p=case(i)
    if p.get('model')!='Schwarzschild_ingoing_PG':return stop('This implementation is scoped to nonrotating Schwarzschild in ingoing Painleve-Gullstrand coordinates.')
    M=float(p['mass']);r=np.asarray(p['radii'],float)
    if M<=0 or r.ndim!=1 or np.any(r<=0) or not np.all(np.isfinite(r)):return stop('Positive mass and strictly positive radii required; r=0 is excluded.')
    if p.get('observer','infalling')=='static' and np.any(r<=2*M):return stop('A timelike static observer does not extend to or inside the Schwarzschild horizon.')
    u=-np.sqrt(2*M/r);f=1-2*M/r
    return {'horizon_radius':2*M,'radii':r.tolist(),'outgoing_dr_dt':(u+1).tolist(),'ingoing_dr_dt':(u-1).tolist(),
        'local_light_speeds_relative_to_infall':[-1,1],
        'constant_radius_causal_type':['null' if abs(x)<1e-12 else ('timelike' if x>0 else 'spacelike') for x in f],
        'kretschmann':(48*M*M/r**6).tolist(),'scope':'Classical model prediction in units G=c=1. Coordinate ray slopes are not locally measured superluminal speeds. No outgoing interior telemetry.'}

def opacity_channels(i,*_):
    p=case(i);tau=np.asarray(p['optical_depth'],float);U=float(p['flow_speed']);cs=float(p['sound_speed'])
    if np.any(tau<0) or not np.all(np.isfinite(tau)) or cs<=0:return stop('Nonnegative optical depth and positive sound speed required.')
    if p.get('radiative_model')!='pure_absorption':return stop('Only the declared pure-absorption transmission proxy is implemented, not full solar radiative transfer.')
    return {'direct_transmission':np.exp(-tau).tolist(),'acoustic_characteristics':[U-cs,U+cs],
        'two_acoustic_directions':bool(abs(U)<cs),
        'scope':'Local dimensionless opacity/acoustic proxy. Solar photospheric optical opacity is not by itself a causal event horizon; no solar profile is inferred here.'}

def _obs(p):
    L=matrix(p['L']);C=matrix(p['C']);times=np.asarray(p['times'],float);n=len(L)
    if L.shape!=(n,n) or C.shape[1]!=n or times.ndim!=1 or len(times)<1 or np.any(times<0):raise ValueError('Compatible dynamics, observation matrix, and nonnegative times required.')
    O=np.vstack([C@np.linalg.matrix_power(L,k) for k in range(n)])
    sigma=float(p['noise_sigma']);scale=float(p.get('state_scale',1))
    if sigma<=0 or scale<=0:raise ValueError('Positive noise and state scales required.')
    K=np.vstack([C@expm(L*t) for t in times]);_,s,Vh=np.linalg.svd(K,full_matrices=True)
    s=np.pad(s,(0,max(0,n-len(s))));threshold=float(p.get('snr_threshold',1))
    if threshold<=0:raise ValueError('Positive SNR threshold required.')
    return L,C,O,K,s,Vh,scale/sigma,threshold

def observability(i,*_):
    p=case(i)
    if p.get('measurement_allowed',True) is not True:return stop('The requested observation is not available to the declared observer.')
    try:L,C,O,K,s,Vh,ratio,threshold=_obs(p)
    except ValueError as e:return stop(str(e))
    n=len(L);rank=int(np.linalg.matrix_rank(O));effective=int(np.sum(s*ratio>=threshold))
    return {'state_dimension':n,'algebraic_observability_rank_numeric':rank,'sampled_singular_values':s.tolist(),
        'snr_per_unit_scaled_state':(s*ratio).tolist(),'noise_resolved_directions':effective,
        'least_visible_direction':Vh[-1].tolist(),'observation_matrix':K.tolist(),
        'scope':'Known finite linear dynamics, independent equal-variance noise, declared state coordinates and scale. Noise rank is a diagnostic, not a posterior probability or physical measurement.'}

def interior_ambiguity(i,*_):
    p=case(i)
    if p.get('measurement_allowed',True) is not True:return stop('Forbidden observer channel cannot resolve a physical inference problem.')
    C=matrix(p['C']);times=np.asarray(p['times'],float);sigma=float(p['noise_sigma']);models=p['models']
    if len(models)<2 or sigma<=0 or np.any(times<0):return stop('At least two candidate interiors, nonnegative times and positive noise required.')
    curves=[];targets=[]
    for m in models:
        L=matrix(m['L']);x=np.asarray(m['initial'],float);D=matrix(m['target'])
        states=np.array([expm(t*L)@x for t in times]);curves.append((states@C.T).ravel());targets.append((states@D.T).ravel())
    rows=[]
    for a in range(len(models)):
        for b in range(a):
            rows.append({'models':[b,a],'outside_difference_norm':float(np.linalg.norm(curves[a]-curves[b])),
                'outside_difference_in_noise_units':float(np.linalg.norm(curves[a]-curves[b])/sigma),
                'inside_target_difference_norm':float(np.linalg.norm(targets[a]-targets[b]))})
    return {'comparisons':rows,'scope':'Explicit candidate-model counterexamples, not an exhaustive uniqueness test. Distinguishability is evaluated only at the supplied observation times and channels.'}

def two_sided_response(i,*_):
    p=case(i);L=matrix(p['L']);n=len(L);P=p['retained'];z=complex(p['z_real'],p.get('z_imag',0))
    if L.shape!=(n,n) or not P or len(set(P))!=len(P) or any(type(j)is not int or j<0 or j>=n for j in P) or len(P)==n:return stop('A nonempty proper partition of a square finite operator is required.')
    Q=[j for j in range(n) if j not in P];M=z*np.eye(n)-L
    A=M[np.ix_(P,P)];B=M[np.ix_(P,Q)];C=M[np.ix_(Q,P)];D=M[np.ix_(Q,Q)]
    if any(np.linalg.matrix_rank(T)<len(T) for T in [A,D,M]):return stop('Singular pivot or full resolvent; change spectral point or partition.')
    Sp=A-B@np.linalg.solve(D,C);Sq=D-C@np.linalg.solve(A,B);R=np.linalg.inv(M)
    return {'retained_pencil':encode(Sp),'complement_pencil':encode(Sq),
        'retained_residual':float(np.linalg.norm(np.linalg.inv(Sp)-R[np.ix_(P,P)])),
        'complement_residual':float(np.linalg.norm(np.linalg.inv(Sq)-R[np.ix_(Q,Q)])),
        'bare_deletion_error':float(np.linalg.norm(np.linalg.inv(A)-R[np.ix_(P,P)])),
        'scope':'Two Schur complements of one declared pencil. Eliminating hidden variables is exact algebra, not recovering a unique hidden physical system.'}

def riesz_group(i,*_):
    p=case(i);A=matrix(p['A']);n=len(A);c=complex(p['center']);r=float(p['radius']);N=int(p.get('points',512));expected=int(p['expected_count'])
    if r<=0 or N<64 or N>8192 or A.shape!=(n,n):return stop('Positive contour radius, square real operator and 64..8192 points required.')
    ev=np.linalg.eigvals(A);clearance=float(np.min(np.abs(np.abs(ev-c)-r)))
    count=int(np.sum(np.abs(ev-c)<r))
    if clearance<1e-10 or count!=expected:return stop('Contour touches spectrum or fails the declared enclosed-count gate.')
    P=np.zeros_like(A,dtype=complex)
    for th in np.arange(N)*2*np.pi/N:
        dz=r*np.exp(1j*th);P+=dz*np.linalg.solve((c+dz)*np.eye(n)-A,np.eye(n))/N
    return {'projector':encode(P),'trace':encode(np.trace(P)),
        'idempotence_residual':float(np.linalg.norm(P@P-P)),
        'commutator_residual':float(np.linalg.norm(A@P-P@A)),
        'euclidean_norm':float(np.linalg.norm(P,2)),'enclosed_count_numeric':count,
        'sample_points':N,'spectral_clearance_numeric':clearance,
        'scope':'Numerical circular Riesz integral with an eigenvalue count guard; not a rigorous floating-point enclosure. Group persistence does not identify hidden spacetime.'}
