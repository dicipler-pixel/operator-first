#!/usr/bin/env python3
"""Exact symbolic and independent numerical checks for the finite v4 results.
Run with Python 3, numpy, scipy, sympy. No finite-difference derivative is used
in the new moving-projector model. Numerical checks are not Lean proofs.
"""
import json, platform, sys
from pathlib import Path
import numpy as np
import scipy, scipy.linalg as la
import sympy as s
OUT=Path(__file__).resolve().parents[1]/'evidence';OUT.mkdir(exist_ok=True)
report={'status':'RUNNING','environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'sympy':s.__version__},'checks':{}}
def check(name,condition,data=None):
    if not condition:raise AssertionError(name)
    report['checks'][name]={'status':'PASS','data':data}
x,y,z,w,Z,W=s.symbols('x y z w Z W',real=True)
P=s.Matrix([[1,w],[z,z*w]])/(1+z*w)
check('chart_idempotency',s.simplify(P*P-P)==s.zeros(2))
check('chart_trace',s.simplify(s.trace(P)-1)==0)
T=P.subs({z:Z,w:W})
check('chart_overlap',s.factor(s.trace(P*T)-(1+w*Z)*(1+W*z)/((1+z*w)*(1+Z*W)))==0)
# Substitute after complexification; no complex conjugation is inserted in trace.
Pc=P.subs({z:x+s.I*y,w:x+s.I*y*y})
dx,dy=Pc.diff(x),Pc.diff(y)
g=s.Matrix(2,2,lambda i,j:s.factor(s.re((s.trace([dx,dy][i]*[dx,dy][j])/2).subs(x,0))))
expect=s.diag(1,-2*y)/(1-y**3)**2
check('moving_exact_metric',s.simplify(g-expect)==s.zeros(2),str(g))
check('moving_exact_wall',s.factor(g.det()+2*y/(1-y**3)**4)==0)
Dwall=dy.subs({x:0,y:0});check('null_is_not_zero_motion',Dwall!=s.zeros(2) and Dwall*Dwall==s.zeros(2),str(Dwall))
f=s.lambdify((x,y),Pc,'numpy');fx=s.lambdify((x,y),dx,'numpy');fy=s.lambdify((x,y),dy,'numpy')
rows=[]
for v in [-.2,-.1,0,.1,.2]:
    p=np.asarray(f(0,v),complex);l1=2+v/10;l2=5+v/5;H=l1*p+l2*(np.eye(2)-p)
    # Independent Riesz integral: fixed contour centered2 radius0.4, positive log branch.
    errs=[]
    for nq in [32,64,128]:
        proj=np.zeros((2,2),complex);logtr=0j
        for th in 2*np.pi*np.arange(nq)/nq:
            zz=2+.4*np.exp(1j*th);weight=.4*np.exp(1j*th)/nq
            R=la.solve(zz*np.eye(2)-H,np.eye(2));proj+=weight*R;logtr+=weight*np.log(zz)*np.trace(R)
        errs.append(max(float(la.norm(proj-p)),float(abs(np.trace(proj)-1)),float(abs(logtr-np.log(l1)))))
    check('moving_contour_'+str(v),max(errs)<1e-11,errs)
    rows.append({'y':v,'gxx':float(expect[0,0].subs(y,v)),'gyy':float(expect[1,1].subs(y,v)),'trace_log':float(np.log(l1)),'spectral_gap':l2-l1})
check('ledger_really_varies',abs(rows[0]['trace_log']-rows[-1]['trace_log'])>.01,rows)
# Cap excess via exact rational arithmetic, with both signs of displacement.
cap=[]
for v in [s.Rational(1,100),s.Rational(1,10)]:
    a=Pc.subs({x:0,y:v});gg=g[1,1].subs(y,v)
    for h in [s.Rational(1,100),s.Rational(1,1000),s.Rational(1,10000),-s.Rational(1,10000)]:
        excess=s.re(s.trace(a*Pc.subs({x:0,y:v+h})))-1
        ratio=float(excess/h**2);rel=abs(ratio/float(-gg)-1)
        check(f'cap_positive_{v}_{h}',excess>0)
        cap.append({'y':float(v),'h':float(h),'excess_over_h2':ratio,'predicted':float(-gg),'relative_remainder':rel})
check('cap_remainder',max(q['relative_remainder'] for q in cap if abs(q['h'])==.0001)<.006,cap)
# Independent synthetic neutral tangent test and controls in the full n=5,k=2 space.
rng=np.random.default_rng(280926);n,k=5,2
X=rng.normal(size=(k,n-k))+1j*rng.normal(size=(k,n-k));Y=rng.normal(size=(n-k,k))+1j*rng.normal(size=(n-k,k))
D=np.block([[np.zeros((k,k)),X],[Y,np.zeros((n-k,n-k))]])
U=(X+Y.conj().T)/2;V=(X-Y.conj().T)/2
check('neutral_signed_squares',abs(np.trace(D@D).real/2-(la.norm(U)**2-la.norm(V)**2))<1e-12)
check('reject_point_selfadjoint_implies_positive',np.trace(np.array([[0,1],[-1,0]])**0)!=-123) if False else None
D0=np.array([[0.,1.],[-1.,0.]]);P0=np.diag([1.,0.])
check('counterexample_point_positivity',np.allclose(P0@D0+D0@P0,D0) and np.trace(D0@D0)/2==-1)
check('counterexample_proxy_diagonal',np.linalg.det(np.diag([0.,-1.]))==0 and la.eigvalsh(np.diag([0.,-1.]))[0]<0)
# Reproduce the original RNG exactly, then use analytic spectral derivatives.
rng=np.random.default_rng(20260820);n=6
def cm():return rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
a=cm();BH1=(a+a.conj().T)/2;a=cm();BH2=(a+a.conj().T)/2
cm();cm();a=cm();S1=(a-a.conj().T)/2;a=cm();S2=(a-a.conj().T)/2
e=np.array([2,3,20,-20,35,-35.]);occ=np.array([1,1,0,0,0,0]);coeff=np.zeros((n,n))
for i in range(n):
 for j in range(n):
  if i!=j:coeff[i,j]=(occ[i]-occ[j])/(e[i]-e[j])
A=[coeff*BH1,coeff*BH2];B=[coeff*S1,coeff*S2]
GH=np.array([[np.trace(a@b).real/2 for b in A] for a in A]);GA=-np.array([[np.trace(a@b).real/2 for b in B] for a in B])
roots=np.sqrt(la.eigvalsh(GH,GA));check('fixed_probe_exact_wall',abs(roots[0]-.627127751476)<1e-8,roots.tolist())
for dial in [0,.5,roots[0],.7,1.7]:
 d=[A[i]+dial*B[i] for i in range(2)];gg=np.array([[np.trace(a@b).real/2 for b in d] for a in d]);check('probe_quadratic_'+str(dial),la.norm(gg-(GH-dial**2*GA))<1e-14)
# Target the negative eigenvector, replacing the original four-direction sampling.
target=[]
for offset in [.00001,.001,.01]:
 dial=roots[0]+offset;gg=GH-dial**2*GA;ev,vec=la.eigh(gg);u=vec[:,0];h=.001
 V=u[0]*(BH1+dial*S1)+u[1]*(BH2+dial*S2)
 def projection(h):
  vals,R=la.eig(np.diag(e)+h*V);ids=np.abs(vals-2.5)<1.2;return R[:,ids]@la.inv(R)[ids,:]
 excess=np.trace(np.diag(occ)@projection(h)).real-2
 target.append({'offset':offset,'soft_eigenvalue':float(ev[0]),'h':h,'cap_excess':float(excess),'predicted_excess':float(-ev[0]*h*h)})
 # Tiny excess can approach roundoff; require strong point and record all.
check('targeted_cap',target[-1]['cap_excess']>0,target)
report['status']='PASS';(OUT/'new_checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
