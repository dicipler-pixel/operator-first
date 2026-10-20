# ACC work summary: UPG-H session + sub-agent ("partner"), 14 Oct 2026 00:00Z to 12:00Z

Covers everything this Claude Code session did in the last 2-3 days. All of it is on 14 Oct; this session made no commits on 11-13 Oct. Branch `claude/gallant-bardeen-0pgpae`, 49 commits, 107 files. **No submissions were sent by this session.** Board used throughout: SAIR export generated 00:10Z (pulled 00:11-00:13Z).

## 1. Bottom line

- **No new ties, beats or first solves today.** One tiny tie line is queued, not sent: ac-06299 36 (AC, k12, worth about 0.0002) and sac-06299 38 (Stable, k9, about 0.002), in `inbox/upgh_symrecog_20261014T081341Z_r1_all.txt`.
- **Biggest findings:**
  1. The beam binary was broken for a week.
  2. The leaders' points sit on long rows, where we have almost nothing.
  3. 334 rows have Stable records well above AC + 2.
  4. The unsolved pool is mostly literature-open problems.
  5. memcon's ladder law.
- **Still running at 12:00Z:** Caltech's own PPO model (AC-SolverX 610model) on the minimal forms of all unsolved rows. It runs as 4 local CPU workers, uses no Claude usage, and saves results to disk. 43 of 1,156 keys are done, 0 solved. To stop it: `kill 13722 16994 17004 17018` (worker.sh PIDs), then kill their python children.

## 2. For Bob (done 00:15-00:30Z)

- `SUBMISSION_AUDIT_20261014T0015Z.md`: every recent submission graded good / bad / duplicate / scored. No double sends; 489 duplicate lines; the new lines were all on rows with k >= 7.
- `SUBMITTED_RECORD_FOR_BOB_20261014T0020Z.txt` (1,482 rows, R/O marks, dedupe rule; also on Drive), `SUBMITTED_LEDGER_20261014T0020Z.tsv`, `SUBMITTED_BEST_20261014T0020Z.json`, `SUBMISSIONS_LIST_20261014T0020Z.tsv`, `mine_20261014T0011Z.json`.
- `PAYING_ROWS_20261014T0020Z.txt`: our scoring rows by teamPoints (sac-07194 at k1 = 1.0; several k3 rows at 0.25; ac-09839 at k4 = 0.125).
- `teams/top_ac_20261014T0022Z.json.gz`: the top-3 teams' rows (memcon.ai 5,545 rows / 653 k1; AC-Solver =D 5,473 / 493 k1; T00118 5,167 / 188 k1).

## 3. Findings, most important first

**3.1 The cached beam binary ignored most options from 6 Oct to 14 Oct 02:20Z.**
- `/root/.cache/acc_beam_bin/acc_beam` read only BEAM_DIV. It ignored BEAM_P2, DUAL, ELITE, NOISE, SEED and CLIMB.
- Every "dual-P2 / seed / climb miss" from that week is really a plain-beam miss.
- Rebuilt from the repo source. The old build is kept as `acc_beam_plain_oct6`. Warning added to `tools/acc/METHODS_PLAYBOOK.md`.

**3.2 Where the points are** (`TOP_TEAMS_METHODS_BESTGUESS_20261014T0030Z.md`, addenda 03:10Z and 04:42Z)
- memcon has 459 of its 653 solo rows above 100 moves, and only 2 at 40 or below. AC-Solver =D has 313 of 493 above 100.
- The board has 1,333 AC rows with a record over 100; 1,005 of them are k1. **We hold a verified road on only 20 of them**, at 1.16-1.75x the record.
- Long-row test: the real dual-P2 beam (W 20000, depth 121) on 6 rows with record 101 and k2-3. ac-00173 reached 122. **The other 5 found no road within 121 at all.** Our beam family cannot reach long-row records.

**3.3 Stable-gap rows** (`STABLE_GAP_20261014.md`)

Stable record minus AC record, per row:

| Stable − AC | −1 | 0 | +1 | +2 | +3 | +4 | +5 | more than +5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rows | 2 | 70 | 833 | 6,204 | 103 | 59 | 29 | 143 |

- **On 334 rows the Stable record is at least AC + 3**, because the AC holder never sent the Stable copy. An AC road over the AC record can still **beat** the Stable record if it is at most Stable − 3.
- Lane on the 16 rows with the most slack (sac-00590: AC 116, Stable 148): 00590 and 02933 found no road at all (depths 145 and 253). Stopped.
- Change-of-variables transfer onto gap rows: 0 of 51 pairs.
- The short gap rows (AC record ≤ 80; 25 of them accept AC + 1 to + 4) overlap the owner's other session (08451, 09747, 00430, 02264, 05309). Ranked list: `sweeps/rival3/stable_gap_ranked_20261014.json`.

**3.4 Unsolved pool**

| Group | Rows | Status |
|---|---:|---|
| All unsolved AC rows | 2,672 | unchanged since 6 Oct (no team has made a first solve in 8 days) |
| MS-1190 "open" presentations | 1,440 | no known trivialization in the literature (`ms1190_metadata.csv`) |
| AK(3) up to automorphism | 5 | ac-00137, 00399, 06194, 06279, 06945; open problem |
| Length-14 minimal forms | 24 | the known MS holdouts |
| Rows of the 216 "uncertified" (literature-solved) presentations | 366 | all already solved on the board |

- The 2,672 rows reduce to **1,157 Whitehead-minimal keys** (about 2.3 rows per key). **No unsolved key equals a solved key**, so no road can be borrowed from a solved row.

**3.5 memcon.ai's ladder law** (TOP_TEAMS addenda 00:55Z and 01:25Z; `sweeps/ladder_law/SONG_IDEAS_upgh_20261014T0151Z.md`)
- Five exponential ladders: XXYxy, XYXYxy, XYXyxY, XYYXYxy, XYYXyxY. Records ≈ 2^n + c·2^(n/2), with c about 7.5-12. memcon holds all 30 rungs with n = 8-10 (29 at k1). None was still on the old 2^(n+1) law.
- From n = 8, odd n sits below both even neighbours on every ladder (a ⌊n/2⌋ / ⌈n/2⌉ parity split).
- XXYxy is Lisitsa's MS_n(w*) family. Lisitsa's roads are about 16x longer (MS(9): 8,634 vs 710).
- Our canonical loop is exactly optimal between its own level states. The exact (y,x) finish equals fin2. A cheap "block rule" was not found within 23 moves.
- Tying memcon's 30 rungs would be worth about 15 points and needs their construction. Unsolved.

**3.6 Other people's GitHubs** (`ALL_WAYS_TO_BUILD_ROADS_20261014.md`, addendum 03:05Z). All read only; only AC-SolverX was later run, with owner approval (section 5).
- **Math-AI-Caltech/acsolverx (ICML 2026 "Two-Hump").** PPO over substitution supermoves (rotate both relators, then multiply). Probably the method of team "AC-Solver =D". Its stored paths index the AC-19 training set, not SAIR rows.
- **ElliotSteffen/ACSolverES.** Change of variables by Nielsen automorphisms (new to us; tested in 3.7).
- **nahomar/andrews-curtis-solver** (team nahom, 10th). Same family as ours. Their log agrees with ours: windows give no gain, width saturates, it needs a different route.
- **Robby955/ac-square-divisibility.** Only G(1,1) is a SAIR row.
- **ph4ge, Amey-Thakur, alejandrozarco, joe-carr-data, HkHk2Prod.** No record-level roads.
- **rosie-0525** (team Catsitter). Not reachable.
- No public OpenAI / GPT work on ACC was found.

**3.7 Change-of-variables transfer** (`sweeps/cov/FINDINGS.md`; tools `whitehead_min.py`, `cov_transfer.py`)
- Whitehead-minimal keys for all 10,115 starts: 7,745 keys, 926 shared, 3,296 rows. 284 pairs have records that differ by 15 or more.
- Transfer web over 400 pairs: **391 verified roads, 0 ties.** The automorphism x -> y^k x makes every x-conjugation cost k+1 moves, and the leaders' records already price that in.

## 4. Scoped misses (do not redo without a new idea)

| Lane | Rows | Scope | Result |
|---|---|---|---|
| 2-move height web | all rows with k ≤ 4 | 8,924 roads | 69 shorter roads, none at record (closest ac-01871 42 vs 41) |
| window-14 fixpoint | 00631, 01871 | full | no change |
| mid-restart, real dual-P2, W 20000 | 05598, 02288 (xy and yx), 01871, 09501, 03714, 08995, 06045, 06969, 04493, 08578, 07385, 00580, 03060, sac-01784, sac-08078, sac-09758, sac-07337, 00282, 03871, 09312, 06768, 02528 | every state of our best road | 0 hits |
| mid-restart, W 60000 | 05598 | same | 0 hits |
| (y,x) beam, real dual-P2, W 20000 | 13 rows (09501, 06045, 07337, 09758, 01784, 04493, 05598, 02288, 08995, 08889, 09980, 04628, 04647) | swapped start | 0 Stable ties |
| tie-scope MITM | 05598 (cap 28), 04628 (23), 09980 (23), 08889 (27), 06045 (27), 09501 (23/25/26) | complete within caps | none; higher caps incomplete (memory) |
| rival rerun, real binary | 03975, 00669, 03186 | from scratch, D 221 | over / none |
| minimal-form beam pilot | first 50 unsolved keys | W 5000, D 200, 3 modes | 0 roads; only 3 keys shrink, by 2-3 letters |
| PPO 610model | first 43 unsolved keys | W 1024, 150 steps | 0 solved (lane continuing) |
| lost-line audit | every road in research/acc | 07:30Z | 0 unsent scoring lines |
| mirror copies, symmetry radius 1 | all 10,109 rows | 15,374 roads | 1 tiny new tie (06299) |

Earlier 14 Oct scoped misses (sub-agent rounds 1-3: tail meet radius 13, foreign meet, capped 09501, old-binary lanes) are in `sweeps/orows/FINDINGS.md`.

## 5. Tools added today (all in the repo)

- `tools/acc/upgh/whitehead_min.py`: Whitehead-minimal form and key for every row.
- `tools/acc/upgh/cov_transfer.py`: automorphism road transfer between key-mates, official-core verified.
- `tools/acc/upgh/stablegap_cov.py`: the same, aimed at Stable-gap rows.
- `tools/acc/upgh/ppo_convert.py`: AC-SolverX substitution paths -> official moves -> transfer to rows -> AC and Stable verify. Tested on 7 solved rows, all verified.
- `sweeps/mr_upgh/mr_lane.py` (and the partner's `orows/mr_lane_new*`): mid-restart on the real engine.
- `sweeps/cov/firstsolve/firstsolve.py`: the partner's minimal-form pilot driver.
- `sweeps/ppo/worker.sh`: PPO chunk worker.
- PPO setup: Python venv with jax[cpu] 0.6.0 / flax 0.10.4 / gymnax 0.0.8 / distrax 0.1.5 / orbax 0.11.16, in session scratch, not in git. The checkpoint needs a placeholder 157,217-line training file (see `sweeps/ppo/README.md`).

## 6. Blockers and owner decisions

1. **Grok's ACC_MASTER_MOVES WORKED tab** (12,915 roads, 13 CSV parts in the Drive SPLIT folder) cannot be pulled here: Drive downloads are blocked, and the connector would need about 600k tokens per part. Commit the CSVs to the repo if you want them merged. New roads are the one thing that moves the webs.
2. **GROKBOTO folder privacy.** Grok's own atlas says it is shared "anyone with the link" and holds private research. Your call.
3. **Network policy** blocks arxiv, easychair, sciencedirect and drive.google.com downloads. GitHub, PyPI and the Drive connector work.
4. **Send or skip** ac/sac-06299 (value about 0.002).
5. **PPO lane:** let it finish (about 9-10 h on 4 cores) or stop it (section 1).

## 7. File index (this session, 14 Oct)

- `research/acc/live/`: the docs and records in sections 2-3, plus `ALL_WAYS_TO_BUILD_ROADS_20261014.md` and `HUB_INVENTORY_20261014.md`.
- `research/acc/live/sweeps/`: `orows/` (partner lanes and FINDINGS), `rival3/` (rival, long-row and Stable-gap lanes), `cov/` (change of variables, Whitehead keys, first-solve pilot), `ppo/` (Caltech model lane), `mr_upgh/`, `mr_upgh2/`, `webs/`, `ladder_law/`.
- `research/acc/live/inbox/`: `bob/` (Bob's tie roads harvested from Drive) and `upgh_symrecog_20261014T081341Z_r1_all.txt`.
- `tools/acc/upgh/`: the tools in section 5.
