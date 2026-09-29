"""Check failure handling with tiny stub executables, without running a search."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

hook = Path(__file__).resolve().parent
results = []
with tempfile.TemporaryDirectory(prefix='astra_guard_check_') as temporary:
    root = Path(temporary)
    env = dict(os.environ, PYTHONPATH=str(hook), ASTRA_SUBPROCESS_AUDIT_DIR=str(root/'audit'))
    cases = [
        ('beam_failure', 'acc_beam', 7, 'AC NONE\nSAC NONE\n', 'CalledProcessError'),
        ('beam_empty_success', 'acc_beam', 0, '', 'RuntimeError'),
        ('beam_explicit_negative', 'acc_beam', 0, 'AC NONE\nSAC NONE\n', None),
        ('window_failure', 'acc_window', 8, '', 'CalledProcessError'),
    ]
    for name, program, returncode, output, expected in cases:
        executable = root / program
        executable.write_text('#!'+sys.executable+'\nimport sys\nsys.stdout.write('+repr(output)+')\nraise SystemExit('+str(returncode)+')\n')
        executable.chmod(0o755)
        client = '''import json, subprocess, sys
try:
    p = subprocess.run([sys.argv[1]], capture_output=True, text=True)
    result = dict(error=None, returncode=p.returncode, stdout=p.stdout)
except (subprocess.CalledProcessError, RuntimeError) as e:
    result = dict(error=type(e).__name__)
print(json.dumps(result))
'''
        completed = subprocess.run([sys.executable, '-c', client, str(executable)], env=env, capture_output=True, text=True, check=True)
        actual = json.loads(completed.stdout)
        assert actual['error'] == expected, (name, actual, completed.stderr)
        if expected is None:
            assert actual['stdout'] == output
        results.append(dict(case=name, passed=True, **actual))
    receipts = [json.loads(line) for line in (root/'audit/executions.jsonl').read_text().splitlines()]
    assert len(receipts) == 4
    assert [r['returncode'] for r in receipts] == [7, 0, 0, 8]
    assert all((root/'audit'/r['stdout_file']).exists() and (root/'audit'/r['stderr_file']).exists() for r in receipts)
print(json.dumps(dict(passed=True, cases=results, execution_receipts=len(receipts)), indent=2))
