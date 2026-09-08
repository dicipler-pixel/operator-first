"""Independent mathematical controls, exact certificates, and registry execution.
Run directly, or pass --instrument-root to execute every new eye via Compound Eye.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import argparse,copy,hashlib,importlib.util,json,sys
import numpy as np
import sympy as sp
from exact_counts import legendre,correlation,direct
HERE=Path(__file__).resolve().parent
plugin=HERE/'diophantine_eyes.py'
if not plugin.exists():plugin=HERE.parent.parent/'extensions/diophantine_eyes.py'
spec=importlib.util.spec_from_file_location('diophantine_eyes',plugin);eyes=importlib.util.module_from_spec(spec);spec.loader.exec_module(eyes)
METHODS=['integer_witness','discriminant','fibre_transfer','prime_evolution','twist_selection','polynomial_identity','integral_cover','pell_orbit']

def pell_unit(D):
    a0=isqrt(D);m=0;d=1;a=a0;p0,p1=1,a;q0,q1=0,1
    for _ in range(100000):
        if p1*p1-D*q1*q1==1:return p1,q1
        m=d*a-m;d=(D-m*m)//d;a=(a0+m)//d;p0,p1=p1,a*p1+p0;q0,q1=q1,a*q1+q0
    raise RuntimeError('Declared continued fraction bound exceeded')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--instrument-root',type=Path);ap.add_argument('--output',type=Path,default=HERE/'verification.json');a=ap.parse_args();rows=[];root=a.instrument_root
    if root:
        root=root.resolve();sys.path.insert(0,str(root));import machine
        reg=machine.Registry(root);old={k:machine.digest(v) for k,v in reg.eyes.items()}
        for name in METHODS:
            if 'ce.dio.'+name+'@1.0.0' not in reg.eyes:
                reg.add({'id':'ce.dio.'+name,'version':'1.0.0','title':name.replace('_',' ').title(),
                         'family':'Diophantine evolution','status':'implemented','inputs':{'case':'*'},'depends_on':[],
                         'assumptions':['Exact integer or rational inputs where stated; fixed finite scope for prime experiments.'],
                         'output_meaning':'Arithmetic certificate or finite diagnostic, explicitly labeled in its output.',
                         'evidence_class':'explicit_per_request','limits':'No physical inference; no exact rank or infinitude from finite averages.',
                         'implementation':{'path':'extensions/diophantine_eyes.py','sha256':hashlib.sha256(plugin.read_bytes()).hexdigest(),'function':name}},code=plugin)
        if 'ce.set.diophantine@1.0.0' not in reg.sets:
            reg.add_set({'id':'ce.set.diophantine','version':'1.0.0','title':'Diophantine evidence and evolution','eyes':['ce.dio.'+f+'@1.0.0' for f in METHODS]})
        assert all(machine.digest(reg.eyes[k])==h for k,h in old.items())
    def run(name,case,block=False):
        if root:
            req={'schema':'compound-eye-request-v1','context':{'object_id':name,'model_id':'diophantine-surface-v1',
                 'basis_id':'integer-coordinate-ring','boundary_id':'declared-affine-chart','coordinate':{'kind':'verification_case','value':len(rows),'unit':'index'},
                 'unit_system':'dimensionless_arithmetic','source':{'kind':'theoretical','id':'independent-mathematical-control'},'assumptions':[]},
                 'inputs':{'case':{'unit':'exact_or_declared_diagnostic','value':case}}}
            res=machine.execute(req,['ce.dio.'+name+'@1.0.0'],root=root,workers=1)['results'][-1]
        else:
            v=getattr(eyes,name)({'case':case});res={'status':'blocked','reason':v['reason']} if v.get('_status')=='blocked' else {'status':'ok','value':v}
        assert res['status']==('blocked' if block else 'ok'),res
        rows.append({'eye':name,'case':case,'result':res});return res.get('value',{})
    t=sp.Symbol('t');xyz=[-108*t**4-24*t**2-2,36*t**3+2*t,648*t**6+288*t**4+50*t**2+3]
    coeff=[[str(p.expand().coeff(t,i)) for i in range(sp.degree(p,t)+1)] for p in xyz]
    assert run('polynomial_identity',{'abc':[0,1,1],'coefficients':coeff})['identically_zero']
    bad=copy.deepcopy(coeff);bad[0][0]='-3'
    assert not run('polynomial_identity',{'abc':[0,1,1],'coefficients':bad})['identically_zero']
    points=[[int(p.subs(t,10**13+i)) for p in xyz] for i in range(3)]
    val=run('integer_witness',{'abc':[0,1,1],'points':points,'min_abs_x':10**50})
    assert val['all_satisfy'] and val['distinct_x'] and val['all_above_bound']
    pts=[]
    for residue in [542,602,902]:
        u=930*10**11+residue;s=(368-u**3)//930;assert u**3+930*s==368
        pts.append([u*s,s+2,-31*s*s+4*s-1])
    val=run('integer_witness',{'abc':[-1,0,2],'points':pts,'min_abs_x':10**50})
    assert val['all_satisfy'] and val['distinct_x'] and val['all_above_bound']
    witness={'published_plus_family':points,'published_minus_z_family':pts,'source':'Epoch March 2026; reproduced, not new solutions to the six remaining open equations'}
    (HERE/'large_integer_witnesses.json').write_text(json.dumps(witness,indent=2))
    broken=copy.deepcopy(points);broken[0][2]+=1
    assert not run('integer_witness',{'abc':[0,1,1],'points':broken})['all_satisfy']
    run('integer_witness',{'abc':[0,1,1],'points':[[1.0,0,0]]},True)
    from run_experiment import EQS
    for abc in EQS:
        for x,y in [(-2,0),(-1,1),(0,0),(1,2),(8,7),(-13,0)]:
            v=run('discriminant',{'abc':list(abc),'x':x,'y':y})
            assert all(eyes.equation(*abc,x,y,z)==0 for z in v['z'])
            # Independent brute force on a bounded z range, not the square-root algorithm.
            if abs(x)<=2:assert v['z']==[z for z in range(-30,31) if eyes.equation(*abc,x,y,z)==0]
    run('discriminant',{'abc':[0,1,1],'x':1.5,'y':0},True)
    for p in [5,7,11,13,17,19,23,29,31,37,101,401]:
        chi=legendre(p);corr=correlation(p,chi,1);y=np.arange(p,dtype=np.int64);Ay=corr[(y**4-4)%p]
        assert np.array_equal(Ay,direct(p,chi,1,(y**4-4)%p))
        v=run('fibre_transfer',{'prime':p,'traces':Ay.tolist(),'radius':'3/2'})
        assert v['multiplicities_match'] and v['identity_residual']==0
    run('fibre_transfer',{'prime':9,'traces':[0]*9},True)
    series=json.loads((HERE/'evolution.json').read_text())
    for col in range(9):
        for window in [(401,1499),(1501,4999)]:
            sel=[r for r in series['base'] if window[0]<=r['prime']<=window[1]]
            v=run('prime_evolution',{'primes':[r['prime'] for r in sel],'numerators':[r['numerators'][col] for r in sel]})
            assert not v['rank_proven']
    run('prime_evolution',{'primes':[5,5],'numerators':[0,0]},True)
    candidates=series['selected_candidates'];ds=series['discovery_primes'];vs=series['validation_primes']
    for e in range(9):
        cs=[c for c in candidates if c['equation']==e]
        v=run('twist_selection',{'labels':[str((c['pair'],c['twist'])) for c in cs],
            'values':[c['discovery_values']+[n/p for n,p in zip(c['validation_numerators'],vs)] for c in cs], 'discovery_count':len(ds)})
        assert abs(v['discovery']['mean']-cs[0]['discovery_mean'])<1e-12
    run('twist_selection',{'labels':['a'],'values':[[1,2,3]],'discovery_count':3},True)
    assert run('integral_cover',{'radius':'3/2'})['integer_y_reachable']==[0]
    assert run('integral_cover',{'radius':'1'})['integer_y_reachable']==[-1,0,1]
    run('integral_cover',{'radius':'-1'},True)
    # Construct the formerly missing section, not just sample points on fibres.
    u=sp.Symbol('u');q=1+u*u;N=u**4-34*u*u+1
    x=N/(4*q*q);y=3*(1-u*u)/(2*q);w=3*u*N/(2*q**3)
    assert sp.factor(w*w-y**4+4*(x**3+x+1))==0
    for v in [F(-4),F(-2),F(-3,2),F(-1),F(0),F(1,2),F(1),F(2),F(4)]:
        xv,yv,wv=[sp.factor(f.subs(u,sp.Rational(v.numerator,v.denominator))) for f in [x,y,w]]
        assert sp.factor(wv*wv-yv**4+4*(xv**3+xv+1))==0
    # At u=1: P=(8,-24) on Y²=X³+16X-64. Its double is nonintegral.
    X,Y=F(8),F(-24);m=(3*X*X+16)/(2*Y);X2=m*m-2*X;Y2=m*(X-X2)-Y
    assert (X2,Y2)==(F(25,9),F(37,27)) and Y2*Y2==X2**3+16*X2-64
    section={'x':'(u^4-34u^2+1)/(4(1+u^2)^2)','y':'3(1-u^2)/(2(1+u^2))','w':'3u(u^4-34u^2+1)/(2(1+u^2)^3)',
             'symbolic_residual':'0','specialized_point':['8','-24'],'doubled_point':[str(X2),str(Y2)],
             'rank_lower_bound_argument':'Nagell-Lutz: 2P nonintegral implies P nontorsion; smooth specialization makes section nontorsion.',
             'integer_image':[[-2,0,-3],[-2,0,3]],'exact_rank_proven':False}
    (HERE/'section_certificate.json').write_text(json.dumps(section,indent=2))
    # Latest-paper auxiliary Pell seed and its large exact orbit.
    A=17006096;x0=22108343594783571;v0=91171377945572295096;r,s=pell_unit(A)
    assert 162**3-4==350**2+2032**2 and v0*v0-A*x0*x0==-688752720
    v=run('pell_orbit',{'A':A,'x':x0,'v':v0,'unit_r':r,'unit_s':s,'steps':3});assert v['preserved']
    (HERE/'pell_orbit.json').write_text(json.dumps(v,indent=2))
    run('pell_orbit',{'A':2,'x':1,'v':1,'unit_r':2,'unit_s':1},True)
    mm,rr,ss,dd=sp.symbols('m r s d')
    assert sp.expand(4*mm*(mm+rr*ss+ss*ss*dd)-(2*mm+rr*ss)**2-ss*ss*(4*mm*dd-rr*rr))==0
    summary={'evaluations':len(rows),'ok':sum(r['result']['status']=='ok' for r in rows),
             'expected_blocks':sum(r['result']['status']=='blocked' for r in rows),'symbolic_section_verified':True,
             'published_large_integer_witnesses':6,'ntt_independent_direct_checks':series['independent_direct_sum_checks'],
             'registry_history_preserved':True if root else 'not tested in standalone mode',
             'formal_status':'See formal build log separately; symbolic checks are not Lean compilation.'}
    a.output.write_text(json.dumps({'summary':summary,'results':rows},indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
