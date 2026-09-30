"""Observe the running Astra batch and verify new paths; never launch a search."""
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time

root = Path.cwd()
sys.path.insert(0, str(root / 'SAIR/competition/tools'))
from verifier import core, stable_core

manifest = json.loads((root / 'SAIR/competition/tools/verifier/data/manifest.json').read_text())
challenges = {c['challenge_id']: c for c in manifest['challenges']}
targets = {t['id']: t for t in json.loads((root / os.environ.get('ASTRA_WATCH_TARGETS', 'research/acc/live/targets_astra_rank_20260928T2050Z.json')).read_text())}
out = root / os.environ.get('ASTRA_WATCH_OUT', 'work/astra_rank_cap.jsonl')
checks_file = root / os.environ.get('ASTRA_WATCH_CHECKS', 'work/astra_resume_20260929T0328/new_path_checks.jsonl')
events_file = root / os.environ.get('ASTRA_WATCH_EVENTS', 'work/astra_resume_20260929T0328/watch_events.jsonl')
start, stop = int(sys.argv[1]), int(sys.argv[2])
cursor = start

def emit(record):
    with events_file.open('a') as f:
        f.write(json.dumps(record) + '\n')
    print(json.dumps(record), flush=True)

emit({'event': 'WATCH_STARTED', 'from_completed': start, 'stop_after': stop})
while cursor < stop:
    raw = out.read_text() if out.exists() else ''
    lines = raw.splitlines()
    if raw and not raw.endswith('\n'):
        lines = lines[:-1]
    for line in lines[cursor:stop]:
        r = json.loads(line)
        t = targets[r['id']]
        verified = []
        qualifying = []
        for board, verifier, spec in [('ac', core, 'ac-r2-v1'), ('sac', stable_core, 'sac-r8-v1')]:
            if board not in r:
                continue
            cid = board + '-' + r['id'].split('-')[1]
            check = verifier.verify(challenges[cid], r[board], spec, manifest['limits'])
            entry = dict(id=cid, moves=r[board], record=t[board+'_record'], verifier=check,
                         sair_commit='a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e')
            with checks_file.open('a') as f:
                f.write(json.dumps(entry) + '\n')
            if not check['ok']:
                emit({'event': 'VERIFICATION_FAILED', 'id': cid, 'check': check})
                raise SystemExit(2)
            verified.append(dict(id=cid, length=len(r[board]), record=t[board+'_record']))
            if len(r[board]) <= t[board+'_record']:
                qualifying.append((cid, r[board]))
        cursor += 1
        utc = dt.datetime.now(dt.timezone.utc)
        inbox = None
        if qualifying:
            inbox = root / 'research/acc/live/inbox' / (utc.strftime('%Y%m%dT%H%M%SZ') + '_astra_' + r['id'] + '.txt')
            inbox.parent.mkdir(parents=True, exist_ok=True)
            inbox.write_text(''.join(cid + ': ' + json.dumps(moves) + '\n' for cid, moves in qualifying))
        emit(dict(event='ROW_COMPLETE', utc=utc.isoformat(timespec='seconds'), completed=cursor,
                  id=r['id'], verdict=r['verdict'], wall_s=r['wall_s'], verified=verified,
                  qualifying_lines=len(qualifying), inbox=str(inbox) if inbox else None))
    if cursor < stop:
        time.sleep(2)
emit({'event': 'BATCH_OBSERVED', 'completed': cursor})
