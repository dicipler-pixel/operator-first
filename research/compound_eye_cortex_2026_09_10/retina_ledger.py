#!/usr/bin/env python3
"""Compound Eye full-retina ledger 0.4.

Design rule: attention prioritizes; it does not erase.

Every registered eye version receives a ledger row for every recorded research
pass. If an eye was actually part of the native run, its native status/value
hash/reason are preserved. If it was not selected, the ledger records
NOT_ATTEMPTED rather than silently omitting it. This makes retrospective miss
analysis possible without pretending an unexecuted eye produced evidence.

The report gate does not claim metaphysical truth. It licenses only conclusions
that are established or falsified *within a declared scope*, have their stated
assumptions satisfied, and cite usable evidence rows. Inconclusive, blocked,
inapplicable, errored and unattempted material stays in the ledger.

Standard-library only. Scientific acceptance remains with the registered eyes,
formal proof systems, exact certificates, measurements, and explicit theorem
contracts.
"""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import hashlib, json, sys, time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
INSTRUMENT = REPO / "tools" / "compound-eye"
sys.path.insert(0, str(INSTRUMENT))
import machine  # noqa: E402

LEDGER_SCHEMA = "compound-eye-full-retina-ledger-v1"
CLAIM_SCHEMA = "compound-eye-report-claim-v1"
REPORTABLE = {"established_within_scope", "falsified_within_scope"}


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def _semver(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except Exception as exc:
        raise ValueError("Invalid semantic version: " + str(v)) from exc


def active_refs(root=INSTRUMENT):
    """Highest registered semantic version for each stable eye ID.

    Historical versions remain in the ledger, but only one version per stable ID
    is labelled active. Running incompatible historical versions simultaneously
    is deliberately not implied by this function.
    """
    reg = machine.Registry(root)
    groups = {}
    for ref, spec in reg.eyes.items():
        groups.setdefault(spec["id"], []).append((spec["version"], ref))
    active = {}
    for eye_id, rows in groups.items():
        rows.sort(key=lambda x: (_semver(x[0]), x[1]))
        active[eye_id] = rows[-1][1]
    return active


def ledger_from_run(run, root=INSTRUMENT, surfaced_refs=()):
    """Create one complete registry ledger from one native Compound Eye run.

    `surfaced_refs` records what the foreground report actually mentioned. It is
    separate from what executed successfully.
    """
    if run.get("schema") != "compound-eye-run-v1":
        raise ValueError("Expected compound-eye-run-v1")
    reg = machine.Registry(root)
    active = active_refs(root)
    rows_by_ref = {row["eye"]: row for row in run.get("results", [])}
    if len(rows_by_ref) != len(run.get("results", [])):
        raise ValueError("Duplicate eye rows in native run")
    surfaced = set(surfaced_refs)
    unknown_surface = surfaced - set(reg.eyes)
    if unknown_surface:
        raise ValueError("Surfaced reference not in registry: " + sorted(unknown_surface)[0])
    rows = []
    for ref, spec in sorted(reg.eyes.items()):
        native = rows_by_ref.get(ref)
        base = {
            "eye": ref,
            "stable_id": spec["id"],
            "version": spec["version"],
            "title": spec["title"],
            "family": spec["family"],
            "definition_status": spec["status"],
            "active_version": active[spec["id"]] == ref,
            "required_inputs": sorted(spec.get("inputs", {})),
            "assumptions": deepcopy(spec.get("assumptions", [])),
            "limits": spec.get("limits", ""),
            "evidence_class": spec.get("evidence_class"),
            "surfaced": ref in surfaced,
        }
        if native is None:
            row = dict(base,
                       execution_status="not_attempted",
                       reason="Not selected/expanded in this native run; retained for retrospective miss tracing.",
                       value_sha256=None,
                       native_context_sha256=None,
                       native_definition_sha256=None)
        else:
            row = dict(base,
                       execution_status=native.get("status"),
                       reason=native.get("reason"),
                       value_sha256=native.get("value_sha256"),
                       native_context_sha256=native.get("context_sha256"),
                       native_definition_sha256=native.get("definition_sha256"))
        rows.append(row)
    counts = {}
    for row in rows:
        counts[row["execution_status"]] = counts.get(row["execution_status"], 0) + 1
    out = {
        "schema": LEDGER_SCHEMA,
        "request_sha256": run.get("request_sha256"),
        "native_result_sha256": run.get("result_sha256"),
        "native_engine_version": run.get("engine_version"),
        "registry_eye_versions": len(reg.eyes),
        "active_stable_eye_ids": len(active),
        "execution_status_counts": counts,
        "surfaced_count": sum(row["surfaced"] for row in rows),
        "rows": rows,
        "rule": "Every registered version gets a row. NOT_ATTEMPTED is a record, not evidence.",
    }
    out["ledger_sha256"] = digest(out)
    return out


def append_hashed_record(path, record):
    """Append one immutable-style hash-chained ledger event.

    The filesystem itself is not an append-only database, but a later edit to an
    earlier row breaks the chain under `verify_hashed_records`.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    prior = verify_hashed_records(p) if p.exists() else []
    row = {
        "sequence": len(prior),
        "previous": prior[-1]["event_sha256"] if prior else "0" * 64,
        "record_sha256": digest(record),
        "record": deepcopy(record),
        "recorded_unix_ns": time.time_ns(),
    }
    row["event_sha256"] = digest(row)
    with p.open("a", encoding="utf-8") as f:
        f.write(canonical(row) + "\n")
    return row


def verify_hashed_records(path):
    p = Path(path)
    previous = "0" * 64
    out = []
    if not p.exists():
        return out
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
        row = json.loads(line)
        given = row.pop("event_sha256")
        if row.get("sequence") != i or row.get("previous") != previous:
            raise ValueError("Broken ledger chain at sequence " + str(i))
        if digest(row.get("record")) != row.get("record_sha256"):
            raise ValueError("Record hash mismatch at sequence " + str(i))
        if digest(row) != given:
            raise ValueError("Event hash mismatch at sequence " + str(i))
        row["event_sha256"] = given
        out.append(row)
        previous = given
    return out


def report_gate(claims, ledger):
    """License only scoped conclusions supported by usable recorded evidence.

    A falsified positive claim is reportable as the *true negative conclusion*
    that the claim is falsified within its stated scope. Unknown is never
    promoted to false. Eye agreement is not a voting rule.
    """
    if ledger.get("schema") != LEDGER_SCHEMA:
        raise ValueError("Expected full-retina ledger")
    by_ref = {row["eye"]: row for row in ledger["rows"]}
    report = []
    held = []
    for claim in claims:
        if claim.get("schema") != CLAIM_SCHEMA:
            raise ValueError("Wrong claim schema")
        verdict = claim.get("verdict")
        refs = list(claim.get("evidence_refs", []))
        unknown = [r for r in refs if r not in by_ref]
        usable = [r for r in refs if r in by_ref and by_ref[r]["execution_status"] == "ok"]
        reasons = []
        if verdict not in REPORTABLE:
            reasons.append("Verdict is not established/falsified within scope")
        if claim.get("assumptions_met") is not True:
            reasons.append("Not all declared assumptions are satisfied")
        if not refs:
            reasons.append("No evidence references supplied")
        if unknown:
            reasons.append("Unknown evidence references: " + ", ".join(unknown))
        if refs and len(usable) != len(refs):
            reasons.append("At least one cited eye did not return status=ok")
        entry = deepcopy(claim)
        entry["usable_evidence_refs"] = usable
        if reasons:
            entry["report_status"] = "ledger_only"
            entry["gate_reasons"] = reasons
            held.append(entry)
        else:
            entry["report_status"] = "licensed_conclusion"
            entry["gate_reasons"] = []
            report.append(entry)
    return {
        "licensed_conclusions": report,
        "ledger_only_claims": held,
        "rule": "Only established/falsified conclusions with satisfied assumptions and usable evidence are surfaced. This is scoped licensing, not absolute truth.",
    }


def trace_miss(earlier_ledger, later_relevant_refs):
    """Explain what happened to eyes later judged relevant to a discovery."""
    if earlier_ledger.get("schema") != LEDGER_SCHEMA:
        raise ValueError("Expected full-retina ledger")
    by_ref = {row["eye"]: row for row in earlier_ledger["rows"]}
    rows = []
    for ref in later_relevant_refs:
        if ref not in by_ref:
            rows.append({"eye": ref, "miss_class": "NOT_IN_EARLIER_REGISTRY"})
            continue
        row = by_ref[ref]
        status = row["execution_status"]
        if row["surfaced"]:
            cls = "SURFACED_EARLIER"
        elif status == "ok":
            cls = "SEEN_BUT_NOT_SURFACED"
        elif status == "blocked":
            cls = "BLOCKED_EARLIER"
        elif status == "inapplicable":
            cls = "DECLARED_INAPPLICABLE_EARLIER"
        elif status == "error":
            cls = "ERRORED_EARLIER"
        elif status == "not_attempted":
            cls = "NOT_ATTEMPTED_EARLIER"
        else:
            cls = "OTHER_EARLIER_STATUS"
        rows.append({
            "eye": ref,
            "miss_class": cls,
            "earlier_status": status,
            "earlier_reason": row.get("reason"),
            "earlier_value_sha256": row.get("value_sha256"),
            "active_version_then": row.get("active_version"),
        })
    counts = {}
    for row in rows:
        counts[row["miss_class"]] = counts.get(row["miss_class"], 0) + 1
    return {
        "rows": rows,
        "counts": counts,
        "value": "A miss is evidence about routing/contracts only after the later relevance relation is explicitly supplied; hindsight does not retroactively make an unexecuted eye evidence.",
    }


def foreground_priority(ledger, refs):
    """Mark attention priority without deleting any ledger row."""
    wanted = set(refs)
    out = deepcopy(ledger)
    known = {row["eye"] for row in out["rows"]}
    if wanted - known:
        raise ValueError("Unknown foreground eye")
    for row in out["rows"]:
        row["foreground_priority"] = row["eye"] in wanted
    out["foreground_count"] = len(wanted)
    out["rule"] += " Foreground priority never deletes background records."
    out["ledger_sha256"] = digest({k: v for k, v in out.items() if k != "ledger_sha256"})
    return out
