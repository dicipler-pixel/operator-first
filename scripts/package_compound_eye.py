#!/usr/bin/env python3
"""Build a complete deterministic ZIP from the current tracked tool source."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools/compound-eye'


def files():
    return sorted(p for p in TOOL.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')


def main():
    from restore_large_files import restore
    restore()
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    manifest = {'release': '3.2', 'source_releases': ['2.2', '3.1'],
                'scope': 'File identity, not scientific certification.', 'files': {}}
    for p in files():
        if p.name == 'UNIVERSAL_MANIFEST.json' and p.parent == TOOL:
            continue
        manifest['files'][str(p.relative_to(TOOL))] = hashlib.sha256(p.read_bytes()).hexdigest()
    (TOOL / 'UNIVERSAL_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    archive = args.output / 'Compound_Eye_Universal_3_2_Complete.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files():
            info = zipfile.ZipInfo('compound_eye_universal_3_2/' + str(p.relative_to(TOOL)), (2026, 9, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 << 16)
            z.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    html = args.output / 'Compound_Eye_Universal_3_2.html'
    shutil.copy2(TOOL / 'START_HERE.html', html)
    print(json.dumps({'archive': str(archive.resolve()), 'archive_bytes': archive.stat().st_size,
                      'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                      'html': str(html.resolve()), 'manifest_files': len(manifest['files'])}))


if __name__ == '__main__':
    main()
