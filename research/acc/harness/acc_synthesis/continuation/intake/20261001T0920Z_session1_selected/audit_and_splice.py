#!/usr/bin/env python3
"""Validate fresh session-1 selected-row roads and exact-splice their lineages."""
import ast
import hashlib
import json
import re
import resource
import signal
import sys
import time
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
sys.path.insert(0, str(ROOT))
from official_checker import load_kernel

SOURCE = OUT / "source_snapshot.txt"
SOURCE_SHA256 = "b268515e51d35cca4add3ea499b72601a2157539963c10fd9ea456baa128382a"
SOURCE_BLOB = "ddfdb8d8d4fa4171d0a3f07b68b97a11bb0971bb"
SOURCE_HEAD = "61208aeb35f4d9fec6ab594319e9ac0c2c50a2bc"
POOL_SHA256 = "f10748695d7a8cf906df7cda342e8d4d9d82bbae04f60ffe8a63241b2bde063c"
OWN_SHA256 = "ff93a9ecbba27401dc2b5ca21aac85f52038d994b4e5681b85b9263936a506a9"
GOAL = ((1,), (2,))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def state(relators):
    return tuple(tuple(w) for w in relators)


def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError("session1 intake wall cap; incomplete, not a miss")))
    signal.alarm(180)
    started = time.monotonic()
    records = 0
    last_check = 0.0

    def tick(n=1):
        nonlocal records, last_check
        records += n
        if records > 600000:
            raise RuntimeError("session1 intake record cap; incomplete, not a miss")
        now = time.monotonic()
        if now - started > 180:
            raise TimeoutError("session1 intake wall cap; incomplete, not a miss")
        if now - last_check >= 0.1:
            cp = json.loads((ROOT / "continuation/checkpoint.json").read_text())
            if cp["stopped"] or cp["active"] is not None or cp.get("intake_lease"):
                raise RuntimeError("stop or competing lease observed")
            last_check = now

    assert sha(SOURCE) == SOURCE_SHA256
    pool_file = ROOT / "helpers/kernel_sources/roads_input.json"
    own_file = ROOT / "continuation/routes.json"
    assert sha(pool_file) == POOL_SHA256
    assert sha(own_file) == OWN_SHA256
    pool = json.loads(pool_file.read_text())
    own = json.loads(own_file.read_text())
    core, specs, pins, selected = load_kernel()

    fresh = []
    for line_number, line in enumerate(SOURCE.read_text().splitlines(), 1):
        match = re.fullmatch(r"(ac-\d{5}):\s*(\[.*\])", line.strip())
        if match:
            fresh.append({"row_id": match.group(1), "moves": ast.literal_eval(match.group(2)), "line": line_number})
    assert len(fresh) == 25
    assert all(r["row_id"] in selected for r in fresh)

    def replay(challenge, moves):
        s = state(challenge["initial_relators"])
        path = [s]
        for move in moves:
            s = core.apply_move(s, move)
            path.append(s)
            tick()
        return path

    # Independently validate every incoming road.
    receipts = []
    fresh_paths = []
    for fresh_index, route in enumerate(fresh):
        ch = selected[route["row_id"]]
        verdict = core.verify(ch, route["moves"], ch["move_spec_version"], pins["limits"])
        tick(len(route["moves"]) + 1)
        receipts.append({"fresh_index": fresh_index, "row_id": route["row_id"], "line": route["line"], "length": len(route["moves"]), "verdict": verdict})
        assert verdict["ok"]
        path = replay(ch, route["moves"])
        assert path[-1] == GOAL
        fresh_paths.append(path)

    own_keys = {(r["row_id"], tuple(r["moves"])) for r in own["routes"]}
    pool_keys = {(r["row_id"], tuple(r["moves"])) for r in pool["routes"]}
    exact_own_duplicates = [i for i, r in enumerate(fresh) if (r["row_id"], tuple(r["moves"])) in own_keys]
    exact_pool_duplicates = [i for i, r in enumerate(fresh) if (r["row_id"], tuple(r["moves"])) in pool_keys]
    fresh_lineage_indices = [i for i, r in enumerate(fresh) if (r["row_id"], tuple(r["moves"])) not in own_keys]

    own_by_row = defaultdict(list)
    for route in own["routes"]:
        own_by_row[route["row_id"]].append(route)
    baselines = {row: min(len(r["moves"]) for r in routes) for row, routes in own_by_row.items()}
    direct_improvements = []
    for i, route in enumerate(fresh):
        baseline = baselines[route["row_id"]]
        if len(route["moves"]) < baseline:
            direct_improvements.append({"fresh_index": i, "row_id": route["row_id"], "baseline": baseline, "length": len(route["moves"]), "moves": route["moves"], "saving": baseline - len(route["moves"]), "official_verdict": receipts[i]["verdict"]})

    candidate_map = {}
    one_junctions = 0
    interval_pairs = 0
    interval_shortening_derivations = 0
    match_summary = defaultdict(lambda: {"one_junction_matches": 0, "two_junction_pairs": 0, "shortening_intervals": 0})

    def verify_candidate(row, moves, derivation):
        baseline = baselines[row]
        if len(moves) >= baseline:
            return
        key = (row, tuple(moves))
        if key in candidate_map:
            candidate_map[key]["derivations"].append(derivation)
            return
        ch = selected[row]
        verdict = core.verify(ch, moves, ch["move_spec_version"], pins["limits"])
        tick(len(moves) + 1)
        assert verdict["ok"]
        candidate_map[key] = {"row_id": row, "baseline": baseline, "length": len(moves), "saving": baseline - len(moves), "moves": moves, "official_verdict": verdict, "derivations": [derivation]}

    # New donor suffixes by exact state, retaining all occurrences.
    suffixes = defaultdict(list)
    for fresh_index, route in enumerate(fresh):
        for j, s in enumerate(fresh_paths[fresh_index]):
            suffixes[s].append((fresh_index, j, route["moves"][j:]))

    for row, saved_routes in sorted(own_by_row.items()):
        ch = selected[row]
        for saved_index, saved in enumerate(saved_routes):
            saved_path = replay(ch, saved["moves"])
            saved_positions = defaultdict(list)
            for i, s in enumerate(saved_path):
                saved_positions[s].append(i)

            # One-junction selected prefix + any fresh suffix.
            for i, s in enumerate(saved_path):
                for fresh_index, j, suffix in suffixes.get(s, []):
                    one_junctions += 1
                    donor_row = fresh[fresh_index]["row_id"]
                    match_summary[(row, donor_row)]["one_junction_matches"] += 1
                    candidate = saved["moves"][:i] + suffix
                    verify_candidate(row, candidate, {"kind": "one_junction", "saved_route_index": saved_index, "saved_prefix": i, "fresh_index": fresh_index, "fresh_row": donor_row, "fresh_suffix": j})

            # Two-junction interval substitution from each fresh road, either direction.
            for fresh_index, donor in enumerate(fresh):
                donor_positions = defaultdict(list)
                for j, s in enumerate(fresh_paths[fresh_index]):
                    donor_positions[s].append(j)
                common = set(saved_positions) & set(donor_positions)
                matches = [(i, j) for s in common for i in saved_positions[s] for j in donor_positions[s]]
                for i1, j1 in matches:
                    for i2, j2 in matches:
                        if i1 >= i2:
                            continue
                        interval_pairs += 1
                        match_summary[(row, donor["row_id"])]["two_junction_pairs"] += 1
                        if j1 <= j2:
                            segment = donor["moves"][j1:j2]
                            direction = "forward"
                        else:
                            segment = [core.INVERSE_MOVE[m] for m in reversed(donor["moves"][j2:j1])]
                            direction = "reverse"
                        if len(segment) >= i2 - i1:
                            continue
                        interval_shortening_derivations += 1
                        match_summary[(row, donor["row_id"])]["shortening_intervals"] += 1
                        candidate = saved["moves"][:i1] + segment + saved["moves"][i2:]
                        verify_candidate(row, candidate, {"kind": "two_junction", "saved_route_index": saved_index, "saved_interval": [i1, i2], "fresh_index": fresh_index, "fresh_row": donor["row_id"], "fresh_interval": [j1, j2], "direction": direction})

    candidates = sorted(candidate_map.values(), key=lambda x: (x["row_id"], x["length"], x["moves"]))
    best_by_row = {}
    for candidate in candidates:
        best_by_row.setdefault(candidate["row_id"], candidate)
    result = {
        "schema": "acc-session1-selected-intake/1",
        "kind": "completed_exact_fresh_lineage_intake_and_splice",
        "algorithm_id": "exact-session1-lineage-junction-interval-v1",
        "source_head": SOURCE_HEAD,
        "source_git_blob": SOURCE_BLOB,
        "source_projection_sha256": SOURCE_SHA256,
        "official_commit": pins["source_commit"],
        "pool_sha256": POOL_SHA256,
        "selected_routes_sha256": OWN_SHA256,
        "incoming_routes": len(fresh),
        "verified_incoming_routes": sum(1 for r in receipts if r["verdict"]["ok"]),
        "incoming_rows": sorted({r["row_id"] for r in fresh}),
        "exact_own_duplicate_indices": exact_own_duplicates,
        "exact_pool_duplicate_indices": exact_pool_duplicates,
        "fresh_lineage_indices": fresh_lineage_indices,
        "fresh_lineage_count": len(fresh_lineage_indices),
        "direct_improvements": direct_improvements,
        "one_junction_occurrences": one_junctions,
        "two_junction_interval_pairs": interval_pairs,
        "shortening_interval_derivations": interval_shortening_derivations,
        "verified_improvement_count": len(candidates),
        "verified_improvement_rows": sorted(best_by_row),
        "best_by_row": list(best_by_row.values()),
        "match_summary": [{"selected_row": k[0], "fresh_row": k[1], **v} for k, v in sorted(match_summary.items()) if any(v.values())],
        "receipts": receipts,
        "primitive_records": records,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        "model_workers": 0,
        "new_move_searches": 0,
        "pool_mutated": False,
        "limits": {"seconds": 180, "memory_mib": 1024, "records": 600000},
        "scope": "Pinned-core replay plus exact state-equality suffix and interval composition only; no neighborhood search, API call, submission, or live score claim."
    }
    write(OUT / "receipt.json", result)
    write(OUT / "verified_candidates.json", {"candidates": candidates})
    signal.alarm(0)
    print(json.dumps({
        "verified_incoming": result["verified_incoming_routes"],
        "fresh_lineages": result["fresh_lineage_count"],
        "one_junctions": one_junctions,
        "interval_pairs": interval_pairs,
        "shortening_intervals": interval_shortening_derivations,
        "verified_improvements": len(candidates),
        "rows": sorted(best_by_row),
        "records": records,
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
