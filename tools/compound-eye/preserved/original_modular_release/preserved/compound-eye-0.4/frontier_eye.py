#!/usr/bin/env python3
"""Compound Eye 0.4: exact finite mathematical-target interface.

Use ak to produce a certificate, check-ak to verify one, or earth to screen
a proposed graph. The original compound_lab.py retains its numerical model API.
"""
import argparse
import json
import gzip
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent/'frontier'))
sys.path.insert(0,str(Path(__file__).resolve().parent/'dag_search'))
from exact_ak import certify
from check_ak_certificate import check
from earth_moon import screen


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['ak','check-ak','earth','search-ak','check-dag','check-earth-family'])
    p.add_argument('input',help='JSON path or - for standard input')
    p.add_argument('--output',help='Write the complete JSON result to this file.')
    a=p.parse_args()
    try:
        if a.input=='-':
            data=json.load(sys.stdin)
        else:
            path=Path(a.input)
            data=json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes())
        if a.command=='search-ak':
            from decision_dag import Context,DecisionDAG
            from check_dag import check as check_dag
            dag=DecisionDAG(Context(data['problem'],data['pool']),data['generator_budget'],learning=data.get('learning',True))
            dag.run()
            for node in dag.nodes:
                if node['kind']=='complete':
                    node['positive_certificate']=certify(dag.ctx.candidate(node['representative']),include_cuts=False)
            result=dag.artifact()
            result['independent_audit']=check_dag(result)
        elif a.command=='check-dag':
            from check_dag import check as check_dag
            result=check_dag(data)
        elif a.command=='check-earth-family':
            from earth_families import check as check_family
            result=check_family(data)
        else:
            result={'ak':certify,'check-ak':check,'earth':screen}[a.command](data)
        if a.output:
            Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
            print(json.dumps({'status':'written','output':a.output}))
        else:
            print(json.dumps(result,indent=2))
        return 0
    except (ValueError,TypeError,KeyError,IndexError,AttributeError,OSError) as exc:
        print(json.dumps({'status':'invalid_input_or_certificate','error':str(exc)}))
        return 2


if __name__=='__main__':raise SystemExit(main())
