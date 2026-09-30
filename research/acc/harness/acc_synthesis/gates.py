"""Exact-artifact gates for an externally supplied, pinned ACC checker.

This module is not an ACC solver or verifier implementation.  It checks the
identity of a user-selected checker, requires its replay receipt, and applies
fresh board eligibility rules.  Nothing here submits a candidate.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable


_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")
_GRADES = {"T", "V", "C", "L", "H"}
_OUTPUT_LIMIT = 1024 * 1024


def _stop_process(process: subprocess.Popen) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        process.kill()
    process.wait()


def _run_checker(
    command: list[str], root: Path, run_dir: Path, timeout: float,
    cancelled: Callable[[], bool],
) -> tuple[int | None, str | None]:
    """Drain bounded logs while checking stop, receipt size and timeout."""
    receipt_path = run_dir / "receipt.json"
    with (run_dir / "stdout.txt").open("wb") as stdout, (
        run_dir / "stderr.txt"
    ).open("wb") as stderr, selectors.DefaultSelector() as selector:
        process = subprocess.Popen(
            command, cwd=root, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, start_new_session=True,
        )
        selector.register(process.stdout, selectors.EVENT_READ, [stdout, 0])
        selector.register(process.stderr, selectors.EVENT_READ, [stderr, 0])
        deadline = time.monotonic() + timeout
        reason = None
        try:
            while True:
                if cancelled():
                    reason = "checker_cancelled"
                    break
                if receipt_path.exists() and receipt_path.stat().st_size > _OUTPUT_LIMIT:
                    reason = "checker_output_limit"
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    reason = "checker_timeout"
                    break
                for key, _ in selector.select(timeout=min(0.05, remaining)):
                    block = os.read(key.fileobj.fileno(), 65536)
                    if not block:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
                        continue
                    stream, used = key.data
                    available = _OUTPUT_LIMIT - used
                    stream.write(block[:available])
                    key.data[1] += min(len(block), available)
                    if len(block) > available:
                        reason = "checker_output_limit"
                        break
                if reason:
                    break
                if process.poll() is not None and not selector.get_map():
                    break
            if reason:
                _stop_process(process)
            else:
                process.wait()
            # A receipt is written directly by the checker. Detect oversize
            # while it runs and keep the retained failed artifact bounded.
            if receipt_path.exists() and receipt_path.stat().st_size > _OUTPUT_LIMIT:
                with receipt_path.open("r+b") as receipt:
                    receipt.truncate(_OUTPUT_LIMIT)
                reason = reason or "checker_output_limit"
            return process.returncode, reason
        finally:
            if process.poll() is None:
                _stop_process(process)
            for pipe in (process.stdout, process.stderr):
                if pipe is not None:
                    pipe.close()


def _canonical_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(obj: Any) -> str:
    """SHA-256 of sorted-key UTF-8 JSON, with no insignificant whitespace."""
    return hashlib.sha256(_canonical_bytes(obj)).hexdigest()


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _hash_value(value: Any) -> str | None:
    return value.lower() if isinstance(value, str) and _SHA256.fullmatch(value) else None


def _path(value: Any, root: Path) -> Path:
    if not isinstance(value, (str, os.PathLike)) or not str(value):
        raise ValueError("path must be a nonempty string")
    path = Path(value)
    return (path if path.is_absolute() else root / path).resolve()


def _integer(value: Any) -> bool:
    return type(value) is int and value >= 0


def _strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(x, str) for x in value)


def _finite_number(value: Any) -> bool:
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _strict_json(data: bytes) -> Any:
    def no_constant(value: str) -> None:
        raise ValueError("nonfinite JSON number: " + value)

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    return json.loads(data, parse_constant=no_constant, object_pairs_hook=no_duplicates)


def _command(checker: dict[str, Any], pinned: Path, root: Path) -> list[str]:
    """Bind execution to the pinned file, directly or through this Python."""
    command = checker.get("command")
    if not isinstance(command, list) or not command or not all(
        isinstance(arg, str) and arg for arg in command
    ):
        raise ValueError("checker.command must be a nonempty list of strings")
    if not any("{candidate}" in arg for arg in command) or not any(
        "{receipt}" in arg for arg in command
    ):
        raise ValueError("checker command needs {candidate} and {receipt} placeholders")
    command = list(command)
    if command[0] == '{python}':
        command[0] = sys.executable
    first = command[0]
    executable = _path(first, root) if ("/" in first or "\\" in first) else None
    if executable is None:
        found = shutil.which(first)
        if found:
            executable = Path(found).resolve()
        elif _path(first, root) == pinned:
            executable = pinned
    if executable == pinned:
        command[0] = str(pinned)
    elif executable == Path(sys.executable).resolve() and len(command) > 1 and (
        _path(command[1], root) == pinned
    ):
        command[0] = str(executable)
        command[1] = str(pinned)
    else:
        raise ValueError("command must execute the pinned checker directly or with the current Python")
    return command


def verify_candidate(
    candidate: dict[str, Any], config: dict[str, Any], root: Path,
    now: float | None = None, *, cancelled: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Replay a candidate and independently determine current scoring eligibility.

    ``withheld`` means missing/untrusted evidence prevents a ready result.
    ``invalid`` means the candidate or its exact replay fails a required check.
    ``verified_nonscoring`` means replay passed but a fresh board rules it out.
    ``verified_scoring`` means replay and eligibility both passed; it does not
    authorize publication or submission.  Agent claims never replace replay.
    """
    root = Path(root).resolve()
    checked_at = time.time() if now is None else now
    common: dict[str, Any] = {"exact_verified": False, "checked_at": checked_at}

    def result(status: str, reason: str, **details: Any) -> dict[str, Any]:
        return {**common, "status": status, "reason": reason, **details}

    def is_cancelled() -> bool:
        try:
            return bool(cancelled()) if cancelled is not None else False
        except Exception:
            # A broken stop monitor cannot grant a ready result.
            return True

    if is_cancelled():
        return result("withheld", "checker_cancelled")

    if not _finite_number(checked_at):
        return result("withheld", "invalid_check_time")
    if not isinstance(candidate, dict) or not isinstance(config, dict):
        return result("invalid", "malformed_candidate_or_config")
    if (
        not isinstance(candidate.get("row_id"), str) or not candidate["row_id"]
        or candidate.get("track") not in ("AC", "SAC")
        or not _strings(candidate.get("start"))
        or not isinstance(candidate.get("moves"), list)
        or _hash_value(candidate.get("ruleset_sha256")) is None
        or not isinstance(candidate.get("evidence_grade"), str)
        or candidate["evidence_grade"] not in _GRADES
        or "family" not in candidate
    ):
        return result("invalid", "malformed_candidate")
    try:
        candidate_bytes = _canonical_bytes(candidate)
        # JSON round-trip equality excludes tuples/non-string keys and other
        # Python objects whose serialized meaning differs from the supplied one.
        if _strict_json(candidate_bytes) != candidate:
            return result("invalid", "candidate_is_not_plain_json")
    except (ValueError, TypeError, UnicodeError, OverflowError):
        return result("invalid", "candidate_is_not_plain_json")
    common["candidate_sha256"] = hashlib.sha256(candidate_bytes).hexdigest()
    common["row_id"] = candidate["row_id"]
    common["track"] = candidate["track"]
    if candidate["evidence_grade"] == "H":
        return result("withheld", "hypothesis_cannot_authorize_verification")

    try:
        manifest_path = _path(config.get("target_manifest"), root)
        manifest_pin = _hash_value(config.get("target_manifest_sha256"))
        if manifest_pin is None:
            return result("withheld", "target_manifest_pin_missing_or_invalid")
        manifest_bytes = manifest_path.read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != manifest_pin:
            return result("withheld", "target_manifest_hash_mismatch")
        manifest = _strict_json(manifest_bytes)
    except (OSError, ValueError, TypeError, UnicodeError):
        return result("withheld", "target_manifest_unavailable_or_malformed")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("targets"), list):
        return result("withheld", "malformed_target_manifest")
    ruleset = _hash_value(manifest.get("ruleset_sha256"))
    if ruleset is None or ruleset != _hash_value(candidate["ruleset_sha256"]):
        return result("invalid", "ruleset_mismatch")
    targets = [row for row in manifest["targets"] if isinstance(row, dict) and (
        row.get("row_id") == candidate["row_id"] and row.get("track") == candidate["track"]
    )]
    if len(targets) != 1:
        return result("withheld", "target_missing_or_ambiguous")
    target = targets[0]
    if not _strings(target.get("start")) or not _strings(target.get("goal")):
        return result("withheld", "malformed_target")
    if target["start"] != candidate["start"]:
        return result("invalid", "exact_start_mismatch")

    checker = config.get("checker")
    if not isinstance(checker, dict):
        return result("withheld", "checker_not_configured")
    checker_pin = _hash_value(checker.get("sha256"))
    if checker_pin is None:
        return result("withheld", "checker_pin_missing_or_invalid")
    try:
        checker_path = _path(checker.get("path"), root)
        if sha256_file(checker_path) != checker_pin:
            return result("withheld", "checker_hash_mismatch")
        command_template = _command(checker, checker_path, root)
    except (OSError, ValueError, TypeError):
        return result("withheld", "checker_unavailable_or_unsafe_command")
    timeout = checker.get("timeout_seconds", 60)
    if not _finite_number(timeout) or timeout <= 0:
        return result("withheld", "invalid_checker_timeout")
    common["checker_sha256"] = checker_pin
    common["ruleset_sha256"] = ruleset
    try:
        checks = _path(config.get("checks_directory", "state/checks"), root)
        checks.mkdir(parents=True, exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix="check-", dir=checks))
        candidate_path = run_dir / "candidate.json"
        receipt_path = run_dir / "receipt.json"
        candidate_path.write_bytes(candidate_bytes)
        command = []
        for arg in command_template:
            # Literal substitution only: do not interpret arbitrary format
            # expressions supplied in configuration.
            remainder = arg.replace("{candidate}", "").replace("{receipt}", "")
            if "{" in remainder or "}" in remainder:
                return result("withheld", "unknown_checker_command_placeholder")
            command.append(arg.replace("{candidate}", str(candidate_path)).replace(
                "{receipt}", str(receipt_path)
            ))
        common["check_directory"] = str(run_dir)
        returncode, stop_reason = _run_checker(command, root, run_dir, timeout, is_cancelled)
        if stop_reason:
            return result("withheld", stop_reason)
        if is_cancelled():
            return result("withheld", "checker_cancelled")
        if sha256_file(checker_path) != checker_pin:
            return result("withheld", "checker_changed_during_execution")
        if candidate_path.read_bytes() != candidate_bytes:
            return result("withheld", "candidate_changed_during_execution")
        if returncode != 0:
            return result("withheld", "checker_process_failed", returncode=returncode)
        with receipt_path.open("rb") as receipt_file:
            receipt_bytes = receipt_file.read(_OUTPUT_LIMIT + 1)
        if len(receipt_bytes) > _OUTPUT_LIMIT:
            return result("withheld", "checker_output_limit")
        receipt = _strict_json(receipt_bytes)
    except (OSError, ValueError, TypeError, KeyError, IndexError, UnicodeError):
        return result("withheld", "checker_execution_or_receipt_error")
    if not isinstance(receipt, dict):
        return result("withheld", "malformed_checker_receipt")
    if (
        _hash_value(receipt.get("candidate_sha256")) != common["candidate_sha256"]
        or _hash_value(receipt.get("checker_sha256")) != checker_pin
        or _hash_value(receipt.get("ruleset_sha256")) != ruleset
    ):
        return result("withheld", "receipt_binding_mismatch")
    if type(receipt.get("valid")) is not bool:
        return result("withheld", "malformed_checker_receipt")
    common["receipt_path"] = str(receipt_path)
    if not receipt["valid"]:
        return result("invalid", "exact_replay_rejected")
    if (
        not _strings(receipt.get("exact_endpoint"))
        or not _integer(receipt.get("cost"))
        or not _integer(receipt.get("peak_length"))
    ):
        return result("withheld", "malformed_checker_receipt")
    if receipt["cost"] != len(candidate["moves"]):
        return result("invalid", "unit_move_cost_mismatch")
    if receipt["exact_endpoint"] != target["goal"]:
        return result("invalid", "exact_endpoint_mismatch")
    common.update(
        exact_verified=True, evidence_grade="V", cost=receipt["cost"],
        peak_length=receipt["peak_length"], exact_endpoint=receipt["exact_endpoint"],
    )

    # Freshness is measured after replay, when the result can actually become
    # ready. An explicit now value is a deterministic clock for caller/tests.
    if now is None:
        checked_at = time.time()
        common["checked_at"] = checked_at

    try:
        board = _strict_json(_path(config.get("board_snapshot"), root).read_bytes())
    except (OSError, ValueError, TypeError, UnicodeError):
        return result("withheld", "board_unavailable_or_malformed")
    if not isinstance(board, dict) or not isinstance(board.get("rows"), list):
        return result("withheld", "malformed_board")
    if _hash_value(board.get("ruleset_sha256")) != ruleset:
        return result("withheld", "board_ruleset_mismatch")
    observed = board.get("observed_at")
    max_age = config.get("board_max_age_seconds")
    if not _finite_number(observed) or not _finite_number(max_age) or max_age < 0:
        return result("withheld", "invalid_board_clock")
    age = checked_at - observed
    common["board_observed_at"] = observed
    common["board_age_seconds"] = age
    if age < -5:
        return result("withheld", "board_timestamp_in_future")
    if age > max_age:
        return result("withheld", "board_stale")
    rows = [row for row in board["rows"] if isinstance(row, dict) and (
        row.get("row_id") == candidate["row_id"] and row.get("track") == candidate["track"]
    )]
    if len(rows) != 1:
        return result("withheld", "board_row_missing_or_ambiguous")
    row = rows[0]
    if not _integer(row.get("record")) or type(row.get("held_by_us")) is not bool:
        return result("withheld", "board_row_eligibility_unknown")
    common["record"] = row["record"]
    common["held_by_us"] = row["held_by_us"]
    own_best = row.get('our_best_accepted')
    if own_best is not None and (not _integer(own_best)):
        return result('withheld', 'invalid_accepted_history')
    if own_best is not None and receipt['cost'] >= own_best:
        return result('verified_nonscoring', 'not_better_than_accepted_history')
    if row["held_by_us"] and receipt["cost"] >= row["record"]:
        return result("verified_nonscoring", "row_already_held")
    if receipt["cost"] > row["record"]:
        return result("verified_nonscoring", "cost_above_record")
    if is_cancelled():
        return result("withheld", "checker_cancelled")
    return result("verified_scoring", "exact_replay_and_fresh_eligibility_passed")
