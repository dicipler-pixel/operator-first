"""Tests for the Compound Eye run ledger: recorder and checker.

    python3 -m unittest tools.acc.test_mixer_log_v1
    python3 tools/acc/test_mixer_log_v1.py
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import mixer_trace_v1 as T  # noqa: E402

RECORDER = ROOT / "tools" / "acc" / "mixer_log_v1.js"


def run_recorder(runs, ledger_dir):
    """Record runs into a scratch ledger by pointing the recorder at a temp root."""
    payload = json.dumps(runs if isinstance(runs, list) else [runs])
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        fh.write(payload)
        p = fh.name
    env = {"PATH": "/usr/bin:/bin:/usr/local/bin"}
    return subprocess.run(["node", str(RECORDER), "record", p],
                          cwd=ROOT, capture_output=True, text=True, env=env)


BASE = {
    "lane": "testlane",
    "run_id": "case",
    "claim": "a falsifiable sentence",
    "evidence": "computation",
    "status": "verified",
}


class TestRecorderValidation(unittest.TestCase):
    """The recorder must refuse malformed runs rather than record them."""

    def _expect_failure(self, run, needle):
        res = run_recorder(run, None)
        self.assertNotEqual(res.returncode, 0, f"should have failed: {run}")
        self.assertIn(needle, res.stderr, res.stderr)

    def test_missing_required_field(self):
        bad = dict(BASE)
        del bad["claim"]
        self._expect_failure(bad, "missing required field: claim")

    def test_unknown_evidence_class(self):
        self._expect_failure({**BASE, "evidence": "vibes"}, "evidence must be one of")

    def test_unknown_status(self):
        self._expect_failure({**BASE, "status": "probably"}, "status must be one of")

    def test_verified_requires_real_evidence(self):
        self._expect_failure({**BASE, "evidence": "none", "status": "verified"},
                             "evidence stronger than none")

    def test_channel_length_must_match_the_coordinate(self):
        bad = {**BASE, "x": [0, 1, 2],
               "channels": [{"id": "c", "unit": "u", "values": [1, 2]}]}
        self._expect_failure(bad, "but the coordinate has")


class TestChecker(unittest.TestCase):
    """Invariants in mixer_trace_v1.check."""

    def test_clean_ledger_passes(self):
        rows = [{**BASE, "mixable": False, "depends_on": []}]
        self.assertEqual(T.check(rows), [])

    def test_verified_with_no_evidence_is_caught(self):
        rows = [{**BASE, "evidence": "none", "mixable": False}]
        self.assertTrue(any("evidence is none" in p for p in T.check(rows)))

    def test_duplicate_id_without_supersedes_is_caught(self):
        rows = [{**BASE, "mixable": False}, {**BASE, "mixable": False}]
        self.assertTrue(any("recorded twice" in p for p in T.check(rows)))

    def test_duplicate_id_with_supersedes_is_allowed(self):
        rows = [{**BASE, "mixable": False},
                {**BASE, "mixable": False, "supersedes": "testlane/case"}]
        self.assertEqual([p for p in T.check(rows) if "recorded twice" in p], [])

    def test_failed_roundtrip_is_caught(self):
        rows = [{**BASE, "mixable": True, "roundtrip_ok": False,
                 "traces_path": "nope.json"}]
        self.assertTrue(any("does not replay" in p for p in T.check(rows)))

    def test_missing_artifact_is_caught(self):
        rows = [{**BASE, "mixable": True, "roundtrip_ok": True,
                 "traces_path": "ledger/mixer/definitely-not-here.json"}]
        self.assertTrue(any("missing from disk" in p for p in T.check(rows)))

    def test_dangling_dependency_is_caught(self):
        rows = [{**BASE, "mixable": False, "depends_on": ["testlane/ghost"]}]
        self.assertTrue(any("not in the ledger" in p for p in T.check(rows)))

    def test_bad_status_and_evidence_are_caught(self):
        rows = [{**BASE, "status": "maybe", "evidence": "hunch", "mixable": False}]
        problems = T.check(rows)
        self.assertTrue(any("bad status" in p for p in problems))
        self.assertTrue(any("bad evidence" in p for p in problems))


class TestLiveLedger(unittest.TestCase):
    """The ledger actually committed in this repo must hold its invariants."""

    def test_committed_ledger_is_clean(self):
        rows = T.load()
        if not rows:
            self.skipTest("ledger not present")
        self.assertEqual(T.check(rows), [])

    def test_every_mixable_run_replays(self):
        for r in T.load():
            if r.get("mixable"):
                self.assertTrue(r.get("roundtrip_ok"), f"{r['lane']}/{r['run_id']}")

    def test_claim_only_runs_have_no_fabricated_coordinate(self):
        for r in T.load():
            if not r.get("mixable"):
                self.assertIsNone(r.get("traces_path"))
                self.assertNotIn("coordinate", r)


if __name__ == "__main__":
    unittest.main()
