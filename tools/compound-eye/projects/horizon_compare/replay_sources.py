"""Replay selected supplied sources, without changing their scientific code.

Each process has a finite time budget. A zero exit is recorded as execution,
not blanket validation of paper claims. See SOURCE_AUDIT.md for interpretation.
"""
from pathlib import Path
import os, subprocess, sys, time, json, hashlib, platform, importlib.metadata
ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).parent/'sources'
OUT=ROOT/'runs/horizon/source_replay';OUT.mkdir(parents=True,exist_ok=True)
JOBS=['bh/bh_curv_01.py','bh/bh_ledger_01.py',
 'upg/upg_gate_01.py','upg/upg_gate_02.py','upg/upg_prove_01a.py','upg/upg_prove_02.py','upg/dirac_spine_01.py',
 'sun/bh_dynamo_01b.py','sun/shear_lane_01.py','sun/n_recovery_01b.py','sun/n_recovery_02_final.py','sun/dkist_compare_02.py']
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','MPLBACKEND':'Agg'}
rows=[]
for name in JOBS:
    path=BASE/name;start=time.perf_counter();log=OUT/(name.replace('/','__')+'.txt')
    with log.open('w') as f:
        try:
            r=subprocess.run([sys.executable,'-u',str(path)],cwd=path.parent,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180)
            status='executed' if r.returncode==0 else 'failed';exit_code=r.returncode
        except subprocess.TimeoutExpired:status='timeout';exit_code=None
    row={'source':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':status,'exit_code':exit_code,'seconds':round(time.perf_counter()-start,3),'log':str(log.relative_to(ROOT)),'evidence_stage':'theoretical_or_synthetic_source_replay'}
    rows.append(row);print(json.dumps(row),flush=True)
    (OUT/'manifest.json').write_text(json.dumps({'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in ['numpy','scipy','sympy','mpmath','networkx','matplotlib']},'jobs':rows,'scope':'Selected scripts only. Not a replay of every historical script or experimental analysis.'},indent=2))
if any(r['status']!='executed' for r in rows):sys.exit(1)
