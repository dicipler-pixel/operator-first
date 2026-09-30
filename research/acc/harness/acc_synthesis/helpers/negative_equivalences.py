"""Validate narrow, evidence-backed equivalences without fabricating searches."""
from collections import deque
import hashlib
import json
from pathlib import Path


def validated_keys(root, checkpoint, identity, digest):
    ledger=Path(root)/'continuation/negative_equivalences.json'
    if not ledger.exists():
        return set()
    doc=json.loads(ledger.read_text())
    if doc.get('schema')!='acc-negative-equivalences/1':
        raise ValueError('Unsupported negative equivalence ledger')
    attempts={a['key']:a for a in checkpoint['attempts']}
    def load_checked(path, expected):
        file=(Path(root)/path).resolve()
        file.relative_to(Path(root).resolve())
        data=file.read_bytes()
        if hashlib.sha256(data).hexdigest()!=expected:
            raise ValueError('Negative equivalence evidence hash mismatch: '+path)
        return json.loads(data)
    def result(key):
        a=attempts[key]
        if a['kind']=='interrupted':
            raise ValueError('Interrupted work cannot establish an equivalence')
        return a,load_checked(a['result_path'],a['result_sha256'])
    def evidence(r, name):
        found=[e for e in r['evidence'] if Path(e['path']).name==name]
        if len(found)!=1:
            raise ValueError('Missing equivalence evidence: '+name)
        return load_checked(found[0]['path'],found[0]['sha256'])
    keys=set()
    for entry in doc['closures']:
        if entry['type']!='bob-zero-match-plus-complete-own-union':
            raise ValueError('Unregistered equivalence type')
        job=entry['job']
        if identity(job)!=job['key'] or job['helper']!='bob':
            raise ValueError('Invalid equivalence identity')
        old,old_result=result(entry['donor_attempt_key'])
        union,union_result=result(entry['union_attempt_key'])
        old_job=old['job']; union_job=union['job']
        for field in ('row_id','track','helper','algorithm_id','script','method_sha256','inputs','caps'):
            if old_job[field]!=job[field]:
                raise ValueError('Donor search contract differs: '+field)
        coverage=evidence(old_result,'coverage.json')
        source_key=next(iter(job['inputs']))
        bundle=load_checked(entry['donor_source_archive'],job['inputs'][source_key])
        count=sum(d['id']!=job['row_id'] for d in bundle['rows'])
        if (coverage['row_id']!=job['row_id'] or
            coverage['termination_reason']!='exhausted_donor_automorphisms' or
            coverage['relator_class_matches']!=0 or
            coverage['verified_donor_transfer_attempts']!=0 or
            coverage['successful_transfers']!=0 or
            coverage['donors_examined']!=count or
            coverage['automorphisms']<=0 or
            coverage['automorphism_comparisons']!=count*coverage['automorphisms']):
            raise ValueError('Donor comparisons are not a complete zero-match pass')
        snap=next(e for e in old_result['evidence'] if Path(e['path']).name=='executed_bob_lane_v1.py')
        if snap['sha256']!=job['method_sha256']:
            raise ValueError('Donor method snapshot differs')
        raw=(Path(root)/snap['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=snap['sha256']:
            raise ValueError('Donor method evidence changed')
        if (union_job['row_id']!=job['row_id'] or union_job['track']!=job['track'] or
            union_job['algorithm_id']!='exact-layered-bidirectional-route-union-v1' or
            union_job['seed_sha256']!=job['seed_sha256'] or union_job['baseline']!=job['baseline']):
            raise ValueError('Own-road union contract differs')
        saved=evidence(union_result,'saved_union.json')
        roads=sorted({tuple(r['moves']) for r in saved['routes']})
        if digest(roads)!=job['seed_sha256'] or saved['row_id']!=job['row_id']:
            raise ValueError('Own-road union input differs')
        # This is a finite check of an already archived exact graph, not a new
        # expansion or proof of a global lower bound. Unit primitive edges only.
        states=saved['states']
        if len(states)>job['caps']['node_cap']:
            raise ValueError('Archived union exceeds the existing record bound')
        start=states.index(saved['start']); target=states.index(saved['target'])
        graph=[[] for _ in states]
        for s,m,t in saved['edges']:
            if not (0<=s<len(states) and 0<=t<len(states) and 0<=m<14):
                raise ValueError('Invalid archived union edge')
            graph[s].append(t)
        queue=deque([start]);dist={start:0}
        while queue:
            s=queue.popleft()
            for t in graph[s]:
                if t not in dist:
                    dist[t]=dist[s]+1;queue.append(t)
        if dist.get(target)!=job['baseline'] or saved['union_shortest_length']!=job['baseline']:
            raise ValueError('The new own-road union may still improve')
        # Zero class matches is independent of saved-route cutoffs. The two
        # completed pieces cover this exact Bob input, even though its earlier
        # donor pass was part of a candidate-producing union run.
        keys.add(job['key'])
    return keys
