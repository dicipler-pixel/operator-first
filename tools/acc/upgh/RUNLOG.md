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

**Fable 5.1 and the lead role (30 September, 17:40–20:50Z)**
- The owner asked why Fable 5.1 was not in the harness. The advisor had run only once: lanes are code-only, and heat imported with `negative` never opened advisor tasks. New `upgh advise` queues advisor tasks for spent rows; `construction` is an agent-builder method.
- Fable 5.1 ran: two advisors (ac-00975 raised-ceiling surgery, ac-00145 echo funnel: both scoped misses), the MS(n,YXXyx) chain generator (first paths on 12 rows; the Stable-beat idea failed: pre-strip is 2^(n+1)), the MS(n,XYxYYY) structure proof (template closes only for n=1,3), the y-run negative (flank orientation, 102/128 rows), the board-level zoom-out, and the overlooked-work audit.
- The owner approved making Fable the default advisor model (`.claude/agents/upgh-advisor.md`, `config.json roles.advisor`) at 20:50Z; the edit had been blocked earlier as self-modification without that approval.
- Lead tools: `comms.py` (message sweep), `scout.py` (low-k rows with roads, 0 API), 50 MB commit guard in `commit_state.sh`, harvest reads nested JSON and `route`/`line` keys.
- Sends 17:36–20:43Z: #2902, #2904, #2907, #2909, #2914 (ties; sac-03272 and sac-04086 from session 1's new-seed lane, sac-08862 from session 2's yx_mid).

**Splice rung (30 September, 22:30Z)**
- Astra's receipt audit (`research/acc/live/UPDATE_astra_to_upgh_20260930T2216Z_mathagent_release.md`) found all five of the day's independently verified improving attempts came from unions of saved roads (Kernel ac-00028 58->51, Kernel ac-00003 92->84, Bob ac-00003 53->49). None came from fresh bridges. The ladder had no rung that joins roads, so every code rung worked on one road or from scratch.
- New code method `splice` (`adapters/splice_rows.py` running `tools/acc/splice/splice.py`) is the second rung, after yx. For each row it pools our best path, every `path.best` the ledger recorded (and the AC part of `+[16,15]` Stable lines) and every team road for the row under `research/acc/**` and `ACC_*.txt`, keeping at most 40. It adds exact radius-3 shortcut edges between all pool states, runs Dijkstra, restarts acc_beam from waypoints, and splices again. It writes `ac` and `sac = ac + [16,15]`.
- The rung is deterministic for a given pool: it runs once per row, then the ladder moves on. `upgh wake` reopens the row when a new road arrives.
- Hand test on ac-04086: 91 team hits, 15 distinct roads (Kernel's joined roads, Bob's lineage, ours), 483 nodes, 50 s, best 35 (record 34). No cut; the pool's roads already share the best join. The tests were updated for the new ladder order.
- **Never-send rows are now code, not only prose (22:35Z).** ONBOARDING rule 3 (ac/sac 09839, 02257, 09311, 06403, 04718, 05378: the owner handles them) had no check in the harness or in `sair_api.py send`. The new splice rung picked sac-05378 (t00134) because nothing stopped it. Now `gates.never_rows` is a standing owner claim in `external_claims()`, so lanes, `open`, `advise` and the scout skip those rows. `plan` never lists them, and `send` drops them ("DROP never-send row"). t00134 was already running and is allowed to finish; its sac-05378 output can be harvested but can never be planned or sent. Test added (27 OK).

**SIGILL false misses (1 October, 01:20Z)**
- Astra found `rc: -4` rows in five UPG-H window artifacts (t00167, t00232, t00235, t00236, t00245; 10 rows; 0.0-0.2 s, empty passes). The kernel log shows
  `acc_capped ... trap invalid opcode`. The binaries were built with `-march=native` on 30 Sep, and the container has since run on another host CPU.
  `run_window.py` records the per-row rc and exits 0, so the harness logged those runs as misses and heated the rows.
- Fixes: binaries now build with portable flags (`CFLAGS = -O3 -march=x86-64-v2 -mtune=generic`), and the build stamp covers source + flags, so `doctor`
  flags a mismatch. A crash anywhere in a run (any `rc < 0` row in out.jsonl) closes the task as **blocked**, never a miss (new test, 28 OK).
  The five tasks are voided; binaries rebuilt with `upgh setup`.
