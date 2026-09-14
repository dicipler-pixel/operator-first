"""Adversarial tests for the event stream. Each one tries to break a property.

A test bed that has not been attacked is a claim, not a test bed.

    python3 tools/acc/test_event_log_v1.py
"""

import json
import multiprocessing
import os
import signal
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog, EYE_STATES, RELATIONSHIPS, unsafe_integers  # noqa: E402


def _writer(directory, tag, count):
    """Separate process: real concurrency, not threads sharing a lock object."""
    log = EventLog(directory)
    for i in range(count):
        log.append("note", {"tag": tag, "i": i}, run_id=tag)


class TestTamperEvidence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)
        for i in range(6):
            self.log.append("note", {"i": i})

    def tearDown(self):
        self.tmp.cleanup()

    def _lines(self):
        return self.log.path.read_text().splitlines()

    def _write(self, lines):
        self.log.path.write_text("\n".join(lines) + "\n")

    def test_clean_stream_verifies(self):
        n, problems = self.log.verify()
        self.assertEqual(problems, [])
        self.assertEqual(n, 6)

    def test_editing_a_record_is_caught(self):
        lines = self._lines()
        rec = json.loads(lines[2])
        rec["body"]["i"] = 999                 # change the payload, keep the digest
        lines[2] = json.dumps(rec)
        self._write(lines)
        _, problems = self.log.verify()
        self.assertTrue(any("digest mismatch" in p for p in problems), problems)

    def test_deleting_a_record_breaks_the_chain(self):
        lines = self._lines()
        del lines[3]
        self._write(lines)
        _, problems = self.log.verify()
        self.assertTrue(any("chain break" in p for p in problems), problems)

    def test_reordering_records_breaks_the_chain(self):
        lines = self._lines()
        lines[2], lines[3] = lines[3], lines[2]
        self._write(lines)
        _, problems = self.log.verify()
        self.assertTrue(any("chain break" in p for p in problems), problems)

    def test_a_forged_record_with_a_recomputed_digest_still_breaks_later_links(self):
        """The hardest case: an attacker who knows the digest rule."""
        import hashlib
        from event_log_v1 import canonical
        lines = self._lines()
        rec = json.loads(lines[2])
        rec["body"]["i"] = 999
        rec["digest"] = hashlib.sha256(canonical(
            {k: rec[k] for k in ("seq", "ts", "run_id", "kind", "body", "prev")})
        ).hexdigest()
        lines[2] = json.dumps(rec)
        self._write(lines)
        _, problems = self.log.verify()
        # digest now matches, but every later record points at the old one
        self.assertTrue(any("chain break" in p for p in problems), problems)


class TestTornWrites(unittest.TestCase):
    """A process killed mid-append must leave evidence, not plausible data."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_truncated_tail_is_reported_as_torn(self):
        for i in range(4):
            self.log.append("note", {"i": i})
        raw = self.log.path.read_bytes()
        self.log.path.write_bytes(raw[:-40])      # simulate a kill mid-line
        n, problems = self.log.verify()
        self.assertTrue(any("TORN" in p for p in problems), problems)
        self.assertEqual(n, 3, "the three intact records must still be readable")

    def test_a_real_killed_writer_leaves_a_recoverable_stream(self):
        script = textwrap.dedent(f"""
            import sys, time
            sys.path.insert(0, {str(HERE)!r})
            from event_log_v1 import EventLog
            log = EventLog({self.tmp.name!r})
            for i in range(10000):
                log.append("note", {{"i": i, "pad": "x" * 200}})
        """)
        p = subprocess.Popen([sys.executable, "-c", script])
        time.sleep(1.2)
        p.send_signal(signal.SIGKILL)
        p.wait()
        n, problems = self.log.verify()
        self.assertGreater(n, 0, "the killed writer should have committed events")
        # Whatever survived must be a valid prefix: no chain break, no forgery.
        self.assertEqual([x for x in problems if "chain break" in x or "digest" in x],
                         [], f"a kill must not corrupt committed history: {problems}")

    def test_appending_after_a_torn_tail_does_not_silently_fork(self):
        for i in range(3):
            self.log.append("note", {"i": i})
        raw = self.log.path.read_bytes()
        self.log.path.write_bytes(raw + b'{"seq": 3, "kind": "not json really')
        self.log.append("note", {"i": "after"})
        _, problems = self.log.verify()
        self.assertTrue(any("TORN" in p for p in problems),
                        "the torn line must stay visible in the record")


class TestConcurrency(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_four_processes_appending_at_once_lose_nothing(self):
        per, tags = 60, ["a", "b", "c", "d"]
        procs = [multiprocessing.Process(target=_writer,
                                         args=(self.tmp.name, t, per)) for t in tags]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        n, problems = self.log.verify()
        self.assertEqual(problems, [], problems)
        self.assertEqual(n, per * len(tags), "every append must survive")
        counts = {}
        for _, rec, _ in self.log.read():
            counts[rec["body"]["tag"]] = counts.get(rec["body"]["tag"], 0) + 1
        self.assertEqual(counts, {t: per for t in tags})

    def test_concurrent_appends_do_not_fork_the_chain(self):
        for p in [multiprocessing.Process(target=_writer, args=(self.tmp.name, t, 40))
                  for t in ("x", "y", "z")]:
            p.start()
            p.join() if False else None
        # start/join properly
        procs = [multiprocessing.Process(target=_writer, args=(self.tmp.name, t, 40))
                 for t in ("p", "q")]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        _, problems = self.log.verify()
        self.assertEqual([x for x in problems if "chain" in x or "seq" in x], [])


class TestUnsafeIntegersEverywhere(unittest.TestCase):
    """The earlier guards checked one field. This checks the whole event."""

    BIG = 217541503961543485618350976479

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _refused(self, body, needle):
        with self.assertRaises(ValueError) as e:
            self.log.append("note", body)
        self.assertIn(needle, str(e.exception))

    def test_top_level(self):
        self._refused({"D": self.BIG}, "body.D")

    def test_nested_in_a_dict(self):
        self._refused({"a": {"b": {"c": self.BIG}}}, "body.a.b.c")

    def test_inside_a_list(self):
        self._refused({"xs": [1, 2, self.BIG]}, "body.xs[2]")

    def test_list_of_dicts(self):
        self._refused({"rows": [{"ok": 1}, {"D": self.BIG}]}, "body.rows[1].D")

    def test_deeply_mixed(self):
        self._refused({"a": [{"b": [{"c": [self.BIG]}]}]}, "body.a[0].b[0].c[0]")

    def test_negative_is_caught_too(self):
        self._refused({"D": -self.BIG}, "body.D")

    def test_float_past_the_boundary(self):
        self._refused({"D": 2.2e29}, "body.D")

    def test_a_dict_key_that_is_a_huge_number(self):
        bad = unsafe_integers({str("x"): 1})
        self.assertEqual(bad, [])
        self.assertTrue(unsafe_integers({"m": {self.BIG: "v"}}))

    def test_booleans_are_not_integers(self):
        self.log.append("note", {"flag": True, "other": False})

    def test_the_boundary_itself_is_allowed(self):
        self.log.append("note", {"n": 2 ** 53 - 1})

    def test_quoted_big_integer_is_the_supported_route(self):
        rec = self.log.append("note", {"D": str(self.BIG)})
        self.assertEqual(rec["body"]["D"], str(self.BIG))


class TestEyeDiscipline(unittest.TestCase):
    """No eye disappears, and a non-observation must say why."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_all_six_states_are_filable(self):
        for s in sorted(EYE_STATES):
            self.log.eye_reading("r", "c", f"eye-{s}", s,
                                 output={"x": 1}, reason="because")
        _, problems = self.log.verify()
        self.assertEqual(problems, [])

    def test_an_unknown_state_is_refused(self):
        with self.assertRaises(ValueError):
            self.log.eye_reading("r", "c", "e", "probably")

    def test_blocked_disabled_and_failed_require_a_reason(self):
        for s in ("blocked", "disabled", "failed"):
            with self.assertRaises(ValueError) as e:
                self.log.eye_reading("r", "c", "e", s)
            self.assertIn("requires a reason", str(e.exception))

    def test_a_zero_weight_eye_still_files_and_is_readable(self):
        self.log.eye_reading("r", "c", "carried", "observed",
                             output={"three_rank": 8}, weight=0)
        rows = [rec for _, rec, _ in self.log.read()
                if rec["kind"] == "eye-reading"]
        self.assertEqual(rows[0]["body"]["weight"], 0)
        self.assertIsNotNone(rows[0]["body"]["output"])


class TestRelationships(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_every_declared_relationship_is_recordable(self):
        for r in sorted(RELATIONSHIPS):
            self.log.relationship("run", r, "eye-a", "eye-b", evidence="e")
        _, problems = self.log.verify()
        self.assertEqual(problems, [])
        self.assertEqual(len(RELATIONSHIPS), 10)

    def test_an_invented_relationship_is_refused(self):
        with self.assertRaises(ValueError):
            self.log.relationship("run", "vibes-with", "a", "b")


class TestChunkStoreAndDeltas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = EventLog(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_same_state_is_stored_once(self):
        s = {"r0": [1, 2, -1], "r1": [2]}
        a = self.log.put_chunk(s)
        b = self.log.put_chunk(dict(s))
        self.assertEqual(a, b)
        files = list((Path(self.tmp.name) / "chunks").rglob("*.json"))
        self.assertEqual(len(files), 1, "content addressing must deduplicate")

    def test_a_transition_stores_a_delta_not_a_copy(self):
        parent = self.log.put_chunk({"r0": [1], "r1": [2]})
        rec = self.log.search_transition("run", parent, 4, "expand",
                                         reason="length dropped",
                                         eyes={"tau": "invariant"})
        self.assertTrue(rec["body"]["child_derivable"])
        self.assertIsNone(rec["body"]["child"])
        self.assertEqual(rec["body"]["move"], 4)

    def test_chunks_are_written_atomically(self):
        ref = self.log.put_chunk({"a": 1})
        tmps = list((Path(self.tmp.name) / "chunks").rglob("*.tmp"))
        self.assertEqual(tmps, [], "no half-written chunk may remain")
        self.assertEqual(self.log.get_chunk(ref), {"a": 1})


class TestLiveStream(unittest.TestCase):
    def test_the_committed_stream_verifies(self):
        log = EventLog()
        n, problems = log.verify()
        self.assertEqual(problems, [], problems)


if __name__ == "__main__":
    unittest.main(verbosity=1)
