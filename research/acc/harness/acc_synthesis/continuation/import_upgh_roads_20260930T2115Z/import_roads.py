from pathlib import Path
import hashlib, json, resource, time
from acc_synthesis.harness import Harness, atomic_json, controller_lock, digest

resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
root=Path('acc_synthesis').resolve()
out=root/'continuation/import_upgh_roads_20260930T2115Z'
source=json.loads((out/'source.json').read_text())
body=source['content'].encode()
assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==source['sha']
targets=json.loads((root/'integration/exact_targets.json').read_text())
selected=json.loads((root/'integration/selected_rows.json').read_text())
assert any(r['row_id']=='ac-00003' for r in selected['rows'])
row=next(r for r in targets['targets'] if r['row_id']=='ac-00003')
paths=[json.loads(line.split(': ',1)[1]) for line in source['content'].splitlines() if line.startswith('ac-00003: ')]
assert len(paths)==len({tuple(p) for p in paths})
h=Harness(root/'config.json',root/'state')
started=time.monotonic()
with controller_lock(h.state):
    cp=json.loads((root/'continuation/checkpoint.json').read_text())
    assert cp['active'] is None and not cp['stopped'] and not h.store.stopped()
    roads=json.loads((root/'continuation/routes.json').read_text())
    atomic_json(out/'routes_before.json',roads)
    prior={tuple(r['moves']) for r in roads['routes'] if r['row_id']=='ac-00003'}
    receipts=[]
    for i,moves in enumerate(paths):
        if tuple(moves) in prior:
            receipts.append({'length':len(moves),'already_present':True,'moves_sha256':digest(moves)})
            continue
        assert time.monotonic()-started<180
        candidate={'row_id':'ac-00003','track':'AC','start':row['start'],'moves':moves,'ruleset_sha256':targets['ruleset_sha256'],'evidence_grade':'V','family':{'origin':'UPGH t00108 data-only road union','source_commit':source['head'],'source_blob':source['sha']}}
        gate=h.check_candidate(candidate)
        assert gate.get('exact_verified'),gate
        receipt=json.loads(Path(gate.pop('receipt_path')).read_text())
        gate['official_receipt']=receipt
        atomic_json(out/f'candidate_{i}.json',candidate)
        atomic_json(out/f'gate_{i}.json',gate)
        atomic_json(out/f'receipt_{i}.json',receipt)
        roads['routes'].append({'row_id':'ac-00003','moves':moves,'sources':[{'archive':str((out/f'candidate_{i}.json').relative_to(root)),'source_commit':source['head'],'source_blob':source['sha'],'exact_receipt':receipt,'origin':'UPGH data only; independently checked before road-union search'}]})
        prior.add(tuple(moves))
        receipts.append({'length':len(moves),'exact_verified':True,'moves_sha256':digest(moves),'scoring':gate['status'],'certificate_sha256':receipt.get('certificate_sha256')})
    atomic_json(root/'continuation/routes.json',roads)
    event={'row_id':'ac-00003','source_commit':source['head'],'source_blob':source['sha'],'routes':receipts,'best_length':min(len(p) for p in prior),'attempts_unchanged':len(cp['attempts']),'model_dispatches':0,'elapsed_seconds':time.monotonic()-started,'next_experiment':'Existing exact-layered-bidirectional-route-union-v1 on this genuinely new own-road input; same caps and target'}
    atomic_json(out/'import_receipt.json',event)
    h.store.event('memory.external_roads_verified',event)
    print(json.dumps(event))
