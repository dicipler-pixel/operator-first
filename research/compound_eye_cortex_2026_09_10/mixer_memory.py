#!/usr/bin/env python3
"""Compound Eye Mixer Memory / Epiphany Replay.

Record how compatible eye outputs were combined without deleting native rows,
then replay old combinations after a later discovery to learn whether a signal
was never selected, produced no usable output, was seen but not surfaced, was
surfaced inside a risky fusion, or was already visible in the earlier view.

This is a meta-layer. It does not infer scientific truth from agreement and it
does not silently average incompatible quantities.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import math
import statistics
import time

MIX_SCHEMA = "compound-eye-mix-trial-v1"
LEDGER_SCHEMA = "compound-eye-full-retina-ledger-v1"
LOG_SCHEMA = "compound-eye-mix-log-event-v1"


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(x):
    return hashlib.sha256(canonical(x).encode("utf-8")).hexdigest()


def _finite_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def _validate_observation(row):
    required = {"eye", "channel", "value", "units", "scope", "lineage"}
    missing = required - set(row)
    if missing:
        raise ValueError("Observation missing " + sorted(missing)[0])
    if not _finite_number(row["value"]):
        raise ValueError("Mixer currently accepts finite scalar values only")
    for key in ("eye", "channel", "units", "scope", "lineage"):
        if not isinstance(row[key], str) or not row[key]:
            raise ValueError("Observation field must be a non-empty string: " + key)


def _sign(v):
    return 1 if v > 0 else -1 if v < 0 else 0


def combine_observations(observations):
    """Group compatible scalar channels while preserving every source row.

    Compatibility key is (channel, units, scope). Scale is deliberately not
    part of that key: mixed scales may share a visual group but force an
    OVERLAY_ONLY warning rather than a collapsed summary.

    Mean/median/range are descriptive diagnostics only. They are never a truth
    vote and never replace the native rows.
    """
    rows = [deepcopy(r) for r in observations]
    seen = set()
    for row in rows:
        _validate_observation(row)
        key = (row["eye"], row["channel"], row["units"], row["scope"], canonical(row.get("scale")))
        if key in seen:
            raise ValueError("Duplicate eye/channel observation in one mix")
        seen.add(key)

    groups = defaultdict(list)
    for row in rows:
        groups[(row["channel"], row["units"], row["scope"])].append(row)

    out_groups = []
    for (channel, units, scope), src in sorted(groups.items()):
        src = sorted(src, key=lambda r: (r["eye"], canonical(r.get("scale"))))
        vals = [float(r["value"]) for r in src]
        lineages = {r["lineage"] for r in src}
        scale_tokens = {canonical(r.get("scale")) for r in src}
        nonzero_signs = {_sign(v) for v in vals if v != 0.0}
        sign_conflict = len(nonzero_signs) > 1
        sum_abs = sum(abs(v) for v in vals)
        cancellation = 0.0 if sum_abs == 0.0 else 1.0 - abs(sum(vals)) / sum_abs
        mean = sum(vals) / len(vals)
        median = float(statistics.median(vals))

        loo = []
        if len(vals) > 1:
            for i, row in enumerate(src):
                other = (sum(vals) - vals[i]) / (len(vals) - 1)
                loo.append({"eye": row["eye"], "mean_without_eye": other,
                            "absolute_mean_shift": abs(mean - other)})
        else:
            loo.append({"eye": src[0]["eye"], "mean_without_eye": None,
                        "absolute_mean_shift": 0.0})
        dominant = max(loo, key=lambda x: (x["absolute_mean_shift"], x["eye"]))

        flags = []
        if sign_conflict:
            flags.append("SIGN_CANCELLATION")
        if len(lineages) < len(src):
            flags.append("SHARED_LINEAGE")
        if len(scale_tokens) > 1:
            flags.append("MIXED_SCALE")

        out_groups.append({
            "channel": channel,
            "units": units,
            "scope": scope,
            "source_count": len(src),
            "independent_lineages": len(lineages),
            "lineage_redundancy_fraction": 1.0 - len(lineages) / len(src),
            "scales": [json.loads(x) for x in sorted(scale_tokens)],
            "descriptive_mean": mean,
            "descriptive_median": median,
            "minimum": min(vals),
            "maximum": max(vals),
            "span": max(vals) - min(vals),
            "sign_conflict": sign_conflict,
            "cancellation_fraction": cancellation,
            "largest_leave_one_out_mean_shift": dominant,
            "distortion_flags": flags,
            "recommended_view": "OVERLAY_ONLY" if flags else "SUMMARY_PLUS_SOURCES",
            "source_rows": src,
            "source_rows_sha256": digest(src),
            "warning": "Summary statistics are descriptive. Native source rows remain authoritative and are never replaced by the composite.",
        })

    ordered = sorted(rows, key=lambda r: (r["channel"], r["units"], r["scope"], r["eye"]))
    return {
        "groups": out_groups,
        "source_rows": ordered,
        "source_rows_sha256": digest(ordered),
        "rule": "Combine only matching channel+units+scope. Mixed scale, shared lineage, or opposite signs force overlay-first inspection.",
    }


def make_mix_trial(trial_id, question_id, enabled_eyes, surfaced_eyes, observations,
                   routing_reasons=None, parameters=None, notes=""):
    """Create one replayable mixer trial with foreground and source records."""
    if not isinstance(trial_id, str) or not trial_id:
        raise ValueError("trial_id required")
    if not isinstance(question_id, str) or not question_id:
        raise ValueError("question_id required")
    enabled = list(enabled_eyes)
    surfaced = list(surfaced_eyes)
    if len(enabled) != len(set(enabled)):
        raise ValueError("Duplicate enabled eye")
    if len(surfaced) != len(set(surfaced)):
        raise ValueError("Duplicate surfaced eye")
    if not set(surfaced) <= set(enabled):
        raise ValueError("Surfaced eyes must be enabled")
    observed_eyes = {r.get("eye") for r in observations}
    if not observed_eyes <= set(enabled):
        raise ValueError("Observation produced by an eye that was not enabled")

    routing_reasons = {} if routing_reasons is None else deepcopy(routing_reasons)
    if set(routing_reasons) - set(enabled):
        raise ValueError("Routing reason supplied for a disabled eye")

    combined = combine_observations(observations)
    trial = {
        "schema": MIX_SCHEMA,
        "trial_id": trial_id,
        "question_id": question_id,
        "enabled_eyes": enabled,
        "surfaced_eyes": surfaced,
        "routing_reasons": routing_reasons,
        "parameters": deepcopy(parameters or {}),
        "notes": notes,
        "no_output_eyes": sorted(set(enabled) - observed_eyes),
        "composite": combined,
        "rule": "Foreground is a view, not deletion. Every source observation remains in composite.source_rows.",
    }
    trial["trial_sha256"] = digest(trial)
    return trial


def append_mix_trial(path, trial):
    """Append a hash-chained mixer trial to JSONL history."""
    if trial.get("schema") != MIX_SCHEMA:
        raise ValueError("Expected mix trial")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    prior = verify_mix_log(p) if p.exists() else []
    row = {
        "schema": LOG_SCHEMA,
        "sequence": len(prior),
        "previous": prior[-1]["event_sha256"] if prior else "0" * 64,
        "trial_sha256": digest(trial),
        "trial": deepcopy(trial),
        "recorded_unix_ns": time.time_ns(),
    }
    row["event_sha256"] = digest(row)
    with p.open("a", encoding="utf-8") as f:
        f.write(canonical(row) + "\n")
    return row


def verify_mix_log(path):
    p = Path(path)
    if not p.exists():
        return []
    previous = "0" * 64
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
        row = json.loads(line)
        given = row.pop("event_sha256")
        if row.get("schema") != LOG_SCHEMA:
            raise ValueError("Wrong mixer log schema at sequence " + str(i))
        if row.get("sequence") != i or row.get("previous") != previous:
            raise ValueError("Broken mixer log chain at sequence " + str(i))
        if digest(row.get("trial")) != row.get("trial_sha256"):
            raise ValueError("Mixer trial hash mismatch at sequence " + str(i))
        if digest(row) != given:
            raise ValueError("Mixer event hash mismatch at sequence " + str(i))
        row["event_sha256"] = given
        out.append(row)
        previous = given
    return out


def _ledger_miss_class(row):
    status = row.get("execution_status")
    if row.get("surfaced"):
        return "SURFACED_EARLIER"
    if status == "ok":
        return "SEEN_BUT_NOT_SURFACED"
    if status == "blocked":
        return "BLOCKED_EARLIER"
    if status == "inapplicable":
        return "DECLARED_INAPPLICABLE_EARLIER"
    if status == "error":
        return "ERRORED_EARLIER"
    if status == "not_attempted":
        return "NOT_ATTEMPTED_EARLIER"
    return "OTHER_EARLIER_STATUS"


def replay_epiphany(earlier_ledger, mix_trials, relevant_eyes, relevant_channels=()):
    """Replay old eye selection/fusion after a later relevance relation is known.

    Hindsight diagnoses the old routing/mixer without rewriting the old evidence
    state or pretending an unexecuted eye had produced evidence.
    """
    if earlier_ledger.get("schema") != LEDGER_SCHEMA:
        raise ValueError("Expected full-retina ledger")
    relevant_eyes = list(dict.fromkeys(relevant_eyes))
    relevant_channels = set(relevant_channels)
    by_ref = {r["eye"]: r for r in earlier_ledger.get("rows", [])}

    ledger_rows = []
    for eye in relevant_eyes:
        if eye not in by_ref:
            ledger_rows.append({"eye": eye, "miss_class": "NOT_IN_EARLIER_REGISTRY"})
        else:
            r = by_ref[eye]
            ledger_rows.append({
                "eye": eye,
                "miss_class": _ledger_miss_class(r),
                "earlier_status": r.get("execution_status"),
                "earlier_reason": r.get("reason"),
                "earlier_value_sha256": r.get("value_sha256"),
            })

    trial_rows = []
    lesson_counter = Counter()
    for trial in mix_trials:
        if trial.get("schema") != MIX_SCHEMA:
            raise ValueError("Expected mix trial")
        enabled = set(trial["enabled_eyes"])
        surfaced = set(trial["surfaced_eyes"])
        source_rows = trial["composite"]["source_rows"]
        source_eyes = {r["eye"] for r in source_rows}
        source_channels = {r["channel"] for r in source_rows}
        rel_enabled = sorted(enabled & set(relevant_eyes))
        rel_source = sorted(source_eyes & set(relevant_eyes))
        rel_surfaced = sorted(surfaced & set(relevant_eyes))
        rel_channels = sorted(source_channels & relevant_channels)

        failure_modes = []
        if relevant_eyes and not rel_enabled:
            failure_modes.append("ATTENTION_MISS")
        if rel_enabled and not rel_source:
            failure_modes.append("ENABLED_BUT_NO_RECORDED_OUTPUT")
        if rel_source and not rel_surfaced:
            failure_modes.append("SEEN_BUT_NOT_SURFACED")

        affected_groups = []
        for group in trial["composite"]["groups"]:
            group_eyes = {r["eye"] for r in group["source_rows"]}
            relevant_group = bool(group_eyes & set(relevant_eyes)) or group["channel"] in relevant_channels
            if relevant_group:
                affected_groups.append({
                    "channel": group["channel"],
                    "recommended_view": group["recommended_view"],
                    "distortion_flags": group["distortion_flags"],
                    "cancellation_fraction": group["cancellation_fraction"],
                    "largest_leave_one_out_mean_shift": group["largest_leave_one_out_mean_shift"],
                })
                for flag in group["distortion_flags"]:
                    failure_modes.append("FUSION_" + flag)

        if rel_source and rel_surfaced and not failure_modes:
            failure_modes.append("VISIBLE_IN_REPLAY")
        for mode in set(failure_modes):
            lesson_counter[mode] += 1

        score = 3 * len(rel_source) + 2 * len(rel_surfaced) + len(rel_channels)
        score -= sum(1 for x in failure_modes if x.startswith("FUSION_"))
        trial_rows.append({
            "trial_id": trial["trial_id"],
            "score": score,
            "relevant_enabled_eyes": rel_enabled,
            "relevant_source_eyes": rel_source,
            "relevant_surfaced_eyes": rel_surfaced,
            "relevant_channels_present": rel_channels,
            "failure_modes": sorted(set(failure_modes)),
            "affected_groups": affected_groups,
            "routing_reasons": {k: v for k, v in trial.get("routing_reasons", {}).items() if k in rel_enabled},
        })

    trial_rows.sort(key=lambda r: (-r["score"], r["trial_id"]))
    actions = []
    for mode, count in sorted(lesson_counter.items()):
        if mode == "ATTENTION_MISS":
            text = "Expand routing/compatibility search: later-relevant eyes were not enabled."
        elif mode == "ENABLED_BUT_NO_RECORDED_OUTPUT":
            text = "Inspect input contracts/execution: an enabled relevant eye produced no recorded channel."
        elif mode == "SEEN_BUT_NOT_SURFACED":
            text = "Improve foreground/salience logic: the relevant signal existed but was hidden from the report."
        elif mode == "FUSION_SIGN_CANCELLATION":
            text = "Keep signed layers separate before any summary; opposite contributions were capable of canceling."
        elif mode == "FUSION_SHARED_LINEAGE":
            text = "Downweight visual confidence from repeated lineage; seek an independent implementation or evidence source."
        elif mode == "FUSION_MIXED_SCALE":
            text = "Use multiscale overlay/commutator checks rather than collapsing resolutions."
        elif mode == "VISIBLE_IN_REPLAY":
            text = "The old trial already exposed the later-relevant signal; inspect interpretation/claim selection rather than routing."
        else:
            continue
        actions.append({"mode": mode, "trial_count": count, "learning_action": text})

    return {
        "ledger_replay": ledger_rows,
        "trial_replay": trial_rows,
        "closest_prior_trial": trial_rows[0]["trial_id"] if trial_rows else None,
        "learning_actions": actions,
        "rule": "Post-epiphany replay diagnoses the old sensing/routing/fusion process without rewriting what was known then.",
    }
