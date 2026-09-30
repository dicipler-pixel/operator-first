import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from acc_synthesis.harness import ROOT, atomic_json, digest
from acc_synthesis.helper_batch import HelperContinuation
from acc_synthesis.helpers.negative_equivalences import validated_keys


class NegativeEquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.ledger=json.loads((ROOT/'continuation/negative_equivalences.json').read_text())
        self.entry=self.ledger['closures'][0]
        source_cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
        keys={self.entry['donor_attempt_key'],self.entry['union_attempt_key']}
        self.cp={'attempts':[a for a in source_cp['attempts'] if a['key'] in keys]}
        paths=['continuation/negative_equivalences.json',self.entry['donor_source_archive']]
        for a in self.cp['attempts']:
            paths.append(a['result_path'])
            r=json.loads((ROOT/a['result_path']).read_text())
            paths.extend(e['path'] for e in r['evidence'] if Path(e['path']).name in
                         {'coverage.json','saved_union.json','executed_bob_lane_v1.py'})
        for name in paths:
            dest=self.root/name;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,dest)

    def keys(self):
        return validated_keys(self.root,self.cp,HelperContinuation.search_identity,digest)

    def rewrite_evidence(self, attempt_key, name, change):
        a=next(a for a in self.cp['attempts'] if a['key']==attempt_key)
        r=json.loads((self.root/a['result_path']).read_text())
        e=next(e for e in r['evidence'] if Path(e['path']).name==name)
        p=self.root/e['path'];d=json.loads(p.read_text());change(d);atomic_json(p,d)
        e['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        p=self.root/a['result_path'];atomic_json(p,r)
        a['result_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()

    def test_candidate_run_can_prove_no_transfer_without_inventing_a_miss(self):
        before=json.dumps(self.cp,sort_keys=True)
        self.assertEqual(self.keys(),{self.entry['job']['key']})
        self.assertEqual(json.dumps(self.cp,sort_keys=True),before)
        donor=next(a for a in self.cp['attempts'] if a['key']==self.entry['donor_attempt_key'])
        self.assertEqual(donor['kind'],'candidate')

    def test_new_seed_or_donor_input_remains_eligible(self):
        closed=self.keys()
        for field in ('seed_sha256','inputs'):
            j=dict(self.entry['job'])
            j[field]='new-seed' if field=='seed_sha256' else {'donor.json':'new-input'}
            self.assertNotIn(HelperContinuation.search_identity(j),closed)

    def test_damaged_evidence_is_rejected(self):
        a=next(a for a in self.cp['attempts'] if a['key']==self.entry['donor_attempt_key'])
        r=json.loads((self.root/a['result_path']).read_text())
        p=self.root/next(e['path'] for e in r['evidence'] if Path(e['path']).name=='coverage.json')
        p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            self.keys()

    def test_partial_donor_pass_cannot_close_job_even_with_rehashed_fixture(self):
        self.rewrite_evidence(self.entry['donor_attempt_key'],'coverage.json',
                             lambda c:c.update(termination_reason='node_cap'))
        with self.assertRaisesRegex(ValueError,'complete zero-match'):
            self.keys()

    def test_shorter_union_cannot_close_job_even_with_rehashed_fixture(self):
        def shortcut(s):
            s['edges'].append([s['states'].index(s['start']),0,s['states'].index(s['target'])])
        self.rewrite_evidence(self.entry['union_attempt_key'],'saved_union.json',shortcut)
        with self.assertRaisesRegex(ValueError,'may still improve'):
            self.keys()


if __name__=='__main__':
    unittest.main()
