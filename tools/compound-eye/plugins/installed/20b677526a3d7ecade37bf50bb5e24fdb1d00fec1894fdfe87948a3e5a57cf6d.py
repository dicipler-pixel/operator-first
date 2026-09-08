"""Explicit domains for Gram, singular-angle, relaxation and Gram-ladder records."""
import numpy as np

def gram(i,*_):
 X=np.asarray(i['case']['X'],dtype=float)
 if X.ndim!=2 or X.shape[0]!=X.shape[1] or np.linalg.norm(X)==0:
  return {'_status':'blocked','reason':'A nonzero real square Jacobi matrix is required.'}
 scale=float(np.linalg.norm(X));Y=X/scale;G=Y.T@Y;d=len(Y)
 return {'gram':G.tolist(),'size':scale,'signed_normalized_volume':float(np.linalg.det(Y)),'rank':int(np.linalg.matrix_rank(Y)), 'dimension':d*(d+1)//2-1,'scope':'Normalized Gram data forget size and orientation. A horizontal lift additionally requires a connection and initial frame; arbitrary physical rotation is not fixed by the Gram curve.'}

def singular_angle(i,*_):
 M=np.asarray(i['case']['M'],float)
 if M.ndim!=2 or M.shape[0]!=M.shape[1] or np.linalg.norm(M)==0:
  return {'_status':'blocked','reason':'Nonzero real square transport required.'}
 M=M/np.linalg.norm(M);u,s,vh=np.linalg.svd(M)
 if len(s)>1 and s[1]>1e-9:
  return {'_status':'blocked','reason':'The single-angle identity is restricted to normalized rank-one transport.'}
 C=M@M.T-M.T@M;cosine=float(abs(u[:,0]@vh[0]));phi=float(np.linalg.norm(C)**2/2)
 return {'phi':phi,'sin_squared':1-cosine**2,'angle_radians':float(np.arccos(np.clip(cosine,0,1))),'scope':'Left/right singular lines of rank-one transport; not a generic occupied-state metric or signed phase.'}

def relaxation(i,*_):
 K=np.asarray(i['case']['K'],complex)
 if K.ndim!=2 or K.shape[0]!=K.shape[1]:return {'_status':'blocked','reason':'Square finite operator required.'}
 C=K@K.conj().T-K.conj().T@K;A=C@K-K@C;V=-2*A;phi=float(np.linalg.norm(C)**2/2)
 return {'phi':phi,'norm_derivative':float(2*np.vdot(K,V).real),'minus_eight_phi':-8*phi,'stress_derivative':float(-4*np.linalg.norm(A)**2),'henrici_budget':float(np.linalg.norm(K)**2-np.sum(abs(np.linalg.eigvals(K))**2)),'scalar_residual':float(np.linalg.norm(K-np.trace(K)/len(K)*np.eye(len(K)))),'scope':'Isospectral mathematical relaxation. Normality does not imply isotropy, and the Frobenius budget is not physical heat without a device model.'}

def ladder(i,*_):
 c=i['case'];g=np.asarray(c['g'],float);t=np.asarray(c['t'],float)
 if g.ndim!=1 or t.shape!=g.shape or np.any(g<=0) or np.any(t<=0) or abs(g.sum()-1)>1e-9:
  return {'_status':'blocked','reason':'Strictly positive g,t with sum(g)=1 required for the interior positive metric.'}
 S=np.diag(np.sqrt(g/t));u=np.sqrt(g*t);M=np.diag(t)-np.outer(g,t);A=np.diag(t)-np.outer(u,u);W=np.diag(t/g)
 return {'similarity_residual':float(np.linalg.norm(M-S@A@np.linalg.inv(S))),'weighted_adjoint_residual':float(np.linalg.norm(W@M-M.T@W)),'eigenvalues':np.linalg.eigvalsh(A).tolist(),'euclidean_nonnormality':float(np.linalg.norm(M@M.T-M.T@M)),'metric_condition':float(np.linalg.cond(W)),'scope':'Full diagonal rank-one block before restriction to the trace-zero tangent. Positive metric proves real diagonalizability in the interior; boundary metric failure does not itself prove an exceptional point.'}
