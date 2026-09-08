#!/usr/bin/env python3
"""Compile both pinned projects and reject every deliberately false control.
Requires Python 3, Git, and elan with lake on PATH. No source edits are needed.
"""
from pathlib import Path
import subprocess, json, re, hashlib, sys, time
root=Path(__file__).resolve().parent
reports=[]
for project in (sys.argv[1:] or ['lean_4_19_0','lean_4_33_0']):
    p=root/project;logs=p/'evidence';logs.mkdir(exist_ok=True)
    report={'project':project,'commands':[],'negative_controls':[]}
    def run(args, name):
        start=time.monotonic();r=subprocess.run(args,cwd=p,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        (logs/(name+'.log')).write_text(r.stdout)
        item={'command':args,'exit_code':r.returncode,'seconds':time.monotonic()-start,'log':name+'.log'}
        report['commands'].append(item);print(project,name,r.returncode,flush=True)
        return r
    for args,name in [(['lake','--version'],'lake_version'),(['lake','env','lean','--version'],'lean_version'),(['lake','update'],'lake_update'),(['lake','exe','cache','get'],'cache'),(['lake','build'],'build'),(['lake','env','lean','FreshAxiomAudit.lean'],'axiom_audit')]:
        r=run(args,name)
        if r.returncode:
            (logs/'report.json').write_text(json.dumps(report,indent=2));print(r.stdout);raise SystemExit(r.returncode)
        if name=='axiom_audit': print(r.stdout, flush=True)
        if name=='axiom_audit' and 'sorryAx' in r.stdout:
            raise SystemExit('Rejected: axiom audit includes sorryAx')
    for f in sorted((p/'negative').glob('*.lean')):
        r=run(['lake','env','lean',str(f.relative_to(p))],f.stem)
        item={'file':str(f.relative_to(p)),'exit_code':r.returncode,'rejected':r.returncode!=0}
        report['negative_controls'].append(item)
        print(r.stdout, flush=True)
        if not r.returncode:raise SystemExit('False control unexpectedly accepted: '+str(f))
        if 'unsolved goals' not in r.stdout and 'failed' not in r.stdout:
            raise SystemExit('Negative control failed for an unexpected reason; inspect '+f.stem+'.log')
    report['sources']=[{'file':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'theorem_count':len(re.findall(r'^theorem\s+',f.read_text(),re.M))} for f in sorted(p.rglob('*.lean')) if '.lake' not in f.parts]
    report['accepted']=True;(logs/'report.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
(root/'fresh_lean_report.json').write_text(json.dumps(reports,indent=2)+'\n')
print('Both pinned projects compiled; all false controls were rejected.')
