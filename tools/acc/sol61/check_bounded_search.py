"""Synthetic bounded-search correctness experiment; no competition rows."""
import collections
import datetime
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "official/competition/tools"))
from verifier import core

OUT = ROOT / "sol61"
GOAL = ((1,), (2,))
LETTERS = {1: "x", -1: "X", 2: "y", -2: "Y"}


def bfs(cap):
    distance = {GOAL: 0}
    queue = collections.deque([GOAL])
    while queue:
        state = queue.popleft()
        depth = distance[state]
        if depth == 4:
            continue
        for move in range(14):
            child = core.apply_move(state, move)
            if sum(map(len, child)) > cap or child in distance:
                continue
            distance[child] = depth + 1
            queue.append(child)
    return distance


def word(relator):
    return "".join(LETTERS[a] for a in relator) or "-"


bounded, global4 = bfs(10), bfs(30)
# Every state on any radius-four path has length <= 25: cap30 is global here.
# Select states with identical global and cap10 distances, avoiding a test
# expectation that would incorrectly reject a valid larger-ball-cap shortcut.
chosen = []
for depth, number in [(3, 2), (4, 3)]:
    candidates = [s for s, d in bounded.items() if d == depth and global4[s] == d]
    candidates.sort(key=lambda s: (-sum(map(len, s)), s))
    chosen.extend((s, depth) for s in candidates[:number])

results, raw = [], []
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
for index, (state, true_depth) in enumerate(chosen):
    source = OUT / f"synthetic_exact_{index}.txt"
    source.write_text(f"{word(state[0])} {word(state[1])} x y\n")
    for ball_cap in (8, 10, 14):
        for requested in (true_depth - 1, true_depth):
            tt_limit = 3 if ball_cap != 10 else 10000
            command = [str(OUT / "sol61_ida"), "--input", str(source),
                       "--depth", str(requested), "--cap", "10", "--ball", "2",
                       "--ball-cap", str(ball_cap), "--ball-states", "5000",
                       "--tt-states", str(tt_limit), "--seconds", "10"]
            process = subprocess.run(command, capture_output=True, text=True, timeout=15)
            raw.append("COMMAND " + " ".join(command) + "\n" + process.stdout + process.stderr)
            found = re.search(r"^MOVES (\[[^\n]+\])", process.stdout, re.MULTILINE)
            result = {"state": [list(r) for r in state], "true_depth": true_depth,
                      "requested_depth": requested, "cap": 10, "ball_cap": ball_cap,
                      "tt_limit": tt_limit, "exit_code": process.returncode,
                      "command": command}
            if requested < true_depth:
                assert process.returncode == 2 and not found, process.stdout
                assert "STOP status=complete_no_path" in process.stdout, process.stdout
                assert "status=incomplete" not in process.stdout, process.stdout
                result["outcome"] = "complete_no_path_agrees_with_exact_BFS"
            else:
                assert process.returncode == 0 and found, process.stdout
                moves = json.loads(found.group(1))
                assert len(moves) == true_depth, (moves, true_depth)
                replay, peak = state, sum(map(len, state))
                for move in moves:
                    replay = core.apply_move(replay, move)
                    peak = max(peak, sum(map(len, replay)))
                assert replay == GOAL, replay
                result.update(outcome="exact_depth_route_core_replayed", moves=moves, peak=peak)
            results.append(result)

summary = {"started_utc": started, "completed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "status": "complete", "competition_rows_used": False,
           "ground_truth": "official core bounded BFS radius4; cap10 and globally complete cap30",
           "bounded_BFS_states": len(bounded), "global_radius4_states": len(global4),
           "selected_states": len(chosen), "cases": len(results), "passed": len(results),
           "results": results}
(OUT / "synthetic_exact_raw.txt").write_text("\n".join(raw))
(OUT / "synthetic_exact_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "results"}, indent=2))
