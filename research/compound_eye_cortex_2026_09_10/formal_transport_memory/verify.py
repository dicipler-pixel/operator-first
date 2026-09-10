#!/usr/bin/env python3
"""Compile/audit the QG transport-memory Lean module with negative controls."""
import hashlib, json, pathlib, re, shutil, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
report={'status':'RUNNING','commands':[],'theorems':[]}
def run(name,args,negative=False):
    p=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
    (OUT/(name+'.log')).write_text(p.stdout)
    print(p.stdout,flush=True)
    report['commands'].append({'name':name,'args':args,'returncode':p.returncode})
    if negative:
        if p.returncode==0 or not re.search(r'proved that the proposition.*false|unsolved goals|tactic.*failed',p.stdout,re.S|re.I):
            raise RuntimeError('False control did not fail mathematically: '+name)
        if re.search(r'unknown (?:module|identifier|constant)|unexpected token',p.stdout,re.I):
            raise RuntimeError('False control failed for infrastructure/syntax reason: '+name)
    elif p.returncode:
        raise RuntimeError(name+' failed')
    return p.stdout
try:
    for f in ['lake-manifest.json','lean-toolchain']:
        if (ROOT/f).exists(): shutil.copyfile(ROOT/f,OUT/f)
    run('toolchain',['lake','env','lean','--version'])
    src=ROOT/'TransportMemory.lean'
    report['sha256']=hashlib.sha256(src.read_bytes()).hexdigest()
    report['theorems']=['QGTransportMemory.'+x for x in re.findall(r'^theorem\s+(\w+)',src.read_text(),re.M)]
    run('build',['lake','build','TransportMemory'])
    audit=OUT/'axioms.lean'
    audit.write_text('import TransportMemory\n'+'\n'.join('#print axioms '+x for x in report['theorems'])+'\n')
    log=run('axioms',['lake','env','lean',str(audit)])
    allowed={'propext','Classical.choice','Quot.sound'}
    for name in report['theorems']:
        m=re.search(re.escape("'"+name+"'")+r'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])',log,re.S)
        if not m: raise RuntimeError('Missing axiom audit: '+name)
        if m.group(2):
            got={x.strip() for x in m.group(2).split(',') if x.strip()}
            if got-allowed: raise RuntimeError('Forbidden axiom(s) for '+name+': '+repr(sorted(got-allowed)))
    run('leanchecker',['lake','env','leanchecker','TransportMemory'])
    false_controls={
      'false_fiber_memory':'example : QGTransportMemory.netFlow [(1:ℤ), -1] = 1 := by norm_num [QGTransportMemory.netFlow]',
      'false_exponent':'example : (1 + (2:ℝ)/2) - ((2:ℝ)/2) = 2 := by norm_num',
    }
    for name,text in false_controls.items():
        f=OUT/(name+'.lean'); f.write_text('import TransportMemory\n'+text+'\n')
        run(name,['lake','env','lean',str(f)],negative=True)
    report['named_theorems']=len(report['theorems'])
    report['status']='PASS'
except Exception as exc:
    report['status']='FAIL'; report['error']=str(exc)
finally:
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
