#!/usr/bin/env python3
"""Build a self-contained source supplement from the current Offset workspace."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from source_revision import source_revision

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default='offset_endpoint_standalone.zip')
    args = ap.parse_args()
    destination = Path(args.out).resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        package = Path(temporary) / 'offset_endpoint_standalone'
        package.mkdir()

        def copy(source, target=None):
            src = ROOT / source
            dst = package / (target or source)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

        for name in ('OperatorFirst.lean', 'lakefile.toml', 'lean-toolchain', 'LICENSE'):
            copy(name)
        for name in ('Offset', 'OffsetFock', 'OffsetEndpoint', 'EndpointProgress',
                     'EndpointTransfer', 'FiniteCovariance', 'BandObstruction', 'LaurentBoundary'):
            copy('OperatorFirst/' + name + '.lean')
        for name in ('source_revision', 'verify_offset', 'verify_endpoint',
                     'verify_endpoint_progress', 'verify_offset_completion', 'verify_laurent_boundary'):
            copy('scripts/' + name + '.py')
        for name in ('endpoint_probe', 'hankel_endpoint', 'transfer_check', 'validation'):
            copy('endpoint_progress/' + name + '.py')
        for name in ('ALL_SIZE_TRANSFER.md', 'verify_moduli_transfer.py'):
            copy('moduli_transfer/' + name)
        copy('laurent_boundary/FORMAL_BOUNDARY_SCOPE.md', 'proofs/FORMAL_BOUNDARY_SCOPE.md')
        copy('laurent_boundary/ENDPOINT_ANALYSIS.md', 'proofs/ENDPOINT_ANALYSIS.md')
        copy('laurent_boundary/standalone_README.md', 'README.md')
        copy('laurent_boundary/reproduce.py', 'reproduce.py')
        for directory in ('endpoint_progress', 'offset_completion', 'moduli_transfer',
                          'laurent_boundary/evidence'):
            for p in (ROOT / directory).glob('*'):
                if p.is_file() and p.suffix in ('.json', '.log'):
                    copy(str(p.relative_to(ROOT)), 'evidence/' + directory + '/' + p.name)
        # A freshly executed checkout can add complete per-step evidence.
        for directory in ('endpoint', 'endpoint_progress', 'offset_completion', 'laurent_boundary'):
            src = ROOT / 'verification' / directory
            if src.exists():
                shutil.copytree(src, package / 'evidence' / 'current_lean' / directory)
        (package / 'requirements.txt').write_text('sympy==1.14.0\nmpmath==1.3.0\n')
        lakefile = package / 'lakefile.toml'
        lakefile.write_text(lakefile.read_text().replace('rev = "v4.33.0"',
            'rev = "db584cd6d46c92f209a44c0f1c829460d327499d"'))
        (package / 'SOURCE_REVISION.txt').write_text(source_revision(ROOT) + '\n')
        manifest = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(package.rglob('*')) if p.is_file() and
                    'evidence' not in p.relative_to(package).parts}
        (package / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(package.rglob('*')):
                if p.is_file():
                    z.write(p, str(p.relative_to(package.parent)))
    print(destination)
    print('SHA-256:', hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
