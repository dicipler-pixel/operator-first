#!/usr/bin/env python3
"""No green result from comments or source scans: build and recheck every module."""
from pathlib import Path
import hashlib,json,re,subprocess,sys,shutil
root=Path(__file__).resolve().parents[1]
out=root/'verification'/'mixed-review';out.mkdir(parents=True,exist_ok=True)
lib=root/'.lake'/'build'/'lib'/'lean'/'MixedIntake';lib.mkdir(parents=True,exist_ok=True)
allowed={'propext','Classical.choice','Quot.sound'}
report={'status':'RUNNING','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'checks':{},'sources':{},'allowed_axioms':sorted(allowed)}

def run(name,args,negative=False):
 r=subprocess.run(args,cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
 (out/(name+'.log')).write_text(r.stdout,encoding='utf-8')
 print('===',name,'exit',r.returncode,'===\n'+r.stdout,flush=True)
 report['checks'][name]={'argv':args,'exit_code':r.returncode,'negative_control':negative}
 if not negative:
  if r.returncode!=0:raise RuntimeError(name+' failed')
  if 'sorryAx' in r.stdout or "declaration uses 'sorry'" in r.stdout:raise RuntimeError(name+' has unfinished dependency')
 else:
  if r.returncode==0:raise RuntimeError(name+' accepted a false control')
  if re.search(r'unknown (?:constant|identifier|module)|unexpected token|not found',r.stdout,re.I):raise RuntimeError(name+' failed for infrastructure/syntax')
  if not re.search(r'unsolved goals|is false',r.stdout):raise RuntimeError(name+' did not yield a mathematical rejection')
 return r.stdout
try:
 audit=['import MixedIntake.FCS_original','import MixedIntake.AK_original','import MixedIntake.Review']
 all_names=[]
 for stem,namespace in [('FCS_original','FCS'),('AK_original','AK'),('Review','MixedReview')]:
  source=root/'MixedIntake'/(stem+'.lean');text=source.read_text()
  names=re.findall(r'^theorem\s+([A-Za-z_0-9]+)',text,re.M)
  names=[namespace+'.'+x for x in names];all_names+=names
  report['sources'][str(source.relative_to(root))]={'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'named_theorems':names}
  (out/'sources'/'MixedIntake').mkdir(parents=True,exist_ok=True)
  shutil.copy2(source,out/'sources'/'MixedIntake'/source.name)
  run(stem+'_build',['lake','env','lean','-o',str((lib/(stem+'.olean')).relative_to(root)),str(source.relative_to(root))])
  run(stem+'_kernel',['lake','env','leanchecker','MixedIntake.'+stem])
  audit += ['#print axioms '+x for x in names]
 audit_path=out/'Audit.lean';audit_path.write_text('\n'.join(audit)+'\n')
 text=run('axiom_audit',['lake','env','lean',str(audit_path.relative_to(root))])
 found=dict(re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text))
 for name in re.findall(r"'([^']+)' does not depend on any axioms",text):found[name]=''
 for name in all_names:
  if name not in found:raise RuntimeError('missing dependency report '+name)
  used={x.strip() for x in found[name].split(',') if x.strip()}
  if used-allowed:raise RuntimeError('unapproved axioms '+name+': '+str(used))
 report['named_theorems']=len(all_names)
 controls={'false_arithmetic':'import Mathlib\nexample : (1:Nat)=2 := by decide\n',
 'false_strict_threshold':'import Mathlib\nexample : 3*72 ≤ 5*43 := by decide\n',
 'false_nonzero_phase_ban':'import MixedIntake.Review\nexample : MixedReview.phaseDefect (0:ZMod 3) 0 1 0 1 2 ≠ 0 := by decide\n'}
 for name,text in controls.items():
  p=out/(name+'.lean');p.write_text(text)
  run(name,['lake','env','lean',str(p.relative_to(root))],True)
 report['status']='PASS'
except Exception as e:
 report['status']='FAIL';report['error']=str(e)
finally:
 report['toolchain']=(root/'lean-toolchain').read_text().strip()
 shutil.copy2(__file__,out/'verify_mixed.py')
 (out/'verification_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report,indent=2),flush=True)
sys.exit(report['status']!='PASS')
