#!/usr/bin/env python3
"""Compound Eye theorem/claim genome 0.2.

This is a *contract registry*, not a theorem prover. It makes the information
that usually disappears between papers machine-checkable: scope, assumptions,
dependencies, evidence class, formal status, negative controls, counterexamples
and explicit cross-domain assumption mappings.
"""
from __future__ import annotations
from collections import defaultdict
import hashlib,json,re

ID=re.compile(r'[a-z][a-z0-9_.-]+$');VER=re.compile(r'\d+\.\d+\.\d+$')
EVIDENCE={'literature','written_proof','formal_proof','exact_certificate','numerical_diagnostic','measurement','counterexample','construction'}
FORMAL={'not_formalized','partly_formalized','formally_verified'}
STATUS={'idea','conjecture','conditional','established_within_scope','falsified','superseded'}

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def ref(c):return c['id']+'@'+c['version']

def validate_claim(c):
    required=['id','version','title','statement','domain','scope','assumptions','dependencies','evidence','acceptance','formal_status','status','negative_controls','counterexamples','limits']
    missing=[k for k in required if k not in c]
    if missing:raise ValueError('Missing claim fields: '+','.join(missing))
    if not ID.fullmatch(c['id']) or not VER.fullmatch(c['version']):raise ValueError('Invalid claim ID/version')
    for k in ['assumptions','dependencies','evidence','acceptance','negative_controls','counterexamples']:
        if not isinstance(c[k],list):raise ValueError(k+' must be a list')
    if c['formal_status'] not in FORMAL or c['status'] not in STATUS:raise ValueError('Invalid status')
    for e in c['evidence']:
        if not isinstance(e,dict) or e.get('class') not in EVIDENCE or not e.get('ref'):raise ValueError('Malformed evidence')
    if c['status']=='established_within_scope' and (not c['evidence'] or not c['acceptance']):
        raise ValueError('Established claim needs evidence and an acceptance mechanism')
    if c['formal_status']=='formally_verified' and not any(e['class']=='formal_proof' for e in c['evidence']):
        raise ValueError('Formally verified status requires formal-proof evidence')
    canonical(c);return True

def audit(claims):
    table={}
    for c in claims:
        validate_claim(c);r=ref(c)
        if r in table:raise ValueError('Duplicate claim '+r)
        table[r]=c
    missing=[]
    for r,c in table.items():
        for d in c['dependencies']:
            if d not in table:missing.append({'claim':r,'missing_dependency':d})
    visiting=set();done=set();order=[]
    def visit(r):
        if r in done:return
        if r in visiting:raise ValueError('Claim dependency cycle at '+r)
        visiting.add(r)
        for d in table[r]['dependencies']:
            if d in table:visit(d)
        visiting.remove(r);done.add(r);order.append(r)
    for r in table:visit(r)
    contradiction=[]
    for r,c in table.items():
        if c['status']=='falsified' and not any(e['class']=='counterexample' for e in c['evidence']):
            contradiction.append({'claim':r,'warning':'Falsified status has no counterexample evidence record.'})
    return {'claims':len(table),'topological_order':order,'missing_dependencies':missing,'status_warnings':contradiction,
            'claim_hashes':{r:digest(c) for r,c in table.items()},
            'scope':'Schema/dependency/evidence audit only; statements are not proved by registration.'}

def assumption_transfer(source_claim,target_facts,mapping):
    """Audit an explicit source-assumption -> target-fact dictionary.

    target_facts values are one of satisfied/unknown/contradicted. A completed
    mapping licenses only the *assumption bookkeeping*, never theorem transfer by itself.
    """
    validate_claim(source_claim);allowed={'satisfied','unknown','contradicted'}
    if any(v not in allowed for v in target_facts.values()):raise ValueError('Bad target fact status')
    rows=[]
    for a in source_claim['assumptions']:
        target=mapping.get(a)
        status='unmapped' if target is None else target_facts.get(target,'unknown')
        rows.append({'source_assumption':a,'target_fact':target,'status':status})
    extra=sorted(set(mapping)-set(source_claim['assumptions']))
    blocked=[r for r in rows if r['status']!='satisfied']
    return {'source_claim':ref(source_claim),'rows':rows,'extra_mapping_keys':extra,
            'all_source_assumptions_accounted_for':not blocked and not extra,
            'blocked':blocked,
            'scope':'Assumption dictionary audit only. A successful mapping does not prove the target theorem or physical identification.'}

def label_loss(required_labels,retained_labels):
    req=set(required_labels);got=set(retained_labels);missing=sorted(req-got)
    return {'required':sorted(req),'retained':sorted(got),'missing':missing,'safe_for_declared_question':not missing,
            'warning':None if not missing else 'The reduction discarded labels explicitly required by the downstream question.'}
