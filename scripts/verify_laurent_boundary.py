#!/usr/bin/env python3
"""Build, audit and independently kernel-check the arbitrary-size Laurent boundary module.

Run from any directory: python3 scripts/verify_offset_completion.py
Uses the repository's pinned Lean/mathlib installation. Reports live in
verification/offset_completion and include the exact checked commit and hashes.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from source_revision import source_revision

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification' / 'laurent_boundary'
MODULES = ('LaurentBoundary',)
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
OUT.mkdir(parents=True, exist_ok=True)
report = {'status': 'RUNNING', 'checks': {}, 'modules': {}}


def run(name, argv, negative=False):
    proc = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=480)
    (OUT / (name + '.log')).write_text(proc.stdout)
    print(name, proc.returncode, proc.stdout, flush=True)
    report['checks'][name] = {'exit_code': proc.returncode,
                             'expected_failure': negative, 'argv': argv}
    if negative:
        if proc.returncode == 0 or not re.search(
                r'proved that the proposition.*false|unsolved goals', proc.stdout, re.S):
            raise RuntimeError('False control was not mathematically rejected: ' + name)
        if re.search(r'unknown (?:module|identifier|constant)|unexpected token', proc.stdout):
            raise RuntimeError('False control infrastructure error: ' + name)
    elif proc.returncode:
        raise RuntimeError(name + ' failed')
    return proc.stdout


try:
    report['commit'] = source_revision(ROOT)
    report['lean_version'] = subprocess.check_output(
        ['lake', 'env', 'lean', '--version'], cwd=ROOT, text=True).strip()
    report['lean_toolchain'] = (ROOT / 'lean-toolchain').read_text().strip()
    manifest = ROOT / 'lake-manifest.json'
    if manifest.exists():
        report['manifest_sha256'] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    run('build_all', ['lake', 'build'] + ['OperatorFirst.' + short for short in MODULES])
    for short in MODULES:
        module = 'OperatorFirst.' + short
        source = ROOT / 'OperatorFirst' / (short + '.lean')
        names = re.findall(r'^theorem\s+(\w+)', source.read_text(), re.M)
        if not names:
            raise RuntimeError('No theorems discovered in ' + module)
        report['modules'][module] = {
            'named_theorems': len(names), 'theorems': names,
            'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
        run(short + '_build', ['lake', 'build', module])
        log = run(short + '_axioms', ['lake', 'env', 'lean', str(source.relative_to(ROOT))])
        matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
        found = {name for name, _ in matches} | set(re.findall(
            r"'([^']+)' does not depend on any axioms", log))
        missing = {module + '.' + name for name in names} - found
        if missing:
            raise RuntimeError('Missing axiom audit: ' + ', '.join(sorted(missing)))
        for name, axioms in matches:
            extras = {a.strip() for a in axioms.split(',') if a.strip()} - ALLOWED
            if extras:
                raise RuntimeError('Unapproved axiom in ' + name + ': ' + str(extras))
        run(short + '_kernel', ['lake', 'env', 'leanchecker', module])
    controls = {
        'false_two_columns_affine': """import OperatorFirst.LaurentBoundary
open LaurentPolynomial
example : ((T 1 * T 1 : LaurentPolynomial ℚ).coeff 2) = 0 := by
  norm_num [← T_add, T_apply]
""",
        'false_top_coefficient_sign': """import OperatorFirst.LaurentBoundary
open LaurentPolynomial
example : ((C (2:ℚ) * T 1 * (C 3 * T 1) : LaurentPolynomial ℚ).coeff 2) = -6 := by
  norm_num [← single_eq_C_mul_T, AddMonoidAlgebra.single_mul_single,
    AddMonoidAlgebra.coeff_single]
""",
    }
    for name, content in controls.items():
        source = OUT / (name + '.lean')
        source.write_text(content)
        run(name, ['lake', 'env', 'lean', str(source.relative_to(ROOT))], negative=True)
    report['named_theorems'] = sum(m['named_theorems'] for m in report['modules'].values())
    report['status'] = 'PASS'
except Exception as exc:
    report['status'] = 'FAIL'
    report['error'] = str(exc)
finally:
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
sys.exit(0 if report['status'] == 'PASS' else 1)
