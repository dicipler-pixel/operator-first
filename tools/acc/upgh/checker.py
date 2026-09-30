"""Exact evidence: pinned official verifier, plus the independent kernel as a second witness.

A path is admitted to the ledger as grade V only when:
  1. every pinned SAIR file still has its recorded SHA-256 (licence open),
  2. the official verifier returns ok, and
  3. the independent kernel agrees on ok/length.
Disagreement is never resolved by preference. The path is refused, and the
harness opens a checker task.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import kernel
from ledger import sha256_file

HERE = Path(__file__).resolve().parent
VERIFIER = "competition/tools/verifier"


def moves_sha(moves) -> str:
    return hashlib.sha256(json.dumps(moves, separators=(",", ":")).encode()).hexdigest()


def track_of(cid: str) -> str:
    return "SAC" if cid.startswith("sac-") else "AC"


class PinError(Exception):
    pass


class Checker:
    def __init__(self, sair_dir, pins: dict, commit: str | None = None):
        self.sair = Path(sair_dir).expanduser()
        self.pins = pins
        self.commit = commit
        self._manifest = None
        self._specs = None

    # -- licence ---------------------------------------------------------------
    def pin_problems(self) -> list[str]:
        problems = []
        if not self.sair.is_dir():
            return ["official SAIR repo not found at %s (run `upgh setup`)" % self.sair]
        for rel, want in sorted(self.pins.items()):
            path = self.sair / rel
            if not path.is_file():
                problems.append("missing pinned file " + rel)
            elif sha256_file(path) != want:
                problems.append("pinned file changed: " + rel)
        return problems

    def require_pins(self):
        problems = self.pin_problems()
        if problems:
            raise PinError("; ".join(problems))

    # -- data --------------------------------------------------------------------
    @property
    def manifest(self) -> dict:
        if self._manifest is None:
            path = self.sair / VERIFIER / "data" / "manifest.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            self._manifest = {"limits": data["limits"],
                              "challenges": {c["challenge_id"]: c for c in data["challenges"]}}
        return self._manifest

    def challenge(self, cid: str) -> dict | None:
        return self.manifest["challenges"].get(cid)

    @property
    def specs(self) -> dict:
        if self._specs is None:
            data = self.sair / VERIFIER / "data"
            self._specs = {"ac-r2-v1": kernel.Spec.load(data / "move_spec.json"),
                           "sac-r8-v1": kernel.Spec.load(data / "stable_move_spec.json")}
        return self._specs

    # -- replay ------------------------------------------------------------------
    def kernel_verdict(self, cid: str, moves) -> dict:
        ch = self.challenge(cid)
        if ch is None:
            return {"ok": False, "code": "E_UNKNOWN_CHALLENGE"}
        spec = self.specs[ch["move_spec_version"]]
        return kernel.replay(ch["initial_relators"], moves, spec, self.manifest["limits"])

    def official_verdicts(self, items) -> list[dict]:
        if not items:
            return []
        payload = "".join(json.dumps({"cid": c, "moves": m}) + "\n" for c, m in items)
        proc = subprocess.run([sys.executable, str(HERE / "official_driver.py"), str(self.sair)],
                              input=payload, capture_output=True, text=True, timeout=1800,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        lines = [json.loads(x) for x in proc.stdout.splitlines() if x.strip()]
        if proc.returncode != 0 or len(lines) != len(items) or any("fatal" in x for x in lines):
            raise PinError("official verifier failed (exit %s): %s %s"
                           % (proc.returncode, proc.stderr[-400:], proc.stdout[-400:]))
        return lines

    def check(self, items) -> list[dict]:
        """items: list of (cid, moves). Returns one receipt per item, in order."""
        self.require_pins()
        items = [(c, m) for c, m in items]
        official = self.official_verdicts(items)
        receipts = []
        for (cid, moves), off in zip(items, official):
            mine = self.kernel_verdict(cid, moves)
            agree = (bool(off.get("ok")) == bool(mine.get("ok"))
                     and (not off.get("ok") or off.get("length") == mine.get("length"))
                     and (off.get("ok") or off.get("code") == mine.get("code")))
            receipts.append({
                "cid": cid, "track": track_of(cid), "moves_sha": moves_sha(moves),
                "length": len(moves) if isinstance(moves, list) else None,
                "ok": bool(off.get("ok")) and agree,
                "agree": agree,
                "official": {k: off.get(k) for k in ("ok", "code", "length", "work",
                                                     "certificate_hash", "verifier_version")
                             if k in off},
                "kernel": {k: mine.get(k) for k in ("ok", "code", "length", "work") if k in mine},
            })
        return receipts
