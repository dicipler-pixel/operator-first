import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import eyes

L = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}
def w(s): return tuple(L[c] for c in s if c in L)


class TestConventions(unittest.TestCase):
    """Values below were produced by exact replay under the official kernel and match Grok's reports."""
    def test_hab_signed_perm_matches_all_reported_values(self):
        cases = [  # (r0, r1, expected hab, expected foxA)
            (w("YxyxYXY"), w("yXXyxxxYX"), 2, 3),                                     # ac-00008 T16
            (w("YYxyxYX"), w("YXyXXyxxx"), 2, 5),                                     # ac-00008 official start
            (w("XYYYxyyX"), w("yxxyXyx"), 5, 5),                                      # ac-00162 plateau
            (w("XXYxYXXYx"), w("YYxxyXyxxYYXyyyxyyy"), 10, 0),                        # ac-00162 P162-H0
            (w("YYYYYYYxxxxYXyXXyXyxyxYXYXyXXyxxxyyyy"), w("xxxxYXyXXyX"), 0, 0),      # ac-00008 T48
        ]
        for r0, r1, h, f in cases:
            self.assertEqual(eyes.hab((r0, r1)), h, (r0, r1))
            self.assertEqual(eyes.foxA((r0, r1)), f, (r0, r1))

    def test_identity_distance_would_be_wrong(self):
        s = (w("XYYYxyyX"), w("yxxyXyx"))  # ac-00162 plateau: identity-distance gives 7, Grok reports 5
        m = eyes.exponent_matrix(s)
        ident = abs(m[0][0]-1)+abs(m[0][1])+abs(m[1][0])+abs(m[1][1]-1)
        self.assertEqual(ident, 7); self.assertEqual(eyes.hab(s), 5)

    def test_target_is_zero(self):
        self.assertEqual(eyes.hab(((1,), (2,))), 0); self.assertEqual(eyes.foxA(((1,), (2,))), 0)


class TestEvents(unittest.TestCase):
    def test_t48_to_t16_pattern(self):
        vecs = [{"tot": 48, "hab": 0, "foxA": 0}, {"tot": 46, "hab": 1, "foxA": 2}, {"tot": 16, "hab": 2, "foxA": 3}]
        names = [e for _, e in eyes.events(vecs)]
        self.assertIn("HAB_EXIT", names); self.assertIn("FOXA_EXIT", names); self.assertIn("LENGTH_DROP", names)

    def test_reenter_is_detected(self):
        vecs = [{"tot": 1, "hab": 0, "foxA": 0}, {"tot": 1, "hab": 1, "foxA": 0}, {"tot": 1, "hab": 0, "foxA": 0}]
        names = [e for _, e in eyes.events(vecs)]
        self.assertEqual(names, ["HAB_EXIT", "HAB_REENTER"])

    def test_nondominated(self):
        vecs = [{"tot": 48, "hab": 0, "foxA": 0}, {"tot": 16, "hab": 2, "foxA": 3}, {"tot": 50, "hab": 2, "foxA": 3}]
        self.assertEqual(eyes.nondominated(vecs), [True, True, False])


class TestStartOrbit(unittest.TestCase):
    """Regression for the 2026-09-12 correction: T16 is three conjugations from the
    official ac-00008 start, so eyes that differ between them are coordinate changes."""
    START = (w("YYxyxYX"), w("YXyXXyxxx"))
    T16 = (w("YxyxYXY"), w("yXXyxxxYX"))

    def _apply(self, s, m):
        try:
            from verifier import core
            return core.apply_move(s, m)
        except ImportError:  # local mirror of ac-r2-v1 for the test only
            r0, r1 = s
            inv = lambda w_: tuple(-a for a in reversed(w_))
            red = eyes._free_reduce
            if m == 0: return (inv(r0), r1)
            if m == 1: return (r0, inv(r1))
            if m == 2: return (red(r0 + r1), r1)
            if m == 3: return (red(r0 + inv(r1)), r1)
            if m == 4: return (r0, red(r1 + r0))
            if m == 5: return (r0, red(r1 + inv(r0)))
            g = (1, -1, 2, -2)[(m - 6) % 4]
            return ((red((g,) + r0 + (-g,)), r1) if m <= 9 else (r0, red((g,) + r1 + (-g,))))

    def test_t16_is_in_start_orbit(self):
        s = self.START
        for m in [8, 12, 10]:
            s = self._apply(s, m)
        self.assertEqual(s, self.T16)
        self.assertTrue(eyes.in_start_orbit(self.T16, self.START))
        self.assertEqual(eyes.distance_back(self.T16, self.START, self._apply, 4), 3)

    def test_relator_class_invariant_under_conjugation_and_inversion(self):
        s = self.START
        for m in [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 8, 12]:
            s = self._apply(s, m)
            self.assertEqual(eyes.orbit_signature(s), eyes.orbit_signature(self.START))

    def test_multiplication_leaves_orbit(self):
        s = self._apply(self.START, 2)
        self.assertFalse(eyes.in_start_orbit(s, self.START))
        self.assertEqual(eyes.orbit_vector(s, self.START)["class_changes"], 1)

    def test_collapse_outcome_labels_return_vs_advance(self):
        # T48 -> ... -> T16: the final collapse lands in the start orbit => 'return'
        T48 = (w("YYYYYYYxxxxYXyXXyXyxyxYXYXyXXyxxxyyyy"), w("xxxxYXyXXyX"))
        states = [T48]
        for m in [0, 8, 8, 8, 8, 8, 8, 13, 2, 12, 11, 9, 0, 11, 11, 11, 12, 3, 10]:
            states.append(self._apply(states[-1], m))
        self.assertEqual(states[-1], self.T16)
        outcomes = eyes.collapse_outcome(states, self.START)
        self.assertEqual(outcomes[-1][1], "return")
        self.assertTrue(all(o == "advance" for _, o in outcomes[:-1]))

    def test_grok_vocabulary_on_noff9(self):
        """Grok's 2026-09-12 briefing: Noff-9 is an r0-only escape; T16 is on-orbit at both levels."""
        s = self.START
        for m in [2, 10, 2, 12, 8, 8, 8, 12, 12]:
            s = self._apply(s, m)
        self.assertEqual(len(eyes.core(s[0])), 25)
        self.assertEqual(len(eyes.core(s[1])), 9)
        self.assertEqual(eyes.conj_sig(s[1]), eyes.conj_sig(self.START[1]))   # rotation of start r1
        self.assertEqual(eyes.orbit_flags(s, self.START, "conj"), {"r0_off": True, "r1_off": False, "pair_off": True})
        self.assertEqual(eyes.lane(s, self.START), "r0-only")
        self.assertEqual(eyes.orbit_flags(self.T16, self.START, "conj"), {"r0_off": False, "r1_off": False, "pair_off": False})
        self.assertEqual(eyes.lane(self.T16, self.START), "padding")

    def test_conj_level_is_finer_than_invconj(self):
        s = self._apply(self.START, 0)  # invert r0: off at conj level, on at invconj level
        self.assertTrue(eyes.orbit_flags(s, self.START, "conj")["r0_off"])
        self.assertFalse(eyes.orbit_flags(s, self.START, "invconj")["r0_off"])

    def test_checkpoint_has_three_flags_at_both_levels(self):
        c = eyes.checkpoint(self.T16, self.START, self._apply, radius=4)
        for lvl in ("conj", "invconj"):
            self.assertEqual(set(c[lvl]), {"r0_off", "r1_off", "pair_off"})
        self.assertEqual(c["return_distance"], 3)
        self.assertEqual(c["lane"], "padding")

    def test_cancellation_eye_frozen_values(self):
        """Pinned to the acc-collab implementation (83724f1); checked equal on 1,380 random states."""
        self.assertEqual(eyes.cancellation_eye(self.START), {"k": 3, "surplus": -1, "cyclic_tot": 16, "floor": 17})
        T48 = (w("YYYYYYYxxxxYXyXXyXyxyxYXYXyXXyxxxyyyy"), w("xxxxYXyXXyX"))
        self.assertEqual(eyes.cancellation_eye(T48)["floor"], 29)
        ak3 = (w("YXYxyx"), w("YYYYxxx"))  # ac-00399
        self.assertEqual(eyes.cancellation_eye(ak3), {"k": 2, "surplus": -2, "cyclic_tot": 13, "floor": 15})

    def test_holdout_first_ply_products_rank_above_padding(self):
        ak3 = (w("YXYxyx"), w("YYYYxxx"))
        floors = {m: eyes.cancellation_eye(self._apply(ak3, m))["floor"] for m in range(14)}
        self.assertTrue(all(floors[m] == 13 for m in (2, 3, 4, 5)))
        self.assertTrue(all(floors[m] == 15 for m in range(14) if m not in (2, 3, 4, 5)))
        m5 = self._apply(ak3, 5)
        self.assertEqual((eyes.total(m5), eyes.hab(m5), eyes.lane(m5, ak3)), (17, 5, "r1-only"))


if __name__ == "__main__":
    unittest.main()
