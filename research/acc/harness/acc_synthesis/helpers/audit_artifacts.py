#!/usr/bin/env python3
"""Refuse persistence of changed completed evidence; optionally flush local files."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import sqlite3


def audit_all(root, sync=False):
    root=Path(root).resolve()
    cp=json.loads((root/'continuation/checkpoint.json').read_text())
    checked=set()
    def check(name,expected):
        p=(root/name).resolve();p.relative_to(root)
        with p.open('rb') as f:
            digest=hashlib.sha256()
            for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
            actual=digest.hexdigest()
            if actual!=expected:raise ValueError('Completed evidence hash mismatch: '+name)
            if sync:os.fsync(f.fileno())
        checked.add(name)
        return p
    for a in cp['attempts']:
        if not a.get('result_path'):
            if a['kind']!='interrupted':raise ValueError('Terminal attempt lacks result: '+a['key'])
            continue
        p=check(a['result_path'],a['result_sha256'])
        for e in json.loads(p.read_text()).get('evidence',[]):check(e['path'],e['sha256'])
    db=root/'state/ledger.sqlite3'
    if db.exists():
        with contextlib.closing(sqlite3.connect(db)) as conn:
            if sync and conn.execute('pragma wal_checkpoint(FULL)').fetchone()[0]!=0:
                raise ValueError('SQLite checkpoint busy; persistence must wait')
            if conn.execute('pragma integrity_check').fetchone()[0]!='ok':
                raise ValueError('SQLite integrity check failed')
            completed={a['key'] for a in cp['attempts'] if a.get('result_path')}
            for task_id,payload,status in conn.execute("select id,payload,status from tasks where role='code_search'"):
                if json.loads(payload).get('key') in completed and status!='completed':
                    raise ValueError(f'Completed checkpoint conflicts with local task {task_id}: {status}')
        if sync:
            with db.open('rb') as f:os.fsync(f.fileno())
    return {'status':'verified','attempts':len(cp['attempts']),'unique_artifacts_checked':len(checked),'synced':sync}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',default=str(Path(__file__).resolve().parents[1]))
    p.add_argument('--sync',action='store_true');a=p.parse_args()
    print(json.dumps(audit_all(a.root,a.sync)))
