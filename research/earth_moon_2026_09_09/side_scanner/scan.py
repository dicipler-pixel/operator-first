#!/usr/bin/env python3
"""Native Compound Eye side scanner, consolidated adapter 1.2.0.

python scan.py --out fresh_scan
python scan.py --input checkpoint.json --out another_scan

Uses the unchanged registry, versioned plugin installer and dependency scheduler.
Without --instrument it creates a focused native registry in the output folder.
With --instrument it appends new versions to an existing instrument without
replacing old definitions. Source graphs are read only; no main search is run.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,sys
from itertools import combinations
from pathlib import Path
import machine

ROOT=Path(__file__).resolve().parent
VERSION='1.2.0'
EYES=[('identity',[]),('endpoint',[]),('defect_support',[]),('repair_budget',[]),
      ('joint_repair',[]),('flip_damage',[]),('colouring',[]),('lateral',[]),('structural_context',[]),
      ('invariants_set',['identity','endpoint','structural_context']),
      ('repair_set',['defect_support','repair_budget','flip_damage','joint_repair']),
      ('peripheral_set',['colouring','lateral']),
      ('whole',['invariants_set','repair_set','peripheral_set'])]
SETS={'identity':['invariants_set'],'repair':['repair_set'],'peripheral':['peripheral_set'],'whole':['whole']}

def ref(name):return 'ce.em.side.'+name+'@'+VERSION

def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def normalize(d):
    d=copy.deepcopy(d)
    if 'faces' in d and 'layers' not in d:
        d['layers']=[{'faces':fs,'edges':list(map(list,sorted({tuple(sorted(e))for f in fs for e in combinations(f,2)})))}for fs in d.pop('faces')]
    return d

def read_items(p):
    if p.suffix=='.faces':
        fs=[list(map(int,l.split()))for l in p.read_text().splitlines()if l.strip()]
        if len(fs)!=68:raise ValueError('Expected 68 triangular faces')
        return [(normalize({'n':19,'faces':[fs[:34],fs[34:]]}),str(p))]
    d=json.loads(p.read_text())
    rows=d if isinstance(d,list)else[d]
    return [(normalize(x.get('candidate',x)),x.get('source',str(p)+':'+str(i)))for i,x in enumerate(rows)]

def register(root):
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=True)
    for directory in ('catalog/eyes','catalog/sets','plugins/dependencies'):(root/directory).mkdir(parents=True,exist_ok=True)
    if hashlib.sha256((ROOT/'machine.py').read_bytes()).hexdigest()!='df154d77260f040bcc3336e75a6d7cbe1a9a36526ff81ec355303cade6b276f0':raise ValueError('Native engine changed')
    reg=machine.Registry(root);old=copy.deepcopy(reg.eyes);oldsets=copy.deepcopy(reg.sets)
    dep=root/'plugins/dependencies/em19_graph_core.py';data=(ROOT/'graph_core.py').read_bytes()
    if hashlib.sha256(data).hexdigest()!='a51d453a7489e7272a9d0300b0a72de2e39aed77ba1bb3ae4b66b496dc41d76c':raise ValueError('Graph core changed')
    if dep.exists()and dep.read_bytes()!=data:raise ValueError('Existing dependency differs')
    if not dep.exists():dep.write_bytes(data)
    code=ROOT/'earth_moon_eye.py';codehash=hashlib.sha256(code.read_bytes()).hexdigest()
    for name,deps in EYES:
        spec={'id':'ce.em.side.'+name,'version':VERSION,'title':name.replace('_',' ').title(),
              'family':'Earth Moon side scanner','status':'implemented','models':['earth-moon-labelled-19-v1'],
              'unit_system':'dimensionless-graph','inputs':{'candidate':'labelled-graph'},
              'depends_on':[ref(k)for k in deps],
              'assumptions':['Exactly 19 labelled vertices; supplied spherical layers are checked; missing layers remain UNKNOWN.','Endpoint degree and density conditions do not prohibit temporary setup states.'],
              'output_meaning':'A discrete graph observation or a combined set/whole output on the same graph.',
              'evidence_class':'exact_finite_graph_diagnostic',
              'limits':'Bounded neighborhoods and necessary edit budgets are not a general planarity/chromatic solver or independent votes.',
              'implementation':{'function':name}}
        if ref(name)not in reg.eyes:reg.add(spec,code)
        elif reg.eyes[ref(name)]['implementation']['sha256']!=codehash:raise ValueError('Versioned adapter changed')
    for name,names in SETS.items():
        key='ce.set.em.side.'+name+'@'+VERSION
        if key not in reg.sets:reg.add_set({'id':'ce.set.em.side.'+name,'version':VERSION,'title':'Earth Moon '+name,'eyes':[ref(k)for k in names]})
    p=root/'catalog/models.json';models=json.loads(p.read_text())if p.exists()else{}
    contract={'basis_id':'vertex-labels-0-through-18','boundary_id':'two-labelled-spheres-or-explicitly-missing','unit_system':'dimensionless-graph','coordinate':{'kind':'snapshot','unit':'index'}}
    if 'earth-moon-labelled-19-v1'in models and models['earth-moon-labelled-19-v1']!=contract:raise ValueError('Model contract differs')
    models['earth-moon-labelled-19-v1']=contract;write(p,models)
    check=machine.Registry(root)
    if any(check.eyes[k]!=v for k,v in old.items())or any(check.sets[k]!=v for k,v in oldsets.items()):raise AssertionError('Earlier definitions changed')
    return dict(native_engine=machine.VERSION,adapter=VERSION,old_eyes=len(old),old_sets=len(oldsets),eyes_now=len(check.eyes),sets_now=len(check.sets),old_definitions_preserved=True,active_outputs=13)

def request(d,source,index):
    return {'schema':'compound-eye-request-v1','context':{'object_id':'em19:'+machine.digest(d),
      'model_id':'earth-moon-labelled-19-v1','basis_id':'vertex-labels-0-through-18',
      'boundary_id':'two-labelled-spheres-or-explicitly-missing','unit_system':'dimensionless-graph',
      'coordinate':{'kind':'snapshot','value':index,'unit':'index'},
      'source':{'kind':'theoretical','id':source},'assumptions':['Read-only finite observation; no unbounded coverage.']},
      'inputs':{'candidate':{'value':d,'unit':'labelled-graph'}}}

def observe(d,source,index,root):
    return machine.execute(request(d,source,index),['ce.set.em.side.whole@'+VERSION],root=root,workers=4)

def values(run):return {r['eye'].split('@')[0].split('.')[-1]:r['value']for r in run['results']if r['status']=='ok'}

def verify_minimum(d,joint):
    """Independent all-missing-edge enumeration, not the adapter DP."""
    U={tuple(e)for t in d['layers']for e in t['edges']};absent=[e for e in combinations(range(19),2)if e not in U]
    triples=[t for t in combinations(range(19),3)if all(e not in U for e in combinations(t,2))]
    degree=[sum(v in e for e in U)for v in range(19)];vs=[v for v in range(19)if degree[v]<10]
    masks=[sum(1<<i for i,t in enumerate(triples)if set(e)<=set(t))for e in absent]
    codes=[sum(5**j for j,v in enumerate(vs)if v in e)for e in absent];full=(1<<len(triples))-1;count=0;passed=0
    for k in range(5):
        for ids in combinations(range(len(absent)),k):
            count+=1;m=0
            for i in ids:m|=masks[i]
            if m!=full:continue
            code=sum(codes[i]for i in ids)
            if all(degree[v]+code//(5**j)%5>=10 for j,v in enumerate(vs)):passed+=1
    add=set(map(tuple,joint['one_relaxed_minimizer']))
    assert passed==0 and len(add)==5 and not(U&add)
    assert all(any(e in add for e in combinations(t,2))for t in triples)
    assert all(sum(v in e for e in U|add)>=10 for v in range(19))
    assert joint['minimum_additions_for_old_triples_and_degree']==5
    return dict(missing_edges=len(absent),subsets_through_four=count,passing_subsets=passed,explicit_five_edge_minimizer=list(map(list,sorted(add))))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path);ap.add_argument('--out',type=Path,default=ROOT/'fresh_scan')
    ap.add_argument('--instrument',type=Path);ap.add_argument('--check-reference-budgets',action='store_true')
    a=ap.parse_args()
    if a.out.exists():raise FileExistsError('Choose a new output path; earlier evidence is never overwritten')
    a.out.mkdir(parents=True);root=a.instrument or a.out/'focused_instrument'
    write(a.out/'REGISTRATION.json',register(root))
    paths=[a.input]if a.input else[ROOT.parent/'inputs'/s for s in ('five.faces','five_triples_102_compact.json','c5_71_survivor_G.json')]
    rows=[];checked=[];i=0
    for p in paths:
      for d,source in read_items(p):
        before=hashlib.sha256(p.read_bytes()).hexdigest();r=observe(d,source,i,root);fn='runs/'+str(i).zfill(4)+'.json';write(a.out/fn,r)
        assert r['statistics']['status_counts']['ok']==13,r['statistics']
        v=values(r);w=v['whole'];rows.append({'source':source,'run':fn,'state_id':w['state_id'],'graph_id':w['graph_id'],'target_success':w['target_success'],'endpoint':v['endpoint'],'joint_repair':v['joint_repair']})
        if a.check_reference_budgets and i<2:
            checked.append(verify_minimum(d,v['joint_repair']))
            assert v['joint_repair']['minimum_old_union_edge_removals']==4+i
        if a.check_reference_budgets and i==2:
            assert v['colouring']['chi']==10 and not w['target_success'] and not v['endpoint']['biplanar_certificate']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==before
        print(i,v['endpoint']['independent_triples'],v['endpoint']['union_edges'],v['joint_repair'].get('minimum_additions_for_old_triples_and_degree'),flush=True);i+=1
    write(a.out/'SUMMARY.json',dict(status='PASS',records=rows,reference_budget_checks=checked,main_search_mutated=False,new_Lean_compilation=False,continued_after_exit=False))
    write(a.out/'SOURCE_SHA256.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in ROOT.glob('*.py')})

if __name__=='__main__':main()
