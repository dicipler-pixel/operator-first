#!/usr/bin/env python3
"""Compile, recheck and audit every extension theorem; retain failing evidence."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'verification'/'extension'
OUT.mkdir(parents=True,exist_ok=True)
MODULES = ['OperatorFirst.RestrictionBridge','OperatorFirst.KakeyaExtension',
           'OperatorFirst.EarthMoon','OperatorFirst.FCSMoments',
           'OperatorFirst.KakeyaSeedingControl','OperatorFirst.KakeyaCut',
           'OperatorFirst.KakeyaForcingLinear','OperatorFirst.KakeyaAtlasFamily',
           'OperatorFirst.KakeyaAtlasProjector']
report = {'status':'RUNNING','checks':{},'sources':{},'named_theorems':0,
          'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}

def run(name,args,negative=False):
    p=subprocess.run(args,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                     text=True,timeout=360)
    (OUT/(name+'.log')).write_text(p.stdout)
    print(name,p.returncode,p.stdout,flush=True)
    report['checks'][name]={'exit_code':p.returncode,'argv':args,'expected_failure':negative}
    if negative:
        if p.returncode==0 or not re.search(r'proved that the proposition.*false|unsolved goals',p.stdout,re.S):
            raise RuntimeError('negative control not mathematically rejected: '+name)
        if re.search(r'unknown (?:module|identifier|constant)|unexpected token',p.stdout):
            raise RuntimeError('negative control infrastructure failure: '+name)
    elif p.returncode!=0:
        raise RuntimeError(name+' failed')
    return p.stdout

try:
    run('build',['lake','build',*MODULES])
    for mod in MODULES:
        path=ROOT/(mod.replace('.','/')+'.lean')
        source=path.read_text()
        names=re.findall(r'^theorem\s+(\w+)',source,re.M)
        report['sources'][mod]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'theorems':names}
        report['named_theorems']+=len(names)
        log=run(mod+'_elaborate',['lake','env','lean',str(path.relative_to(ROOT))])
        matches=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",log)
        empty=re.findall(r"'([^']+)' does not depend on any axioms",log)
        found={n for n,_ in matches}|set(empty)
        namespace='EarthMoon' if mod.endswith('.EarthMoon') else mod
        for name in names:
            if namespace+'.'+name not in found:
                raise RuntimeError('missing axiom audit for '+name)
        for name,axs in matches:
            if {a.strip() for a in axs.split(',') if a.strip()}-{'propext','Classical.choice','Quot.sound'}:
                raise RuntimeError('unapproved axiom in '+name)
        run(mod+'_recheck',['lake','env','leanchecker',mod])
    negatives={
        'false_family_q_one':'import OperatorFirst.KakeyaAtlasFamily\nexample : OperatorFirst.KakeyaAtlasFamily.Complete 1 := by rw [OperatorFirst.KakeyaAtlasFamily.completion_iff_q_two]; norm_num\n',
        'false_projector_value':'import OperatorFirst.KakeyaAtlasProjector\nexample : OperatorFirst.KakeyaAtlasProjector.dot OperatorFirst.KakeyaAtlasProjector.targetVector (OperatorFirst.KakeyaAtlasProjector.project OperatorFirst.KakeyaAtlasProjector.targetVector) = 0 := by norm_num [OperatorFirst.KakeyaAtlasProjector.projector_target_value]\n',
        'false_no_seed_witness':'import OperatorFirst.KakeyaSeedingControl\nexample : ¬ OperatorFirst.KakeyaSeedingControl.Step OperatorFirst.KakeyaSeedingControl.coeff₁ ∅ 2 := by decide\n',
        'false_join_count':'import OperatorFirst.EarthMoon\nset_option maxRecDepth 100000\nset_option maxHeartbeats 2000000\nexample : EarthMoon.joinEdges.length = 104 := by decide\n',
        'false_granularity':'import Mathlib\nexample : (3 : Nat)*72 ≤ 5*43 := by decide\n',
        'false_endpoint_symmetry':'import OperatorFirst.FCSMoments\nexample : OperatorFirst.FCSMoments.law (1/24) 0 = OperatorFirst.FCSMoments.law (1/24) 3 := by norm_num [OperatorFirst.FCSMoments.law]\n',
    }
    for name,source in negatives.items():
        p=OUT/(name+'.lean');p.write_text(source)
        run(name,['lake','env','lean',str(p.relative_to(ROOT))],True)
    report['status']='PASS'
except Exception as exc:
    report['status']='FAIL';report['error']=str(exc)
finally:
    (OUT/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)
sys.exit(0 if report['status']=='PASS' else 1)
