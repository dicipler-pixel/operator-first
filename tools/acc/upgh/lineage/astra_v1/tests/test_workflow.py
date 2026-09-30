import copy
import json
from pathlib import Path
import tempfile
import unittest
from acc_synthesis.demo import prepare_demo
from acc_synthesis.harness import Harness,read_json

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.work=prepare_demo(self.root)
        self.h=Harness(self.root/'config.json',self.root/'state')

    def test_failure_switch_review_exact_gate_end_to_end(self):
        self.h.add(self.work);status=self.h.run()
        self.assertEqual(status['tasks'],{'completed':6})
        self.assertEqual([t['role'] for t in self.h.store.tasks()],
                         ['luna_memory','sol_builder','astra_advisor','luna_memory','sol_builder','sol_checker'])
        results=list((self.root/'state'/'demo_results').glob('*.json'))
        self.assertEqual(len(results),1)
        self.assertEqual(read_json(results[0])['gate']['status'],'verified_scoring')
        self.assertFalse((self.root/'state'/'ready').exists())
        self.h.reconcile();self.assertEqual(len(self.h.store.tasks()),6)
        self.assertTrue(any(x['kind']=='memory.parked' for x in self.h.memory()))

    def test_cosmetic_switch_does_not_dispatch_new_family(self):
        self.h.add(self.work)
        task=self.h.store.claim();payload=task['payload']
        self.h.store.finish(task['id'],task['token'],{'kind':'context','summary':'fixture','evidence':[]})
        advisor=self.h.store.enqueue('astra_advisor',payload,'manual-advisor',family=payload['row_id'])
        task=self.h.store.claim(role='astra_advisor')
        result={'kind':'proposal','summary':'cosmetic','strategy':{**payload['strategy'],'beam':999},
                'evidence':[],'discriminating_test':'none'}
        self.h.store.finish(task['id'],task['token'],result);self.h.reconcile()
        events=[e for e in self.h.memory() if e['kind']=='memory.parked']
        self.assertEqual(events[-1]['payload']['reason'],'no_supported_switch')

    def test_reopen_matches_event_and_preserves_negative(self):
        self.h.add(self.work);self.h.run()
        ref={'path':'fixture_observation.json','sha256':__import__('hashlib').sha256((self.root/'fixture_observation.json').read_bytes()).hexdigest()}
        self.assertEqual(self.h.wake({'event':'unrelated','row_id':'DEMO-ONLY','evidence':[ref]}),0)
        self.assertEqual(self.h.wake({'event':'verified_bridge','row_id':'DEMO-ONLY','evidence':[ref]}),1)
        self.assertEqual(len(self.h.store.tasks('queued')),1)
        self.h.wake({'event':'verified_bridge','row_id':'DEMO-ONLY','evidence':[ref]})
        self.assertEqual(len(self.h.store.tasks('queued')),1)

    def test_stop_persists_and_prevents_dispatch(self):
        self.h.add(self.work);self.h.store.stop('operator stop')
        restarted=Harness(self.root/'config.json',self.root/'state')
        self.assertEqual(restarted.run()['processed_tasks'],0)
        self.assertTrue(restarted.status()['stopped'])

    def test_bad_evidence_and_bad_strategy_rejected_without_crash(self):
        self.h.add(self.work);task=self.h.store.claim()
        with self.assertRaises(ValueError):
            self.h.accept(task['id'],task['token'],{'kind':'context','summary':'fake','evidence':[{'path':'absent','sha256':'0'*64}]})

