"""Regression tests for the FrontierMath (ell=3, r=9) Python lane.

    python3 -m unittest discover -s research/frontiermath

The class-group engine is validated against the classical table of class
numbers and against the group axioms, because a silently wrong composition
would poison every downstream 3-rank.
"""

import os
import sys
import unittest
from itertools import product
from random import Random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bqf_class_group_v1 as B
import f3_witness_v1 as F

CLASS_NUMBERS = {
    -3: 1, -4: 1, -7: 1, -8: 1, -11: 1, -15: 2, -19: 1, -20: 2, -23: 3,
    -24: 2, -31: 3, -35: 2, -39: 4, -40: 2, -43: 1, -47: 5, -52: 2, -55: 4,
    -56: 4, -59: 3, -67: 1, -71: 7, -79: 5, -83: 3, -84: 4, -87: 6, -88: 2,
    -91: 2, -95: 8, -103: 5, -104: 6, -107: 3, -111: 8, -163: 1, -199: 9,
    -203: 4, -227: 5, -239: 15, -283: 3,
}


class TestClassGroupEngine(unittest.TestCase):
    def test_class_numbers_match_the_classical_table(self):
        for D, h in CLASS_NUMBERS.items():
            self.assertEqual(B.class_number(D), h, f"h({D})")

    def test_reduction_is_idempotent_and_discriminant_preserving(self):
        for D in range(-3, -400, -1):
            if D % 4 not in (0, 1):
                continue
            for f in B.reduced_forms(D):
                self.assertTrue(B.is_reduced(f))
                self.assertEqual(B.disc(f), D)
                self.assertEqual(B.reduce_form(f), f)

    def test_group_axioms(self):
        rng = Random(4)
        for D in range(-3, -260, -1):
            if D % 4 not in (0, 1):
                continue
            forms = B.reduced_forms(D)
            e = B.principal_form(D)
            self.assertIn(e, forms)
            for f in forms:
                self.assertEqual(B.compose(e, f), f)
                inv = B.reduce_form((f[0], -f[1], f[2]))
                self.assertEqual(B.compose(f, inv), e)
                self.assertIn(B.compose(f, rng.choice(forms)), forms)
            for _ in range(8):
                x, y, z = (rng.choice(forms) for _ in range(3))
                self.assertEqual(B.compose(B.compose(x, y), z),
                                 B.compose(x, B.compose(y, z)))

    def test_element_orders_divide_the_class_number(self):
        for D in (-23, -47, -71, -87, -95, -199, -239):
            h = B.class_number(D)
            for f in B.reduced_forms(D):
                self.assertEqual(h % B.order_of(f), 0)

    def test_engine_refuses_discriminants_it_cannot_honestly_enumerate(self):
        with self.assertRaises(ValueError):
            B.reduced_forms(-217541503961543485618350976479)


class TestControls(unittest.TestCase):
    def test_control_c0(self):
        D, f = -23, (2, 1, 3)
        self.assertEqual(B.disc(f), D)
        self.assertTrue(B.is_reduced(f))
        self.assertEqual(B.class_number(D), 3)
        self.assertEqual(B.order_of(f), 3)
        _, r = B.three_torsion(D)
        self.assertEqual(r, 1)

    def test_control_c1_invariant_factors(self):
        D = -3321607
        self.assertEqual(B.class_number(D), 567)
        _, r = B.three_torsion(D)
        self.assertEqual(r, 3)
        self.assertEqual(max(B.element_orders(D).values()), 63)

    def test_elkies_constants(self):
        d16 = 72513834653847828539450325493
        self.assertEqual(-3 * d16, -217541503961543485618350976479)
        m = 908800736629952526116772283648363
        self.assertEqual(2195745961 * 413891567044514092637683, m)
        self.assertEqual(27 * m, 24537619889008718205152851658505801)
        self.assertEqual(3 * m, 2726402209889857578350316850945089)
        self.assertEqual(m % 4, 3)
        self.assertNotEqual(m % 3, 0)


class TestF3Witness(unittest.TestCase):
    def test_the_three_way_equivalence(self):
        rng = Random(11)
        space = list(product(range(3), repeat=4))
        for _ in range(400):
            W = [rng.choice(space) for _ in range(rng.randrange(0, 4))]
            g = rng.choice(space)
            inc = F.rank_increment(W, g)
            chi = F.separating_dual(W, g)
            self.assertEqual(inc == 0, chi is None)
            if chi is not None:
                v = F.verify_separation(W, g, chi)
                self.assertTrue(v["chi_kills_W"])
                self.assertEqual(v["chi_of_g"], 1)
                self.assertEqual(v["augmented_rank"], v["old_span_rank"] + 1)

    def test_transport_conserves_the_pairing(self):
        rng = Random(12)
        n = 5
        for _ in range(200):
            while True:
                T = [tuple(rng.randrange(3) for _ in range(n)) for _ in range(n)]
                if F.inverse(T) is not None:
                    break
            chi = tuple(rng.randrange(3) for _ in range(n))
            v = tuple(rng.randrange(3) for _ in range(n))
            self.assertEqual(F.dot(F.transport_dual(chi, T), F.matvec(T, v)),
                             F.dot(chi, v))

    def test_transport_cannot_make_an_old_direction_look_new(self):
        rng = Random(13)
        n = 5
        for _ in range(150):
            while True:
                T = [tuple(rng.randrange(3) for _ in range(n)) for _ in range(n)]
                if F.inverse(T) is not None:
                    break
            W = [tuple(rng.randrange(3) for _ in range(n)) for _ in range(2)]
            g = tuple(rng.randrange(3) for _ in range(n))
            self.assertEqual(
                F.rank_increment(W, g),
                F.rank_increment([F.matvec(T, w) for w in W], F.matvec(T, g)))

    def test_the_full_sweep_both_ways(self):
        ident = [tuple(1 if i == j else 0 for j in range(9)) for i in range(9)]
        ok = F.independence_sweep(ident, expect_order=19683)
        self.assertEqual(ok["combinations_checked"], 19683)
        self.assertEqual(ok["subgroup_order"], 19683)
        self.assertTrue(ok["independent"])
        dep = ident[:8] + [tuple((ident[0][i] + ident[1][i]) % 3 for i in range(9))]
        bad = F.independence_sweep(dep)
        self.assertFalse(bad["independent"])
        self.assertEqual(bad["subgroup_order"], 3 ** 8)
        self.assertIsNotNone(bad["first_nontrivial_relation"])

    def test_odd_dimensional_alternating_form_has_a_radical(self):
        n = 9
        M = [[0] * n for _ in range(n)]
        for i in range(0, n - 1, 2):
            M[i][i + 1] = 1
            M[i + 1][i] = 2                    # 2 == -1 in F3
        M = [tuple(r) for r in M]
        rep = F.skew_adjoint_report(F.identity(n), M)
        self.assertTrue(rep["B_alternating"])
        self.assertEqual(rep["rank_B"] % 2, 0)
        self.assertGreaterEqual(rep["radical_dimension"], 1)


if __name__ == "__main__":
    unittest.main()
