#!/usr/bin/env python3
"""Replay recovered routes through the pinned official checker; no model calls."""
import argparse
import json
from pathlib import Path
import time
try:
    from .harness import Harness, ROOT, atomic_json, controller_lock
    from .official_checker import load_kernel, render
except ImportError:
    from harness import Harness, ROOT, atomic_json, controller_lock
    from official_checker import load_kernel, render


def run(state, output):
    h = Harness(ROOT/'config.json', state)
    _, specs, doc, challenges = load_kernel()
    rows = {x['row_id']:x for x in json.loads((ROOT/'integration/selected_rows.json').read_text())['rows']}
    saved = json.loads((ROOT/'integration/recovered_routes.json').read_text())
    results = []
    with controller_lock(h.state):
        for route in saved['routes']:
            if h.store.stopped():
                break
            cid = route['row_id']; c = challenges[cid]
            candidate = {'row_id':cid, 'track':'AC', 'start':render(c['initial_relators']),
                'moves':route['moves'], 'ruleset_sha256':specs.get(c['move_spec_version']).move_spec_hash.removeprefix('sha256:'),
                'evidence_grade':'V', 'family':'recovered-route', 'source_evidence':route['sources']}
            gate = h.check_candidate(candidate)
            receipt_path = gate.pop('receipt_path', None)
            official_receipt = json.loads(Path(receipt_path).read_text()) if receipt_path else None
            results.append({'row_id':cid, 'length':len(route['moves']), 'pasted_record':rows[cid]['record'],
                'sources':route['sources'], 'gate':gate, 'official_receipt':official_receipt})
    verified = [x for x in results if x['gate'].get('exact_verified')]
    best = {cid:min(x['length'] for x in verified if x['row_id']==cid) for cid in {x['row_id'] for x in verified}}
    report = {'checked_at':time.time(), 'scope':'Exact offline route replay; eligibility is separately gated.',
        'attempted':len(results), 'exact_verified':len(verified), 'rows_with_verified_paths':len(best),
        'model_workers_dispatched':h.status()['reserved_worker_dispatches'], 'submission_enabled':False,
        'best_verified_lengths':best, 'results':results}
    atomic_json(output, report)
    return {k:v for k,v in report.items() if k!='results'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state',default=str(ROOT/'state'))
    parser.add_argument('--output',default=str(ROOT/'integration/real_replay_report.json'))
    args=parser.parse_args()
    print(json.dumps(run(args.state, args.output),indent=2))
