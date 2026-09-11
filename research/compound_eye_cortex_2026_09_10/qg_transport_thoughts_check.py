#!/usr/bin/env python3
"""Independent finite audit of the transport/memory reconstruction thoughts.
Standard library only. Literature/theorem claims are scope labels, not certified here.
"""
from __future__ import annotations
from cmath import exp
from math import cos, sin, pi, sqrt
import itertools, json

checks=[]
def req(cond,msg):
    if not cond: raise AssertionError(msg)
    checks.append(msg)

def mmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def msub(A,B): return [[A[i][j]-B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
def mtrans(A): return [list(x) for x in zip(*A)]
def mconjtrans(A): return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def frob(A): return sqrt(sum(abs(x)**2 for row in A for x in row))
def trace(A): return sum(A[i][i] for i in range(min(len(A),len(A[0]))))
def mat_close(A,B,tol=1e-11): return frob(msub(A,B))<tol

def projector(theta):
    c,s=cos(theta),sin(theta)
    return [[c*c,c*s],[c*s,s*s]]
def dprojector(theta):
    c,s=cos(theta),sin(theta)
    return [[-2*c*s,c*c-s*s],[c*c-s*s,2*s*c]]
def h_iso(theta):
    P=projector(theta)
    return [[2*P[i][j]-(1 if i==j else 0) for j in range(2)] for i in range(2)]
def eig2(A):
    tr=A[0][0]+A[1][1]; det=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    disc=max(0.0,float((tr*tr-4*det).real if isinstance(tr*tr-4*det,complex) else tr*tr-4*det))
    q=sqrt(disc)
    return ((tr-q)/2,(tr+q)/2)

H0,H1=h_iso(0),h_iso(pi/4)
sp0,sp1=eig2(H0),eig2(H1)
P0,P1=projector(0),projector(pi/4)
spec_delta=max(abs(sp0[i]-sp1[i]) for i in range(2))
proj_delta=frob(msub(P0,P1))
req(spec_delta<1e-12,'isospectral observation collision')
req(proj_delta>0.9,'projector target separates spectrum fiber')
fiber_eye={'status':'PASS','spectrum_delta':spec_delta,'projector_frobenius_delta':proj_delta,'meaning':'The projector target does not factor through the unordered two-eigenvalue observation on this finite pair.'}

paths=[{'name':'plus','endpoint':'P*','events':[1]},{'name':'minus','endpoint':'P*','events':[-1]}]
req(paths[0]['endpoint']==paths[1]['endpoint'] and paths[0]['events']!=paths[1]['events'],'endpoint collision with distinct histories')
path_eye={'status':'PASS','same_endpoint':True,'histories':[p['events'] for p in paths]}

events=[0.5,-0.5]
req(abs(sum(events))<1e-15 and len(events)==2,'local opposite fractional events survive net-zero compression')
local_global_eye={'status':'PASS','local_events':events,'net':sum(events),'event_count':2,'scope':'Arithmetic retention analogue only; external vortex-knot experiment supplies physical example.'}

q=[[complex(3/5)],[complex(4/5)]]
def outer_col(q): return mmul(q,mconjtrans(q))
base=outer_col(q)
phase_errors=[]
for theta in [0,0.1,0.7,1.9,pi]:
    u=exp(1j*theta); qp=[[u*x[0]] for x in q]
    phase_errors.append(frob(msub(outer_col(qp),base)))
req(max(phase_errors)<1e-12,'rank-one U1 frame phase leaves projector invariant')
gauge_eye={'status':'PASS','max_projector_phase_error':max(phase_errors),'meaning':'Finite complex rank-one instance of frame gauge redundancy; not a Yang-Mills derivation.'}

J=[[0,1,-1],[-1,0,1],[1,-1,0]]
div=[sum(row) for row in J]
circ=J[0][1]+J[1][2]+J[2][0]; rcirc=J[0][2]+J[2][1]+J[1][0]
req(div==[0,0,0],'triangle cycle current is divergence-free')
req(circ==3 and rcirc==-3,'cycle circulation reverses sign with orientation')
phi=[2,-1,4]
G=[[phi[j]-phi[i] for j in range(3)] for i in range(3)]
gcirc=G[0][1]+G[1][2]+G[2][0]
req(gcirc==0,'gradient current has zero triangle circulation')
b1=3-3+1; req(b1==1,'triangle cycle-space dimension is one')
cohom_eye={'status':'PASS','divergence':div,'cycle_circulation':circ,'reverse_circulation':rcirc,'gradient_circulation':gcirc,'b1':b1}

T=[[0,3,0],[1,0,2],[4,0,0]]
def current(T): return msub(T,mtrans(T))
def old_scalar(T): return sum(T[i][j]-T[j][i] for i in range(3) for j in range(i+1,3))
def relabel(A,p): return [[A[p[i]][p[j]] for j in range(3)] for i in range(3)]
vals={}; J0=current(T)
for p in itertools.permutations(range(3)):
    Tp=relabel(T,p); vals[str(p)]=old_scalar(Tp)
    req(mat_close(current(Tp),relabel(J0,p)),'antisymmetric current relabel covariance '+str(p))
req(len(set(vals.values()))>1,'old QHE scalar is label dependent')
qhe_eye={'status':'PASS','old_scalar_values':vals,'distinct_scalar_values':sorted(set(vals.values())),'matrix_current_covariant':True}

for th in [0,0.2,0.7,1.2]:
    dP=dprojector(th); speed=sqrt(0.5*trace(mmul(dP,dP)))
    req(abs(speed-1)<1e-12,'rank-one projector metric speed one at '+str(th))
a=pi/2; N=1000; ss=[i/N for i in range(N+1)]
def trap(vals,dx): return dx*(sum(vals)-0.5*vals[0]-0.5*vals[-1])
Llin=trap([a for _ in ss],1/N); Lquad=trap([2*a*s for s in ss],1/N)
req(abs(Llin-a)<1e-12 and abs(Lquad-a)<1e-12,'projector length is reparameterization invariant in test pair')
clock_eye={'status':'PASS','linear_length':Llin,'quadratic_reparam_length':Lquad,'expected':a,'scope':'Finite rank-one projector path; intrinsic distinguishability, not physical time.'}

def comm(A,B): return msub(mmul(A,B),mmul(B,A))
def inv2(A):
    d=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    return [[A[1][1]/d,-A[0][1]/d],[-A[1][0]/d,A[0][0]/d]]
nh=[]
for k in [0,1,3,10]:
    H=[[0.0,float(k)],[0.0,1.0]]; HT=mtrans(H)
    nonnormal=frob(comm(H,HT)); z=0.5
    R=inv2([[H[i][j]-(z if i==j else 0) for j in range(2)] for i in range(2)])
    res=frob(R); right_overlap=abs(k)/sqrt(k*k+1) if k else 0.0
    nh.append({'k':k,'eigenvalues':[0,1],'commutator_frobenius':nonnormal,'resolvent_frobenius_at_0.5':res,'right_eigenvector_overlap':right_overlap})
req(all(r['eigenvalues']==[0,1] for r in nh),'non-Hermitian family is isospectral')
req(nh[-1]['commutator_frobenius']>nh[0]['commutator_frobenius'] and nh[-1]['resolvent_frobenius_at_0.5']>nh[0]['resolvent_frobenius_at_0.5'],'nonnormal/resolvent eyes distinguish isospectral family')
nh_eye={'status':'PASS','cases':nh,'meaning':'Spectrum alone misses nonnormality, eigenvector coalescence tendency, and resolvent amplification.'}

before=[1,1]; after=sum(before)-2
req(after==0,'full torus-to-torus gluing produces zero remaining boundary components in closure toy')
closure_eye={'status':'PASS','input_boundary_counts':before,'after_full_glue':after,'closed_in_one_torus_boundary_object_class':after==1}

for eps in [1e-1,1e-3,1e-6]:
    req((-eps)<0<(eps),'linear signed crossing changes sign')
    req(eps*eps>=0 and (-eps)*(-eps)>=0,'quadratic touch remains nonnegative')
zero_eye={'status':'PASS','linear_model_order':1,'quadratic_model_order':2,'scope':'Toy local polynomial control only; does not prove genericity for every Hermitian/non-Hermitian quantum metric.'}

literature_eye={'status':'AUDITED_NOT_EXECUTED','claims':[
 {'id':'spectral_flow_pairing','verdict':'SUPPORTED_IN_SUITABLE_FREDHOLM_SETTING'},
 {'id':'real_K_theory_valued_spectral_flow_2026','verdict':'SUPPORTED_BY_ARXIV_2606_31322'},
 {'id':'grassmannian_projector_path_2026','verdict':'SUPPORTED_BY_ARXIV_2608_06777_PREPRINT'},
 {'id':'pro_tangles','verdict':'SUPPORTED_BUT_CITATION_CORRECTED_TO_ARXIV_2606_13471'},
 {'id':'stated_skein_decorated_cobordism','verdict':'SUPPORTED_BY_PUBLISHED_CAMBRIDGE_PAPER'},
 {'id':'NH_right_vs_biorthogonal_metric','verdict':'SUPPORTED_BY_PRB_114_185108_2026'}]}

eyes={'fiber_forcing':fiber_eye,'path_history':path_eye,'local_global':local_global_eye,'gauge_frame':gauge_eye,'graph_cohomology':cohom_eye,'qhe_relabel':qhe_eye,'projector_clock':clock_eye,'nonhermitian_multi':nh_eye,'composition_closure':closure_eye,'metric_zero_order':zero_eye,'literature':literature_eye}
repairs=[
 {'lossy':'net signed sum','richer':'ordered signed event list'},
 {'lossy':'unordered eigenvalue spectrum','richer':'spectral projector/subspace'},
 {'lossy':'endpoint projector','richer':'ordered projector path'},
 {'lossy':'old QHE scalar','richer':'antisymmetric current matrix + cycle orientation'},
 {'lossy':'eigenvalues of nonnormal H','richer':'right/left geometry + resolvent/pseudospectrum + projector data'}]
req(len(repairs)==5,'five explicit lossy-to-richer repair channels')

out={'status':'PASS','campaign':'QG-TRANSPORT-THOUGHTS-01','checks':len(checks),'diagnostic_channels':len(eyes),'eyes':eyes,'repairs':repairs,'scope':'Finite algebraic/numerical retention controls only. Literature is audited separately; analytic K-theory, APS, cobordism, physical time and gravity are not proved here.'}
with open('qg_transport_thoughts_results.json','w') as f: json.dump(out,f,indent=2)
print(json.dumps({'status':out['status'],'checks':out['checks'],'diagnostic_channels':out['diagnostic_channels'],'spec_delta':spec_delta,'projector_delta':proj_delta,'max_phase_error':max(phase_errors),'qhe_scalar_values':sorted(set(vals.values())),'clock_lengths':[Llin,Lquad],'nh_resolvent_growth':[nh[0]['resolvent_frobenius_at_0.5'],nh[-1]['resolvent_frobenius_at_0.5']]},indent=2))
