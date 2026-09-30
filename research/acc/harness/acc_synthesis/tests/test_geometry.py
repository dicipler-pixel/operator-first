import unittest
from acc_synthesis.geometry import diagnostics

class GeometryTests(unittest.TestCase):
    def test_normal_operator_can_cross_projector(self):
        d=diagnostics([[0,0],[0,1]],[[.5,.5],[.5,.5]])
        self.assertEqual(d['commutator_squared'],0)
        self.assertGreater(d['projector_mixing_squared'],0)

    def test_preserved_projector_can_have_nonnormal_operator(self):
        d=diagnostics([[1,1,0],[0,1,0],[0,0,2]],[[1,0,0],[0,1,0],[0,0,0]])
        self.assertEqual(d['projector_mixing_squared'],0)
        self.assertGreater(d['commutator_squared'],0)

    def test_reject_nonprojector(self):
        with self.assertRaises(ValueError): diagnostics([[1,0],[0,1]],[[2,0],[0,0]])
