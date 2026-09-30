import sys
import time
import unittest
import json
import tempfile
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'helpers'))
sys.path.insert(0, str(ROOT))
import charlie_lane_v1 as lane
from vendor.verifier import core


class CharlieLaneTests(unittest.TestCase):
    def test_goal_ball_and_ordered_route(self):
        goal = ((1,), (2,))
        # An inverse move produces an independently checkable nontrivial start.
        start = core.apply_move(goal, 2)
        route, coverage = lane.exact_cap(start, goal, 5, 2, 100000,
                                          time.monotonic() + 15, 1024, 3)
        state = start
        for move in route:
            state = core.apply_move(state, move)
        self.assertEqual(state, goal)
        self.assertEqual(len(route), 1)
        self.assertEqual(coverage['termination_reason'], 'candidate_found')

    def test_partial_layer_never_closed(self):
        start = ((1, 2), (2, 1))
        goal = ((1,), (2,))
        route, coverage = lane.exact_cap(start, goal, 8, 3, 3,
                                          time.monotonic() + 15, 1024, 8)
        self.assertIsNone(route)
        self.assertEqual(coverage['termination_reason'], 'node_cap')
        self.assertFalse(coverage['complete_under_cap'])
        self.assertIsNotNone(coverage['partial_layer'])

    def test_unseeded_row_reaches_bounded_search_with_absent_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'continuation').mkdir()
            (root / 'continuation/routes.json').write_text('{"routes":[]}')
            report = {'admitted_records': 3, 'complete_under_cap': False,
                      'termination_reason': 'node_cap'}
            with patch.object(lane, 'ROOT', root), patch.object(lane, 'address_limit'), patch.object(lane, 'exact_cap', return_value=(None, report)) as search:
                lane.main(['--row', 'ac-00001', '--output-dir', str(root / 'run'), '--node-cap', '3'])
            self.assertEqual(search.call_count, 1)
            baseline = json.loads((root / 'run/baseline.json').read_text())
            self.assertIsNone(baseline['moves'])
            self.assertIsNone(baseline['official_receipt'])

    def test_wall_budget_cannot_be_increased_or_nan(self):
        for wall in ['181', 'nan']:
            with self.assertRaises(SystemExit):
                lane.main(['--row', 'ac-00001', '--output-dir', 'unused', '--wall-seconds', wall])


if __name__ == '__main__':
    unittest.main()
