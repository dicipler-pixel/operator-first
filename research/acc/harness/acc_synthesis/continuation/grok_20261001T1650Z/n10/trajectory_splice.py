"""Finite paid-join graph of existing traces; no new-state search."""
import hashlib
import heapq
import itertools
import json
import resource
import signal
import time
from collections import defaultdict

from replay import HERE, HARNESS, encode, text, replay, CORE_PIN
from verifier.core import apply_move, invert, INVERSE_MOVE, GENS

resource.setrlimit(resource.RLIMIT_AS, (192 * 1024 * 1024,) * 2)
BASE = json.loads((HERE / "replay_receipt.json").read_text())["n10_full119_verified_not_competitive"]
MANIFEST = json.loads((HARNESS / "integration/repo/official_manifest.json").read_text())
SOURCE = HARNESS / "continuation/intake/20261001T0735Z_step2_junction/source_snapshot.txt"
ROWS = {c["challenge_id"]: c for c in MANIFEST["challenges"] if c["challenge_id"] in ["ac-05698", "ac-06792"]}
ROUTES = {}
for line in SOURCE.read_text().splitlines():
    if line.split(":")[0] in ROWS:
        name, route = line.split(":", 1)
        ROUTES[name] = json.loads(route)

def im(w, gen):
    return tuple(gen[abs(a)-1] * (1 if a > 0 else -1) for a in w)

def signature(word):
    if not word:
        return ()
    # Full words only: no silent cyclic reduction/conjugating-tail removal.
    return min(w[i:] + w[:i] for w in [word, invert(word)] for i in range(len(word)))

def join(a, b):
    moves = []
    for j in range(2):
        opts = []
        for inv in [False, True]:
            w = invert(a[j]) if inv else a[j]
            if len(w) != len(b[j]):
                continue
            if not w and not b[j]:
                opts.append([])
            for k in range(len(w)):
                if w[k:] + w[:k] != b[j]:
                    continue
                conjugators = tuple(-x for x in w[:k]) if k <= len(w)-k else tuple(reversed(w[k:]))
                opts.append(([j] if inv else []) + [6 + 4*j + GENS.index(x) for x in conjugators])
        if not opts:
            return None
        moves += min(opts, key=len)
    s = a
    for m in moves:
        s = apply_move(s, m)
    assert s == b
    return moves

def main():
    start_time = time.monotonic()
    count = 0
    graph = defaultdict(dict)
    def edge(a, b, route):
        old = graph[a].get(b)
        if old is None or len(route) < len(old):
            graph[a][b] = route
    def put(start, route):
        result = [start]
        for m in route:
            nxt = apply_move(result[-1], m)
            edge(result[-1], nxt, [m])
            edge(nxt, result[-1], [INVERSE_MOVE[m]])
            result.append(nxt)
        return result
    oldstates = set()
    for rid, route in ROUTES.items():
        states = put(tuple(tuple(w) for w in ROWS[rid]["initial_relators"]), route)
        assert states[-1] == ((1,), (2,))
        oldstates.update(states)
    newstates = set()
    original_start = tuple(encode(w) for w in BASE["start"])
    for ordering in [(1, 2), (2, 1)]:
        for signs in itertools.product([1, -1], repeat=2):
            gen = tuple(a*b for a, b in zip(ordering, signs))
            for swapped in [False, True]:
                mapped = tuple(im(w, gen) for w in original_start)
                if swapped:
                    mapped = mapped[::-1]
                route = []
                for m in BASE["moves"]:
                    if m < 6:
                        route.append(([1, 0, 4, 5, 2, 3][m] if swapped else m))
                    else:
                        relator = (m - 6) // 4
                        if swapped:
                            relator = 1-relator
                        route.append(6 + relator*4 + GENS.index(im((GENS[(m-6)%4],), gen)[0]))
                newstates.update(put(mapped, route))
    index = defaultdict(list)
    for state in newstates:
        index[tuple(signature(w) for w in state)].append(state)
    joins = 0
    for a in oldstates:
        for b in index.get(tuple(signature(w) for w in a), []):
            count += 1
            if count > 100000 or time.monotonic() - start_time > 10:
                raise RuntimeError("budget exceeded before finite graph completed")
            route = join(a, b)
            if route is not None:
                edge(a, b, route)
                edge(b, a, [INVERSE_MOVE[m] for m in reversed(route)])
                joins += 1
    results = []
    for rid in ROUTES:
        start = tuple(tuple(w) for w in ROWS[rid]["initial_relators"])
        queue = [(0, start)]
        dist = {start: 0}
        parent = {}
        goal = ((1,), (2,))
        while queue:
            cost, state = heapq.heappop(queue)
            if cost != dist[state]:
                continue
            if state == goal:
                break
            for nxt, route in graph[state].items():
                newcost = cost + len(route)
                if newcost < dist.get(nxt, 10**9):
                    dist[nxt] = newcost
                    parent[nxt] = (state, route)
                    heapq.heappush(queue, (newcost, nxt))
        segments = []
        state = goal
        while state != start:
            state, route = parent[state]
            segments.append(route)
        route = [m for s in reversed(segments) for m in s]
        result = replay(text(start), route, ["x", "y"])
        results.append({"challenge_id": rid, "old_length": len(ROUTES[rid]),
                        "finite_graph_best": len(route), "reported_team_best": 110 if rid == "ac-05698" else 117,
                        "verified": result})
    receipt = {"core_sha256": CORE_PIN, "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
               "canonical_source_length": len(BASE["moves"]), "old_trace_states": len(oldstates),
               "transformed_trace_states": len(newstates), "joins": joins, "comparisons": count,
               "graph_nodes": len(graph), "bounds": {"seconds": 10, "memory_bytes": 192*1024*1024,
                                                     "comparisons": 100000},
               "elapsed_seconds": time.monotonic()-start_time, "classification": "completed_finite_trace_graph",
               "free_relabeling_edges_added": False, "new_state_search": False,
               "results": results}
    (HERE / "trajectory_splice_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"comparisons": count, "joins": joins, "elapsed_seconds": receipt["elapsed_seconds"],
                      "lengths": [(r["challenge_id"], r["old_length"], r["finite_graph_best"], r["reported_team_best"]) for r in results]}))

if __name__ == "__main__":
    main()
