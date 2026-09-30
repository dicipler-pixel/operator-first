import json
from pathlib import Path
import shutil
import tempfile
import unittest
from acc_synthesis.continue_batch import Continuation
from acc_synthesis.harness import ROOT, atomic_json


class ContinuationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'integration').mkdir();(self.root/'continuation').mkdir()
        for file in ['config.json','integration/selected_rows.json']:
            shutil.copy(ROOT/file,self.root/file)
        routes=json.loads((ROOT/'integration/recovered_routes.json').read_text())
        routes['routes']=[r for r in routes['routes'] if r['row_id']=='ac-00037']
        atomic_json(self.root/'continuation/routes.json',routes)
        atomic_json(self.root/'continuation/checkpoint.json',{'schema':'acc-continuation/1',
                    'stopped':False,'active':None,'attempts':[],'notifications':[]})
        # Transport fixture only; does not pretend to search or verify an AC path.
        (self.root/'bridge_search.py').write_text('''import sys,json,pathlib,hashlib
p=pathlib.Path(sys.argv[sys.argv.index('--output-dir')+1]);p.mkdir(parents=True)
e=p/'coverage.json';e.write_text('{"fixture":true}')
r={"kind":"bounded_miss","summary":"transport fixture only","limits":{"fixture":1},
"reopen_when":{"event":"new_fixture"},"evidence":[{"path":str(e.relative_to(pathlib.Path(__file__).parent)),"sha256":hashlib.sha256(e.read_bytes()).hexdigest()}]}
(p/'worker_result.json').write_text(json.dumps(r))
print(json.dumps({"fixture":True}))
''')

    def reserve(self,c):
        key=c.plan()['job']['key'];c.reserve(key,'a'*40);return key

    def test_code_batch_persists_miss_without_model_dispatch_and_never_repeats(self):
        c=Continuation(self.root);key=self.reserve(c)
        result=c.run_reserved(key,'b'*40)
        self.assertEqual(result['attempt']['kind'],'bounded_miss')
        self.assertEqual(c.h.status()['reserved_worker_dispatches'],0)
        self.assertEqual(c.h.store.tasks('completed')[0]['role'],'code_search')
        restarted=Continuation(self.root,state=self.root/'fresh_host')
        self.assertEqual(restarted.plan()['status'],'exhausted')

    def test_reservation_survives_host_loss_and_cannot_be_adopted(self):
        c=Continuation(self.root);key=self.reserve(c)
        restarted=Continuation(self.root,state=self.root/'fresh_host')
        self.assertEqual(restarted.plan()['status'],'active')
        with self.assertRaisesRegex(ValueError,'Local lease'):
            restarted.run_reserved(key,'b'*40)
        with self.assertRaisesRegex(ValueError,'still active'):
            restarted.recover()
        restarted.cp['active']['expires_at']=0;restarted.save();restarted.recover()
        self.assertEqual(restarted.plan()['status'],'exhausted')

    def test_changed_seed_cannot_run_under_old_reservation(self):
        c=Continuation(self.root);key=self.reserve(c)
        routes=c.seeds();routes['routes'].pop();atomic_json(self.root/'continuation/routes.json',routes)
        with self.assertRaisesRegex(ValueError,'seeds or method changed'):
            c.run_reserved(key,'b'*40)

    def test_portable_stop_blocks_fresh_host(self):
        c=Continuation(self.root);c.cp['stopped']=True;c.save()
        restarted=Continuation(self.root,state=self.root/'fresh_host')
        self.assertEqual(restarted.plan()['status'],'stopped')

    def test_cosmetic_source_edit_does_not_erase_negative_memory(self):
        c=Continuation(self.root);key=self.reserve(c);c.run_reserved(key,'b'*40)
        script=self.root/'bridge_search.py';script.write_text(script.read_text()+'\n# cosmetic edit\n')
        self.assertEqual(Continuation(self.root).plan()['status'],'exhausted')

    def test_missing_result_is_interrupted_not_a_miss_or_repeat(self):
        (self.root/'bridge_search.py').write_text('print("{}")')
        c=Continuation(self.root);key=self.reserve(c)
        with self.assertRaises(FileNotFoundError):c.run_reserved(key,'b'*40)
        self.assertEqual(c.cp['attempts'][-1]['kind'],'interrupted')
        self.assertEqual(c.h.store.tasks('failed')[0]['role'],'code_search')
        self.assertEqual(Continuation(self.root).plan()['status'],'exhausted')


if __name__=='__main__':unittest.main()
