#!/usr/bin/env python3
"""Compile and axiom-audit the overlap bridge, with an independent kernel recheck."""
import hashlib, json, pathlib, re, subprocess, sys, shutil
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / 'evidence'
OUT.mkdir(exist_ok=True)
report = {'status': 'RUNNING', 'commands': [], 'theorems': []}
def run(name, args, negative=False):
    p = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=900)
    (OUT / (name+'.log')).write_text(p.stdout)
    print(p.stdout, flush=True)
    report['commands'].append({'name':name, 'args':args, 'returncode':p.returncode})
    if negative:
        if p.returncode == 0 or not re.search(r'proved that the proposition.*false|unsolved goals', p.stdout, re.S):
            raise RuntimeError('False control did not fail mathematically')
        if re.search(r'unknown (?:module|identifier|constant)|unexpected token', p.stdout):
            raise RuntimeError('False control failed for an infrastructure reason')
    elif p.returncode:
        raise RuntimeError(name+' failed')
    return p.stdout
try:
    for filename in ['lake-manifest.json', 'lean-toolchain']:
        shutil.copyfile(ROOT/filename, OUT/filename)
    run('toolchain',['lake','env','lean','--version'])
    run('examples',[sys.executable,'check_examples.py'])
    source = ROOT / 'GravityOverlap.lean'
    report['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    report['theorems'] = ['GravityOverlap.'+x for x in re.findall(r'^theorem\s+(\w+)',source.read_text(),re.M)]
    run('build',['lake','build','GravityOverlap'])
    audit=OUT/'axioms.lean'
    audit.write_text('import GravityOverlap\n'+'\n'.join('#print axioms '+n for n in report['theorems'])+'\n')
    log=run('axioms',['lake','env','lean',str(audit)])
    for name in report['theorems']:
        m=re.search(re.escape("'"+name+"'")+r'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])', log,re.S)
        if not m: raise RuntimeError('Missing audit: '+name)
        if m.group(2) and set(x.strip() for x in m.group(2).split(','))-{'propext','Classical.choice','Quot.sound'}:
            raise RuntimeError('Forbidden axiom: '+name)
    run('leanchecker',['lake','env','leanchecker','GravityOverlap'])
    for name, text in {
        'wrong_quadratic_sign':'example : (0:ℝ) ≤ -1 := by norm_num',
        'false_null_cap':'example : (1:ℝ)+(1/10)^4/(1-(1/10)^4) ≤ 1 := by norm_num',
    }.items():
        f=OUT/(name+'.lean'); f.write_text('import GravityOverlap\n'+text+'\n')
        run(name,['lake','env','lean',str(f)],negative=True)
    report['status']='PASS'
except Exception as e:
    report['status']='FAIL'; report['error']=str(e)
finally:
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
