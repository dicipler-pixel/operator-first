#!/usr/bin/env python3
"""Run the real Lean build and dependency audit; fail closed when unavailable.

Usage: python verify.py [--math] [--setup]
--math also runs the independent numpy/scipy/sympy model checks.
--setup permits Lake to fetch pinned Mathlib and its precompiled cache.
A successful mathematical script never substitutes for a Lean build.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LEAN=ROOT/'lean'; CHECKS=ROOT/'checks';CHECKS.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--math',action='store_true');parser.add_argument('--setup',action='store_true')
args=parser.parse_args()
report={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'kernel_verified':False,'certified_declarations':0,'state':'NOT_RUN','steps':[],
        'scope':'Only the exact Lean theorem statements; not validation of material or gravity hypotheses.'}
log=[]

def finish(code):
    (CHECKS/'lean_status.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (CHECKS/'lean_checks.log').write_text('\n'.join(log)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));raise SystemExit(code)

def run(cmd,cwd=LEAN,timeout=600):
    log.append('$ '+' '.join(map(str,cmd)))
    try:
        p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout)
        text=p.stdout+'\n'+p.stderr;log.append(text)
        report['steps'].append({'command':cmd,'returncode':p.returncode})
        return p.returncode,text
    except (OSError,subprocess.TimeoutExpired) as exc:
        log.append(repr(exc));report['steps'].append({'command':cmd,'error':repr(exc)})
        return None,repr(exc)

if args.math:
    code,text=run([sys.executable,str(CHECKS/'run_tests.py')],cwd=ROOT,timeout=240)
    report['independent_model_checks_passed']=code==0
    if code!=0:report['state']='MATHEMATICAL_CHECK_FAILURE';finish(1)

files=list((LEAN/'Hypersurface').glob('*.lean'))+[LEAN/'Hypersurface.lean',LEAN/'Audit.lean']
report['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
for p in files:
    text=p.read_text()
    if re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s|skipKernelTC|trustCompiler',text,re.M):
        report['state']='FORBIDDEN_SOURCE_CONSTRUCT';report['file']=str(p);finish(1)
report['static_scan']='NO_PLACEHOLDERS_FOUND (NOT A TYPECHECK)'

lake=shutil.which('lake')
if lake is None:
    # Real invocation produces the missing-executable record, not a forged compiler log.
    run(['lake','--version'],timeout=10)
    report['state']='BLOCKED_NO_LAKE';finish(2)
code,text=run([lake,'env','lean','--version'],timeout=30)
if code!=0:report['state']='BLOCKED_TOOLCHAIN';finish(2)
report['compiler_version']=text.strip()
if args.setup:
    for command in [[lake,'update'],[lake,'exe','cache','get']]:
        code,text=run(command,timeout=900)
        if code!=0:report['state']='DEPENDENCY_SETUP_FAILED';finish(2)
code,text=run([lake,'build'])
if code!=0:report['state']='COMPILATION_FAILED';finish(1)
code,text=run([lake,'env','lean','Audit.lean'])
if code!=0:report['state']='AXIOM_AUDIT_FAILED';finish(1)
expected=json.loads((LEAN/'theorems.json').read_text())
allowed={'propext','Classical.choice','Quot.sound'};axioms={}
for name in expected:
    match=re.search(r"'?"+re.escape(name)+r"'?\s+depends on axioms:\s*\[([^\]]*)\]",text)
    if match:
        deps={x.strip() for x in match[1].split(',') if x.strip()}
    elif re.search(r"'?"+re.escape(name)+r"'?\s+does not depend on any axioms",text):deps=set()
    else:report['state']='INCOMPLETE_AXIOM_OUTPUT';report['missing']=name;finish(1)
    axioms[name]=sorted(deps)
    if not deps<=allowed:
        report['state']='UNAPPROVED_AXIOM';report['theorem']=name;report['dependencies']=sorted(deps);finish(1)
report['axioms']=axioms
for filename in ['FalseHall.lean','FalseExterior.lean']:
    code,output=run([lake,'env','lean',str(Path('negative')/filename)])
    infrastructure=any(s in output for s in ['unknown module','unknown identifier','failed to synthesize','file does not exist','unexpected token'])
    if code is None or code==0 or infrastructure or 'unsolved goals' not in output:
        report['state']='NEGATIVE_CONTROL_NOT_VALIDATED';report['negative_file']=filename;finish(1)
report['state']='BUILD_AND_AXIOM_AUDIT_PASSED'
report['kernel_verified']=True;report['certified_declarations']=len(expected)
finish(0)
