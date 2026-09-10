#!/usr/bin/env python3
"""Evidence-lineage diagnostics for Compound Eye Cortex 0.2.

A shared source *file* is not automatically shared evidence: the baseline uses
large adapter modules. We therefore distinguish module identity from executable
entry-point identity (content hash + function + adapter) and from dependency
lineage. This module never converts either relation into a statistical
independence claim.
"""
from __future__ import annotations
from collections import defaultdict
from pathlib import Path
import json, sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
INSTRUMENT=REPO/'tools'/'compound-eye'
sys.path.insert(0,str(INSTRUMENT))
import machine


def module_key(spec):
    impl=spec.get('implementation') or {}
    if not impl:return None
    return (impl.get('sha256'),impl.get('path'))


def entrypoint_key(spec):
    impl=spec.get('implementation') or {}
    if not impl:return None
    return (impl.get('sha256'),impl.get('function'),spec.get('adapter'))


def ancestors(reg,ref,memo=None):
    memo={} if memo is None else memo
    if ref in memo:return memo[ref]
    out={ref}
    for d in reg.eyes[ref].get('depends_on',[]):out|=ancestors(reg,d,memo)
    memo[ref]=out
    return out


def audit_run(run,root=INSTRUMENT,threshold=0.5):
    if run.get('schema')!='compound-eye-run-v1':raise ValueError('Expected compound-eye-run-v1')
    reg=machine.Registry(root);refs=[x['eye'] for x in run['results'] if x['eye'] in reg.eyes];memo={};rows=[]
    for i,a in enumerate(refs):
        A=reg.eyes[a];aa=ancestors(reg,a,memo)
        for b in refs[i+1:]:
            B=reg.eyes[b];bb=ancestors(reg,b,memo);inter=aa&bb;union=aa|bb;j=len(inter)/len(union) if union else 0.0
            same_module=bool(module_key(A) and module_key(A)==module_key(B))
            same_entry=bool(entrypoint_key(A) and entrypoint_key(A)==entrypoint_key(B))
            if same_entry or j>=threshold:
                rows.append({'a':a,'b':b,'same_module':same_module,'same_entrypoint':same_entry,
                             'dependency_jaccard':j,'shared_dependency_nodes':sorted(inter),
                             'warning':'This is shared computational lineage, not a numerical estimate of evidence correlation.'})
    rows.sort(key=lambda x:(-int(x['same_entrypoint']),-x['dependency_jaccard'],x['a'],x['b']))
    return {'pairs':rows,'threshold':threshold,'scope':'Module reuse alone is not treated as duplicate evidence.'}


def catalog_groups(root=INSTRUMENT):
    reg=machine.Registry(root);modules=defaultdict(list);entries=defaultdict(list)
    for ref,s in reg.eyes.items():
        if module_key(s):modules[module_key(s)].append(ref)
        if entrypoint_key(s):entries[entrypoint_key(s)].append(ref)
    def rows(d):
        return sorted(({'key':list(k),'count':len(v),'refs':sorted(v)} for k,v in d.items() if len(v)>1),
                      key=lambda x:(-x['count'],x['key']))
    return {'eyes':len(reg.eyes),'shared_modules':rows(modules),'shared_entrypoints':rows(entries),
            'scope':'Shared module is code packaging. Shared entrypoint is stronger lineage, but still not proof of identical mathematical evidence.'}

if __name__=='__main__':print(json.dumps(catalog_groups(),indent=2))
