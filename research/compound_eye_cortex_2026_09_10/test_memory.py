#!/usr/bin/env python3
"""Controls for correction and obstruction memory."""
from pathlib import Path
import json
import memory

n=0
def ok(x,msg):
    global n
    if not x:raise AssertionError(msg)
    n+=1
records=[
 {'ref':'gap.bound@1.0.0','claim_id':'gap.bound','value_hash':'old','status':'established','supersedes':[]},
 {'ref':'gap.bound@1.1.0','claim_id':'gap.bound','value_hash':'new','status':'established','supersedes':['gap.bound@1.0.0']},
 {'ref':'window.rule@1.0.0','claim_id':'window.rule','value_hash':'A','status':'established','supersedes':[]},
 {'ref':'window.rule@1.1.0','claim_id':'window.rule','value_hash':'B','status':'established','supersedes':[]},
]
r=memory.correction_audit(records,[{'source':'paper-old','claim_ref':'gap.bound@1.0.0'},{'source':'paper-new','claim_ref':'gap.bound@1.1.0'}])
ok(len(r['stale_source_references'])==1,'Stale citation not isolated')
ok(r['stale_source_references'][0]['source']=='paper-old','Wrong stale source')
ok(len(r['parallel_live_variants'])==1 and r['parallel_live_variants'][0]['claim_id']=='window.rule','Parallel variants missing')
obs={'id':'triangle-free-cut','required_facts':{'N':19,'alpha_at_most_two':True},'excluded_domain':{'host':'family-A'},'certificate_ref':'cert://1'}
r=memory.obstruction_applicability(obs,{'N':19,'alpha_at_most_two':True,'host':'family-A'})
ok(r['status']=='APPLIES','Matching obstruction should apply')
r=memory.obstruction_applicability(obs,{'N':19,'alpha_at_most_two':True,'host':'family-B'})
ok(r['status']=='DOES_NOT_APPLY','Changed domain should release obstruction')
r=memory.obstruction_applicability(obs,{'N':19,'host':'family-A'})
ok(r['status']=='UNKNOWN','Missing premise must be unknown')
refused=0
for fn in [lambda:memory.correction_audit([{'ref':'bad','claim_id':'x','value_hash':'a','status':'x','supersedes':[]}]),
           lambda:memory.correction_audit([records[0],dict(records[1],supersedes=['other@1.0.0'])]),
           lambda:memory.obstruction_applicability({'id':'x'}, {})]:
    try:fn()
    except ValueError:refused+=1
ok(refused==3,'Malformed memory inputs were not rejected')
out={'status':'PASS','checks':n,'refused_controls':refused,'scope':'Explicit metadata memory controls; no prose plagiarism/priority inference.'}
Path('memory_test_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
