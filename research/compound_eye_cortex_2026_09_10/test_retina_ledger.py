#!/usr/bin/env python3
"""Finite controls for the full-retina ledger/report gate/miss tracer."""
from pathlib import Path
import json, tempfile
import retina_ledger as rl

OK_SURFACED = 'ce.data.provenance@1.0.0'
OK_HIDDEN = 'ce.frontier.coverage@1.0.0'
BLOCKED = 'ce.frontier.forcing@1.0.0'
NOT_ATTEMPTED = 'ce.extensions.inference@1.0.0'


def main():
    checks = 0
    refused = 0
    def req(x):
        nonlocal checks
        if not x: raise AssertionError('retina-ledger control failed')
        checks += 1

    run = {
        'schema':'compound-eye-run-v1',
        'engine_version':'test',
        'request_sha256':'a'*64,
        'result_sha256':'b'*64,
        'results':[
            {'eye':OK_SURFACED,'status':'ok','value_sha256':'1'*64,
             'context_sha256':'c'*64,'definition_sha256':'d'*64},
            {'eye':OK_HIDDEN,'status':'ok','value_sha256':'2'*64,
             'context_sha256':'c'*64,'definition_sha256':'e'*64},
            {'eye':BLOCKED,'status':'blocked','reason':'Missing exact tower',
             'context_sha256':'c'*64,'definition_sha256':'f'*64},
        ]
    }
    led = rl.ledger_from_run(run, surfaced_refs=[OK_SURFACED])
    req(led['schema']==rl.LEDGER_SCHEMA)
    req(led['registry_eye_versions']>=191)
    req(len(led['rows'])==led['registry_eye_versions'])
    req(led['surfaced_count']==1)
    by={r['eye']:r for r in led['rows']}
    req(by[OK_SURFACED]['execution_status']=='ok' and by[OK_SURFACED]['surfaced'])
    req(by[OK_HIDDEN]['execution_status']=='ok' and not by[OK_HIDDEN]['surfaced'])
    req(by[BLOCKED]['execution_status']=='blocked')
    req(by[NOT_ATTEMPTED]['execution_status']=='not_attempted')
    req(sum(led['execution_status_counts'].values())==led['registry_eye_versions'])

    claims=[
      {'schema':rl.CLAIM_SCHEMA,'id':'c.good','statement':'Scoped positive conclusion',
       'verdict':'established_within_scope','assumptions_met':True,'evidence_refs':[OK_SURFACED]},
      {'schema':rl.CLAIM_SCHEMA,'id':'c.negative','statement':'Candidate claim is false in scope',
       'verdict':'falsified_within_scope','assumptions_met':True,'evidence_refs':[OK_HIDDEN]},
      {'schema':rl.CLAIM_SCHEMA,'id':'c.unknown','statement':'Unknown claim',
       'verdict':'inconclusive','assumptions_met':True,'evidence_refs':[OK_SURFACED]},
      {'schema':rl.CLAIM_SCHEMA,'id':'c.blocked','statement':'Unsupported claim',
       'verdict':'established_within_scope','assumptions_met':True,'evidence_refs':[BLOCKED]},
      {'schema':rl.CLAIM_SCHEMA,'id':'c.assumption','statement':'Premise missing',
       'verdict':'established_within_scope','assumptions_met':False,'evidence_refs':[OK_SURFACED]},
    ]
    gate=rl.report_gate(claims,led)
    req([x['id'] for x in gate['licensed_conclusions']]==['c.good','c.negative'])
    req({x['id'] for x in gate['ledger_only_claims']}=={'c.unknown','c.blocked','c.assumption'})

    miss=rl.trace_miss(led,[OK_SURFACED,OK_HIDDEN,BLOCKED,NOT_ATTEMPTED,'ce.future.eye@1.0.0'])
    cls={r['eye']:r['miss_class'] for r in miss['rows']}
    req(cls[OK_SURFACED]=='SURFACED_EARLIER')
    req(cls[OK_HIDDEN]=='SEEN_BUT_NOT_SURFACED')
    req(cls[BLOCKED]=='BLOCKED_EARLIER')
    req(cls[NOT_ATTEMPTED]=='NOT_ATTEMPTED_EARLIER')
    req(cls['ce.future.eye@1.0.0']=='NOT_IN_EARLIER_REGISTRY')

    fg=rl.foreground_priority(led,[OK_HIDDEN])
    req(len(fg['rows'])==len(led['rows']))
    req(sum(r['foreground_priority'] for r in fg['rows'])==1)
    req(next(r for r in fg['rows'] if r['eye']==OK_SURFACED)['surfaced'])

    active=rl.active_refs()
    req(len(active)<=led['registry_eye_versions'] and len(active)>0)
    req(all(ref in by for ref in active.values()))

    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'history.jsonl'
        a=rl.append_hashed_record(p,led); b=rl.append_hashed_record(p,fg)
        rows=rl.verify_hashed_records(p)
        req(len(rows)==2 and rows[0]['event_sha256']==a['event_sha256'] and rows[1]['event_sha256']==b['event_sha256'])
        text=p.read_text();p.write_text(text.replace('not_attempted','tampered',1))
        try: rl.verify_hashed_records(p)
        except ValueError: refused += 1
        else: raise AssertionError('tampered ledger chain accepted')

    bad=[
      lambda:rl.ledger_from_run({'schema':'wrong','results':[]}),
      lambda:rl.ledger_from_run(run,surfaced_refs=['ce.no.such.eye@1.0.0']),
      lambda:rl.report_gate([{'schema':'wrong'}],led),
      lambda:rl.trace_miss({'schema':'wrong'},[OK_SURFACED]),
      lambda:rl.foreground_priority(led,['ce.no.such.eye@1.0.0']),
    ]
    for fn in bad:
        try: fn()
        except ValueError: refused += 1
        else: raise AssertionError('invalid retina-ledger input accepted')
    req(refused==6)

    out={'status':'PASS','positive_controls':checks,'refused_or_tampered_controls':refused,
         'registry_eye_versions':led['registry_eye_versions'],
         'active_stable_eye_ids':led['active_stable_eye_ids'],
         'seen_not_surfaced_demo':cls[OK_HIDDEN],
         'scope':'Meta-layer controls only; no scientific theorem is certified by this test.'}
    Path('retina_ledger_test_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
