import unittest
from unittest.mock import patch
import bridge_search as bridge
import official_checker


class BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core, _, _, cls.challenges = official_checker.load_kernel()

    def test_saved_union_exact_edges_and_inverse(self):
        start = ((1,), (2,))
        moves = [6, 8, 9, 7]
        graph, traces, prefix, suffix = bridge.saved_union(self.core, start, start, [{'moves': moves}])
        self.assertEqual(prefix[start], [])
        for state, edges in graph.items():
            for dest, move in edges:
                self.assertEqual(self.core.apply_move(state, move), dest)
                self.assertIn((state, self.core.INVERSE_MOVE[move]), graph[dest])
        for state, path in suffix.items():
            self.assertEqual(bridge.replay_states(self.core, state, path)[-1], start)

    def test_exact_order_and_word_rotation_are_not_normalized(self):
        a = ((1,2), (2,1))
        b = ((2,1), (1,2))
        graph, _, _, _ = bridge.saved_union(self.core, a, b, [])
        self.assertEqual(len(graph), 2)

    def test_fresh_bidirectional_route_reconstruction(self):
        goal = ((1,), (2,))
        start = self.core.apply_move(self.core.apply_move(goal, 2), 8)
        best, coverage = bridge.bounded_bridge(self.core, {start: []}, {goal: []}, None,
            wall_seconds=2, node_cap=10000, depth=4, target_length=2, stop_check=lambda:False)
        self.assertIsNotNone(best)
        self.assertLessEqual(len(best), 2)
        self.assertEqual(bridge.replay_states(self.core, start, best)[-1], goal)
        self.assertEqual(coverage['termination_reason'], 'target_found')
        self.assertGreater(coverage['generated_moves'], 0)

    def test_real_node_cap(self):
        start, goal = ((1,2,1), (2,1,2)), ((1,), (2,))
        best, coverage = bridge.bounded_bridge(self.core, {start: []}, {goal: []}, None,
            wall_seconds=2, node_cap=3, depth=4, stop_check=lambda:False)
        self.assertIsNone(best)
        self.assertEqual(coverage['admitted_records'], 3)
        self.assertEqual(coverage['termination_reason'], 'node_cap')

    def test_honors_stop(self):
        state = ((1,), (2,))
        _, coverage = bridge.bounded_bridge(self.core, {state: []}, {state: []}, [],
            wall_seconds=2, node_cap=100, depth=2, stop_check=lambda:True)
        self.assertEqual(coverage['termination_reason'], 'controller_stopped')
        self.assertEqual(coverage['generated_moves'], 0)


if __name__ == '__main__':
    unittest.main()
