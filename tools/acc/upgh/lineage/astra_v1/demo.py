#!/usr/bin/env python3
"""Exercise the complete controller with labelled toy workers and checker."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time
try:
    from .harness import ROOT,Harness,atomic_json,read_json
    from .gates import sha256_file
except ImportError:
    from harness import ROOT,Harness,atomic_json,read_json
    from gates import sha256_file

def prepare_demo(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    for name in ('demo_worker.py','demo_checker.py'):
        shutil.copyfile(ROOT/'workers'/name,root/name)
    config=read_json(ROOT/'config.json');config['demo']=True
    for role in config['roles'].values():
        role['command']=[sys.executable,str(root/'demo_worker.py')]
    ruleset='d'*64
    atomic_json(root/'targets.json',{'ruleset_sha256':ruleset,
                'targets':[{'row_id':'DEMO-ONLY','track':'AC','start':['ab','b'],'goal':['a','b']}]})
    atomic_json(root/'board.json',{'observed_at':time.time(),'ruleset_sha256':ruleset,
                'rows':[{'row_id':'DEMO-ONLY','track':'AC','record':1,'held_by_us':False}]})
    config.update(target_manifest='targets.json',target_manifest_sha256=sha256_file(root/'targets.json'),board_snapshot='board.json')
    config['checker']={'path':'demo_checker.py','sha256':sha256_file(root/'demo_checker.py'),
                       'command':[sys.executable,'demo_checker.py','{candidate}','{receipt}'],'timeout_seconds':3}
    atomic_json(root/'config.json',config)
    return {'objective':'DEMO controller recovery, not a real ACC search','row_id':'DEMO-ONLY',
            'ruleset_sha256':ruleset,'strategy':{'seed':'toy','route_family':'toy-initial','probe':'toy-endpoint',
            'representation':'toy-words','cost_model':'toy-unit','board_filter':'toy-unheld'}}

def main():
    root=Path(tempfile.mkdtemp(prefix='acc-harness-demo-'))
    work=prepare_demo(root);h=Harness(root/'config.json',root/'state');h.add(work)
    status=h.run()
    outputs=list((root/'state'/'demo_results').glob('*.json'))
    passed=len(outputs)==1 and read_json(outputs[0])['gate']['status']=='verified_scoring'
    report={'test':'complete-controller-toy-demonstration','passed':passed,'language_models_called':False,
            'real_ACC_checker_used':False,'real_candidates_produced':False,'status':status,'directory':str(root),
            'sequence':[t['role'] for t in h.store.tasks()]}
    atomic_json(root/'demo_report.json',report)
    print(json.dumps(report,indent=2));return 0 if passed else 1

if __name__=='__main__': raise SystemExit(main())
