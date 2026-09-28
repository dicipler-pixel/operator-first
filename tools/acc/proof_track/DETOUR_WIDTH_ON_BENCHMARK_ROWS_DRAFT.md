# Exact length-bounded detour widths on SAIR benchmark presentations

**Team:** Mad Hatters. **Track:** Proof Track, AC, direction *proof*. This is a partial computational
result about the scored Discovery graph `ac-r2-v1`. It does not resolve AC or Stable AC.
**Status:** DRAFT for the team to review before submission (2026-09-28).

## 1. Summary

Recent Proof Track notes define *detour width*: the least possible peak total relator length over
paths to a presentation. They show it is not a function of graph distance, using two
one-move neighbours of ⟨x, y⟩ (ph4ge/ac-detour-width; our note ACC-P000009 on the
letter-restricted graph). Fagan et al. (*The Two-Hump Problem*, arXiv:2606.21611) observe
empirically that short AC paths often have to climb first.

We measure that climb **exactly on scored benchmark presentations**. For a start S and a length
bound R, define

  DW_R(S) = min over `ac-r2-v1` paths from S to (x, y) of length ≤ R of the maximum total relator
  length along the path.

- For **four** scored presentations, with R = the live record, we determine DW_R(S) exactly: an
  exhaustive search rules out every lower peak, and an explicit path attains it. The largest climb is
  **+16 letters above the start** (ac-03305: start 24, DW_23 = 40).
- For **45** more, we prove lower bounds. For example, every path of record length for ac-03060
  (start 22, record 28) climbs to ≥ 38.

## 2. Method

**Target ball.** T₉ is every state within 9 moves of (x, y), with its exact distance: 214,977,551
states, SHA-256 `48a81fea88f49c5c9499bde3738b813792c405bedff41b8ddc229f9aee7bb053`. The move set
is closed under inversion, so "within 9 moves of the target" and "reaches the target in ≤ 9 moves"
are the same set.

**Capped lemma.** Let BFS_C be breadth-first search from S over states with total relator length
≤ C. Each generated state is looked up in T₉. If BFS_C completes every layer through depth R − 9
without meeting T₉, then **no path of length ≤ R has all of its first R − 9 states within total
length C**. *Proof:* such a path of length L ≤ R reaches, at step max(0, L − 9) ≤ R − 9, a state
of T₉ that BFS_C would have met. ∎ Hence DW_R(S) ≥ C + 1.

**Exactness.** When a search at cap C + 1 meets T₉ and returns a path of length ≤ R whose whole
peak is C + 1, then DW_R(S) = C + 1. For the rows below, the T₉ part of each returned path does
not exceed that peak.

**Scope.** Only `ac-r2-v1`: 14 moves, and conjugation by a single letter, so this is the letter
graph of ACC-P000009, not the word graph of `AC.lean`. Every path is replayed and accepted by the
official verifier (commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`) and by the SAIR server.

**Hashing caveat.** Visited sets use 128-bit fingerprints (123 effective bits). A collision could
only hide a state, which could only make a lower bound wrong, with probability about 1e-20 at
these sizes. It cannot create a path: every path is rebuilt from exact words and replayed.

## 3. Exact values (R = live record)

| row | start total | R (record) | caps proved empty | DW_R | climb | path (accepted, SAIR submission) |
|---|---|---|---|---|---|---|
| ac-03305 | 24 | 23 | 24–39 | **40** | +16 | `[0,11,13,2,5,7,3,8,11,13,13,2,0,6,3,9,9,4,1,3,5,3,3]` (2566) |
| ac-01629 | 34 | 23 | 34–37 | **38** | +4 | `[1,9,12,12,4,8,4,8,8,8,8,6,5,13,13,2,0,5,3,11,3,3,3]` (2569) |
| ac-05558 | 27 | 24 | 27–28 | **29** | +2 | `[6,4,4,3,7,8,6,12,5,1,11,2,11,13,11,13,11,3,7,5,5,3,3,5]` (2572) |
| ac-07435 | 26 | 26 | 26 | **27** | +1 | `[0,4,8,12,12,4,10,5,1,13,11,3,12,11,12,4,12,3,0,2,6,3,9,12,4,2]` (2581) |

ac-03305 is a sharp two-hump instance: its record-length paths must climb 16 letters above a
start of 24, and some do so without going any higher. For all four rows, the returned path's peak
over its whole length equals its peak over the first R − 9 moves.

## 4. Lower bounds (no path of length ≤ record stays within the cap)

Top 15 of 45, by climb. The full list is in `research/acc/live/dw_bounds_20260928.json`.

| row | start | record R | DW_R ≥ | climb ≥ |
|---|---|---|---|---|
| ac-03060 | 22 | 28 | 38 | +16 |
| ac-03871 | 23 | 30 | 33 | +10 |
| ac-05598 | 19 | 39 | 29 | +10 |
| ac-03799 | 17 | 25 | 27 | +10 |
| ac-06936 | 25 | 26 | 34 | +9 |
| ac-06717 | 21 | 38 | 30 | +9 |
| ac-00513 | 16 | 30 | 25 | +9 |
| ac-00828 | 15 | 30 | 24 | +9 |
| ac-01079 | 19 | 30 | 28 | +9 |
| ac-05521 | 19 | 31 | 28 | +9 |
| ac-01770 | 16 | 31 | 25 | +9 |
| ac-00145 | 15 | 39 | 23 | +8 |
| ac-09763 | 26 | 26 | 34 | +8 |
| ac-02153 | 35 | 27 | 43 | +8 |
| ac-06969 | 27 | 38 | 33 | +6 (separate run, caps 27–32; see METHODS_PLAYBOOK.md) |

Paths at these records exist (other teams hold them), so each bound says how high those
unpublished paths must climb.

## 4a. An empirical observation (not a theorem)

Is the size of the hump visible in the start presentation? We measured the **cyclic commutator
load**: the minimum over cyclic rotations a of r0 and b of r1 of the reduced length of
a b a⁻¹ b⁻¹, divided by 2 × (start length). It measures how far the two relators are from
commuting.

Across 292 verified known paths, the correlation between this load and the climb (path peak − start
length) is +0.36. The quarter of rows whose relators commute least climbs about 75% higher. Start
length is the stronger signal (−0.45): short starts climb more.

Neither signal predicts the extreme humps of §3–4. ac-03305 climbs +16 with a load of 0.67, while
ac-07435 climbs +1 with a load of 0.73. A structural invariant that predicts DW_R before searching
remains open.

## 5. What remains open

- Exact DW_R for the 45 bounded rows. The searches stop at 70–180M states (15 GB), which limits the
  caps.
- Whether DW_R can exceed start + 16 on the benchmark, and how it relates to the full detour width
  (no length bound) of ph4ge's definition.
- Anything about the word graph of `AC.lean`, or about Stable AC.

## 6. Reproduction

```
git clone https://github.com/SAIRcompetition/Andrews-Curtis sair && git -C sair checkout a0fd6e6
git clone https://github.com/dicipler-pixel/operator-first && cd operator-first
bash tools/acc/build_T9.sh work                     # T9.tab, SHA-256 checked
gcc -O3 -march=native -o work/acc_capped research/acc/optimality/acc_capped.c -lm
# one cap:  MAXD=R-9 INIT_LOG2=27 work/acc_capped work/T9.tab C 180000000 tmpdir tag l0 w.. l1 w..
# sweep:    python3 research/acc/optimality/run_capped_sweep.py sair/.../manifest.json work work/T9.tab tmp targets.json out.jsonl
```

Code commits: `acc_capped.c` / `acc_opt.c` at `68ad3965603aeaab57e6d6c052bc050507f216c9`, sweep
driver at `de40c3c7687f06e6543e681ee6f924f3b8fb1342` (repository dicipler-pixel/operator-first).

## 7. Prior work and credit

- ph4ge, *ac-detour-width* (SAIR Proof Track, 2026-09): the detour-width definition and its
  independence from graph distance. We use the definition, restricted to length-bounded paths on
  the letter graph.
- Mad Hatters, ACC-P000009 (Grok-prepared note): the word/letter graph split and the exponential
  envelope on the letter graph. This note is its computational companion on benchmark rows.
- L. Fagan et al., *The Two-Hump Problem*, arXiv:2606.21611 (ICML 2026): the empirical two-hump
  phenomenon.
- A. Shehper et al., arXiv:2408.15332v2: AC search as a benchmark. The ACSolverX priority is used in
  our path-finding beam, not in these proofs.
- M. Bridson, arXiv:1504.04187: context on the complexity of balanced presentations.
- SAIR: `AC.lean`, `ac-r2-v1`, reference verifier and benchmark (commit a0fd6e6).

## 8. Provenance and AI use

This work was done by the Mad Hatters team with substantial AI assistance. We describe each
part's role.

- **Direction (human).** The team lead set the mission and chose what to pursue. They made the
  working rules: fresh live-board checks before every submission, batched sends, and a written
  proof for every 1-point result. They reviewed results throughout and directed the other AI
  helpers.
- **Guidance: [NAME OF THE TEAM'S MAIN AI ASSISTANT].** For more than a week, the team lead worked
  with this assistant to plan the project and write the instructions and prompts that steered the
  Claude sessions.
- **Execution and drafting: Claude (Anthropic), in Claude Code sessions.** Claude wrote and ran the
  search code in this repository and ran the exact capped searches: the T₉ table, `acc_capped.c`,
  the sweep driver, and the analysis scripts. It computed the tables and drafted this note.
  Earlier Claude sessions on the same project built the T₉ table and the capped-search engine.
- **Other helpers.** A Codex assistant prepared route maps used elsewhere in the project, but not
  in this note's results. Grok prepared our companion note ACC-P000009.
- **Checks.** Every path in §3 was replayed and accepted by the official verifier and by the SAIR
  server. Every bound comes from code and logs in the repository at the commits in §6. The team
  lead reviewed the note before submission. AI assistance does not change the scope of the claims
  in §2 and §5.
