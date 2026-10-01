#!/usr/bin/env python3
"""Replay four fresh UPGH donor roads and test exact saved-route junctions.

This intentionally does not repeat the interrupted full-graph BFS.  It only
measures graph delta and checks exact states already present on saved selected
routes against suffixes of the new donor roads.
"""
import ast
import hashlib
import json
import re
import resource
import signal
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
WORKSPACE = ROOT.parent
sys.path.insert(0, str(ROOT))

from official_checker import load_kernel

MANIFEST_SHA256 = "dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37"
POOL_SHA256 = "f10748695d7a8cf906df7cda342e8d4d9d82bbae04f60ffe8a63241b2bde063c"
OWN_SHA256 = "ff93a9ecbba27401dc2b5ca21aac85f52038d994b4e5681b85b9263936a506a9"
SOURCE_BLOB = "c7702f14dcf3334a1706c5c78714c7da2c027106"
SOURCE_HEAD = "8ee0173c8925124c509e98a19038b4cd64638f96"
SOURCE_PATH = "research/acc/live/inbox/upgh_bs_doubling2_20261001T0646Z.txt"
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
        TimeoutError("junction audit wall cap; incomplete, not a miss")))
    signal.alarm(180)
    started = time.monotonic()
    records = 0
    last_stop_check = 0.0

    def tick(n=1):
        nonlocal records, last_stop_check
        records += n
        if records > 600000:
            raise RuntimeError("junction audit record cap; incomplete, not a miss")
        now = time.monotonic()
        if now - started > 180:
            raise TimeoutError("junction audit wall cap; incomplete, not a miss")
        if now - last_stop_check >= 0.1:
            checkpoint = json.loads((ROOT / "continuation/checkpoint.json").read_text())
            if checkpoint["stopped"] or checkpoint["active"] is not None or checkpoint.get("intake_lease"):
                raise RuntimeError("stop or competing lease observed")
            last_stop_check = now

    source_file = OUT / "source_snapshot.txt"
    manifest_file = WORKSPACE / "manifest/unpacked/manifest.json"
    pool_file = ROOT / "helpers/kernel_sources/roads_input.json"
    own_file = ROOT / "continuation/routes.json"
    assert sha(manifest_file) == MANIFEST_SHA256
    assert sha(pool_file) == POOL_SHA256
    assert sha(own_file) == OWN_SHA256

    donor_routes = []
    for line_number, line in enumerate(source_file.read_text().splitlines(), 1):
        match = re.fullmatch(r"(ac-\d{5}):\s*(\[.*\])", line.strip())
        if match:
            donor_routes.append({
                "row_id": match.group(1),
                "moves": ast.literal_eval(match.group(2)),
                "source_line": line_number,
            })
    assert len(donor_routes) == 4
    assert len({r["row_id"] for r in donor_routes}) == 4

    manifest = json.loads(manifest_file.read_text())
    manifest_rows = {c["challenge_id"]: c for c in manifest["challenges"]}
    pool = json.loads(pool_file.read_text())
    own = json.loads(own_file.read_text())
    core, specs, pins, selected = load_kernel()
    from verifier.canon import instance_hash

    # Validate the four records and roads against the pinned official core.
    receipts = []
    donor_state_suffixes = {}
    donor_paths = {}
    for route in donor_routes:
        row = route["row_id"]
        challenge = manifest_rows[row]
        expected_hash = instance_hash(
            challenge["challenge_id"], challenge["generators"],
            challenge["initial_relators"], challenge["target_relators"],
            challenge["move_spec_version"],
            specs.get(challenge["move_spec_version"]).move_spec_hash,
        )
        assert expected_hash == challenge["instance_hash"]
        verdict = core.verify(challenge, route["moves"], challenge["move_spec_version"], manifest["limits"])
        tick(len(route["moves"]) + 1)
        receipts.append({
            "row_id": row,
            "length": len(route["moves"]),
            "source_line": route["source_line"],
            "instance_hash": expected_hash,
            "verdict": verdict,
        })
        assert verdict["ok"]
        s = state(challenge["initial_relators"])
        path = [s]
        for move in route["moves"]:
            s = core.apply_move(s, move)
            path.append(s)
            tick()
        assert s == GOAL
        donor_paths[row] = path
        for index, donor_state in enumerate(path):
            suffix = route["moves"][index:]
            current = donor_state_suffixes.get(donor_state)
            if current is None or len(suffix) < len(current["moves"]):
                donor_state_suffixes[donor_state] = {
                    "row_id": row,
                    "path_index": index,
                    "moves": suffix,
                }

    # Determine exact route/edge novelty without doing global shortest paths.
    old_states = set()
    old_edges = set()

    def record_path(challenge, moves, states_set, edges_set):
        s = state(challenge["initial_relators"])
        states_set.add(s)
        for move in moves:
            u = core.apply_move(s, move)
            states_set.add(u)
            edges_set.add((s, u, move))
            edges_set.add((u, s, core.INVERSE_MOVE[move]))
            s = u
            tick()
        return s

    pool_challenges = pool["challenges"]
    for route in pool["routes"]:
        assert record_path(pool_challenges[route["row_id"]], route["moves"], old_states, old_edges) == GOAL
    for route in own["routes"]:
        assert record_path(selected[route["row_id"]], route["moves"], old_states, old_edges) == GOAL

    donor_states = set()
    donor_edges = set()
    for route in donor_routes:
        assert record_path(manifest_rows[route["row_id"]], route["moves"], donor_states, donor_edges) == GOAL

    # Exact route junction: selected prefix + donor suffix at an identical state.
    selected_routes = {}
    for route in own["routes"]:
        selected_routes.setdefault(route["row_id"], []).append(route)
    junctions = []
    improvements = []
    row_summaries = []
    for row, challenge in selected.items():
        routes = selected_routes.get(row, [])
        baseline = min((len(r["moves"]) for r in routes), default=None)
        best_candidate = None
        nontrivial = 0
        matched_states = set()
        for route_index, route in enumerate(routes):
            prefix = []
            s = state(challenge["initial_relators"])
            for path_index in range(len(route["moves"]) + 1):
                donor = donor_state_suffixes.get(s)
                if donor is not None:
                    matched_states.add(s)
                    candidate = prefix + donor["moves"]
                    is_nontrivial = s != GOAL and path_index > 0 and len(donor["moves"]) > 0
                    if is_nontrivial:
                        nontrivial += 1
                    if baseline is not None and len(candidate) < baseline:
                        verdict = core.verify(challenge, candidate, challenge["move_spec_version"], pins["limits"])
                        tick(len(candidate) + 1)
                        assert verdict["ok"]
                        item = {
                            "row_id": row,
                            "baseline": baseline,
                            "candidate_length": len(candidate),
                            "saving": baseline - len(candidate),
                            "selected_route_index": route_index,
                            "selected_prefix_length": path_index,
                            "donor_row_id": donor["row_id"],
                            "donor_path_index": donor["path_index"],
                            "moves": candidate,
                            "official_verdict": verdict,
                        }
                        junctions.append(item)
                        if best_candidate is None or len(candidate) < best_candidate["candidate_length"]:
                            best_candidate = item
                if path_index < len(route["moves"]):
                    move = route["moves"][path_index]
                    s = core.apply_move(s, move)
                    prefix.append(move)
                    tick()
        if best_candidate is not None:
            improvements.append(best_candidate)
        row_summaries.append({
            "row_id": row,
            "saved_route_count": len(routes),
            "baseline": baseline,
            "matched_exact_states": len(matched_states),
            "nontrivial_junction_occurrences": nontrivial,
            "best_candidate_length": None if best_candidate is None else best_candidate["candidate_length"],
        })

    exact_duplicates = []
    pool_keys = {(r["row_id"], tuple(r["moves"])) for r in pool["routes"]}
    for route in donor_routes:
        if (route["row_id"], tuple(route["moves"])) in pool_keys:
            exact_duplicates.append(route["row_id"])

    result = {
        "schema": "acc-step2-junction-audit/1",
        "kind": "completed_read_only_exact_route_junction",
        "algorithm_id": "exact-saved-route-to-fresh-donor-junction-v1",
        "source_head": SOURCE_HEAD,
        "source_path": SOURCE_PATH,
        "source_git_blob": SOURCE_BLOB,
        "source_sha256": sha(source_file),
        "official_commit": pins["source_commit"],
        "manifest_sha256": MANIFEST_SHA256,
        "pool_sha256": POOL_SHA256,
        "selected_routes_sha256": OWN_SHA256,
        "donor_receipts": receipts,
        "exact_pool_duplicates": exact_duplicates,
        "old_graph_vertices": len(old_states),
        "old_directed_edges": len(old_edges),
        "donor_vertices": len(donor_states),
        "donor_directed_edges": len(donor_edges),
        "new_vertices_vs_saved_graph": len(donor_states - old_states),
        "new_directed_edges_vs_saved_graph": len(donor_edges - old_edges),
        "selected_rows": row_summaries,
        "selected_improvements": improvements,
        "verified_improvement_count": len(improvements),
        "junction_candidate_count": len(junctions),
        "primitive_records": records,
        "elapsed_seconds": time.monotonic() - started,
        "peak_rss_mib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
        "model_workers": 0,
        "row_searches": 0,
        "pool_mutated": False,
        "limits": {"seconds": 180, "memory_mib": 1024, "records": 600000},
        "scope": (
            "Exact verifier replay, graph-delta count, and state-equality joins between saved selected-route "
            "prefixes and fresh donor suffixes. No global shortest-path claim, board claim, or submission."
        ),
    }
    write(OUT / "receipt.json", result)
    write(OUT / "candidates.json", {"candidates": junctions})
    signal.alarm(0)
    print(json.dumps({
        "verified_donors": sum(1 for r in receipts if r["verdict"]["ok"]),
        "new_vertices": result["new_vertices_vs_saved_graph"],
        "new_directed_edges": result["new_directed_edges_vs_saved_graph"],
        "nontrivial_junctions": sum(r["nontrivial_junction_occurrences"] for r in row_summaries),
        "verified_improvements": len(improvements),
        "records": records,
        "elapsed_seconds": result["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
