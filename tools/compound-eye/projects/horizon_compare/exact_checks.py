"""Exact symbolic identities. These are not Lean/kernel-certified proofs."""
import sympy as s

def verify():
    a,q,d,x,y,t1,t2,t3=s.symbols('a q d x y t1 t2 t3',real=True)
    z=1-x-y;aa=t1-t2;S=t1+t2-2*t3
    A=s.Matrix([[t1+t2-aa*(x-y),(aa-S*(x-y))/s.sqrt(3)],[s.sqrt(3)*aa*z,2*t3+S*z]])
    E=s.Matrix([[1,-1,0],[1/s.sqrt(3),1/s.sqrt(3),-2/s.sqrt(3)]])/s.sqrt(2)
    g=E*s.diag(1/(4*x),1/(4*y),1/(4*z))*E.T
    simplify=lambda M:M.applyfunc(s.simplify)
    checks={}
    checks['shape_operator_selfadjoint_in_quotient_metric']=simplify(g*A-A.T*g)==s.zeros(2)
    Aq=A.subs({x:(1-q*q+d)/2,y:(1-q*q-d)/2},simultaneous=True)
    J=s.diag(1/s.sqrt(2),-s.sqrt(6)*q)
    B=s.Matrix([[t1+t2-aa*d,-2*q*(aa-S*d)],[-aa*q/2,2*t3+q*q*S]])
    checks['signed_tangent_intertwining_off_wall']=simplify(Aq*J-J*B)==s.zeros(2)
    checks['lifted_limit_scalar_on_jordan_condition']=simplify(B.subs(q,0).subs(t3,(t1+t2-aa*d)/2)-(t1+t2-aa*d)*s.eye(2))==s.zeros(2)
    w=s.Matrix([a*(1-q*q),(1-a)*(1-q*q),q*q])
    metric=s.factor(sum(s.diff(v,q)**2/(4*v) for v in w))
    checks['horizontal_path_metric_qq']=s.simplify(metric-1/(1-q*q))==0
    checks['finite_length_primitive']=s.simplify(s.diff(s.asin(q),q)-1/s.sqrt(1-q*q))==0
    checks['gram_path_even_in_signed_coordinate']=w.subs(q,-q)==w
    b,c,zz=s.symbols('b c zz')
    L=s.Matrix([[-1,0],[c,-b]]);C=s.Matrix([[1,0]])
    checks['one_way_exterior_observability_rank_one']=C.col_join(C*L).rank()==1
    R=(zz*s.eye(2)-L).inv()
    checks['one_way_exterior_resolvent_independent_of_hidden_rate']=s.simplify(R[0,0]-1/(zz+1))==0
    omega,energy=s.symbols('omega energy',positive=True)
    amp=s.sqrt(2*energy)/omega
    checks['fixed_energy_velocity_amplitude_constant']=s.simplify(omega*amp-s.sqrt(2*energy))==0
    assert all(checks.values()),checks
    return {'status':'pass','kind':'exact_symbolic_checks','checks':checks,
      'domain':'Positive Gram eigenvalues for metric identities; q!=0 for similarity, smooth limit evaluated separately; 0<a<1 and |q|<1 for path.',
      'formal_status':'SymPy simplification and exact finite linear algebra; no new Lean proof.'}

if __name__=='__main__':
    import json
    print(json.dumps(verify(),indent=2))
