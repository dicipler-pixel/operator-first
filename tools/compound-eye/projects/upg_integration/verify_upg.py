"""Independent controls; optional execution through the complete Compound Eye registry.
python verify_upg.py [--instrument-root PATH] [--output PATH]
Standalone layout expects upg_eyes.py beside this file, or ../../extensions/upg_eyes.py.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
import numpy as np
from scipy.linalg import block_diag

HERE=Path(__file__).resolve().parent
plugin=HERE/'upg_eyes.py'
if not plugin.exists(): plugin=HERE.parent.parent/'extensions/upg_eyes.py'
spec=importlib.util.spec_from_file_location('upg_eyes',plugin);eyes=importlib.util.module_from_spec(spec);spec.loader.exec_module(eyes)
METHODS=['redistribution_memory','spectral_susceptibility','gluing_sign','nct_anchor','signature_flow']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--instrument-root',type=Path);ap.add_argument('--output',type=Path,default=HERE/'verification.json');a=ap.parse_args()
    rows=[];root=a.instrument_root
    if root:
        root=root.resolve();sys.path.insert(0,str(root));import machine
        registry=machine.Registry(root);old={k:machine.digest(v) for k,v in registry.eyes.items()}
        for f in METHODS:
            key='ce.upg.'+f+'@1.0.0'
            if key not in registry.eyes:
                registry.add({'id':'ce.upg.'+f,'version':'1.0.0','title':f.replace('_',' ').title(),'family':'Projector and boundary integration','status':'implemented','inputs':{'case':'*'},'depends_on':[],
                'assumptions':['Finite declared matrices; units, inner product and physical interpretation supplied separately.'],
                'output_meaning':'Guarded diagnostic for UPG and peeling; see function-specific output scope.','evidence_class':'explicit_per_request','limits':'A passed identity is not a fit to atomic, electrical or cosmological data.',
                'implementation':{'path':'extensions/upg_eyes.py','sha256':hashlib.sha256(plugin.read_bytes()).hexdigest(),'function':f}},code=plugin)
        if 'ce.set.upg@1.0.0' not in registry.sets: registry.add_set({'id':'ce.set.upg','version':'1.0.0','title':'UPG guarded integration','eyes':['ce.upg.'+f+'@1.0.0' for f in METHODS]})
        assert all(machine.digest(registry.eyes[k])==v for k,v in old.items())
        template=json.loads((root/'projects/peeling_cascade/template.json').read_text())
    def run(f,c,block=False,label='Declared mathematical control'):
        if root:
            req=copy.deepcopy(template);req['context']['object_id']=label;req['context']['source']={'kind':'theoretical','id':label};req['inputs']={'case':{'unit':'declared_dimensionless_control','value':c}}
            res=machine.execute(req,['ce.upg.'+f+'@1.0.0'],root=root,workers=1)['results'][-1]
        else:
            v=getattr(eyes,f)({'case':c});res={'status':'blocked','reason':v['reason']} if v.get('_status')=='blocked' else {'status':'ok','value':v}
        assert res['status']==('blocked' if block else 'ok'),res
        rows.append({'eye':f,'label':label,'case':c,'result':res});return res.get('value',{})
    rng=np.random.default_rng(20260907)
    E=eyes.enc
    for n in [2,3,5,8]:
        for trial in range(20):
            k=1+trial%(n-1);Z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));U,_=np.linalg.qr(Z);P=U[:,:k]@U[:,:k].conj().T
            Z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));H=(Z+Z.conj().T)/2
            v=run('redistribution_memory',{'H':E(H),'P':E(P),'times':[0,.1,1]})
            assert v['identity_residual']<1e-9 and v['K0_min_eigenvalue']>-1e-9
            assert abs(v['redistribution_norm']-v['commutator_norm'])<1e-9
            if trial==0:
                Q=np.eye(n)-P;h=P@H@P+Q@H@Q
                assert run('redistribution_memory',{'H':E(h),'P':E(P)})['feedback_numerically_zero']
    run('redistribution_memory',{'H':[[0,1],[0,0]],'P':[[1,0],[0,0]]},True,'One-way non-Hermitian coupling excluded')
    run('redistribution_memory',{'H':[[1,0],[0,2]],'P':[[1,1],[0,0]]},True,'Oblique idempotent excluded')
    # Nonzero coupling at time zero can recur to zero later without vanishing identically.
    H=np.array([[0,1,1],[1,-1,0],[1,0,1]],float);P=np.diag([1,0,0]);v=run('redistribution_memory',{'H':E(H),'P':E(P),'times':[0,np.pi/2]})
    assert np.linalg.norm(eyes.mat(v['trajectory'][1]['kernel']))<1e-12 and not v['feedback_numerically_zero']
    # Projector derivative vs independent centered eigenspace reconstruction.
    fd=[]
    for gap in [.01,.1,1,3]:
        H=np.diag([0.,gap]);V=np.array([[.2,1.],[1.,-.1]])
        v=run('spectral_susceptibility',{'H':E(H),'Hdot':E(V),'rank':1})
        h=gap*1e-5
        def proj(x):
            _,u=np.linalg.eigh(x);return np.outer(u[:,0],u[:,0].conj())
        dp=(proj(H+h*V)-proj(H-h*V))/(2*h);error=np.linalg.norm(dp-eyes.mat(v['projector_derivative']))
        fd.append(float(error));assert error<1e-6 and abs(v['metric_speed']-gap**-2)<1e-7
    # Equal-mass Gram family: rank loss has a gap; full-rank pole has no selected gap.
    run('spectral_susceptibility',{'H':[[0,0],[0,1]],'Hdot':[[0,0],[0,0]],'rank':1},label='Syzygy rank loss with separated cluster')
    run('spectral_susceptibility',{'H':[[1,0],[0,1]],'Hdot':[[0,0],[0,0]],'rank':1},True,'Equilateral full rank with closed cluster gap')
    for n in [1,2,4]:
        for _ in range(20):
            Z=rng.normal(size=(n,n));A=Z@Z.T+np.eye(n);Z=rng.normal(size=(n,n));D=Z@Z.T+np.eye(n);B=rng.normal(size=(n,n))*.05
            v=run('gluing_sign',{'A':E(A),'D':E(D),'B':E(B)})
            assert v['interface_logdet_correction']<0 and v['identity_residual']<1e-10
    scalar=run('gluing_sign',{'A':[[1]],'D':[[1]],'B':[[.5]]},label='UPG Eq.5 sign counterexample')
    assert abs(scalar['interface_logdet_correction']-np.log(.75))<1e-12
    run('gluing_sign',{'A':[[1]],'D':[[1]],'B':[[2]]},True,'Positive diagonal blocks do not suffice')
    for n in [2,3,4,5,7,11,31,97]:
        U=np.diag(np.exp(2j*np.pi*np.arange(n)/n));V=np.roll(np.eye(n),1,axis=0)
        v=run('nct_anchor',{'U':E(U),'V':E(V)},n==2,'Clock-shift dimension '+str(n))
        if n>2: assert v['winding']==1 and abs(v['domain_sum']-4)<1e-9 and v['amplitude_bound']>=1
    for n in [3,5,8]:
        for _ in range(15):
            U,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)));V,_=np.linalg.qr(rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)))
            v=run('nct_anchor',{'U':E(U),'V':E(V)})
            assert v['integer_residual']<1e-9 and v['domain_sum']<=4+1e-9 and abs(v['winding'])<=v['amplitude_bound']+1e-9
    assert run('nct_anchor',{'U':E(np.eye(3)),'V':E(np.eye(3))})['winding']==0
    run('nct_anchor',{'U':[[2,0],[0,1]],'V':[[1,0],[0,1]]},True)
    S=np.array([[1,0],[-1,1]]);angles=[np.pi/6,np.pi/3,np.pi/2,np.pi,5*np.pi/3,11*np.pi/6]
    trefoil=run('signature_flow',{'seifert':S.tolist(),'angles':angles},label='Oriented trefoil Seifert form')
    assert [x['signature'] for x in trefoil['samples']]==[0,1,2,2,1,0]
    cancel=run('signature_flow',{'seifert':block_diag(S,-S).tolist(),'angles':angles},label='Trefoil plus mirror: roots without signature jumps')
    assert all(x['signature']==0 for x in cancel['samples']) and cancel['samples'][1]['alexander_determinant_modulus']<1e-12
    run('signature_flow',{'seifert':[[1,0],[0,1]],'angles':[1]},True)
    # Exact scalar controls and dimensional counterexamples, independent of the plugins.
    import sympy as sp
    t=sp.symbols('t',real=True);halfwidth=sp.Rational(1,10);eps=sp.Rational(1,100)
    linear=sp.integrate((t*t-1)**2+eps,(t,-1,1))
    fast=sp.integrate(((t/halfwidth)**2-1)**2,(t,-halfwidth,halfwidth))+2*eps
    assert fast<linear and linear==sp.Rational(163,150) and fast==sp.Rational(19,150)
    d0=sp.Matrix([1,0]);d1=sp.zeros(1,2)
    correct_laplacian=d1.T*d1+d0*d0.T
    assert len(correct_laplacian.nullspace())==1 and len(d1.nullspace())==2
    chart=sp.Matrix([[1,t],[-t,-t*t]])/(1-t*t);assert sp.simplify(chart*chart-chart)==sp.zeros(2)
    speed=sp.trace(chart.diff(t).subs(t,0)**2)/2;assert speed==-1
    # Z3 alone permits linear anisotropy; the exact Gram calculation needs its stronger structure.
    x,y=sp.symbols('x y',real=True);rot=sp.Matrix([[-sp.Rational(1,2),-sp.sqrt(3)/2],[sp.sqrt(3)/2,-sp.Rational(1,2)]])
    anis=lambda x,y:sp.Matrix([[x,-y],[-y,-x]])
    xy=rot*sp.Matrix([x,y]);assert sp.simplify(anis(*xy)-rot*anis(x,y)*rot.T)==sp.zeros(2)
    # Smooth chart fold has divergent du/dv, with no phase discontinuity.
    points=np.linspace(-.1,.1,1001);ph=np.unwrap(np.angle(1+points+1j*points**2));assert max(abs(np.diff(ph)))<1e-3
    controls={'gluing_claim_log_one_plus':float(np.log(1.25)),'actual_gluing_log_one_minus':scalar['interface_logdet_correction'],
        'commuting_potential_linear_path':str(linear),'commuting_potential_fast_path':str(fast),
        'oblique_projector_metric_speed':str(speed),'single_differential_kernel_dimension':2,'full_hodge_homology_dimension':1,
        'Z3_equivariant_linear_anisotropy':'[[x,-y],[-y,-x]]; exact rotation identity verified',
        'nonprimitive_closed_loop_winding':[2,0],'chart_fold_max_phase_step':float(max(abs(np.diff(ph)))),
        'projector_derivative_max_fd_error':max(fd),
        'interpretation':'Counterexamples refute specified universal statements; they do not refute the entire research program.'}
    summary={'status':'PASS','eye_evaluations':len(rows),'successful':sum(x['result']['status']=='ok' for x in rows),
        'expected_blocks':sum(x['result']['status']=='blocked' for x in rows),'standalone_or_registry':'registry' if root else 'standalone',
        'seed':20260907,'new_eyes':5,'independent_controls':controls,'formal_status':'Written mathematics and numerical/symbolic controls; no new Lean compilation.'}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps({'summary':summary,'evaluations':rows},indent=2,allow_nan=False)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
