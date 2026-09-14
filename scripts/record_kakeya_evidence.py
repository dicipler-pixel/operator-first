#!/usr/bin/env python3
"""Append actual verification evidence through the preserved mixer recorder.

The inputs retain complete output, not only verdicts. Every invocation writes
new input/event files and appends observations. Failed attempts remain present.
No logical result is converted to a fabricated numeric channel.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INSTRUMENT = ROOT / 'research/kakeya_formal_2026_09_14/instrument'
CLAIM = 'kakeya-integer-witness-cut-20260914'
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
INPUTS = INSTRUMENT / 'inputs' / STAMP
INPUTS.mkdir(parents=True, exist_ok=False)


def full(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'text': data.decode()}


def invoke(name, args):
    p = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    (INPUTS / (name + '.stdout.log')).write_text(p.stdout)
    (INPUTS / (name + '.stderr.log')).write_text(p.stderr)
    if p.returncode:
        raise RuntimeError(name + ': ' + p.stderr)


def observe(eye, verdict, output, assumptions=None, blocked=None):
    row = {'claim_id': CLAIM, 'eye_id': eye, 'verdict': verdict,
           'evidence': 'exact-replay', 'output': output,
           'assumptions': assumptions or [], 'source': 'Preserved files with byte counts and SHA-256',
           'weight': 1, 'reproduce': 'python3 scripts/verify_kakeya_bridges.py'}
    if blocked:
        row['blocked_on'] = blocked
    return row


report_path = Path(sys.argv[1]).resolve()
report = json.loads(report_path.read_text())
evidence_dir = report_path.parent
evidence = [full(p) for p in sorted(evidence_dir.rglob('*')) if p.is_file()]
checks = report['checks']
rows = []
for eye, selected in [
    ('local-compile', ['build']),
    ('kernel-recheck', [k for k in checks if k.endswith('_kernel')]),
    ('axiom-audit', ['declaration_audit']),
    ('boundary-controls', [k for k in checks if k.startswith('false_')]),
]:
    passed = bool(selected) and all(k in checks and (
        checks[k]['exit_code'] != 0 if checks[k].get('expected_rejection')
        else checks[k]['exit_code'] == 0) for k in selected)
    rows.append(observe(eye, 'supports' if passed else 'obstructs',
        {'report': report, 'selected_checks': selected, 'complete_evidence': evidence},
        ['Pinned Lean kernel and mathlib dependencies', 'Nonzero-multiple operational forcing model'],
        None if passed else 'Correct and rerun the recorded verification gate'))

review_paths = sorted((ROOT / 'review').glob('*.md'))
rows.append(observe('definitions', 'supports', {'reviews': [full(p) for p in review_paths]},
    ['Reviewed operational definitions; official unit-target equivalence remains unproved']))
history_paths = []
for p in sorted((ROOT / 'logs').rglob('*')):
    if p.is_file() and p.suffix in {'.log', '.txt', '.json', '.md', '.lean', '.c', '.py'}:
        history_paths.append(p)
rows.append(observe('scope-history', 'orthogonal', {
    'work_history': [full(p) for p in history_paths],
    'prior_scope': 'Prior arithmetic and transport audit preserved separately. This run neither changes the finite search count nor repairs false analytic transport claims.',
    'limitations': 'Repeated elaboration and kernel replay are checks of the same proofs, not independent mathematical evidence. The local runtime uses the disclosed app-path compatibility adapter.'}))
obs_path = INPUTS / 'observations.json'
obs_path.write_text(json.dumps(rows, indent=2) + '\n')
invoke('record_observations', ['node', str(INSTRUMENT / 'tools/acc/eye_log_v2.js'), 'observe', str(obs_path)])
run = {'lane': 'kakeya-formal', 'run_id': 'finite-bridges-' + STAMP,
       'claim': 'Pinned finite arithmetic witness and iterative cut verification gate passes.',
       'status': 'verified' if report['status'] == 'PASS' else 'blocked',
       'evidence': 'exact-replay', 'observed': {'report': report, 'complete_evidence': evidence},
       'reproduce': 'python3 scripts/verify_kakeya_bridges.py',
       'caveat': 'Local runtime adapter disclosed. Hosted GitHub CI is a separate eye. Nonzero-multiple forcing only; no official challenge-definition equivalence.'}
run_path = INPUTS / 'run.json';run_path.write_text(json.dumps(run, indent=2) + '\n')
invoke('record_run', ['node', str(INSTRUMENT / 'tools/acc/mixer_log_v1.js'), 'record', str(run_path)])
invoke('mix', ['node', str(INSTRUMENT / 'tools/acc/eye_log_v2.js'), 'mix', CLAIM])
invoke('report', ['python3', str(INSTRUMENT / 'tools/acc/eye_report_v1.py'), CLAIM, '--json'])
print(json.dumps({'status': 'RECORDED', 'inputs': str(INPUTS), 'verification_status': report['status']}))
