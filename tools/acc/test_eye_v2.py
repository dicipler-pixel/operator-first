"""Tests for hand-off v2 and eye_log v2 — the three gaps found in review.

    python3 tools/acc/test_eye_v2.py
"""

import importlib
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

EYE_V2 = ROOT / "tools" / "acc" / "eye_log_v2.js"
CLAIM = "a falsifiable sentence long enough to count as a real claim"

BASE = {"claim_id": "t", "eye_id": "a", "verdict": "orthogonal",
        "evidence": "computation", "output": {}, "commensurable_set": "s",
        "unit": "u", "coordinate": "candidate row", "x_unit": "row ordinal",
        "x": [0, 1, 2], "values": [1, 2, 3]}


def node(cmd, arg, eye_dir):
    env = dict(os.environ, ACC_EYE_DIR=str(eye_dir), PATH="/usr/bin:/bin:/usr/local/bin")
    return subprocess.run(["node", str(EYE_V2), cmd, str(arg)],
                          cwd=ROOT, capture_output=True, text=True, env=env)


def write(d, name, payload):
    p = Path(d) / name
    p.write_text(json.dumps(payload))
    return p


class TestTransportIsNotClaim(unittest.TestCase):
    """Gap 1: an envelope check must never read as mathematical verification."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["ACC_HANDOFF_LEDGER"] = str(Path(self.tmp.name) / "h.jsonl")
        sys.modules.pop("handoff_v2", None)
        self.H = importlib.import_module("handoff_v2")

    def tearDown(self):
        os.environ.pop("ACC_HANDOFF_LEDGER", None)
        self.tmp.cleanup()

    def test_row_handoff_verifies_transport_but_withholds_the_claim(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"target": 9})
        c = self.H.verify(env["handoff_id"], "gpt")
        self.assertTrue(c["transport_verified"])
        self.assertIsNone(c["claim_verified"])
        self.assertEqual(c["claim_status"], "withheld")
        self.assertIn("not that the claim is true", c["claim_reason"])
        self.assertIn("no mathematical artifact at all", c["claim_reason"])

    def test_attesting_support_without_a_result_artifact_is_refused(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"target": 9})
        with self.assertRaises(SystemExit) as e:
            self.H.attest(env["handoff_id"], "gpt", "supports", "computation")
        self.assertIn("requires a result artifact", str(e.exception))

    def test_a_result_from_the_claims_own_producer_is_refused(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"a": 1})
        res = self.H.seal("claude", "the result package for that claim", "computation",
                          payload={"b": 2})
        with self.assertRaises(SystemExit) as e:
            self.H.attest(env["handoff_id"], "gpt", "supports", "computation",
                          result_id=res["handoff_id"])
        self.assertIn("same", str(e.exception))

    def test_open_is_attestable_without_a_result(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"a": 1})
        a = self.H.attest(env["handoff_id"], "gpt", "open", "none")
        self.assertEqual(a["claim_status"], "open")
        self.assertFalse(a["claim_verified"])

    def test_producer_cannot_attest_to_its_own_claim(self):
        env = self.H.seal("claude", CLAIM, "computation", payload={"a": 1})
        with self.assertRaises(SystemExit):
            self.H.attest(env["handoff_id"], "claude", "open", "none")


class TestPayloadIsHashed(unittest.TestCase):
    """Gap 2: an inline payload could be edited after sealing and still pass."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.led = Path(self.tmp.name) / "h.jsonl"
        os.environ["ACC_HANDOFF_LEDGER"] = str(self.led)
        sys.modules.pop("handoff_v2", None)
        self.H = importlib.import_module("handoff_v2")

    def tearDown(self):
        os.environ.pop("ACC_HANDOFF_LEDGER", None)
        self.tmp.cleanup()

    def _rewrite(self, fn):
        rows = [json.loads(l) for l in self.led.read_text().splitlines()]
        fn(rows[0])
        self.led.write_text("\n".join(json.dumps(r) for r in rows) + "\n")

    def test_edited_payload_is_caught(self):
        env = self.H.seal("claude", CLAIM, "computation",
                          payload={"three_rank": 3, "target": 9})
        self._rewrite(lambda r: r["payload"].__setitem__("three_rank", 9))
        c = self.H.verify(env["handoff_id"], "gpt")
        self.assertFalse(c["transport_verified"])
        self.assertEqual(c["transport_status"], "payload-altered")

    def test_key_order_does_not_change_the_digest(self):
        a = self.H.seal("claude", CLAIM, "computation", payload={"x": 1, "y": 2})
        b = self.H.seal("gpt", CLAIM, "computation", payload={"y": 2, "x": 1})
        self.assertEqual(a["payload_sha256"], b["payload_sha256"])

    def test_dropping_a_file_from_the_manifest_is_caught(self):
        f1 = Path(self.tmp.name) / "one.txt"; f1.write_text("a" * 10)
        f2 = Path(self.tmp.name) / "two.txt"; f2.write_text("b" * 20)
        env = self.H.seal("claude", CLAIM, "computation", artifacts=[f1, f2])
        self._rewrite(lambda r: r["artifacts"].pop())
        c = self.H.verify(env["handoff_id"], "gpt")
        self.assertEqual(c["transport_status"], "manifest-altered")

    def test_package_of_files_is_sealed_and_each_is_checked(self):
        f1 = Path(self.tmp.name) / "one.txt"; f1.write_text("a" * 10)
        f2 = Path(self.tmp.name) / "two.txt"; f2.write_text("b" * 20)
        env = self.H.seal("claude", CLAIM, "computation", artifacts=[f1, f2])
        self.assertEqual(len(env["artifacts"]), 2)
        f2.write_text("b" * 7)
        c = self.H.verify(env["handoff_id"], "gpt",
                          files={"one.txt": str(f1), "two.txt": str(f2)})
        self.assertEqual(c["transport_status"], "damaged-in-transit")
        self.assertIn("short by 13", c["transport_reason"])

    def test_unsafe_integers_anywhere_in_the_payload_are_refused(self):
        with self.assertRaises(SystemExit) as e:
            self.H.seal("claude", CLAIM, "computation",
                        payload={"rows": [{"D": -217541503961543485618350976479}]})
        self.assertIn("payload.rows[0].D", str(e.exception))


class TestCoordinateAgreement(unittest.TestCase):
    """Gap 3: equal length is not agreement."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _pair(self, second):
        node("observe", write(self.dir, "o.json", [BASE, {**BASE, "eye_id": "b", **second}]),
             self.dir)
        return node("mix", "t", self.dir)

    def test_same_length_different_points_is_refused(self):
        res = self._pair({"x": [0, 5, 9], "values": [4, 5, 6]})
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("different points", res.stderr)
        self.assertIn("first difference at index 1", res.stderr)

    def test_different_coordinate_label_is_refused(self):
        res = self._pair({"coordinate": "step index", "values": [4, 5, 6]})
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('coordinate "step index"', res.stderr)

    def test_different_coordinate_unit_is_refused(self):
        res = self._pair({"x_unit": "seconds", "values": [4, 5, 6]})
        self.assertNotEqual(res.returncode, 0)
        self.assertIn('x_unit "seconds"', res.stderr)

    def test_a_zero_weight_member_is_checked_too(self):
        res = self._pair({"weight": 0, "x": [0, 5, 9], "values": [4, 5, 6]})
        self.assertNotEqual(res.returncode, 0, "a weight-zero eye is still declared "
                                               "commensurable and must actually be")

    def test_agreeing_coordinates_mix_and_say_so(self):
        res = self._pair({"values": [4, 5, 6]})
        self.assertEqual(res.returncode, 0, res.stderr)
        row = [json.loads(l) for l in (self.dir / "sets_v1.jsonl").read_text().splitlines()][-1]
        self.assertEqual(row["schema"], "compound-eye-set-v2")
        self.assertIn("identical x array", row["coordinate_agreement"])

    def test_unsafe_integers_in_x_and_values_are_refused(self):
        for field in ("x", "values"):
            res = node("observe", write(self.dir, "o.json",
                       {**BASE, field: [0, 1, 217541503961543485618350976479]}), self.dir)
            self.assertNotEqual(res.returncode, 0, f"{field} went through unchecked")
            self.assertIn("past 2^53", res.stderr)


class TestLiveRank9(unittest.TestCase):
    """The rank-9 hand-off must not read as mathematically verified."""

    def test_claim_is_withheld_or_open_never_verified(self):
        sys.modules.pop("handoff_v2", None)
        os.environ.pop("ACC_HANDOFF_LEDGER", None)
        import handoff_v2 as H
        importlib.reload(H)
        env, at = H.seals(), H.attestations()
        if not env:
            self.skipTest("no hand-offs sealed")
        for hid in env:
            a = at.get(hid)
            self.assertNotEqual((a or {}).get("claim_verified"), True,
                                f"{hid} is marked claim-verified; no rank-9 "
                                f"certificate exists")


if __name__ == "__main__":
    unittest.main(verbosity=1)
