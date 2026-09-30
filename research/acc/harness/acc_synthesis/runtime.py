"""Small durable task kernel and bounded JSON subprocess transport.

Only the task/event database is authoritative.  A model response is data, never
an automatic declaration that an ACC result is valid.  This module has no model
provider, submission client, search algorithm, or background retry policy.
"""

from __future__ import annotations

import contextlib
import json
import math
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import tempfile
import time
import uuid
from typing import Any, Iterator


class HarnessError(RuntimeError):
    """An explicit failed operation; ``code`` is suitable for programmatic use."""

    def __init__(self, message: str, code: str = "harness_error") -> None:
        super().__init__(message)
        self.code = code


def _json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    except (TypeError, ValueError, RecursionError) as exc:
        raise HarnessError("Value is not finite JSON data", "invalid_json") from exc


def _positive(value: float, name: str) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise HarnessError(f"{name} must be finite and positive", "invalid_argument") from exc
    if not math.isfinite(value) or value <= 0:
        raise HarnessError(f"{name} must be finite and positive", "invalid_argument")
    return value


class Store:
    """SQLite WAL/FULL state, append-only events, and token-fenced task leases.

    Statuses: queued, running, completed, failed, interrupted.  An interrupted
    or failed task is retained and never automatically queued again.  To make
    a justified new attempt, enqueue a new unique key referring to that task.
    Each method uses its own connection, allowing separate processes and
    threads to coordinate through the same file.
    """

    def __init__(self, path: str | os.PathLike[str]) -> None:
        if str(path) == ":memory:":
            raise HarnessError("A durable database file is required", "invalid_argument")
        self.path = str(Path(path).expanduser().resolve())
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with contextlib.closing(self._connect()) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
        with self._transaction() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS control (
                singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
                stopped INTEGER NOT NULL CHECK (stopped IN (0, 1)),
                reason TEXT NOT NULL, updated_at REAL NOT NULL
            )""")
            conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                payload TEXT NOT NULL,
                unique_key TEXT NOT NULL UNIQUE,
                family TEXT NOT NULL,
                status TEXT NOT NULL CHECK
                    (status IN ('queued','running','completed','failed','interrupted')),
                attempts INTEGER NOT NULL DEFAULT 0,
                token TEXT,
                lease_until REAL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                result TEXT,
                error TEXT,
                CHECK ((status = 'running' AND token IS NOT NULL AND lease_until IS NOT NULL)
                    OR (status != 'running' AND token IS NULL AND lease_until IS NULL))
            )""")
            conn.execute("""CREATE UNIQUE INDEX IF NOT EXISTS one_running_family
                ON tasks(family) WHERE status = 'running' AND family != ''""")
            conn.execute("CREATE INDEX IF NOT EXISTS tasks_queue ON tasks(status, role, id)")
            conn.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                at REAL NOT NULL, kind TEXT NOT NULL, payload TEXT NOT NULL
            )""")
            conn.execute("""CREATE TRIGGER IF NOT EXISTS events_no_update
                BEFORE UPDATE ON events BEGIN
                SELECT RAISE(ABORT, 'events are append-only'); END""")
            conn.execute("""CREATE TRIGGER IF NOT EXISTS events_no_delete
                BEFORE DELETE ON events BEGIN
                SELECT RAISE(ABORT, 'events are append-only'); END""")
            now = time.time()
            created = conn.execute(
                "INSERT OR IGNORE INTO control VALUES (1, 0, '', ?)", (now,)
            ).rowcount
            if created:
                self._event(conn, "store.created", {"schema": 1}, now)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=10000")
        conn.execute("PRAGMA synchronous=FULL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    @contextlib.contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        with contextlib.closing(self._connect()) as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                yield conn
            except BaseException:
                conn.rollback()
                raise
            else:
                conn.commit()

    @staticmethod
    def _event(conn: sqlite3.Connection, kind: str, payload: Any, now: float) -> int:
        cursor = conn.execute(
            "INSERT INTO events(at, kind, payload) VALUES (?, ?, ?)",
            (now, kind, _json(payload)),
        )
        return int(cursor.lastrowid)

    @staticmethod
    def _is_stopped(conn: sqlite3.Connection) -> bool:
        return bool(conn.execute("SELECT stopped FROM control WHERE singleton=1").fetchone()[0])

    @staticmethod
    def _task(row: sqlite3.Row | dict) -> dict[str, Any]:
        result = dict(row)
        for key in ("payload", "result", "error"):
            result[key] = json.loads(result[key]) if result[key] is not None else None
        return result

    def enqueue(self, role: str, payload: dict, unique_key: str, family: str = "") -> int:
        if not isinstance(role, str) or not role.strip():
            raise HarnessError("role must be nonempty", "invalid_argument")
        if not isinstance(unique_key, str) or not unique_key:
            raise HarnessError("unique_key must be nonempty", "invalid_argument")
        if not isinstance(family, str) or not isinstance(payload, dict):
            raise HarnessError("family must be a string and payload an object", "invalid_argument")
        encoded = _json(payload)
        with self._transaction() as conn:
            old = conn.execute(
                "SELECT id,role,payload,family FROM tasks WHERE unique_key=?", (unique_key,)
            ).fetchone()
            if old:
                if old["role"] != role or old["family"] != family or json.loads(old["payload"]) != json.loads(encoded):
                    raise HarnessError(
                        "unique_key already identifies a different task",
                        "idempotency_conflict",
                    )
                return int(old["id"])
            now = time.time()
            cursor = conn.execute("""INSERT INTO tasks
                (role,payload,unique_key,family,status,created_at,updated_at)
                VALUES (?,?,?,?,'queued',?,?)""", (role, encoded, unique_key, family, now, now))
            task_id = int(cursor.lastrowid)
            self._event(conn, "task.enqueued", {
                "id": task_id, "role": role, "payload": payload,
                "unique_key": unique_key, "family": family,
            }, now)
            return task_id

    def _recover(self, conn: sqlite3.Connection, now: float) -> int:
        expired = conn.execute(
            "SELECT id,token,lease_until FROM tasks WHERE status='running' AND lease_until<=?",
            (now,),
        ).fetchall()
        for row in expired:
            conn.execute("""UPDATE tasks SET status='interrupted',token=NULL,
                lease_until=NULL,updated_at=?,error=? WHERE id=?""",
                (now, _json({"code": "lease_expired"}), row["id"]))
            self._event(conn, "task.interrupted", {
                "id": row["id"], "reason": "lease_expired",
                "token": row["token"], "lease_until": row["lease_until"],
            }, now)
        return len(expired)

    def recover(self) -> int:
        """Revoke expired work; a recovery is not permission to repeat it."""
        with self._transaction() as conn:
            return self._recover(conn, time.time())

    def claim(self, role: str | None = None, lease_seconds: float = 300, task_id: int | None = None) -> dict | None:
        duration = _positive(lease_seconds, "lease_seconds")
        with self._transaction() as conn:
            now = time.time()
            self._recover(conn, now)
            if self._is_stopped(conn):
                return None
            row = conn.execute("""SELECT q.* FROM tasks AS q
                WHERE q.status='queued' AND (? IS NULL OR q.role=?)
                AND (? IS NULL OR q.id=?)
                AND (q.family='' OR NOT EXISTS (
                    SELECT 1 FROM tasks AS r
                    WHERE r.status='running' AND r.family=q.family))
                ORDER BY q.id LIMIT 1""", (role, role, task_id, task_id)).fetchone()
            if row is None:
                return None
            token = uuid.uuid4().hex
            lease_until = now + duration
            if not math.isfinite(lease_until):
                raise HarnessError("lease deadline must be finite", "invalid_argument")
            conn.execute("""UPDATE tasks SET status='running',attempts=attempts+1,
                token=?,lease_until=?,updated_at=? WHERE id=?""",
                (token, lease_until, now, row["id"]))
            claimed = self._task(conn.execute("SELECT * FROM tasks WHERE id=?", (row["id"],)).fetchone())
            self._event(conn, "task.claimed", {
                "id": claimed["id"], "role": claimed["role"], "family": claimed["family"],
                "token": token, "lease_until": lease_until, "attempts": claimed["attempts"],
            }, now)
            return claimed

    def _leased(self, conn: sqlite3.Connection, task_id: int, token: str, now: float) -> sqlite3.Row:
        if self._is_stopped(conn):
            raise HarnessError("Harness is stopped", "stopped")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None or row["status"] != "running" or row["token"] != token:
            raise HarnessError(f"Task {task_id} has no matching active lease", "stale_lease")
        if row["lease_until"] <= now:
            raise HarnessError(f"Task {task_id} lease expired", "lease_expired")
        return row

    def heartbeat(self, task_id: int, token: str, lease_seconds: float = 300) -> float:
        duration = _positive(lease_seconds, "lease_seconds")
        with self._transaction() as conn:
            now = time.time()
            self._leased(conn, task_id, token, now)
            deadline = now + duration
            if not math.isfinite(deadline):
                raise HarnessError("lease deadline must be finite", "invalid_argument")
            conn.execute("UPDATE tasks SET lease_until=?,updated_at=? WHERE id=?",
                         (deadline, now, task_id))
            self._event(conn, "task.heartbeat", {"id": task_id, "lease_until": deadline}, now)
            return deadline

    def finish(self, task_id: int, token: str, result: dict) -> None:
        encoded = _json(result)
        with self._transaction() as conn:
            now = time.time()
            self._leased(conn, task_id, token, now)
            conn.execute("""UPDATE tasks SET status='completed',result=?,error=NULL,
                token=NULL,lease_until=NULL,updated_at=? WHERE id=?""", (encoded, now, task_id))
            self._event(conn, "task.completed", {"id": task_id, "result": result}, now)

    def fail(self, task_id: int, token: str, error: Any) -> None:
        encoded = _json(error)
        with self._transaction() as conn:
            now = time.time()
            self._leased(conn, task_id, token, now)
            conn.execute("""UPDATE tasks SET status='failed',error=?,token=NULL,
                lease_until=NULL,updated_at=? WHERE id=?""", (encoded, now, task_id))
            self._event(conn, "task.failed", {"id": task_id, "error": error}, now)

    def stop(self, reason: str) -> None:
        if not isinstance(reason, str):
            raise HarnessError("stop reason must be text", "invalid_argument")
        with self._transaction() as conn:
            now = time.time()
            running = conn.execute("SELECT id,token FROM tasks WHERE status='running'").fetchall()
            conn.execute("UPDATE control SET stopped=1,reason=?,updated_at=? WHERE singleton=1",
                         (reason, now))
            for row in running:
                conn.execute("""UPDATE tasks SET status='interrupted',error=?,token=NULL,
                    lease_until=NULL,updated_at=? WHERE id=?""",
                    (_json({"code": "stopped", "reason": reason}), now, row["id"]))
                self._event(conn, "task.interrupted", {
                    "id": row["id"], "token": row["token"], "reason": "stopped",
                }, now)
            self._event(conn, "harness.stopped", {"reason": reason}, now)

    def resume(self) -> None:
        with self._transaction() as conn:
            now = time.time()
            conn.execute("UPDATE control SET stopped=0,reason='',updated_at=? WHERE singleton=1", (now,))
            self._event(conn, "harness.resumed", {}, now)

    def stopped(self) -> bool:
        with contextlib.closing(self._connect()) as conn:
            return self._is_stopped(conn)

    def tasks(self, status: str | None = None) -> list[dict]:
        with contextlib.closing(self._connect()) as conn:
            rows = conn.execute("SELECT * FROM tasks WHERE (? IS NULL OR status=?) ORDER BY id",
                                (status, status)).fetchall()
            return [self._task(row) for row in rows]

    def event(self, kind: str, payload: Any) -> int:
        if not isinstance(kind, str) or not kind:
            raise HarnessError("event kind must be nonempty", "invalid_argument")
        with self._transaction() as conn:
            return self._event(conn, kind, payload, time.time())

    def admit(self, kind: str, payload: Any) -> int:
        """Record an authoritative admission only if stop has not committed.

        The stop check and event append share one write transaction.  An export
        made from the returned event is a historical view of that admission;
        it is not a fresh admission or permission to submit anything.
        """
        if not isinstance(kind, str) or not kind:
            raise HarnessError("event kind must be nonempty", "invalid_argument")
        with self._transaction() as conn:
            if self._is_stopped(conn):
                raise HarnessError("Harness is stopped", "stopped")
            return self._event(conn, kind, payload, time.time())

    def events(self) -> list[dict]:
        with contextlib.closing(self._connect()) as conn:
            rows = conn.execute("SELECT * FROM events ORDER BY id").fetchall()
            return [{**dict(row), "payload": json.loads(row["payload"])} for row in rows]


def _terminate(proc: subprocess.Popen) -> None:
    """On POSIX terminate the whole session, including inherited child jobs."""
    if os.name == "posix":
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            proc.wait(timeout=0.2)
        except subprocess.TimeoutExpired:
            pass
        # The leader may exit before its descendants; kill the group regardless.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif proc.poll() is None:
        proc.kill()
    try:
        proc.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass


def run_command(
    command: list[str],
    request: dict,
    timeout_seconds: float,
    store: Store | None = None,
    lease: dict | None = None,
    max_output_bytes: int = 1_048_576,
) -> dict:
    """Run a JSON-in/JSON-out command with no shell and return its JSON object.

    Raises HarnessError on nonzero exit, malformed/non-object JSON, output
    overflow, stop, lost lease, or timeout.  stdout and stderr go to temporary
    files, avoiding pipe deadlocks and unbounded RAM; their combined file size
    is polled and overflow terminates the process group.  A fast producer may
    exceed the file cap between polls, but never causes an unbounded read into
    memory.  An optional lease is renewed at one third of its initial remaining
    duration.  This transport does not finish/fail tasks or certify results.
    """
    timeout = _positive(timeout_seconds, "timeout_seconds")
    if not isinstance(command, list) or not command or any(not isinstance(x, str) for x in command):
        raise HarnessError("command must be a nonempty string argument list", "invalid_argument")
    if not command[0] or not isinstance(request, dict):
        raise HarnessError("command executable and JSON request object are required", "invalid_argument")
    if isinstance(max_output_bytes, bool) or not isinstance(max_output_bytes, int) or max_output_bytes < 1:
        raise HarnessError("max_output_bytes must be a positive integer", "invalid_argument")
    if lease is not None and store is None:
        raise HarnessError("A lease requires its Store", "invalid_argument")
    request_bytes = (_json(request) + "\n").encode("utf-8")
    heartbeat_interval = 30.0
    duration = 300.0
    if lease is not None:
        try:
            duration = float(lease["lease_until"]) - time.time()
            task_id, token = lease["id"], lease["token"]
        except (KeyError, TypeError, ValueError) as exc:
            raise HarnessError("lease must be a claim() result", "invalid_argument") from exc
        if not math.isfinite(duration) or duration <= 0:
            raise HarnessError("Lease expired before command launch", "lease_expired")
        heartbeat_interval = max(0.001, min(30.0, duration / 3.0))

    def check_control(renew: bool = False) -> None:
        if store is not None and store.stopped():
            raise HarnessError("Harness stopped while command was active", "stopped")
        if lease is not None and renew:
            store.heartbeat(task_id, token, lease_seconds=duration)

    check_control(renew=True)
    started = time.monotonic()
    deadline = started + timeout
    next_heartbeat = started + heartbeat_interval
    with tempfile.TemporaryFile() as stdin, tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        stdin.write(request_bytes)
        stdin.seek(0)
        try:
            proc = subprocess.Popen(
                command, stdin=stdin, stdout=stdout, stderr=stderr,
                shell=False, start_new_session=(os.name == "posix"),
            )
        except (OSError, ValueError) as exc:
            raise HarnessError(f"Command could not start: {exc}", "launch_failed") from exc
        cleaned_up = False
        try:
            while True:
                now = time.monotonic()
                renew = lease is not None and now >= next_heartbeat
                check_control(renew=renew)
                if renew:
                    next_heartbeat = time.monotonic() + heartbeat_interval
                now = time.monotonic()
                out_size = os.fstat(stdout.fileno()).st_size
                err_size = os.fstat(stderr.fileno()).st_size
                if out_size + err_size > max_output_bytes:
                    raise HarnessError("Command exceeded its combined output cap", "output_limit")
                if now >= deadline:
                    raise HarnessError("Command exceeded its deadline", "timeout")
                if proc.poll() is not None:
                    # A child must not keep writing after the command leader exits.
                    _terminate(proc)
                    cleaned_up = True
                    check_control(renew=True)
                    if time.monotonic() >= deadline:
                        raise HarnessError("Command exceeded its deadline", "timeout")
                    out_size = os.fstat(stdout.fileno()).st_size
                    err_size = os.fstat(stderr.fileno()).st_size
                    if out_size + err_size > max_output_bytes:
                        raise HarnessError("Command exceeded its combined output cap", "output_limit")
                    break
                delay = min(0.05, deadline - now)
                if lease is not None:
                    delay = min(delay, max(0.001, next_heartbeat - now))
                try:
                    proc.wait(timeout=max(0.001, delay))
                except subprocess.TimeoutExpired:
                    pass
            if proc.returncode != 0:
                # Do not echo arbitrary subprocess output or the inherited environment.
                raise HarnessError(f"Command exited with status {proc.returncode}", "command_failed")
            stdout.seek(0)
            raw = stdout.read(max_output_bytes + 1)
            try:
                parsed = json.loads(raw.decode("utf-8"))
                # This also catches exponent overflow such as 1e999, which the
                # standard parser accepts and converts to infinity.
                _json(parsed)
            except (UnicodeDecodeError, ValueError, RecursionError, HarnessError) as exc:
                raise HarnessError("Command stdout is not one valid finite JSON object", "invalid_output") from exc
            if not isinstance(parsed, dict):
                raise HarnessError("Command stdout must contain one JSON object", "invalid_output")
            return parsed
        finally:
            if not cleaned_up:
                _terminate(proc)
