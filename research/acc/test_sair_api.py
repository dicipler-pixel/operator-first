"""Tests for sair_api pagination and reconcile_live classification. No network, no POST."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import sair_api            # noqa: E402
import reconcile_live      # noqa: E402


class TestPagination(unittest.TestCase):
    def _pages(self, pages):
        calls = []
        def http(path, method="GET", body=None):
            calls.append((path, method))
            assert method == "GET", "tests must never POST"
            idx = 0
            if "cursor=" in path:
                idx = int(path.split("cursor=")[1])
            return 200, pages[idx], {}
        return http, calls

    def test_follows_next_cursor_and_dedupes(self):
        pages = [
            {"data": {"items": [{"submissionId": "s1", "results": [{"challenge_id": "ac-00001", "ok": True, "length": 5}]},
                                {"submissionId": "s2", "results": []}], "nextCursor": "1"}},
            {"data": {"items": [{"submissionId": "s2", "results": []},   # duplicate across pages
                                {"submissionId": "s3", "results": [{"challenge_id": "ac-00002", "ok": False}]}], "nextCursor": "2"}},
            {"data": {"items": [{"submissionId": "s4", "results": []}], "nextCursor": None}},
        ]
        http, calls = self._pages(pages)
        items, n_pages, errors = sair_api.fetch_all("/submissions/mine", http=http)
        self.assertEqual(n_pages, 3)
        self.assertEqual([i["submissionId"] for i in items], ["s1", "s2", "s3", "s4"])
        self.assertEqual(errors, [])
        self.assertTrue(all(m == "GET" for _, m in calls))

    def test_top_level_cursor_and_list_payload(self):
        pages = [{"items": [{"id": "a"}], "nextCursor": "1"}, {"items": [{"id": "b"}]}]
        http, _ = self._pages(pages)
        items, n, _ = sair_api.fetch_all("/x", http=http)
        self.assertEqual(n, 2); self.assertEqual(len(items), 2)

    def test_http_error_stops_and_is_reported(self):
        def http(path, method="GET", body=None):
            return 403, {"error": "forbidden"}, {}
        items, n, errors = sair_api.fetch_all("/submissions/mine", http=http)
        self.assertEqual(items, []); self.assertEqual(n, 1); self.assertEqual(errors[0]["status"], 403)

    def test_key_never_in_output(self):
        os.environ["SAIR_API_KEY"] = "SECRET-DO-NOT-LEAK"
        def http(path, method="GET", body=None):
            return 200, {"data": {"items": [], "nextCursor": None}}, {}
        items, n, errors = sair_api.fetch_all("/submissions/mine", http=http)
        self.assertNotIn("SECRET", json.dumps([items, n, errors]))


class TestReconcile(unittest.TestCase):
    def test_every_classification(self):
        live = {"data": {"items": [
            {"challengeId": "ac-00001", "status": "unsolved", "currentBestLength": None, "kTeams": 0},
            {"challengeId": "ac-00002", "status": "solved", "currentBestLength": 30, "kTeams": 1},
            {"challengeId": "ac-00003", "status": "solved", "currentBestLength": 22, "kTeams": 4},
            {"challengeId": "ac-00004", "status": "solved", "currentBestLength": 22, "kTeams": 4},
            {"challengeId": "ac-00005", "status": "solved", "currentBestLength": 10, "kTeams": 2},
            {"challengeId": "ac-00006", "status": "solved", "currentBestLength": 10, "kTeams": 2},
            {"challengeId": "ac-00007", "status": "solved", "currentBestLength": 10, "kTeams": 2},
            {"challengeId": "ac-00008", "status": "solved", "currentBestLength": 10, "kTeams": 2},
        ]}}
        mine = {"pages": 2, "errors": [], "items": [
            {"submissionId": "s1", "results": [
                {"challenge_id": "ac-00004", "ok": True, "length": 22},   # tie already on server
                {"challenge_id": "ac-00005", "ok": True, "length": 40},   # server worse than local 30
                {"challenge_id": "ac-00006", "ok": True, "length": 15},   # server better than local 30
                {"challenge_id": "ac-00008", "ok": True, "length": 12},   # no local cert
            ]}]}
        certs = "\n".join([
            "ac-00001: [0, 1]  # unsolved live, local path",
            "ac-00002: [0, 1, 2]  # beats live 30",
            "ac-00003: [0, 1, 2, 3]  # equals live 22, not on server (lengths faked; trust_unverified)",
            "ac-00004: [0, 1, 2, 3]",
            "ac-00005: [0]*30",
            "ac-00006: [0]*30",
            "ac-00007: [0]*30  # loses to live 10, nothing on server -> obsolete",
            "sac-00001: [0, 1, 16, 15]  # stable lines are ignored here",
        ]).replace("[0]*30", json.dumps([0] * 30))
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "snap.json").write_text(json.dumps(live)); (d / "mine.json").write_text(json.dumps(mine)); (d / "c.txt").write_text(certs)
            # fake lengths for classification: 00002 -> 3 (<30), 00003/00004 -> want == 22; patch by trust_unverified and explicit lengths
            # Use lengths as written: 00003 has 4 moves so it would be STRICT_LIVE_WIN; adjust live to match.
            live["data"]["items"][2]["currentBestLength"] = 4
            live["data"]["items"][3]["currentBestLength"] = 4
            mine["items"][0]["results"][0]["length"] = 4
            (d / "snap.json").write_text(json.dumps(live)); (d / "mine.json").write_text(json.dumps(mine))
            reconcile_live.run(str(d / "snap.json"), str(d / "mine.json"), [str(d / "c.txt")], str(d / "out"), trust_unverified=True)
            rep = json.load(open(d / "out" / "PRIVATE_RECONCILIATION.json"))
            t = rep["table"]
            self.assertEqual(t["ac-00001"]["classification"], "UNSOLVED_LOCAL_SOLUTION")
            self.assertEqual(t["ac-00002"]["classification"], "STRICT_LIVE_WIN")
            self.assertEqual(t["ac-00003"]["classification"], "TIE_NOT_ON_SERVER")
            self.assertEqual(t["ac-00004"]["classification"], "TIE_ALREADY_ON_SERVER")
            self.assertEqual(t["ac-00005"]["classification"], "LOCAL_BETTER_THAN_SERVER")
            self.assertEqual(t["ac-00006"]["classification"], "SERVER_BETTER_THAN_LOCAL")
            self.assertEqual(t["ac-00007"]["classification"], "OBSOLETE_LOCAL")
            self.assertEqual(t["ac-00008"]["classification"], "NO_LOCAL_CERT")
            self.assertEqual(t["ac-00004"]["submission_ids_containing_ours"], ["s1"])
            submit = (d / "out" / "PRIVATE_SUBMIT_NOW.txt").read_text()
            self.assertIn("ac-00001:", submit); self.assertIn("ac-00002:", submit); self.assertNotIn("ac-00004:", submit)
            self.assertNotIn("_moves", json.dumps(rep))  # moves never leak into the json table

    def test_unverified_paths_are_not_trusted_by_default(self):
        live = {"data": {"items": [{"challengeId": "ac-00001", "status": "unsolved", "currentBestLength": None}]}}
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "s.json").write_text(json.dumps(live)); (d / "m.json").write_text(json.dumps({"items": []})); (d / "c.txt").write_text("ac-00001: [0, 1]\n")
            saved = reconcile_live._verifier; reconcile_live._verifier = lambda: None
            try:
                reconcile_live.run(str(d / "s.json"), str(d / "m.json"), [str(d / "c.txt")], str(d / "out"))
            finally:
                reconcile_live._verifier = saved
            rep = json.load(open(d / "out" / "PRIVATE_RECONCILIATION.json"))
            self.assertEqual(rep["table"]["ac-00001"]["classification"], "INVALID_OR_UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
