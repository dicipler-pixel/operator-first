#!/usr/bin/env python3
"""Transparent discriminator planner for Compound Eye Cortex 0.3 prototype.

Input actions declare, rather than predict, which live hypotheses would remain
possible under each outcome. The planner ranks experiments by worst-case
remaining hypotheses and pair separation per declared cost. It does not invent
outcome models or execute actions.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
import json

SCHEMA='compound-eye-discriminator-v1'

def frac(x):return F(str(x))
def pair_count(n):return n*(n-1)//2

def evaluate(plan):
    if plan.get('schema')!=SCHEMA:raise ValueError('Wrong planner schema')
    hs=[h['id'] for h in plan.get('hypotheses',[])]
    if len(hs)<2 or len(set(hs))!=len(hs):raise ValueError('Need at least two unique hypotheses')
    universe=set(hs);rows=[]
    for a in plan.get('actions',[]):
        cost=frac(a.get('cost',1))
        if cost<=0:raise ValueError('Action cost must be positive')
        outcomes=a.get('outcomes',{})
        if not outcomes:raise ValueError('Action needs declared outcome partitions')
        seen=[]
        for name,bucket in outcomes.items():
            if not bucket or len(set(bucket))!=len(bucket):raise ValueError('Outcome buckets must be nonempty unique lists')
            if not set(bucket)<=universe:raise ValueError('Unknown hypothesis in outcome '+name)
            seen.extend(bucket)
        if len(seen)!=len(set(seen)) or set(seen)!=universe:raise ValueError('Each hypothesis must occur in exactly one outcome bucket')
        sizes=sorted((len(x) for x in outcomes.values()),reverse=True)
        total_pairs=pair_count(len(hs));unseparated=sum(pair_count(n) for n in sizes);separated=total_pairs-unseparated
        expected_num=sum(n*n for n in sizes);expected_den=len(hs)
        rows.append({'id':a['id'],'cost':str(cost),'outcome_count':len(sizes),'worst_case_remaining':sizes[0],
                     'expected_remaining_uniform':str(F(expected_num,expected_den)),
                     'separated_hypothesis_pairs':separated,'total_pairs':total_pairs,
                     'pair_separation_per_cost':str(F(separated,1)/cost),
                     'changes_object':bool(a.get('changes_object',False)),
                     'acceptance':a.get('acceptance',[]),'inputs':a.get('inputs',[]),'notes':a.get('notes','')})
    if not rows:raise ValueError('No actions')
    rows.sort(key=lambda r:(r['worst_case_remaining'],-float(F(r['pair_separation_per_cost'])),float(F(r['cost'])),r['id']))
    return {'hypotheses':hs,'ranked_actions':rows,'recommended':rows[0]['id'],
            'ranking_rule':'minimize worst-case survivors, then maximize separated hypothesis pairs per declared cost, then lower cost',
            'scope':'Decision aid under user-declared outcome partitions; not a probability model or autonomous experiment executor.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('plan');a=p.parse_args();print(json.dumps(evaluate(json.load(open(a.plan))),indent=2))
