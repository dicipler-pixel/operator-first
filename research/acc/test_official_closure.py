"""Regression: the independent official-kernel closure engine reproduces the
first ac-00015 well. Requires a checkout of SAIRcompetition/andrews-curtis;
skips cleanly when it is absent so the suite stays runnable everywhere.

Run: SAIR_REPO=/path/to/andrews-curtis python3 -m unittest research/acc/test_official_closure.py
"""

import os
import sys
import unittest
from pathlib import Path

SAIR = Path(os.environ.get("SAIR_REPO", "/home/user/saircompetition/andrews-curtis"))
TOOLS = SAIR / "competition" / "tools"


@unittest.skipUnless((TOOLS / "verifier" / "core.py").exists(), "official SAIR verifier not available")
class TestOfficialClosure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(TOOLS))
        sys.path.insert(0, str(Path(__file__).parent))
        import official_closure  # noqa: E402
        cls.oc = official_closure

    def test_ac00015_first_well_cap26(self):
        """LENGTH_WELL_STATUS.md: cap-26 component closes at 105,912, no descent."""
        start = [[-2, -1, 2, -1, -2, 1, 2, -1, 2, 1], [-2, -2, 1, -2, 1, -2, 1, -2, 1, 2, 1]]
        size, min_len, closed, census = self.oc.closure(start, 26)
        self.assertTrue(closed)
        self.assertEqual(size, 105912)
        self.assertEqual(min_len, 21)
        self.assertEqual(census[21], 1760)

    def test_ac00015_first_well_escapes_at_27(self):
        """The +6 well depth is exact: cap 27 must admit a descent to length 20."""
        start = [[-2, -1, 2, -1, -2, 1, 2, -1, 2, 1], [-2, -2, 1, -2, 1, -2, 1, -2, 1, 2, 1]]
        _, min_len, closed, _ = self.oc.closure(start, 27)
        self.assertTrue(closed)
        self.assertEqual(min_len, 20)

    def test_key_is_injective_on_small_sample(self):
        from verifier import core
        s = ((1,), (2,))
        seen = {}
        frontier = [s]
        for _ in range(4):
            nxt = []
            for st in frontier:
                for m in range(14):
                    t = core.apply_move(st, m)
                    k = self.oc.key(t)
                    if k in seen:
                        self.assertEqual(seen[k], t, "key collision")
                    else:
                        seen[k] = t
                        nxt.append(t)
            frontier = nxt
        self.assertEqual(len(seen), 5115)  # cumulative radius-4 basin (target re-entered via inverse moves)


if __name__ == "__main__":
    unittest.main()
