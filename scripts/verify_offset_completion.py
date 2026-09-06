#!/usr/bin/env python3
"""Build, audit and independently kernel-check the Offset completion modules.

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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification' / 'offset_completion'
MODULES = ('EndpointTransfer', 'FiniteCovariance', 'BandObstruction')
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
    report['commit'] = subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
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
        'false_transfer_sign': '''import OperatorFirst.EndpointTransfer
example : OperatorFirst.Offset.asymmetry
    (OperatorFirst.EndpointTransfer.mix (1/2) 1 3)
    (OperatorFirst.EndpointTransfer.mix (-(1/2)) 1 3) = -(1/4 : ℝ) := by
  norm_num [OperatorFirst.Offset.asymmetry, OperatorFirst.EndpointTransfer.mix]
''',
        'false_error_denominator': '''import OperatorFirst.EndpointTransfer
example : |OperatorFirst.Offset.asymmetry (1-(1/2)) (1+(1/2)) -
    OperatorFirst.Offset.asymmetry 1 1| ≤ (1/2 : ℝ)/(1+1/2) := by
  norm_num [OperatorFirst.Offset.asymmetry]
''',
        'false_decoupled_obstruction': '''import OperatorFirst.BandObstruction
example : ¬ ((∀ z : ℂ, z*(1:ℂ)^2 =
    (OperatorFirst.BandObstruction.dispersion 0 0 1).eval z) ∧
    (∀ z : ℂ, z*1*(1:Polynomial ℂ).eval z =
      1*z*(1:Polynomial ℂ).eval z-(0*z+0)*(0:Polynomial ℂ).eval z)) := by
  norm_num [OperatorFirst.BandObstruction.dispersion]
''',
        'false_strictness_from_projection_alone': '''import OperatorFirst.FiniteCovariance
example : 0 < (1-(1 : Matrix (Fin 1) (Fin 1) ℝ)).det := by
  norm_num
''',
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
