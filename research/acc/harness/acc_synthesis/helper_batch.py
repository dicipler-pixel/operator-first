#!/usr/bin/env python3
"""Complete multi-lane continuation entry point; no model/provider client.

Preserves continue_batch.py and its history. Recovered methods are explicit
registered commands, not instructions generated from untrusted search output.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
try:
    from .continue_batch import Continuation
    from .harness import ROOT, atomic_json, controller_lock, digest, read_json
    from .runtime import HarnessError, run_command
except ImportError:
    from continue_batch import Continuation
    from harness import ROOT, atomic_json, controller_lock, digest, read_json
    from runtime import HarnessError, run_command

CAPS={'wall_seconds':180,'node_cap':600000,'memory_mib':1024}


class HelperContinuation(Continuation):
    def lanes(self):
        registry=read_json(self.root/'helpers/lanes.json')
        if registry.get('schema')!='acc-helper-lanes/1':
            raise ValueError('Unsupported helper registry.')
        return [x for x in registry['lanes'] if x.get('enabled')]

    def fingerprints(self,lane):
        return {p:hashlib.sha256(self.h.local_file(p).read_bytes()).hexdigest()
                for p in lane['input_files']}

    @staticmethod
    def search_identity(job):
        ignored={'method_sha256','key'}
        # Charlie explores only the official start/goal, cap and target. Saved
        # routes are a baseline gate; an unchanged target gives the same search.
        if job.get('helper')=='charlie':ignored.update({'seed_sha256','baseline'})
        if job.get('helper')=='named' and job.get('query_uses_own_road') is False:
            ignored.update({'seed_sha256','baseline','target'})
        contract={k:v for k,v in job.items() if k not in ignored}
        if job.get('helper')=='named' and 'query_identity' in job:
            contract['inputs']={k:v for k,v in contract['inputs'].items() if k!='helpers/named_queries.json'}
        return digest(contract)

    @staticmethod
    def named_query_identity(query):
        # Fence the whole source file at execution, but remember only this row's
        # mathematical query. Changing another row or prose cannot reopen it.
        fields={'type','moves','entry_index','exit_indices','expected_state','ms_state'}
        return digest({k:v for k,v in query.items() if k in fields})

    def jobs(self,excluded=()):
        selected=read_json(self.root/'integration/selected_rows.json')['rows']
        routes=self.seeds()['routes']
        seen={a['key'] for a in self.cp['attempts']}
        try:
            from .helpers.negative_equivalences import validated_keys
        except ImportError:
            from helpers.negative_equivalences import validated_keys
        seen.update(validated_keys(self.root,self.cp,self.search_identity,digest))
        seen.update(self.search_identity(a['job']) for a in self.cp['attempts']
                    if a.get('job',{}).get('helper')=='charlie')
        for attempt in self.cp['attempts']:
            old=attempt.get('job',{})
            if old.get('helper')!='named':continue
            if 'query_identity' in old and 'query_uses_own_road' in old:
                seen.add(self.search_identity(old));continue
            if not attempt.get('result_path'):
                raise ValueError('Historical named query lacks portable result; reconcile explicitly.')
            archive=self.h.local_file(str(Path(attempt['result_path']).parent/'executed_named_queries.json'))
            if hashlib.sha256(archive.read_bytes()).hexdigest()!=old['inputs']['helpers/named_queries.json']:
                raise ValueError('Historical named query snapshot changed; do not reopen its miss.')
            saved=read_json(archive)['rows'][old['row_id']]
            alias={**old,'query_identity':self.named_query_identity(saved),
                   'query_uses_own_road':saved.get('type')=='road_exit' and saved.get('moves') is None}
            seen.add(self.search_identity(alias))
        jobs=[]
        for lane in self.lanes():
            sources=self.fingerprints(lane)
            method=hashlib.sha256(self.h.local_file(lane['script']).read_bytes()).hexdigest()
            for row in selected:
                cid=row['row_id']
                if cid in excluded or (lane.get('rows') and cid not in lane['rows']):
                    continue
                moves=sorted({tuple(r['moves']) for r in routes if r['row_id']==cid})
                baseline=min(map(len,moves)) if moves else None
                target=min(row['record'],baseline-1) if baseline is not None else row['record']
                job={'row_id':cid,'track':'AC','helper':lane['name'],
                     'algorithm_id':lane['algorithm_id'],'script':lane['script'],
                     'method_sha256':method,'inputs':sources,'seed_sha256':digest(moves),
                     'baseline':baseline,'target':target,'caps':CAPS}
                if lane['name']=='named':
                    query=read_json(self.root/'helpers/named_queries.json')['rows'][cid]
                    job['query_identity']=self.named_query_identity(query)
                    job['query_uses_own_road']=query.get('type')=='road_exit' and query.get('moves') is None
                job['key']=self.search_identity(job)
                if job['key'] not in seen:
                    jobs.append(job)
        # Balanced helper coverage; within a lane, near-record unheld rows first.
        counts={lane['name']:sum(a.get('job',{}).get('helper')==lane['name']
                 for a in self.cp['attempts']) for lane in self.lanes()}
        jobs.sort(key=lambda j:(counts[j['helper']],j['row_id'] in {'ac-00005','ac-00021'},
                               j['baseline'] is None,
                               j['baseline']-j['target'] if j['baseline'] is not None else 0,
                               j['helper'],j['row_id']))
        return jobs

    def plan(self,excluded=()):
        if self.cp['stopped'] or self.h.store.stopped():return {'status':'stopped'}
        if self.cp.get('active'):return {'status':'active','active':self.cp['active']}
        jobs=self.jobs(excluded)
        return ({'status':'planned','job':jobs[0],'remaining_jobs':len(jobs)} if jobs else
                {'status':'exhausted','reason':'All eligible helper/row/input probes are already recorded or claimed. New evidence or a justified method is required.'})

    def record(self,job,result_path,origin,task_id=None):
        result_path=Path(result_path).resolve();result_path.relative_to(self.root)
        result=read_json(result_path)
        sha=hashlib.sha256(result_path.read_bytes()).hexdigest()
        old=next((a for a in self.cp['attempts'] if a['key']==job['key']),None)
        if old:
            if old.get('result_sha256')==sha:return old
            raise ValueError('Attempt key already has a different result.')
        self.h.validate_result({'role':'sol_builder'},result)
        gate=None
        if result['kind']=='candidate':
            candidate=result['candidate']
            if candidate['row_id']!=job['row_id'] or candidate['track']!='AC':
                raise ValueError('Result differs from reserved row/track.')
            gate=self.h.check_candidate(candidate,task_id)
            receipt=gate.pop('receipt_path',None)
            if receipt:gate['official_receipt']=read_json(receipt)
            improved=(job['baseline'] is None or len(candidate['moves'])<job['baseline'])
            if gate.get('exact_verified') and improved:
                seeds=self.seeds()
                route={'row_id':candidate['row_id'],'moves':candidate['moves'],
                       'sources':[{'archive':str(result_path.relative_to(self.root)),
                                   'exact_receipt':gate.get('official_receipt')} ]}
                if not any(r['row_id']==route['row_id'] and r['moves']==route['moves'] for r in seeds['routes']):
                    seeds['routes'].append(route)
                    atomic_json(self.root/'continuation/routes.json',seeds)
        entry={'key':job['key'],'job':job,'origin':origin,'finished_at':time.time(),
               'result_path':str(result_path.relative_to(self.root)),'result_sha256':sha,
               'kind':result['kind'],'summary':result['summary'],'gate':gate,
               'limits':result.get('limits'),'reopen_when':result.get('reopen_when')}
        self.cp['attempts'].append(entry);self.cp['active']=None
        self.h.store.event('helper.batch.recorded',entry);self.save()
        return entry

    def run_reserved(self,key,reservation_commit):
        a=self.cp.get('active')
        if not a or a['job']['key']!=key:raise ValueError('No matching reservation.')
        if 'helper' not in a['job']:return super().run_reserved(key,reservation_commit)
        if not isinstance(reservation_commit,str) or len(reservation_commit)!=40 or any(c not in '0123456789abcdef' for c in reservation_commit):
            raise ValueError('Commit the reservation before execution.')
        if self.cp['stopped'] or self.h.store.stopped():raise ValueError('Harness stopped.')
        job=a['job']
        lease=next((t for t in self.h.store.tasks('running') if t['id']==a['task_id']),None)
        if not lease or lease['token']!=a['lease_token'] or lease['lease_until']<=time.time():
            raise ValueError('Local lease missing or expired; recover explicitly without rerunning.')
        lane=next((x for x in self.lanes() if x['name']==job['helper']),None)
        if not lane or lane['script']!=job['script'] or lane['algorithm_id']!=job['algorithm_id']:
            raise ValueError('Registered helper changed after reservation.')
        script=self.h.local_file(job['script'])
        seeds=sorted({tuple(r['moves']) for r in self.seeds()['routes'] if r['row_id']==job['row_id']})
        if hashlib.sha256(script.read_bytes()).hexdigest()!=job['method_sha256'] or self.fingerprints(lane)!=job['inputs'] or digest(seeds)!=job['seed_sha256']:
            raise ValueError('Reserved source or inputs changed.')
        out=self.root/'runs'/(job['helper']+'_revival')/('code_'+key[:16])
        a.update(phase='running',reservation_commit=reservation_commit);self.save()
        caps=job['caps']
        command=[sys.executable,str(script),'--row',job['row_id'],'--output-dir',str(out),
                 '--wall-seconds',str(caps['wall_seconds']),'--node-cap',str(caps['node_cap']),
                 '--target-length',str(job['target']),'--memory-mib',str(caps['memory_mib'])]
        try:
            summary=run_command(command,{},255,store=self.h.store,lease=lease,max_output_bytes=1048576)
            if hashlib.sha256(script.read_bytes()).hexdigest()!=job['method_sha256'] or self.fingerprints(lane)!=job['inputs']:
                raise ValueError('Helper source or inputs changed during execution.')
            result=read_json(out/'worker_result.json')
            self.h.validate_result({'role':'sol_builder'},result)
            entry=self.record(job,out/'worker_result.json','deterministic_helper_code',lease['id'])
            self.h.store.finish(lease['id'],lease['token'],result)
            self.h.store.event('task.handled',{'task_id':lease['id']})
            return {'status':'completed','attempt':entry,'worker_summary':summary}
        except Exception as exc:
            code=exc.code if isinstance(exc,HarnessError) else type(exc).__name__
            if not any(x['key']==key for x in self.cp['attempts']):
                self.cp['attempts'].append({'key':key,'job':job,'kind':'interrupted',
                    'reason':code,'finished_at':time.time(),'output_dir':str(out.relative_to(self.root))})
            self.cp['active']=None;self.save()
            try:self.h.store.fail(lease['id'],lease['token'],{'code':code})
            except HarnessError:pass
            raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','reserve','run','recover','stop','ack'])
    p.add_argument('--key');p.add_argument('--repo-head');p.add_argument('--reservation-commit')
    p.add_argument('--exclude-row',action='append',default=[]);p.add_argument('--state')
    args=p.parse_args();c=HelperContinuation(state=args.state)
    with controller_lock(c.h.state):
        if args.action=='plan':result=c.plan(args.exclude_row)
        elif args.action=='reserve':result=c.reserve(args.key,args.repo_head,args.exclude_row)
        elif args.action=='run':result=c.run_reserved(args.key,args.reservation_commit)
        elif args.action=='recover':result=c.recover()
        elif args.action=='stop':
            c.cp['stopped']=True;c.h.store.stop('helper continuation stopped');c.save();result={'status':'stopped'}
        else:
            if not args.key:raise ValueError('Notification key required.')
            if args.key not in c.cp['notifications']:c.cp['notifications'].append(args.key)
            c.save();result={'status':'acknowledged'}
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
