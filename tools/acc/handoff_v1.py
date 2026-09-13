"""Sealed hand-offs: nothing crosses a boundary without a fingerprint.

Four files were damaged in transit this session and the receiving side had no
way to know. This tool closes that: a hand-off carries the byte count and the
SHA-256 of what was sent, plus the claim as it stood *before* the work, and the
receiver recomputes all three and refuses on any mismatch.

Three refusals are mechanical, not advisory:

  * byte count or digest differs      -> damaged-in-transit, result fail
  * the claim text was edited after   -> claim-rewritten, result fail
  * the checker is the producer       -> refused, no self-verification

A hand-off does not have to carry a file. `row` seals a small ledger row
inline, which is the normal case: files move only when a row points at one.

    python3 tools/acc/handoff_v1.py seal   <file> --producer P --claim C --evidence E
    python3 tools/acc/handoff_v1.py row    --producer P --claim C --evidence E --data '{...}'
    python3 tools/acc/handoff_v1.py verify <handoff_id> --checker Q [--file PATH]
    python3 tools/acc/handoff_v1.py list [--open] [--failed]
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mixer_trace_v1 import EVIDENCE_RANK  # one evidence vocabulary for the repo

import os

# Tests point this at a scratch file; the default is the real append-only ledger.
LEDGER = Path(os.environ.get("ACC_HANDOFF_LEDGER",
                             ROOT / "ledger" / "handoff" / "handoffs_v1.jsonl"))
PARTIES = {"gpt", "claude", "jeromie", "sage", "pari", "magma", "ci"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(s):
    return sha256_bytes(s.encode("utf-8"))


def append(row):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as fh:
        fh.write(json.dumps(row) + "\n")
    return row


def load():
    if not LEDGER.exists():
        return []
    return [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]


def seals():
    return {r["handoff_id"]: r for r in load() if r.get("record") == "seal"}


def verdicts():
    """Latest verification per hand-off id."""
    out = {}
    for r in load():
        if r.get("record") == "verify":
            out[r["handoff_id"]] = r
    return out


def make_id(producer, claim, digest, when):
    return sha256_text("|".join([producer, claim, digest or "-", when]))[:12]


def seal(producer, claim, evidence, artifact=None, payload=None, note=None):
    """Produce an envelope. The claim is fixed here, before the work is judged."""
    if producer not in PARTIES:
        raise SystemExit(f"handoff: unknown producer {producer!r}; "
                         f"one of {sorted(PARTIES)}")
    if evidence not in EVIDENCE_RANK:
        raise SystemExit(f"handoff: evidence must be one of {sorted(EVIDENCE_RANK)}")
    if not claim or len(claim.strip()) < 12:
        raise SystemExit("handoff: a hand-off needs a falsifiable claim, written "
                         "before the work, not a label")

    art = None
    if artifact is not None:
        p = Path(artifact)
        if not p.exists():
            raise SystemExit(f"handoff: {artifact} does not exist")
        data = p.read_bytes()
        art = {"name": p.name,
               "path": str(p.relative_to(ROOT)) if ROOT in p.resolve().parents else str(p),
               "bytes": len(data),
               "sha256": sha256_bytes(data)}

    when = now()
    row = {
        "schema": "acc-handoff-v1",
        "record": "seal",
        "handoff_id": make_id(producer, claim, art["sha256"] if art else None, when),
        "sealed_utc": when,
        "producer": producer,
        "claim": claim,
        "claim_sha256": sha256_text(claim),
        "artifact": art,
        "payload": payload,
        "evidence": evidence,
        "note": note,
        "verification": "pending",
    }
    return append(row)


def verify(handoff_id, checker, file=None):
    """Recompute everything the envelope asserts. Refuse on any mismatch."""
    env = seals().get(handoff_id)
    if not env:
        raise SystemExit(f"handoff: no sealed hand-off {handoff_id!r}")
    if checker not in PARTIES:
        raise SystemExit(f"handoff: unknown checker {checker!r}")

    status, reason = "verified", None

    # The checker must not be the producer. Self-verification is not verification.
    if checker == env["producer"]:
        status, reason = "refused", (
            f"the checker is the producer ({checker}); an independent party must "
            f"check this hand-off")

    # The claim is fixed at seal time; a claim edited to match the outcome is
    # a description, not a test.
    elif sha256_text(env["claim"]) != env["claim_sha256"]:
        status, reason = "claim-rewritten", (
            "the claim text no longer hashes to the digest sealed with it")

    elif env["artifact"]:
        art = env["artifact"]
        p = Path(file) if file else (ROOT / art["path"])
        if not p.exists():
            status, reason = "missing", f"{p} is not on disk at the receiving side"
        else:
            data = p.read_bytes()
            got_bytes, got_sha = len(data), sha256_bytes(data)
            if got_bytes != art["bytes"] or got_sha != art["sha256"]:
                status = "damaged-in-transit"
                reason = (f"expected {art['bytes']} bytes / {art['sha256'][:16]}, "
                          f"received {got_bytes} bytes / {got_sha[:16]}"
                          + (f" (short by {art['bytes'] - got_bytes})"
                             if got_bytes < art["bytes"] else ""))

    row = {
        "schema": "acc-handoff-v1",
        "record": "verify",
        "handoff_id": handoff_id,
        "checked_utc": now(),
        "checker": checker,
        "producer": env["producer"],
        "status": status,
        "result": "pass" if status == "verified" else "fail",
        "failure_reason": reason,
    }
    return append(row)


def fmt(env, v=None):
    kind = "file" if env["artifact"] else "row"
    head = (f"{env['handoff_id']}  {env['producer']:<8} {kind:<5} "
            f"{env['evidence']:<16} ")
    if v:
        head += f"{v['result']:<5} {v['status']:<19} checked by {v['checker']}"
    else:
        head += "—     pending".ljust(25) + " no independent check"
    lines = [head, "      " + env["claim"][:100]]
    if env["artifact"]:
        a = env["artifact"]
        lines.append(f"      {a['name']}  {a['bytes']} bytes  sha256 {a['sha256'][:16]}…")
    if v and v.get("failure_reason"):
        lines.append(f"      ! {v['failure_reason']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seal"); s.add_argument("file")
    r = sub.add_parser("row"); r.add_argument("--data", default="{}")
    for p in (s, r):
        p.add_argument("--producer", required=True)
        p.add_argument("--claim", required=True)
        p.add_argument("--evidence", required=True)
        p.add_argument("--note")

    v = sub.add_parser("verify")
    v.add_argument("handoff_id"); v.add_argument("--checker", required=True)
    v.add_argument("--file")

    l = sub.add_parser("list")
    l.add_argument("--open", action="store_true", help="sealed but never checked")
    l.add_argument("--failed", action="store_true")

    a = ap.parse_args(argv)

    if a.cmd in ("seal", "row"):
        row = seal(a.producer, a.claim, a.evidence,
                   artifact=a.file if a.cmd == "seal" else None,
                   payload=json.loads(a.data) if a.cmd == "row" else None,
                   note=a.note)
        print(f"sealed {row['handoff_id']}  "
              + (f"{row['artifact']['bytes']} bytes  sha256 {row['artifact']['sha256']}"
                 if row["artifact"] else "row payload"))
        print(f"  a different party must now run: python3 tools/acc/handoff_v1.py "
              f"verify {row['handoff_id']} --checker <party>")
        return 0

    if a.cmd == "verify":
        row = verify(a.handoff_id, a.checker, a.file)
        print(f"{row['result'].upper()}  {row['handoff_id']}  {row['status']}")
        if row["failure_reason"]:
            print("  " + row["failure_reason"])
        return 0 if row["result"] == "pass" else 1

    env, ver = seals(), verdicts()
    ids = list(env)
    if a.open:
        ids = [i for i in ids if i not in ver]
    if a.failed:
        ids = [i for i in ids if ver.get(i, {}).get("result") == "fail"]
    for i in ids:
        print(fmt(env[i], ver.get(i)))
    print(f"\n{len(ids)} hand-off(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
