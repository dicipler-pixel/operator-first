#!/usr/bin/env python3
"""Restore large source files from checked repository pieces, without network."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def restore():
    manifest = json.loads((ROOT / 'large-files.json').read_text())
    for row in manifest['files']:
        target = (ROOT / row['path']).resolve()
        assert target.is_relative_to(ROOT)
        if target.is_file():
            assert target.stat().st_size == row['bytes'] and hashlib.sha256(target.read_bytes()).hexdigest() == row['sha256'], 'Existing file differs; refusing overwrite'
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        temp = target.with_suffix(target.suffix + '.restoring')
        h = hashlib.sha256()
        total = 0
        with temp.open('xb') as out:
            for part in row['parts']:
                source = (ROOT / part['path']).resolve()
                assert source.is_relative_to(ROOT)
                data = source.read_bytes()
                assert len(data) == part['bytes'] and hashlib.sha256(data).hexdigest() == part['sha256']
                out.write(data)
                h.update(data)
                total += len(data)
        assert total == row['bytes'] and h.hexdigest() == row['sha256']
        temp.replace(target)
    return len(manifest['files'])


if __name__ == '__main__':
    print(json.dumps({'verified_large_files': restore(), 'all_hashes_match': True}))
