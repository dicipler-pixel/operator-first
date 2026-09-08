#!/usr/bin/env python3
"""Exhaust all 3-generator sets for one explicitly fixed six-vertex labelling.

The primitive height-two pool has 42 vertex-label choices and C(42,3)=11480
distinct generator sets. No same-vertex seeding restriction is applied.
Sound subset-rank obstructions may reject candidates; every other candidate is
checked by the supplied exact-existence engine. Any hit requires an independent
integer certificate before it can be called a target candidate.
"""
from pathlib import Path
from itertools import combinations
from copy import deepcopy
import hashlib
import json
import math
import time
from exact_ak import controls,build,rank2,certify
from check_ak_certificate import check

ROOT=Path(__file__).resolve().parent


def legacy_engine():
    text=(ROOT/'originals'/'AK-VERIFIER-02(1).py').read_text()
    namespace={}
    exec(compile(text.split('print("CONTROL 1')[0], 'supplied_exact_existence_engine', 'exec'),namespace)
    return namespace


def run():
    start=time.perf_counter()
    D=[(a,b) for a in range(-2,3) for b in range(-2,3) if a+b>=1 and math.gcd(abs(a),abs(b))==1]
    assert len(D)==7
    p=controls()['kt_11_6'];p['X']=[[0,0]]+[list(x) for x in D]
    p['generators']=[]
    V,_,edges=build(p);n=len(V)
    options=[(v,label) for v in range(n) for label in D]
    cuts=[]
    for mask in range(1,1<<n):
        labs=[lab for a,b,lab in edges if bool(mask>>a&1)!=bool(mask>>b&1)]
        if rank2(labs)<2:cuts.append((mask,labs))
    klass=legacy_engine()['AK']
    fs=[{tuple(x['prefix']):tuple(x['label']) for x in level} for level in p['levels']]
    counts={'enumerated':0,'cut_rejected':0,'forcing_engine_calls':0,'complete':0,
            'three_distinct_generator_vertices':0,'seed_restricted_unique_sets':0}
    hits=[];trace=[]
    for combo in combinations(range(len(options)),3):
        gens=[options[j] for j in combo]
        counts['enumerated']+=1
        if len({v for v,x in gens})==3:counts['three_distinct_generator_vertices']+=1
        else:counts['seed_restricted_unique_sets']+=1
        bad=None
        for mask,labs in cuts:
            if rank2(labs+[label for v,label in gens if mask>>v&1])<2:bad=mask;break
        if bad is not None:
            counts['cut_rejected']+=1
            trace.append([*combo,'cut',bad]);continue
        counts['forcing_engine_calls']+=1
        old=klass([(0,0)]+D,p['dims'],fs,[],[{V[v]:label} for v,label in gens])
        forced=old.run()
        trace.append([*combo,'forced',sorted(V.index(v) for v in forced)])
        if len(forced)==n:
            candidate=deepcopy(p)
            candidate['generators']=[{'vertex':list(V[v]),'label':list(label)} for v,label in gens]
            c=certify(candidate);assert check(c)['target_conditions_met']
            hits.append(c);counts['complete']+=1
    assert counts['enumerated']==math.comb(42,3)==11480
    assert counts['three_distinct_generator_vertices']==6860
    raw=json.dumps(trace,separators=(',',':')).encode()
    report={'status':'exhausted_fixed_label_cell','counts':counts,'seconds':time.perf_counter()-start,
            'fixed_problem_without_generators':p,'dilate_pool':[list(x) for x in D],
            'generator_budget':3,'trace_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Only the supplied Katz-Tao figure-2 edge labelling at dims (2,3), T empty, and this seven-direction pool. Other rail labellings and the other orientation are not exhausted.',
            'seeding_prune_used':False,'official_epoch_verifier_run':False,
            'empty_result_evidence':'Full finite enumeration with sound subset cuts and supplied exact-existence forcing engine. Run certify_search_log.py for independent integer certificates of every remaining case; the delivered audit and compressed proof log are included separately.',
            'verified_hits':hits}
    (ROOT/'fixed_ladder_search_trace.json').write_bytes(raw+b'\n')
    (ROOT/'fixed_ladder_search.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['fixed_problem_without_generators','verified_hits']},indent=2),flush=True)
    return report


if __name__=='__main__':run()
