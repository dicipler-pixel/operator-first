"""Sealed hand-offs v2 — transport and claim are verified separately.

v1 conflated two different questions. This version keeps them apart, because
they have different answers and different checkers:

  TRANSPORT  did exactly what was sent arrive? Byte count and SHA-256 over
             every artifact, a canonical digest over any inline payload, the
             claim text still hashing to the digest sealed with it, and a
             checker who is not the producer.

  CLAIM      is the sentence true? This is NEVER established by inspecting an
             envelope. It requires an independently supplied result artifact,
             produced by a party other than the one who sealed the claim, and
             carrying evidence stronger than none. Absent that, claim status
             is `withheld` — not pending, not passing.

v1 gaps this closes, all three found in review:
  * `artifact: null` made verify() prove only that the claim string was not
    rewritten, while reporting a bare pass;
  * inline row payloads were stored but never hashed, so a payload could be
    edited after sealing and still verify;
  * one artifact per hand-off could not describe a computation package.

    python3 tools/acc/handoff_v2.py seal <file>... --producer P --claim C --evidence E
    python3 tools/acc/handoff_v2.py row  --producer P --claim C --evidence E --data '{...}'
    python3 tools/acc/handoff_v2.py verify <handoff_id> --checker Q [--file NAME=PATH]...
    python3 tools/acc/handoff_v2.py attest <handoff_id> --checker Q --outcome O
                                   --result <handoff_id> --evidence E
    python3 tools/acc/handoff_v2.py list [--open] [--failed] [--withheld]
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mixer_trace_v1 import EVIDENCE_RANK

LEDGER = Path(os.environ.get("ACC_HANDOFF_LEDGER",
                             ROOT / "ledger" / "handoff" / "handoffs_v2.jsonl"))
PARTIES = {"gpt", "claude", "jeromie", "sage", "pari", "magma", "ci"}
OUTCOMES = {"supports", "refutes", "open"}

MAX_EXACT = 2 ** 53 - 1


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_text(s):
    return sha256_bytes(s.encode("utf-8"))


def canonical(obj):
    """Stable bytes for a JSON value: sorted keys, no incidental whitespace.

    Without this an inline payload is unhashable in practice, because two
    equivalent serializations differ and any digest would be noise.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def unsafe_integers(value, where="payload"):
    """Every number in the record, not just one field.

    A JSON number past 2^53 has already lost digits by the time it is parsed.
    v1 swept only an eye's `output`; a discriminant sitting in `x`, `values`,
    or anywhere else in the row went through unchecked.
    """
    bad = []
    if isinstance(value, bool):
        return bad
    if isinstance(value, float) and abs(value) > MAX_EXACT:
        bad.append((where, repr(value)))
    elif isinstance(value, int) and abs(value) > MAX_EXACT:
        # Python parsed it exactly; a JSON consumer will not.
        bad.append((where, str(value)))
    elif isinstance(value, dict):
        for k, v in value.items():
            bad += unsafe_integers(v, f"{where}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            bad += unsafe_integers(v, f"{where}[{i}]")
    return bad


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


def checks():
    out = {}
    for r in load():
        if r.get("record") == "check":
            out[r["handoff_id"]] = r
    return out


def describe(p):
    p = Path(p)
    if not p.exists():
        raise SystemExit(f"handoff: {p} does not exist")
    data = p.read_bytes()
    try:
        rel = str(p.resolve().relative_to(ROOT))
    except ValueError:
        rel = str(p)
    return {"name": p.name, "path": rel, "bytes": len(data),
            "sha256": sha256_bytes(data)}


def seal(producer, claim, evidence, artifacts=(), payload=None, note=None):
    if producer not in PARTIES:
        raise SystemExit(f"handoff: unknown producer {producer!r}")
    if evidence not in EVIDENCE_RANK:
        raise SystemExit(f"handoff: evidence must be one of {sorted(EVIDENCE_RANK)}")
    if not claim or len(claim.strip()) < 12:
        raise SystemExit("handoff: a hand-off needs a falsifiable claim, written "
                         "before the work, not a label")

    arts = sorted((describe(a) for a in artifacts), key=lambda a: a["path"])
    if payload is not None:
        bad = unsafe_integers(payload)
        if bad:
            raise SystemExit("handoff: numbers past 2^53 lose digits in JSON; "
                             "quote them as strings — " +
                             "; ".join(f"{w} = {v}" for w, v in bad))

    when = now()
    # The manifest digest covers the whole package, so adding, dropping or
    # swapping a file is as detectable as corrupting one.
    manifest = sha256_bytes(canonical([[a["path"], a["bytes"], a["sha256"]]
                                       for a in arts]))
    payload_sha = sha256_bytes(canonical(payload)) if payload is not None else None

    row = {
        "schema": "acc-handoff-v2",
        "record": "seal",
        "handoff_id": sha256_text("|".join(
            [producer, claim, manifest, payload_sha or "-", when]))[:12],
        "sealed_utc": when,
        "producer": producer,
        "claim": claim,
        "claim_sha256": sha256_text(claim),
        "artifacts": arts,
        "manifest_sha256": manifest,
        "payload": payload,
        "payload_sha256": payload_sha,
        "evidence": evidence,
        "note": note,
    }
    return append(row)


def check_transport(env, checker, files=None):
    """Did exactly what was sealed arrive? Nothing here speaks to truth."""
    files = files or {}
    if checker == env["producer"]:
        return ("refused", f"the checker is the producer ({checker}); an "
                           f"independent party must check this hand-off")
    if sha256_text(env["claim"]) != env["claim_sha256"]:
        return ("claim-rewritten",
                "the claim text no longer hashes to the digest sealed with it")

    if env.get("payload") is not None:
        got = sha256_bytes(canonical(env["payload"]))
        if got != env.get("payload_sha256"):
            return ("payload-altered",
                    f"inline payload hashes to {got[:16]}, sealed as "
                    f"{(env.get('payload_sha256') or '-')[:16]}")

    for a in env.get("artifacts") or []:
        p = Path(files.get(a["name"], ROOT / a["path"]))
        if not p.exists():
            return ("missing", f"{p} is not on disk at the receiving side")
        data = p.read_bytes()
        if len(data) != a["bytes"] or sha256_bytes(data) != a["sha256"]:
            short = a["bytes"] - len(data)
            return ("damaged-in-transit",
                    f"{a['name']}: expected {a['bytes']} bytes / "
                    f"{a['sha256'][:16]}, received {len(data)} bytes / "
                    f"{sha256_bytes(data)[:16]}"
                    + (f" (short by {short})" if short > 0 else ""))

    got_manifest = sha256_bytes(canonical([[a["path"], a["bytes"], a["sha256"]]
                                           for a in env.get("artifacts") or []]))
    if got_manifest != env.get("manifest_sha256"):
        return ("manifest-altered", "the artifact list differs from the sealed manifest")

    return ("verified", None)


def verify(handoff_id, checker, files=None):
    env = seals().get(handoff_id)
    if not env:
        raise SystemExit(f"handoff: no sealed hand-off {handoff_id!r}")
    if checker not in PARTIES:
        raise SystemExit(f"handoff: unknown checker {checker!r}")

    status, reason = check_transport(env, checker, files)
    ok = status == "verified"

    # The claim is a separate question and this is not the tool that answers it.
    claim_reason = (
        "no independently supplied result artifact; this check establishes that "
        "the envelope arrived intact, not that the claim is true")
    if not env.get("artifacts"):
        claim_reason += ". This hand-off carries no mathematical artifact at all"

    row = {
        "schema": "acc-handoff-v2", "record": "check",
        "handoff_id": handoff_id, "checked_utc": now(),
        "checker": checker, "producer": env["producer"],
        "transport_verified": ok,
        "transport_status": status,
        "transport_reason": reason,
        "claim_verified": None,
        "claim_status": "withheld",
        "claim_reason": claim_reason,
        "result_artifact": None,
        "summary": ("transport envelope inspected; mathematical verification withheld"
                    if ok else f"transport check failed: {status}"),
    }
    return append(row)


def attest(handoff_id, checker, outcome, evidence, result_id=None, result_files=()):
    """Claim-level verification. Requires an independent result artifact."""
    env = seals().get(handoff_id)
    if not env:
        raise SystemExit(f"handoff: no sealed hand-off {handoff_id!r}")
    if checker not in PARTIES:
        raise SystemExit(f"handoff: unknown checker {checker!r}")
    if checker == env["producer"]:
        raise SystemExit("handoff: the producer cannot attest to its own claim")
    if outcome not in OUTCOMES:
        raise SystemExit(f"handoff: outcome must be one of {sorted(OUTCOMES)}")
    if evidence not in EVIDENCE_RANK:
        raise SystemExit(f"handoff: evidence must be one of {sorted(EVIDENCE_RANK)}")
    if outcome in ("supports", "refutes") and evidence == "none":
        raise SystemExit("handoff: a supports/refutes attestation needs evidence "
                         "stronger than none")

    result = None
    if result_id:
        r = seals().get(result_id)
        if not r:
            raise SystemExit(f"handoff: result hand-off {result_id!r} is not sealed")
        if r["producer"] == env["producer"] and outcome != "open":
            raise SystemExit(
                f"handoff: the result was produced by {r['producer']}, the same "
                f"party that sealed the claim; an outcome of {outcome} needs a "
                f"result from somewhere else")
        st, why = check_transport(r, checker)
        if st != "verified":
            raise SystemExit(f"handoff: the result hand-off does not verify: {why}")
        result = {"handoff_id": result_id, "producer": r["producer"],
                  "manifest_sha256": r["manifest_sha256"]}
    elif result_files:
        result = {"files": sorted((describe(f) for f in result_files),
                                  key=lambda a: a["path"])}
    elif outcome != "open":
        raise SystemExit("handoff: a supports/refutes attestation requires a result "
                         "artifact (--result or --result-file); an envelope check "
                         "is not mathematical verification")

    row = {
        "schema": "acc-handoff-v2", "record": "attest",
        "handoff_id": handoff_id, "attested_utc": now(),
        "checker": checker, "producer": env["producer"],
        "claim_status": outcome,
        "claim_verified": outcome == "supports",
        "evidence": evidence,
        "result_artifact": result,
    }
    return append(row)


def attestations():
    out = {}
    for r in load():
        if r.get("record") == "attest":
            out[r["handoff_id"]] = r
    return out


def fmt(env, c=None, a=None):
    n = len(env.get("artifacts") or [])
    kind = f"{n} file{'s' if n != 1 else ''}" if n else "row"
    lines = [f"{env['handoff_id']}  {env['producer']:<8} {kind:<8} {env['evidence']:<16}"]
    lines.append(f"      {env['claim'][:96]}")
    lines.append("      transport  " + (
        f"{c['transport_status']}  (checked by {c['checker']})" if c
        else "not checked — no independent party has inspected this envelope"))
    if c and c.get("transport_reason"):
        lines.append(f"                 ! {c['transport_reason']}")
    if a:
        lines.append(f"      claim      {a['claim_status']}  evidence {a['evidence']}"
                     f"  (attested by {a['checker']})")
    else:
        lines.append("      claim      WITHHELD — " + (
            c["claim_reason"] if c else "no attestation on record"))
    for art in (env.get("artifacts") or [])[:6]:
        lines.append(f"      · {art['path']}  {art['bytes']} bytes  {art['sha256'][:16]}…")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seal"); s.add_argument("file", nargs="+")
    r = sub.add_parser("row"); r.add_argument("--data", default="{}")
    for p in (s, r):
        p.add_argument("--producer", required=True)
        p.add_argument("--claim", required=True)
        p.add_argument("--evidence", required=True)
        p.add_argument("--note")

    v = sub.add_parser("verify")
    v.add_argument("handoff_id"); v.add_argument("--checker", required=True)
    v.add_argument("--file", action="append", default=[], metavar="NAME=PATH")

    t = sub.add_parser("attest")
    t.add_argument("handoff_id"); t.add_argument("--checker", required=True)
    t.add_argument("--outcome", required=True); t.add_argument("--evidence", required=True)
    t.add_argument("--result"); t.add_argument("--result-file", action="append", default=[])

    va = sub.add_parser("verify-all")
    va.add_argument("--checker", required=True)

    l = sub.add_parser("list")
    l.add_argument("--open", action="store_true")
    l.add_argument("--failed", action="store_true")
    l.add_argument("--withheld", action="store_true")

    a = ap.parse_args(argv)

    if a.cmd in ("seal", "row"):
        row = seal(a.producer, a.claim, a.evidence,
                   artifacts=a.file if a.cmd == "seal" else (),
                   payload=json.loads(a.data) if a.cmd == "row" else None,
                   note=a.note)
        print(f"sealed {row['handoff_id']}")
        for art in row["artifacts"]:
            print(f"  · {art['path']}  {art['bytes']} bytes  sha256 {art['sha256']}")
        if row["payload_sha256"]:
            print(f"  · inline payload  sha256 {row['payload_sha256']}")
        print(f"  manifest sha256 {row['manifest_sha256']}")
        print(f"  transport check: python3 tools/acc/handoff_v2.py verify "
              f"{row['handoff_id']} --checker <party>")
        print(f"  claim stays WITHHELD until an independent result artifact is attested.")
        return 0

    if a.cmd == "verify":
        files = dict(f.split("=", 1) for f in a.file)
        row = verify(a.handoff_id, a.checker, files)
        print(f"transport  {row['transport_status'].upper()}   {row['handoff_id']}")
        if row["transport_reason"]:
            print("  " + row["transport_reason"])
        print(f"claim      WITHHELD")
        print("  " + row["claim_reason"])
        return 0 if row["transport_verified"] else 1

    if a.cmd == "attest":
        row = attest(a.handoff_id, a.checker, a.outcome, a.evidence,
                     a.result, a.result_file)
        print(f"claim {row['claim_status'].upper()}  {row['handoff_id']}  "
              f"evidence {row['evidence']}  attested by {row['checker']}")
        return 0

    if a.cmd == "verify-all":
        env = seals()
        bad = 0
        for hid, e in env.items():
            if a.checker == e["producer"]:
                print(f"skip   {hid}  sealed by the checker ({a.checker})")
                continue
            row = verify(hid, a.checker)
            ok = row["transport_verified"]
            bad += 0 if ok else 1
            print(f"{'ok' if ok else 'FAIL':<6} {hid}  transport "
                  f"{row['transport_status']}  claim {row['claim_status']}")
            if row["transport_reason"]:
                print("       " + row["transport_reason"])
        print(f"\n{len(env)} sealed, {bad} transport failure(s). "
              f"Claim status is withheld on all of them: an envelope check is "
              f"not mathematical verification.")
        return 1 if bad else 0

    env, c, at = seals(), checks(), attestations()
    ids = list(env)
    if a.open:
        ids = [i for i in ids if i not in c]
    if a.failed:
        ids = [i for i in ids if c.get(i) and not c[i]["transport_verified"]]
    if a.withheld:
        ids = [i for i in ids if i not in at]
    for i in ids:
        print(fmt(env[i], c.get(i), at.get(i)))
        print()
    print(f"{len(ids)} hand-off(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
