#!/usr/bin/env python3
"""Compile, inventory, kernel-recheck and record the finite Kakeya bridges.

Every invocation creates a new evidence directory, including failed attempts.
This gate audits defining modules rather than guessing namespaces from filenames.
Definition bodies and theorem types accompany axiom lists; mathematical scope
still requires the separate review/DEFINITION_AUDIT.md assessment.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
OUT = ROOT / 'verification' / 'kakeya_bridges' / STAMP
OUT.mkdir(parents=True, exist_ok=False)
MODULES = [
    'OperatorFirst.KakeyaDenominators',
    'OperatorFirst.KakeyaCutCompletion',
    'OperatorFirst.KakeyaForcingBridge',
    'OperatorFirst.KakeyaAuditControls',
    'OperatorFirst.KakeyaCutAssumptionControl',
]
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
REQUIRED = {
    'OperatorFirst.KakeyaDenominators.clear_row_denominators',
    'OperatorFirst.KakeyaDenominators.stepQ_iff_stepZ',
    'OperatorFirst.KakeyaCutCompletion.completion_has_independent_surviving_labels',
    'OperatorFirst.KakeyaAuditControls.rational_unit_without_integer_unit',
    'OperatorFirst.KakeyaAuditControls.same_range_different_kernels',
}
LAKE = os.environ.get('KAKEYA_LAKE', 'lake')
report = {
    'schema': 'kakeya-bridges-verification-v1', 'status': 'RUNNING',
    'started_utc': STAMP, 'checks': {}, 'sources': {},
    'github_sha': os.environ.get('GITHUB_SHA'),
    'github_head_sha': os.environ.get('PR_HEAD_SHA'),
    'github_run_id': os.environ.get('GITHUB_RUN_ID'),
    'local_compatibility_wrapper': LAKE != 'lake',
    'scope': 'Finite nonzero-multiple forcing; no Euclidean exponent, unit-target equivalence, or search completeness claim.',
}


def run(name, argv, expected_rejection=False):
    start = datetime.now(timezone.utc).isoformat()
    try:
        p = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=1200)
        output, code = p.stdout, p.returncode
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ''
        if isinstance(output, bytes):
            output = output.decode(errors='replace')
        output += '\nVERIFIER_TIMEOUT\n'
        code = 124
    path = OUT / (name + '.log')
    path.write_text(output)
    report['checks'][name] = {
        'argv': argv, 'started_utc': start, 'exit_code': code,
        'expected_rejection': expected_rejection,
        'log': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    print(f'{name}: exit {code} ({path.name})', flush=True)
    if expected_rejection:
        if code == 0 or not re.search(r'unsolved goals|proved that the proposition.*false', output, re.S):
            raise RuntimeError(name + ': expected mathematical rejection was absent')
        if re.search(r'unknown (module|identifier|constant)|unexpected token|failed to locate', output):
            raise RuntimeError(name + ': infrastructure failure is not a negative control')
    elif code:
        raise RuntimeError(name + ' failed; see retained log')
    return output


try:
    for module in MODULES:
        p = ROOT / (module.replace('.', '/') + '.lean')
        report['sources'][str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    for name in ['lean-toolchain', 'lakefile.toml', 'lake-manifest.json',
                 'scripts/AuditKakeyaBridges.lean', 'scripts/verify_kakeya_bridges.py']:
        p = ROOT / name
        report['sources'][name] = hashlib.sha256(p.read_bytes()).hexdigest()
    for name in report['sources']:
        saved = OUT / 'sources' / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes((ROOT / name).read_bytes())
    run('lean_version', [LAKE, 'env', 'lean', '--version'])
    manifest = json.loads((ROOT / 'lake-manifest.json').read_text())
    mathlib = next(p for p in manifest['packages'] if p['name'] == 'mathlib')
    report['mathlib_revision'] = mathlib['rev']
    if mathlib['rev'] != 'db584cd6d46c92f209a44c0f1c829460d327499d':
        raise RuntimeError('unexpected mathlib revision')
    run('build', [LAKE, 'build', *MODULES])
    for module in MODULES:
        run(module + '_kernel', [LAKE, 'env', 'leanchecker', '-v', module])
    audit = run('declaration_audit', [LAKE, 'env', 'lean', 'scripts/AuditKakeyaBridges.lean'])
    rows = [json.loads(line.split('AUDIT_JSON ', 1)[1])
            for line in audit.splitlines() if 'AUDIT_JSON ' in line]
    if not rows or {row['module'] for row in rows} != set(MODULES):
        raise RuntimeError('missing defining module in audit')
    seen = {row['name'] for row in rows}
    if REQUIRED - seen:
        raise RuntimeError('missing required declarations: ' + repr(REQUIRED - seen))
    for row in rows:
        if set(row['axioms']) - ALLOWED or row['kind'] == 'axiom':
            raise RuntimeError('unapproved declaration: ' + row['name'])
    (OUT / 'declarations.json').write_text(json.dumps(sorted(rows, key=lambda x: x['name']), indent=2) + '\n')
    report['declarations'] = len(rows)
    report['theorem_declarations_including_generated'] = [row['name'] for row in rows if row['kind'] == 'theorem']
    report['top_level_theorem_declarations'] = [row['name'] for row in rows
        if row['kind'] == 'theorem' and '.' not in row['name'].removeprefix(row['module'] + '.')]
    # The counterexample propositions themselves are compiled theorems. These
    # deliberate failed proofs ensure the gate also rejects their negations.
    negatives = {
        'false_integer_unit': 'import OperatorFirst.KakeyaAuditControls\nexample : (∃ z : ℤ, 2 * z = 1) := by\n  have h := OperatorFirst.KakeyaAuditControls.rational_unit_without_integer_unit.2\n  simp_all\n',
        'false_equal_kernel': 'import OperatorFirst.KakeyaAuditControls\nexample : LinearMap.ker (LinearMap.fst ℚ ℚ ℚ) = LinearMap.ker (LinearMap.snd ℚ ℚ ℚ) := by\n  have h := OperatorFirst.KakeyaAuditControls.same_range_different_kernels.2\n  simp_all\n',
    }
    for name, source in negatives.items():
        p = OUT / (name + '.lean')
        p.write_text(source)
        run(name, [LAKE, 'env', 'lean', str(p.relative_to(ROOT))], True)
    report['status'] = 'PASS'
except Exception as exc:
    report['status'] = 'FAIL'
    report['error'] = str(exc)
finally:
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'evidence': str(OUT),
                      'error': report.get('error')}, indent=2), flush=True)
sys.exit(0 if report['status'] == 'PASS' else 1)
