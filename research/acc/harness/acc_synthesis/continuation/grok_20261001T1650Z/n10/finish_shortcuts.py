"""Exact two-primitive replacements of fixed finish-route windows."""
import json
import pathlib
import resource
import signal
import sys
import time

from replay import HERE, HARNESS, encode, text, replay, CORE_PIN
from verifier.core import apply_move

resource.setrlimit(resource.RLIMIT_AS, (192 * 1024 * 1024,) * 2)
START_TIME = time.monotonic()
NODES = 0
MAX_NODES = 100000

def alarm(signum, frame):
    raise TimeoutError()

def finish(m):
    return ([4, 1, 11, 3, 8, 8, 4] + [7] * (m - 1) + [12, 5, 12, 5]
            + [6] * (m - 2) + [8, 11, 4, 12, 2, 4, 4, 6, 3] + [5] * (m - 2))

def states(start, route):
    result = [start]
    for m in route:
        result.append(apply_move(result[-1], m))
    return result

def shorten(start, route):
    global NODES
    records = []
    while True:
        path = states(start, route)
        best = None
        for i in range(len(route) - 2):
            endpoints = {path[i]: []}
            for a in range(14):
                first = apply_move(path[i], a)
                NODES += 1
                endpoints.setdefault(first, [a])
                for b in range(14):
                    second = apply_move(first, b)
                    NODES += 1
                    if NODES > MAX_NODES:
                        raise OverflowError()
                    endpoints.setdefault(second, [a, b])
            for j in range(i + 3, min(len(route), i + 8) + 1):
                replacement = endpoints.get(path[j])
                if replacement is not None:
                    save = j - i - len(replacement)
                    if best is None or save > best[0]:
                        best = (save, i, j, replacement)
        if best is None:
            return route, records
        save, i, j, replacement = best
        records.append({"start_index": i, "old": route[i:j], "replacement": replacement, "saving": save})
        route = route[:i] + replacement + route[j:]

def main():
    report = {"official_core_sha256": CORE_PIN, "bounds": {
        "seconds": 10, "memory_bytes": 192 * 1024 * 1024, "generated_records": MAX_NODES,
        "old_window_lengths": [3, 8], "new_max_length": 2}, "cases": [], "classification": "running"}
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, 10)
    try:
        for m in [4, 8, 16]:
            start = (encode("YY" + "x" * m + "yyyX"), encode("xxYYXyy"))
            original = finish(m)
            route, replacements = shorten(start, original)
            verified = replay(text(start), route, ["x", "y"])
            report["cases"].append({"m": m, "original": original, "original_length": len(original),
                                    "final_length": len(route), "replacements": replacements,
                                    "verified": verified})
        report["classification"] = "completed_local_scope"
    except TimeoutError:
        report["classification"] = "wall_cap_incomplete"
    except OverflowError:
        report["classification"] = "record_cap_incomplete"
    except MemoryError:
        report["classification"] = "memory_cap_incomplete"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        report["generated_records"] = NODES
        report["elapsed_seconds"] = time.monotonic() - START_TIME
        (HERE / "finish_shortcuts_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"classification": report["classification"], "generated_records": NODES,
                      "elapsed_seconds": report["elapsed_seconds"],
                      "lengths": [(r["m"], r["original_length"], r["final_length"]) for r in report["cases"]]}))

if __name__ == "__main__":
    main()
