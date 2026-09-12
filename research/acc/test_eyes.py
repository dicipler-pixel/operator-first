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


if __name__ == "__main__":
    unittest.main()
