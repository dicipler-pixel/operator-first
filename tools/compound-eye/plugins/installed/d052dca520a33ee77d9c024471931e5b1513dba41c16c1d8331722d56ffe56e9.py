import numpy as np
from scipy.linalg import expm

def stop(s):return {'_status':'blocked','reason':s}
def normality(inputs,*_):
 d=inputs['case'];H=np.array(d['H'],complex);S=(H+H.conj().T)/2;K=(H-H.conj().T)/2;comm=S@K-K@S;normal=H@H.conj().T-H.conj().T@H;ev=np.linalg.eigvals(H)
 return {'decomposition_residual':float(np.linalg.norm(H-S-K)),'normality_identity_residual':float(np.linalg.norm(normal+2*comm)),'commutator_norm':float(np.linalg.norm(comm)),'spectral_abscissa':float(max(ev.real)),'numerical_abscissa':float(max(np.linalg.eigvalsh(S))),'sampled_amplitude_gains':[float(np.linalg.norm(expm(float(t)*H),2)) for t in d.get('times',[0,.1,1])],'scope':'xdot=Hx, declared Euclidean norm; for complex matrices use adjoints. Non-normality alone does not imply transient amplification.'}
def gram(inputs,*_):
 B=np.array(inputs['case']['B'],complex);H=B.conj().T@B;tr=np.trace(H).real
 if tr<=0:return stop('Nonzero transport required.')
 H/=tr;e,V=np.linalg.eigh(H);gap=float(e[-1]-e[-2]);P=np.outer(V[:,-1],V[:,-1].conj())
 return {'eigenvalues':e.tolist(),'top_gap':gap,'top_projector_real':P.real.tolist() if gap>1e-10 else None,'top_projector_imag':P.imag.tolist() if gap>1e-10 else None,'scope':'Finite-depth right singular projector. No convergence inferred from a single sample; a tied top block is not assigned an arbitrary line.'}
def pairing(inputs,*_):
 d=inputs['case'];A=np.array(d['A'],complex);x=np.array(d['x'],complex);ell=np.array(d['ell'],complex);S=np.array(d['frame'],complex)
 try:y=A@x;m=np.linalg.solve(A.T,ell);xp=np.linalg.solve(S,y);lp=S.T@m
 except np.linalg.LinAlgError:return stop('Invertible transport and frame required.')
 before=ell@x
 return {'pairing_real':float(before.real),'pairing_imag':float(before.imag),'transport_residual':float(abs(m@y-before)),'frame_residual':float(abs(lp@xp-before)),'scope':'Algebraic bilinear dual, inverse transpose; not the Hermitian dual unless conjugations are changed consistently.'}
def metric_frame(inputs,*_):
 d=inputs['case'];H=np.array(d['H'],complex);G=np.array(d['G'],complex);S=np.array(d['frame'],complex);x=np.array(d['x'],complex)
 if not np.allclose(G,G.conj().T) or min(np.linalg.eigvalsh(G))<=0:return stop('Positive definite physical metric required.')
 Hp=np.linalg.solve(S,H@S);Gp=S.conj().T@G@S;xp=np.linalg.solve(S,x);D=H.conj().T@G+G@H
 return {'norm_covariance_residual':float(abs(x.conj()@G@x-xp.conj()@Gp@xp)),'rate_covariance_residual':float(np.linalg.norm(Hp.conj().T@Gp+Gp@Hp-S.conj().T@D@S)),'G_energy_rate_max_eigenvalue':float(max(np.linalg.eigvalsh(D))),'reset_Euclidean_norm_error':float(abs(x.conj()@G@x-xp.conj()@xp)),'scope':'Fixed coordinate change and consistently transformed norm. Moving frames additionally require derivative terms.'}
def cluster(inputs,*_):
 d=inputs['case'];delta=float(d['delta']);radius=float(d.get('radius',1));N=int(d.get('nodes',256));H=np.array([[0,1,0],[delta,0,0],[0,0,5]],complex)
 if abs(delta)>=radius**2 or radius>=5 or radius<=0:return stop('Contour must enclose the two-dimensional cluster and exclude eigenvalue 5.')
 P=np.zeros((3,3),complex)
 for t in np.arange(N)*2*np.pi/N:
  z=radius*np.exp(1j*t);P+=z*np.linalg.inv(z*np.eye(3)-H)/N
 expected=np.diag([1,1,0]);condition=None if delta==0 else float(np.linalg.cond(np.linalg.eig(H[:2,:2])[1]))
 return {'cluster_projector_error':float(np.linalg.norm(P-expected)),'cluster_trace':float(np.trace(P).real),'cluster_norm':float(np.linalg.norm(P,2)),'individual_eigenframe_condition':condition,'scope':'Contour quadrature on explicit EP2 block plus isolated eigenvalue. Cluster remains separated at delta=0; no simple eigenline is assigned there.'}
def stress_composition(inputs,*_):
 d=inputs['case'];a=float(d['s1']);b=float(d['s2'])
 if not 0<=a<=1 or not 0<=b<=1:return stop('Rank-one normalized overlap deficits must lie in [0,1].')
 def mat(s):return np.outer([1.,0.],[np.sqrt(1-s),np.sqrt(s)])
 A=mat(a);B=mat(b);C=np.kron(A,B);value=float(np.linalg.norm(C@C.T-C.T@C,'fro')**2/2)
 return {'tensor_stress':value,'composition_formula':a+b-a*b,'residual':abs(value-(a+b-a*b)),'scope':'Normalized rank-one overlap-deficit stress only. Not a general full-rank stress law.'}
def hall_power(inputs,*_):
 d=inputs['case'];sigma=np.array(d['conductivity'],float);E=np.array(d['field'],float);D=(sigma+sigma.T)/2;A=(sigma-sigma.T)/2
 return {'power_density':float(E@sigma@E),'symmetric_power':float(E@D@E),'antisymmetric_power':float(E@A@E),'scope':'Real DC linear conductivity and Joule power. Antisymmetric Hall response is distinct from microscopic skew scattering and from second-order Hall tensors.'}
