"""Tests for the sealed hand-off envelope and the information-preserving eye.

    python3 tools/acc/test_eye_v1.py
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

EYE_LOG = ROOT / "tools" / "acc" / "eye_log_v1.js"
CLAIM = ("a falsifiable sentence long enough to be a real claim")


def node(cmd, arg, eye_dir):
    env = dict(os.environ, ACC_EYE_DIR=str(eye_dir), PATH="/usr/bin:/bin:/usr/local/bin")
    return subprocess.run(["node", str(EYE_LOG), cmd, str(arg)],
                          cwd=ROOT, capture_output=True, text=True, env=env)


def write(tmp, name, payload):
    p = Path(tmp) / name
    p.write_text(json.dumps(payload))
    return p


OBS = {"claim_id": "c", "eye_id": "e1", "verdict": "orthogonal",
       "evidence": "computation", "output": {"n": 1}}


class TestHandoffEnvelope(unittest.TestCase):
    """Damaged, rewritten and self-checked hand-offs must all be refused."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["ACC_HANDOFF_LEDGER"] = str(Path(self.tmp.name) / "h.jsonl")
        for m in list(sys.modules):
            if m == "handoff_v1":
                del sys.modules[m]
        import handoff_v1
        self.H = handoff_v1

    def tearDown(self):
        os.environ.pop("ACC_HANDOFF_LEDGER", None)
        self.tmp.cleanup()

    def _file(self, text):
        p = Path(self.tmp.name) / "artifact.txt"
        p.write_text(text)
        return p

    def test_intact_file_verifies(self):
        p = self._file("x" * 4096)
        env = self.H.seal("claude", CLAIM, "computation", artifact=p)
        v = self.H.verify(env["handoff_id"], "gpt", file=p)
        self.assertEqual(v["result"], "pass")
        self.assertEqual(env["artifact"]["bytes"], 4096)

    def test_truncated_file_is_refused_and_says_how_short(self):
        p = self._file("x" * 4096)
        env = self.H.seal("claude", CLAIM, "computation", artifact=p)
        p.write_text("x" * 953)                      # the Drive failure mode
        v = self.H.verify(env["handoff_id"], "gpt", file=p)
        self.assertEqual(v["result"], "fail")
        self.assertEqual(v["status"], "damaged-in-transit")
        self.assertIn("short by 3143", v["failure_reason"])

    def test_same_size_different_bytes_is_still_refused(self):
        p = self._file("abcd" * 64)
        env = self.H.seal("claude", CLAIM, "computation", artifact=p)
        p.write_text("abce" * 64)                    # the corrupted-band failure mode
        v = self.H.verify(env["handoff_id"], "gpt", file=p)
        self.assertEqual(v["status"], "damaged-in-transit")

    def test_producer_cannot_check_own_handoff(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"a": 1})
        v = self.H.verify(env["handoff_id"], "claude")
        self.assertEqual(v["status"], "refused")
        self.assertIn("independent party", v["failure_reason"])

    def test_claim_rewritten_after_sealing_is_caught(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"a": 1})
        rows = [json.loads(l) for l in Path(self.H.LEDGER).read_text().splitlines()]
        rows[0]["claim"] = "a claim edited afterwards to match the outcome"
        Path(self.H.LEDGER).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        v = self.H.verify(env["handoff_id"], "gpt")
        self.assertEqual(v["status"], "claim-rewritten")

    def test_a_label_is_not_a_claim(self):
        with self.assertRaises(SystemExit):
            self.H.seal("claude", "done", "computation", payload={})

    def test_unknown_producer_and_evidence_are_refused(self):
        with self.assertRaises(SystemExit):
            self.H.seal("somebody", CLAIM, "computation", payload={})
        with self.assertRaises(SystemExit):
            self.H.seal("claude", CLAIM, "vibes", payload={})


class TestEyeRecorder(unittest.TestCase):
    """The recorder preserves every eye and refuses invented coordinates."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _bad(self, obs, needle):
        res = node("observe", write(self.dir, "o.json", obs), self.dir)
        self.assertNotEqual(res.returncode, 0, res.stdout)
        self.assertIn(needle, res.stderr, res.stderr)

    def test_claim_must_declare_the_eyes_it_wants(self):
        res = node("claim", write(self.dir, "c.json",
                                  {"claim_id": "c", "claim": CLAIM}), self.dir)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("eyes_wanted", res.stderr)

    def test_unknown_verdict_is_refused(self):
        self._bad({**OBS, "verdict": "probably"}, "verdict must be one of")

    def test_supporting_verdict_needs_evidence(self):
        self._bad({**OBS, "verdict": "supports", "evidence": "none"},
                  "stronger than none")

    def test_silent_eye_must_say_what_would_let_it_see(self):
        self._bad({**OBS, "verdict": "silent", "evidence": "none"}, "blocked_on")

    def test_joining_a_set_requires_a_real_coordinate(self):
        self._bad({**OBS, "commensurable_set": "s"}, "rather than have one invented")

    def test_coordinate_and_values_must_line_up(self):
        self._bad({**OBS, "commensurable_set": "s", "unit": "u",
                   "coordinate": "k", "x_unit": "i", "x": [0, 1, 2], "values": [1, 2]},
                  "against 3 coordinates")

    def test_large_integers_must_be_quoted(self):
        self._bad({**OBS, "output": {"D": -217541503961543485618350976479}},
                  "past 2^53")

    def test_weight_zero_is_recorded_in_full(self):
        res = node("observe", write(self.dir, "o.json",
                                    {**OBS, "weight": 0}), self.dir)
        self.assertEqual(res.returncode, 0, res.stderr)
        row = json.loads((self.dir / "observations_v1.jsonl").read_text().strip())
        self.assertEqual(row["weight"], 0)
        self.assertEqual(row["output"], {"n": 1})    # nothing dropped

    def test_negative_weight_is_refused(self):
        self._bad({**OBS, "weight": -1}, "weight must be >= 0")

    def test_eyes_without_a_set_are_never_auto_grouped(self):
        node("observe", write(self.dir, "o.json",
                              [OBS, {**OBS, "eye_id": "e2"}]), self.dir)
        res = node("mix", "c", self.dir)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("2 eye(s) declare no commensurable set", res.stdout)
        self.assertFalse((self.dir / "sets_v1.jsonl").exists())


class TestCompoundView(unittest.TestCase):
    """Level 3 is derived from the observations, never asserted."""

    def setUp(self):
        import importlib
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["ACC_EYE_DIR"] = self.tmp.name
        sys.modules.pop("eye_report_v1", None)
        self.R = importlib.import_module("eye_report_v1")

    def tearDown(self):
        os.environ.pop("ACC_EYE_DIR", None)
        self.tmp.cleanup()

    def _rel(self, claim, obs):
        for i, o in enumerate(obs):
            o.setdefault("observed_utc", f"2026-09-13T00:00:{i:02d}Z")
            o.setdefault("weight", 1)
        return self.R.relationships(claim, obs)

    def test_contradiction_is_flagged_not_averaged(self):
        rel = self._rel(None, [
            {"eye_id": "a", "verdict": "supports", "evidence": "computation"},
            {"eye_id": "b", "verdict": "refutes", "evidence": "computation"}])
        self.assertEqual(rel["standing"], "contradicted")
        self.assertEqual(rel["contradiction"], [{"supports": "a", "refutes": "b"}])

    def test_blind_spots_come_from_the_roster(self):
        claim = {"claim_id": "c", "eyes_wanted": [
            {"eye_id": "a", "sees": "x"}, {"eye_id": "never-built", "sees": "y"}]}
        rel = self._rel(claim, [{"eye_id": "a", "verdict": "orthogonal",
                                 "evidence": "computation"}])
        self.assertEqual([b["eye"] for b in rel["blind_spots"]], ["never-built"])

    def test_shared_assumptions_surface_as_correlated_failure(self):
        rel = self._rel(None, [
            {"eye_id": "a", "verdict": "supports", "evidence": "computation",
             "assumptions": ["the transcription is faithful"]},
            {"eye_id": "b", "verdict": "supports", "evidence": "computation",
             "assumptions": ["the transcription is faithful"]}])
        self.assertEqual(rel["sensitivity"],
                         [{"assumption": "the transcription is faithful",
                           "eyes": ["a", "b"]}])
        self.assertEqual(rel["agreement"], {"supports": ["a", "b"]})

    def test_a_flipped_verdict_is_marked_unstable(self):
        rel = self._rel(None, [
            {"eye_id": "a", "verdict": "supports", "evidence": "computation",
             "observed_utc": "2026-09-13T00:00:00Z"},
            {"eye_id": "a", "verdict": "refutes", "evidence": "computation",
             "observed_utc": "2026-09-13T01:00:00Z"}])
        p = rel["persistence"][0]
        self.assertFalse(p["stable"])
        self.assertEqual(p["verdicts"], ["supports", "refutes"])

    def test_next_eye_is_ranked_by_how_much_one_bridge_opens(self):
        obs = [{"eye_id": f"e{i}", "verdict": "silent", "evidence": "none",
                "blocked_on": "bridge A"} for i in range(3)]
        obs.append({"eye_id": "e9", "verdict": "silent", "evidence": "none",
                    "blocked_on": "bridge B"})
        rel = self._rel(None, obs)
        self.assertEqual(rel["next_eye_needed"][0]["bridge"], "bridge A")
        self.assertEqual(rel["next_eye_needed"][0]["unblocks"], 3)


class TestLiveClaim(unittest.TestCase):
    """The claim actually recorded in this repo."""

    def setUp(self):
        sys.modules.pop("eye_report_v1", None)
        import eye_report_v1
        self.R = eye_report_v1

    def test_every_filed_eye_keeps_its_own_output_or_says_why_not(self):
        _, obs, _ = self.R.load("frontiermath-ell3-rank9")
        if not obs:
            self.skipTest("claim not present")
        for o in obs:
            self.assertTrue(o.get("output") is not None or o.get("blocked_on"),
                            f"{o['eye_id']} says nothing and gives no reason")

    def test_the_zero_weight_eye_is_still_in_the_record(self):
        _, obs, _ = self.R.load("frontiermath-ell3-rank9")
        if not obs:
            self.skipTest("claim not present")
        zero = [o for o in obs if o["weight"] == 0]
        self.assertTrue(zero, "the carried-literature eye should be present at weight 0")
        self.assertIsNotNone(zero[0]["output"])

    def test_the_report_names_a_bridge_that_unblocks_four_eyes(self):
        claims, obs, _ = self.R.load("frontiermath-ell3-rank9")
        if not obs:
            self.skipTest("claim not present")
        rel = self.R.relationships(claims[-1], obs)
        self.assertEqual(rel["next_eye_needed"][0]["unblocks"], 4)
        self.assertEqual(len(rel["blind_spots"]), 2)
        self.assertEqual(rel["contradiction"], [])


if __name__ == "__main__":
    unittest.main(verbosity=1)
