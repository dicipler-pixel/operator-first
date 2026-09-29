"""Opt-in subprocess audit for the unchanged run_beam_raw.py runner.

Enable only for that runner by adding this directory to PYTHONPATH and setting
ASTRA_SUBPROCESS_AUDIT_DIR. Search decisions, arguments and BEAM settings are not
modified. A failed executable stops the runner before it can append 'nopath'.
"""
import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import time

_audit_dir = os.environ.get('ASTRA_SUBPROCESS_AUDIT_DIR')
_original_run = subprocess.run

def _audited_run(*args, **kwargs):
    result = _original_run(*args, **kwargs)
    command = result.args
    if not isinstance(command, (list, tuple)) or not command:
        return result
    program = Path(str(command[0])).name
    if program not in ('acc_beam', 'acc_window'):
        return result
    destination = Path(_audit_dir)
    destination.mkdir(parents=True, exist_ok=True)
    stem = str(time.time_ns()) + '_' + program
    for name, data in [('stdout', result.stdout), ('stderr', result.stderr)]:
        if data is not None:
            if isinstance(data, str):
                data = data.encode()
            (destination / (stem + '.' + name)).write_bytes(data)
    receipt = dict(
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
        command=[str(a) for a in command], returncode=result.returncode,
        stdout_file=stem+'.stdout', stderr_file=stem+'.stderr',
    )
    with (destination / 'executions.jsonl').open('a') as handle:
        handle.write(json.dumps(receipt) + '\n')
        handle.flush()
        os.fsync(handle.fileno())
    result.check_returncode()
    if program == 'acc_beam':
        output = result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout
        if not output or not re.search(r'^AC (?:NONE|\d+ PATH)', output, re.M) or not re.search(r'^SAC (?:NONE|\d+ PATH)', output, re.M):
            raise RuntimeError('acc_beam exited zero without explicit AC and SAC results; raw logs: ' + stem)
    return result

if _audit_dir:
    subprocess.run = _audited_run
