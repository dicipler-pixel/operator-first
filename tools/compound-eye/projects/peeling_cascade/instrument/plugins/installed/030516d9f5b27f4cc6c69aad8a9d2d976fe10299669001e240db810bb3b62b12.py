"""Peeling-cascade controls. Exact rational certificates are labelled separately from floats."""
import numpy as np
import sympy as s
from scipy.linalg import expm

def stop(reason):return {'_status':'blocked','reason':reason}
def data(i):return i['case']
def arr(x):return np.asarray(x,dtype=complex)
def encode(x):return {'real':np.real(x).tolist(),'imag':np.imag(x).tolist()}

def positive_peel(i,*_):
 p=data(i);Q=s.Matrix(p['channels']);weights=p['weights'];Gs=[];ranks=[];kernels=[]
 for w in weights:
  if len(w)!=Q.rows or any(s.Rational(v)<0 for v in w):return stop('Nonnegative rational weights matching fixed channels required.')
  W=s.diag(*[s.Rational(v) for v in w]);G=Q.T*W*Q;Gs.append(G);ranks.append(G.rank());kernels.append(G.nullspace())
 if any(s.Rational(b)>s.Rational(a) for w,v in zip(weights,weights[1:]) for a,b in zip(w,v)):return stop('Weights increase: outside the positive removal theorem.')
 inclusion=all(all(Gnext*v==s.zeros(Q.cols,1) for v in K) for K,Gnext in zip(kernels,Gs[1:]))
 return {'ranks_exact':ranks,'nullities_exact':[Q.cols-r for r in ranks],'rank_losses':[a-b for a,b in zip(ranks,ranks[1:])],'kernel_inclusion_exact':inclusion,'forms':[[[str(v) for v in row] for row in G.tolist()] for G in Gs],'scope':'Exact fixed real rational channel model; not atomic constituent counts.'}

def schur_cascade(i,*_):
 p=data(i);H=arr(p['H']);z=complex(p['z']);labels=list(range(len(H)));M=z*np.eye(len(H))-H;S=M.copy();errors=[];conditions=[]
 for kept in p['retained_layers']:
  if not kept or len(set(kept))!=len(kept) or not set(kept)<set(labels):return stop('Each layer must be a nonempty strict subset of current labels.')
  ix=[labels.index(k) for k in kept];qx=[j for j in range(len(labels)) if j not in ix];D=S[np.ix_(qx,qx)]
  if np.linalg.matrix_rank(D)<len(D):return stop('Singular elimination pivot; select a different contour or block.')
  conditions.append(float(np.linalg.cond(D)));S=S[np.ix_(ix,ix)]-S[np.ix_(ix,qx)]@np.linalg.solve(D,S[np.ix_(qx,ix)]);labels=kept
  allq=[j for j in range(len(H)) if j not in kept];direct=M[np.ix_(kept,kept)]-M[np.ix_(kept,allq)]@np.linalg.solve(M[np.ix_(allq,allq)],M[np.ix_(allq,kept)])
  errors.append(float(np.linalg.norm(S-direct)))
 full=np.linalg.inv(M)[np.ix_(labels,labels)];exact=np.linalg.inv(S);bare=np.linalg.inv(M[np.ix_(labels,labels)])
 return {'nested_direct_residuals':errors,'boundary_inverse_residual':float(np.linalg.norm(exact-full)),'bare_deletion_error':float(np.linalg.norm(bare-full)),'pivot_condition_numbers':conditions,'effective_pencil':encode(S),'scope':'Exact-elimination identities evaluated in complex128; bare deletion is a different model.'}

def memory_certificate(i,*_):
 p=data(i);B=s.Matrix(p['B']);D=s.Matrix(p['D']);C=s.Matrix(p['C']);q=D.rows
 if D.cols!=q or B.cols!=q or C.rows!=q or q<1:return stop('Compatible nonempty hidden-state matrices required.')
 if any(v.has(s.Float) for M in [B,C,D] for v in M):return stop('Exact integers or rational strings required for algebraic silence certificate.')
 moments=[B*D**j*C for j in range(2*q-1)];zero=all(M==s.zeros(B.rows,C.cols) for M in moments[:q]);first=next((j for j,M in enumerate(moments[:q]) if M!=s.zeros(B.rows,C.cols)),None)
 Hank=s.BlockMatrix([[moments[j+k] for k in range(q)] for j in range(q)]).as_explicit()
 z=s.symbols('z');F=(B*(z*s.eye(q)-D).inv()*C).applyfunc(s.cancel)
 return {'hidden_dimension':q,'first_nonzero_moment':first,'all_frequency_silent_exact':zero,'moments':[[[str(v) for v in row] for row in M.tolist()] for M in moments[:q]],'transfer':[[str(v) for v in row] for row in F.tolist()],'Hankel_rank_exact':Hank.rank(),'scope':'Cayley-Hamilton finite transfer certificate with zero hidden initial state. Hidden-initial-state forcing requires a separate observability test.'}

def time_memory(i,*_):
 from scipy.integrate import quad_vec
 p=data(i);H=arr(p['H']);n=p['retained_dimension'];x0=arr(p['initial']);A=H[:n,:n];B=H[:n,n:];C=H[n:,:n];D=H[n:,n:];rows=[]
 for t in p['times']:
  x=expm(t*H)@x0;mem,err=quad_vec(lambda u:B@expm((t-u)*D)@C@(expm(u*H)@x0)[:n],0,t,epsabs=1e-11,epsrel=1e-11)
  forcing=B@expm(t*D)@x0[n:];rhs=A@x[:n]+mem+forcing;der=(H@x)[:n]
  rows.append({'time':t,'memory_norm':float(np.linalg.norm(mem)),'initial_forcing_norm':float(np.linalg.norm(forcing)),'equation_residual':float(np.linalg.norm(rhs-der)),'memoryless_state_error':float(np.linalg.norm(expm(t*A)@x0[:n]-x[:n]))})
 return {'trajectory':rows,'scope':'Variation-of-constants checked against full matrix exponential; quadrature uses the full reference trajectory, not an independent reduced solver.'}

def cycle_profile(i,*_):
 p=data(i);cycles=p['cycles']
 if not cycles or any(type(v)is not int or v<1 for v in cycles) or max(cycles)==1:return stop('Nontrivial permutation cycle lengths required.')
 N=sum(cycles);P=np.zeros((N,N));offset=0
 for ell in cycles:
  for j in range(ell):P[offset+(j+1)%ell,offset+j]=1
  offset+=ell
 V=(P-np.eye(N))/np.sqrt(2);G=V.T@V;l=np.maximum(np.linalg.eigvalsh(G),0);lm=float(max(l));mu=np.clip(l/lm,0,1);entropy=sum(-x*np.log(x)-(1-x)*np.log1p(-x) for x in mu if 1e-12<x<1-1e-12);D=sum(v for v in cycles if v>1);eps=p.get('thresholds',[.01,.25,.5,.9,1])
 return {'ambient_dimension':N,'moved_points':D,'Hamming_fraction':D/N,'trace':float(np.trace(G)),'lambda_max':lm,'spectrum':l.tolist(),'normalized_profile':[int(sum(mu>=e-1e-12)) for e in eps],'thresholds':eps,'entropy':float(entropy),'zero_entropy_class':all(v in [1,2] for v in cycles) or all(v in [1,3] for v in cycles),'scope':'Permutation displacement Gram including fixed-point zeros. 2-cycles use parallel-edge multiplicity; normalized profiles alone omit spectral scale and zero multiplicity.'}

def window_census(i,*_):
 p=data(i);values=np.asarray(p['eigenvalues'],float);eps=float(p['epsilon'])
 if not 0<eps<.5 or values.ndim!=2 or np.min(values)<0 or np.max(values)>1:return stop('Contraction eigenvalues in [0,1], fixed 0<epsilon<1/2 required.')
 return {'counts':[int(sum((v>=eps)&(v<=1-eps))) for v in values],'traces':values.sum(axis=1).tolist(),'ordered_diagonal_decrease':bool(np.all(np.diff(values,axis=0)<=0)),'scope':'Two-sided window census, not matrix rank. Ordered diagonal example only; no monotonicity theorem for the census.'}

def tomography(i,*_):
 G=np.asarray(data(i)['form'],float);n=len(G)
 if not np.allclose(G,G.T):return stop('Real symmetric response form required.')
 R=np.diag(np.diag(G));readouts=list(np.diag(G))
 for j in range(n):
  for k in range(j+1,n):
   e=np.eye(n)[j]+np.eye(n)[k];v=float(e@G@e);readouts.append(v);R[j,k]=R[k,j]=(v-G[j,j]-G[k,k])/2
 return {'probe_count':len(readouts),'readouts':readouts,'reconstruction_error':float(np.linalg.norm(R-G)),'scope':'Complete noiseless real quadratic-form tomography with basis and pair-sum probes; not identification of physical constituents.'}

def affine_scale(i,*_):
 p=data(i);H=arr(p['H']);a=float(p['scale']);b=float(p['offset']);z=complex(p['z']);Hp=a*H+b*np.eye(len(H));zp=a*z+b
 if a<=0:return stop('Positive common scale required.')
 R=np.linalg.inv(z*np.eye(len(H))-H);Rp=np.linalg.inv(zp*np.eye(len(H))-Hp)
 return {'resolvent_covariance_residual':float(np.linalg.norm(a*Rp-R)),'scope':'Scale and energy reference transform together. Fixed external thresholds or temperatures are additional data and need not remain invariant.'}
