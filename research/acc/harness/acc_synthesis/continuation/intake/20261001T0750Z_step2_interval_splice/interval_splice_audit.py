#!/usr/bin/env python3
"""Exact two-junction interval splices from fresh donor roads into selected roads."""
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
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT))
from official_checker import load_kernel

SOURCE = ROOT / "continuation/intake/20261001T0735Z_step2_junction/source_snapshot.txt"
SOURCE_SHA256 = "c740509b1a9c3107f58d316bf0997b333b8313af1b8e7a4da50ab604e13e41e5"
SOURCE_BLOB = "c7702f14dcf3334a1706c5c78714c7da2c027106"
SOURCE_HEAD_REVIEWED = "5f0208687c7654abbf554d3d4ee1a3bb3dffcdb1"
MANIFEST_SHA256 = "dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37"
POOL_SHA256 = "f10748695d7a8cf906df7cda342e8d4d9d82bbae04f60ffe8a63241b2bde063c"
OWN_SHA256 = "ff93a9ecbba27401dc2b5ca21aac85f52038d994b4e5681b85b9263936a506a9"
GOAL = ((1,), (2,))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def state(relators):
    return tuple(tuple(w) for w in relators)


def write(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    resource.setrlimit(resource.RLIMIT_AS, (1024**3, 1024**3))
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(
        TimeoutError("interval-splice wall cap; incomplete, not a miss")))
    signal.alarm(180)
    started = time.monotonic()
    primitive_records = 0
    last_stop_check = 0.0

    def tick(n=1):
        nonlocal primitive_records, last_stop_check
        primitive_records += n
        if primitive_records > 600000:
            raise RuntimeError("interval-splice record cap; incomplete, not a miss")
        now = time.monotonic()
        if now - started > 180:
            raise TimeoutError("interval-splice wall cap; incomplete, not a miss")
        if now - last_stop_check >= 0.1:
            cp = json.loads((ROOT / "continuation/checkpoint.json").read_text())
            if cp["stopped"] or cp["active"] is not None or cp.get("intake_lease"):
                raise RuntimeError("stop or competing lease observed")
            last_stop_check = now

    assert sha(SOURCE) == SOURCE_SHA256
    manifest_file = WORKSPACE / "manifest/unpacked/manifest.json"
    pool_file = ROOT / "helpers/kernel_sources/roads_input.json"
    own_file = ROOT / "continuation/routes.json"
    assert sha(manifest_file) == MANIFEST_SHA256
    assert sha(pool_file) == POOL_SHA256
    assert sha(own_file) == OWN_SHA256

    donor_routes = []
    for line_number, line in enumerate(SOURCE.read_text().splitlines(), 1):
        match = re.fullmatch(r"(ac-\d{5}):\s*(\[.*\])", line.strip())
        if match:
            donor_routes.append({"row_id": match.group(1), "moves": ast.literal_eval(match.group(2)), "line": line_number})
    assert len(donor_routes) == 4

    manifest = json.loads(manifest_file.read_text())
    manifest_rows = {c["challenge_id"]: c for c in manifest["challenges"]}
    own = json.loads(own_file.read_text())
    core, specs, pins, selected = load_kernel()

    def replay(challenge, moves):
        s = state(challenge["initial_relators"])
        path = [s]
        for move in moves:
            s = core.apply_move(s, move)
            path.append(s)
            tick()
        return path

    donor_paths = {}
    donor_receipts = []
    for route in donor_routes:
        ch = manifest_rows[route["row_id"]]
        verdict = core.verify(ch, route["moves"], ch["move_spec_version"], manifest["limits"])
        tick(len(route["moves"]) + 1)
        assert verdict["ok"]
        path = replay(ch, route["moves"])
        assert path[-1] == GOAL
        donor_paths[route["row_id"]] = path
        donor_receipts.append({"row_id": route["row_id"], "length": len(route["moves"]), "verdict": verdict})

    routes_by_row = defaultdict(list)
    for route in own["routes"]:
        routes_by_row[route["row_id"]].append(route)
    baselines = {row: min(len(r["moves"]) for r in routes) for row, routes in routes_by_row.items()}

    examined_intervals = 0
    nontrivial_intervals = 0
    shortening_intervals = []
    verified_by_moves = {}
    pair_summaries = []

    for selected_row, selected_routes in sorted(routes_by_row.items()):
        ch = selected[selected_row]
        baseline = baselines[selected_row]
        for selected_route_index, selected_route in enumerate(selected_routes):
            selected_path = replay(ch, selected_route["moves"])
            selected_positions = defaultdict(list)
            for i, s in enumerate(selected_path):
                selected_positions[s].append(i)
            for donor_route in donor_routes:
                donor_row = donor_route["row_id"]
                donor_path = donor_paths[donor_row]
                donor_positions = defaultdict(list)
                for j, s in enumerate(donor_path):
                    donor_positions[s].append(j)
                common = sorted(set(selected_positions) & set(donor_positions), key=repr)
                matches = []
                for s in common:
                    for i in selected_positions[s]:
                        for j in donor_positions[s]:
                            matches.append((i, j, s))
                pair_nontrivial = 0
                pair_best_delta = None
                for left in range(len(matches)):
                    i1, j1, _ = matches[left]
                    for right in range(len(matches)):
                        i2, j2, _ = matches[right]
                        if i1 >= i2:
                            continue
                        examined_intervals += 1
                        if j1 <= j2:
                            segment = donor_route["moves"][j1:j2]
                            direction = "forward"
                        else:
                            segment = [core.INVERSE_MOVE[m] for m in reversed(donor_route["moves"][j2:j1])]
                            direction = "reverse"
                        old_length = i2 - i1
                        new_length = len(segment)
                        delta = old_length - new_length
                        if delta != 0 or j1 != j2:
                            nontrivial_intervals += 1
                            pair_nontrivial += 1
                        if pair_best_delta is None or delta > pair_best_delta:
                            pair_best_delta = delta
                        if delta <= 0:
                            continue
                        candidate = selected_route["moves"][:i1] + segment + selected_route["moves"][i2:]
                        item = {
                            "selected_row": selected_row,
                            "baseline": baseline,
                            "source_route_length": len(selected_route["moves"]),
                            "candidate_length": len(candidate),
                            "saving_vs_source": len(selected_route["moves"]) - len(candidate),
                            "saving_vs_baseline": baseline - len(candidate),
                            "selected_route_index": selected_route_index,
                            "selected_interval": [i1, i2],
                            "donor_row": donor_row,
                            "donor_interval": [j1, j2],
                            "donor_direction": direction,
                        }
                        shortening_intervals.append(item)
                        if len(candidate) >= baseline:
                            continue
                        key = tuple(candidate)
                        prior = verified_by_moves.get(key)
                        if prior is not None:
                            prior["derivations"].append(item)
                            continue
                        verdict = core.verify(ch, candidate, ch["move_spec_version"], pins["limits"])
                        tick(len(candidate) + 1)
                        assert verdict["ok"]
                        verified_by_moves[key] = {
                            "row_id": selected_row,
                            "moves": candidate,
                            "length": len(candidate),
                            "baseline": baseline,
                            "saving": baseline - len(candidate),
                            "official_verdict": verdict,
                            "derivations": [item],
                        }
                if len(matches) > 1:
                    pair_summaries.append({
                        "selected_row": selected_row,
                        "selected_route_index": selected_route_index,
                        "donor_row": donor_row,
                        "exact_match_occurrences": len(matches),
                        "distinct_common_states": len(common),
                        "examined_pair_intervals": len(matches) * (len(matches) - 1) // 2,
                        "nontrivial_intervals": pair_nontrivial,
                        "best_segment_saving": pair_best_delta,
                    })

    improvements = sorted(verified_by_moves.values(), key=lambda x: (x["row_id"], x["length"], x["moves"]))
    best_by_row = {}
    for item in improvements:
        best_by_row.setdefault(item["row_id"], item)

    result = {
        "schema": "acc-step2-interval-splice-audit/1",
        "kind": "completed_read_only_exact_two_junction_splice",
        "algorithm_id": "exact-two-junction-donor-interval-splice-v1",
        "source_head_reviewed": SOURCE_HEAD_REVIEWED,
        "source_git_blob": SOURCE_BLOB,
        "source_sha256": SOURCE_SHA256,
        "official_commit": pins["source_commit"],
        "manifest_sha256": MANIFEST_SHA256,
        "pool_sha256": POOL_SHA256,
        "selected_routes_sha256": OWN_SHA256,
        "donor_receipts": donor_receipts,
        "pair_summaries": pair_summaries,
        "examined_intervals": examined_intervals,
        "nontrivial_intervals": nontrivial_intervals,
        "shortening_interval_derivations": len(shortening_intervals),
        "verified_improvement_count": len(improvements),
        "verified_improvement_rows": sorted(best_by_row),
        "best_by_row": list(best_by_row.values()),
        "primitive_records": primitive_records,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        "model_workers": 0,
        "new_move_searches": 0,
        "pool_mutated": False,
        "limits": {"seconds": 180, "memory_mib": 1024, "records": 600000},
        "scope": "Exact interval substitution only between two identical saved states; no neighborhood search, board claim, API call, or submission."
    }
    write(OUT / "receipt.json", result)
    write(OUT / "verified_candidates.json", {"candidates": improvements})
    write(OUT / "shortening_derivations.json", {"derivations": shortening_intervals})
    signal.alarm(0)
    print(json.dumps({
        "examined_intervals": examined_intervals,
        "nontrivial_intervals": nontrivial_intervals,
        "shortening_derivations": len(shortening_intervals),
        "verified_improvements": len(improvements),
        "rows": sorted(best_by_row),
        "records": primitive_records,
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
