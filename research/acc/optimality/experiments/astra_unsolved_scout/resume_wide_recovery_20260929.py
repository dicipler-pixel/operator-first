"""Recover finished wide row 1, then run only the first-three-row pilot.
No SAIR API calls or submissions. Run with the existing subprocess audit env.
"""
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

root = Path.cwd()
work = root / 'work/astra_scout_20260929'
lock = (work / 'resume_wide.lock').open('a')
fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
PIN = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
assert subprocess.check_output(['git', '-C', str(root/'SAIR'), 'rev-parse', 'HEAD'], text=True).strip() == PIN
assert (root/'work/T8.tab').stat().st_size == 640000000
with (root/'work/T8.tab').open('rb') as h:
    assert hashlib.file_digest(h, 'sha256').hexdigest() == '38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8'
sys.path.insert(0, str(root/'SAIR/competition/tools'))
from verifier import core, stable_core
manifest = json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch = {c['challenge_id']: c for c in manifest['challenges']}

def event(stage, **extra):
    data = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pid': os.getpid(), 'stage': stage, **extra}
    with (work/'resume_events.jsonl').open('a') as f:
        f.write(json.dumps(data)+'\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(data), flush=True)

def verify(cid, path):
    stable = cid.startswith('sac-')
    result = (stable_core if stable else core).verify(ch[cid], path, 'sac-r8-v1' if stable else 'ac-r2-v1', manifest['limits'])
    assert result['ok'], (cid, result)
    return result

event('waiting_for_positive_window_control')
deadline = time.monotonic() + 900
while True:
    probe = json.loads((work/'window_positive04953.json').read_text())
    if 'returncode' in probe:
        break
    if time.monotonic() > deadline:
        raise RuntimeError('Window positive-control receipt did not complete within 900 seconds')
    time.sleep(2)
assert probe['returncode'] in (0, 3), probe
control_output = (work/'window_positive04953.stdout').read_text()
control_paths = [list(map(int, m.group(1).split())) for m in re.finditer(r'^(?:FINALPATH|PATH) ([\d ]+)$', control_output, re.M)]
assert control_paths, 'No recoverable positive control path'
control_path = min(control_paths, key=len)
assert len(control_path) <= 37, probe
verify('ac-04953', control_path)
old = root/'bin/acc_window'
event('verified_intermediate_recovery_enabled', retained_binary_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),
      control_length=len(control_path), rebuilt_window_exit=probe['returncode'],
      underlying_window_fixed=False, recovery='guard preserves officially verified intermediate PATH; actual failure stays in audit')

out = root/'work/astra_wide_cap.jsonl'
done = {json.loads(line)['id'] for line in out.read_text().splitlines()} if out.exists() else set()
targets = json.loads((root/'work/astra_wide_targets.json').read_text())
assert [r['id'] for r in targets[:3]] == ['ac-04316','ac-07194','ac-05423']
first3 = root/'work/astra_wide_first3.json'
first3.write_text(json.dumps(targets[:3], indent=2)+'\n')
if 'ac-04316' not in done:
    t = targets[0]
    raw = (root/'work/astra_resume_20260929T0328/subprocess_audit/1790680368123435801_acc_beam.stdout').read_text()
    ac_raw = list(map(int, re.search(r'^AC \d+ PATH ([\d ]+)', raw, re.M)[1].split()))
    sac_raw = list(map(int, re.search(r'^SAC \d+ PATH ([\d ]+)', raw, re.M)[1].split()))
    ac = list(map(int, re.search(r'FINALPATH ?([\d ]*)', (work/'window_rebuild_probe.stdout').read_text())[1].split()))
    assert json.loads((work/'window_rebuild_probe.json').read_text())['returncode'] == 0
    verify('ac-04316', ac_raw); verify('sac-04316', sac_raw); verify('ac-04316', ac)
    E = {1:0,-1:1,2:2,-2:3}; SW={1:2,-1:-2,2:1,-2:-1}; PI={6:8,8:6,7:9,9:7,10:12,12:10,11:13,13:11}
    words = [[SW[x] for x in r] for r in ch['ac-04316']['initial_relators']]
    core_path = [PI.get(x,x) for x in sac_raw[:-2]]
    wd = work/'window_sac04316'; wd.mkdir(exist_ok=True)
    enc = []
    for r in words:
        enc += [str(len(r)), *[str(E[x]) for x in r]]
    event('recovering_finished_beam_sac_window', id='ac-04316', ac_len=len(ac), sac_beam=len(sac_raw))
    cp = subprocess.run([str(old),str(wd),*enc,str(len(core_path)),*map(str,core_path)], capture_output=True, text=True)
    (work/'wide04316_sac_window.stdout').write_text(cp.stdout)
    (work/'wide04316_sac_window.stderr').write_text(cp.stderr)
    match = re.search(r'FINALPATH ?([\d ]*)', cp.stdout)
    sac = sac_raw
    recovered = getattr(cp, 'astra_verified_window_path', None)
    if recovered is not None or match:
        literal = recovered if recovered is not None else list(map(int, match[1].split()))
        short = [PI.get(x,x) for x in literal] + [15,15]
        verify('sac-04316', short)
        if len(short) <= len(sac):
            sac = short
    if len(ac)+2 < len(sac):
        sac = ac+[16,15]
    checks = {'ac': verify('ac-04316', ac), 'sac': verify('sac-04316', sac)}
    rec = {'id':'ac-04316','record':t['record'],'k':t['k'],'checked':True,'seed':None,'noise':None,
           'ac_beam':len(ac_raw),'sac_beam':len(sac_raw),'ac':ac,'sac':sac,'ac_len':len(ac),'sac_len':len(sac),
           'wall_s':None,'verdict':'BEAT' if len(ac)<t['record'] else 'TIE' if len(ac)==t['record'] else 'above',
           'recovered_finished_beam_receipt':'1790680368123435801_acc_beam.stdout',
           'sac_window_returncode':cp.returncode,'sair_pin':PIN,'official_checks':checks}
    with out.open('a') as f:
        f.write(json.dumps(rec)+'\n'); f.flush(); os.fsync(f.fileno())
    event('row1_recovered_without_repeating_beam', ac_len=len(ac), sac_len=len(sac))

for name, value in {'BEAM_H':'1','BEAM_DIV':'0.8','BEAM_P2':'2','BEAM_QUOTA':'16','BEAM_ELITE':'5000','BEAM_DUAL':'0.75'}.items():
    assert os.environ[name] == value
assert not os.environ.get('BEAM_CHAIN')
event('starting_remaining_two_wide_rows', target_file=str(first3), width=200000, depth_rule='record+2')
command = [sys.executable,'research/acc/optimality/run_beam_raw.py','SAIR/competition/tools/verifier/data/manifest.json',
           'bin','work/T8.tab','work/w_astra_wide','200000','200','work/astra_wide_cap.jsonl',str(first3)]
with (root/'work/astra_wide.log').open('a') as log:
    completed = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
event('first_three_wide_pilot_stopped', returncode=completed.returncode, next_action='compare first3 gaps before any row4')
raise SystemExit(completed.returncode)
