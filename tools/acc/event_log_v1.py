"""Immutable raw event stream for the Compound Eye.

Jeromie's rule, which this file exists to enforce:

    All eyes on always means every eye leaves a record. Mixing may change what
    influences a decision, but it may never erase what an eye saw -- or failed
    to see.

The run ledger records outcomes. This records EVENTS: every input, state,
action, eye reading, failure, decision and relationship, appended once and
never rewritten. Reports are derived from it and never replace it.

Four properties, each with a test that tries to break it:

  TAMPER-EVIDENT   every event carries the digest of the previous one, so the
                   stream is a hash chain. Editing or deleting any event breaks
                   every later link, and `verify` names the first break.

  TORN-WRITE SAFE  a record is one line written under an exclusive lock and
                   fsynced. A process killed mid-append leaves a short final
                   line, which fails its own digest and is reported as TORN
                   rather than parsed as data.

  CONCURRENT SAFE  appends take flock(LOCK_EX). Two writers interleave whole
                   records, never bytes.

  EXACTLY TYPED    unsafe integers are rejected RECURSIVELY OVER THE WHOLE
                   EVENT, not over one field. A JSON number past 2^53 has
                   already lost digits; quote it.

Storage. States are content-addressed: a state is written once under its
sha256 and referenced everywhere after. A search transition stores the parent
reference and the move, and marks the child derivable, so a million-state
search costs one chunk per distinct state and not one copy per visit.

    python3 tools/acc/event_log_v1.py --verify
    python3 tools/acc/event_log_v1.py --summary
"""

import argparse
import fcntl
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(os.environ.get("ACC_EVENT_DIR", ROOT / "ledger" / "events"))
STREAM = "stream_v1.jsonl"
CHUNKS = "chunks"

MAX_EXACT = 2 ** 53 - 1
GENESIS = "0" * 64

# An eye must file exactly one of these. There is no seventh option and there
# is no silence: an eye that is not on the roster is a blind spot, and an eye
# on the roster that files nothing is a defect in the run, not a shrug.
EYE_STATES = {
    "observed",      # it saw something and says what
    "silent",        # the instrument exists and has no input it can see
    "blocked",       # it is waiting on a named capability or artifact
    "failed",        # it ran and errored; the error is the record
    "contradicted",  # another eye's reading is incompatible with this one
    "disabled",      # deliberately off, with a reason; still on the roster
}

# Relationships are first-class permanent objects, not something a report
# derives and then forgets.
RELATIONSHIPS = {
    "supports", "contradicts", "shared-assumption", "shared-source",
    "derived-from", "duplicates", "supersedes", "failed-to-surface",
    "candidate-led-to-certificate", "candidate-later-became-useful",
}

KINDS = {
    "input", "state", "action", "eye-reading", "failure", "decision",
    "relationship", "search-transition", "checkpoint", "certificate",
    "import", "note",
}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def unsafe_integers(value, where="event"):
    """Recursive over the WHOLE event. The earlier guards checked one field."""
    bad = []
    if isinstance(value, bool):
        return bad
    if isinstance(value, (int, float)) and abs(value) > MAX_EXACT:
        bad.append((where, repr(value)))
    elif isinstance(value, dict):
        for k, v in value.items():
            if isinstance(k, (int, float)) and abs(k) > MAX_EXACT:
                bad.append((f"{where}.<key>", repr(k)))
            bad += unsafe_integers(v, f"{where}.{k}")
    elif isinstance(value, (list, tuple)):
        for i, v in enumerate(value):
            bad += unsafe_integers(v, f"{where}[{i}]")
    return bad


class EventLog:
    def __init__(self, directory=None):
        self.dir = Path(directory) if directory else DIR
        self.path = self.dir / STREAM
        self.chunks = self.dir / CHUNKS

    # --- content-addressed chunk store ---------------------------------------

    def put_chunk(self, obj):
        """Store a state once, by content. Returns its reference."""
        blob = canonical(obj)
        ref = sha256(blob)
        p = self.chunks / ref[:2] / f"{ref}.json"
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(".tmp")
            tmp.write_bytes(blob)
            os.replace(tmp, p)          # atomic: never a half-written chunk
        return ref

    def get_chunk(self, ref):
        p = self.chunks / ref[:2] / f"{ref}.json"
        return json.loads(p.read_text()) if p.exists() else None

    # --- the stream ----------------------------------------------------------

    def _tail(self):
        """(seq, digest) of the last intact record, without parsing the file."""
        if not self.path.exists():
            return -1, GENESIS
        last = None
        for line in self.path.read_text(errors="replace").splitlines():
            if line.strip():
                try:
                    last = json.loads(line)
                except json.JSONDecodeError:
                    continue        # a torn tail is not a link; verify reports it
        if last is None:
            return -1, GENESIS
        return last.get("seq", -1), last.get("digest", GENESIS)

    def append(self, kind, body, run_id="default"):
        if kind not in KINDS:
            raise ValueError(f"unknown event kind {kind!r}; one of {sorted(KINDS)}")
        bad = unsafe_integers(body, "body")
        if bad:
            raise ValueError(
                "numbers past 2^53 lose digits in JSON; quote them as strings — "
                + "; ".join(f"{w} = {v}" for w, v in bad))

        self.dir.mkdir(parents=True, exist_ok=True)
        # The lock covers read-tail AND write, so two writers cannot both read
        # the same prev and fork the chain.
        with open(self.path, "a+") as fh:
            fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
            try:
                seq, prev = self._tail()
                rec = {"schema": "acc-event-v1", "seq": seq + 1, "ts": now(),
                       "run_id": run_id, "kind": kind, "body": body, "prev": prev}
                rec["digest"] = sha256(canonical(
                    {k: rec[k] for k in ("seq", "ts", "run_id", "kind", "body", "prev")}))
                fh.write(json.dumps(rec) + "\n")
                fh.flush()
                os.fsync(fh.fileno())   # survive a kill between write and close
            finally:
                fcntl.flock(fh.fileno(), fcntl.LOCK_UN)
        return rec

    # --- typed helpers -------------------------------------------------------

    def eye_reading(self, run_id, claim_id, eye_id, state, output=None,
                    reason=None, **extra):
        if state not in EYE_STATES:
            raise ValueError(f"eye state must be one of {sorted(EYE_STATES)}")
        if state in ("blocked", "disabled", "failed") and not reason:
            raise ValueError(f"state {state!r} requires a reason; that is the "
                             f"whole point of keeping the eye on the roster")
        return self.append("eye-reading", {
            "claim_id": claim_id, "eye_id": eye_id, "state": state,
            "output": output, "reason": reason, **extra}, run_id)

    def relationship(self, run_id, kind, source, target, evidence=None, **extra):
        if kind not in RELATIONSHIPS:
            raise ValueError(f"relationship must be one of {sorted(RELATIONSHIPS)}")
        return self.append("relationship", {
            "relation": kind, "source": source, "target": target,
            "evidence": evidence, **extra}, run_id)

    def search_transition(self, run_id, parent_ref, move, decision,
                          reason=None, child_ref=None, eyes=None):
        """Deterministic delta: the child is recoverable from parent + move, so
        it is not stored again unless the caller wants it addressable."""
        return self.append("search-transition", {
            "parent": parent_ref, "move": move,
            "child": child_ref, "child_derivable": child_ref is None,
            "decision": decision, "reason": reason, "eyes": eyes or {}}, run_id)

    # --- verification --------------------------------------------------------

    def read(self):
        """Yields (lineno, record_or_None, raw). None means the line is torn."""
        if not self.path.exists():
            return
        for n, line in enumerate(self.path.read_text(errors="replace").splitlines(), 1):
            if not line.strip():
                continue
            try:
                yield n, json.loads(line), line
            except json.JSONDecodeError:
                yield n, None, line

    def verify(self):
        problems, prev, expect = [], GENESIS, 0
        seen = 0
        for n, rec, raw in self.read():
            if rec is None:
                problems.append(f"line {n}: TORN — not parseable as JSON "
                                f"({len(raw)} bytes). A killed writer looks "
                                f"exactly like this.")
                continue
            seen += 1
            want = sha256(canonical(
                {k: rec.get(k) for k in ("seq", "ts", "run_id", "kind", "body", "prev")}))
            if rec.get("digest") != want:
                problems.append(f"line {n} (seq {rec.get('seq')}): digest mismatch — "
                                f"the record was altered after it was written")
            if rec.get("prev") != prev:
                problems.append(f"line {n} (seq {rec.get('seq')}): chain break — "
                                f"prev is {str(rec.get('prev'))[:12]}, expected "
                                f"{prev[:12]}. Something earlier was edited or removed.")
            if rec.get("seq") != expect:
                problems.append(f"line {n}: seq {rec.get('seq')}, expected {expect}")
            prev = rec.get("digest", GENESIS)
            expect = rec.get("seq", expect) + 1
            bad = unsafe_integers(rec.get("body"), "body")
            if bad:
                problems.append(f"line {n}: unsafe integer stored: {bad[0][0]}")
        return seen, problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--dir")
    a = ap.parse_args(argv)

    log = EventLog(a.dir)
    n, problems = log.verify()
    if a.verify or not a.summary:
        if problems:
            print(f"{len(problems)} problem(s) in {n} event(s):")
            for p in problems:
                print("  " + p)
            return 1
        print(f"event stream OK — {n} events, hash chain intact")
        if not a.summary:
            return 0

    from collections import Counter
    kinds, states, rels = Counter(), Counter(), Counter()
    for _, rec, _ in log.read():
        if not rec:
            continue
        kinds[rec["kind"]] += 1
        if rec["kind"] == "eye-reading":
            states[rec["body"]["state"]] += 1
        if rec["kind"] == "relationship":
            rels[rec["body"]["relation"]] += 1
    print(f"\n{n} events")
    for k, v in kinds.most_common():
        print(f"  {k:<20}{v:>6}")
    if states:
        print("\neye states filed")
        for k in sorted(EYE_STATES):
            print(f"  {k:<20}{states.get(k, 0):>6}")
    if rels:
        print("\nrelationships")
        for k, v in rels.most_common():
            print(f"  {k:<32}{v:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
