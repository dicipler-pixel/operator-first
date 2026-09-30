#!/usr/bin/env python3
"""Read immutable attempt evidence; never search, dispatch models or access a network."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import resource
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import official_checker

FAMILY_SOURCE = 'research/acc/live/UPDATE_fable_to_astra_20260930T1800Z.md'
FAMILIES = {
    'ac-00003': 'MS(3)', 'ac-00028': 'MS(3)', 'ac-00016': 'MS(5)',
    'ac-00017': 'BS(1,2)', 'ac-00022': 'BS(1,2)', 'ac-00032': 'BS(1,2)',
    'ac-00013': 'prefix-scrambled', 'ac-00029': 'prefix-scrambled',
    'ac-00021': 'prefix-scrambled', 'ac-00005': 'trefoil-type',
    'ac-00011': 'trefoil-type', 'ac-00012': 'trefoil-type',
    'ac-00018': 'x2Yx5=y',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def group(rows, field):
    groups = defaultdict(list)
    for row in rows:
        groups[row[field]].append(row)
    out = {}
    for key, values in sorted(groups.items()):
        elapsed = [x['elapsed_seconds'] for x in values if x['elapsed_seconds'] is not None]
        out[key] = {
            'attempts': len(values), 'unique_rows': sorted({x['row_id'] for x in values}),
            'kinds': dict(Counter(x['kind'] for x in values)),
            'termination_reasons': dict(Counter(x['termination_reason'] for x in values)),
            'verified_improvements': sum(x['verified_improvement'] for x in values),
            'saved_moves': sum(x['saved_moves'] for x in values),
            'median_measured_seconds': statistics.median(elapsed) if elapsed else None,
            'max_measured_seconds': max(elapsed) if elapsed else None,
        }
    return out

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--checkpoint', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (1024*1024*1024, resource.RLIM_INFINITY))
    cp_path = Path(args.checkpoint)
    cp = json.loads(cp_path.read_text())
    core, _, _, challenges = official_checker.load_kernel()
    rows, sources = [], []
    for attempt in cp['attempts']:
        job = attempt['job']
        result, coverage = {}, {}
        if attempt.get('result_path'):
            result_path = ROOT / attempt['result_path']
            assert sha(result_path) == attempt['result_sha256']
            result = json.loads(result_path.read_text())
            sources.append({'path': attempt['result_path'], 'sha256': sha(result_path)})
            for evidence in result.get('evidence', []):
                path = ROOT / evidence['path']
                assert sha(path) == evidence['sha256'], evidence['path']
                if path.name == 'coverage.json':
                    coverage = json.loads(path.read_text())
                    sources.append(evidence)
        caps = coverage.get('caps_executed', [])
        start = challenges[job['row_id']]['initial_relators']
        start_length = sum(map(len, start))
        gate = attempt.get('gate') or {}
        verified = bool(gate.get('exact_verified') and result.get('candidate') and job.get('baseline') is not None
                        and len(result['candidate']['moves']) < job['baseline'])
        fresh_events = coverage.get('improvements')
        elapsed = coverage.get('elapsed_seconds')
        if elapsed is None and caps:
            elapsed = sum(x.get('elapsed_seconds', 0) for x in caps)
        row = {
            'key': attempt['key'], 'row_id': job['row_id'],
            'method': job.get('helper', 'bridge'), 'algorithm_id': job.get('algorithm_id'),
            'kind': attempt['kind'], 'baseline': job.get('baseline'), 'target': job['target'],
            'best_length': coverage.get('best_length', coverage.get('winner_length')),
            'verified_improvement': verified,
            'saved_moves': job['baseline'] - len(result['candidate']['moves']) if verified else 0,
            'family_hypothesis': FAMILIES.get(job['row_id'], 'unclassified'),
            'exact_start_total_length': start_length,
            'start_length_cohort': '<=16' if start_length <= 16 else '17..24' if start_length <= 24 else '>=25',
            'termination_reason': result.get('termination_reason', coverage.get('termination_reason', attempt.get('reason', 'unrecorded'))),
            'elapsed_seconds': elapsed,
            'peak_rss_mib': coverage.get('peak_rss_mib', max((c.get('peak_rss_mib', 0) for c in caps), default=None)),
            'admitted_records': coverage.get('total_admitted_state_records', coverage.get('admitted_records', sum(c.get('admitted_records', 0) for c in caps))),
            'partial_layer': coverage.get('partial_layer', caps[-1].get('partial_layer') if caps else None),
            'cap_slices': [{k:c.get(k) for k in ['cap','goal_radius','completed_expansion_depth','bounded_negative_through','termination_reason','partial_layer']} for c in caps],
            'saved_graph_shortest_length': coverage.get('saved_graph_shortest_length'),
            'fresh_improvement_events': fresh_events,
            'bob_paid_attempts': coverage.get('verified_donor_transfer_attempts'),
            'bob_successful_transfers': coverage.get('successful_transfers'),
            'result_path': attempt.get('result_path'),
        }
        rows.append(row)
    prefixes = []
    for cid, moves, expected in [
        ('ac-00013',[12,10,12,10,12,10,10,12,10,12,10,13,11,5],['YXYXYXXYXYXyx','xYXYXXyx']),
        ('ac-00029',[12,12,12,11,13,13,11,11,12,11,12,11,11,11,5],['YYYxyyxxYxYxxx','YYxyx']),
    ]:
        state = tuple(tuple(w) for w in challenges[cid]['initial_relators'])
        for move in moves:
            state = core.apply_move(state, move)
        actual = official_checker.render(state)
        prefixes.append({'row_id':cid, 'moves':moves, 'paid_length':len(moves),
                         'actual_state':actual, 'matches_fable':actual==expected,
                         'total_letters':sum(map(len,state)), 'full_solution':False})
    output = {
        'schema':'acc-probe-pattern/1', 'checkpoint_sha256':sha(cp_path),
        'attempts':len(rows), 'model_worker_dispatch':0, 'search_performed_by_this_script':False,
        'family_source':FAMILY_SOURCE, 'family_grade':'H: source classification, not independently established here',
        'scope':'Selected rows, unequal sequential inputs; descriptive counts are not success probabilities or live scoring claims.',
        'by_method':group(rows,'method'), 'by_family_hypothesis':group(rows,'family_hypothesis'),
        'by_start_length':group(rows,'start_length_cohort'),
        'improvements':[x for x in rows if x['verified_improvement']],
        'prefix_checks':prefixes, 'attempt_details':rows, 'sources':sources,
        'checker_sha256':sha(ROOT/'official_checker.py'),
    }
    Path(args.output).write_text(json.dumps(output,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:output[k] for k in ['attempts','by_method','prefix_checks']},indent=2))

if __name__ == '__main__':
    main()
