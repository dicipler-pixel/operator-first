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
