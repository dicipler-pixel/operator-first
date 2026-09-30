#!/usr/bin/env python3
"""DEMONSTRATION ONLY. Deterministic role responses; no language model is called."""
import hashlib
import json
from pathlib import Path
import sys

req=json.load(sys.stdin)
if not req.get('demo'):
    raise SystemExit('demo_worker refuses non-demo requests')
root=Path(req['workspace'])
artifact=root/'fixture_observation.json'
artifact.write_text(json.dumps({'simulation':True,'observation':'first strategy misses; alternate toy route supplied'}))
evidence=[{'path':artifact.name,'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest()}]
role=req['role']; task=req['task']
if role=='luna_memory':
    result={'kind':'context','summary':'DEMO: retained failed-attempt context loaded.','evidence':evidence}
elif role=='sol_builder' and task['switches']==0:
    result={'kind':'bounded_miss','summary':'DEMO: simulated bounded miss.','evidence':evidence,
            'limits':{'fixture_states':1},'reopen_when':{'event':'verified_bridge','row_id':task['row_id']}}
elif role=='astra_advisor':
    result={'kind':'proposal','summary':'DEMO: change the toy route family.','evidence':evidence,
            'strategy':{**task['strategy'],'route_family':'toy-direct'},
            'disputed_assumption':'Initial toy family contains the supplied route.',
            'discriminating_test':{'input':['ab','b'],'test':'apply the supplied toy suffix deletion'},
            'outcome_meanings':{'pass':'send candidate to independent review','fail':'retain bounded miss'}}
elif role=='sol_builder':
    result={'kind':'candidate','summary':'DEMO: toy route, not an ACC claim.','evidence':evidence,
            'candidate':{'row_id':task['row_id'],'track':'AC','start':['ab','b'],
                         'moves':['toy-remove-suffix-b'],'ruleset_sha256':task['ruleset_sha256'],
                         'evidence_grade':'V','family':'toy-direct'}}
else:
    result={'kind':'review','verdict':'accept','summary':'DEMO: fixture review; exact toy check still required.','evidence':evidence}
print(json.dumps(result))
