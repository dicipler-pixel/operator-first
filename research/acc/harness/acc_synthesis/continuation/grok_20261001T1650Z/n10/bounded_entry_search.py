"""Bounded frozen-r1 beam probe, never a proof of nonexistence."""
import hashlib
import json
import pathlib
import resource
import signal
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
HARNESS = HERE.parents[2]
sys.path.insert(0, str(HARNESS / "vendor"))
from verifier.core import apply_move
from replay import CORE_PIN, BLOCK, encode, text, replay

MEMORY = 192 * 1024 * 1024
WALL = 20
MAX_STATES = 100000
MAX_DEPTH = 34
BEAM = 600
MOVES = [0, 2, 3, 6, 7, 8, 9]
TOTAL_CAP = 80
resource.setrlimit(resource.RLIMIT_AS, (MEMORY, MEMORY))
assert hashlib.sha256((HARNESS / "vendor/verifier/core.py").read_bytes()).hexdigest() == CORE_PIN
START = (encode("YYxxxxyyyyyyyXYYYY"), encode("xxYYXyy"))
TARGET = (encode("YY" + "x" * 16 + "yyyX"), START[1])

def ranked(word):
    # A conjectural rank only: match the five-run target up to cyclic frame.
    # The terminal goal comparison always uses the exact ordered state.
    runs = []
    for c in word:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
        else:
            runs.append([c, 1])
    cyclic = len(runs) - int(len(runs) > 1 and runs[0][0] == runs[-1][0])
    yp = sum(c == 2 for c in word)
    yn = sum(c == -2 for c in word)
    xp = sum(c == 1 for c in word)
    xn = sum(c == -1 for c in word)
    longest_x = max((n for c, n in runs if c == 1), default=0)
    excess_y = abs(yp - 3) + abs(yn - 2)
    exponent_gap = min(abs(xp - xn - 15), abs(xn - xp - 15))
    return (4 * excess_y + 3 * abs(cyclic - 5) + exponent_gap +
            max(0, xp - longest_x) + 2 * abs(xn - 1))

def run():
    start_time = time.monotonic()
    report = {"core_sha256": CORE_PIN, "start": text(START), "target": text(TARGET),
              "prefix_moves": BLOCK, "method": "frozen-r1 heuristic beam",
              "bounds": {"wall_seconds": WALL, "memory_bytes": MEMORY,
                         "max_states": MAX_STATES, "max_depth": MAX_DEPTH,
                         "beam_width": BEAM, "max_total_relator_length": TOTAL_CAP},
              "classification": "not_started", "miss_is_proof": False,
              "layers": [], "generated": 0, "seen": 1, "solution": None}
    def expired(signum, frame):
        raise TimeoutError("wall cap")
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, WALL)
    frontier = [(START[0], [])]
    seen = {START[0]}
    try:
        for depth in range(1, MAX_DEPTH + 1):
            nxt = []
            stop = False
            for word, path in frontier:
                for m in MOVES:
                    report["generated"] += 1
                    after = apply_move((word, START[1]), m)
                    if after[0] in seen or sum(map(len, after)) > TOTAL_CAP:
                        continue
                    seen.add(after[0])
                    if after == TARGET:
                        report["solution"] = path + [m]
                        report["classification"] = "hit"
                        stop = True
                        break
                    nxt.append((after[0], path + [m]))
                    if len(seen) >= MAX_STATES:
                        report["classification"] = "state_cap"
                        stop = True
                        break
                if stop:
                    break
            report["layers"].append({"depth": depth, "generated_new": len(nxt), "seen": len(seen)})
            if stop:
                break
            if not nxt:
                report["classification"] = "restricted_frontier_exhausted"
                break
            # Global choice plus abelian x-exponent bins preserves distinct runs.
            nxt.sort(key=lambda item: (ranked(item[0]), len(item[0]), item[0]))
            chosen = nxt[:BEAM // 2]
            bins = {}
            for item in nxt:
                exponent = sum(c == 1 for c in item[0]) - sum(c == -1 for c in item[0])
                bins.setdefault(exponent, []).append(item)
            chosen_keys = {w for w, _ in chosen}
            for offset in range(BEAM):
                for exponent in sorted(bins, key=lambda a: abs(a - 15)):
                    group = bins[exponent]
                    if offset < len(group) and group[offset][0] not in chosen_keys:
                        chosen.append(group[offset])
                        chosen_keys.add(group[offset][0])
                    if len(chosen) >= BEAM:
                        break
                if len(chosen) >= BEAM or offset >= max(map(len, bins.values())):
                    break
            frontier = chosen
        else:
            report["classification"] = "depth_cap"
    except TimeoutError:
        report["classification"] = "wall_cap_incomplete"
    except MemoryError:
        report["classification"] = "memory_cap_incomplete"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        report["seen"] = len(seen)
        report["elapsed_seconds"] = time.monotonic() - start_time
        if report["solution"] is not None:
            report["verified_solution"] = replay(text(START), report["solution"], text(TARGET))
            report["full_entry"] = BLOCK + report["solution"]
        (HERE / "bounded_entry_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["classification", "elapsed_seconds", "seen", "generated", "solution"]}))

if __name__ == "__main__":
    run()
