#!/usr/bin/env python3
"""Compile each light module, audit each theorem, recheck with leanchecker."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification/gravity';OUT.mkdir(parents=True,exist_ok=True)
modules=['Gravity']
report={'status':'RUNNING','modules':{},'controls':{}}
def run(name,args,negative=False):
 p=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=600)
 (OUT/(name+'.log')).write_text(p.stdout)
 print(name, p.returncode, p.stdout,flush=True)
 if negative:
  if p.returncode==0 or not re.search(r'proved that the proposition.*false|unsolved goals',p.stdout,re.S):raise RuntimeError('Control did not reject mathematically: '+name)
  if re.search(r'unknown (?:module|identifier|constant)|unexpected token',p.stdout):raise RuntimeError('Control infrastructure error')
 elif p.returncode:raise RuntimeError(name+' failed')
 return p.stdout
try:
 run('all_build',['lake','build','Gravity'])
 for mod in modules:
  src=ROOT/(mod.replace('.','/')+'.lean')
  names=re.findall(r'^theorem\s+(\w+)',src.read_text(),re.M)
  ns='Gravity'
  qualified=[ns+'.'+x for x in names]
  report['modules'][mod]={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'theorems':qualified}
  run(mod+'_build',['lake','build',mod])
  audit=OUT/(mod+'_audit.lean');audit.write_text('import '+mod+'\n'+'\n'.join('#print axioms '+n for n in qualified)+'\n')
  out=run(mod+'_axioms',['lake','env','lean',str(audit.relative_to(ROOT))])
  for n in qualified:
   m=re.search(re.escape("'"+n+"'")+r'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])',out,re.S)
   if not m:raise RuntimeError('Missing audit '+n)
   if m.group(2) and set(x.strip() for x in m.group(2).split(','))-{'propext','Classical.choice','Quot.sound'}:raise RuntimeError('Forbidden axioms '+n)
  run(mod+'_recheck',['lake','env','leanchecker',mod])
 controls={
 'false_reciprocal_positive': 'import Gravity\nexample : (1:ℝ)^2*(-1)-0 > 0 := by norm_num\n',
 'false_point_positivity': 'import Gravity\nexample : (0:ℝ) ≤ -1 := by norm_num\n',
 'false_cap': 'import Gravity\nexample : (1:ℝ)-(-1)*1^2+0 ≤ 1 := by norm_num\n',
 'false_moving_signature': 'import Gravity\nexample : (0:ℝ) ≤ -2*(1/10) := by norm_num\n'}
 for name,src in controls.items():
  f=OUT/(name+'.lean');f.write_text(src)
  run(name,['lake','env','lean',str(f.relative_to(ROOT))],True)
  report['controls'][name]='MATHEMATICALLY_REJECTED'
 report['status']='PASS'
except Exception as e:report['status']='FAIL';report['error']=str(e)
finally:
 report['named_theorems']=sum(len(v['theorems']) for v in report['modules'].values())
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
