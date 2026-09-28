Adam, Bob, Charlie: here's the plan for the SAIR ACC challenge.

WHERE EVERYTHING IS
Repo dicipler-pixel/operator-first, branch claude/gallant-bardeen-0pgpae. Always pull first.
- Setup and search gear: tools/acc/HANDOFF_SAIR_ACC.md. It covers the SAIR verifier clone and the T9 table
  build (4.5 GB, needs about 6 GB RAM). The main tools are acc_beam (beam search), acc_capped (exact search
  under a length cap), acc_window (exact shortening of short windows), crossrow.py (borrows known roads from
  other rows and their mirror images) and plan_offline.py (runs the official verifier and labels each line
  TIE / BEAT / UNSOLVED against the live board).
- What works and what doesn't: tools/acc/METHODS_PLAYBOOK.md
- Where we work: research/acc/live/
    WORKING_*.md   rows someone is already running. Add yours before you start.
    ledger/        every finished search, including the failed ones, with its cap and scope. Read it so you don't redo a dead end.
    IDEAS.md       add one idea per turn with what you tested and the result. Read the latest entry first.
    inbox/         put verified hits here, one file per hit, lines like "ac-01234: [..]".

RULES
- Nobody submits to SAIR except the sender session. You find, verify, and drop lines in the inbox.
- Only hand over a line the official verifier accepted.
- Save raw output and exact settings, and mark each run complete or incomplete.

JOBS
Adam: unsolved rows (a full point each). Take research/acc/live/targets_codex_oddeasyB.json
  (213 rows) with acc_beam through research/acc/optimality/run_beam.py, BEAM_H=1, then again with BEAM_BAL=1.
  Stop after 100 rows with no solution.
Bob: near misses and your eyes. Borrowed roads came within 1-2 moves of the record on ac-00766 (34 vs 33)
  and ac-00974 (26 vs 24); the paths are in ledger/crossrow_r2_20260928.json. Look for the shortcut near where
  the borrowed road joins, then test your move-rhythm idea on the 424 SAIR training solutions against a
  shuffled baseline.
Charlie: the memory wall. 52 of our 76 exact capped runs stopped at about 210M states before finishing
  (ledger/exact_capped_runs.jsonl). A disk-backed or two-sided version of acc_capped that can finish them
  is the big unlock. Rank-3 Stable AC on long rows is also untested. Short rows turned out to be the
  (y,x) swap finish (see IDEAS.md).
