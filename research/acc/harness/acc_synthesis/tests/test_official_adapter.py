"""Real frozen verifier controls. These are not new challenge discoveries."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from acc_synthesis.official_checker import ROOT, check, load_kernel, render


class OfficialAdapterTests(unittest.TestCase):
    def candidate(self):
        _,specs,_,challenges=load_kernel()
        c=challenges['ac-00005']
        saved=json.loads((ROOT/'integration/recovered_routes.json').read_text())
        moves=min((r['moves'] for r in saved['routes'] if r['row_id']=='ac-00005'),key=len)
        return {'row_id':'ac-00005','track':'AC','start':render(c['initial_relators']),
                'moves':moves,'ruleset_sha256':specs.get('ac-r2-v1').move_spec_hash.removeprefix('sha256:')}

    def test_real_saved_tie_is_verified_with_official_certificate(self):
        verdict=check(self.candidate())
        self.assertTrue(verdict['valid'])
        self.assertEqual(verdict['cost'],27)
        self.assertEqual(verdict['exact_endpoint'],['x','y'])
        self.assertTrue(verdict['official_verdict']['certificate_hash'].startswith('sha256:'))

    def test_real_checker_rejects_bool_move_without_endpoint_claim(self):
        c=self.candidate();c['moves']=[True]
        verdict=check(c)
        self.assertFalse(verdict['valid'])
        self.assertEqual(verdict['official_verdict']['code'],'E_BAD_MOVE_ID')
        self.assertIsNone(verdict['exact_endpoint'])

    def test_case_changed_real_start_is_rejected(self):
        c=self.candidate();c['start'][0]=c['start'][0].swapcase()
        with self.assertRaisesRegex(ValueError,'starting presentation'):
            check(c)
