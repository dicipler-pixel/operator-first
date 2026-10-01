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
