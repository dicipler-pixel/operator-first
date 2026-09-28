# ACC methods playbook: what works, what doesn't, quick recipes

Mad Hatters, SAIR Andrews–Curtis Challenge. Keep this file current: every method that wins (or
clearly fails) gets a line here with its evidence. Newest facts first inside each section.

## Beam flag dependency (checked 2026-09-28)
`BEAM_BAL` changes only `hprio()`, and `acc_beam.c` calls `hprio()` only when `BEAM_H=1`. Set both `BEAM_H=1 BEAM_BAL=1` for a balanced heuristic pass. `BEAM_BAL=1` alone is the ordinary length beam; interpret older BAL-only logs accordingly.

## Scoring in one line
Per row: beat the live record = 1.0; tie with k teams already on it = 2^-k (k=1 → 0.5, k=2 → 0.25,
k=3 → 0.125). Points last only while we hold a current shortest length. Confirmed against the
leaderboard to 4 decimals on 2026-09-27.

## Which rows to pick (fast triage)
1. **Low k + short record.** Rows held by 1–2 teams with record ≤ 36 (89 on 2026-09-27, 76 never
   tried by us). Short records are where our exact tools are strongest.
   List: `tools/acc/targets_easy_lowk_20260927.json`.
2. **Rival rows.** `sair_api.py teams` shows the rows each team above us scores on. Tying a rival's
   k=2 row gives us +0.25 and takes 0.25 from them.
3. **Near misses.** Rows where our best is 1–3 over the live record (`sair_api.py changes` / `plan`).
4. Long rows held alone (≥ 80 moves, ~2,000 on AC) are worth 1.0 each but our beam rarely finds any
   path there (1 of 195 tried). Use only with a new idea.

## Methods that work (with evidence)

| Method | Use it for | Evidence | How |
|---|---|---|---|
| **H-beam + T9 finish** (`acc_beam`, `BEAM_H=1`) | first path on rows with record ≤ ~45 | most of our 431 accepted ties | `run_beam_raw.py` (no verifier) or `run_beam.py` |
| **Seeded restarts** (`BEAM_SEED`, `BEAM_NOISE` 1–4, `BEAM_DIV` 0.6–1.0, W 200k/400k) | squeezing the last 1–2 moves | ties at 30–35 on 2026-09-27 | `hunt.sh WORKER ROW RECORD` |
| **Exact capped BFS** (`acc_capped`) | short-start rows; either finds a record-length path or proves none within the cap | 71 of 212 exact runs found a record-length path that never exceeded total length 26; ac/sac-00313 tie at 33 | `cap.sh ROW RECORD "caps"`, `run_capped_sweep.py` (caps start..start+6) |
| **Window-14 exact shortening** (`acc_window`) | polishing our own path: any ≤ 14-move segment replaced by a geodesic | 2 of 9 paths shortened (ac-05558 32→30, ac-02628 28→27) | built into `run_beam_raw.py` |
| **(y,x) finish for Stable AC** | SAC: path to (y,x) + `[15,15]` beats AC path + `[16,15]` | sac-08374 21→16, sac-00894 17→15, five more 17→16 (2026-09-24) | automatic in the beam (swap = moves 6↔8, 7↔9, 10↔12, 11↔13) |
| **Exact MITM (S_a ∩ T_9)** (`acc_opt`, `acc_batch`) | proving optimality / board-wide screens ≤ 15 | all 10,115 rows screened; 53 exact optima at 15–19 | see `proof_track/PROOF_TRACK_SUBMISSION.md` |

| **SAC = our accepted AC + `[16,15]`** | free SAC ties when the SAC record = our AC length + 2 | 6 found on 2026-09-27 (`ACC_SUBMIT_SACPLUS2_20260927.txt`) | offline check vs board; moves from `sair_api.py download ID` |

Always: keep the shorter of searched SAC and AC + 2 (`emitcap.sh`). Re-run the AC+2 check after
every board pull: SAC records move, and a row can become a tie without any new search. Every line goes through the
official verifier before `sair_api.py send`.

### Win log
- **2026-09-27 23:36Z, sac-03305: tie at 24 on a row held by one team (about +0.5), plus
  ac-03305 at 23 (tie, k 6→7). Submission 2566.** Found by the adaptive exact capped sweep
  (`run_capped_sweep.py`: start total length 24, raise the cap until the state budget runs out).
  - Caps 24–36 are proved empty.
  - The Stable AC path first appears at cap 37 and the AC path at cap 40 (133M states).
  - The H-beam on the same row gave only 27/29.
  - Lesson: on short rows held by 1–2 teams, the record path climbs 13–16 letters above the start,
    so push the cap high. A cheap start (2M states at start + 6) means big caps are affordable.
- **2026-09-27 23:50Z, ac-01629 23 and sac-01629 25 (ties, k4 and k3, about +0.19), submission 2569.**
  Found by exact sweep C (start total length 23, AC path at cap 42). The Stable AC line is the
  AC path + `[16,15]`: every AC hit now produces its Stable AC line automatically.

### Exact capped proofs so far (no record-length path stays within the cap)
| row | start total | record (target) | proved empty through cap | budget at the next cap |
|---|---|---|---|---|
| ac-06969 | 27 | AC 38 | 32 (first 29 moves) | 123M states at cap 32 |
| ac-00145 | 15 | AC 39 | 22 (first 30 moves) | 70M budget hit at cap 23 |
| ac-06936 | 25 | AC 26 / SAC 27 | 33 | 180M budget hit at cap 34 |
| ac-03305 | 24 | AC 23 / SAC 24 | 36 (then SAC found at 37, AC at 40) | solved |
| ac-03871 | 23 | AC 30 / SAC 32 | 32 | cap 33: `FATAL mmap table` (the table doubling hit the 13 GB limit, which acts as the budget) |
| ac-05818 | 25 | AC 34 / SAC 36 | 26 | 180M budget hit at cap 27 (depth 25) |

Short rows held by few teams need humps of 10+ letters.

**Probe-and-predict caps (2026-09-28):** before a full run, probe the cap with 10M states. Fit the
decay of log(layer growth) on the last 6 layers and extrapolate the total to depth MAXD. Skip the
cap if the prediction is above 90% of the budget. Validated on ac-05818: cap 26 predicted 80M,
actual 87M; cap 27 predicted 397M, actual > 196M.

**Jump-ahead caps (2026-09-28):** a cap-C search contains every lower cap, so start at
start + CAP_JUMP (8 / 3 / 5 by budget) instead of climbing from the start (2–3.5× faster). The
capped search works best at depth ≤ 22 (records ≤ 31). At depth 25+ the budget stops within 1–2
caps of the start (ac-05818: cap 26). Memory (15 GB) caps us near 180M
states per run.

## What has not worked (don't repeat without a new idea)
- k=2 rows with records 44–70: 0 of 34 reached with H-beam.
- SAC k=1 rows: 0 of 17. Unsolved rows: 0 of 126 (beam). Beat-by-one on scoring rows: 0.
- Long rows (record ≥ 70): path found on 1 of 195 (5–80 min each).

## Why mid-length rows are hard: the hump
Exact capped proofs show record paths must first **grow** the relators:
- ac-06969 (start total length 27, record 38): no ≤ 38 path stays within total length 27, 28, 29,
  30 or 31 for its first 29 moves (2026-09-27). The record path climbs above 31.
- ac-00037 (record 31): must exceed total length 35 within its first 22 moves.
Our H-beam ranks states by (mostly) length, so it prunes exactly the states a record path needs.
Ideas to test: beam that rewards "structure" over length at mid-depth, bigger noise at depths
5–20, or capped BFS with caps 35–40 when memory allows.

## Submitting (user rule, 2026-09-27)
`python3 tools/acc/sair_api.py send FILE --yes`: fresh boards + history, only UNSOLVED/BEAT/TIE,
POST within 5 minutes of the pull. Boards and leaderboard refresh on a timer (`generatedAt` seen at 22:35, 22:45, 22:50 UTC). Reads are
limited (360 per window, reset 00:00 UTC); the client keeps 40 for submissions.

## Every 1-point result gets a proof-track write-up
Beat or hold-alone → `tools/acc/proof_track/WIN_<row>_<date>.md` from `WIN_TEMPLATE.md`, with
the commit hashes of the tool and the result.

## Memory note from session 1 (2026-09-28 00:45Z)
- The exact search crashes at about 214M states. The state table (16 bytes per slot) doubles at
  80% full. While it doubles, the old and new tables are both in memory, on top of the 4.5 GB T9
  table, and that goes over the 14 GB ulimit.
- Tried: starting at `INIT_LOG2=29` (8.6 GB, no doubling, budget 420M). It ran at 12.8 GB RSS, and
  **the container restarted minutes later** (probably out of memory). Don't use 29 on a 15 GB
  machine.
- Safe setting: `INIT_LOG2=28`, `BUDGET=210000000`. That skips one wasted doubling and stops
  cleanly before the crash.
- A real fix needs 8-byte entries (fingerprint + distance) or a disk-backed/bidirectional BFS.
  Still open.

## Path shape findings (session 1, 2026-09-28, 163 record-length AC paths)
- **Flat rail:** 35% of shortest paths never go above their start length. Exact search capped at
  the start length (cheap, seconds) covers those rows completely. Running on 563 valuable rows
  (`flat.log`).
- **Push, not oscillation:** about half of all moves keep the length the same. Rises come in
  bursts of 1–3 (+2/+3 each). Falls are larger (down to −10 and below). Push-versus-oscillation
  score +0.34. The length-weighted H-beam prunes exactly these bursts. Idea: allow up to 3
  consecutive rises without penalty.
- **Balance:** both words shrink together. Mid-path lopsidedness averages 0.27, and one word only
  reaches length 1 at 84% of the path on average. Idea: add a |len r0 − len r1| penalty to the
  beam priority.
- **Chart:** `research/acc/optimality/path_chart_163.svg` (word lengths ÷ start length).

## BEAM_BAL test (session 1, 2026-09-28): W=20000, depth cap record+6, 9 near-miss rows
| row (live) | BAL 0 | 1 | 2 | 4 |
|---|---|---|---|---|
| ac-00145 (39) | 40 | 53 | – | – |
| ac-09189 (30) | 32 | 31 | 31 | 31 |
| ac-00147 (34) | 48 | 46 | 45 | – |
| ac-04276 (32) | – | 42 | 43 | 47 |
| ac-05702 (39) | 49 | 47 | 51 | 53 |
| ac-06045 (36) | 44 | 44 | 48 | 48 |
| ac-08995 (45) | 47 | 50 | 50 | 55 |
| ac-09091 (29) | – | 40 | 40 | 40 |
| ac-00037 (31) | – | – | – | – |

- Result: BAL=1 is better on 5 rows (shorter, or finds a path where BAL 0 finds none) and worse on
  2. It ties no record.
- Use BAL=1 as a second "eye" next to BAL 0 (different paths), not as a replacement.

## Cross-row lookup with mirror twins (session 1, 2026-09-28): `tools/acc/crossrow.py`
- Index every state on every known path. For each row, look up the states within R moves of its
  start under 16 mirrors: signed letter permutations × optional word switch. Each mirror maps
  official moves to official moves exactly, plus a BFS fix when the finish moves. Every path is
  replayed with the verifier kernel.
- First run (372 paths, R=1, 14 s): 13 rows new or shorter than our own. Mirrors are real, e.g.
  ac-00974 27 (own 37) via a mirror of ac-07289, and ac-03028 solved via a mirror of ac-09650.
  No record ties yet.
- It scales with memory size (`tools/acc/path_memory.py`) and radius.

## Periodicity eye (Bob's idea 1, tested 2026-09-28): SURVIVES
- Score = best cyclic self-match of a relator. At matched start length, unsolved rows are much
  more periodic than solved ones: +0.15 overall, +0.28 at length ≥ 30. Permutation p = 0.003.
  Kill condition not met.
- The driver is **long runs of one letter**. By the longest single-letter run in the row:

| Longest run | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 11+ |
|---|---|---|---|---|---|---|---|---|
| Unsolved | 6% | 11% | 19% | 34% | 46% | 63% | 75% | 79% |

- No relator is an exact proper power. The runs sit inside the words (Akbulut–Kirby shape).
- Action: the 427 unsolved rows with run ≤ 3 are the "odd easy" ones. The odd-easy list is `work/oddeasy_targets.json`; use
  `BEAM_H=1 BEAM_BAL=1` for the balanced heuristic, and inspect the actual env in prior runs.

## Smaller goal ball under an 8 GB limit (Codex ABC pilot, 2026-09-28)
- Rebuild T8 with `acc_opt tball 8 40000000 work/T8.tab work/abc_t8`. It has 24,587,144 states and uses 640 MB; T9 has 214,977,551 states and uses 4.48 GB. T8 may require one more start-side move, so compare both depth and cumulative states before calling it a win.
- On ac-00236 (cap 25), both tables found official AC 15/SAC 17. T9 first met at depth 6 after 2,561 states; T8 met at depth 7 after 7,615. The wall-time comparison was affected by cache pressure. Reproduce via `research/acc/live/ledger/codex_abc_ball_split.py`; raw output is next to it.
- Two 100-row unsolved screens at width 2,000/depth 80 with T8 (`BEAM_H=1` and `BEAM_H=1 BEAM_BAL=1`) found zero paths. This does not rule out longer or wider paths. Per-row outputs and status: `research/acc/live/ledger/codex_abc_unsolved_*_t8_20260928.jsonl`.
- The file-backed fixed visited-table pilot is `research/acc/optimality/acc_capped_disk.c`. It matched the original on a 299,177-state bounded run, but the repeat was much slower under concurrent memory pressure. It keeps the existing fingerprint-collision caveat; do not call it a memory-wall fix yet.
