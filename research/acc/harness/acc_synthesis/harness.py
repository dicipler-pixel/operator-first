#!/usr/bin/env python3
"""Offline agent orchestration. Commands are configured clients, never model output."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import sys
import time
try:
    from .runtime import Store, HarnessError, run_command
    from .gates import verify_candidate
except ImportError:
    from runtime import Store, HarnessError, run_command
    from gates import verify_candidate

ROOT = Path(__file__).resolve().parent
SWITCH_FIELDS = ('seed', 'route_family', 'probe', 'representation', 'cost_model', 'board_filter')
ROLES = ('luna_memory', 'sol_builder', 'sol_checker', 'astra_advisor')

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp-' + str(os.getpid()))
    with tmp.open('w', encoding='utf-8') as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write('\n')
        out.flush()
        os.fsync(out.fileno())
    os.replace(tmp, path)

@contextlib.contextmanager
def controller_lock(state):
    state.mkdir(parents=True, exist_ok=True)
    with (state / 'controller.lock').open('a+b') as handle:
        if os.name == 'nt':
            import msvcrt
            handle.seek(0)
            if handle.read(1) == b'':
                handle.write(b'0'); handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == 'nt':
                handle.seek(0); msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)

class Harness:
    def __init__(self, config_path, state):
        self.config_path = Path(config_path).resolve()
        self.root = self.config_path.parent
        self.config = read_json(self.config_path)
        self.state = Path(state).resolve()
        self.state.mkdir(parents=True, exist_ok=True)
        self.config['checks_directory']=str(self.state/'checks')
        self.store = Store(self.state / 'ledger.sqlite3')
        self.limits = self.config['limits']
        if self.config.get('submission_enabled') or self.config.get('mode') != 'offline':
            raise ValueError('This implementation supports offline work only; no submission transport exists.')
        self.selected_rows = None
        if self.config.get('selected_rows'):
            path = self.local_file(self.config['selected_rows'])
            if hashlib.sha256(path.read_bytes()).hexdigest() != self.config.get('selected_rows_sha256'):
                raise ValueError('Selected row manifest hash mismatch.')
            rows = read_json(path)['rows']
            self.selected_rows = {r['row_id'] for r in rows}
            if not rows or len(rows) != len(self.selected_rows):
                raise ValueError('Selected rows must be nonempty and unique.')

    def in_scope(self, row_id):
        return self.selected_rows is None or row_id in self.selected_rows

    def local_file(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError('Evidence must be inside the configured workspace.')
        return path

    def validate_evidence(self, refs):
        if not isinstance(refs, list):
            raise ValueError('evidence must be a list')
        for ref in refs:
            if not isinstance(ref, dict) or not isinstance(ref.get('path'), str):
                raise ValueError('Each evidence entry requires path and sha256.')
            path = self.local_file(ref['path'])
            if not path.is_file() or path.stat().st_size > self.limits['max_evidence_bytes']:
                raise ValueError('Evidence file missing or over size cap: ' + ref['path'])
            if hashlib.sha256(path.read_bytes()).hexdigest() != ref.get('sha256'):
                raise ValueError('Evidence hash mismatch: ' + ref['path'])

    def validate_result(self, task, result):
        if not isinstance(result, dict) or not isinstance(result.get('summary'), str):
            raise ValueError('Worker must return a JSON object with summary.')
        role, kind = task['role'], result.get('kind')
        allowed = {'luna_memory': {'context','blocked'}, 'sol_builder': {'candidate','bounded_miss','blocked'},
                   'sol_checker': {'review','blocked'}, 'astra_advisor': {'proposal','review','blocked'}}
        if kind not in allowed[role]:
            raise ValueError('Unsupported result kind for role: ' + role)
        self.validate_evidence(result.get('evidence', []))
        if kind == 'bounded_miss':
            if not result.get('limits') or not result.get('evidence') or not result.get('reopen_when'):
                raise ValueError('A bounded miss requires limits, execution evidence, and reopen_when.')
        if kind == 'candidate' and not isinstance(result.get('candidate'), dict):
            raise ValueError('Candidate payload missing.')
        if kind == 'review' and result.get('verdict') not in ('accept','repair','escalate'):
            raise ValueError('Review must accept, repair, or escalate.')

    def add(self, work):
        if not self.in_scope(work.get('row_id')):
            raise ValueError('Row is outside the user-selected target set.')
        for key in ('objective','row_id','strategy'):
            if not work.get(key):
                raise ValueError('Work requires ' + key)
        if not isinstance(work['strategy'], dict):
            raise ValueError('strategy must be an object')
        if any(not work['strategy'].get(k) for k in SWITCH_FIELDS):
            raise ValueError('strategy must supply all six nonempty signature fields')
        work = {**work, 'repairs': 0, 'switches': 0}
        work['work_id'] = digest(work)
        return self.store.enqueue(self.context_role(), work, 'start:' + work['work_id'], family=work['row_id'])

    def context_role(self):
        return 'luna_memory' if self.config.get('routing', {}).get('model_memory', True) else 'sol_builder'

    def dispatch_budget(self, role):
        """Persistent launch count, not provider-token or currency accounting."""
        budget = self.config.get('dispatch_budget', {})
        cap = budget.get('total', 0)
        role_cap = budget.get('per_role', {}).get(role, 0)
        if type(cap) is not int or type(role_cap) is not int or min(cap, role_cap) < 0:
            raise ValueError('Dispatch limits must be nonnegative integers.')
        used = [e for e in self.store.events() if e['kind'] == 'worker.dispatch_reserved']
        return len(used) < cap and sum(e['payload']['role'] == role for e in used) < role_cap

    def reserve_dispatch(self, task):
        if not self.dispatch_budget(task['role']):
            raise HarnessError('Worker dispatch budget exhausted; no worker launched.', 'dispatch_budget')
        # Called under controller_lock. Failed launches are still charged to the cap.
        self.store.admit('worker.dispatch_reserved', {'task_id': task['id'], 'role': task['role']})

    def check_candidate(self, candidate, task_id=None):
        """Exact replay and eligibility without any model dispatch."""
        if not self.in_scope(candidate.get('row_id')):
            gate = {'status':'withheld', 'reason':'outside_user_selected_rows', 'exact_verified':False}
        else:
            gate = verify_candidate(candidate, self.config, self.root, cancelled=self.store.stopped)
        self.store.event('gate.result', {'task_id': task_id, 'candidate_sha256': digest(candidate), 'gate': gate})
        if self.store.stopped():
            gate = {**gate, 'status': 'withheld', 'reason': 'global_stop_before_export'}
        admission_id = None
        if gate['status'] == 'verified_scoring':
            try:
                admission_id = self.store.admit('candidate.admitted', {'task_id': task_id,
                    'candidate_sha256': digest(candidate), 'gate': gate, 'demo': bool(self.config.get('demo'))})
            except HarnessError:
                gate = {**gate, 'status': 'withheld', 'reason': 'global_stop_before_admission'}
        area = 'demo_results' if self.config.get('demo') else ('ready' if gate['status'] == 'verified_scoring' else 'withheld')
        atomic_json(self.state/area/(digest(candidate)+'.json'), {'candidate': candidate, 'gate': gate,
            'admission_event': admission_id, 'demo': bool(self.config.get('demo')),
            'scope': 'historical eligibility at checked_at; recheck before any external use'})
        return gate

    def child(self, task, role, payload, suffix):
        return self.store.enqueue(role, payload, f"task:{task['id']}:{suffix}", family=payload['row_id'])

    def memory(self):
        return [e for e in self.store.events() if e['kind'] in ('memory.parked','memory.reopened','memory.distinguished','gate.result','strategy.changed')]

    def park(self, task, result, reason):
        self.store.event('memory.parked', {'task_id':task['id'], 'work':task['payload'], 'result':result,
                         'reason':reason, 'reopen_when':result.get('reopen_when', {'event':'new_evidence', 'row_id':task['payload']['row_id']})})

    def reconcile(self):
        with controller_lock(self.state):
            self._reconcile()

    def _reconcile(self):
        """Replay completed tasks; unique child keys and stable output names make recovery idempotent."""
        handled = {e['payload']['task_id'] for e in self.store.events() if e['kind']=='task.handled'}
        for task in self.store.tasks('completed'):
            if task['id'] in handled or self.store.stopped():
                continue
            work, result, role = task['payload'], task['result'], task['role']
            if not self.in_scope(work.get('row_id')):
                self.park(task,result,'outside_user_selected_rows')
                self.store.event('task.handled', {'task_id':task['id']})
                continue
            kind = result['kind']
            if kind == 'blocked':
                self.park(task,result,'worker_blocked')
            elif role == 'luna_memory':
                self.child(task,'sol_builder',{**work,'retrieved_context':result},'build')
            elif role == 'sol_builder':
                if kind == 'candidate':
                    if self.config.get('routing', {}).get('model_candidate_review', True) or work.get('requires_model_review'):
                        self.child(task,'sol_checker',{**work,'builder_result':result},'review')
                    else:
                        gate = self.check_candidate(result['candidate'], task['id'])
                        if gate['status'] in ('invalid', 'withheld'):
                            self.park(task, {'kind':'blocked', 'summary':gate['reason'], 'evidence':[]}, 'gate_'+gate['status'])
                else:
                    self.park(task,result,'bounded_miss')
                    if work['switches'] < self.limits['max_switches']:
                        self.child(task,'astra_advisor',{**work,'failure':result},'advise')
            elif role == 'sol_checker':
                if result['verdict'] == 'accept':
                    gate = self.check_candidate(work['builder_result']['candidate'], task['id'])
                    if gate['status'] in ('invalid','withheld'):
                        self.park(task,{'kind':'blocked','summary':gate['reason'],'evidence':[]},'gate_'+gate['status'])
                elif result['verdict']=='repair' and work['repairs'] < self.limits['max_repairs']:
                    self.child(task,'sol_builder',{**work,'repairs':work['repairs']+1,'review':result},'repair')
                elif work['switches'] < self.limits['max_switches']:
                    self.child(task,'astra_advisor',{**work,'failure':result},'advise')
                else:
                    self.park(task,result,'review_budget_exhausted')
            elif role == 'astra_advisor':
                proposed = result.get('strategy')
                old = work['strategy']
                changed = [k for k in SWITCH_FIELDS if isinstance(proposed,dict) and old.get(k) != proposed.get(k)]
                if not isinstance(proposed,dict) or any(not proposed.get(k) for k in SWITCH_FIELDS) or not changed or not result.get('evidence') or not result.get('discriminating_test'):
                    self.park(task,result,'no_supported_switch')
                elif work['switches'] >= self.limits['max_switches']:
                    self.park(task,result,'switch_budget_exhausted')
                else:
                    self.store.event('strategy.changed',{'task_id':task['id'],'before':old,'after':proposed,'changed':changed,'evidence':result['evidence']})
                    updated = {**work,'strategy':proposed,'switches':work['switches']+1,'repairs':0,'advisor':result}
                    for key in ('builder_result','failure','review'):
                        updated.pop(key,None)
                    self.child(task,self.context_role(),updated,'switch')
            self.store.event('task.handled', {'task_id':task['id']})

    def wake(self, event):
        """Exact declarative event matching, with hash-checked supplied evidence; no LLM truth vote."""
        if not isinstance(event.get('event'),str) or not event.get('evidence'):
            raise ValueError('Wake needs event and hashed evidence.')
        self.validate_evidence(event['evidence'])
        key = digest(event)
        self.store.event('evidence.arrived',event)
        count = 0
        for entry in self.memory():
            if entry['kind'] != 'memory.parked':
                continue
            data = entry['payload']; condition = data['reopen_when']
            if not isinstance(condition,dict) or not condition:
                continue
            if all(event.get(k)==v for k,v in condition.items()):
                work = {**data['work'],'new_evidence':event}
                self.store.enqueue(self.context_role(),work,f"wake:{data['task_id']}:{key}",family=work['row_id'])
                self.store.event('memory.reopened',{'task_id':data['task_id'],'evidence_key':key})
                count += 1
        return count

    def distinguish(self, witness):
        for field in ('left','right','probe','left_output','right_output','evidence'):
            if field not in witness:
                raise ValueError('Distinction requires '+field)
        if witness['left']==witness['right'] or witness['left_output']==witness['right_output'] or not witness['evidence']:
            raise ValueError('A split requires different exact states and witnessed different outputs under one declared probe.')
        self.validate_evidence(witness['evidence'])
        self.store.event('memory.distinguished',{**witness,'witness_id':digest(witness),'grade':'V',
                                               'scope':'empirical witness; not a complete predictive quotient'})
        return digest(witness)

    def request(self, task):
        role = task['role']; spec = self.config['roles'][role]
        prompt_file = ROOT/'prompts'/f'{role}.md'
        return {'protocol':'acc-harness/1','task_id':task['id'],'lease_token':task['token'],
                'role':role,'model':spec['model'],'reasoning_effort':spec['effort'],
                'instruction':prompt_file.read_text(encoding='utf-8'), 'task':task['payload'],
                'memory':self.memory()[-40:], 'workspace':str(self.root),
                'limits':self.limits,'demo':bool(self.config.get('demo'))}

    def export_one(self, role=None):
        with controller_lock(self.state):
            self.store.recover(); self._reconcile()
            choices = [t for t in self.store.tasks('queued') if self.in_scope(t['payload'].get('row_id')) and (role is None or t['role'] == role) and self.dispatch_budget(t['role'])]
            if not choices:
                return None
            role = choices[0]['role']
            task = self.store.claim(role=role,lease_seconds=self.limits['worker_seconds']+30,task_id=choices[0]['id'])
            if task is None:
                return None
            self.reserve_dispatch(task)
            path=self.state/'requests'/f"{task['id']}.json"
            atomic_json(path,self.request(task))
            return {'path':str(path),'task_id':task['id'],'lease_until':task['lease_until']}

    def accept(self, task_id, token, result):
        with controller_lock(self.state):
            task=next((t for t in self.store.tasks() if t['id']==task_id),None)
            if task is None:
                raise ValueError('Unknown task.')
            self.validate_result(task,result)
            self.store.finish(task_id,token,result)
            self._reconcile()

    def run(self):
        started=time.monotonic(); completed=0
        with controller_lock(self.state):
            self.store.recover(); self._reconcile()
            while completed < self.limits['max_tasks_per_run'] and not self.store.stopped():
                remaining=self.limits['batch_seconds']-(time.monotonic()-started)
                if remaining <= 0:
                    break
                queued=self.store.tasks('queued')
                runnable=[t for t in queued if self.in_scope(t['payload'].get('row_id')) and self.config['roles'][t['role']].get('command') and self.dispatch_budget(t['role'])]
                if not runnable:
                    break
                task=self.store.claim(role=runnable[0]['role'],lease_seconds=self.limits['worker_seconds']+30,task_id=runnable[0]['id'])
                if task is None:
                    break
                spec=self.config['roles'][task['role']]
                command=[x.replace('{python}',sys.executable).replace('{root}',str(self.root)) for x in spec['command']]
                try:
                    self.reserve_dispatch(task)
                    result=run_command(command,self.request(task),min(remaining,self.limits['worker_seconds']),
                                       store=self.store,lease=task,max_output_bytes=self.limits['max_output_bytes'])
                    self.validate_result(task,result)
                    self.store.finish(task['id'],task['token'],result)
                except Exception as exc:
                    try:
                        self.store.fail(task['id'],task['token'],{'type':type(exc).__name__,'message':str(exc)})
                    except HarnessError:
                        pass
                completed+=1
                self._reconcile()
        return {'processed_tasks':completed,**self.status()}

    def status(self):
        counts={}
        for task in self.store.tasks():
            counts[task['status']]=counts.get(task['status'],0)+1
        missing=[role for role in ROLES if not self.config['roles'][role].get('command')]
        return {'stopped':self.store.stopped(),'tasks':counts,'unconnected_roles':missing,
                'dispatch_budget':self.config.get('dispatch_budget', {'total':0, 'per_role':{}}),
                'reserved_worker_dispatches':sum(e['kind']=='worker.dispatch_reserved' for e in self.store.events()),
                'selected_rows':sorted(self.selected_rows) if self.selected_rows is not None else None,
                'checker_connected':bool(self.config['checker'].get('command')),
                'demo':bool(self.config.get('demo')),'submission_enabled':False,
                'state':str(self.state)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default=str(ROOT/'config.json'))
    parser.add_argument('--state',default=str(ROOT/'state'))
    sub=parser.add_subparsers(dest='cmd',required=True)
    sub.add_parser('status'); sub.add_parser('run'); sub.add_parser('resume'); sub.add_parser('recover')
    p=sub.add_parser('stop'); p.add_argument('--reason',default='user stop')
    p=sub.add_parser('add'); p.add_argument('file')
    p=sub.add_parser('check'); p.add_argument('file')
    p=sub.add_parser('wake'); p.add_argument('file')
    p=sub.add_parser('distinguish'); p.add_argument('file')
    p=sub.add_parser('export'); p.add_argument('--role',choices=ROLES)
    p=sub.add_parser('accept'); p.add_argument('task_id',type=int); p.add_argument('token'); p.add_argument('file')
    p=sub.add_parser('heartbeat'); p.add_argument('task_id',type=int); p.add_argument('token')
    args=parser.parse_args()
    try:
        h=Harness(args.config,args.state)
        if args.cmd=='status': answer=h.status()
        elif args.cmd=='add': answer={'task_id':h.add(read_json(args.file))}
        elif args.cmd=='check':
            with controller_lock(h.state): answer=h.check_candidate(read_json(args.file))
        elif args.cmd=='run': answer=h.run()
        elif args.cmd=='export': answer=h.export_one(args.role)
        elif args.cmd=='accept': h.accept(args.task_id,args.token,read_json(args.file)); answer=h.status()
        elif args.cmd=='heartbeat': h.store.heartbeat(args.task_id,args.token,lease_seconds=h.limits['worker_seconds']+30); answer={'heartbeat':True}
        elif args.cmd=='stop': h.store.stop(args.reason); answer=h.status()
        elif args.cmd=='resume': h.store.resume(); answer=h.status()
        elif args.cmd=='recover': answer={'interrupted':h.store.recover()}
        elif args.cmd=='wake': answer={'matched_attempts':h.wake(read_json(args.file))}
        elif args.cmd=='distinguish': answer={'witness_id':h.distinguish(read_json(args.file))}
        print(json.dumps(answer,indent=2))
    except Exception as exc:
        print(json.dumps({'error':type(exc).__name__,'message':str(exc)}),file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':
    raise SystemExit(main())
