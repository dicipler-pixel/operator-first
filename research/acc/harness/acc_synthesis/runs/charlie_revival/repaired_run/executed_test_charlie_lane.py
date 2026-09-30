import sys
import time
import unittest
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


if __name__ == '__main__':
    unittest.main()
