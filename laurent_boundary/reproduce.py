#!/usr/bin/env python3
"""Reproduce the included Offset endpoint evidence without a research checkout."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def verify_manifest():
    expected = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
    for name, digest in expected.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError('Source hash mismatch: ' + name)
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['numerics', 'lean', 'all'], default='numerics')
    args = parser.parse_args()
    count = verify_manifest()
    out = ROOT / 'verification' / 'standalone'
    out.mkdir(parents=True, exist_ok=True)
    report = {'status': 'RUNNING', 'mode': args.mode, 'source_files_checked': count,
              'python': sys.version, 'platform': platform.platform(), 'runs': []}
    commands = []
    if args.mode in ('numerics', 'all'):
        import mpmath
        import sympy
        report['dependencies'] = {'mpmath': mpmath.__version__, 'sympy': sympy.__version__}
        if (mpmath.__version__, sympy.__version__) != ('1.3.0', '1.14.0'):
            raise RuntimeError('Install the versions in requirements.txt before this reference run.')
        commands += [
            [sys.executable, 'moduli_transfer/verify_moduli_transfer.py',
             '--out', 'verification/standalone/moduli_report.json'],
            [sys.executable, 'endpoint_progress/hankel_endpoint.py',
             '--out', 'verification/standalone/hankel_report.json'],
            [sys.executable, 'endpoint_progress/endpoint_probe.py', '--max-L', '21',
             '--dps', '160', '--cases', '.3,1,.4', '.6,1,.4', '1,1,.1',
             '--out', 'verification/standalone/endpoint_report.json'],
        ]
    if args.mode in ('lean', 'all'):
        commands += [[sys.executable, 'scripts/' + name] for name in (
            'verify_laurent_boundary.py', 'verify_offset.py', 'verify_endpoint.py',
            'verify_endpoint_progress.py', 'verify_offset_completion.py')]
    try:
        for i, command in enumerate(commands):
            print('Running:', ' '.join(command), flush=True)
            p = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, timeout=1800)
            log = out / ('run_%02d_%s.log' % (i + 1, args.mode))
            log.write_text(p.stdout)
            print(p.stdout[-4000:], flush=True)
            report['runs'].append({'command': command, 'exit_code': p.returncode,
                                   'log': str(log.relative_to(ROOT))})
            if p.returncode:
                raise RuntimeError('Reproduction command failed: ' + command[1])
        if args.mode in ('numerics', 'all'):
            moduli = json.loads((out / 'moduli_report.json').read_text())
            if moduli['status'] != 'PASS':
                raise RuntimeError('Moduli verification did not pass.')
            from mpmath import mp
            mp.dps = 100
            hankel = json.loads((out / 'hankel_report.json').read_text())
            errors = [abs(mp.mpf(row['difference'])) for case in hankel for row in case['rows']]
            prefactors = [abs(mp.mpf(case['prefactor_identity_error'])) for case in hankel]
            if max(errors + prefactors) >= mp.mpf('1e-55'):
                raise RuntimeError('Hankel cross-check exceeds the stated tolerance.')
            report['hankel_max_abs_error'] = str(max(errors))
            report['hankel_prefactor_max_abs_error'] = str(max(prefactors))
            report['numerical_scope'] = 'High-precision computation, not interval certification.'
        report['status'] = 'PASS'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = str(exc)
    (out / ('report_' + args.mode + '.json')).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
