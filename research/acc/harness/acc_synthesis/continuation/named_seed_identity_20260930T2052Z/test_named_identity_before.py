import copy
import json
from pathlib import Path
import unittest
from helper_batch import HelperContinuation

ROOT=Path(__file__).resolve().parents[1]

class NamedIdentityTests(unittest.TestCase):
    def test_other_rows_and_prose_cannot_change_probe_identity(self):
        query={'type':'paid_prefix','moves':[1,2], 'expected_state':['x','y'],'note':'old prose'}
        job={'helper':'named','row_id':'ac-00013','inputs':{'helpers/named_queries.json':'old-file','graph':'same'},
             'key':'ignored','method_sha256':'old-source','query_identity':HelperContinuation.named_query_identity(query)}
        changed=copy.deepcopy(job);changed['inputs']['helpers/named_queries.json']='other-row-edited'
        changed['method_sha256']='cosmetic-source';query['note']='new prose'
        changed['query_identity']=HelperContinuation.named_query_identity(query)
        self.assertEqual(HelperContinuation.search_identity(job),HelperContinuation.search_identity(changed))
        query['moves']=[1,3];changed['query_identity']=HelperContinuation.named_query_identity(query)
        self.assertNotEqual(HelperContinuation.search_identity(job),HelperContinuation.search_identity(changed))

    def test_legacy_completed_named_probes_stay_closed(self):
        c=HelperContinuation(ROOT)
        before=json.loads(c.path.read_text())
        self.assertEqual(sum(a.get('job',{}).get('helper')=='named' for a in before['attempts']),5)
        self.assertFalse(any(j['helper']=='named' for j in c.jobs()))
        self.assertEqual(json.loads(c.path.read_text()),before)

if __name__=='__main__':unittest.main()
