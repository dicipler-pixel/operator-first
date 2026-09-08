"""Quantum heat engine views: declared models, explicit energy signs and evidence limits."""
import numpy as np
from scipy.linalg import expm

def stop(reason):return {'_status':'blocked','reason':reason}
def mat(v):return np.asarray(v,dtype=complex)
def herm(x):return x.ndim==2 and x.shape[0]==x.shape[1] and np.isfinite(x).all() and np.allclose(x,x.conj().T,atol=1e-10)
def state(v):
 x=mat(v)
 if not herm(x) or not np.isclose(np.trace(x),1,atol=1e-9) or np.linalg.eigvalsh(x).min() < -1e-9:raise ValueError('A normalized positive Hermitian density matrix is required.')
 return x
def entropy(r):
 e=np.linalg.eigvalsh(r);e=e[e>1e-14];return float(-sum(e*np.log(e)))
def td(a,b):return float(np.linalg.eigvalsh(a-b).__abs__().sum()/2)
def enc(x):return {'real':x.real.tolist(),'imag':x.imag.tolist()}

def ledger(i,*_):
 p=i['case']
 if p.get('coupling_regime')!='weak_or_negligible_interaction_energy':return stop('Declare weak/negligible interaction energy, or use a model including interaction energy and switching costs.')
 try:R=[state(x) for x in p['states']];H=[mat(x) for x in p['hamiltonians']]
 except (ValueError,KeyError) as e:return stop(str(e))
 if len(R)!=len(H) or len(R)<2 or any(not herm(h) or h.shape!=r.shape for h,r in zip(H,R)):return stop('Matching finite Hermitian Hamiltonians and states required.')
 rows=[]
 for r,s,h,k in zip(R,R[1:],H,H[1:]):
  w=float(np.trace((r+s)/2@(k-h)).real);q=float(np.trace((h+k)/2@(s-r)).real);du=float(np.trace(s@k-r@h).real)
  rows.append({'work_on':w,'heat_into':q,'delta_U':du,'balance_residual':du-w-q,'mixed_step':bool(not np.allclose(h,k) and not np.allclose(r,s))})
 w=sum(x['work_on'] for x in rows);q=sum(x['heat_into'] for x in rows);closed=td(R[0],R[-1])<1e-9 and np.allclose(H[0],H[-1]);hot=sum(max(x['heat_into'],0) for x in rows)
 return {'strokes':rows,'work_output':-w,'net_heat_into':q,'cycle_closed':bool(closed),'state_closure_distance':td(R[0],R[-1]),'engine_like_energy_ledger':bool(closed and -w>1e-10 and hot>0),'efficiency_from_positive_heat':-w/hot if closed and -w>0 and hot>0 else None,'scope':'Work on system positive; heat into system positive. Midpoint splitting is an exact finite algebraic identity, but mixed steps do not uniquely identify physical heat/work. Control, bath preparation and reset costs are not inferred.'}

def entropy_balance(i,*_):
 p=i['case']
 if p.get('reservoirs')!='equilibrium_positive_temperature' or p.get('initial_correlations')!='none':return stop('This Clausius balance requires declared initially uncorrelated equilibrium baths with positive temperatures.')
 try:a=state(p['initial']);b=state(p['final']);T=np.asarray(p['temperatures'],float);Q=np.asarray(p['heat_into'],float)
 except Exception as e:return stop(str(e))
 if T.shape!=Q.shape or not np.isfinite(T).all() or not np.isfinite(Q).all() or np.any(T<=0):return stop('Finite matching positive temperatures and bath heats required.')
 ds=entropy(b)-entropy(a);sigma=ds-float(sum(Q/T))
 return {'delta_entropy_kB':ds,'entropy_production_kB':sigma,'nonnegative_with_tolerance':bool(sigma>=-1e-9),'scope':'kB=1; heats and temperatures must share energy units. Negative output diagnoses inconsistent assumptions/data; no Carnot comparison for unspecified nonthermal baths.'}

def ergotropy(i,*_):
 p=i['case']
 try:r=state(p['state']);H=mat(p['H'])
 except Exception as e:return stop(str(e))
 if not herm(H) or H.shape!=r.shape:return stop('Matching Hermitian Hamiltonian required.')
 E,U=np.linalg.eigh(H);pop=np.linalg.eigvalsh(r)[::-1];energy=float(np.trace(r@H).real);passive=float(E@pop)
 # Dephase between distinct eigenspaces, retaining within-degeneracy blocks.
 rb=U.conj().T@r@U;rb[np.abs(E[:,None]-E[None,:])>1e-9]=0;rd=U@rb@U.conj().T
 return {'energy':energy,'passive_energy':passive,'ergotropy':max(0.,energy-passive),'relative_entropy_coherence':max(0.,entropy(rd)-entropy(r)),'scope':'Finite-system maximum cyclic-unitary work relative to the declared H. This is not automatically net engine work; coherence is relative to energy eigenspaces.'}

def lindblad(i,*_):
 p=i['case'];H=mat(p['H']);rates=np.asarray(p['rates'],float);J=[mat(x) for x in p['jumps']];t=float(p.get('time',1))
 if not herm(H) or len(J)!=len(rates) or np.any(rates<0) or not np.isfinite(rates).all() or t<0 or any(j.shape!=H.shape for j in J):return stop('Hermitian H, nonnegative finite rates, matching jumps and nonnegative time required.')
 n=len(H);I=np.eye(n);L=-1j*(np.kron(I,H)-np.kron(H.T,I))
 for g,j in zip(rates,J):
  A=j.conj().T@j;L+=g*(np.kron(j.conj(),j)-.5*np.kron(I,A)-.5*np.kron(A.T,I))
 E=expm(t*L);choi=np.zeros((n*n,n*n),complex)
 for a in range(n):
  for b in range(n):
   X=np.zeros((n,n));X[a,b]=1;choi[a*n:(a+1)*n,b*n:(b+1)*n]=(E@X.reshape(-1,order='F')).reshape(n,n,order='F')
 ev,V=np.linalg.eig(L);tracevec=I.reshape(-1,order='F')
 return {'trace_preservation_residual':float(np.linalg.norm(tracevec@L)),'choi_min_eigenvalue':float(np.linalg.eigvalsh((choi+choi.conj().T)/2).min()),'eigenvalues':enc(ev),'eigenvector_condition':float(min(np.linalg.cond(V),1e300)),'generator':enc(L),'scope':'Full GKSL generator, hbar=1. Large eigenvector condition is a warning, not an exceptional-point proof. Includes jump terms absent from a no-jump effective Hamiltonian.'}

def ladder(i,*_):
 p=i['case'];E=np.asarray(p['energies'],float);K=np.asarray(p['generator'],float);P=np.asarray(p['initial'],float);ts=np.asarray(p['times'],float);n=len(E)
 if K.shape!=(n,n) or P.shape!=(n,) or not np.isfinite(K).all() or np.min(P)<0 or not np.isclose(sum(P),1) or np.min(ts)<0:return stop('Finite compatible population ladder and nonnegative times required.')
 off=K-np.diag(np.diag(K))
 if np.min(off)<-1e-12 or not np.allclose(K.sum(axis=0),0):return stop('Column generator convention: nonnegative off-diagonals, zero column sums required.')
 rows=[]
 for t in ts:
  pt=expm(t*K)@P;flux=K*pt[None,:];np.fill_diagonal(flux,0)
  rows.append({'time':float(t),'populations':pt.tolist(),'mean_energy':float(E@pt),'heat_rate_into':float(E@K@pt),'flux_into_i_from_j':flux.tolist()})
 return {'trajectory':rows,'scope':'Classical population dynamics on declared quantum energy levels; population data alone do not certify coherence or non-Markovianity. Fixed H has heat flow, no extracted work term.'}

def spectral_overlap(i,*_):
 p=i['case'];w=np.asarray(p['frequencies'],float);J=np.asarray(p['reservoir_spectrum'],float);F=np.asarray(p['filters'],float)
 if w.ndim!=1 or len(w)<2 or np.any(np.diff(w)<=0) or J.shape!=w.shape or F.ndim!=2 or F.shape[1]!=len(w) or not all(np.isfinite(x).all() for x in [w,J,F]) or np.min(J)<0 or np.min(F)<0:return stop('Increasing frequencies and nonnegative finite matched spectra/filters required.')
 overlap=np.trapezoid(F*J,w,axis=1)
 return {'overlaps':overlap.tolist(),'scope':'Declared nonnegative spectral-overlap integrals. Rates require dimensional normalization and coupling calibration; this alone does not prove an anti-Zeno boost.'}

def backflow(i,*_):
 p=i['case']
 try:A=[state(x) for x in p['states_a']];B=[state(x) for x in p['states_b']]
 except Exception as e:return stop(str(e))
 t=np.asarray(p['times'],float)
 if len(A)!=len(B) or len(A)!=len(t) or len(t)<2 or np.any(np.diff(t)<=0) or p.get('same_channel_preparation') is not True:return stop('Two preparations evolved by the same channel at strictly increasing times required.')
 d=[td(a,b) for a,b in zip(A,B)];increase=float(np.maximum(np.diff(d),0).sum())
 return {'trace_distances':d,'sampled_positive_variation':increase,'backflow_witness':bool(increase>1e-9),'scope':'A resolved trace-distance increase witnesses failure of CP-divisibility under the declared common-channel assumptions. No increase in this sampled pair is not proof of Markovianity; experimental noise needs uncertainty analysis.'}

def data_audit(i,*_):
 p=i['case'];n=p.get('total_entries');valid=p.get('finite_entries')
 if type(n)is not int or type(valid)is not int or not 0<=valid<=n or n==0:return stop('Explicit valid/total integer acquisition counts required.')
 return {'finite_fraction':valid/n,'missing_fraction':1-valid/n,'stage':p.get('stage','unspecified'),'calibration_supplied':bool(p.get('calibration_supplied',False)),'thermodynamic_inference_ready':bool(p.get('calibration_supplied') and p.get('energy_schedule_supplied') and p.get('state_assignment_verified')),'scope':'Audit only. Missing entries are not zero populations. IQ voltages are not density-matrix coherences or energies without a validated readout model.'}

def readout_transfer(i,*_):
 p=i['case'];C=np.asarray(p['selection_matrix'],float);y=np.asarray(p['selected_counts'],float)
 if C.ndim!=2 or C.shape[0]!=C.shape[1] or y.shape!=(len(C),) or not np.isfinite(C).all() or not np.isfinite(y).all() or np.min(C)<0 or np.min(y)<0 or sum(y)<=0:return stop('Square nonnegative finite selection matrix (rows prepared states, columns readout regions) and positive total counts required.')
 if np.linalg.matrix_rank(C)<len(C):return stop('Singular readout map: populations are not identifiable by inversion.')
 x=np.linalg.solve(C.T,y);forward=C.T@x;replay=C@y
 return {'inverted_unscaled_populations':x.tolist(),'normalized_inverse':(x/sum(x)).tolist() if sum(x)>0 else None,'minimum_inverted_component':float(min(x)),'condition_number':float(np.linalg.cond(C)),'forward_residual':float(np.linalg.norm(forward-y)),'multiply_then_normalize':(replay/sum(replay)).tolist() if sum(replay)>0 else None,'scope':'Under rows=prepared states and columns=readout regions, y=C^T x. Inversion is a diagnostic, not an automatically noise-robust estimator. Region widths must match between calibration and acquisition; negative solutions are reported, not clipped.'}
