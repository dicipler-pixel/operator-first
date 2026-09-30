import json
from pathlib import Path
import shutil
import tempfile
import unittest
from acc_synthesis.helper_batch import HelperContinuation
from acc_synthesis.harness import ROOT,atomic_json


class HelperBatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for name in ['helpers','integration','continuation']:(self.root/name).mkdir()
        for name in ['config.json','integration/selected_rows.json']:
            shutil.copy(ROOT/name,self.root/name)
        atomic_json(self.root/'continuation/checkpoint.json',{'schema':'acc-continuation/1',
                    'stopped':False,'active':None,'attempts':[],'notifications':[]})
        atomic_json(self.root/'continuation/routes.json',{'routes':[]})
        (self.root/'helpers/donor.json').write_text('{}')
        (self.root/'helpers/fixture.py').write_text('''import sys,json,pathlib,hashlib
p=pathlib.Path(sys.argv[sys.argv.index('--output-dir')+1]);p.mkdir(parents=True)
e=p/'coverage.json';e.write_text('{"fixture":true}')
r={"kind":"bounded_miss","summary":"transport fixture only","limits":{"fixture":1},
"reopen_when":{"event":"new_fixture"},"evidence":[{"path":str(e.relative_to(pathlib.Path(__file__).parent.parent)),"sha256":hashlib.sha256(e.read_bytes()).hexdigest()}]}
(p/'worker_result.json').write_text(json.dumps(r));print(json.dumps({"fixture":True}))
''')
        atomic_json(self.root/'helpers/lanes.json',{'schema':'acc-helper-lanes/1','lanes':[
            {'name':n,'algorithm_id':n+'/fixture','script':'helpers/fixture.py',
             'input_files':['helpers/donor.json'],'enabled':True,'rows':['ac-00001']}
            for n in ['bob','charlie','kernel']]})

    def test_distinct_lanes_share_negative_memory_without_dispatching_models(self):
        c=HelperContinuation(self.root);names=[]
        for _ in range(3):
            job=c.plan()['job'];names.append(job['helper']);self.assertIsNone(job['baseline'])
            c.reserve(job['key'],'a'*40);c.run_reserved(job['key'],'b'*40)
        self.assertEqual(len(set(names)),3)
        self.assertEqual(c.h.status()['reserved_worker_dispatches'],0)
        fresh=HelperContinuation(self.root,state=self.root/'fresh_host')
        self.assertEqual(fresh.plan()['status'],'exhausted')

    def test_changed_foreign_pool_invalidates_reservation(self):
        c=HelperContinuation(self.root);job=c.plan()['job'];c.reserve(job['key'],'a'*40)
        (self.root/'helpers/donor.json').write_text('{"new_seed":true}')
        with self.assertRaisesRegex(ValueError,'Reserved source or inputs changed'):
            c.run_reserved(job['key'],'b'*40)

    def test_out_of_contract_candidate_is_rejected_before_checker(self):
        c=HelperContinuation(self.root);job=c.plan()['job']
        path=self.root/'bad.json';atomic_json(path,{'kind':'candidate','summary':'invalid fixture',
                'evidence':[],'candidate':{'row_id':'ac-00003','track':'AC'}})
        with self.assertRaisesRegex(ValueError,'reserved row/track'):
            c.record(job,path,'fixture')
        self.assertEqual(c.cp['attempts'],[])

    def test_new_seed_does_not_repeat_charlie_when_search_target_is_unchanged(self):
        atomic_json(self.root/'continuation/routes.json',{'routes':[
            {'row_id':'ac-00001','moves':[0]*410}]})
        c=HelperContinuation(self.root)
        job=next(j for j in c.jobs() if j['helper']=='charlie')
        # Preserve the historical seed-sensitive key as a migrated record.
        from acc_synthesis.harness import digest
        old_key=digest({k:v for k,v in job.items() if k not in {'key','method_sha256'}})
        c.cp['attempts'].append({'key':old_key,'job':{**job,'key':old_key}})
        c.save()
        atomic_json(self.root/'continuation/routes.json',{'routes':[
            {'row_id':'ac-00001','moves':[0]*410},
            {'row_id':'ac-00001','moves':[0]*409}]})
        self.assertEqual({j['helper'] for j in c.jobs()},{'bob','kernel'})
        self.assertEqual(c.cp['attempts'][0]['key'],old_key)


if __name__=='__main__':unittest.main()
