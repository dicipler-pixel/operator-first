# Orders for Codex (helper), 2026-09-28

You are a searcher, not a sender. Only session 2 sends to SAIR.
Your machine has 8 GiB, so you get jobs that fit in 8 GiB and don't overlap sessions 1 and 2.

## 0. Every cycle, before any compute (5 minutes)
1. `git pull --no-rebase origin claude/gallant-bardeen-0pgpae`
2. Read `ORDERS.md`, `WORKING_session1.md`, `WORKING_session2.md`, `SENT_ROWS.txt` in this folder.
   Skip any row listed there unless this file gives it to you.
3. Add the rows you are about to run to `research/acc/live/WORKING_codex.md` (make it), then push.
   This is how we avoid three machines running the same row.

## 1. Setup (once)
```
git clone https://github.com/SAIRcompetition/Andrews-Curtis SAIR && (cd SAIR && git checkout a0fd6e6)
bash tools/acc/build_T9.sh work          # 4.5 GB table, checks its SHA-256
gcc -O3 -march=native -o work/acc_beam   research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o work/acc_window research/acc/optimality/acc_window.c
```
The table takes 4.5 GB of your 8. Run **one** beam at a time, width 100000 at most.

## 2. Lane A (main job): the unsolved rows, half B
Every unsolved row we solve is worth a full 1.0 point, the same as a beat.
File: `research/acc/live/targets_codex_oddeasyB.json` (213 rows).
These are unsolved rows whose words have no single-letter run longer than 3.
Our data says those are the "easy-looking" unsolved rows: only 6-11% of rows like this stay unsolved.
Session 1 runs the other half (A). Don't touch half A.

How:
```
cd research/acc/optimality   # SAIR, work = full paths to your clone and table folder
BEAM_H=1 BEAM_DIV=1.0 BEAM_BAL=0 python3 run_beam.py SAIR work work/T9.tab work/wB 100000 600 \
    work/beam_oddeasyB_bal0.jsonl ../../acc/live/targets_codex_oddeasyB.json
```
- `record: 2000` in the file is on purpose. It lets the beam go deep.
- When bal0 finishes, run it again with `BEAM_BAL=1` into `beam_oddeasyB_bal1.jsonl`.
  BAL=1 penalizes the two words for having very different lengths. It found different paths on some rows.
- Stop the lane (kill condition): 100 rows with zero solutions at both BAL values. Report and move to lane B.

## 3. Lane B: your mountain-pass RETURN/ADVANCE idea
Your Atlas result (680 exits collapsing to 23 components) is worth a real test. Fit it in 8 GiB like this:
1. Pick 3 rows with AC record 22-30 and kTeams 1-3 that are **not** in any WORKING file.
   (Short records keep the basin small.)
2. Build the exact basin up to a small length cap (start length + 4) and store it on disk, not in RAM.
3. Label each exit RETURN (its component comes back to the start basin) or ADVANCE (it doesn't).
4. From each ADVANCE exit, run a beam with depth (record - moves used) and see if it reaches (x,y).
5. Also look up the ADVANCE states in the solved-path index: `tools/acc/crossrow.py` builds that
   index from any path file (`--radius 1` is quick). Paths to feed it: all `ac-NNNNN: [...]` lines in
   `research/acc/live/queue/*` and `inbox/sent/*`.
- Kill condition: on all 3 rows, ADVANCE exits don't reach the goal in fewer total moves than the
  same beam run from plain random exits. If ADVANCE doesn't beat random, the gate isn't helping. Write that down and stop.

## 4. Lane C (only if A and B stop): real rank-3 Stable AC
Untested by anyone here. Take 5 rows from the bottom of session 1's SAC-gap list (last 20 lines
of the list in `WORKING_session1.md`) where the SAC record is at least AC record + 3.
Use the official 257-move Stable AC table from the SAIR verifier (`stable_core`), with a beam.
- Kill condition: no rank-3 path shorter than the rank-2 path (AC path + [16,15]) on all 5 rows.

## 5. When you get a hit
1. Verify with the official CLI. Easiest: `python3 tools/acc/plan_offline.py HITS.txt --sair SAIR --out plan.txt`.
   It runs the official verifier and marks each line TIE / BEAT / UNSOLVED / REJECTED against the newest board in `boards/`.
   Never hand over a line the CLI didn't accept.
2. Write one file per hit: `research/acc/live/inbox/<UTC time>_<rows>.txt`, containing only lines like
   `ac-01234: [ ... ]` and `sac-01234: [ ... ]`. Commit and push.
3. For every AC line, also add the SAC line: AC path + `[16, 15]`.
4. Don't send to SAIR. Session 2 pulls fresh boards, checks the record and team count, then sends.

## 6. What to report each cycle (short)
- Rows done / rows with a path / rows in the inbox.
- For exact runs: cap, state count, and NO_SHORTER_UNDER_CAP / INCOMPLETE / NO_SIGNAL.
- `ps` output showing what is still running. "Nothing is running" is a problem. Start the next lane.

## Rules
- Kill processes by PID only.
- No new ACC_SUBMIT_* files. Use the inbox.
- Keep the T9 table off GitHub.
