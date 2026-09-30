#!/usr/bin/env python3
"""One bounded code search through the harness, with portable negative memory.

The host commits a reservation before executing it and commits the result after.
There is no model, GitHub, scheduling, or submission client in this program.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
try:
    from .harness import Harness, ROOT, atomic_json, controller_lock, digest, read_json
    from .runtime import HarnessError, run_command
except ImportError:
    from harness import Harness, ROOT, atomic_json, controller_lock, digest, read_json
    from runtime import HarnessError, run_command

CAPS = {'wall_seconds':180, 'node_cap':600000, 'depth':8,
        'profile':'route-local', 'memory_mib':1024}
ALGORITHM_ID = 'exact-layered-bidirectional-route-union-v1'


class Continuation:
    def __init__(self, root=ROOT, state=None):
        self.root = Path(root).resolve()
        self.h = Harness(self.root/'config.json', state or self.root/'state')
        self.path = self.root/'continuation/checkpoint.json'
        self.cp = read_json(self.path)
        if self.cp.get('schema') != 'acc-continuation/1':
            raise ValueError('Missing or unsupported continuation checkpoint; do not reset it.')

    def save(self):
        self.cp['updated_at'] = time.time()
        atomic_json(self.path, self.cp)

    def seeds(self):
        return read_json(self.root/'continuation/routes.json')

    def plan(self, excluded=()):
        if self.cp['stopped'] or self.h.store.stopped():
            return {'status':'stopped'}
        if self.cp.get('active'):
            return {'status':'active', 'active':self.cp['active']}
        selected = read_json(self.root/'integration/selected_rows.json')['rows']
        routes = self.seeds()['routes']
        method = hashlib.sha256((self.root/'bridge_search.py').read_bytes()).hexdigest()
        rows = []
        seen = {a['key'] for a in self.cp['attempts']}
        for row in selected:
            cid = row['row_id']
            if cid in excluded:
                continue
            moves = sorted({tuple(r['moves']) for r in routes if r['row_id']==cid})
            if not moves:
                continue
            best = min(map(len,moves))
            target = min(row['record'],best-1)
            job = {'row_id':cid, 'track':'AC', 'baseline':best, 'target':target,
                   'seed_sha256':digest(moves), 'method_sha256':method, 'caps':CAPS,
                   'algorithm_id':ALGORITHM_ID}
            # Source hashes fence execution; cosmetic edits do not erase misses.
            job['key'] = digest({k:v for k,v in job.items() if k!='method_sha256'})
            if job['key'] not in seen:
                rows.append(job)
        if not rows:
            return {'status':'exhausted', 'reason':'No untested seeded row under these bounds; new seeds or a justified new method are needed.'}
        # Prioritize near-record unheld rows before improvements to accepted ties.
        rows.sort(key=lambda j:(j['row_id'] in {'ac-00005','ac-00021'},
                                j['baseline']-j['target'],j['row_id']))
        return {'status':'planned', 'job':rows[0], 'remaining_jobs':len(rows)}

    def reserve(self, expected_key, repo_head, excluded=()):
        plan = self.plan(excluded)
        if plan['status']!='planned' or plan['job']['key']!=expected_key:
            raise ValueError('Plan changed or another batch is active; inspect again.')
        if len(repo_head)!=40 or any(c not in '0123456789abcdef' for c in repo_head):
            raise ValueError('A freshly inspected GitHub commit SHA is required.')
        job = plan['job']
        self.h.store.admit('code.batch.reserving', {'job':job,'repo_head':repo_head})
        task_id = self.h.store.enqueue('code_search',job,'code:'+job['key'],family=job['row_id'])
        lease = self.h.store.claim('code_search',lease_seconds=600,task_id=task_id)
        if not lease:
            raise ValueError('Row already active or this exact local task already ran.')
        self.cp['active'] = {'job':job,'task_id':task_id,'lease_token':lease['token'],
                             'expires_at':lease['lease_until'],'repo_head':repo_head,
                             'phase':'reserved','host_must_commit_before_execution':True}
        self.save()
        return {'status':'reserved','active':self.cp['active']}

    def record(self, job, result_path, origin, task_id=None):
        result_path = Path(result_path).resolve()
        result_path.relative_to(self.root)
        result = read_json(result_path)
        old = next((a for a in self.cp['attempts'] if a['key']==job['key']),None)
        if old:
            if old.get('result_sha256')==hashlib.sha256(result_path.read_bytes()).hexdigest():
                return old
            raise ValueError('An immutable attempt already exists for this probe key.')
        self.h.validate_result({'role':'sol_builder'},result)
        gate = None
        if result['kind']=='candidate':
            candidate = result['candidate']
            if candidate['row_id']!=job['row_id'] or candidate['track']!='AC':
                raise ValueError('Result row/track differs from reserved contract.')
            gate = self.h.check_candidate(candidate,task_id)
            receipt_path = gate.pop('receipt_path',None)
            if receipt_path:
                gate['official_receipt'] = read_json(receipt_path)
            if gate.get('exact_verified') and len(candidate['moves']) < job['baseline']:
                seeds = self.seeds()
                route = {'row_id':candidate['row_id'],'moves':candidate['moves'],
                         'sources':[{'archive':str(result_path.relative_to(self.root)),
                                     'exact_receipt':gate.get('official_receipt')}]}
                if not any(r['row_id']==route['row_id'] and r['moves']==route['moves'] for r in seeds['routes']):
                    seeds['routes'].append(route)
                    atomic_json(self.root/'continuation/routes.json',seeds)
        entry = {'key':job['key'],'job':job,'origin':origin,'finished_at':time.time(),
                 'result_path':str(result_path.relative_to(self.root)),
                 'result_sha256':hashlib.sha256(result_path.read_bytes()).hexdigest(),
                 'kind':result['kind'],'summary':result['summary'],'gate':gate,
                 'limits':result.get('limits'), 'reopen_when':result.get('reopen_when')}
        self.cp['attempts'].append(entry)
        self.h.store.event('code.batch.recorded',entry)
        self.cp['active'] = None
        self.save()
        return entry

    def run_reserved(self, expected_key, reservation_commit):
        active = self.cp.get('active')
        if not active or active['job']['key']!=expected_key:
            raise ValueError('No matching reservation.')
        if len(reservation_commit)!=40 or any(c not in '0123456789abcdef' for c in reservation_commit):
            raise ValueError('Commit the reservation privately before running.')
        if self.cp['stopped'] or self.h.store.stopped():
            raise ValueError('Harness stopped.')
        lease = next((t for t in self.h.store.tasks('running') if t['id']==active['task_id']),None)
        if not lease or lease['token']!=active['lease_token'] or lease['lease_until']<=time.time():
            raise ValueError('Local lease missing or expired. Recover explicitly; do not repeat the probe.')
        job = active['job']
        caps = job['caps']
        # Bind execution to the exact code and seeds that were reserved.
        seeds = sorted({tuple(r['moves']) for r in self.seeds()['routes'] if r['row_id']==job['row_id']})
        if digest(seeds)!=job['seed_sha256'] or hashlib.sha256((self.root/'bridge_search.py').read_bytes()).hexdigest()!=job['method_sha256']:
            raise ValueError('Reserved seeds or method changed.')
        out = self.root/'runs'/('code_'+job['key'][:16])
        active.update(phase='running',reservation_commit=reservation_commit)
        self.save()
        command = [sys.executable,str(self.root/'bridge_search.py'),'--row',job['row_id'],
                   '--output-dir',str(out),'--wall-seconds',str(caps['wall_seconds']),
                   '--node-cap',str(caps['node_cap']),'--profile',caps['profile'],
                   '--depth',str(caps['depth']),'--target-length',str(job['target']),
                   '--memory-mib',str(caps['memory_mib']),
                   '--routes',str(self.root/'continuation/routes.json')]
        try:
            summary = run_command(command,{},255,store=self.h.store,lease=lease,max_output_bytes=1048576)
            if hashlib.sha256((self.root/'bridge_search.py').read_bytes()).hexdigest()!=job['method_sha256']:
                raise ValueError('Search source changed during execution; preserve artifacts for review.')
            result = read_json(out/'worker_result.json')
            self.h.validate_result({'role':'sol_builder'},result)
            entry = self.record(job,out/'worker_result.json','deterministic_code',lease['id'])
            self.h.store.finish(lease['id'],lease['token'],result)
            self.h.store.event('task.handled',{'task_id':lease['id']})
            return {'status':'completed','attempt':entry,'worker_summary':summary}
        except Exception as exc:
            code = exc.code if isinstance(exc,HarnessError) else type(exc).__name__
            failure = {'key':job['key'],'job':job,'kind':'interrupted','reason':code,
                       'finished_at':time.time(),'output_dir':str(out.relative_to(self.root))}
            if not any(a['key']==job['key'] for a in self.cp['attempts']):
                self.cp['attempts'].append(failure)
            self.cp['active']=None
            self.save()
            try:
                self.h.store.fail(lease['id'],lease['token'],{'code':code})
            except HarnessError:
                pass
            raise

    def recover(self):
        active=self.cp.get('active')
        if not active:
            return {'status':'idle'}
        if active['expires_at']>time.time():
            raise ValueError('Reservation is still active; leave it alone.')
        self.h.store.recover()
        self.cp['attempts'].append({'key':active['job']['key'],'job':active['job'],
                                   'kind':'interrupted','reason':'expired_portable_reservation',
                                   'finished_at':time.time()})
        self.cp['active']=None
        self.save()
        return {'status':'recovered_without_retry'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','reserve','run','recover','stop','ack'])
    p.add_argument('--key')
    p.add_argument('--repo-head')
    p.add_argument('--reservation-commit')
    p.add_argument('--exclude-row',action='append',default=[])
    p.add_argument('--state')
    a=p.parse_args()
    c=Continuation(state=a.state)
    with controller_lock(c.h.state):
        if a.action=='plan': result=c.plan(a.exclude_row)
        elif a.action=='reserve': result=c.reserve(a.key,a.repo_head,a.exclude_row)
        elif a.action=='run': result=c.run_reserved(a.key,a.reservation_commit)
        elif a.action=='recover': result=c.recover()
        elif a.action=='stop':
            c.cp['stopped']=True;c.h.store.stop('continuation stopped');c.save();result={'status':'stopped'}
        else:
            if not a.key: raise ValueError('Notification key required.')
            if a.key not in c.cp['notifications']: c.cp['notifications'].append(a.key)
            c.save();result={'status':'acknowledged'}
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
