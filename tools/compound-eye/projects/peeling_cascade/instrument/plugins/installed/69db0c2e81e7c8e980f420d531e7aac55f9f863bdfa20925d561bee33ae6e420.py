"""Scoped knot/phase/field diagnostics. No inferred atom labels or fitted constants."""
import math,itertools
import numpy as np
import sympy as s
import mpmath as mp

def stop(reason):return {'_status':'blocked','reason':reason}
def data(inputs):return inputs['case']
def finite(x):return np.all(np.isfinite(np.asarray(x,dtype=float)))
def torus(inputs,*args):
    d=data(inputs);p,q=d['p'],d['q']
    if not all(type(v)is int and v>1 for v in [p,q]) or math.gcd(p,q)!=1:return stop('Coprime positive torus-knot parameters >1 required.')
    t=s.symbols('t');poly=s.cancel((t**(p*q)-1)*(t-1)/((t**p-1)*(t**q-1)))
    return {'torus_parameters':[p,q],'crossing_number':min((p-1)*q,(q-1)*p),'genus':(p-1)*(q-1)//2,'Alexander':str(s.expand(poly)),'determinant':int(abs(poly.subs(t,-1))),'hyperbolic_complement':False,'hyperbolic_volume':None,'simplicial_volume':0,'scope':'Exact torus family formulas; geometric material volume is not assigned.'}

def recipe(inputs,*args):
    d=data(inputs);p,q=d['p'],d['q'];r=torus(inputs)
    if '_status'in r:return r
    # |z|^p=|w|^q and |z|²+|w|²=1, with opposite phases.
    lo,hi=0.,1.
    for _ in range(80):
        a=(lo+hi)/2
        if a**p>(1-a*a)**(q/2):hi=a
        else:lo=a
    a=(lo+hi)/2;b=np.sqrt(1-a*a);theta=np.linspace(0,2*np.pi,1201)
    z=a*np.exp(1j*q*theta);w=b*np.exp(1j*(p*theta+np.pi/q))
    return {'p':p,'q':q,'radius_z':a,'radius_w':float(b),'zero_residual':float(np.max(abs(z**p+w**q))),'sphere_residual':float(np.max(abs(abs(z)**2+abs(w)**2-1))),'scope':'Designed algebraic zero set on S³. No dynamical selection or material stability calculation.'}

def rational_degree(inputs,*args):
    d=data(inputs);p,q,alpha=d['p'],d['q'],d['alpha']
    r=torus({'case':d})
    if '_status'in r:return r
    if type(alpha)is not int or alpha<1:return stop('Positive integer alpha required; this independent root-count check fixes beta=1.')
    eps=1e-4;Q=alpha*q+p
    # P=z^alpha*w=eps, denominator z^p+w^q=0.
    z=eps**(q/Q)*np.exp(1j*(np.pi+2*np.pi*np.arange(Q))/Q);w=eps/z**alpha
    residual=max(np.max(abs(z**alpha*w-eps)),np.max(abs(z**p+w**q)))
    jac=alpha*q*z**(alpha-1)*w**q-p*z**(alpha+p-1)
    return {'Hopf_charge_formula':Q,'generic_preimage_count':len(z),'max_B4_radius_squared':float(max(abs(z)**2+abs(w)**2)),'min_complex_jacobian_modulus':float(min(abs(jac))),'equation_residual':float(residual),'denominator_knot':[p,q],'scope':'Sutcliffe rational-map ansatz beta=1. Count verifies degree at a regular small target; not a nematic equilibrium or 3D Hopf integral.'}

def fox_core(d):
    u,t=s.symbols('u t');I=s.eye(2);X=s.Matrix([[1,1],[0,1]]);Y=s.Matrix([[1,0],[u,1]])
    if d.get('corrupt',False):Y[1,0]=u+1
    C=s.Matrix(d.get('basis',[[1,0],[0,1]]))
    if C.det()==0:raise ValueError('Invertible coefficient basis required.')
    reps={1:C*X*C.inv(),2:C*Y*C.inv()}
    left=[1,-2,-1,2,1];right=[2,1,-2,-1,2];rel=left+[-v for v in right[::-1]]
    if d.get('move')=='inverse':rel=[-v for v in rel[::-1]]
    if d.get('move')=='conjugate':rel=[1]+rel+[-1]
    def red(v):return s.factor(s.rem(s.expand(v),u*u-u+1,u))
    P=I;Ds={1:s.zeros(2),2:s.zeros(2)}
    for a in rel:
        M=(t if a>0 else 1/t)*(reps[abs(a)] if a>0 else reps[abs(a)].inv())
        Ds[abs(a)]+=P if a>0 else -P*M;P=P*M
    relation=(P-I).applyfunc(red)==s.zeros(2)
    chain=(Ds[1]*(t*reps[1]-I)+Ds[2]*(t*reps[2]-I)).applyfunc(red)==s.zeros(2)
    deleted=d.get('deleted',2)
    if deleted not in [1,2]:raise ValueError('Deleted generator is 1 or 2.')
    tau=s.factor(red(Ds[3-deleted].det())/red((t*reps[deleted]-I).det())) if relation and chain else None
    return relation,chain,tau,t
def fox(inputs,*args):
    relation,chain,tau,t=fox_core(data(inputs))
    if not relation or not chain:return stop('Representation/group relation or twisted chain identity fails; torsion not admitted.')
    return {'relation':relation,'boundary_squared_zero':chain,'torsion':str(tau),'scope':'Figure-eight standard SL(2,C) two-dimensional twist; not adjoint torsion.'}
def moves(inputs,*args):
    d=data(inputs);r,c,tau,t=fox_core(d)
    if not r or not c:return stop('Invalid representation.')
    ratio=s.factor(tau/((t*t-4*t+1)/t**2))
    return {'ratio_to_fixed_reference':str(ratio),'allowed_unit':ratio in [1,-1,t*t,-t*t,t**-2,-t**-2],'scope':'Specified presentation/basis controls, not arbitrary diagram moves.'}
def branch(inputs,*args):
    u=s.symbols('u');roots=[(1+s.sqrt(3)*s.I)/2,(1-s.sqrt(3)*s.I)/2]
    return {'peripheral_eigenvalues_equal':True,'peripheral_pair':[-1,1],'character_traces':[str(2-r) for r in roots],'different_characters':s.simplify(roots[0]-roots[1])!=0,'standard_twisted_polynomial_distinguishes':False,'scope':'Exact fixed figure-eight witness; not injectivity of a general invariant package.'}

def jvalue(N,xi):
    term=mp.mpc(1);v=term
    for k in range(1,N):term*=2*mp.cosh(xi)-2*mp.cosh(k*xi/N);v+=term
    return v
def jones(inputs,*args):
    d=data(inputs);N=d['N']
    if type(N)is not int or not 1<=N<=5000:return stop('Integer color 1..5000 required.')
    with mp.workdps(70):
        if d['regime']=='root_unity':
            v=mp.mpf(1);term=v
            for k in range(1,N):term*=4*mp.sin(mp.pi*k/N)**2;v+=term
            return {'log_abs_J':float(mp.log(v)),'volume_estimator':float(2*mp.pi*mp.log(v)/N),'scope':'Finite figure-eight root-of-unity evaluation, not a volume theorem.'}
        if d['regime']!='small_xi':return stop('Unknown asymptotic regime.')
        xi=mp.mpc(*d['xi']);v=jvalue(N,xi);target=1/(3-2*mp.cosh(xi))
        return {'J':[float(v.real),float(v.imag)],'Alexander_limit_error':float(abs(v-target)),'scope':'Finite evaluation and comparison; domain is not proved by this eye.'}
def saddle(inputs,*args):
    if data(inputs).get('knot')!='4_1':return stop('This dilogarithm saddle calibration is for 4_1 only; no torus-knot substitution.')
    with mp.workdps(45):
        v=2*mp.im(mp.polylog(2,mp.exp(mp.j*mp.pi/3)))
        integ=4*mp.pi*mp.quad(lambda x:mp.log(2*mp.sin(mp.pi*x)),[0,mp.mpf(1)/6,mp.mpf(5)/6])
        return {'volume':float(v),'quadrature_discrepancy':float(abs(v-integ)),'stationary_s':5/6,'second_derivative':float(-2*mp.pi*mp.sqrt(3)),'scope':'Specified figure-eight potential, not a universal energy.'}
def winding(inputs,*args):
    d=data(inputs);z=np.array([complex(*v) for v in d['values']]);a=z[:-1];b=z[1:];v=b-a
    if len(z)<4 or not np.isfinite(z).all() or abs(z[0]-z[-1])>1e-12:return stop('Finite explicitly closed complex polygon required.')
    vv=abs(v)**2;u=np.divide(-(a.conjugate()*v).real,vv,out=np.zeros(len(v)),where=vv>0)
    gap=float(min(abs(a+np.clip(u,0,1)*v)))
    if gap<=1e-10:return stop('Path reaches or cannot resolve separation from zero.')
    w=float(np.sum(np.angle(b/a))/(2*np.pi))
    return {'winding':round(w),'unrounded':w,'segment_clearance':gap,'scope':'Supplied polygon; phase lift depends on path. Not arbitrary-curve sampling certification.'}
def eta(inputs,*args):
    a=float(data(inputs)['a']);f=a-math.floor(a);integer=abs(f)<1e-12
    value=0. if integer else 1-2*f
    hurwitz=0. if integer else float(mp.zeta(0,f)-mp.zeta(0,1-f))
    return {'eta':value,'Hurwitz_zeta_check':hurwitz,'kernel_dimension':int(integer),'reduced_eta':.5 if integer else .5-f,'scope':'Exact zeta-regularized circle formula for eigenvalues n+a, with a numerical integer tolerance.'}
def spectral_flow(inputs,*args):
    d=data(inputs);a,b=d['a'],d['b']
    if any(abs(v-round(v))<1e-10 for v in [a,b]):return stop('Invertible endpoints required by this convention.')
    sf=math.floor(b)-math.floor(a);delta=eta({'case':{'a':b}})['reduced_eta']-eta({'case':{'a':a}})['reduced_eta']
    return {'spectral_flow':sf,'eta_change':delta,'local_term':-(b-a),'balance_residual':delta+(b-a)-sf,'scope':'Circle n+a along linear path; no general continuum spectral-flow computation.'}
def chiral(inputs,*args):
    A=np.array(data(inputs)['A'],dtype=float);m,n=A.shape;H=np.block([[np.zeros((m,m)),A],[A.T,np.zeros((n,n))]])
    vals=np.linalg.eigvalsh(H);tol=max(np.linalg.norm(H,2)*1e-10,1e-14);h=int(sum(abs(vals)<=tol))
    return {'eigenvalues':vals.tolist(),'eta_finite':int(sum(vals>tol)-sum(vals< -tol)),'kernel_dimension':h,'pairing_residual':float(max(abs(vals+vals[::-1]))),'scope':'Finite Hermitian chiral matrix; kernel is separate from eta.'}
def cs(inputs,*args):
    d=data(inputs);level=d['level'];shift=d['integer_shift']
    if type(shift)is not int:return stop('Declared gauge shift must be integer.')
    return {'phase_shift_modulus':float(abs(np.exp(2j*np.pi*level*shift)-1)),'scope':'Bare exp(2πik CS) convention; no spin/refined CS theory implemented.'}
def potential(inputs,*args):
    d=data(inputs);eps=d['epsilon'];val=d['A_value']
    if eps<=0:return stop('Positive regulator required.')
    return {'regularized_value':float(np.log(abs(val)+eps)),'constant_on_defining_zero_set':True,'scope':'log(|A|+epsilon) is constant when A=0; not an action on that curve.'}

def braid_jones_value(word,n):
    if n<1 or any(type(v)is not int or v==0 or abs(v)>=n for v in word) or len(word)>12:raise ValueError('Valid braid up to 12 crossings required.')
    A=s.symbols('A');delta=-A*A-A**-2;total=0;m=len(word)
    for mask in range(1<<m):
        parent=list(range((m+1)*n))
        def root(x):
            while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
            return x
        def join(a,b):parent[root(a)]=root(b)
        power=0
        for k,g in enumerate(word):
            i=abs(g)-1;e=(mask>>k)&1;sign=1 if g>0 else -1;power+=sign*(1-2*e)
            for j in range(n):
                if not e or j not in [i,i+1]:join(k*n+j,(k+1)*n+j)
            if e:join(k*n+i,k*n+i+1);join((k+1)*n+i,(k+1)*n+i+1)
        for j in range(n):join(j,m*n+j)
        loops=len({root(j) for j in range((m+1)*n)})
        total+=A**power*delta**(loops-1)
    poly=s.expand(total*(-A**3)**(-sum(1 if v>0 else -1 for v in word)))
    return str(poly)
def braid_jones(inputs,*args):
    d=data(inputs)
    return {'Jones_in_A':braid_jones_value(d['word'],d['strands']),'q_convention':'q=A^-4','scope':'Exact Kauffman state sum of a closed oriented braid, ≤12 crossings. Equality is not a complete knot identifier.'}
def braid_move(inputs,*args):
    d=data(inputs);w=d['before'];v=d['after'];kind=d['move'];i=d.get('index',0);valid=False
    if kind=='RII':valid=w[:i]+w[i+2:]==v and len(w)>=i+2 and w[i]==-w[i+1]
    if kind=='RIII':
        block=w[i:i+3];valid=len(block)==3 and block[0]==block[2] and abs(abs(block[0])-abs(block[1]))==1 and block[0]*block[1]>0 and v==w[:i]+[block[1],block[0],block[1]]+w[i+3:]
    if kind=='Markov_stabilize':valid=v==w+[d['strands']] or v==w+[-d['strands']]
    return {'local_move_valid':bool(valid),'scope':'Braid RII, same-sign RIII, or signed Markov stabilization of closure. No reconnection accepted as isotopy.'}

def linking(inputs,*args):
    d=data(inputs);a=np.array(d['curve1'],float);b=np.array(d['curve2'],float)
    if not finite(a) or not finite(b) or a.ndim!=2 or b.ndim!=2 or a.shape[1]!=3 or b.shape[1]!=3:return stop('Finite 3D polygon arrays required.')
    if not np.allclose(a[0],a[-1]) or not np.allclose(b[0],b[-1]):return stop('Closed curves required.')
    da=np.diff(a,axis=0);db=np.diff(b,axis=0);ma=(a[:-1]+a[1:])/2;mb=(b[:-1]+b[1:])/2;value=0.;gap=float('inf')
    for x,dx in zip(ma,da):
        r=x-mb;norm=np.linalg.norm(r,axis=1);gap=min(gap,float(min(norm)))
        if min(norm)<1e-10:return stop('Unresolved/intersecting curves.')
        value+=sum(np.einsum('ij,ij->i',r,np.cross(dx,db))/norm**3)
    return {'gauss_midpoint_estimate':float(value/(4*np.pi)),'midpoint_clearance':gap,'scope':'Quadrature estimate; requires resolution convergence. Not a general segment-intersection certificate or 3D field Hopf integral.'}
def nematic_energy(inputs,*args):
    d=data(inputs);theta=np.asarray(d['theta'],float);L=d['L'];K=d['K'];q=d['q0'];electric=d['electric_strength']
    if len(theta)<3 or not finite(theta) or L<=0 or K<=0:return stop('Finite lifted angles, L>0, K>0 required.')
    dx=L/(len(theta)-1);slope=np.diff(theta)/dx;mid=(theta[1:]+theta[:-1])/2
    elastic=.5*K*np.sum((slope-q)**2)*dx;elect=-.5*electric*np.sum(np.cos(mid)**2)*dx
    return {'elastic':float(elastic),'electric':float(elect),'total':float(elastic+elect),'end_twist_turns':float((theta[-1]-theta[0])/(2*np.pi)),'scope':'1D helical director ansatz with transverse electric field, fixed lifted endpoint angles. Not 3D heliknoton energy.'}
def optical_jones(inputs,*args):
    d=data(inputs);J=np.eye(2,dtype=complex)
    for angle,ret in d['layers']:
        R=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        J=(R@np.diag([np.exp(.5j*ret),np.exp(-.5j*ret)])@R.T)@J
    e=np.array([complex(*v) for v in d['incident']]);out=J@e
    return {'field':[[float(v.real),float(v.imag)] for v in out],'intensity':float(np.vdot(out,out).real),'unitarity_error':float(np.linalg.norm(J.conj().T@J-np.eye(2))),'scope':'Lossless layered optical Jones matrices. Jones optical matrices are not Jones knot polynomials.'}
def aps_admission(inputs,*args):
    d=data(inputs);issues=[]
    if not d.get('self_adjoint_operator'):issues.append('self-adjoint operator/domain not supplied')
    if not d.get('boundary_conditions'):issues.append('boundary conditions missing')
    if not d.get('regularization'):issues.append('spectral regularization missing')
    if d.get('representation')=='SL2C_hyperbolic':issues.append('non-unitary twist requires a compatible analytic construction')
    return {'admitted_by_metadata':not issues,'issues':issues,'scope':'Assumption checklist only; metadata cannot certify an operator theorem.'}

def homfly(inputs,*args):
    if data(inputs).get('knot')!='8_19':return stop('Only the published 8_19 HOMFLY calibration is supplied.')
    a,z,r=s.symbols('a z r');P=z**6/a**6+6*z**4/a**6-z**4/a**8+10*z**2/a**6-5*z**2/a**8+5/a**6-5/a**8+1/a**10
    alex=s.expand(P.subs({a:1,z:r-1/r}));jones=s.expand(P.subs({a:r**-2,z:r-1/r}))
    return {'Alexander_in_r':str(alex),'Jones_in_r':str(jones),'t_and_q':'r²','scope':'Exact specializations of a sourced HOMFLY polynomial. Not an arbitrary HOMFLY generator, a colored-Jones tower, or eta phase locking.'}
def spin_response(inputs,*args):
    T=np.asarray(data(inputs)['spin_transmission'],float)
    if T.shape!=(2,) or not finite(T) or min(T)<0:return stop('Two nonnegative spin-resolved transmissions required.')
    total=float(sum(T))
    if total==0:return stop('Polarization undefined at zero total transmission.')
    return {'total_transmission':total,'spin_polarization':float((T[0]-T[1])/total),'scope':'Declared transmission data; no knot Hamiltonian or CISS mechanism inferred.'}
