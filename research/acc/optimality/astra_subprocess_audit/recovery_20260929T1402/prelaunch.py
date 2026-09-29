"""Resume only row three after receipt recovery and existing controls."""
import hashlib
import json
from pathlib import Path
import subprocess

root=Path.cwd()
ctl=json.loads((root/'work/astra_recovery_20260929T1303/control.json').read_text())
assert ctl['passed'] and ctl['stage']=='all_controls_passed'
for name,want in ctl['binary_sha256'].items():
    assert hashlib.sha256((root/'bin'/name).read_bytes()).hexdigest()==want
assert subprocess.check_output(['git','-C','SAIR','rev-parse','HEAD'],text=True).strip()==ctl['sair_pin']
assert not subprocess.check_output(['git','-C','SAIR','status','--porcelain','--untracked-files=no'],text=True).strip()
assert (root/'work/T8.tab').stat().st_size==640000000
with (root/'work/T8.tab').open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()=='38f05b56d5e79d9df03cc3cd96cd8433725b051111984a8dad4fbe30d07068f8'
source=json.loads((root/'research/acc/live/targets_astra_wide_20260929T0720Z.json').read_text())
assert source==json.loads((root/'work/astra_wide_targets.json').read_text())
assert source[:3]==json.loads((root/'work/astra_wide_first3.json').read_text())
rows=[json.loads(l) for l in (root/'work/astra_wide_cap.jsonl').read_text().splitlines()]
assert [r['id'] for r in rows]==['ac-04316','ac-07194']
assert all(r['official_checks'][b]['ok'] for r in rows for b in ('ac','sac'))
status=json.loads(subprocess.check_output(['python3','work/astra_recovery_20260929T1303/inspect.py'],text=True))
searches=[p for p in status['processes'] if Path(p['command'][0]).name in ('acc_beam','acc_window') or any(Path(a).name=='run_beam_raw.py' for a in p['command'][1:])]
assert not searches,searches
man=json.loads((root/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
target=next(c for c in man['challenges'] if c['challenge_id']=='ac-05423')
E={1:0,-1:1,2:2,-2:3}
enc=[s for w in target['initial_relators'] for s in [str(len(w)),*[str(E[x]) for x in w]]]
receipts=[json.loads(s) for s in (root/'work/astra_resume_20260929T0328/subprocess_audit/executions.jsonl').read_text().splitlines()]
finished=[r for r in receipts if Path(r['command'][0]).name=='acc_beam' and r['command'][2:4]==['200000','35'] and r['command'][4:]==enc]
assert not finished, 'Recover finished row-three audit receipt instead of repeating beam'
events=[json.loads(s) for s in (root/'work/astra_resume_20260929T0328/wide_watch_events.jsonl').read_text().splitlines()]
assert not any(e.get('id')=='ac-05423' and e.get('event')=='ROW_COMPLETE' for e in events)
print('PASS: 2 verified rows; unfinished 05423; pin/table/binaries/control intact; no live search; no completed row-three receipt. Watcher next cursor2.')
