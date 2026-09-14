"""Deliberately damaged controls: prove each detector fires before trusting a clean run.

A detector that has only ever returned zero is indistinguishable from a
detector that cannot return anything else.

    python3 tools/acc/test_governance_v1.py
"""
import sys, tempfile, unittest
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from event_log_v1 import EventLog                                    # noqa: E402
from eye_governance_v1 import duplicates, leakage, sweep, rank       # noqa: E402


class TestDamagedControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_duplicate_eyes_are_caught(self):
        for i in range(4):
            for eye in ("panel-a", "panel-b"):          # byte-identical twins
                self.log.eye_reading("t", "c", eye, "observed",
                                     item_id="c", output={"v": i})
            self.log.eye_reading("t", "c", "panel-c", "observed",
                                 item_id="c", output={"v": i * 7})
        found = duplicates(self.log)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][1], ["panel-a", "panel-b"])

    def test_a_leaking_eye_is_caught(self):
        """The v4.1 defect, structurally: output is a bijection of the answer."""
        for i in range(5):
            self.log.eye_reading("t", "c", "answer", "observed",
                                 item_id="c", output={"y": i})
            self.log.eye_reading("t", "c", "leaker", "observed",
                                 item_id="c", output={"y": i})      # reads the answer
            self.log.eye_reading("t", "c", "honest", "observed",
                                 item_id="c", output={"y": i % 2})  # genuinely coarser
        found = leakage(self.log)
        eyes = {e for _, e in found}
        self.assertIn("leaker", eyes, "an eye reading the answer must be caught")
        self.assertNotIn("honest", eyes, "a coarser eye is not leakage")

    def test_an_eye_that_never_observes_is_auto_disabled(self):
        for i in range(4):
            self.log.eye_reading("t", "c", "never-sees", "blocked",
                                 item_id="c", reason="no input")
            self.log.eye_reading("t", "c", "works", "observed",
                                 item_id="c", output={"v": i})
        found = sweep(self.log, threshold=3)
        eyes = {e for (_, e), _, _ in found}
        self.assertEqual(eyes, {"never-sees"})

    def test_the_sweep_files_a_reason_and_keeps_the_eye(self):
        for _ in range(3):
            self.log.eye_reading("t", "c", "stuck", "blocked",
                                 item_id="c", reason="needs Sage")
        sweep(self.log, apply=True, threshold=3)
        rows = [r["body"] for _, r, _ in self.log.read()
                if r and r["kind"] == "eye-reading" and r["body"]["eye_id"] == "stuck"]
        self.assertEqual(len(rows), 4, "the disable is appended, not substituted")
        self.assertEqual(rows[-1]["state"], "disabled")
        self.assertIn("needs Sage", rows[-1]["reason"])
        self.assertEqual([r["state"] for r in rows[:3]], ["blocked"] * 3,
                         "the original filings must be untouched")

    def test_ranking_reproduces_the_measured_ab(self):
        """Computed from invariance and cost alone; the A/B is not an input."""
        rows = rank("search")
        order = [e for _, e, *_ in rows]
        self.assertLess(order.index("displacement-gram"),
                        order.index("twisted-determinant"),
                        "the ranking must predict the arm that actually won")
        gram = next(r for r in rows if r[1] == "displacement-gram")[0]
        tau = next(r for r in rows if r[1] == "twisted-determinant")[0]
        self.assertGreater(gram / max(tau, 1e-9), 100,
                           "the measured gap was decisive; the ranking should say so")

    def test_ranking_is_per_use_not_per_eye(self):
        a = {e: s for s, e, *_ in rank("search")}
        b = {e: s for s, e, *_ in rank("conjugacy-only")}
        self.assertNotEqual(a["displacement-gram"], b["displacement-gram"],
                            "an eye's rank must change with the use")


if __name__ == "__main__":
    unittest.main(verbosity=1)
