# Charlie handoff at the ACC stop checkpoint — 2026-09-28 15:25 UTC

Source: user-supplied `charlie_acc_v1.zip`, SHA-256 `31ba2e4f7ad1010989f60f0161bcac618017f1954c1f9315931da5addb5cb760`. The ZIP was integrity-tested. Its text code, ledgers, logs, route memory, and original candidate lines are archived in this private branch. Seven Python files were adjusted only to use `SAIR_TOOLS`/repository-relative paths and the existing `ledger/exact_capped_runs.jsonl`; Charlie's C++ search engine is byte-for-byte unchanged (SHA-256 `80bf76166569489ea1eb1cdf2d20efe5868299843cb45760ba423ace56c4c8bc`). No large search was resumed at this stop checkpoint.

## What Charlie built and found

`tools/acc/charlie/acc_disk.cpp` stores exact ordered AC BFS layers on disk as sorted 128-bit keys under a total relator-length cap. Because the 14-move capped graph is undirected, it subtracts the current and immediately preceding layers when constructing the next frontier. The two-sided version meets a precomputed trivial ball. His supplied `charlie_exact_disk_runs.jsonl` records 28 rows/runs: cap-limited negative results, ten runs stopped for disk space, a 37-move ac-03719 path, and a 35-move ac-02528 path (533,115,233 forward states reported for the latter). These were a tie and a beat **against the older records in Charlie's input ledger**. The deep frontier files are absent from the handoff, so the large negative searches and the 533M-state count are reported from his logs, not independently reenumbered here. They certify only the stated cap and move bound when their runs are complete, never unrestricted AC shortestness.

His rotate-and-cut presolve exposes whole cyclic blocks of the shorter relator inside the longer one. `cutchain_lines_ac.txt` and `cutchain_lines_sac.txt` preserve 270 paths on each board as reusable path memory. The greedy chain often trails the record; keep it as a source of routes for joins/splices, not a shortest-path claim. `cores_groups.json` groups 6,855 cut cores for further cross-row work.

## Independent checks here

- All four candidate paths replayed under pinned SAIR `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e` with the appropriate `core` or `stable_core` verifier. All **540** chain paths also replayed: 270/270 AC and 270/270 Stable AC accepted, with no duplicate row in either file. The exact SHA and accepted certificate results are in `ledger/charlie_verifier_recheck_20260928.json`.
- The C++ source compiled locally. Its 14 moves matched the official AC core on **1,428** local applications; the ported supplied `xcheck_moves.py` matched **56,056/56,056**. Its closed identity cap-10 component had **169,992** states with the same complete layer histogram as our independent reverse BFS, and ac-00738 cap 21 closed at **189,944** states. These controls are recorded in `ledger/charlie_disk_local_controls_20260928.json`.
- The supplied code uses unchecked low-level file writes in the large disk search. For a publication-level negative certificate, keep the frontier files or an independently checked hash/count and add explicit I/O error handling before relying solely on a `CLOSED` or `MAXLAYER` log. Positive paths have independent official verifier acceptance regardless of that issue.

## Sender routing against saved board 15:13 UTC

| Path | Moves | Snapshot record / teams | Status at snapshot |
| --- | ---: | ---: | --- |
| ac-02528 | 35 | 35 / 8 | Tie; not present in our `SENT_ROWS.txt` at this checkpoint |
| sac-02528 | 37 | 36 / 1 | Behind by 1 |
| ac-03719 | 37 | 35 / 1 | Behind by 2 |
| sac-03719 | 39 | 36 / 2 | Behind by 3 |

Only the ac-02528 tie is placed in `inbox/charlie_ac-02528_tie35.txt` for the sender's live recheck and batching. The four unmodified original candidate files are preserved under `charlie/source_inbox/`; three are **not** active submission candidates. Against the same board snapshot, the 540 chain lines consist of 56 ties and 484 behind-record lines; all 56 ties already appear at equal or better lengths in `SENT_ROWS.txt` (blob `798d6b57404b1f019d6b9ab31beba34272dc4121`). There are no fresh chain submissions.

## Resume instructions

Build `tools/acc/charlie/acc_disk.cpp`, set `SAIR_TOOLS` to the pinned clone's `competition/tools`, and run `tools/acc/charlie/xcheck_moves.py` first. `ledger_run.py` reads `research/acc/live/ledger/exact_capped_runs.jsonl` by default; set `CHARLIE_BOARD` to override it. Two-sided runs additionally require the radius-9 trivial ball in `tools/acc/charlie/runs/B36/` (`union9.bin` and individual layers), which is **not** included in the ZIP. The complete T16 component is also absent; the 540 accepted chain paths are preserved so they can be spliced without rebuilding it. The source `README_charlie.md` describes the engine and prior controls; use this checkpoint for the current candidate status.
