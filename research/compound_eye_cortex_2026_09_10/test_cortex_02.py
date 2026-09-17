#!/usr/bin/env python3
"""Independent finite controls for Cortex 0.2/0.3 meta-organs."""
from pathlib import Path
import json,sys
import lineage,theorem_genome as tg,planner

checks=0
def ok(x,msg):
    global checks
    if not x:raise AssertionError(msg)
    checks+=1

# Correct the source-module versus executable-entrypoint distinction.
g=lineage.catalog_groups()
ok(g['eyes']>=191,'Catalog missing')
root=lineage.machine.Registry(lineage.INSTRUMENT)
a=root.eyes['ce.frontier.forcing@1.0.0'];b=root.eyes['ce.frontier.coverage@1.0.0']
ok(lineage.module_key(a)==lineage.module_key(b),'Expected shared adapter module')
ok(lineage.entrypoint_key(a)!=lineage.entrypoint_key(b),'Different adapters must not collapse to one entrypoint')

# Theorem genome: dependency graph and evidence class are explicit.
c1={'id':'demo.base','version':'1.0.0','title':'Base','statement':'Finite demo base','domain':'demo','scope':'finite demo',
    'assumptions':['A'],'dependencies':[],'evidence':[{'class':'exact_certificate','ref':'demo://base'}],
    'acceptance':['exact check'],'formal_status':'not_formalized','status':'established_within_scope',
    'negative_controls':['change A'],'counterexamples':[],'limits':'demo only'}
c2={'id':'demo.child','version':'1.0.0','title':'Child','statement':'Conditional child','domain':'demo','scope':'finite demo',
    'assumptions':['B'],'dependencies':['demo.base@1.0.0'],'evidence':[],'acceptance':[],
    'formal_status':'not_formalized','status':'conditional','negative_controls':[],'counterexamples':[],'limits':'demo only'}
r=tg.audit([c2,c1])
ok(r['claims']==2,'Wrong claim count')
ok(r['topological_order'].index('demo.base@1.0.0')<r['topological_order'].index('demo.child@1.0.0'),'Dependency order lost')
ok(not r['missing_dependencies'],'Unexpected missing dependency')

tr=tg.assumption_transfer(c1,{'target-A':'satisfied'},{'A':'target-A'})
ok(tr['all_source_assumptions_accounted_for'],'Valid assumption map rejected')
tr=tg.assumption_transfer(c1,{'target-A':'unknown'},{'A':'target-A'})
ok(not tr['all_source_assumptions_accounted_for'] and tr['blocked'][0]['status']=='unknown','Unknown assumption must block transfer')
lab=tg.label_loss(['source','energy','orientation'],['source','orientation'])
ok(lab['missing']==['energy'] and not lab['safe_for_declared_question'],'Label loss not detected')

# Discriminator planner must prefer the four-way diagnostic over a blind basis growth.
plan=json.loads((Path(__file__).parent/'examples/discriminator_plan.json').read_text())
p=planner.evaluate(plan)
ok(p['recommended']=='diagnostic_factorial_split','Wrong discriminator recommendation')
rows={x['id']:x for x in p['ranked_actions']}
ok(rows['diagnostic_factorial_split']['worst_case_remaining']==1,'Four-way split should resolve every declared hypothesis')
ok(rows['grow_basis_blindly']['worst_case_remaining']==2,'Blind growth partition changed')

# Negative controls.
refused=0
bad_est=dict(c1);bad_est['evidence']=[]
cycle1=dict(c1,id='demo.c1',status='conditional',evidence=[],acceptance=[],dependencies=['demo.c2@1.0.0'])
cycle2=dict(c2,id='demo.c2',dependencies=['demo.c1@1.0.0'])
for fn in [lambda:tg.validate_claim(bad_est),lambda:tg.audit([cycle1,cycle2]),
           lambda:planner.evaluate({'schema':planner.SCHEMA,'hypotheses':[{'id':'a'},{'id':'b'}],
                                    'actions':[{'id':'x','cost':1,'outcomes':{'o':['a']}}]}),
           lambda:tg.assumption_transfer(c1,{'target-A':'maybe'},{'A':'target-A'})]:
    try:fn()
    except ValueError:refused+=1
ok(refused==4,'Malformed meta claims/plans were not all rejected')

out={'status':'PASS','checks':checks,'refused_controls':refused,'catalog_eyes_seen':g['eyes'],
     'planner_recommendation':p['recommended'],
     'scope':'Meta-organ controls only; no scientific theorem is certified.'}
Path('cortex_02_test_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
