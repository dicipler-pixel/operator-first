# SAIR ACC: handoff for a new Claude session (written 2026-09-27)

Read this first. It records what the earlier session knew, so a new session can continue
without its chat history. Branch: `claude/gallant-bardeen-0pgpae`.

## SUBMISSION RULE (agreed with the user, 2026-09-27): no exceptions
Before **every** submission:
1. Pull the live boards (`sair_api.py boards`) and our history (`sair_api.py mine`) fresh, right then.
   Never reuse an older pull.
2. For each line, read the live record (`currentBestLength`) and the team count (`kTeams`) for its
   exact row number.
3. Keep a line only if it is UNSOLVED, a BEAT, or a TIE, and we haven't already sent that length
   or shorter. Drop everything else.
4. Every kept line must have passed the official verifier (this session can run it, and
   `tools/acc/plan_offline.py` does all of steps 2–4 offline).
5. The user's rule (2026-09-27 22:4xZ): **ties, beats and unsolved rows may be sent without
   asking first**, but the live check must be **at most 5 minutes old** when the POST goes out.
   Report the row, length, live record and k after sending.
   **Batches (user rule, 2026-09-28):** queue verified lines in `research/acc/live/queue/`, then
   send with `sair_api.py send-queue --yes` once 3 or more lines wait. A line worth ≥ 0.25 waits
   at most 30 minutes (`--force`).
6. The session with SAIR network access sends. The search session produces and verifies lines.

**Tool:** `python3 tools/acc/sair_api.py send FILE... --yes` does steps 1–3 and 5 in one go. It
pulls fresh, prints the table, keeps only UNSOLVED, BEAT or TIE lines that haven't been sent, and
refuses to POST if the pull is more than 300 s old. `submit --yes` alone is refused on purpose.
Without `--yes`, it's a dry run.

**Sent log:** `research/acc/live/submit_log.jsonl`.
- Submission 2558 (22:45Z): NEW15, 6 ties, all accepted.
- Submission 2565 (23:29Z): SACPLUS2, 6 Stable AC ties (our accepted AC paths + `[16,15]`), all
  accepted. It already covers all 4 rows of NEW16 (sac-09757, 06754, 00276, 08702). **Don't
  resend NEW16.**

- Submission 2566 (23:36Z): ac-03305 23 (tie, k6) and **sac-03305 24 (tie on a row held by one
  team, about +0.5)**, found by the adaptive exact capped sweep at caps 37 and 40.

- Submission 2569 (23:50Z): ac-01629 23 (tie, k4→5) and sac-01629 25 (tie, k3→4, AC + `[16,15]`),
  about +0.19. From exact sweep C.

- Submission 2572 (23:56Z): ac-05558 24 and sac-05558 26 (ties, k5→6 each, about +0.06), from sweep C.

- Submission 2581 (01:24Z, first batch under the batching rule): ac/sac-07435 (26/28, k6→7) and
  ac/sac-08201 (31/33, k5→6), 4/4 accepted, about +0.09. From sweep C.
- Submission 2606 (04:23Z, batch): 13 Stable AC ties from session 1's mirrored roads (crossrow, (y,x)
  finish) plus ac/sac-03028 (26/28), 15/15 accepted, about +0.02 (best: sac-02902 k6, sac-04278 and
  sac-00974 k8; the rest sit on rows with 12–20 teams).
- Board watcher: `changes` every 30 min into `research/acc/live/changes/`. It alerts on
  "LOST OUR TIE" or a newly solved row.

**Verifier permission:** at 23:29Z the user told the API session to run the official verifier
("run the verifier"). That session can now verify and send by itself.

## Key docs (2026-09-27)
- `tools/acc/METHODS_PLAYBOOK.md`: what works and what doesn't, with evidence. Read it before
  picking a method, and add to it after every win or clear failure.
- `tools/acc/HELP_WANTED.md`: the brief for the user's helper AIs (our struggles and the asks).
- `tools/acc/proof_track/WIN_TEMPLATE.md`: **every 1-point result** (a beat, or a row we hold
  alone) gets a write-up on how we got it, with commit hashes (user rule).
- `tools/acc/targets_easy_lowk_20260927.json`: 66 rows held by 1–2 teams with records of 36 or less.
- `tools/acc/targets_mid_25to40_k2to6_20260927.json`: 496 rows (records 25–40, 1–6 teams, AC and
  Stable AC), sorted by tie value. Sweeps B and C run the exact capped search on them.
- **Tracker page:** https://claude.ai/artifact/PesMNAWMhazVqhNx5DpP5u (private to the user, charts and
  tables). To update it:
  1. Run `python3 tools/acc/dashboard_data.py`. It uses no API reads and writes
     `research/acc/live/dashboard.json`.
  2. Write each top-level key to the page's database: ArtifactData `batch`, `set dash/<key>`.
  3. Change the page layout only in `tools/acc/dashboard/acc_tracker_template.html`. Build it with
     `--page OUT` and republish with the Artifact tool using `url`.

## Goal
Get Mad Hatters points in the SAIR Andrews–Curtis Challenge (Discovery track, AC and Stable AC).
- Beat a live record: 1.0 point. Tie it: 2^(1-k), where k is the number of teams on it.
- Only compare against **live** records. The 09-14 snapshot records are stale: other teams have
  beaten most of them since.
- Deliver clean lines `ac-XXXXX: [...]` and `sac-XXXXX: [...]`. Every line must pass the official
  checker first. When the user asks for "new ones", give one file with only the new lines.
- The user wants plain, short language and short lists. The user also wants the searches kept running.

## Live board
- Needs network access to `api.sair.foundation` and the key in env var `SAIR_API_KEY`.
- See `tools/acc/SAIR_API_NOTES.md`. It needs a browser User-Agent, or Cloudflare returns error 1010.
```
curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36" \
  -H "Authorization: Bearer $SAIR_API_KEY" -H "Accept: application/json" \
  "https://api.sair.foundation/api/public/v1/competitions/acc/discoveries/snapshot?problem=ac" -o live_ac.json
```
- Repeat with `problem=stable_ac`.
- The last manual check of our rows, from 2026-09-27 19:20Z, is in
  `research/acc/optimality/runs/2026-09-27/live_board_our_rows_20260927T1920Z.txt`.
  Its columns are id, live record and k.

## API client: `tools/acc/sair_api.py` (added 2026-09-27, second session)
Standard library only. Reads the key from `SAIR_API_KEY` and never prints it.
- `check`: tests the network, the key and the team status, and reports the results in plain words. Run it first.
- `boards`: pulls both live boards into `research/acc/live/boards/` as gzipped JSON.
- `mine`: shows our submission history and our best length per row.
- `plan FILE... --sair $S/sair`: runs the official verifier on each line, then compares it with the
  live board and our history. It writes `ACC_SUBMIT_API_<time>.txt` with only the lines that
  score, best first.
- `submit FILE`: a dry run. `submit FILE --yes` sends the file with one POST, which is never
  retried, then waits and logs to `research/acc/live/submit_log.jsonl`.
- `status ID`: waits for one submission to finish.

**Before it can work, the user must:**
1. Add `api.sair.foundation` to the environment's allowed domains. Without it, the proxy returns
   `CONNECT tunnel failed, response 403`.
2. Add the key as an environment **API credential**: allowed website `api.sair.foundation`, header
   `Authorization`, prefix `Bearer`, value = the key. The proxy adds the header, so the key never
   enters the container. A `SAIR_API_KEY` environment variable also works as a fallback.

Both take effect in a new session.

The user wants Claude to lead submissions through the API. Show the `plan` output to the user
before the first `--yes`.

**Permission note:** in session 2, the auto-mode classifier blocked running the official SAIR
verifier because it is external code cloned from GitHub. `run_beam.py`, `splice.py` and the other
tools import it. The user must allow it, for example with a Bash permission rule for
`python3 -m verifier`. Until then, use `research/acc/optimality/run_beam_raw.py`. It is the same
search with no verifier import, and it saves unchecked paths (`"checked": false`).

## Setup (about 10 minutes)
```
S=<scratchpad>; mkdir -p $S/work
git clone https://github.com/SAIRcompetition/Andrews-Curtis $S/sair && (cd $S/sair && git checkout a0fd6e6)
gcc -O3 -march=native -o $S/acc_beam research/acc/optimality/acc_beam.c -lm
gcc -O3 -march=native -o $S/acc_opt  research/acc/optimality/acc_opt.c -lm
bash tools/acc/build_T9.sh $S/work     # builds T9.tab: 4.48 GB, SHA-256 checked, takes a few minutes
```
- Official checker:
  `cd $S/sair && PYTHONPATH=competition/tools python3 -m verifier --manifest competition/tools/verifier/data/manifest.json --submission FILE`
- Old session scripts are in `research/acc/optimality/runs/2026-09-27/scripts/`. They hard-code
  the old scratch path. Fix that with:
  `sed -i "s#/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad#$S#g" *.sh`
- Their results (`results/*.jsonl`) and target lists (`targets/*.json`) are next to the scripts.
  Copy them into `$S/work` so the helper scripts can find them.

## Tools and what works
- **Moves:** official kernel ac-r2-v1, moves 0..13.
- **SAC finish:** AC path + `[16,15]`, or the swap path (6↔8, 7↔9, 10↔12, 11↔13) + `[15,15]`.
  Always keep the shorter of the searched SAC and AC+2. The script `emitcap.sh` does this.
- **Search engine:** `acc_beam`, beam search with the T9 table as the finish. Settings are
  environment variables:
  - `BEAM_H=1`: the ACSolverX priority (L + 2.53K + 6.418MK + 8.458S + 3.292·|#x−#y|/L). This
    produced most of our ties.
  - `BEAM_DIV`, `BEAM_NOV`, `BEAM_LOOK`.
  - `BEAM_SEED` + `BEAM_NOISE`: seeded restarts that explore different routes.
- **Runners:**
  - `run_beam.py`: loops over a targets JSON list `[{"id","record","k"}]`.
  - `run_live.sh NAME` / `run_live_seed.sh NAME` (with `SEED=`, `NOISE=`): run on
    `work/NAME_targets.json`.
- **Splicer:** `tools/acc/splice/splice.py`. It builds a pool of paths, adds radius-R shortcut
  edges, runs Dijkstra, and restarts from waypoints. `seedsplice.sh` seeds it with the best
  H-beam path.
- **Exact capped search:** `acc_capped.c`, driven by the `capgen*.sh` scripts. Give it caps
  **above** the start length.
- **Line emitter:** `emitH.sh NNNNN`, with the number only and **no `ac-` prefix**. Passing the
  prefix once made a bad commit.
- **Weak spots so far:**
  - k=2 rows with records of 44–70: 0 found out of 34.
  - SAC k=1 rows: 0 out of 17.
  - Unsolved rows: 0 out of 126.
  - Beat-by-one on the scoring rows: 0.

## Status at handoff
- Live-confirmed ties are in `ACC_SUBMIT_NEW14_20260927.txt`: ac-09391 (35), ac-01373 (30),
  ac-00313 (33), and sac-00313 (35, not yet checked against the SAC board).
- Do **not** send NEW11/12/13. Their lines are longer than the live records now.
- Still unchecked against the live SAC board: `ACC_SUBMIT_FIX_sac01734_20260927.txt` (38) and
  `ACC_SUBMIT_SACFILL_20260927.txt` (sac-07158, 41).
- **Next steps:**
  1. Pull both live boards.
  2. Build targets from rows where our best path is 1–3 moves over the live record, putting low
     k first. `targets/livenear_targets.json` is a start.
  3. Add k=1 rows with records of 25–60.
  4. Run the seeded H-beam and the splicer on them.
- Don't upload the T9 table to GitHub until the user says so. `tools/acc/make_T9_zip.sh` is ready.
- Never ask the user to paste keys or tokens into chat.
