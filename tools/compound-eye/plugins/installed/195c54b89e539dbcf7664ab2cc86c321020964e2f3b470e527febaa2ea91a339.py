"""Finite calibration models, with declared domains. Complex JSON uses strings, e.g. '1j'."""
import numpy as np
from scipy.linalg import expm

def stop(s):return {'_status':'blocked','reason':s}
def d(i):return i['case']
def arr(x):return np.asarray(x,dtype=complex)
def enc(x):return [float(np.real(x)),float(np.imag(x))]
def state(x):
 a=arr(x);n=np.linalg.norm(a)
 if n<1e-14:raise ValueError('Zero state')
 return a/n
X=arr([[0,1],[1,0]]);Y=arr([[0,-1j],[1j,0]]);Z=arr([[1,0],[0,-1]])

def holonomy(i,*_):
 p=d(i);a=np.array(p['link_phases'],float);g=np.array(p['vertex_gauge'],float)
 if len(a)!=len(g):return stop('Closed cycle: one link per vertex required.')
 w=np.prod(np.exp(1j*a));v=np.prod(np.exp(1j*(a+g-np.roll(g,-1))))
 return {'Wilson_loop':enc(w),'gauge_residual':float(abs(w-v)),'phase_mod_2pi':float(np.angle(w)),'balanced_interference_probability':float((1+w.real)/2),'scope':'U(1) closed-cycle holonomy; link phases already include charge/hbar.'}

def geometric_phase(i,*_):
 s=[state(v) for v in d(i)['states']];b=np.prod([np.vdot(a,c) for a,c in zip(s,s[1:]+s[:1])])
 if abs(b)<1e-13:return stop('An adjacent overlap vanishes; polygon phase undefined.')
 return {'Bargmann_product':enc(b),'polygon_geometric_phase':float(-np.angle(b)),'scope':'Discrete projective polygon, negative-argument convention. Continuum AA phase needs convergence and a cyclic evolution.'}

def weak_value(i,*_):
 p=d(i);a=state(p['pre']);b=state(p['post']);A=arr(p['observable'])
 if not np.allclose(A,A.conj().T):return stop('This eye requires a Hermitian observable.')
 z=np.vdot(b,a);v=np.vdot(b,A@a)
 if abs(z)<1e-12:return stop('Orthogonal pre/postselection: weak value undefined.')
 return {'weak_value':enc(v/z),'success_at_zero_coupling':float(abs(z)**2),'weighted_squared_value':float(abs(v)**2),'second_moment':float(np.vdot(A@a,A@a).real),'scope':'Conditional response, not an eigenvalue or unconditional transferred energy.'}

def pointer(i,*_):
 p=d(i);a=state(p['pre']);b=state(p['post']);A=arr(p['observable']);g=float(p['g'])
 if not np.allclose(A,A.conj().T):return stop('Hermitian interaction required for this unitary pointer.')
 psi=expm(-1j*g*np.kron(A,Y))@np.kron(a,[1,0]);m=b.conj()@psi.reshape(len(a),2);prob=float(np.vdot(m,m).real)
 if prob<1e-20:return stop('No successful postselection events.')
 m=m/np.sqrt(prob)
 return {'success':prob,'pointer_X':float(np.vdot(m,X@m).real),'pointer_Y':float(np.vdot(m,Y@m).real),'pointer_Z':float(np.vdot(m,Z@m).real),'scope':'Exact finite-strength qubit meter; compare X/(2g) to Re weak value only in its weak regime.'}

def abl(i,*_):
 p=d(i);a=state(p['pre']);b=state(p['post']);Ps=[arr(v) for v in p['projectors']];I=np.eye(len(a))
 if not np.allclose(sum(Ps),I) or any(not np.allclose(P,P.conj().T) or not np.allclose(P@P,P) for P in Ps):return stop('Complete orthogonal projective instrument required.')
 if any(not np.allclose(P@Q,0) for j,P in enumerate(Ps) for Q in Ps[j+1:]):return stop('Projectors overlap.')
 w=np.array([abs(np.vdot(b,P@a))**2 for P in Ps]);total=float(w.sum())
 if total<1e-14:return stop('Postselection impossible for this instrument.')
 return {'conditional_probabilities':(w/total).tolist(),'success_after_intermediate_measurement':total,'scope':'ABL probabilities for the declared intervention; grouping outcomes is not generally coherent coarse projection.'}

def cheshire(i,*_):
 a=state([1,0,0,1]);b=state([1,0,1,0]);PL=np.diag([1,1,0,0]);PR=np.eye(4)-PL;SX=np.kron(np.eye(2),X)
 return {'weak_values':{k:enc(np.vdot(b,A@a)/np.vdot(b,a)) for k,A in [('L',PL),('R',PR),('L_X',PL@SX),('R_X',PR@SX)]},'unconditional_path_populations':[.5,.5],'postselection_probability':.25,'scope':'Four-dimensional interferometer calibration. No proof of property physically detached from particle.'}

def phase_conjugation(i,*_):
 z=complex(d(i).get('amplitude','1+2j'));target=np.conj(1j*z);linear=1j*np.conj(z)
 return {'complex_linearity_obstruction':float(abs(target-linear)),'universal_passive_conjugation_admitted':False,'scope':'Any fixed complex-linear map fails on {z,iz} for nonzero z. Known references can be synthesized; general conjugation needs additional resources.'}

def constitutive_null(i,*_):
 p=d(i);h=arr(p.get('d',[2,0,'0.4+0.6j']));theta=np.linspace(0,np.pi,int(p.get('samples',20001)));vs=np.array([np.cos(theta),0*theta,np.sin(theta)]).T
 D=h@h
 if abs(D)<1e-12:return stop('Degenerate spectral gap; simple-eigenvalue formula unavailable.')
 H=h[0]*X+h[1]*Y+h[2]*Z;ev,R=np.linalg.eig(H);L=np.linalg.inv(R);gap2=(ev[0]-ev[1])**2;phase=np.angle(gap2)
 V=vs[:,0,None,None]*X+vs[:,2,None,None]*Z
 A=np.einsum('i,tij,j->t',L[0],V,R[:,1]);B=np.einsum('i,tij,j->t',L[1],V,R[:,0]);Q=A*B/gap2
 analytic=(np.sum(vs*vs,axis=1)-(vs@h)**2/D)/(4*D)
 contrast=4*np.real(A*B*np.exp(-1j*phase));naive=4*np.real(A*B)
 def roots(y):
  ix=np.where(y[:-1]*y[1:]<0)[0]
  return [float(np.degrees(theta[k]-y[k]*(theta[k+1]-theta[k])/(y[k+1]-y[k]))) for k in ix]
 return {'metric_null_degrees':roots(Q.real),'matched_null_degrees':roots(contrast),'naive_null_degrees':roots(naive),'analytic_residual':float(max(abs(Q-analytic))),'contrast_identity_residual':float(max(abs(contrast-4*abs(gap2)*Q.real))),'min_real_Q':float(min(Q.real)),'max_real_Q':float(max(Q.real)),'scope':'Two-level complex bilinear susceptibility; sampled sign-changing roots only, not tangential zeros. Hardware not certified.'}

def passivity(i,*_):
 S=arr(d(i)['transfer']);s=np.linalg.svd(S,compute_uv=False)
 return {'largest_power_gain':float(s[0]**2),'contractive':bool(s[0]<=1+1e-12),'scope':'Power-normalized transfer ports at a specified frequency; contractivity alone is not causality or broadband realizability.'}

def recycling(i,*_):
 p=d(i);e=float(p['escape_useful']);l=float(p['loss']);r=float(p['return']);N=p.get('passes',100)
 if min(e,l,r)<0 or abs(e+l+r-1)>1e-10 or type(N)is not int or N<0:return stop('Exclusive probabilities must sum to one; nonnegative integer pass count required.')
 fac=N if r==1 else (1-r**N)/(1-r)
 return {'useful_finite':e*fac,'loss_finite':l*fac,'remaining':r**N,'useful_asymptote':None if r==1 else e/(1-r),'expected_visits':None if r==1 else 1/(1-r),'scope':'Independent repeated encounters with fixed competing risks; probability budget, not photon-energy gain.'}

def reservoir(i,*_):
 p=d(i);a=float(p['optical_to_electronic']);b=float(p['electronic_to_optical']);u=float(p['useful_output']);heat=float(p['heat_output']);pin=float(p['external_input'])
 if min(a,b,u,heat,pin)<0:return stop('Declared directed powers must be nonnegative.')
 optical=b-a-u;electronic=pin+a-b-heat
 return {'optical_dU_dt':optical,'electronic_dU_dt':electronic,'total_dU_dt':optical+electronic,'external_balance':pin-u-heat,'scope':'Two-reservoir energy rates in watts; all external/control inputs included in external_input, all heat in heat_output exactly once.'}

def loop_loss(i,*_):
 p=d(i);eta=float(p['transmission']);N=p['passes']
 if not 0<=eta<=1 or type(N)is not int or N<0:return stop('Passive per-pass transmission and nonnegative integer depth required.')
 return {'survival_probability':eta**N,'scope':'Independent passive losses. Conditional output fidelity alone does not report throughput.'}

def kerr(i,*_):
 p=d(i);chi=float(p['chi']);n=np.arange(int(p.get('cutoff',5)));ph=-chi*n*(n-1)/2
 return {'phases_unwrapped':ph.tolist(),'second_phase_difference':np.diff(ph,n=2).tolist(),'scope':'Declared Kerr U=exp[-i chi n(n-1)/2]. Nonlinear resource is assumed, not synthesized by a linear optical matrix.'}

def neutrality(i,*_):
 p=d(i);ne,nh,me,mh=[float(p[k]) for k in ['ne','nh','mu_e','mu_h']]
 if min(ne,nh,me,mh)<0 or ne*me+nh*mh==0:return stop('Nonnegative densities/mobilities and nonzero conductance required.')
 e=float(p.get('charge_magnitude',1));s=e*(ne*me+nh*mh)
 return {'net_density':nh-ne,'conductivity':s,'weak_field_Hall_coefficient':(nh*mh**2-ne*me**2)/(e*(ne*me+nh*mh)**2),'scope':'Two-carrier Drude model; density and mobility units determine conductivity units. Not a hydrodynamic interacting-fluid fit.'}

def hall_fit(i,*_):
 p=d(i);x=np.asarray(p['current'],float);y=np.asarray(p['second_harmonic_voltage'],float)
 if len(x)!=len(y) or len(x)<4 or not np.all(np.isfinite(x+y)):return stop('At least four finite paired measurements required.')
 scale=float(max(abs(x)))
 if scale==0:return stop('Nonzero current required.')
 D=np.c_[np.ones(len(x)),(x/scale)**2]
 if np.linalg.matrix_rank(D)<2:return stop('Distinct current magnitudes required.')
 beta=np.linalg.lstsq(D,y,rcond=None)[0];res=y-D@beta;sse=float(res@res);sst=float((y-y.mean())@(y-y.mean()))
 return {'intercept':float(beta[0]),'quadratic_coefficient':float(beta[1]/scale**2),'r_squared':None if sst==0 else 1-sse/sst,'residual_rms':float(np.sqrt(sse/len(x))),'n':len(x),'scope':'Unweighted V_2omega = intercept + coefficient I^2. A quadratic fit alone cannot identify Berry, metric, scattering or thermal mechanism; no uncertainty model supplied.'}

def harmonic(i,*_):
 p=d(i);amp=float(p['amplitude']);chi=float(p['chi']);t=np.linspace(0,2*np.pi,4096,endpoint=False);v=chi*(amp*np.sin(t))**2
 return {'dc':float(np.mean(v)),'cos_2omega':float(2*np.mean(v*np.cos(2*t))),'sin_2omega':float(2*np.mean(v*np.sin(2*t))),'scope':'Peak-amplitude sine-drive convention, instantaneous quadratic response; lock-in RMS and reference phase require explicit conversion.'}


def probability_budget(i,*_):
 p=d(i);v=np.asarray(p['probabilities'],float)
 if v.ndim!=2 or not np.all(np.isfinite(v)) or np.min(v)<0:return stop('Finite nonnegative outcome table required.')
 return {'row_sums':v.sum(axis=1).tolist(),'max_normalization_residual':float(max(abs(v.sum(axis=1)-1))),'scope':'Published conditional outcome table. Normalization does not recover unreported lost events.'}

def fidelity_drift(i,*_):
 p=d(i);t=np.asarray(p['time_s'],float);f=np.asarray(p['fidelity'],float)
 if len(t)!=len(f) or len(t)<2 or np.any(np.diff(t)<=0) or np.min(f)<0 or np.max(f)>1:return stop('Ordered times and [0,1] fidelities required.')
 slope=float(np.polyfit(t-t[0],f,1)[0])
 return {'start':float(f[0]),'end':float(f[-1]),'duration_s':float(t[-1]-t[0]),'change':float(f[-1]-f[0]),'OLS_slope_per_s':slope,'scope':'Descriptive source-table drift, unweighted. No extrapolated lifetime, energy efficiency or raw-event reconstruction.'}

def modular_translation(i,*_):
 p=d(i);a=state(p['state']);k=int(p.get('shift',1));v=np.vdot(a,np.roll(a,k))
 return {'translation_expectation':enc(v),'position_probabilities':(abs(a)**2).tolist(),'scope':'Periodic finite-lattice translation; characteristic function of lattice momentum, not a continuum momentum reconstruction.'}

def nonabelian_loop(i,*_):
 p=d(i);Us=[arr(u) for u in p['links']];Gs=[arr(g) for g in p['gauge']];n=Us[0].shape[0]
 if len(Us)!=len(Gs) or any(not np.allclose(u.conj().T@u,np.eye(n)) for u in Us+Gs):return stop('Matched cycle of unitary links and vertex gauge matrices required.')
 W=np.eye(n,dtype=complex);V=W.copy()
 for j,u in enumerate(Us):W=W@u;V=V@(Gs[j]@u@Gs[(j+1)%len(Gs)].conj().T)
 return {'Wilson_trace':enc(np.trace(W)),'trace_gauge_residual':float(abs(np.trace(W)-np.trace(V))),'matrix_covariance_residual':float(np.linalg.norm(V-Gs[0]@W@Gs[0].conj().T)),'scope':'Ordered matrix holonomy. Gauge covariance does not imply invariance under physical path deformation.'}

def incoherent_covariance(i,*_):
 from scipy.linalg import solve_continuous_lyapunov
 p=d(i);A=arr(p['drift']);D=arr(p['noise_covariance'])
 if np.max(np.linalg.eigvals(A).real)>=-1e-12:return stop('Strictly stable linear drift required.')
 if not np.allclose(D,D.conj().T) or np.min(np.linalg.eigvalsh(D))<0:return stop('Positive semidefinite input covariance required.')
 C=solve_continuous_lyapunov(A,-D)
 return {'steady_covariance':[[enc(v) for v in row] for row in C],'occupations':np.real(np.diag(C)).tolist(),'balance_residual':float(np.linalg.norm(A@C+C@A.conj().T+D)),'scope':'Classical linear noise-driven covariance. A calibration for incoherent excitation, not a reproduction of the published SSH experiment.'}
