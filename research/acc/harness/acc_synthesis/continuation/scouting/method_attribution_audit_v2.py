"""Hash-checked receipt attribution. Read-only; no route replay or search."""
import hashlib,json,time,argparse,resource
from pathlib import Path
def audit(root,historical=None):
    raw_checkpoint=(root/'continuation/checkpoint.json').read_bytes()
    cp=json.loads(raw_checkpoint)
    keys=None if historical is None else {r['job_key'] for r in json.loads(historical.read_text())['rows']}
    started=time.monotonic(); rows=[]
    for attempt in cp['attempts']:
        if not (attempt.get('gate') or {}).get('exact_verified'): continue
        if keys is not None and attempt['key'] not in keys: continue
        raw=(root/attempt['result_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==attempt['result_sha256']
        result=json.loads(raw)
        item=next(e for e in result['evidence'] if e['path'].endswith('/coverage.json'))
        cov_raw=(root/item['path']).read_bytes()
        assert hashlib.sha256(cov_raw).hexdigest()==item['sha256']
        cov=json.loads(cov_raw); job=attempt['job']; gate=attempt['gate']
        if job.get('helper')=='bob':
            mechanism='saved_union' if cov.get('best_origin')=='saved_union' else 'generator_transfer'
            if mechanism=='generator_transfer': assert cov.get('successful_transfers',0)>0
        elif cov.get('improvements'): mechanism='fresh_bridge_anchored_on_saved_union'
        elif (cov.get('saved_graph_shortest_length') or cov.get('union_shortest_length') or 10**9)<job['baseline']: mechanism='saved_graph_union'
        else: mechanism='unresolved'
        rows.append(dict(row_id=job['row_id'],helper_label=job.get('helper','bridge'),actual_mechanism=mechanism,before=job['baseline'],after=gate['cost'],successful_transfers=cov.get('successful_transfers'),class_matches=cov.get('class_matches'),best_origin=cov.get('best_origin'),source_result=attempt['result_path'],source_result_sha256=hashlib.sha256(raw).hexdigest(),coverage_sha256=hashlib.sha256(cov_raw).hexdigest(),job_key=job['key']))
    assert raw_checkpoint==(root/'continuation/checkpoint.json').read_bytes()
    return dict(scope='Hash-checked independently verified improvement receipts; external imports excluded',rows=rows,elapsed_seconds=time.monotonic()-started,memory_limit_mib=1024,model_dispatches=0,new_searches=0,checkpoint_unchanged=True,checkpoint_sha256=hashlib.sha256(raw_checkpoint).hexdigest(),interpretation='Immediate improving mechanism is distinct from dependence on witnessed saved states. Unequal sequential inputs do not form a controlled lane comparison.')
if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
    p=argparse.ArgumentParser();p.add_argument('--historical',type=Path);a=p.parse_args()
    print(json.dumps(audit(Path(__file__).resolve().parents[2],a.historical),indent=2))

