# TEAM UPDATE: Git (session 3), 2026-09-29 14:00Z. Everything we think we know now, plus Astra's review in full

Private team research. Everything below is official-core verified or measured on files that are named here.
These are information, **three ties to send**, and proposed tests. No lead orders change. No SAIR API calls were made.
The owner sends ac-09839, ac-09311, ac-06403, ac-04718, ac-05378 and sac-02257. Nothing here touches them.

---

## 0. Three new ties: 2 AC + 1 Stable AC (official core ok, boards 20260929T1145Z)

| Row | Ours now | Record (k) | Came from | Certificate |
|---|---|---|---|---|
| ac-07119 | 33 | 33 (k10) | Kernel's 34 (bob crossclass bundle 2) run through the road-keeping DP (§3) | sha256:695e3a957b6aa181… |
| ac-08371 | 25 | 25 (k7) | our 26 (sweeps/fe_cap.jsonl) run through the road-keeping DP | sha256:a3b02ea666868… |

```
ac-07119: [7, 9, 13, 4, 6, 4, 3, 8, 2, 0, 12, 5, 8, 11, 5, 9, 10, 12, 5, 1, 12, 2, 7, 9, 9, 3, 5, 5, 5, 5, 5, 3, 3]
ac-08371: [10, 2, 5, 1, 6, 8, 12, 10, 2, 6, 4, 7, 13, 10, 10, 3, 9, 6, 4, 4, 4, 6, 2, 4, 4]
```
Plus **one Stable AC tie**: sac-08371 = AC path + [16,15] = 27 = record (k7, stable board 11:45Z). Neither row is in SENT_ROWS.
```
sac-08371: [10, 2, 5, 1, 6, 8, 12, 10, 2, 6, 4, 7, 13, 10, 10, 3, 9, 6, 4, 4, 4, 6, 2, 4, 4, 16, 15]
```
Inbox files: `inbox/20260929T1415Z_git_skeldp_07119.txt` and `inbox/20260929T1400Z_git_skeldp_08371.txt` (which carries both lines).
sac-07119 via +[16,15] is 35 vs 34 (k2): one over, no SAC tie there.

---

## 1. The whole picture: what we did, what we missed, and why

### 1.1 The data
- We pooled **1,746 distinct official-verified AC paths covering 1,086 rows** from every run on file: beams, Kernel/Bob,
  Charlie, the suggester, windows, cross-row, the pool roads and auto-recordings.
  - 433 paths are at record (355 rows) and 1,313 are above record.
  - 292 path lists were rejected by the core.
  - File: `exchange/session3/picture/all_paths.json.gz`.
- Every state on every path was read by six eyes:
  - total length;
  - κ (the relation rail: log|tr[ρr0,ρr1]−18| under the faithful Sanov map);
  - scale (the Sanov stretch, log(1+|tr²−4|) per line);
  - exponent-ledger distance;
  - cyclic 2-letter patterns;
  - "down" (moves that shorten from here).
- The group studies were loaded into the owner's Mixer 5.2 and viewed. They are in `exchange/session3/picture/*.traces.json`,
  with the snapshot `v_grid.png`.

### 1.2 The two rails (standing facts from 28-29 Sep)
- **Scale changes only under multiplications.** On 183 verified team routes, 0 of 2,810 conjugations changed it.
- **κ changes only under conjugations.** The exponent ledger sits on the scale rail.
- **Order on every path.** κ resolves first (it reaches 0 roughly 10→4 moves before the end). Scale falls next and the ledger last.
  The count of cyclic patterns falls steadily all the way.

### 1.3 Where our paths lose (record band 25–50)
- **Groups:**
  - AT RECORD: 229 paths / 216 rows.
  - 1–3 OVER: 254 / 166.
  - 4+ OVER: 790 / 543.
- **At 8 moves to go, the record paths carry the most relation load:**
  - κ: 15.4 at record vs 12.9 for 1–3 over vs 8.4 for 4+ over.
  - Scale: 21.4 vs 19.6 vs 16.4.
  - Record paths hold κ late and then drop it steeply. Longer paths bleed it off slowly over a long approach.
- **The landing is the same length for all groups.** The landing is the moves after κ resolves: 6–7 moves, almost all multiplications.
  **The approach is what differs:** 25 moves at record vs 30 (1–3 over) vs 44 (4+ over).
- **Same-row pairs** (153 pairs, 111 rows):
  - Our extra moves are 88% conjugations, 13% inversions and −4 multiplications.
  - The excess is all in the approach (median +3, mean 3.46). The landing adds +0.05.
  - Ours first carries more scale than the record path at a median of 19 moves to go. It never does in 22/153 pairs.
- **Missed rows differ by record band:**
  - Records 35–50: the rows we do not hold start with lower κ (22.3 vs 28.0), lower scale (27.5 vs 35.5) and a shorter start
    (25 vs 29) than the rows we hold.
  - Records 0–34: the missed rows have higher scale (31.9 vs 29.0).

### 1.4 Why: the anatomy of a near miss
1. **No local waste.** Inside every run of conjugations, we compared the moves spent with the cheapest way to the same pair of
   words (the free-reduced net conjugator, or the shortest rotation arc).
   - Waste was **0%** at record, **0%** at 1–3 over, and 2% of paths at 4+ over.
   - Our beams do not go back and forth, and they do not take the long way round a word.
2. **Junctions.** A multiplication is a junction. Its cost is the conjugations just before it; its gain is the letters it cancels.

   | | mults/path | align conj per junction | letters cancelled per junction |
   |---|---|---|---|
   | at record | 13.0 | 1.28 | 7.73 |
   | 1–3 over | 14.5 | 1.37 | 7.71 |
   | 4+ over | 20.8 | 1.50 | 6.94 |

   - Same-row pairs (48): same number of multiplications (mean extra 0.00), but **+3.40 alignment conjugations**.
   - On the 32 pairs with an equal junction count: +3.03 alignment moves, and our junctions cancel 4.31 fewer letters in total.
3. **Same road, turned the wrong way.** Only 6% of 1-over misses share the record's exact multiplication sequence.
   But compare states **up to rotation, conjugation and inversion** (each relator as a conjugacy class, pair unordered):
   - Our near-miss path visits a **median 88% of the record path's states**.
   - It splits from the record road about **17 moves before the end** and rejoins it about **14 before the end**.
4. **The split of the excess** (68 rows, 1–3 over, 119 excess moves):
   - **60 moves (50%) lie between the SAME two states.** We arrive at the same conjugacy classes, but holding the
     words in a rotation/orientation that costs more conjugations at the next junction.
   - **59 moves (50%) are short detours** through states the record never visits.
   - 25 rows are all "same state, wrong orientation", 13 are all detour, and 30 are mixed.
     Both kinds sit at a median of 6 moves to go on the record clock.
5. **Far misses (4+ over) are different roads:** 21 multiplications vs 13, with slightly weaker cancellation per junction.
   Local repair cannot close them; they need a different road (cross-row, transfer, the 23 stretched targets).

**In one line:** the beams choose each multiplication well (7.7 letters cancelled, no local waste). But they rank states by
length and a few keys that are blind to the *orientation* in which the words are held. The record paths hold their words
turned so that the next junction is cheap. Half of every near miss is that orientation cost, and the other half is a short detour.

### 1.5 What else was tested today (all in IDEAS/ledger)
- **Stretched rows the team misses:** we hold 46% of the flattest decile of starts vs 14–17% of the rest.
  The 23 targets are in `targets_git_scale_20260929T1100Z.json` (~28 points), with orders in `ORDERS_git_scale_20260929T1100Z.md`.
- **Harness v2 eyes** (on 183 routes), correlation with what happens next:
  - Opening: 2-grams +0.73.
  - Breaks: "down" +0.68 and collapse +0.37 before a break.
  - Endgame: ledger/Magnus +0.98.
- **Suggester (the owner's ACC_Replay_Idea_Pool, run unchanged):**
  - 302 transfer tests, 0 shortenings, no trend.
  - It stalls on long ideas: one 286-move idea on ac-03623 blew up the word length (the tool has no length cap).
    That is a finding, and changing it is the owner's call.
- **Missed-break restarts:** 0/17 vs 0/16 control. Negative (`ledger/git_missed_break_restart_20260929.jsonl`).
- **Transport, record vs our near misses:**
  - Our extra moves are mostly conjugations (22 vs 16).
  - The κ-gap drop per conjugation is 1.13 for ours vs 1.45 for the record.
  - The wrong-way share is similar (42% vs 40%).
  - This is the same fact as §1.4 seen on the κ rail.
- **Kernel/Bob relay** (morning): 0 ties at the time. ac-05598 is 40 vs 39 (k1, a full point if it gets shortened by one).
  Several much shorter roads for rows we had sent long, and ac-07119 34, which is now a 33 tie.

---

## 2. What this says to do (proposals, not orders; each is untested until run)
1. **Run the road-keeping DP on every near miss any lane holds** (§3). It costs seconds per path and is verified by the core.
   This is the cheapest source of ties we have found today.
2. **The orientation half:** give the beam an eye for the cost of the next junction (the alignment conjugations needed for the best
   cancelling multiplication from the current rotation), not only the length. Untested; we would build it as its own eye and mix it.
3. **The detour half:** the detours are short (split ~17 to go, rejoin ~14 to go). This is exactly the span where window recovery
   and Astra's quotient lower bound work (spans 2–7, §4). Anchoring windows on the shared conjugacy-class states is new.
4. **Far misses:** a different road is needed. Keep the stretched-target list, cross-row, and session 1's skeleton transfer.

---

## 3. The road-keeping DP (new tool, `exchange/session3/skel_dp.py`)
- **What it does.** It takes any verified path and reads off its *road*: the sequence of conjugacy-class states. It then finds the
  shortest move list that walks exactly that road.
  - Inside a class it runs Dijkstra over moves 0, 1 and 6–13, which never leave the class.
  - Each multiplication (2–5) must land in the next class.
  - Output is re-verified by the official core.
- **Caps:** word growth is capped at +2 letters per relator, with a frontier slack of 3 and an in-class budget of 12.
  The caps are tight, so it is sometimes *longer* than the input. Use min(input, DP).
- **Validation** (rows we already hold, where the excess was all orientation): it recovered the record from our own longer path
  on **14 of 25 rows**.
- **Sweep** on the 731 rows we do not hold (up to 3 paths per row, nearest misses first) is running. Early count:
  - 152 paths / 88 rows done; DP found a route on 135.
  - It was shorter than our input on 10 paths.
  - **2 AC ties + 1 SAC tie so far (§0).** Results: `exchange/session3/picture/skel_dp_sweep.jsonl`.
- **Use:** `from skel_dp import run; run(cid, path)` (needs the verifier and the targets file).

---

## 4. Astra's review (relayed in full as received by the owner, 13:36Z)

Their full notes, runnable checks and results are at `research/acc/optimality/experiments/astra_paper_transfer_20260929/`
(REVIEW_NOTES.md, review_checks.py, checks.json).

```
ASTRA → SESSION 2 / MAD HATTERS
S6 PAPERS, THOMSON PROOF, AND ACC CHAIN REVIEW

Checkpoint: September 29, 2026, 13:36 UTC.
Private team research.

The owner requested two additional review passes, notes, and a team handoff. This is information and proposed experiments, not new lane orders. No new lane was claimed, no production setting changed, and no SAIR API read or submission occurred. Existing lead orders stand.

MAIN FINDING

The useful connection is:

Ordered information → candidate search → exact rejection and verification.

We have a reproducible small affine-quotient diagnostic and an exact Hurwitz macro. Neither has produced a new ACC solution or demonstrated a runtime improvement.

Full review notes, runnable checks, and results are on our private branch:

Repo: dicipler-pixel/operator-first
Branch: claude/gallant-bardeen-0pgpae

research/acc/optimality/experiments/astra_paper_transfer_20260929/

Read: REVIEW_NOTES.md
Run: review_checks.py
Results: checks.json

NEW EXACT CHECKS AND THEIR LIMITS

1. Route verification

All 77 frozen routes were verified again with the clean official SAIR core pinned to a0fd6e6.

The sample contains 2,148 distinct nonterminal states.

2. Finite affine representation

Affine word evaluation modulo p = 5, 7, and 11 agrees with all 14 official AC moves in 90,216 comparisons.

The three target components contain:
- p = 5: 300 states.
- p = 7: 1,176 states.
- p = 11: 8,712 states.

All 142,632 directed-edge distance-label checks pass.

Distances in these quotient graphs give admissible AC lower bounds. Their maximum distances FROM THE TARGET are 5, 6, and 7. These are target eccentricities, not measured all-pairs diameters.

On the 18 wide targets, the maximum across these bounds is only 3–6 moves. This is weak compared with our held route lengths and does not establish a competitive whole-route heuristic.

3. Where the cheap endpoint filter can help

Let h_p(s) be the quotient distance from state s to the target. Then:

L(s,t) = max_p |h_p(s) - h_p(t)|

is a lower bound on the number of AC moves between s and t.

A search with budget b can be rejected when L(s,t) > b.

On overlapping segments of the same 77 routes, this bound certified that no shorter replacement exists for:

- Span 2: 695 of 2,295 windows.
- Span 3: 267 of 2,218 windows.
- Span 4: 132 of 2,141 windows.
- Span 5: 55 of 2,064 windows.
- Span 6: 14 of 1,987 windows.
- Span 7: 1 of 1,910 windows.
- Spans 8–14: zero windows.

These are selected, overlapping observations, not independent trials or a runtime benchmark.

With these tables, L never exceeds 7. Therefore it cannot reject the full 13-move replacement budget for a span-14 window. Its possible use is in low-budget splice subsearches, and it must beat the filters we already use after charging its overhead.

These bounds cover the 14-move AC graph. Do not apply them to searches allowed to use stabilization without a separate justification.

4. Hurwitz macro

The transformation

(u,v) → (u v u^-1, u)

compiles to official moves:

[2,5,2,1]

Its inverse is:

[1,3,4,3]

Each costs FOUR official moves.

The formula, inverse, and product preservation were checked on all 2,148 sampled states.

The macro preserves the reduced product uv exactly. A Hurwitz-only search therefore cannot reach (x,y) unless its starting product is xy; that condition alone is not sufficient.

It could supplement ordinary moves. It cannot be a standalone general solver.

BEAM_MACROS already supports move sequences. Nothing was enabled.

PAPER AND INTERPRETATION CORRECTIONS

1. Pham's paper, 2603.05790v2, proves restricted nonintegrability for g-Codazzi twists. It is NOT another construction of a complex structure on S6.

2. Viaclovsky's paper, 2609.33785v1, supplies useful affine-winding, Hurwitz, and integral-primitivity ideas. Its simply-connectedness argument eventually kills an already abelian fiber lattice. That is not a reduction of arbitrary AC presentations.

3. General generator automorphisms need not preserve our scored move count or beam difficulty. For example, a conjugation by y becomes conjugation by phi(y); when phi(y) = xy, its direct compilation uses two generator conjugations. Transformed endpoints and endgame costs also matter.

Do not conclude that only non-automorphism substitutions can help. Preserve exact move compilations and verification in Kernel/Bob's transfer work. Arbitrary non-automorphism substitutions are not automatically valid problem equivalences either.

4. A Stable-AC solution does not automatically descend to an AC solution. An actual legal route is required.

5. Vals' Thomson proof is a useful example of numerical exploration followed by exact certificates and independent checking. We inspected the documentation; we did not rebuild its Lean proof. Keep their reported verification distinct from our own reproduction.

Source:
https://www.vals.ai/blogs/thomson-n7-lean-proof

Proof package:
https://github.com/huwngtran/thomson-n7-lean

The repository also states that the formal statement is not human-certified and the work is not peer reviewed.

TEAM COORDINATION AND PRIORITIES

Session 1 already runs skeleton transfer. Do not duplicate that family pilot.

Session 2 already runs the BEAM_CHAIN A/B comparison. Do not duplicate that lane.

The reported matched ac-03871 result is:

Chain: AC 31 / SAC 33.
Production baseline: AC 32 / SAC 34.

That is encouraging one-row evidence, equal to noisy seed 11, not a completed A/B win.

The reported sac-08031 splice tie is team evidence. Without the contributing path provenance, we should not attribute it to chain alone.

Window recovery has already converted near misses into ties. That demonstrated engineering gain remains higher-confidence than a new geometric score.

RECOMMENDED ORDER

1. Finish the existing chain A/B with matched settings and per-row route lengths and runtime.

2. If the lead wants the next test, use one offline fixed-workload radius-2/3 splice benchmark:
   - Compare baseline and filtered execution on identical requests.
   - Require identical accepted results.
   - Include table construction, projection, and lookup overhead.
   - Reject the implementation on any discrepancy.
   - Keep it only if total runtime improves.

3. Only then consider a matched Hurwitz-macro experiment, charging all four official moves.

4. A focused later Lean task could prove the projection-to-quotient lower-bound lemma and certify finite distance labels. This is a small, specific proof obligation; it does not require solving the entire Andrews–Curtis conjecture.

No extra agents or production search lanes were started for this review.

PRODUCTION OBSERVATION AT THE CHECKPOINT

This is a historical process observation, not a fresh status claim:

- Runner: PID 690203, start ticks 4294021.
- Beam: PID 690204, start ticks 4294033.
- Row: ac-07194.
- Width: 200,000.
- Depth: 46.
- Watcher: PID 690232, start ticks 4294114.
- Completed wide rows: one, ac-04316, still a non-hit.
- No completed ac-07194 receipt was present at inspection.
- One beam; no chain flag.
- Direct /proc cwd access was denied; command and start identity were readable.

Keep the first-three-wide-row assessment and existing window-recovery safeguards. Refresh actual process identity and output before any restart.

NO SAIR API CALLS OR SUBMISSIONS.
TEAM/OWNER SUBMISSION WORKFLOW REMAINS IN FORCE.
```

### 4.1 How Astra's review and Git's picture fit together (Git's reading; the joint uses are untested)
- **Same conclusion from two directions.** Astra: "window recovery has already converted near misses into ties; that gain is higher
  confidence than a new geometric score." Git: half of each near miss is a short detour (split ~17 to go, rejoin ~14),
  and the other half is orientation. The road-keeping DP turned that orientation half into three ties today (2 AC + 1 SAC).
- **Astra's quotient bound L(s,t)** certifies spans 2–7 and nothing above 7. The detours in §1.4 are in that span range.
  L is a natural reject filter inside a detour-window search anchored on the shared conjugacy-class states. Untested.
- **The Hurwitz macro [2,5,2,1]** preserves the product uv and is a multiplication-only move. On the two rails it moves scale and never κ.
  If it is ever tried, it belongs in the approach, where our paths lose, and must be charged four moves.
- **Astra correction 4 (Stable AC does not descend to AC)** matches our practice: SAC lines here are always AC path + [16,15].

---

## 5. Files (all on this branch)
- `exchange/session3/picture/`:
  - all_paths.json.gz (1,746 verified paths);
  - the Mixer 5.2 studies (`picture_{total,kappa,scale,ledger,grams2,down}.traces.json`, `pair_study.traces.json`);
  - v_grid.png;
  - why_conj.py, why_junction.py, why_seq.py (plus why_seq_rows.json), why_segments.py (plus why_segments_rows.json);
  - skel_dp.py, skel_dp_sweep.py, skel_dp_sweep.jsonl;
  - collect_all_paths.py, eyes_all_paths.py, picture_analysis.py, picture_studies.py.
- `exchange/session3/skel_dp.py` (same tool, top level) and the scale/targets scripts from 11:00Z.
- `targets_git_scale_20260929T1100Z.json` and `ORDERS_git_scale_20260929T1100Z.md`.
- IDEAS.md entries dated 29 Sep for Git 11:00Z, the Kernel relay, the missed-break test and 14:15Z.
