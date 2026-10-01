# t00289 — Sol 6.1 `sol61_ida` exact solver run (builder: Fable 5.1 for the team; solver credit: Sol 6.1)

Contract: `research/acc/upgh/tasks/t00289.json`. Rows (in Sol's order): ac-09409 (control), ac-05343, ac-09400, ac-00764.

## Prediction (written before any run)

- Control ac-09409 (record 23, total start length 23): with cap 36, radius-8 goal ball capped at 4M states, 2M transpositions and 600 s,
  I expect the goal ball to stop short of radius 8 at the 4M-state limit (branching ~13 per layer), so the forward IDA must cover
  most of the 23 moves itself. The mod-p / SL(2,p) pattern databases are admissible but weak at depth ~17-20; I predict roughly
  even odds that a 23-move path is found inside 600 s. If found and accepted by the pinned verifier, the control passes and target
  runs proceed. If the 600 s budget expires, the control is incomplete (not a negative) and Sol's rule stops the target runs.
- Targets (if reached), ~600 s each at caps 36-38: I predict the null outcome of the contract (no row gets a path <= its live record),
  because the forward depth needed (32, 35, and an unknown length for ac-00764) is far beyond what a bounded IDA with these
  heuristics usually completes; any stopped iteration is a scoped miss, never a negative. A hit on ac-05343 (<= 32) or ac-09400
  (<= 35) would be a tie/beat; any verified path at all on ac-00764 would be a first solve.

## Source review verdict

`tools/acc/sol61/sol61_ida.cpp` (sha256 1d0aebf87bf133bf6f2a8006c6dd81652a7d3ebd07d8dd1e65ff87fd5307d3ce): standard headers only
(algorithm, array, chrono, cstdint, cstdlib, fstream, iostream, limits, queue, sstream, stdexcept, string, unordered_map, vector).
The only file access is `std::ifstream` on the `--input` path (read only); all output goes to stdout/stderr. No `system`, `popen`,
`fork`, `exec`, sockets, `getenv`, or any file writes. Pure compute. Verdict: safe to build and run.

`tools/acc/sol61/run_control.py`: no network; spawns only the solver binary via `subprocess.run`; reads the manifest; writes only
under `--output-dir/<UTC stamp>/`; refuses a manifest whose Git blob is not accdb626ee08a06beea3f88dc7f351514c99eb27; writes a
lines file only after `core.verify` accepts the candidate. Run unmodified from a scratch layout (see below).

## Build

Command (run from repo root): `g++ -O3 -std=c++20 -march=x86-64-v2 tools/acc/sol61/sol61_ida.cpp -o ~/.cache/upgh/work/t00289/sol61_ida`
Compiler: g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0. Binary sha256 bff7dcac244d6a617c9ac48efab35a9b7d41f71e65a5d5dc6f8feda0f5f891d7.
No prebuilt binary was used (none is in the repo package).

## Manifest / verifier

Manifest: `~/.cache/upgh/sair/competition/tools/verifier/data/manifest.json`, 12,378,899 bytes, `git hash-object` =
accdb626ee08a06beea3f88dc7f351514c99eb27 (matches Sol's pin). Verifier: `~/.cache/upgh/sair/competition/tools/verifier` (pinned
copy at a0fd6e6), `core.verify(challenge, moves, 'ac-r2-v1', manifest['limits'])`.

Scratch layout for the unmodified `run_control.py` (ROOT = `~/.cache/upgh/work/t00289`): `official` -> symlink to
`~/.cache/upgh/sair`; `sol61/run_control.py` = byte-identical copy; `sol61/sol61_ida` -> symlink to the binary built above.

## Control ac-09409 (board record 23, k12) — attempt 1, Sol's prepared settings: NOT PASSED (incomplete, time)

Run dir: `research/acc/upgh/artifacts/t00289/control/20261001T024922Z/` (settings.json, control_words.txt, stdout.txt, stderr.txt (empty),
receipt.json, SOL61_control_*.txt). Wrapper: unmodified `run_control.py` (exit 2); its stdout/stderr in `control/run_control_std*.txt`.
Command: `sol61_ida --input control_words.txt --depth 23 --cap 36 --ball 8 --ball-cap 36 --ball-states 4000000 --tt-states 2000000 --seconds 600`.
Input words (from the manifest by challenge_id, no known route as input): `YYXXX YYXXXYxxyxyxxyXXyx x y`.
Single process; it got ~59% of one core (box shared with another builder). Peak RSS observed ~0.7 GB; memory never required adjusting.

Result: receipt `control_passed: false`, `search_status: incomplete`, no MOVES line, nothing verified, no lines file written.
- Goal ball (cap 36): layers 1..7 complete with 11 / 88 / 662 / 5115 / 40779 / 336469 / 2835153 states; layer 8 hit the 4M cap -> incomplete; ball_complete=7.
  Layer growth ~8x, so a complete radius-8 ball at cap 36 needs ~24M states (~4 GB at the observed ~150 B/state).
- Pattern databases: mod-p exponent p=7/11/31 (672 / 2640 / 59520 states), SL(2,5) x2 (14396), SL(2,7) x2 (112892).
- IDA iterations (each = forward DFS to rem=7 then ball lookup, absence pruning active since ball-cap >= cap):
  depth 7..13 complete_no_path (1 / 13 / 146 / 1204 / 8443 / 50146 / 253406 nodes); depth 14: 1,087,367; depth 15: 4,037,351 (13 s);
  depth 16: 13,475,456 (50 s); depth 17: 105,482,330 (303 s) complete_no_path; depth 18: 104,717,993 nodes when the 600 s budget expired
  -> `search depth=18 ... status=incomplete`, `STOP status=incomplete nodes=229113856 tt_clears=12`.
- Scope of the completed part: no path of length <= 17 whose relator-total peak stays <= 36 (fully completed iterations only). Depth 18 and
  above: no claim. This is a scoped miss of the control, never a negative about the 23-move record.

Why it failed (brief diagnosis): the forward depth required is 23 - 7 = 16, and the per-iteration node count grows 3.3x-7.8x per depth
(accelerating: 4.0x, 3.7x, 3.3x, 7.8x for depths 14->17). At the observed ~270-350K nodes/s on a shared core, completing depth 18 alone
projects to ~30-60 min, and the depth-22/23 iterations project to >= 10^10 nodes, i.e. hours to days — not reachable in the 600 s budget
nor in this task's 3600 s wall. A complete radius-8 ball (~24M states) would save only one forward level (~4-8x).
Disclosure for diagnosis only: the known 23-move route in the contract context peaks at relator total 31 (per core replay), so Sol's cap 36
does admit it; the obstacle is depth, not cap. The known route was never given to the solver.

Per Sol's rule, the target runs stay stopped unless a control attempt passes. One short diagnostic second attempt follows (tighter cap 32,
which still admits a peak-31 route; cap choice informed by that disclosed peak; larger ball allowance), labeled as diagnostic.

## Control ac-09409 — attempt 2 (diagnostic, tighter cap): NOT PASSED (incomplete, time)

Run dir: `research/acc/upgh/artifacts/t00289/control2/20261001T025948Z/` (same file set; wrapper stdout/stderr in `control2/run_control_std*.txt`).
Command: `sol61_ida --input control_words.txt --depth 23 --cap 32 --ball 8 --ball-cap 32 --ball-states 12000000 --tt-states 2000000 --seconds 420`
(unmodified `run_control.py --cap 32 --ball 8 --ball-states 12000000 --tt-states 2000000 --seconds 420`; exit 2). Single process, ~94% of one core
this time, RSS ~1.6 GB. Cap 32 was chosen knowing the known route peaks at 31 (disclosed above); the solver still received only the manifest words.

Result: receipt `control_passed: false`, `search_status: incomplete`, no MOVES line, nothing verified, no lines file written.
- Goal ball (cap 32): layers 1..7 complete (11 / 88 / 662 / 5115 / 40779 / 336269 / 2806867); layer 8 hit the 12M cap -> incomplete; ball_complete=7.
  (At cap 32 the radius-7 ball is barely smaller than at cap 36, so radius 8 still needs >12M, probably ~20M+ states.)
- IDA iterations: depth 7..16 complete_no_path (1 / 13 / 144 / 1106 / 6675 / 31476 / 121249 / 406141 / 1259189 / 3775882 nodes);
  depth 17: 11,089,444 (22 s); depth 18: 62,295,412 (128 s) complete_no_path; depth 19: 109,937,172 nodes when the 420 s budget expired
  -> `search depth=19 ... status=incomplete`, `STOP status=incomplete nodes=188923904 tt_clears=9`.
- Scope of the completed part: no path of length <= 18 whose relator-total peak stays <= 32. Depth 19 and above: no claim.
- Growth per depth at cap 32: 3.1x, 3.0x, 2.9x, 5.6x (depths 15->18) and still >= 1.8x partway into 19; four more levels (20..23) at >= 5x
  each project to >= 10^10 nodes for the final iterations — hours or more, not reachable within this task's wall.

## Control verdict and consequence

Both attempts ended as `incomplete` (time), never `complete_no_path` at depth 23. No 23-move path was found, so by Sol's rule the control
did NOT pass. Nothing was verified; no path lines exist. `lines.txt` is intentionally empty (verified paths only; there are none).

Target runs: NOT STARTED, per Sol's rule "no target search may begin before the specified control passes". Planned (and not run):
ac-09400 (cap 36-38, depth 35) and ac-00764 (cap 32-36). ac-05343 was removed from this task by the lead at ~03:05Z (Sol 6.1 runs it on its
own machine). A faithful generalization of run_control.py for those rows was prepared at `~/.cache/upgh/work/t00289/sol61/run_target.py`
(copy saved here as `run_target_UNUSED.py`); it was never executed. 0 target rows searched, 0 SAIR calls, 0 submissions.

What would make this worth repeating: a machine where sol61_ida can hold a complete radius-8 or radius-9 goal ball (>= 24M / ~200M states at
cap 36) and run a single iteration for hours, or a solver revision with a much stronger admissible bound; or a shorter-record control row.
No claim is made about any row's record or about the absence of any route beyond the fully completed depths and caps listed above.

Wall: builder started ~02:46Z; attempt 1 02:49:22Z-02:59:33Z; attempt 2 02:59:48Z-03:06:54Z; finalization 03:07Z-03:09Z. Max 1 solver
process at any time (limit was 2). Heartbeats sent at 02:49Z and 02:59Z.
