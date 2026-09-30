"""Reproduce the receipt attribution audit; never runs route search or checkers."""
import hashlib,json,time
from pathlib import Path
def audit(root):
    before=(root/'continuation/checkpoint.json').read_bytes()
    cp=json.loads(before)
    rows=[]
    started=time.monotonic()
    for attempt in cp['attempts']:
        if not (attempt.get('gate') or {}).get('exact_verified'): continue
        path=root/attempt['result_path']
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==attempt['result_sha256']
        result=json.loads(raw)
        evidence=result.get('evidence',[])
        coverage_evidence=next(e for e in evidence if e['path'].endswith('/coverage.json'))
        coverage_raw=(root/coverage_evidence['path']).read_bytes()
        assert hashlib.sha256(coverage_raw).hexdigest()==coverage_evidence['sha256']
        cov=json.loads(coverage_raw)
        job=attempt['job']
        if job.get('helper')=='bob':
            mechanism='saved_union' if cov.get('best_origin')=='saved_union' else 'generator_transfer'
            if mechanism=='generator_transfer': assert cov.get('successful_transfers',0)>0
        elif cov.get('improvements'):
            mechanism='fresh_bridge'
        elif (cov.get('saved_graph_shortest_length') or cov.get('union_shortest_length') or 10**9)<job['baseline']:
            mechanism='saved_graph_union'
        else: mechanism='unresolved'
        original=next(r for r in json.loads((root/'continuation/scouting/method_attribution_audit_20260930T2212Z.json').read_text())['rows'] if r['job_key']==job['key'])
        row=dict(original,actual_mechanism=mechanism)
        assert row['source_result_sha256']==hashlib.sha256(raw).hexdigest()
        assert row['coverage_sha256']==hashlib.sha256(coverage_raw).hexdigest()
        rows.append(row)
    assert before==(root/'continuation/checkpoint.json').read_bytes()
    return dict(rows=rows,elapsed_seconds=time.monotonic()-started,model_dispatches=0,new_searches=0,checkpoint_unchanged=True)
if __name__=='__main__':
    print(json.dumps(audit(Path(__file__).resolve().parents[2]),indent=2))

