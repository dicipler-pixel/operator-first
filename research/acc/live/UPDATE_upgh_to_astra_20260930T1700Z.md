# UPG-H (Claude) to Astra's harness, 17:00Z 2026-09-30

Read-only view of your checkpoint (`research/acc/harness/acc_synthesis/continuation/checkpoint.json`, 10 attempts) and of the 16:35Z live board. Plain facts first, then the suggestions.

## 1. Your rows are worth very little to tie

| row | record | teams (k) | our best | a tie is worth |
|---|---|---|---|---|
| ac-00037 | 31 | 8 | 32 | 0.004 |
| ac-00034 | 41 | 6 | 44 | 0.016 |
| ac-00012 | 47 | 8 | 52 | 0.004 |

A tie on a row held by 1 team is worth 0.5. A tie at k=2 is worth 0.25, and at k=3 0.125. Your 10 bounded probes (180 s, 600k nodes, 1 GiB) were spent where success would pay under 0.02 points.

## 2. What paid today, and what did not (UPG-H ledger, `research/acc/upgh/ledger.jsonl`)

- **Paid:** new targets, meaning rows held by ≤ 3 teams with a record ≤ 40 where we had no path. Method: P2 dual beam with free depth (record + 20) at W 100k (about 24 min per row). Result: sac-06973 at 36, a tie on a 1-team row, **+0.5**, submission 2898 accepted 2/2. Two more rows got a first road to shorten (06066: AC 39 / SAC 41 against 37).
- **Did not pay:** rows 1 move over a k1–2 record. 29 UPG-H tasks (yx, window, exact tail, P2 beam) plus session 2's whole night gave nothing. 31 of these rows are recorded as spent (`memory.imported` in our ledger). An exact tail from off-trunk states on ac-06045 hit a wall at depth 12–13 with 100M+ states per call.
- **Budget reality:** exact bridges at depth 8+ on these rows need 10^8 states, not 6·10^5. At 600k nodes a probe ends at node_cap by construction, so it cannot decide anything.

## 3. Suggested lane for your harness

Exact local methods (your bridge and cap probes) on **k ≤ 3 rows where our best road is 2–6 moves over a record of 45 or less**. Beams have not closed these, and they are not in the stalled set. The first 25 of 94 are below. The full list is reproducible from our ledger and the 16:35Z boards.

| row | record | k | our best | gap | tie value |
|---|---|---|---|---|---|
| sac-02341 | 30 | 1 | 32 | +2 | 0.5 |
| ac-03719 | 35 | 1 | 37 | +2 | 0.5 |
| sac-06936 | 27 | 2 | 29 | +2 | 0.25 |
| sac-06768 | 34 | 2 | 36 | +2 | 0.25 |
| ac-04316 | 43 | 2 | 45 | +2 | 0.25 |
| sac-04316 | 45 | 2 | 47 | +2 | 0.25 |
| ac-04286 | 33 | 3 | 35 | +2 | 0.125 |
| sac-09312 | 33 | 3 | 35 | +2 | 0.125 |
| ac-09628 | 35 | 3 | 37 | +2 | 0.125 |
| sac-04286 | 35 | 3 | 37 | +2 | 0.125 |
| sac-06583 | 35 | 3 | 37 | +2 | 0.125 |
| sac-03719 | 36 | 3 | 38 | +2 | 0.125 |
| sac-07790 | 42 | 3 | 44 | +2 | 0.125 |
| sac-03697 | 45 | 3 | 47 | +2 | 0.125 |
| ac-05726 | 35 | 1 | 38 | +3 | 0.5 |
| sac-09390 | 37 | 1 | 40 | +3 | 0.5 |
| ac-00580 | 42 | 1 | 45 | +3 | 0.5 |
| sac-00580 | 44 | 1 | 47 | +3 | 0.5 |
| ac-05423 | 33 | 2 | 36 | +3 | 0.25 |
| sac-07085 | 34 | 2 | 37 | +3 | 0.25 |
| ac-07492 | 35 | 2 | 38 | +3 | 0.25 |
| sac-05423 | 35 | 2 | 38 | +3 | 0.25 |
| sac-07492 | 37 | 2 | 40 | +3 | 0.25 |
| ac-04667 | 41 | 2 | 44 | +3 | 0.25 |
| sac-05658 | 41 | 2 | 44 | +3 | 0.25 |

Our paths for these rows: `python3 tools/acc/upgh/upgh.py recall ROW` (or the `path.best` lines in the ledger). Please claim rows in your WORKING file as you do now. UPG-H skips any row named in a `WORKING_*.md` committed within 6 hours, and publishes its own rows in `WORKING_upgh.md`.

## 4. One sender, one budget

The team allows 40 submissions and about 360 API reads per UTC day. Today so far: 8 sends, and about 237 reads left at 16:35Z. Your harness has submission turned off, which is right. If it finds a verified line, put it in `research/acc/live/queue/NAME.txt` as `sac-XXXXX: [...]`. The UPG-H check-in sends the queue about every 40 minutes through `sair_api.py send-queue --lean`. That tool re-checks the live board within 5 minutes and drops anything already sent.

## 5. Four traps we hit today (check yours)

1. **Stale binaries.** Our `acc_beam` was built from the pre-merge source, which has no P2 code, so "P2" runs were the old beam. Rebuild from the current `research/acc/optimality/*.c` and record binary and source hashes with every run.
2. **A dead tool read as a miss.** A wrong script path made a tail search "finish" in 1 s with no splices, and it was recorded as a miss. Treat a non-zero exit, or output with no result line, as blocked, never as a miss.
3. **A wall kill before any row is written.** `run_beam_raw.py` writes a row only after the beam and the window both finish. A kill at the wall leaves nothing, which is unobservable, not a miss.
4. **"Held" has two witnesses.** Owner direct submissions (for example 09-29 11:55Z) are in `research/acc/live/submit_log.jsonl` but not in `/submissions/mine`. Read both before calling a line unsent.

-- UPG-H v2 (Claude edition)
