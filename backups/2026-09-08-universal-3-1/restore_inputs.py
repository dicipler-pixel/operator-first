"""Restore the three original user uploads, verifying every byte."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--output', type=Path, required=True)
args = ap.parse_args()
dest = args.output.resolve()
if dest.exists() and any(dest.iterdir()):
    raise ValueError('Choose an empty output directory.')
dest.mkdir(parents=True, exist_ok=True)
manifest = json.loads((ROOT / 'INPUTS.json').read_text())
for row in manifest['files']:
    target = (dest / row['name']).resolve()
    assert target.is_relative_to(dest)
    h = hashlib.sha256()
    total = 0
    with target.open('xb') as out:
        for part in row['parts']:
            source = (ROOT / part['path']).resolve()
            assert source.is_relative_to(ROOT)
            data = source.read_bytes()
            assert len(data) == part['bytes'] and hashlib.sha256(data).hexdigest() == part['sha256']
            out.write(data)
            h.update(data)
            total += len(data)
    assert total == row['bytes'] and h.hexdigest() == row['sha256']
print(json.dumps({'restored_files': len(manifest['files']), 'all_hashes_match': True}))
