#!/usr/bin/env python3
"""Compile and independently recheck all endpoint declarations and false controls."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification'/'endpoint_progress'
OUT.mkdir(parents=True,exist_ok=True)
MOD='OperatorFirst.EndpointProgress'
SOURCE=ROOT/'OperatorFirst'/'EndpointProgress.lean'
report={'status':'RUNNING','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'checks':{}}
def run(name,args,negative=False):
    p=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=360)
    (OUT/(name+'.log')).write_text(p.stdout)
    print(name,p.returncode,p.stdout,flush=True)
    report['checks'][name]={'exit_code':p.returncode,'argv':args,'expected_failure':negative}
    if negative:
        if p.returncode==0 or not re.search(r'proved that the proposition.*false|unsolved goals',p.stdout,re.S):
            raise RuntimeError('False control not mathematically rejected: '+name)
        if re.search(r'unknown (?:module|identifier|constant)|unexpected token',p.stdout):
            raise RuntimeError('False control infrastructure error: '+name)
    elif p.returncode: raise RuntimeError(name+' failed')
    return p.stdout
try:
    run('build',['lake','build',MOD])
    names=re.findall(r'^theorem\s+(\w+)',SOURCE.read_text(),re.M)
    report.update(named_theorems=len(names),theorems=names,source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    log=run('elaborate',['lake','env','lean',str(SOURCE.relative_to(ROOT))])
    matches=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log)
    empty=re.findall(r"'([^']+)' does not depend on any axioms",log)
    found={n for n,_ in matches}|set(empty)
    for n in names:
        if MOD+'.'+n not in found: raise RuntimeError('Missing audit: '+n)
    for n,axs in matches:
        if {x.strip() for x in axs.split(',') if x.strip()}-{'propext','Classical.choice','Quot.sound'}:
            raise RuntimeError('Unapproved axiom: '+n)
    run('recheck',['lake','env','leanchecker',MOD])
    controls={
      'false_gap_free_strict':'import OperatorFirst.OffsetEndpoint\nexample : (0:ℝ)^4 < ((1-1)^2+0^2)*((1+1)^2+0^2) := by norm_num\n',
      'false_monotonicity':'import OperatorFirst.OffsetEndpoint\nexample : OperatorFirst.OffsetEndpoint.nonmonotoneExample 1 ≤ OperatorFirst.OffsetEndpoint.nonmonotoneExample 2 := by norm_num [OperatorFirst.OffsetEndpoint.nonmonotoneExample]\n',
      'false_odd_sign':'import OperatorFirst.OffsetEndpoint\nexample : (fun v : ℝ => v) (-1) - (fun v : ℝ => v) 1 = 2*OperatorFirst.OffsetEndpoint.oddPart (fun v : ℝ => v) 1 := by norm_num [OperatorFirst.OffsetEndpoint.oddPart]\n',
    }
    for name,source in controls.items():
        p=OUT/(name+'.lean');p.write_text(source)
        run(name,['lake','env','lean',str(p.relative_to(ROOT))],True)
    report['status']='PASS'
except Exception as exc:
    report['status']='FAIL';report['error']=str(exc)
finally:
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
