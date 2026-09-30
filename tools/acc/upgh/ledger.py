"""Z, the ledger register: an append-only, hash-chained JSON Lines file.

Nothing counts until its line is written and fsynced. Every other piece of
harness state (tasks, best paths, parked misses, heat, stop) is a fold over
these lines, so the ledger is the only thing that has to survive.

The chain makes accidental edits and torn writes visible. It is not a
security boundary: anyone who can write the file can rebuild the chain.
"""
from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path

GRADES = ("T", "V", "C", "L", "H")
GENESIS = "0" * 64


class LedgerError(Exception):
    pass


def canon(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(text: str) -> float:
    return dt.datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(
        tzinfo=dt.timezone.utc).timestamp()


def event_hash(event: dict) -> str:
    body = {k: v for k, v in event.items() if k != "hash"}
    return sha256_bytes(canon(body))


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.lock_path = self.path.with_name(self.path.name + ".lock")

    @contextlib.contextmanager
    def locked(self):
        """One writer at a time, across processes."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.lock_path, "a+b") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)

    def _read_lines(self):
        if not self.path.exists():
            return []
        raw = self.path.read_bytes()
        if raw and not raw.endswith(b"\n"):
            raise LedgerError("torn last line in %s: run `upgh doctor --repair-tail`" % self.path)
        return raw.decode("utf-8").splitlines()

    def events(self) -> list[dict]:
        """Parse and verify the whole chain. Fails closed on any break."""
        out, prev = [], GENESIS
        for n, line in enumerate(self._read_lines(), 1):
            try:
                event = json.loads(line)
            except ValueError as exc:
                raise LedgerError("line %d is not JSON: %s" % (n, exc))
            if event.get("seq") != n:
                raise LedgerError("line %d has seq %r" % (n, event.get("seq")))
            if event.get("prev") != prev:
                raise LedgerError("line %d does not chain to line %d" % (n, n - 1))
            if event_hash(event) != event.get("hash"):
                raise LedgerError("line %d hash mismatch (edited after writing?)" % n)
            out.append(event)
            prev = event["hash"]
        return out

    def _tail(self):
        lines = self._read_lines()
        if not lines:
            return 0, GENESIS
        last = json.loads(lines[-1])
        return last["seq"], last["hash"]

    def append_many(self, items) -> list[dict]:
        """items: iterable of (kind, data, grade). Written under one lock, one fsync."""
        items = list(items)
        if not items:
            return []
        for kind, data, grade in items:
            if grade not in GRADES:
                raise LedgerError("unknown grade %r for %s" % (grade, kind))
            if not isinstance(kind, str) or not kind:
                raise LedgerError("event kind must be a nonempty string")
        with self.locked():
            seq, prev = self._tail()
            at = now_iso()
            written, chunk = [], []
            for kind, data, grade in items:
                seq += 1
                event = {"seq": seq, "at": at, "kind": kind, "grade": grade,
                         "data": data, "prev": prev}
                event["hash"] = event_hash(event)
                prev = event["hash"]
                chunk.append(json.dumps(event, sort_keys=True, ensure_ascii=False,
                                        allow_nan=False) + "\n")
                written.append(event)
            fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
            try:
                os.write(fd, "".join(chunk).encode("utf-8"))
                os.fsync(fd)
            finally:
                os.close(fd)
            return written

    def append(self, kind, data, grade) -> dict:
        return self.append_many([(kind, data, grade)])[0]

    def repair_tail(self) -> str | None:
        """Move a torn final line aside. The torn bytes are kept, never deleted."""
        with self.locked():
            if not self.path.exists():
                return None
            raw = self.path.read_bytes()
            if not raw or raw.endswith(b"\n"):
                return None
            cut = raw.rfind(b"\n") + 1
            torn = self.path.with_name(self.path.name + ".torn-" + now_iso().replace(":", ""))
            torn.write_bytes(raw[cut:])
            with open(self.path, "r+b") as fh:
                fh.truncate(cut)
                fh.flush()
                os.fsync(fh.fileno())
            return str(torn)
