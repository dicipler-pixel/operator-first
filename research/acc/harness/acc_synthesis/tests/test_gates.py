"""Gate integration tests using a TOY receipt producer, NOT an ACC checker."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest

from acc_synthesis.gates import canonical_hash, sha256_file, verify_candidate


TOY_CHECKER = r'''
# TEST FIXTURE ONLY. This produces configured receipts, not mathematical proofs.
import hashlib, json, pathlib, sys, time
candidate_path, receipt_path = map(pathlib.Path, sys.argv[1:3])
candidate = json.loads(candidate_path.read_text())
mode = candidate.get("test_mode", "valid")
if mode == "timeout":
    time.sleep(5)
if mode == "stdout_overflow":
    sys.stdout.write("x" * (2 * 1024 * 1024))
    sys.stdout.flush()
if mode == "receipt_overflow":
    receipt_path.write_text("x" * (2 * 1024 * 1024))
    raise SystemExit(0)
if mode == "malformed":
    receipt_path.write_text('{"valid": true}')
    raise SystemExit(0)
if mode == "changed_checker":
    pathlib.Path(__file__).write_text(pathlib.Path(__file__).read_text() + "\n# changed\n")
digest = lambda obj: hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()
receipt = {
    "candidate_sha256": digest(candidate),
    "checker_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    "ruleset_sha256": candidate["ruleset_sha256"],
    "valid": mode != "invalid",
    "exact_endpoint": ["a", "b"] if mode != "wrong_endpoint" else ["A", "b"],
    "cost": len(candidate["moves"]) + (1 if mode == "wrong_cost" else 0),
    "peak_length": 4,
}
if mode == "bad_binding":
    receipt["candidate_sha256"] = "0" * 64
if mode == "bool_cost":
    receipt["cost"] = True
receipt_path.write_text(json.dumps(receipt))
'''


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.checker = self.root / "toy_checker.py"
        self.checker.write_text(TOY_CHECKER)
        self.ruleset = "a" * 64
        self.candidate = {
            "row_id": "test-00001", "track": "AC", "start": ["ab", "b"],
            "moves": [{"test_move": "remove_b"}], "ruleset_sha256": self.ruleset,
            "evidence_grade": "V", "family": "test-fixture",
        }
        self.manifest = {
            "ruleset_sha256": self.ruleset,
            "targets": [{"row_id": "test-00001", "track": "AC",
                         "start": ["ab", "b"], "goal": ["a", "b"]}],
        }
        (self.root / "targets.json").write_text(json.dumps(self.manifest))
        self.board = {"observed_at": 995, "ruleset_sha256": self.ruleset,
                      "rows": [{"row_id": "test-00001", "track": "AC",
                                "record": 1, "held_by_us": False}]}
        self.write_board()
        self.config = {
            "checker": {"path": "toy_checker.py", "sha256": sha256_file(self.checker),
                        "command": [sys.executable, "toy_checker.py", "{candidate}", "{receipt}"],
                        "timeout_seconds": 3},
            "target_manifest": "targets.json",
            "target_manifest_sha256": sha256_file(self.root / "targets.json"),
            "board_snapshot": "board.json", "board_max_age_seconds": 30,
        }

    def write_board(self):
        (self.root / "board.json").write_text(json.dumps(self.board))

    def check(self, mode=None, cancelled=None):
        candidate = copy.deepcopy(self.candidate)
        if mode:
            candidate["test_mode"] = mode
        return verify_candidate(candidate, self.config, self.root, now=1000, cancelled=cancelled)

    def test_canonical_hash_key_order(self):
        self.assertEqual(canonical_hash({"a": 1, "b": 2}), canonical_hash({"b": 2, "a": 1}))
        with self.assertRaises(ValueError):
            canonical_hash({"value": float("nan")})

    def test_fresh_exact_candidate_is_scoring(self):
        self.config["checks_directory"] = str(self.root / "controller-state" / "checks")
        result = self.check()
        self.assertEqual(result["status"], "verified_scoring")
        self.assertTrue(result["exact_verified"])
        self.assertEqual(result["cost"], 1)
        self.assertTrue(Path(result["receipt_path"]).exists())
        self.assertEqual(Path(result["check_directory"]).parent,
                         self.root / "controller-state" / "checks")

    def test_start_is_case_exact(self):
        self.candidate["start"] = ["Ab", "b"]
        self.assertEqual(self.check()["reason"], "exact_start_mismatch")

    def test_wrong_checker_pin(self):
        self.config["checker"]["sha256"] = "0" * 64
        self.assertEqual(self.check()["reason"], "checker_hash_mismatch")

    def test_wrong_manifest_pin(self):
        self.config["target_manifest_sha256"] = "0" * 64
        self.assertEqual(self.check()["reason"], "target_manifest_hash_mismatch")

    def test_wrong_ruleset(self):
        self.candidate["ruleset_sha256"] = "b" * 64
        self.assertEqual(self.check()["reason"], "ruleset_mismatch")

    def test_malformed_receipt_is_withheld(self):
        result = self.check("malformed")
        self.assertEqual(result["status"], "withheld")
        self.assertFalse(result["exact_verified"])

    def test_receipt_must_bind_exact_candidate(self):
        self.assertEqual(self.check("bad_binding")["reason"], "receipt_binding_mismatch")

    def test_endpoint_and_cost_require_exact_agreement(self):
        self.assertEqual(self.check("wrong_endpoint")["reason"], "exact_endpoint_mismatch")
        self.assertEqual(self.check("wrong_cost")["reason"], "unit_move_cost_mismatch")
        self.assertEqual(self.check("bool_cost")["reason"], "malformed_checker_receipt")

    def test_replay_rejection_is_invalid(self):
        self.assertEqual(self.check("invalid")["status"], "invalid")

    def test_stale_board_preserves_exact_result_but_withholds_eligibility(self):
        self.board["observed_at"] = 900
        self.write_board()
        result = self.check()
        self.assertEqual(result["reason"], "board_stale")
        self.assertEqual(result["status"], "withheld")
        self.assertTrue(result["exact_verified"])

    def test_future_board_is_withheld(self):
        self.board["observed_at"] = 1006
        self.write_board()
        self.assertEqual(self.check()["reason"], "board_timestamp_in_future")

    def test_owned_row_is_nonscoring(self):
        self.board["rows"][0]["held_by_us"] = True
        self.write_board()
        self.assertEqual(self.check()["status"], "verified_nonscoring")

    def test_cost_above_record_is_nonscoring(self):
        self.board["rows"][0]["record"] = 0
        self.write_board()
        self.assertEqual(self.check()["reason"], "cost_above_record")

    def test_improvement_on_owned_row_can_score(self):
        self.board['rows'][0].update(record=2,held_by_us=True,our_best_accepted=2)
        self.write_board()
        self.config['checker']['command'][0]='{python}'
        self.assertEqual(self.check()['status'],'verified_scoring')

    def test_duplicate_accepted_path_is_not_resubmitted(self):
        self.board['rows'][0].update(record=2,held_by_us=True,our_best_accepted=1)
        self.write_board()
        self.assertEqual(self.check()['reason'],'not_better_than_accepted_history')

    def test_unknown_ownership_is_withheld(self):
        del self.board["rows"][0]["held_by_us"]
        self.write_board()
        self.assertEqual(self.check()["reason"], "board_row_eligibility_unknown")

    def test_hypothesis_never_authorizes_checker(self):
        self.candidate["evidence_grade"] = "H"
        self.assertEqual(self.check()["status"], "withheld")
        self.assertFalse((self.root / "state").exists())

    def test_unpinned_command_is_rejected(self):
        self.config["checker"]["command"] = ["sh", "-c", "{candidate} {receipt}"]
        self.assertEqual(self.check()["reason"], "checker_unavailable_or_unsafe_command")

    def test_checker_change_is_detected(self):
        self.assertEqual(self.check("changed_checker")["reason"], "checker_changed_during_execution")

    def test_timeout_is_withheld(self):
        self.config["checker"]["timeout_seconds"] = 0.05
        self.assertEqual(self.check("timeout")["reason"], "checker_timeout")

    def test_malformed_grade_does_not_crash_gate(self):
        self.candidate["evidence_grade"] = ["V"]
        self.assertEqual(self.check()["reason"], "malformed_candidate")

    def test_unknown_command_placeholder_does_not_crash_gate(self):
        self.config["checker"]["command"].append("{candidate.foo}")
        self.assertEqual(self.check()["reason"], "unknown_checker_command_placeholder")

    def test_stop_before_checker_is_withheld_without_launch(self):
        self.assertEqual(self.check(cancelled=lambda: True)["reason"], "checker_cancelled")
        self.assertFalse((self.root / "state").exists())

    def test_stop_during_checker_terminates_promptly(self):
        began = time.monotonic()
        result = self.check("timeout", cancelled=lambda: time.monotonic() - began >= 0.1)
        self.assertEqual(result["reason"], "checker_cancelled")
        self.assertEqual(result["status"], "withheld")
        self.assertLess(time.monotonic() - began, 1)

    def test_checker_output_files_are_bounded(self):
        for mode, filename in (("stdout_overflow", "stdout.txt"), ("receipt_overflow", "receipt.json")):
            with self.subTest(mode=mode):
                result = self.check(mode)
                self.assertEqual(result["reason"], "checker_output_limit")
                output = Path(result["check_directory"]) / filename
                self.assertLessEqual(output.stat().st_size, 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
