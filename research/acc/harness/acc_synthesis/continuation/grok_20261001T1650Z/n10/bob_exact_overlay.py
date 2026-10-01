"""One bounded data-only overlay against Bob's recovered archived routes."""
import hashlib
import itertools
import json
import resource
import signal
import time

from replay import HERE, HARNESS, encode, text, replay, CORE_PIN
from verifier.core import apply_move, invert, verify

MEMORY = 192 * 1024 * 1024
resource.setrlimit(resource.RLIMIT_AS, (MEMORY, MEMORY))
SOURCE = HARNESS / "helpers/bob_sources/research/acc/live/bob/bob_crossclass_bundle2_20260929.json"
MANIFEST_PATH = HARNESS / "integration/repo/official_manifest.json"
TWINS_PATH = HARNESS / "helpers/kernel_sources/research/acc/live/ledger/kernel_ms_twin_groups_20260928.json"
BASE_PATH = HERE / "replay_receipt.json"
FORBIDDEN = {"09839", "02257", "09311", "06403", "04718", "05378"}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def cyclic(word):
    if not word:
        return ()
    return min(w[i:] + w[:i] for w in [word, invert(word)] for i in range(len(word)))

def twin_key(state):
    keys = []
    for order in [(1, 2), (2, 1)]:
        for signs in itertools.product([1, -1], repeat=2):
            gen = tuple(a*b for a, b in zip(order, signs))
            mapped = [tuple(gen[abs(a)-1] * (1 if a > 0 else -1) for a in w) for w in state]
            keys.append(tuple(sorted(cyclic(w) for w in mapped)))
    return min(keys)

def main():
    start_time = time.monotonic()
    def expired(signum, frame):
        raise TimeoutError()
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 15)
    report = {"classification": "running", "core_sha256": CORE_PIN,
              "source_hashes": {str(p.relative_to(HARNESS)): digest(p) for p in [SOURCE, MANIFEST_PATH, TWINS_PATH, BASE_PATH]},
              "bounds": {"wall_seconds": 15, "memory_bytes": MEMORY, "primitive_and_comparison_records": 100000},
              "forbidden_numeric_ids": sorted(FORBIDDEN), "skipped": [], "donors": [], "matches": [],
              "records": 0, "primitive_replays": 0, "exact_state_comparisons": 0,
              "best_canonical_length": 119, "best_route": None, "new_scored_candidate": False}
    try:
        assert digest(HARNESS / "vendor/verifier/core.py") == CORE_PIN
        manifest = {c["challenge_id"]: c for c in json.loads(MANIFEST_PATH.read_text())["challenges"]}
        rows = json.loads(SOURCE.read_text())["rows"]
        forbidden_keys = {twin_key(tuple(tuple(w) for w in c["initial_relators"]))
                          for rid, c in manifest.items() if rid.startswith("ac-") and rid[-5:] in FORBIDDEN}
        named_twins = set()
        for group in json.loads(TWINS_PATH.read_text()):
            ids = group["kernel_rows"] + group["twins"]
            if any(rid[-5:] in FORBIDDEN for rid in ids):
                named_twins.update(ids)
        report["known_named_twins"] = sorted(named_twins)
        base = json.loads(BASE_PATH.read_text())["n10_full119_verified_not_competitive"]
        start = tuple(encode(w) for w in base["start"])
        state = start
        indexes = {state: 0}
        for i, m in enumerate(base["moves"], 1):
            state = apply_move(state, m)
            report["primitive_replays"] += 1
            indexes.setdefault(state, i)
        assert state == ((1,), (2,))
        best = list(base["moves"])
        for row in rows:
            rid = row["id"]
            if rid[-5:] in FORBIDDEN or rid in named_twins:
                report["skipped"].append({"row": rid, "reason": "forbidden_id_or_known_named_twin"})
                continue
            if rid not in manifest or not rid.startswith("ac-"):
                report["skipped"].append({"row": rid, "reason": "not_in_official_ac_manifest"})
                continue
            state = tuple(tuple(w) for w in row["start"])
            if list(map(list, state)) != manifest[rid]["initial_relators"]:
                report["skipped"].append({"row": rid, "reason": "manifest_start_mismatch"})
                continue
            if twin_key(state) in forbidden_keys:
                report["skipped"].append({"row": rid, "reason": "forbidden_signed_cyclic_twin"})
                continue
            route = row["moves"]
            if any(type(m) is not int or not 0 <= m < 14 for m in route):
                report["skipped"].append({"row": rid, "reason": "bad_move_id"})
                continue
            if report["primitive_replays"] + report["exact_state_comparisons"] + 2*len(route) + 1 > 99500:
                report["classification"] = "record_cap_incomplete"
                break
            matches = []
            if state in indexes:
                matches.append((indexes[state], 0))
            report["exact_state_comparisons"] += 1
            peak = sum(map(len, state))
            for j, m in enumerate(route, 1):
                state = apply_move(state, m)
                report["primitive_replays"] += 1
                peak = max(peak, sum(map(len, state)))
                if state in indexes:
                    matches.append((indexes[state], j))
                report["exact_state_comparisons"] += 1
            valid = state == ((1,), (2,))
            report["donors"].append({"id": rid, "length": len(route), "official_core_final_xy": valid,
                                     "peak_total_length": peak, "exact_join_count": len(matches)})
            if not valid:
                continue
            for i, j in matches:
                length = i + len(route) - j
                if length < len(best):
                    best = base["moves"][:i] + route[j:]
                    report["matches"].append({"donor": rid, "canonical_prefix_length": i,
                                              "donor_suffix_start": j, "new_length": length})
        else:
            report["classification"] = "completed_exact_overlay"
        synthetic = {"challenge_id": "diagnostic-n10", "move_spec_version": "ac-r2-v1",
                     "initial_relators": start, "target_relators": ((1,), (2,))}
        result = verify(synthetic, best, "ac-r2-v1", {"max_path_length": 1000,
                         "max_total_relator_length": 100000, "max_work": 100000000})
        assert result["ok"]
        report["primitive_replays"] += len(best)
        report["best_canonical_length"] = len(best)
        report["best_route"] = best
        report["official_core_receipt"] = result
        report["row_transfer_pending"] = len(best) < len(base["moves"])
        report["comparison"] = "Canonical route only. Reported row incumbents are110/117; a paid row transfer is required before any candidate claim."
    except TimeoutError:
        report["classification"] = "wall_cap_incomplete"
    except MemoryError:
        report["classification"] = "memory_cap_incomplete"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        report["records"] = report["primitive_replays"] + report["exact_state_comparisons"]
        report["elapsed_seconds"] = time.monotonic() - start_time
        (HERE / "bob_exact_overlay_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["classification", "records", "elapsed_seconds", "best_canonical_length"]}
                     | {"verified_donors": len(report["donors"]), "skipped": len(report["skipped"]), "improving_joins": report["matches"]}))

if __name__ == "__main__":
    main()
