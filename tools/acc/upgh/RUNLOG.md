# UPG-H v2 run log

Short human notes on each working batch. The ledger (`research/acc/upgh/ledger.jsonl`) is the record; this file only points into it.

## 2026-09-30, first session (Claude)

**Setup and first real pass (14:00Z)**
- `setup`: pins ok at `a0fd6e6`, T9 SHA-256 verified.
- `harvest` on the stale checkout: 1,513 unique paths checked twice, 554 best rows, 0 invalid, 0 disagreements.
- `board`: live AC and SAC boards; full history of 152 submissions and 1,363 held rows.
- `plan`: 0 scoring lines.
- t00001 (code choice: sac-03272, ac-04086; k = 1, one move behind; beam W = 200000, seed 101): a miss on both rows, parked.

**The branch had moved on (14:09Z)**
- The container was cloned 1,498 commits behind: other sessions had worked on 27–30 September. Merged, keeping both histories. The `sair_api.py` pagination fix had been made independently on both sides; the team's version was kept.
- Re-harvest: 5,417 unique paths, 1,635 improved bests, 3 invalid, 0 disagreements. The invalid ones are fragments that a 09-28 junction-splice file labels as full routes.
- The harness now joins the team's process instead of running beside it:
  - It honours `WORKING_*.md` claims and publishes `WORKING_upgh.md`.
  - It feeds `research/acc/live/queue/`.
  - Its history pulls are incremental, and it imports boards the team tool already pulled.

**Sending (14:15Z)**
- The user asked for sends every 30–40 minutes. Auto mode blocked the harness from sending by itself, and sending was left out of the code on purpose. Scoring lines wait in the queue. A notification asked the user for a Bash permission rule on `python3 tools/acc/sair_api.py send-queue`.
- Queued so far: sac-08748, a tie at 37 with k = 7 (about 0.008 points).

**Bugs found on real data, fixed with tests**
- The verdict put `held` before `above`, hiding rows we lost.
- `recall` crashed on count-valued `rows`.
- **S2 slip:** t00004 reran seed 101 on ac-04086, an exact repeat of t00001. Seeds are now new for every row and twin, and auto-selection refuses exact repeats. t00002–t00004 were abandoned as interrupted, not as misses, when the lanes restarted on the fixed code.
- SAC paths are derived only from checked AC paths (P + `[16,15]`). 301 were recorded; none scores, so the team had already sent those.

**Targets and methods (14:25–14:35Z)**
- The user's rule is to go for rows held by 2–3 teams. Targets are k ≤ 3 rows that are 1–3 moves off the record, plus rows with **no path yet** and a record of 40 or less: 232 targets, 128 of them new k = 2 or 3 rows.
- Rival activity from a board diff (0 API calls): `research/acc/upgh/briefs/RIVAL_ACTIVITY_20260930T0711Z_to_1402Z.md`. Long rows are being shortened by 1–2 moves, and the AC tie campaign is ten times the SAC one.
- The strategy ladder is: window-shorten our best path once, then seeded beam, then the advisor.
- Three lanes are running with a 35-minute cycle. A self check-in is scheduled every 40 minutes.

**Two silent defects, caught by watching wall times (14:40–14:47Z)**
- *Dead lane read as a miss (the map's R rule).* The tail rung "finished" two rows in 1 s. The adapter's path was one directory too high, so `tail_replace.py` never ran. The harness recorded "no splices" as a miss. The earlier smoke test had "passed" for the same reason. Voided: t00018, t00022, t00025.
- *Wrong method label.* `acc_beam` was compiled at 13:43 from the pre-merge source, which has no P2 code, so "beam_p2" ran the old beam at W20k. Voided: t00023, t00026. The binaries were rebuilt, and P2 mode now prints (`p2: mode 2`, `dual`, `atlas: quota 16`).
- Changes:
  - Adapters exit non-zero on tool errors, and a non-zero exit becomes `blocked`, never a miss.
  - Each run records its binary and source hashes, and `doctor` fails on a stale binary.
  - `upgh void` withdraws a result by appending a correction; the original lines stay.
- The yx and window results stand: correct paths, realistic wall times (yx about 10 s per 2 rows, window about 20 min).

**Budget shape (15:10–15:35Z)**
- The real tail rung (t00029–31) hit the 600 s row limit on all six rows, starting from the costliest positions. `tail_replace.py` gained an opt-in `TAIL_ORDER=rev` (default unchanged), and the rung now searches the short end tails first (about 30–40 s per position).
- beam_p2 t00033–35 were killed at 900 s before `run_beam_raw.py` wrote any row. They were voided as unobservable. Timing shows the P2 beam itself takes about 2 min (ac-02528: AC 40, worse than our 35); the window pass afterwards is the slow part. beam_p2 now gets one row per task and a 40-min wall.
- Every new rung restarts the attempt count, so the lanes kept giving the hard near-record rows first turn. Code now alternates near-record rows with **new targets** (k ≤ 3, no path of ours yet), as the user asked.
