"""Tests for the timeline layer: batching, strength grading, context, before/after.

The point of most of these is that the tool must REFUSE to call something a
trend when the data cannot carry one.

    python3 tools/acc/test_timeline_v1.py
"""

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import timeline_v1 as T  # noqa: E402

T0 = datetime(2026, 9, 13, 12, 0, 0, tzinfo=timezone.utc)


def mk(offset_seconds, source="eye-obs", kind="silent", label="x",
       signals=(("blocker", "needs sage"),), ident=None):
    return T.ev(T0 + timedelta(seconds=offset_seconds), source, kind, label,
                signals, None, ident or label)


def stream(*events):
    dated, _ = T.order(list(events))
    return dated


class TestBatching(unittest.TestCase):
    """A write batch is one command, not a pattern."""

    def test_events_written_together_are_one_batch(self):
        self.assertEqual(len(T.batches(stream(mk(0), mk(0.01), mk(0.02)))), 1)

    def test_a_gap_starts_a_new_batch(self):
        self.assertEqual(len(T.batches(stream(mk(0), mk(0.5), mk(60)))), 2)

    def test_boundary_is_the_declared_gap(self):
        g = T.BATCH_GAP_SECONDS
        self.assertEqual(len(T.batches(stream(mk(0), mk(g - 0.1)))), 1)
        self.assertEqual(len(T.batches(stream(mk(0), mk(g + 0.1)))), 2)


class TestStrengthGrading(unittest.TestCase):
    """The honesty gate: repeats inside one write are not recurrence."""

    def test_one_batch_is_named_as_not_evidence_over_time(self):
        s, why = T.strength(stream(mk(0), mk(0.01), mk(0.02), mk(0.03)))
        self.assertEqual(s, "one-batch")
        self.assertIn("not evidence of recurrence over time", why)

    def test_single_occurrence_is_not_a_repeat(self):
        self.assertEqual(T.strength(stream(mk(0)))[0], "single")

    def test_minutes_apart_is_one_session(self):
        self.assertEqual(T.strength(stream(mk(0), mk(600)))[0], "one-session")

    def test_hours_apart_is_one_day(self):
        self.assertEqual(T.strength(stream(mk(0), mk(7200)))[0], "one-day")

    def test_days_apart_is_sustained(self):
        self.assertEqual(T.strength(stream(mk(0), mk(3 * 86400)))[0], "sustained")

    def test_sustained_outranks_a_larger_one_batch_count(self):
        """A signal seen twice over days must be reported above one seen ten
        times in a single write."""
        events = stream(
            *[mk(i * 0.01, signals=(("blocker", "batched"),)) for i in range(10)],
            mk(0, signals=(("blocker", "spread"),)),
            mk(3 * 86400, signals=(("blocker", "spread"),)))
        out = T.recurring_report(events, 2)
        self.assertLess(out.index("blocker=spread"), out.index("blocker=batched"))
        self.assertIn("[sustained]", out)
        self.assertIn("[one-batch]", out)


class TestRecurrence(unittest.TestCase):
    def test_minimum_count_is_respected(self):
        events = stream(mk(0, signals=(("blocker", "once"),)))
        self.assertIn("nothing repeats yet", T.recurring_report(events, 2))

    def test_a_signal_is_counted_across_sources(self):
        events = stream(
            mk(0, source="mixer-run", signals=(("evidence", "computation"),)),
            mk(5000, source="eye-obs", signals=(("evidence", "computation"),)))
        out = T.recurring_report(events, 2)
        self.assertIn("evidence=computation", out)
        self.assertIn("eye-obs, mixer-run", out)


class TestContext(unittest.TestCase):
    """What is going on either side of an occurrence."""

    def test_before_and_after_are_taken_from_the_ordered_stream(self):
        events = stream(
            mk(0, source="commit", kind="fix", label="before-1", signals=()),
            mk(10, source="handoff", kind="seal", label="target",
               signals=(("transport", "damaged-in-transit"),)),
            mk(20, source="commit", kind="ci", label="after-1", signals=()))
        out = T.context_report(events, "transport=damaged", span=1)
        self.assertIn("before  commit", out)
        self.assertIn("> HERE", out)
        self.assertIn("after   commit", out)

    def test_aggregate_names_what_most_often_precedes(self):
        events = stream(
            mk(0, source="commit", kind="acc", label="c1", signals=()),
            mk(10, source="eye-obs", kind="silent", label="e1",
               signals=(("blocker", "needs sage"),)),
            mk(20000, source="commit", kind="acc", label="c2", signals=()),
            mk(20010, source="eye-obs", kind="silent", label="e2",
               signals=(("blocker", "needs sage"),)))
        out = T.context_report(events, "blocker=needs sage", span=1)
        self.assertIn("most often immediately before:", out)
        self.assertIn("2x  commit/acc", out)

    def test_unknown_signal_says_so(self):
        self.assertIn("no signal matching", T.context_report(stream(mk(0)), "nope"))


class TestBeforeAndAfter(unittest.TestCase):
    def test_anchor_resolves_by_id_prefix(self):
        events = stream(mk(0, source="commit", kind="acc", label="abc1234",
                           signals=(), ident="abc1234"))
        t, what = T.resolve_anchor(events, "abc12")
        self.assertIsNotNone(t)
        self.assertIn("commit", what)

    def test_anchor_resolves_by_timestamp(self):
        t, _ = T.resolve_anchor(stream(mk(0)), "2026-09-13T12:00:00+00:00")
        self.assertEqual(t, T0)

    def test_unknown_anchor_is_reported_not_guessed(self):
        self.assertIn("no commit", T.around_report(stream(mk(0)), "zzzzz"))

    def test_a_verdict_flip_across_the_anchor_is_named(self):
        events = stream(
            mk(0, source="eye-obs", kind="silent", label="a", signals=(), ident="a"),
            mk(100, source="commit", kind="acc", label="deadbee", signals=(),
               ident="deadbee"),
            mk(200, source="eye-obs", kind="supports", label="a", signals=(),
               ident="a"))
        out = T.around_report(events, "deadbee")
        self.assertIn("verdict changed across the anchor", out)
        self.assertIn("a: silent -> supports", out)

    def test_a_new_blocker_after_the_anchor_is_named(self):
        events = stream(
            mk(0, source="commit", kind="acc", label="aaaaaaa", signals=(),
               ident="aaaaaaa"),
            mk(100, source="eye-obs", kind="silent", label="e",
               signals=(("blocker", "needs magma"),)))
        out = T.around_report(events, "aaaaaaa")
        self.assertIn("+ needs magma", out)


class TestWindowHonesty(unittest.TestCase):
    def test_a_single_write_is_labelled_as_having_no_spread(self):
        out = T.window_report(stream(mk(0), mk(0.01)), [])
        self.assertIn("single write — no temporal spread", out)

    def test_undated_records_are_excluded_and_declared(self):
        undated = [T.ev(None, "postrun", "mix", "row", (), None, None)] * 848
        out = T.window_report(stream(mk(0), mk(60)), undated)
        self.assertIn("848 records carry no timestamp", out)
        self.assertIn("cannot support a before/after claim", out)

    def test_empty_is_not_an_error(self):
        self.assertIn("nothing recorded", T.window_report([], []))


class TestLiveLedgers(unittest.TestCase):
    def test_the_real_stream_orders_and_indexes(self):
        events, undated = T.collect_events()
        if not events:
            self.skipTest("no ledgers present")
        self.assertEqual([e["ordinal"] for e in events], list(range(len(events))))
        self.assertEqual(events, sorted(events, key=lambda e: e["utc"]))

    def test_the_shared_blocker_is_not_sold_as_a_time_trend(self):
        """Four eyes blocked on one bridge is a fan-in, not a recurrence."""
        events, _ = T.collect_events()
        if not events:
            self.skipTest("no ledgers present")
        idx = T.signal_index(events)
        hits = [k for k in idx if k.startswith("blocker=exact class-group")]
        if not hits:
            self.skipTest("class-group blocker not on record")
        self.assertEqual(T.strength(idx[hits[0]])[0], "one-batch")


if __name__ == "__main__":
    unittest.main(verbosity=1)
