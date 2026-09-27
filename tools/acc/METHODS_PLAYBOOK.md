# ACC methods playbook: what works, what doesn't, quick recipes

Mad Hatters, SAIR Andrews–Curtis Challenge. Keep this file current: every method that wins (or
clearly fails) gets a line here with its evidence. Newest facts first inside each section.

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

Always: keep the shorter of searched SAC and AC + 2 (`emitcap.sh`). Every line goes through the
official verifier before `sair_api.py send`.

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
