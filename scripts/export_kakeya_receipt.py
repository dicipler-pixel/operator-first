#!/usr/bin/env python3
"""Seal complete CI evidence into job logs when artifact transport is unavailable.

All inputs are the verifier's output directory. No credentials, environment
variables or repository secrets are read. Chunk counts, bytes and SHA-256 make
truncation detectable; the ordinary artifact remains available too.
"""
import base64
import hashlib
import io
import json
from pathlib import Path
import tarfile

root = Path(__file__).resolve().parents[1]
evidence = root / 'verification' / 'kakeya_bridges'
reports = sorted(evidence.glob('*/report.json'))
if not reports:
    raise SystemExit('No verification report to preserve')
latest = reports[-1].parent
buffer = io.BytesIO()
entries = []
with tarfile.open(fileobj=buffer, mode='w:xz', preset=6) as archive:
    for path in sorted(latest.rglob('*')):
        if not path.is_file():
            continue
        data = path.read_bytes()
        name = str(path.relative_to(latest))
        entries.append({'path': name, 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
        archive.add(path, arcname=name, recursive=False)
sealed = buffer.getvalue()
if len(sealed) > 2_000_000:
    raise SystemExit('Receipt exceeds explicit log transport limit')
encoded = base64.b64encode(sealed).decode()
chunks = [encoded[i:i+4000] for i in range(0, len(encoded), 4000)]
manifest = {'schema': 'kakeya-ci-log-receipt-v1', 'format': 'tar.xz',
            'bytes': len(sealed), 'sha256': hashlib.sha256(sealed).hexdigest(),
            'chunks': len(chunks), 'entries': entries}
print('KAKEYA_RECEIPT_MANIFEST ' + json.dumps(manifest, separators=(',', ':')), flush=True)
for index, chunk in enumerate(chunks):
    print(f'KAKEYA_RECEIPT_CHUNK {index+1}/{len(chunks)} {chunk}', flush=True)
print('KAKEYA_RECEIPT_END ' + manifest['sha256'], flush=True)
