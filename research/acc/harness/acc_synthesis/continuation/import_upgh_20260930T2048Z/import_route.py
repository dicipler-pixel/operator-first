from pathlib import Path
import json,time,hashlib
from acc_synthesis.harness import Harness, atomic_json, controller_lock, digest
p=Path('acc_synthesis').resolve(); d=p/'continuation/import_upgh_20260930T2048Z'
source=json.loads((d/'source.json').read_text()); targets=json.loads((p/'integration/exact_targets.json').read_text())
row=next(x for x in targets['targets'] if x['row_id']=='ac-00003')
candidate={'row_id':'ac-00003','track':'AC','start':row['start'],'moves':source['moves'],'ruleset_sha256':targets['ruleset_sha256'],'evidence_grade':'V','family':{'origin':'upgh-t00108','source_commit':source['source']['head']}}
h=Harness(p/'config.json',p/'state')
with controller_lock(h.state):
 c=json.loads((p/'continuation/checkpoint.json').read_text())
 assert not c['stopped'] and c['active'] is None and not h.store.stopped()
 routes=json.loads((p/'continuation/routes.json').read_text())
 before=min(len(x['moves']) for x in routes['routes'] if x['row_id']=='ac-00003')
 gate=h.check_candidate(candidate)
 assert gate.get('exact_verified'),gate
 receipt=json.loads(Path(gate.pop('receipt_path')).read_text());gate['official_receipt']=receipt
 atomic_json(d/'candidate.json',candidate);atomic_json(d/'receipt.json',receipt);atomic_json(d/'gate.json',gate)
 duplicate=any(x['row_id']=='ac-00003' and x['moves']==candidate['moves'] for x in routes['routes'])
 if not duplicate:
  atomic_json(d/'routes_before.json',routes)
  routes['routes'].append({'row_id':'ac-00003','moves':candidate['moves'],'sources':[{'archive':str((d/'source.json').relative_to(p)),'source_commit':source['source']['head'],'source_blob':source['source']['sha'],'exact_receipt':receipt,'origin':'UPGH t00108; independently checked here'}]})
  atomic_json(p/'continuation/routes.json',routes)
 event={'row_id':'ac-00003','old_best':before,'new_length':len(candidate['moves']),'exact_verified':True,'imported':not duplicate,'candidate_sha256':digest(candidate),'moves_sha256':digest(candidate['moves']),'source_commit':source['source']['head'],'source_blob':source['source']['sha'],'receipt_sha256':hashlib.sha256((d/'receipt.json').read_bytes()).hexdigest(),'scoring':gate['status'],'reason':gate['reason'],'attempts_unchanged':len(c['attempts']),'model_dispatches':0}
 atomic_json(d/'import_receipt.json',event);h.store.event('memory.external_route_verified',event)
 print(json.dumps(event))

