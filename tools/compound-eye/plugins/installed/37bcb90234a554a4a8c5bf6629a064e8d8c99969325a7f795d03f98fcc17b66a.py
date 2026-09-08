"""Boundary graph and response-pair methods; finite coherent model only."""
import numpy as np

def unpack(a):
 a=np.asarray(a)
 return a[...,0]+1j*a[...,1] if a.ndim==3 and a.shape[-1]==2 else a.astype(complex)
def packed(a):return np.stack([np.asarray(a).real,np.asarray(a).imag],axis=-1).tolist()
def block_graph(U):
 n=len(U);Q=np.vstack([np.eye(n),U])/np.sqrt(2)
 return Q@Q.conj().T

def graph(i,*_):
 p=i['case'];U=unpack(p['U']);n=len(U)
 if U.shape!=(n,n) or np.linalg.norm(U.conj().T@U-np.eye(n))>1e-9:
  return {'_status':'blocked','reason':'Square unitary matrix required. Absorption requires an explicitly enlarged scattering space.'}
 P=block_graph(U);K=(2*np.eye(n)-U-U.conj().T)/4
 out={'projector':packed(P),'displacement':packed(K),'angle_squares':np.linalg.eigvalsh(K).tolist(),'projector_residual':float(np.linalg.norm(P@P-P)),'scope':'Graph of the complete unitary amplitude operator in fixed channel coordinates; not an occupied electronic projector.'}
 if 'V' in p:
  V=unpack(p['V'])
  if V.shape!=U.shape or np.linalg.norm(V.conj().T@V-np.eye(n))>1e-9:return {'_status':'blocked','reason':'Comparison must use a unitary operator on the same channels.'}
  out.update(graph_distance_squared=float(np.linalg.norm(P-block_graph(V))**2),half_amplitude_distance_squared=float(np.linalg.norm(U-V)**2/2))
 return out

def response_pair(i,*_):
 p=i['case'];s=float(p['side_energy']);x=float(p.get('probe_energy',0));g=float(p.get('coupling',1))
 if s not in (-1.,1.) or g<=0:return {'_status':'blocked','reason':'This certified pair uses side energy ±1, positive coupling and per-lead width 1 in the declared energy unit.'}
 H=np.array([[0.,g],[g,s]]);L=np.diag([1.,0]);GR=np.linalg.inv(x*np.eye(2)-H+1j*L)
 W=np.array([[1.,1.],[0.,0.]]);S=np.eye(2)-1j*W.T@GR@W
 eigen,U=np.linalg.eigh(H);P=U[:,[0]]@U[:,[0]].T;D=np.diag([1.,0]);dip=float(abs(U[:,1]@D@U[:,0])**2)
 T=float(abs(S[1,0])**2);K=(2*np.eye(2)-S-S.conj().T)/4
 return {'T':T,'Fano':1-T,'reflection_phase':float(np.angle(S[0,0])),'S':packed(S),'occupied_projector':P.tolist(),'gap':float(eigen[1]-eigen[0]),'isolated_strength':dip,'eigenvalues':eigen.tolist(),'displacement':packed(K),'scattering_unitarity':float(np.linalg.norm(S.conj().T@S-np.eye(2))),'self_energy':float(g*g/(x-s)) if abs(x-s)>1e-12 else None,'scope':'Declared noninteracting two-orbital scatterer. Isolated optical gap/strength and contacted transport are different experimental readouts of the same specified Hamiltonian; no elemental fit.'}
