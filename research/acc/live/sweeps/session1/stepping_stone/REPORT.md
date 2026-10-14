# Stepping stones (idea A) and blind guesses (idea B): experiment report

Date: 14 Oct 2026, 08:15–10:10Z (about 2 h of wall time, at most 3 processes). Branch `claude/gallant-bardeen-0pgpae`.
No SAIR submission or API call was made, the six never-rows and their sac twins were excluded, and nothing was committed.

## Bottom line

- **Scoring lines: 0.** `scoring_lines.txt` is empty. `plan_offline_output.txt` holds the verdicts.
- **New verified roads: 16** (`roads_new.txt`). Each one is shorter than the road we held for that row, none of them was already in `ALL_VERIFIED_ROADS_20261014.txt`, and every one replays on the official core.
  - The best is **sac-04628 at 41**, 1 over the record of 40 (k2).
  - The others are 3 to 7 over the record.
  - The genuinely new ones: ac-00617 61 (we held 63), ac-04676 73 (held 74), and the Stable lines sac-00617, 02909, 04219, 04628, 04676, 07541, 08054 and 08757.
  - The other 6 Stable lines (sac-02932, 03826, 04780, 04794, 06419, 06583) are only an AC road we already held plus `[16,15]`.
- **First solves: 0.** All 146 unsolved short rows had 0 hits, from road states and from walk states.
- **Idea A: works mechanically, but it does not close gaps.** It is cheap enough to keep as an extra web input. It is not worth scaling as a gap-closer.
- **Idea B: works only on easy rows.** It is not worth scaling for hard or unsolved rows.

## What was built (all in `scripts/`, and runnable without a model)

| file | what it does |
|---|---|
| `stones_lib.py` | Contains:<br>• a fast move function. Its self-test checks it against `core.apply_move` on 20k random moves.<br>• the 16 symmetries (x↔y, invert x, invert y, swap relators) with a move relabelling map that is checked on all 16 images.<br>• an exact symmetry normal form (`bytes.translate`, about 400k states/s).<br>• `Store`: every state on every held road, with its best known tail to (x,y) or (y,x). It also has an optional radius-1 halo, and it rebuilds roads move by move. |
| `stones_search.py` | Builds the Store from the verified roads (plus walk files), then runs a capped BFS outward from each target's official start. Every reached state is looked up. A hit gives the road = BFS prefix + donor tail mapped by the symmetry + an exact finish (+`[16,15]` or `[15,15]` for a Stable line). Every candidate is checked with `specs.verify_challenge` on the pinned verifier. Hits are split into road (A) and walk (B), with donor-row attribution. |
| `walks.py` | Idea B: random walks backward from (x,y), where each state's road is the reversed walk with inverse moves. Biases: `band`, `profile` (Metropolis toward the targets' per-relator x/y letter counts), `balanced`, and `--seed-roads` waypoint seeding. |
| `make_targets.py` | Rebuilds the target lists. The CSV has CRLF line ends, so a naive grep finds 0 rows. |
| `run_all.sh` | Reruns everything: `bash research/acc/live/sweeps/session1/stepping_stone/scripts/run_all.sh /path/to/sair` from the repo root. |

**Cyclic rotations are not merged.** The key is the exact 16-symmetry normal form, so relator rotations and inversions are paid as real moves by the BFS (the coordinator's caution). The Store holds 7,372 usable road paths, which make 79,401 distinct states up to symmetry (120k exact states). The webs' fixed point lives on this small set.

## Runs (exact scopes; every row's numbers are in `runs/*_summary.tsv` and `runs/*.log`)

"Depth-complete" means the BFS finished that depth inside the state budget. It does not mean the capped component was exhausted.

| run | targets | Store | cap / depth / budget | target states | status | hits | new roads |
|---|---|---|---|---|---|---|---|
| g1 | 78 rows, 59 starts (k≤2, gap 1–8) | roads + 2.40M walk states (band 16–28, profile 16–28) | start+8 / ≤12 / 1.5M | 92.0M | 25 starts depth-complete, 34 INCOMPLETE (depth 9–11) | road 10,446, **walk 0** | 13 (0 scoring) |
| g1halo | same | roads + 560k radius-1 halo (states ≤ 40) | same | 92.0M | same | road 87,356 (foreign donors in all 59 starts) | +3 (sac-08054 54, sac-07541 47, sac-04628 41) |
| g1gap12 | 17 gap-1/2 rows, 13 starts | roads + halo | start+10 / ≤20 / 5M (+80 rebuilds per row) | ~107M | all INCOMPLETE (depth 9–19) | road only | 0 |
| g2 | 146 unsolved ac rows, start ≤ 16 | roads + 3 walk files (band, profile, balanced 12–18; 4.0M walk states) | start+6 (≤22) / 12 / 2M | 29.3M | all 146 depth-12 complete | **0 / 0** | 0 |
| g2deep | same 146 | roads + halo + climbing walks 12–34 (2.58M) + waypoint-seeded walks 14–34 | 28 / ≤40 / 1.5M | 341.6M | all INCOMPLETE (depth 7–9) | **0 / 0** | 0 |
| controlB | 80 SOLVED rows, start ≤ 16 (random sample) | walks only (no roads) | start+6 / 12 / 1.5M | 42.1M | – | walk hits in 10/80 rows | roads for 10 rows: 5 at the record (records 8–17); others 59–132 moves for records 21–26 |
| controlA | the same 80 solved rows | roads + halo | start+6 / 12 / 1.5M | 42.1M | – | road hits in 80/80, foreign in 78/80 | road ≤ ours in 64 rows (mostly own roads; not a clean control) |

**Hit rate (idea A, group 1).** Every start meets verified road states within 9–12 moves: 10k hits without the halo and 87k with it, and foreign rows' roads are among them in all 59 starts. But the best foreign hit is a lower bound, and it never reaches the record:
- AC rows: estimate > record.
- Stable rows: estimate + 2 > record.

The 12 lowest-estimate hits per row (80 on the gap-1/2 rows) were all rebuilt and replayed, so the misses are real inside these balls. The gains are 1–3 moves, and they come from crossing between our own lineages and their twins. The donors are a handful of common lineages (ac-00042, 00183, 00713, 00963, ...). Their roads pass through low states near (x,y), so a target that reaches them still pays a long shared tail.

**Hit rate (idea B).**
- **Hard rows: 0 walk-state hits** in 59 group-1 starts and 146 unsolved starts. That covers 4.0M + 2.4M + 5.1M walk states and 463M target-side states.
- **Positive control:** blind walks alone rebuilt roads for 10 of 80 solved short rows, and 5 of them at the record. All five record hits are rows with records 8–17.

## Why the unsolved rows were never in reach (and what the literature adds)

- For AK(3) (ac-00399), P1/P2 (ac-02089 / ac-08126) and the 550 open Miller–Schupp rows, every trivialisation must reach a total length of at least 26 (nahomar Theorem A; see `LITERATURE.md`).
  - So a walk banded at 18 lies on a road with peak ≤ 18, and it can never meet those rows. That made pass g2 a control.
  - Pass g2deep fixed this: target cap 28, and walks climbing to 34. It still found 0 hits.
- The short starts sit in thin components. The pass-1 balls were only 0.1–1.1M states at depth 12, and they touch no state on any verified road or walk.
- At cap 28 the space explodes: the AK(3) class alone has about 729M symmetry orbits at cap 25. A random meet there is not a realistic event at any budget we can afford.

## Verdicts (plain language)

**Idea A: stepping stones.**
- It is correct: 16 roads, all verified.
- It is cheap: about 30 minutes for all 78 group-1 rows on one core.
- It reproduces what the webs already know. Around a hard low-k start, the only nearby verified states belong to its own lineage or a few common lineages. Reaching them costs as much as the road we already hold.
- It closed no gap (best: sac-04628 at +1) and solved no unsolved row.
- **Not worth scaling as a gap-closer.** It is worth keeping only as a feeder: run it after each new batch of outside roads arrives, because it does turn new roads into 1–3 move shortcuts.
- A deeper BFS will not change this. The gap-1/2 rows at 5–22M states per start found nothing beyond the 1.5M runs.

**Idea B: blind guess, then reverse engineer.**
- It works only where the answer is short. On solved rows it rediscovers record roads when the record is ≤ 17.
- It produced 0 hits on every hard or unsolved row, including walks seeded at 195k road waypoints and walks allowed to climb past the proven peak of 26.
- **Not worth scaling.** The state space at the needed lengths is many orders of magnitude larger than any walk cloud we can store.

**If anything is scaled, it should be route diversity aimed at the target, not at the goal.** This is the literature's lineage-capped beam with waypoint restarts and splicing, and its cyclic-space substitution planner. Those methods spend their budget near the target and above the peak, which is where both ideas here ran out.

## Files

- `roads_new.txt`: the 16 new verified roads.
- `scoring_lines.txt`: empty, because plan_offline found no TIE, BEAT or UNSOLVED.
- `plan_offline_output.txt`: the verdict for every new road.
- `DISCUSSION.md`: the running log, including which coordinator suggestions were adopted.
- `targets_*.csv`: the exact target lists.
- `runs/`: per-row summaries and logs.
- The walk files are not shipped (about 33 MB). `run_all.sh` regenerates them deterministically from the seeds.
