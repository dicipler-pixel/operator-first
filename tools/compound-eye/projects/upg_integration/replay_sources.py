"""Replay supplied sources without hiding incomplete dependencies."""
from pathlib import Path
import json,os,subprocess,sys,time
root=Path(__file__).resolve().parent;logs=root/'logs';logs.mkdir(exist_ok=True)
env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MPLBACKEND':'Agg'}
rows=[]
for p in sorted((root/'upg_source').glob('*.py'))+sorted((root/'bodies_source').glob('*.py')):
    original=p;note='Original supplied program'
    if p.name=='upg_nct_figs.py':
        figs=root/'figures';figs.mkdir(exist_ok=True)
        target=logs/'upg_nct_figs_portable.py'
        target.write_text(p.read_text().replace('/home/claude/',figs.as_posix()+'/'))
        p=target;note='Working copy changes only hardcoded figure output directory; original retained.'
    started=time.time()
    try:
        r=subprocess.run([sys.executable,str(p)],cwd=logs,env=env,capture_output=True,text=True,timeout=120)
        text=r.stdout+r.stderr;code=r.returncode
    except subprocess.TimeoutExpired as e:
        text='TIMEOUT after 120 seconds';code=None
    (logs/(original.stem+'.txt')).write_text(text)
    rows.append({'source':str(original.relative_to(root)),'exit_code':code,'seconds':time.time()-started,'note':note,
                 'status':'ran' if code==0 else 'blocked_or_failed','last_line':text.strip().splitlines()[-1] if text.strip() else ''})
(root/'source_runs.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
