"""Kernel regressions: durable evidence, fencing, stop, and bounded execution."""

import concurrent.futures
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from runtime import HarnessError, Store, run_command


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "state.sqlite3"
        self.store = Store(self.path)

    def leased(self, family=""):
        task_id = self.store.enqueue("sol", {"question": "bounded work"}, "one", family)
        return task_id, self.store.claim(lease_seconds=30)

    def test_unique_key_survives_completion_and_reopen(self):
        task_id, lease = self.leased()
        self.store.finish(task_id, lease["token"], {"candidate": "artifact.json"})
        reopened = Store(self.path)
        duplicate = reopened.enqueue("sol", {"question": "bounded work"}, "one")
        self.assertEqual(task_id, duplicate)
        tasks = reopened.tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["role"], "sol")
        self.assertEqual(tasks[0]["result"], {"candidate": "artifact.json"})
        self.assertIsNone(reopened.claim())

    def test_conflicting_duplicate_is_rejected_and_key_order_is_irrelevant(self):
        original = self.store.enqueue("sol", {"a": 1, "b": {"c": 2}}, "same", "family")
        self.assertEqual(original, self.store.enqueue("sol", {"b": {"c": 2}, "a": 1}, "same", "family"))
        for role, payload, family in (
            ("astra", {"a": 1, "b": {"c": 2}}, "family"),
            ("sol", {"a": 1, "b": {"c": 3}}, "family"),
            ("sol", {"a": 1, "b": {"c": 2}}, "other-family"),
        ):
            with self.subTest(role=role, payload=payload, family=family), self.assertRaises(HarnessError) as caught:
                self.store.enqueue(role, payload, "same", family)
            self.assertEqual(caught.exception.code, "idempotency_conflict")
        self.assertEqual(len(self.store.tasks()), 1)
        self.assertEqual(self.store.tasks()[0]["payload"], {"a": 1, "b": {"c": 2}})

    def test_stop_blocks_authoritative_admission_without_writing_an_event(self):
        before_stop = self.store.admit("candidate.admitted", {"candidate": "first"})
        self.store.stop("Hold admissions")
        before = self.store.events()
        with self.assertRaises(HarnessError) as caught:
            self.store.admit("candidate.admitted", {"candidate": "second"})
        self.assertEqual(caught.exception.code, "stopped")
        self.assertEqual(self.store.events(), before)
        self.assertEqual([event["id"] for event in before if event["kind"] == "candidate.admitted"], [before_stop])
        self.store.resume()
        self.assertGreater(self.store.admit("candidate.admitted", {"candidate": "second"}), before_stop)

    def test_expired_worker_cannot_renew_finish_or_fail(self):
        task_id, lease = self.leased()
        with patch("runtime.time.time", return_value=lease["lease_until"] + 1):
            for operation in (
                lambda: self.store.heartbeat(task_id, lease["token"]),
                lambda: self.store.finish(task_id, lease["token"], {"false_success": True}),
                lambda: self.store.fail(task_id, lease["token"], "late failure"),
            ):
                with self.assertRaises(HarnessError) as caught:
                    operation()
                self.assertEqual(caught.exception.code, "lease_expired")
            self.assertEqual(self.store.recover(), 1)
            self.assertEqual(self.store.recover(), 0)
        self.assertEqual(self.store.tasks()[0]["status"], "interrupted")
        self.assertIsNone(self.store.claim())
        with self.assertRaises(HarnessError):
            self.store.finish(task_id, lease["token"], {})

    def test_only_one_family_member_runs_even_with_concurrent_claims(self):
        self.store.enqueue("sol", {"a": 1}, "a", "same-search")
        self.store.enqueue("astra", {"b": 2}, "b", "same-search")
        barrier = threading.Barrier(2)

        def worker():
            independent = Store(self.path)
            barrier.wait(timeout=2)
            return independent.claim()

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            claims = list(pool.map(lambda _: worker(), range(2)))
        live = [claim for claim in claims if claim is not None]
        self.assertEqual(len(live), 1)
        self.store.finish(live[0]["id"], live[0]["token"], {})
        self.assertIsNotNone(self.store.claim())

    def test_empty_families_do_not_block_each_other(self):
        self.store.enqueue("sol", {}, "a")
        self.store.enqueue("sol", {}, "b")
        self.assertIsNotNone(self.store.claim())
        self.assertIsNotNone(self.store.claim())

    def test_stop_persists_and_resume_does_not_retry_interrupted_work(self):
        task_id, lease = self.leased()
        queued = self.store.enqueue("luna", {}, "two")
        self.store.stop("User stop")
        reopened = Store(self.path)
        self.assertTrue(reopened.stopped())
        self.assertIsNone(reopened.claim())
        with self.assertRaises(HarnessError) as caught:
            reopened.finish(task_id, lease["token"], {})
        self.assertEqual(caught.exception.code, "stopped")
        reopened.resume()
        self.assertEqual(reopened.claim()["id"], queued)
        self.assertEqual(reopened.tasks("interrupted")[0]["id"], task_id)

    def test_event_log_records_claims_and_is_append_only(self):
        task_id, lease = self.leased()
        self.store.event("claim.proposed", {"grade": "H", "text": "hypothesis"})
        self.store.fail(task_id, lease["token"], {"code": "test_failure"})
        kinds = [event["kind"] for event in self.store.events()]
        self.assertEqual(kinds, ["store.created", "task.enqueued", "task.claimed",
                                 "claim.proposed", "task.failed"])
        with sqlite3.connect(self.path) as conn:
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("DELETE FROM events")
            with self.assertRaises(sqlite3.IntegrityError):
                conn.execute("UPDATE events SET kind='rewritten'")
            self.assertEqual(conn.execute("PRAGMA journal_mode").fetchone()[0], "wal")

    def test_json_round_trip_and_lease_heartbeat(self):
        _, lease = self.leased()
        script = "import json,sys,time; x=json.load(sys.stdin); time.sleep(.08); print(json.dumps({'echo':x}))"
        result = run_command([sys.executable, "-c", script], {"unicode": "\u03a0"}, 2,
                             store=self.store, lease=lease)
        self.assertEqual(result, {"echo": {"unicode": "\u03a0"}})
        self.assertEqual(self.store.tasks()[0]["status"], "running")
        self.assertIn("task.heartbeat", [event["kind"] for event in self.store.events()])

    def test_timeout_returns_promptly(self):
        started = time.monotonic()
        with self.assertRaises(HarnessError) as caught:
            run_command([sys.executable, "-c", "import time; time.sleep(5)"], {}, .1)
        self.assertEqual(caught.exception.code, "timeout")
        self.assertLess(time.monotonic() - started, 1.5)

    def test_persistent_stop_interrupts_running_command(self):
        _, lease = self.leased()
        timer = threading.Timer(.1, lambda: Store(self.path).stop("Stop now"))
        timer.start()
        self.addCleanup(timer.join)
        with self.assertRaises(HarnessError) as caught:
            run_command([sys.executable, "-c", "import time; time.sleep(5)"], {}, 3,
                        store=self.store, lease=lease)
        self.assertEqual(caught.exception.code, "stopped")
        self.assertEqual(self.store.tasks()[0]["status"], "interrupted")

    def test_malformed_output_nonobject_and_nonfinite_are_rejected(self):
        for text in ("narrative before JSON {}", "[]", '{"bad":NaN}', '{"bad":1e999}', "{} {}"):
            with self.subTest(text=text), self.assertRaises(HarnessError) as caught:
                run_command([sys.executable, "-c", f"print({text!r})"], {}, 2)
            self.assertEqual(caught.exception.code, "invalid_output")

    def test_nonzero_and_excess_output_are_rejected(self):
        with self.assertRaises(HarnessError) as caught:
            run_command([sys.executable, "-c", "print('{}'); raise SystemExit(3)"], {}, 2)
        self.assertEqual(caught.exception.code, "command_failed")
        with self.assertRaises(HarnessError) as caught:
            run_command([sys.executable, "-c", "import sys; sys.stderr.write('x'*100000)"], {}, 2,
                        max_output_bytes=4096)
        self.assertEqual(caught.exception.code, "output_limit")

    def test_wrong_token_is_fenced(self):
        task_id, _ = self.leased()
        with self.assertRaises(HarnessError) as caught:
            self.store.finish(task_id, "another-worker", {})
        self.assertEqual(caught.exception.code, "stale_lease")
        self.assertEqual(self.store.tasks()[0]["status"], "running")


if __name__ == "__main__":
    unittest.main()
