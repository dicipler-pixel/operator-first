"""Finite lossless constitutive response diagnostic; no physical classification."""
import numpy as np

def run(inputs,context,dependencies,spec,runtime):
 p=inputs['constitutive'];gaps=np.asarray(p['gaps'],float);a=np.asarray(p['amplitudes'],float);x=float(p['photon_energy']);tol=float(p.get('relative_tolerance',1e-10))
 if gaps.ndim!=1 or not len(gaps) or a.ndim!=2 or a.shape[0]!=len(gaps) or not a.shape[1] or not np.all(np.isfinite(gaps)) or not np.all(np.isfinite(a)) or not np.isfinite(x) or np.any(gaps<=0) or not 0<tol<1e-2:raise ValueError('Finite positive gaps, real amplitude matrix, finite energy and relative tolerance required.')
 den=gaps*gaps-x*x
 if np.any(np.abs(den)<=tol*(gaps*gaps+x*x)):return {'_status':'blocked','reason':'At or too close to a transition pole; lossless diagnostic not applicable.'}
 J=a/gaps[:,None];gm=np.einsum('mi,mj->mij',J,J);w=2*gaps**3/den;g=gm.sum(axis=0);alpha=np.einsum('m,mij->ij',w,gm)
 sv=np.linalg.svd(g,compute_uv=False);scale=float(sv.max());rank=int(np.sum(sv>tol*scale)) if scale else 0
 terms=np.array([np.linalg.norm(t) for t in w[:,None,None]*gm]);ts=float(terms.sum());norm=float(np.linalg.norm(alpha));ratio=norm/ts if ts else 0.
 return {'metric':g.tolist(),'response_symmetric':alpha.tolist(),'weights':w.tolist(),'metric_rank_relative':rank,'relative_tolerance':tol,'metric_scale':scale,'strictly_subgap':bool(x*x<np.min(gaps*gaps)),'all_weights_positive':bool(np.all(w>0)),'response_to_term_norm_ratio':ratio,'cancellation_flag':bool(ts>0 and ratio<tol),'all_transition_amplitudes_zero':bool(np.all(a==0)),'interpretation':'Lossless finite real-dipole model; cancellation flag is numerical, not a proof or particle identification.'}
