#!/usr/bin/env python3
"""Correction and obstruction memory for Compound Eye Cortex 0.4 prototype.

This module is deliberately explicit rather than NLP-magical. Claim identities,
versions, supersession links and obstruction assumptions are supplied as data.
It then detects stale references and decides whether a stored obstruction is
still licensed in the current context.
"""
from __future__ import annotations
from collections import defaultdict
import json,re

VER=re.compile(r'^[A-Za-z0-9_.-]+@\d+\.\d+\.\d+$')

def correction_audit(records, source_references=()):
    """Audit versioned claim records and explicit source references.

    records require ref, claim_id, value_hash, status and supersedes[].
    A claim may have multiple non-superseding active variants; they are surfaced
    as parallel records, not automatically called contradictions.
    """
    table={};byclaim=defaultdict(list)
    for r in records:
        for k in ('ref','claim_id','value_hash','status','supersedes'):
            if k not in r:raise ValueError('Correction record missing '+k)
        if not VER.fullmatch(r['ref']) or not isinstance(r['supersedes'],list):raise ValueError('Malformed correction record')
        if r['ref'] in table:raise ValueError('Duplicate correction ref')
        table[r['ref']]=r;byclaim[r['claim_id']].append(r)
    superseded_by=defaultdict(list)
    for r in records:
        for old in r['supersedes']:
            if old not in table:raise ValueError('Unknown superseded ref '+old)
            if table[old]['claim_id']!=r['claim_id']:raise ValueError('Cannot supersede a different claim_id')
            superseded_by[old].append(r['ref'])
    stale=[]
    for s in source_references:
        if not {'source','claim_ref'}<=set(s):raise ValueError('Malformed source reference')
        if s['claim_ref'] not in table:raise ValueError('Source references unknown claim')
        if superseded_by.get(s['claim_ref']):
            stale.append({'source':s['source'],'old_ref':s['claim_ref'],'superseded_by':sorted(superseded_by[s['claim_ref']])})
    parallel=[]
    for cid,rows in byclaim.items():
        live=[r for r in rows if not superseded_by.get(r['ref']) and r['status'] not in ('withdrawn','superseded')]
        values=defaultdict(list)
        for r in live:values[r['value_hash']].append(r['ref'])
        if len(values)>1:
            parallel.append({'claim_id':cid,'live_variants':sorted(r['ref'] for r in live),
                             'distinct_value_hashes':len(values),
                             'warning':'Different live records require reconciliation or an explicit scope distinction; difference alone is not proof of contradiction.'})
    return {'records':len(records),'claims':len(byclaim),'stale_source_references':stale,'parallel_live_variants':parallel,
            'scope':'Explicit correction/supersession audit. It does not infer semantic equivalence of unrelated prose.'}

def obstruction_applicability(obstruction, context):
    """Three-valued assumption/domain check for a stored exclusion or obstruction.

    required_facts is an exact key->value map. A mismatching known fact makes the
    obstruction inapplicable; a missing fact makes applicability UNKNOWN.
    """
    for k in ('id','required_facts','excluded_domain','certificate_ref'):
        if k not in obstruction:raise ValueError('Obstruction missing '+k)
    if not isinstance(obstruction['required_facts'],dict) or not isinstance(obstruction['excluded_domain'],dict):raise ValueError('Facts/domain must be dictionaries')
    checks=[];unknown=[];mismatch=[]
    required={**obstruction['excluded_domain'],**obstruction['required_facts']}
    for k,wanted in required.items():
        if k not in context:
            checks.append({'fact':k,'wanted':wanted,'actual':None,'status':'unknown'});unknown.append(k)
        elif context[k]!=wanted:
            checks.append({'fact':k,'wanted':wanted,'actual':context[k],'status':'contradicted'});mismatch.append(k)
        else:checks.append({'fact':k,'wanted':wanted,'actual':context[k],'status':'satisfied'})
    status='DOES_NOT_APPLY' if mismatch else 'UNKNOWN' if unknown else 'APPLIES'
    return {'obstruction_id':obstruction['id'],'status':status,'checks':checks,'certificate_ref':obstruction['certificate_ref'],
            'warning':'APPLIES means the stored obstruction contract matches this declared context; the certificate itself must still be valid and available.'}

def obstruction_library(obstructions,context):
    rows=[obstruction_applicability(o,context) for o in obstructions]
    return {'applies':[r for r in rows if r['status']=='APPLIES'],
            'unknown':[r for r in rows if r['status']=='UNKNOWN'],
            'does_not_apply':[r for r in rows if r['status']=='DOES_NOT_APPLY'],
            'scope':'Search memory remembers why a region was excluded and refuses to reuse the exclusion after its assumptions change.'}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('file');a=p.parse_args();d=json.load(open(a.file));print(json.dumps(obstruction_library(d['obstructions'],d['context']),indent=2))
