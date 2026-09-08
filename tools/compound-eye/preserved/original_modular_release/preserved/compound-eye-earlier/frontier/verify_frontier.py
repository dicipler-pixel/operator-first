#!/usr/bin/env python3
"""Reproduce the two real-target calibration suites and their certificates."""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import random
import shutil
import sys
import numpy as np
import sympy as sp
from exact_ak import controls,certify,build,from_legacy,rank2,validate
from check_ak_certificate import check
from earth_moon import (main_certificate,inflation,three_planar_layers,proper_coloring,
                        verify_rotation,screen,planar_certificate,triangle_count)
from search_fixed_ladder import legacy_engine

ROOT=Path(__file__).resolve().parent


def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2)+'\n')


def legacy(p,klass):
    fs=[{tuple(z['prefix']):tuple(z['label']) for z in level} for level in p['levels']]
    R=[{tuple(z['vertex']):tuple(z['label'])} for z in p['generators']]
    return klass([tuple(x) for x in p['X']],p['dims'],fs,p['initial_known'],R)


def run():
    checks=[];cases={};certdir=ROOT/'certificates';examples=ROOT/'examples'
    klass=legacy_engine()['AK']
    for name,p in controls().items():
        c=certify(p);verdict=check(c)
        assert verdict['forcing_complete'] and not verdict['target_conditions_met']
        assert c['score']==('11/6' if name=='kt_11_6' else '7/4')
        assert not c['cut_eye']['obstructions']
        assert {tuple(v) for v in c['forced_vertices']}==legacy(p,klass).run()
        dump(certdir/(name+'.json'),c);dump(examples/(name+'.json'),p)
        first=c['steps'][0]['vertex']
        local=[g['label'] for g in p['generators'] if g['vertex']==first]
        assert rank2(local)==0
        cases[name]={'score':c['score'],'complete':True,'first_forced_vertex':first,
                     'generators_at_first_vertex':len(local),'certificate':str((certdir/(name+'.json')).relative_to(ROOT))}
        checks.append(name+' exact forcing, independent integer certificate and score gate')
        pminus=deepcopy(p);pminus['generators']=pminus['generators'][:-1]
        cminus=certify(pminus);assert not check(cminus)['forcing_complete']
        dump(certdir/(name+'_minus_generator.json'),cminus)
        cases[name+'_minus_generator']={'score':cminus['score'],'complete':False,
                                        'forced_count':len(cminus['forced_vertices']),
                                        'cut_obstructions':len(cminus['cut_eye']['obstructions']),
                                        'subsets_checked':cminus['cut_eye']['subsets_checked']}
    assert cases['kt_11_6_minus_generator']['cut_obstructions']==0
    checks.append('all 63 subset cuts can pass while the 5/3 candidate forces nothing')
    checks.append('published calibration controls refute local seeding: first vertices have no generators')
    # The shortest explanatory counterexample.
    p=from_legacy([(0,0),(1,0),(0,1)],[2],[{(1,):(1,0)}],[],
                  [{(1,):(0,1)},{(2,):(1,0)}],'two-vertex seeding counterexample')
    c=certify(p);assert check(c)['integer_steps_checked']==1
    assert c['forced_vertices']==[[1]]
    dump(certdir/'seeding_path_counterexample.json',c)
    # Check the very simple explicit witness E + R2 - R1 = (1,-1) at vertex 1.
    _,rows,_=build(p);w=[rows[2][j]+rows[1][j]-rows[0][j] for j in range(4)]
    assert w==[1,-1,0,0]
    checks.append('two-vertex seeding counterexample checked by direct integer arithmetic')
    # Adversarial input admission cases; none may reach a mathematical certificate.
    invalid=[]
    q=deepcopy(p);q['generators'][0]['label']=[1,-1];invalid.append(('forbidden generator outside X',q))
    q=deepcopy(p);q['generators'][0]['label']=[2,3];invalid.append(('admissible generator outside X',q))
    q=deepcopy(p);q['levels'][0][0]['label']=[2,3];invalid.append(('edge outside X',q))
    q=deepcopy(p);q['dims']=[0];invalid.append(('zero dimension',q))
    q=deepcopy(p);q['dims']=[2.0];invalid.append(('float dimension',q))
    q=deepcopy(p);q['dims']=[True];invalid.append(('boolean dimension',q))
    q=deepcopy(p);q['initial_known']=[[1],[1]];invalid.append(('duplicate known vertex',q))
    q=deepcopy(p);q['initial_known']=[[1],[2]];invalid.append(('zero denominator',q))
    q=deepcopy(p);q['generators'][0]['vertex']=[3];invalid.append(('generator vertex outside tower',q))
    q=deepcopy(p);q['levels'][0][0]['prefix']=[0];invalid.append(('prefix out of range',q))
    q=deepcopy(p);q['levels'][0].append(deepcopy(q['levels'][0][0]));invalid.append(('duplicate prefix',q))
    q=deepcopy(p);q['X'].append([1.0,2]);invalid.append(('float label',q))
    for label,q in invalid:
        try:certify(q)
        except ValueError:pass
        else:raise AssertionError(label+' was accepted')
    bad=klass([(0,0),(1,0)],[1],[{}],[],[{(1,):(1,-1)}])
    assert len(bad.run())==1
    cases['input_admission']={'invalid_cases_rejected':[k for k,p in invalid],
                              'supplied_verifier_false_admission':'accepts undeclared forbidden generator (1,-1) at one vertex, apparent score 1'}
    checks.append('12 malformed or inadmissible inputs rejected before scoring')
    # Same integer data looks rank one after conversion to double precision.
    M=10**30;x=[M,M+1];y=[M+1,M+2]
    assert x[0]*y[1]-x[1]*y[0]==-1
    p=from_legacy([(0,0),tuple(x),tuple(y)],[1],[{}],[],[{(1,):tuple(x)},{(1,):tuple(y)}],'exact arithmetic stress control')
    c=certify(p);assert check(c)['forcing_complete']
    assert np.linalg.matrix_rank(np.array([x,y],dtype=float))==1
    dump(certdir/'large_integer_rank_control.json',c)
    checks.append('10^30-scale unimodular labels retain exact rank despite floating-point collapse')
    # Mutation controls cover proof integrity, including negative certificates.
    c=json.loads((certdir/'kt_11_6.json').read_text());c['steps'][0]['coefficients'][0]+=1
    try:check(c)
    except ValueError:pass
    else:raise AssertionError('tampered primal accepted')
    c=json.loads((certdir/'kt_11_6_minus_generator.json').read_text())
    c['stalled_dual_certificates'][0]['constraint_weights']=[0]*len(c['stalled_dual_certificates'][0]['constraint_weights'])
    try:check(c)
    except ValueError:pass
    else:raise AssertionError('tampered dual accepted')
    c=json.loads((certdir/'kt_7_4.json').read_text());c['score']='1'
    try:check(c)
    except ValueError:pass
    else:raise AssertionError('tampered score accepted')
    checks.append('tampered forcing, impossibility and score certificates rejected')
    # A bounded independent comparison using arbitrary T and distributed generators.
    rng=random.Random(20260907);shapes=[[1],[2],[3],[2,2],[2,3],[3,2],[2,2,2]]
    pool=[(0,0),(-1,2),(0,1),(1,0),(1,1),(1,2),(2,-1),(2,1)]
    complete=0
    for j in range(240):
        dims=shapes[j%len(shapes)]
        import itertools
        V=list(itertools.product(*(range(1,d+1) for d in dims)))
        fs=[]
        for i in range(len(dims)):
            prefixes=itertools.product(*(range(1,dims[h]+1) for h in range(i)),range(1,dims[i]))
            fs.append({tuple(v):rng.choice(pool) for v in prefixes})
        T=rng.sample(V,rng.randrange(min(2,len(V)-1)+1))
        choices=[(v,x) for v in V for x in pool[1:]]
        gens=rng.sample(choices,rng.randrange(min(len(choices),len(V)+3)+1))
        p=from_legacy(pool,dims,fs,T,[{v:x} for v,x in gens],f'deterministic random control {j}')
        c=certify(p);v=check(c)
        assert {tuple(x) for x in c['forced_vertices']}==legacy(p,klass).run()
        if v['forcing_complete']:
            complete+=1;assert not c['cut_eye']['obstructions']
        dump(certdir/'random'/f'{j:03d}.json',c)
    cases['independent_random_comparison']={'cases':240,'complete':complete,'disagreements':0,'seed':20260907,
                                           'shapes':shapes,'all_certificates_saved':True}
    checks.append('240 arbitrary-T and distributed-generator cases agree with independent integer-checked certificates')
    # Correct the missing sign branch of the row-action symmetry family.
    transforms=[]
    for a in range(-2,3):
        for sigma in [-1,1]:
            for lam in [-1,1]:
                A=[[a,lam-a],[a-sigma,lam-a+sigma]]
                assert A[0][0]-A[1][0]==sigma and A[0][1]-A[1][1]==-sigma
                assert A[0][0]*A[1][1]-A[0][1]*A[1][0]==sigma*lam
                transform=lambda x:[x[0]*A[0][0]+x[1]*A[1][0],x[0]*A[0][1]+x[1]*A[1][1]]
                p=deepcopy(controls()['kt_7_4']);p['X']=[transform(x) for x in p['X']]
                for level in p['levels']:
                    for e in level:e['label']=transform(e['label'])
                for g in p['generators']:g['label']=transform(g['label'])
                c=certify(p);assert check(c)['forcing_complete'] and c['score']=='7/4'
                transforms.append(A)
    assert [[-1,0],[0,-1]] in transforms
    cases['symmetry']={'correct_formula':'M=[[a,lambda-a],[a-sigma,lambda-a+sigma]], sigma,lambda in {-1,1}',
                       'maps_checked':len(transforms),'missing_source_example':[[-1,0],[0,-1]],
                       'height_cutoff_warning':'Normalization need not preserve a finite coordinate-height pool.'}
    checks.append('20 unimodular transport maps including the omitted negative branch preserve calibration')
    # An exact permitted generator move is a useful moduli-space control.
    p=deepcopy(controls()['kt_11_6']);p['generators'][0]['vertex']=[2,2]
    c=certify(p);assert check(c)['forcing_complete'] and c['score']=='11/6'
    dump(certdir/'generator_transport.json',c)
    checks.append('transporting a matching generator across its labelled edge preserves the forcing module and score')
    # The pairwise kernel routine preserves rational span but need not be a full Z-basis.
    ns=legacy_engine();K=ns['kernel_of_functional']([[1,0,0],[0,1,0],[0,0,1]],lambda w:2*w[0]+3*w[1]+5*w[2])
    assert all(row[1]%2==0 and row[2]%2==0 for row in K)
    assert 2*(-4)+3+5==0
    cases['integer_kernel_scope']={'counterexample_functional':[2,3,5],'omitted_integer_vector':[-4,1,1],
                                  'returned_rows':K,'effect':'Full integer-kernel basis claim is false; rational-span existence testing can remain correct.'}
    checks.append('integer-kernel basis overclaim isolated without conflating it with rational forcing existence')
    # Earth-Moon source candidate and its whole deletion route.
    earth=main_certificate();dump(certdir/'earth_moon_c7k4.json',earth);dump(examples/'earth_moon_c7k4.json',earth['candidate'])
    assert earth['screen']['whole_graph_density']['passes_necessary_bound']
    assert earth['screen']['triangle_free_subgraph']['excess']==8
    assert len(earth['join_deletion_nine_colorings'])==112
    checks.append('C7[K4]: correct 10-color certificate and independence bound 3')
    checks.append('C7[K4]: 112 triangle-free join edges violate capacity 104')
    checks.append('C7[K4]: three disjoint planar layers independently checked through rotation systems')
    checks.append('all 112 join-edge deletions have proper 9-color certificates, closing the biplanar-subgraph route')
    family=[]
    for n in range(4,13):
        layers=three_planar_layers(n);N,E,J=inflation(n,4)
        assert len(J)==4*N and len(J)>4*N-8
        family.append({'n':n,'vertices':N,'edges':len(E),'Euler_margin':6*N-12-len(E),'join_excess':8,
                       'thickness':3,'certificate':layers})
    dump(certdir/'inflated_cycle_family.json',family)
    checks.append('nine inflated-cycle instances n=4..12 have exact thickness-three certificates')
    N,E,J=inflation(7,4)
    closing={e for e in J if {e[0]//4,e[1]//4}=={0,6}}
    trajectory=[]
    for k in range(17):
        present=(J-closing)|set(sorted(closing)[:k])
        r=screen({'num_vertices':N,'edges':[list(e) for e in sorted((E-J)|present)],
                  'triangle_free_subgraph':[list(e) for e in sorted(present)]})
        trajectory.append({'closing_edges_restored':k,'join_edges':len(present),'density_rejects':bool(r['rejections'])})
    assert [r['closing_edges_restored'] for r in trajectory if r['density_rejects']]==list(range(9,17))
    cases['earth_moon_closure_trace']=trajectory
    checks.append('closing-edge trace identifies exact global-density rejection threshold at nine restored joins')
    # A passing bound must not turn into an acceptance certificate.
    K5=set(combinations(range(5),2));cycle={tuple(sorted((i,(i+1)%5))) for i in range(5)}
    p={'num_vertices':5,'edges_part1':[list(e) for e in sorted(cycle)],'edges_part2':[list(e) for e in sorted(K5-cycle)],
       'coloring':list(range(5)),'chromatic_number':5}
    r=screen(p);assert all(c['planar'] for c in r['supplied_planar_parts']) and r['status']=='rejected_for_stated_candidate'
    r=screen({'num_vertices':10,'edges':[list(e) for e in combinations(range(10),2)]})
    assert r['status']=='necessary_checks_passed_target_unresolved'
    checks.append('biplanarity of K5 and density feasibility of K10 are not promoted to Epoch success')
    N=4;K4=set(combinations(range(4),2));pc=planar_certificate(N,K4)
    bad=deepcopy(pc['rotation']);bad['0']=list(reversed(bad['0']))
    try:verify_rotation(N,K4,bad)
    except ValueError:pass
    else:raise AssertionError('positive-genus rotation accepted')
    checks.append('tampered positive-genus rotation rejected')
    # Arithmetic portion of the Lean source; this is not a Lean compilation.
    granularity=[{'q':q,'p':67*q//40,'passes':3*(67*q//40)<=5*q} for q in range(1,40)]
    assert all(x['passes'] for x in granularity)
    assert 3*67>5*40
    cases['lean_status']={'compiler_available':bool(shutil.which('lean')),'compiled_in_this_run':False,
                          'arithmetic_granularity_instances_checked':39,
                          'semantic_audit':'below_floor_excluded is h -> h; it does not formalize a sums-differences impossibility theorem. Product lemmas concern defined edge counts/densities, not all possible forcing-score optimizations.'}
    checks.append('integer granularity boundary checked; Lean semantic scope kept distinct from compilation')
    result={'edition':'0.3','all_passed':True,'check_count':len(checks),'named_checks':checks,'cases':cases,
            'earth_moon':{'vertices':28,'edges':154,'join_edges':112,'join_capacity':104,'independence_number':3,
                          'chromatic_number':10,'thickness':3,'single_join_deletion_colorings':112,
                          'biplanar_subgraph_chromatic_upper_bound':9,'epoch_target_solved':False},
            'epoch_targets':{'earth_moon':'two planar parts and exact chromatic number k in 10..12',
                             'arithmetic_kakeya':'valid tower, complete forcing, exact score <=67/40',
                             'official_verifiers_run':False,'new_solution_found':False},
            'limitations':['No Lean executable: supplied Lean file not recompiled.',
                           'No official Epoch verifier access used.',
                           'Earlier millions-of-cases seeded search is not recertified as full coverage.',
                           'Missing historical SAT layer witnesses were not supplied and cannot be rechecked.']}
    dump(ROOT/'frontier_verification.json',result)
    print(json.dumps({'all_passed':True,'check_count':len(checks),'random_cases':240,
                      'earth_moon':result['earth_moon'],'limitations':result['limitations']},indent=2),flush=True)
    return result


if __name__=='__main__':run()
