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
import sys
import time

_audit_dir = os.environ.get('ASTRA_SUBPROCESS_AUDIT_DIR')
_original_run = subprocess.run

def _verified_window_fallback(command, result):
    """Retain an independently verified input after this known optional-step error.

    This does not certify a board submission or a shortest path. The watcher
    must still verify the final AC/SAC path against its actual manifest row.
    """
    if os.environ.get('ASTRA_VERIFIED_WINDOW_FALLBACK') != '1':
        return None
    output = result.stdout.decode() if isinstance(result.stdout, bytes) else (result.stdout or '')
    error = result.stderr.decode() if isinstance(result.stderr, bytes) else (result.stderr or '')
    if result.returncode != 3 or 'FATAL walk to s_j failed' not in error or 'FINALPATH' in output:
        return None
    root = Path.cwd()
    if Path(command[0]).resolve() != root / 'bin/acc_window':
        return None
    pin = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
    head = _original_run(['git', '-C', str(root/'SAIR'), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    if head != pin:
        raise RuntimeError('Cannot verify window fallback: SAIR pin differs')
    words = []; offset = 2; decode = {0: 1, 1: -1, 2: 2, 3: -2}
    for _ in range(2):
        length = int(command[offset]); offset += 1
        if length < 0:
            raise ValueError('Negative window word length')
        words.append([decode[int(x)] for x in command[offset:offset+length]])
        offset += length
    length = int(command[offset]); moves = list(map(int, command[offset+1:]))
    if length != len(moves):
        raise ValueError('Window input path length mismatch')
    sys.path.insert(0, str(root/'SAIR/competition/tools'))
    from verifier import core
    manifest = json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
    challenge = dict(challenge_id='literal-window-input-only', move_spec_version='ac-r2-v1',
                     initial_relators=words, target_relators=[[1], [2]])
    check = core.verify(challenge, moves, 'ac-r2-v1', manifest['limits'])
    if not check['ok']:
        raise RuntimeError('Failed window input also fails official replay: '+repr(check))
    return dict(reason='Known reconstruction error; retain original verified input, no shortening claimed',
                sair_commit=pin, literal_input_check=check, board_submission_verified=False)

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
    if program == 'acc_window' and result.returncode:
        fallback = _verified_window_fallback(command, result)
        if fallback:
            receipt['verified_input_fallback'] = fallback
    with (destination / 'executions.jsonl').open('a') as handle:
        handle.write(json.dumps(receipt) + '\n')
        handle.flush()
        os.fsync(handle.fileno())
    if not receipt.get('verified_input_fallback'):
        result.check_returncode()
    if program == 'acc_beam':
        output = result.stdout.decode() if isinstance(result.stdout, bytes) else result.stdout
        if not output or not re.search(r'^AC (?:NONE|\d+ PATH)', output, re.M) or not re.search(r'^SAC (?:NONE|\d+ PATH)', output, re.M):
            raise RuntimeError('acc_beam exited zero without explicit AC and SAC results; raw logs: ' + stem)
    return result

if _audit_dir:
    subprocess.run = _audited_run
