import hashlib,json,tempfile,unittest
from pathlib import Path
from acc_synthesis.helpers.audit_artifacts import audit_all
from acc_synthesis.runtime import Store


class ArtifactAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'continuation').mkdir()
        self.artifact=self.root/'graph.gz';self.artifact.write_bytes(b'archive-fixture')
        result={'kind':'bounded_miss','evidence':[{'path':'graph.gz','sha256':hashlib.sha256(self.artifact.read_bytes()).hexdigest()}]}
        self.result=self.root/'result.json';self.result.write_text(json.dumps(result))
        self.cp={'attempts':[{'key':'fixture','kind':'bounded_miss','result_path':'result.json','result_sha256':hashlib.sha256(self.result.read_bytes()).hexdigest()}]}
        (self.root/'continuation/checkpoint.json').write_text(json.dumps(self.cp))

    def test_truncated_artifact_blocks_persistence_without_rewriting_history(self):
        self.assertEqual(audit_all(self.root)['unique_artifacts_checked'],2)
        before=(self.root/'continuation/checkpoint.json').read_bytes()
        self.artifact.write_bytes(self.artifact.read_bytes()[:-3])
        with self.assertRaisesRegex(ValueError,'Completed evidence hash mismatch'):
            audit_all(self.root,sync=True)
        self.assertEqual((self.root/'continuation/checkpoint.json').read_bytes(),before)

    def test_stale_completed_task_lease_blocks_persistence(self):
        store=Store(self.root/'state/ledger.sqlite3')
        task=store.enqueue('code_search',{'key':'fixture'},'code:fixture','row')
        lease=store.claim('code_search',task_id=task)
        with self.assertRaisesRegex(ValueError,'conflicts with local task'):
            audit_all(self.root,sync=True)
        store.finish(task,lease['token'],{'kind':'bounded_miss'})
        self.assertEqual(audit_all(self.root,sync=True)['status'],'verified')
