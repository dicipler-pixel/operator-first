#!/usr/bin/env python3
"""Recover a sealed receipt from a complete GitHub job log and verify each file."""
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tarfile

log = Path(sys.argv[1]).read_text()
destination = Path(sys.argv[2]).resolve()
manifest_rows = re.findall(r'KAKEYA_RECEIPT_MANIFEST (\{[^\n]*\})', log)
if len(manifest_rows) != 1:
    raise SystemExit('Expected exactly one receipt manifest')
manifest = json.loads(manifest_rows[0])
found = re.findall(r'KAKEYA_RECEIPT_CHUNK (\d+)/(\d+) ([A-Za-z0-9+/=]+)', log)
chunks = {}
for index, total, content in found:
    index = int(index)
    if int(total) != manifest['chunks'] or index in chunks:
        raise SystemExit('Inconsistent or duplicate receipt chunk')
    chunks[index] = content
if set(chunks) != set(range(1, manifest['chunks'] + 1)):
    raise SystemExit('Missing receipt chunk')
data = base64.b64decode(''.join(chunks[i] for i in sorted(chunks)), validate=True)
if len(data) != manifest['bytes'] or hashlib.sha256(data).hexdigest() != manifest['sha256']:
    raise SystemExit('Receipt byte count or checksum mismatch')
if 'KAKEYA_RECEIPT_END ' + manifest['sha256'] not in log:
    raise SystemExit('Missing receipt end marker')
expected = {item['path']: item for item in manifest['entries']}
if len(expected) != len(manifest['entries']):
    raise SystemExit('Duplicate manifest entry')
verified = {}
with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
    members = archive.getmembers()
    if len(members) != len(expected) or {m.name for m in members} != set(expected):
        raise SystemExit('Archive inventory mismatch')
    for member in members:
        path = Path(member.name)
        if not member.isfile() or path.is_absolute() or '..' in path.parts:
            raise SystemExit('Invalid receipt member')
        payload = archive.extractfile(member).read()
        entry = expected[member.name]
        if len(payload) != entry['bytes'] or hashlib.sha256(payload).hexdigest() != entry['sha256']:
            raise SystemExit('Entry checksum mismatch: ' + member.name)
        verified[member.name] = payload
destination.mkdir(parents=True, exist_ok=True)
if any(destination.iterdir()):
    raise SystemExit('Use a fresh receipt destination')
(destination / 'receipt.tar.xz').write_bytes(data)
(destination / 'receipt_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
for name, payload in verified.items():
    path = destination / 'extracted' / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
print(json.dumps({'status': 'EXACT_RECEIPT_VERIFIED', 'files': len(verified),
                  'sha256': manifest['sha256'], 'destination': str(destination)}))
