#!/usr/bin/env python3
"""Independently certify every rejection in the 11480-case fixed-ladder search."""
from copy import deepcopy
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time
from exact_ak import build,certify,rank2
from check_ak_certificate import check

ROOT=Path(__file__).resolve().parent


def run():
    start=time.perf_counter()
    search=json.loads((ROOT/'fixed_ladder_search.json').read_text())
    trace=json.loads((ROOT/'fixed_ladder_search_trace.json').read_text())
    assert hashlib.sha256(json.dumps(trace,separators=(',',':')).encode()).hexdigest()==search['trace_sha256']
    base=search['fixed_problem_without_generators'];V,_,edges=build(base)
    options=[(v,tuple(label)) for v in range(len(V)) for label in search['dilate_pool']]
    assert len(trace)==11480 and [tuple(r[:3]) for r in trace]==list(combinations(range(42),3))
    cut_count=certificate_count=steps=duals=0
    path=ROOT/'fixed_ladder_certificates.jsonl.gz'
    with gzip.open(path,'wt',encoding='utf-8') as output:
        for row in trace:
            gens=[options[j] for j in row[:3]]
            if row[3]=='cut':
                mask=row[4]
                assert type(mask) is int and 1<=mask<64
                labels=[label for v,label in gens if mask>>v&1]
                labels += [label for a,b,label in edges if bool(mask>>a&1)!=bool(mask>>b&1)]
                assert rank2(labels)<2
                cut_count+=1
            else:
                p=deepcopy(base)
                p['generators']=[{'vertex':list(V[v]),'label':list(label)} for v,label in gens]
                c=certify(p,include_cuts=False)
                result=check(c)
                assert not result['forcing_complete']
                assert c['forced_vertices']==[list(V[v]) for v in row[4]]
                output.write(json.dumps({'combination':row[:3],'certificate':c},separators=(',',':'))+'\n')
                certificate_count+=1;steps+=len(c['steps']);duals+=len(c['stalled_dual_certificates'])
                if certificate_count%500==0:print(f'Independent integer certificates checked: {certificate_count}/4120',flush=True)
    report={'all_passed':True,'enumeration_completeness_checked':True,'cases':len(trace),
            'cut_obstructions_checked':cut_count,'independent_forcing_certificates_checked':certificate_count,
            'integer_forcing_steps_checked':steps,'integer_stall_identities_checked':duals,
            'certificate_log':path.name,'certificate_log_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'seconds':time.perf_counter()-start,'scope':search['scope'],
            'result':'No complete forcing pair in this exact fixed-label cell; no conclusion for other labellings.'}
    (ROOT/'fixed_ladder_certificate_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    return report


if __name__=='__main__':run()
