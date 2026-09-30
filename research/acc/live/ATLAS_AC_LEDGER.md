# The Operator-First Atlas against Andrews–Curtis: complete ledger

2026-09-28, session 2 helper. Every plate (I–XXI), every card in the 2026-09-07 card set (B1–B90, B94–B96;
B91–B93 unavailable) and every repo card (`atlas/cards.json`, 18), one line each.

**Sources read.** Full atlas text (`research/acc/atlas_drive/THE_OPERATOR_FIRST_ATLAS_20260827.txt`); the 93 HTML cards,
manifest, `calculus/ATLAS_CALCULUS.md` and `calculus/SOFIC_SCOPE.md` in
`tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards/`; `atlas/cards.json`; the 2026-09-19 sweeps
on `origin/claude/confident-fermi-09rd02` (`tools/acc/ATLAS_CARDS_FULL_SWEEP_v1.md`, `ATLAS_TRANSFER_TRANSPORT_v1.md`);
`research/acc/live/IDEAS.md` and `tools/acc/METHODS_PLAYBOOK.md` as of commit e46fedf, plus the remote IDEAS entry 09:30Z (9572fdb).
At 09:45Z the working tree also held the lead's uncommitted `acc_beam.c` options `BEAM_QUOTA`, `BEAM_WH` and `BEAM_TRACE_FILE` (and
`optimality/beam_loss.py`), with no results yet. They implement #1, B83's frame key and the B20 diagnostic below, so those stay UNTESTED here.

**Classes.** METHOD: could become a score, pruning/ordering rule, decomposition, construction or certificate.
DIAGNOSTIC: tells us why something fails or where to look. PROCESS: a working rule for experiments. NONE: no AC bearing.
**Status.** TESTED (result, with the IDEAS.md entry time or other source) or UNTESTED. "Test A/B" = run for this ledger (below).
Citations like "IDEAS 05:30Z" mean the 2026-09-28 IDEAS.md entry with that time stamp.

## Counts

| | METHOD | DIAGNOSTIC | PROCESS | NONE | lines |
|---|---|---|---|---|---|
| Plates I–XXI | 5 | 4 | 5 | 7 | 21 |
| Cards B1–B96 (93) | 14 | 15 | 9 | 55 | 93 |
| Repo cards | 4 | 1 | 4 | 9 | 18 |
| **All** | **23** | **20** | **18** | **71** | **132** |

The 23 METHOD lines: 11 fully tested (3 work: Plate IV and B31, both P2; B81, mirror transport. 8 dead), 8 partly tested
with an untested extension, 4 untested. Of the 12 cards not in the PDF (B85–B90, B94–B96), none yields a new search method.
B94 explains why invariant lower bounds die, B95 gives a cheap class hash, B86 restates the hump, and the rest have no AC bearing.

## Tests run for this ledger (offline, one `nice -n 10` Python process, 30 s wall)

Data: every AC path in the repo, replayed with the official verifier, as in `research/acc/optimality/p2_hump_test.py`:
652 distinct row paths, 546 rows verified, 246 at the live record (board snapshot 04:28Z), **59 hump paths** (climb ≥ 6),
1,684 steps, 305 climbing steps. Metric: sibling rank (mid-rank ties, 14 children) of the record move. Baseline
K0 = (P2 cut 8, P1m, raw), the best offline proxy of the P2 beam: top-3 on climbing steps **0.413**, on all hump-path steps **0.593**.
The record child shares the minimum P2 with a sibling on 1,036 of 1,684 steps (62%), so P2 plateaus are common.
Kill conditions were fixed before the run (in the script header): a variant survives only if climbing top-3 ≥ K0 + 0.05 **and**
all-steps top-3 ≥ K0 − 0.02.

| Test | Atlas source | Variant | top-3 climbing | top-3 all | Verdict |
|---|---|---|---|---|---|
| A | B6, B22, B57, Plate XIV | P2, then **more** P2-optimal exits (mult) | 0.325 (−0.088) | 0.625 | DEAD |
| A | B22 | P2, then more non-climbing level-1 exits (cap1) | 0.423 (+0.010) | 0.555 | DEAD |
| A | B22 | P2, then more two-step non-climbing exits (cap2) | 0.416 (+0.003) | 0.574 | DEAD |
| B | B12, B38 | learned linear descent functional: pairwise logistic over 11 state features (raw, P0cyc, P1, P1m, P2, mult, cap1, cap2, min, max, imbalance), 2-fold row-held-out × 5 splits | 0.153 vs K0 0.414 | 0.639 vs 0.592 | DEAD |

Reading: exit counts do not break P2 plateaus in favour of record moves. A single linear functional learns "don't climb"
(raw weight +0.90). It gains on flat steps but loses the climbing steps that hump rows need. The lexicographic P2-first key
remains the best offline proxy. The script is in the appendix. Its raw JSON is in the helper's scratch
(`scratchpad/atlas_ledger/p2_tiebreak_ranker_20260928.json`).

## Plates I–XXI

| Plate | Gist | Class | AC reading (METHOD: compute · cheapest test · kill) | Status |
|---|---|---|---|---|
| I The Chart | strata map, graded bridges | NONE | index only | — |
| II What protects what | amplitude (metric) dies at a wall; phase (integer) crosses | DIAGNOSTIC | reading behind P2: word length climbs over a hump, class-level data crosses it | TESTED via P2: median climb 0 vs raw 9 (IDEAS 05:30Z) |
| III L0 Calibration | positive/negative controls, blinding, permutation nulls | PROCESS | every A/B gets a control arm and a kill fixed first; check stderr "macros: N" / "p2:" before trusting an arm | applied (IDEAS 08:30Z void macro arm, 09:25Z rerun) |
| IV L1 Subspace | change lives between occupied subspace and complement | METHOD | = B31: conjugations stay in the class, multiplications move it → P2 key | TESTED, WIN (see B31) |
| V L2 Spectrum | non-normal operators grow transiently while stable | DIAGNOSTIC | the hump is transient growth; non-commutation of r0, r1 predicts it | TESTED: cyclic commutator load vs climb corr +0.36; linear model R² 0.34 (IDEAS 02:00Z); triage only |
| VI L3 Wall | refraction, walls made by what crosses, subadditive gluing | DIAGNOSTIC | length caps are walls that record paths must cross (hump) | TESTED: exact capped proofs (PLAYBOOK table; 03305 empty through cap 36) |
| VII L4 Census | a direction costs a channel; overflow = forced coarse-graining | METHOD | per-class beam quota (see B16/B17) | UNTESTED → top 8 #1 |
| VIII L5 Memory | integer steps only at Alexander roots | NONE | knot signature; AC invariant bounds are log-scale (IDEAS 02:45Z) | — |
| IX L6 Volume | dilogarithm volumes, Bures geometry | NONE | no AC bearing | — |
| X L7 Realizations | suns, horizons, Λ, colour | NONE | physics landings | — |
| XI The station travels | structural degeneracy; change the instrument, not the exposure; interleave settings | PROCESS | when budget doesn't move a result, change the key or method; run A/B arms on the same rows and seeds | applied: P2 beam 4 ties in 2 h vs exact mid-row sweeps 0 in 6 h (PLAYBOOK) |
| XII The spine | lift to the object that contains a broken descriptor; height is exposure | METHOD | the ladder word → cyclic class (P0cyc) → P1 → P2 is this lift; next rung P3 (three multiplications). Top rung warning: invariants survive everything and bound nothing | lower rungs TESTED (P2 wins); P3 UNTESTED → top 8 #4 |
| XIII The bridges | index of B1–B84 | NONE | one line each below | — |
| XIV Inside, between, or both | zero length, still moving | DIAGNOSTIC | length-neutral moves (about half of all record-path moves, PLAYBOOK path shape) move the state while length reads 0; P2 plateaus | exit-count tie-break TESTED DEAD (Test A) |
| XV The spectrum decides | dominant-mode rate; route by rate; Kronecker factorisation | METHOD | (a) predict capped-search cost from layer growth; (b) route by rate: rank short move blocks by x-mass created per move on MS level states | (a) TESTED, works: probe-and-predict 80M vs 87M (IDEAS 02:20Z); (b) UNTESTED → top 8 #2 |
| XVI The span travels | offset/scale calibration, log running | NONE | (start-normalised features already used in commutator load) | — |
| XVII The method | ask what would falsify it; prior art; symmetry forcing zero; reproduce a known value first | PROCESS | reproduce a known record (e.g. 03305 at 23) before trusting a new search mode; read prior art (Carreras 2607.23611, Two-Hump, MMS) first | applied partly |
| XVIII Tip to tail | compute every rung twice, in two frames | METHOD | (a) Whitehead-minimal frame as a score; (b) primitive-relator finish target; also a process rule: a new score must be mirror-invariant | (a) TESTED weaker than P2: +12 climb on 03305 (IDEAS 04:45Z); (b) UNTESTED → top 8 #5 |
| XIX Standing rules | grade every claim; repair before deleting; argue a check before running | PROCESS | kill conditions written before runs; keep failed results at full size | applied |
| XX The relational web | ring of nine, empty centre | NONE | no AC bearing | — |
| XXI Proof of record | scripts printed whole | PROCESS | every claim ships its runnable script and raw output (as `live/ledger/`) | applied |

## Cards B1–B96 (edition 2026-09-07; B91–B93 unavailable)

| Card | Gist | Class | AC reading (METHOD: compute · cheapest test · kill) | Status |
|---|---|---|---|---|
| B1 | curvature ≤ metric (4 det g ≥ Ω²) | NONE | Berry-curvature bound | — |
| B2 | normality ⇔ [S,K] = 0 | DIAGNOSTIC | commutator [r0,r1] as non-normality predicts hump height | TESTED corr +0.36 (IDEAS 02:00Z) |
| B3 | rigidity ∝ 1/cos⁴θ | NONE | wall asymptotics | — |
| B4 | one metric, or five coincidences | PROCESS | when several methods agree, find the shared step before counting them as independent | — |
| B5 | no boundary, no list | NONE | restates that the cap makes capped BFS finite | — |
| B6 | entropy = membership ambiguity | METHOD | break P2 plateaus by how many continuations realise the best 2-step value · Test A · kill fixed | TESTED DEAD (Test A: −0.088) |
| B7 | signature steps only at unit-circle roots | NONE | knot signature | — |
| B8 | spectral gap = lattice distance | NONE | abelian (exponent-matrix) distance is a log-scale invariant bound, dead class (IDEAS 02:45Z) | — |
| B9 | winding survives a defect | NONE | eigenphase winding | — |
| B10 | Riley constant term = Alexander | NONE | the presentation's representation variety is AC-invariant; its guide form is OBS-PROBE-SPAN | — |
| B11 | volume = sum of dilogarithms | NONE | hyperbolic volume | — |
| B12 | entropy production = exported misalignment | METHOD | find a descent functional that record paths follow · Test B (learned linear functional) | TESTED DEAD (Test B: 0.153 vs 0.414) |
| B13 | going around swaps the pair; twice restores | DIAGNOSTIC | a hump is a loop in the exponent-sum picture: transfers are more often ±I/finite, fewer hyperbolic | TESTED C1 p = 0.005 (IDEAS 05:30Z); search use UNTESTED → top 8 #7 |
| B14 | budget written on horizons | NONE | cosmology reading | — |
| B15 | subadditive; diminishing returns | PROCESS | beam width has diminishing returns; change the key before buying width | applied: on ac-03305, P2 at W=20k gives 24 while plain H at W=100k gives 27 (IDEAS 07:20Z, 02:45Z) |
| B16 | a direction costs one channel | METHOD | per-class quota: class = canonical pair of cyclic words; ≤ q kept states per class | UNTESTED; `BEAM_QUOTA` being coded (uncommitted, 09:45Z) → top 8 #1 |
| B17 | overflow builds the wall it overflows | METHOD | P2 is class-level and conjugates inherit it, so the W best can be rotations of few classes; count distinct classes per depth, then quota | UNTESTED → top 8 #1 |
| B18 | capped capacity forces full dimension | NONE | Kakeya-type deficit bound | — |
| B19 | wall stiffens as fast as stressed (ratio gate) | NONE | the ratio form is already the start-normalised commutator load | — |
| B20 | some questions are closed to their own instrument | DIAGNOSTIC | (a) memory wall: more budget does not move caps, so change method (applied); (b) where does the beam lose the record path: rank and ties of record-path states at W and 2W | (a) applied; (b) UNTESTED (IDEAS 04:45Z #5); `BEAM_TRACE_FILE` + `optimality/beam_loss.py` being coded (uncommitted, 09:45Z); run first |
| B21 | predictability, visibility, entanglement sum to one | NONE | no AC bearing | — |
| B22 | leakage out of a channel = capacity | METHOD | count non-climbing class-changing exits (cap1, cap2) as P2 tie-break · Test A | TESTED DEAD (Test A: +0.010, +0.003) |
| B23 | bound breaks at any non-Hermiticity | NONE | biorthogonal geometry | — |
| B24 | gaps cancel in the ledger | NONE | perturbation bookkeeping | — |
| B25 | gaps belong to the susceptibility | NONE | perturbation bookkeeping | — |
| B26 | exceptional point needs eigenvector coalescence | NONE | EP test | — |
| B27 | dissipation ≥ path length in the transport metric | NONE | a metric lower bound on moves is the dead invariant-bound class (IDEAS 02:45Z) | — |
| B28 | works for mixed states | NONE | Bures/Uhlmann | — |
| B29 | heat-kernel coefficients recovered | NONE | spectral geometry | — |
| B30 | refraction is kinematics | NONE | wall kinematics | — |
| B31 | change has only one place to go | METHOD | P2 = best total after two multiplications with free rotations; beam key P2 first, H second | TESTED, WIN: ac/sac-03060 28/30 (+1.0), ac-03305/01629 records in A/B (IDEAS 07:20Z, PLAYBOOK win log); no signal at records 46–60 (IDEAS 08:55Z) |
| B32 | two-band case saturates the bound | NONE | band geometry | — |
| B33 | measured Chern number on someone else's data | PROCESS | calibrate scores on paths we did not generate (exact capped paths, training_424) | applied (IDEAS 02:45Z beam-free check) |
| B34 | shape space carries a state-space metric | NONE | three-body geometry | — |
| B35 | phase crosses what amplitude cannot | DIAGNOSTIC | same reading as Plate II; realised by P2 | TESTED via P2 |
| B36 | three mechanisms at one locus | NONE | wall diagnostics | — |
| B37 | a finite count makes it finite | NONE | restates capped search | — |
| B38 | isospectral relaxation (Lax flow) | METHOD | group fixed, functional descends: same as B12 · Test B | TESTED DEAD (Test B) |
| B39 | past the critical angle nothing gets through | DIAGNOSTIC | below a critical cap the start's component excludes (x,y) | TESTED: exact caps (PLAYBOOK); 20 closed components, all disjoint (confident-fermi transport note) |
| B40 | prediction on the resolution floor | NONE | solar data | — |
| B41 | wave born at a defective collision | NONE | EP dynamics | — |
| B42 | interlacing keeps the interior real | NONE | spectral theory | — |
| B43 | last metric choice removed | NONE | Koszul–Vinberg | — |
| B44 | small defective block drives the whole | DIAGNOSTIC | in MS(n,w) the Baumslag–Solitar core YXXyx drives the 2^n growth; reach it first (n-uniform prefix 3,8,2,6,12,4,12^n, IDEAS 05:30Z) | applied; transfer to other w → top 8 #3 |
| B45 | curvature over a flat connection | NONE | band sum rule | — |
| B46 | failure to close is the mechanism | NONE | projection defect | — |
| B47 | same operator rebuilds the choreography | METHOD | uniform level block replayed for every n | TESTED: 9-move level is n-uniform (IDEAS 05:50Z); Codex generator valid for all n at 4·2^n+2−n, 1.5–2× records (IDEAS Codex ABC); other w UNTESTED → top 8 #3 |
| B48 | the seam is a Schur complement | METHOD | eliminate hump states as macro-moves | TESTED DEAD: mined macros 03305 27 = plain (IDEAS 03:15Z); Bob40 0 better / 4 worse / 5 same (IDEAS 09:25Z) |
| B49 | det Hessian = adjoint torsion | NONE | knot conjecture | — |
| B50 | which factor stops the arc | NONE | knot census | — |
| B51 | one comparison: trace in [−2, 2] | DIAGNOSTIC | the same trace test classifies hump exponent transfers (C1) | TESTED (C1, IDEAS 05:30Z) |
| B52 | the endpoint decides, not the size | PROCESS | classify rows by family membership (MS(n,w), AK(3) class), not by start length | applied (`ms_families_by_w`, `AK3_CLASS_ROWS.json`) |
| B53 | two curves, one source | NONE | coloured Jones | — |
| B54 | two ways for the bound to fail | NONE | biorthogonal geometry | — |
| B55 | det g = 0 is its own wall | NONE | geometry locus | — |
| B56 | a curve and a point do not meet | NONE | codimension count | — |
| B57 | zero length, still moving | DIAGNOSTIC | plateau moves (see Plate XIV) | exit-count tie-break TESTED DEAD (Test A) |
| B58 | a collective cone exceeds its parts | METHOD | Stable AC: the stabilised slot adds room. Fast peel uses it; hump-in-slot untested | fast peel TESTED as construction, 2k+3m/k (IDEAS 06:05Z); multi-level peel dead by arithmetic (below); hump-in-slot UNTESTED → top 8 #8 |
| B59 | goal scope ≠ admissible continuation | PROCESS | a witness peak is not a closed cap | applied (IDEAS 00:52Z, 02:30Z) |
| B60 | saturation flags hidden rank-one structure | DIAGNOSTIC | a clean record formula (2^(n+1)+n+11 for YXXyx) flags one uniform construction; slow families (YYXYYxyyX 42, 43, 76, 81, …) flag another | applied (IDEAS 05:45Z) |
| B61 | size and mass cannot co-scale | NONE | units | — |
| B62 | two parameters indistinguishable after control | PROCESS | before stacking triage features (periodicity runs, commutator load), check their partial correlation at matched start length | UNTESTED (cheap) |
| B63 | a rescaling appears only as a running | NONE | units | — |
| B64 | one operator, five names | NONE | factor-of-two bookkeeping | — |
| B65 | two diagnostics, not two views | DIAGNOSTIC | persistence key (P2, class-level) and sensitivity key (H, word-level) are complementary | applied: P2=2 uses both (IDEAS 07:20Z) |
| B66 | the wall is branched (orientation double cover) | DIAGNOSTIC | det of the exponent matrix: inversions flip it, other moves keep it; the SAC (y,x)+[15,15] finish is the other sheet | applied ((y,x) finish, PLAYBOOK) |
| B67 | a record that is a group element (holonomy) | DIAGNOSTIC | a hump returning to its class pair leaves net conjugators; measure them | UNTESTED, low |
| B68 | paired spectrum gives integers | NONE | index theory | — |
| B69 | a gap predicts a rate and picks the route | METHOD | (a) layer-growth rate predicts capped cost; (b) score move blocks by x-mass per move | (a) TESTED, works (IDEAS 02:20Z); (b) UNTESTED → top 8 #2 |
| B70 | two null-space questions | PROCESS | "no path within cap C" ≠ "no path"; "beam miss" ≠ "bound" | applied throughout |
| B71 | distance is blind to orientation | NONE | covered by B66 | — |
| B72 | the gap is a stiffness | NONE | perturbation theory | — |
| B73 | exponent derived, not fitted | NONE | EP scaling | — |
| B74 | a degenerate stratum repels | NONE | refraction invariant | — |
| B75 | the middle of an ordered spectrum cancels | NONE | sign accounting | — |
| B76 | a degenerate point is a count in hiding | NONE | critical-point counts | — |
| B77 | extremal limit is a moving packing record | PROCESS | records move; re-pull the board before targeting | applied (5-minute submit rule) |
| B78 | one contour, any function, no eigenvectors | DIAGNOSTIC | rotation-free class quantities (no representative chosen) are the design of P2 | TESTED via P2 |
| B79 | take the phase when the vector is gone | NONE | discriminant winding | — |
| B80 | the running measured from two sides | PROCESS | predict a number two independent ways before trusting it | applied (probe fit 80M vs run 87M) |
| B81 | transport is flat; the bundle keeps the curvature | METHOD | the 16 mirrors commute with the move set, so cross-row mirror transport | TESTED, works inside cross-row borrowing: ac-03028 tie via mirror 5, 13 SAC ties from x↔y mirrors (IDEAS session 1); start-to-start mirrors gave nothing (IDEAS 00:05Z) |
| B82 | the recessive constant crosses the collision | NONE | three-band asymptotics | — |
| B83 | the frame is part of the instrument | METHOD | Whitehead-minimal frame; primitive-relator finish | frame TESTED weaker than P2 (IDEAS 04:45Z); `BEAM_WH` beam key being coded (uncommitted); finish UNTESTED → top 8 #5 |
| B84 | two sectors say what, one says why | NONE | the sector split is B31's | — |
| B85 | real part of a rank-one form is never definite | NONE | bilinear geometry | — |
| B86 | the wall is the only place a cone can open | DIAGNOSTIC | restates the hump: routes open only above the start length | known (PLAYBOOK hump section) |
| B87 | protected degeneracies quadratic, broken ones conical | NONE | symmetric starts are rare, so mirror dedup of the beam is low value | — |
| B88 | shape space as a crystal | NONE | conical refraction | — |
| B89 | reciprocity breaks at first order | NONE | scattering matrices | — |
| B90 | clock exponent 1 vs ½ | NONE | open-system metric | — |
| B94 | a Lipschitz ledger cannot mark a wall | DIAGNOSTIC | why lower bounds die: any readout moving ≤ c per move (or ≤ log 2 per multiplication) bounds distance only by Δ/c | TESTED as a class: mean bound/record 0.11 (IDEAS 02:45Z) |
| B95 | threshold profile reads the cycle type | METHOD | cycle types of ρ(r0), ρ(r1) in S_n are invariant under conjugation and inversion: a cheap class hash for the quota (as a bound: dead finite-quotient class) | UNTESTED; folded into top 8 #1 |
| B96 | the gap between the rails | NONE | grade H, no maps given; the bound-vs-best bracket is already recorded | — |

## Repo cards (`atlas/cards.json`)

| Card | Gist | Class | AC reading | Status |
|---|---|---|---|---|
| ALG-WEIGHTED-KERNEL | ker JᵀWJ = ker J | NONE | linear algebra | — |
| ALG-FORCING-DUAL | factorisation certifies obstruction | METHOD | certified lower bounds from finite shadows | TESTED DEAD: SL(2,p) bounds 9–11, bound/record 0.11 (IDEAS 02:45Z) |
| ALG-BOUNDARY-DEGREE | Laurent degree budgets | NONE | Fox-degree budgets would be another invariant bound | — |
| GEO-OVERLAP | projector overlap identity | NONE | no AC bearing | — |
| GRAPH-SUBGRAPH-CAPACITY | two-layer capacity obstruction | METHOD | charge r0-moves and r1-moves separately | TESTED DEAD: collapses to ≤ 2 per layer (IDEAS 02:45Z); U1 median same-relator run 2 (IDEAS 05:30Z) |
| OPT-TWO-FREQUENCY | silent-subspace test | NONE | optics | — |
| OBS-PROBE-SPAN | probe reconstruction or invisible perturbation | METHOD | SL(2,p) probe shadows as a guide score | bound TESTED DEAD; guide corr +0.31 (hump +0.24 vs length −0.24), one-row plain-H beam no gain (IDEAS 02:45Z); under P2 UNTESTED → top 8 #6 |
| UPG-FEEDBACK | Schur elimination memory | METHOD | hump elimination as macros | TESTED DEAD (IDEAS 03:15Z, 09:25Z) |
| UPG-GLUING-SIGN | gluing correction ≤ 0 | NONE | sign lesson only | — |
| UPG-GAP-RANK | projector susceptibility | NONE | spectral derivative | — |
| UPG-CURRENCY-GUARDS | winding, signature, eta distinct | PROCESS | keep distinct integer records distinct (AC length, SAC length, finish type) | applied |
| CASCADE-FOUR-RECORDS | four separable records | PROCESS | log support, frontier motion, re-entry and component identity separately | applied (confident-fermi transport note) |
| DIO-SECTION-INTEGRAL | integer points on a section | NONE | Diophantine | — |
| DIO-TRACE-BOUNDARY | omitted domain point | NONE | finite fields | — |
| DIO-SEARCH-LIMITS | ranking ≠ validation | PROCESS | freeze candidates, hold out rows, then validate | applied (Test B row-held-out folds) |
| HORIZON-METRIC-WALL | coordinate wall ≠ barrier | NONE | covered by B59/B70 | — |
| OBS-INTERIOR-AMBIGUITY | same exterior, different interior | DIAGNOSTIC | equal component sizes ≠ same component | TESTED (confident-fermi: every same-size pair disjoint) |
| DISPLAY-EYE-MIXER | replayable trace recipes | PROCESS | log exact env and flags per run (BEAM_BAL needs BEAM_H=1) | applied (PLAYBOOK flag note) |

Card-set appendices (not cards, not counted): `ATLAS_CALCULUS.md`, on contextual equivalence and Schur elimination with retained
weight. It is PROCESS: an eliminated macro must carry its true cost, as ours did (dead as B48). `SOFIC_SCOPE.md`, on filling
loads, is NONE: area-type bounds are log-scale in path length.

## Dead by arithmetic (this ledger): a multi-level Stable AC block peel cannot rescue the naive build

Atlas B16/B18 suggest using the extra generators as "channels", as in a positional numeral: blocks of blocks.
Consider any peel of y·X^m that builds a block relator letter by letter (k₁ moves) and spends at least 1 move per block swap.
It costs at least k₁ + m/k₁ ≥ 2√m moves. The actual fast peel is 2k + 3m/k (IDEAS 06:05Z). Take YXyXyx: SAC record = AC record + 2,
and the naive build is 2^(n+1)+17. A beat then needs peel ≤ SAC − 1 − build: n=6: 160−1−145 = **14** < 2√63 ≈ 16;
n=8: 549−1−529 = **19** < 32; n=10: 2090−1−2065 = **24** < 64. So more peel levels cannot turn the naive build into a beat.
The Stable AC lane still needs a build ≤ ~1.85·2^n, or doubling inside the stabilised slots (blocked so far, IDEAS 07:58Z).
This assumes no doubling. It is arithmetic, not a search.

## Top 8 UNTESTED methods, ranked by expected value for points soon

Every kill condition below is fixed now. "K0" = (P2 cut 8, P1m, raw), with climbing top-3 0.413 and all-steps top-3 0.593 on the 59 hump paths (Test A data).

1. **Per-class beam quota under P2** (Plate VII, B16, B17; B95 as a cheap hash). *Why first:* P2 lanes are where the ties
   come from now. P2 is class-level and inherited by all 8 conjugations and 2 inversions, and the record child ties the best
   P2 on 62% of steps. So the W kept states can be many rotations of a few classes. The change is small, and the lead is
   already coding it as `BEAM_QUOTA` (uncommitted at 09:45Z): at most q survivors per class, class = the canonical cyclic pair.
   *Cheapest test:* one instrumented P2=2 run (W = 20k) on ac-00145 and ac-06045 that prints distinct classes among kept states
   per depth. Then a matched A/B (P2=2 vs P2=2 + quota) on the six A/B rows of IDEAS 07:20Z plus 10 recent `p2a/p2b` misses.
   *Kill:* distinct classes ≥ 0.5·W at every depth ≥ 5 (no crowding); or in the A/B, no row shorter and ≥ 1 row longer; or wall time > 2× plain P2.
2. **Route by rate for the doubling build** (Plate XV, B69). *Why:* 68 doubling-chain rows are held by ≤ 2 teams, plus the Stable AC
   beat lane (~30 rows). Everything hinges on building at ~1 new x per move (ours 1/3–1/2). Session 1's exact n=3 path already has
   a rate-1 pair (3, 6) that runs out of leading X's at n=4 (IDEAS 06:10Z). *Compute:* from 12 level states on verified MS(n, YXXyx)
   and MS(n, YXyXyx) paths (n = 3..5: session 1's exact 28-move n=3, Codex generator states for n = 4, 5), enumerate every rank-2 block
   of 2–4 moves (no immediate inverse pairs). Iterate each block while it lengthens the longest x-run, and score new x's per move.
   Pure Python on existing states, < 10 min. *Kill:* no block from any n ≥ 4 state sustains ≥ 0.9 x per move for ≥ 8 iterations.
   Try rank 3 (moves on a stabilised slot) only if rank 2 dies.
3. **n-uniform prefix transfer across MS(n, w)** (B47, B44, B60, B52). *Why:* unsolved rows pay 1.0 for any path, and 1,977 of
   2,672 unsolved rows are MS(n,w). There are 106 second words w where some n is solved and others are not (e.g. YXYxYx: n=2 at 24,
   n = 3..10 unsolved). The first target is the old War Room's R_n = MS(n, x²yx⁻¹y): n=2 is solved (ac-00104, 21) and
   n = 3..10 are 21 rows unsolved by every team, 1 AC + 1 SAC point each (IDEAS 09:30Z, remote). The YXXyx level block was
   found by exactly this replay (IDEAS 05:50Z). *Compute:* replay each
   `training_424` path (all MS) and each of our MS-row paths on MS(n+1, w) with the official kernel. Record the longest prefix along
   which the n+1 state equals the n state with maximal y-runs lengthened by one (a run-shifted twin). No search; seconds.
   *Kill:* fewer than 3 second words w have an n-uniform prefix covering ≥ 50% of a solved path. If ≥ 3 do, the next step is a
   P2 beam from the prefix end on the unsolved n (a lane job).
4. **P3: the next rung of the lifting ladder** (Plate XII, B31). *Why:* P2 shows no signal at records 46–60 (IDEAS 08:55Z) and times out on
   ac-00145. P2 cut 8 still climbs on some humps (mean 0.84, max 11 on the 56-path set, IDEAS 05:30Z). *Compute:* P3 cut 8 = min P1 over the 8 best level-2 states of each of
   the 8 best level-1 states (about 8× P2 cost). *Cheapest test:* climb and sibling rank on the 59 hump paths, reusing
   `p2_hump_test.py` functions; < 10 min Python. *Kill:* P3 mean climb > 0.7 × P2-cut-8 mean climb on the same 59 paths, or climbing top-3 of (P3, P1m, raw) < K0 + 0.05.
5. **Primitive-relator finish target** (Plate XVIII, B83; Lemma A of acwindow-lean). *Why:* on unsolved rows any path scores,
   and "one relator primitive" is a finish region far larger than T9. The constructive proof builds the path. *Compute:* Whitehead
   check in F2 (apply the 12 type-2 Whitehead automorphisms while the cyclic length drops; primitive iff it reaches length 1),
   after the O(L) one-sign letter pre-filter. *Cheapest test:* on the 546 verified paths, find where a relator first becomes primitive
   and how many moves remain. Then run a 100-row P2 screen (W = 2k, depth 60) on non-MS, non-AK(3) unsolved rows with "primitive
   relator" as an extra finish target (path builder only after a hit). *Kill:* median moves remaining ≤ 9 (T9 already covers it)
   **and** 0 screen hits. Prior screen: 0 of 2,672 unsolved rows within 2 moves (IDEAS 05:00Z).
6. **SL(2,p) shadow as the tie-break under P2** (OBS-PROBE-SPAN). *Why:* the shadow is the one guide feature with real hump
   signal (+0.24 where length is −0.24), and it is the kind of information Test B's features lacked. It is already wired:
   `BEAM_P2=2 BEAM_SHADOW=w` puts it next to H after P2. *Cheapest test:* offline sibling rank with key (P2, shadow sum over
   4 probes, P1m, raw) on the 59 hump paths, using the `shadow_probe_export.py` probes. *Kill:* same as Test A (climbing top-3 < K0 + 0.05
   or all-steps top-3 < K0 − 0.02). Beam A/B only if it survives.
7. **Prefer finite-order exponent transfers inside humps** (B13, B51; the C1 result). *Compute:* while above the start length,
   T = M_child · M_leave⁻¹ (exponent-sum matrices); rank ±I < finite < parabolic < hyperbolic as a key after P2.
   Only multiplication children differ. *Cheapest test:* sibling rank on in-hump steps of the 59 paths. *Kill:* in-hump top-3 < K0 + 0.05.
   Low prior: C1's mix difference is modest (TV 0.155).
8. **Stable AC: put the hump in the stabilised slot** (B58). *Why:* the one atlas idea specific to Stable AC's extra generators
   beyond the fast peel. If the transient growth can live in the slot g·w while |r0|+|r1| stays low, a rank-3 beam that does not
   charge the slot would find hump rows' SAC paths. *Cheapest test:* one exact rank-3 capped run (`sac_rank3.c`) on ac-03305
   (start 24, SAC record 24; rank 2 needs cap 37), capping |r0|+|r1| at 30 and the slot at 16. *Kill:* no SAC ≤ 24 path under that cap.
   (This is an exact run, for a lane, not for this ledger.)

**Run first (diagnostics, not methods).** (i) B20 / Plate XI: *where the P2 beam loses the record path.* On ac-05558 (P2 26 vs
record 24) and ac-07435 (28 vs 26), whose exact record paths are known, log at each depth whether the record-path state is kept,
and if not, its rank and tie count at W and 2W. Lost among P2 ties points to #1; rank ≫ W points to #4 or #6; saved by 2W means width alone.
(ii) B62: partial correlation of the periodicity eye and commutator load at matched start length, before combining them in triage.

## Appendix: test script (Test A and Test B)

<details><summary><code>p2_tiebreak_ranker_test.py</code>: run with <code>nice -n 10 python3 p2_tiebreak_ranker_test.py OUT.json</code>
from any directory. It imports <code>research/acc/optimality/p2_hump_test.py</code> and needs the SAIR clone at
<code>p2_hump_test.SAIR_DEFAULT</code>.</summary>

```python
#!/usr/bin/env python3
"""Atlas ledger tests on existing verified paths (no beam, no exact search), 2026-09-28.

Test A (atlas B6 / B22 / B57 / Plate XIV): break P2 plateaus by exit multiplicity.
  For each child state c: level-1 list = the 8 best distinct states after one multiplication
  (same cut as BEAM_P2CUT=8).  P2 = min P1 over that list (as in p2_hump_test.p2, cyc variant).
    mult = number of list entries whose P1 equals P2   (how many ways to realise the best 2-step value)
    cap1 = number of list entries with core total <= core total of c (non-climbing class exits)
    cap2 = number of list entries with P1 <= core total of c (two-step non-climbing exits)
  Keys compared by sibling rank of the record move (mid-rank ties, as in p2_hump_test):
    K0 = (P2, P1m, raw)                     baseline = current best offline proxy (top3 climbing 0.407)
    K1 = (P2, -mult, P1m, raw)   K2 = (P2, -cap1, P1m, raw)   K3 = (P2, -cap2, P1m, raw)
  KILL (fixed before the run): a key survives only if top-3 on climbing steps >= K0 + 0.05 AND
  top-3 on all hump-path steps >= K0 - 0.02.

Test B (atlas B12 / B38: a descent functional that record paths follow): pairwise logistic ranker on
  state features [raw, P0cyc, P1, P1m, P2, mult, cap1, cap2, min, max, |r0|-|r1| abs], trained on the
  sibling sets of training rows, scored on held-out rows (2-fold split by row, 5 random splits).
  KILL (fixed before the run): survives only if mean held-out top-3 on climbing steps >= K0 + 0.05 on
  the same held-out rows AND mean held-out all-steps top-3 >= K0 - 0.02.

Data: the at-record hump paths of p2_hump_test (climb >= 6), collected and replayed with the official
verifier exactly as there.  usage: nice -n 10 python3 p2_tiebreak_ranker_test.py OUT.json
"""
import gzip, json, math, os, random, sys, time

REPO = '/home/user/operator-first'
sys.path.insert(0, os.path.join(REPO, 'research/acc/optimality'))
import p2_hump_test as P  # noqa: E402

SAT = 999


def p2_detail(r0, r1, cut=8, memo={}):
    A, B = P.cycred_s(P.enc(r0)), P.cycred_s(P.enc(r1))
    ca, cb = P.canon(A), P.canon(B)
    key = (ca, cb) if ca <= cb else (cb, ca)
    r = memo.get(key)
    if r is not None:
        return r
    cur = len(A) + len(B)
    if not A or not B:
        r = (SAT, 0, 0, 0)
    else:
        cl, _ = P.level1(A, B, cut)
        vals = [P.p1_cores(x, y)[0] for (_, _, x, y) in cl]
        if not vals:
            r = (SAT, 0, 0, 0)
        else:
            p2v = min(vals)
            r = (p2v, sum(1 for v in vals if v == p2v), sum(1 for (ct, _, _, _) in cl if ct <= cur),
                 sum(1 for v in vals if v <= cur))
    memo[key] = r
    return r


FEATS = ('raw', 'P0cyc', 'P1', 'P1m', 'P2', 'mult', 'cap1', 'cap2', 'mn', 'mx', 'bal')


def feats(s):
    p2v, mult, cap1, cap2 = p2_detail(s[0], s[1])
    a, b = len(s[0]), len(s[1])
    return {'raw': a + b, 'P0cyc': len(P.cycred_s(P.enc(s[0]))) + len(P.cycred_s(P.enc(s[1]))),
            'P1': P.p1(*s)[0], 'P1m': P.p1m(*s), 'P2': p2v, 'mult': mult, 'cap1': cap1, 'cap2': cap2,
            'mn': min(a, b), 'mx': max(a, b), 'bal': abs(a - b)}


def mid_rank(keys, idx):
    v = keys[idx]
    better = sum(1 for x in keys if x < v)
    ties = sum(1 for x in keys if x == v) - 1
    return 1 + better + ties / 2.0


KEYS = {
    'K0_P2>P1m>raw': lambda f: (f['P2'], f['P1m'], f['raw']),
    'K1_P2>-mult>P1m>raw': lambda f: (f['P2'], -f['mult'], f['P1m'], f['raw']),
    'K2_P2>-cap1>P1m>raw': lambda f: (f['P2'], -f['cap1'], f['P1m'], f['raw']),
    'K3_P2>-cap2>P1m>raw': lambda f: (f['P2'], -f['cap2'], f['P1m'], f['raw']),
    'raw': lambda f: (f['raw'],),
}


def summary(steps, rankcol):
    def s(sel):
        if not sel:
            return {'n': 0}
        rs = [r[rankcol] for r in sel]
        return {'n': len(rs), 'mean_rank': round(sum(rs) / len(rs), 3),
                'top3': round(sum(1 for x in rs if x <= 3) / len(rs), 3)}
    return {'all_steps': s(steps), 'climbing': s([r for r in steps if r['climb']]),
            'climbing_mult': s([r for r in steps if r['climb'] and 2 <= r['move'] <= 5])}


def train_logistic(steps, mu, sd, iters=150, lr=0.5, l2=1e-3):
    """Pairwise logistic: record child beats every other sibling. Features standardised."""
    pairs = []
    for r in steps:
        fm = r['F'][r['move']]
        for j, fj in enumerate(r['F']):
            if j == r['move']:
                continue
            d = [((fm[k] - fj[k]) / sd[i]) for i, k in enumerate(FEATS)]
            if any(abs(x) > 0 for x in d):
                pairs.append(d)
    w = [0.0] * len(FEATS)
    n = len(pairs)
    for _ in range(iters):
        g = [0.0] * len(FEATS)
        for d in pairs:
            z = -sum(wi * di for wi, di in zip(w, d))  # want score(record) < score(other): lower is better
            # label: record should have LOWER score; margin m = -(w.d); loss = log(1+exp(-m))
            m = z
            p = 1.0 / (1.0 + math.exp(min(m, 50.0)))
            for i in range(len(g)):
                g[i] += p * d[i]  # d loss / d w = -p * (-d) = p*d
        w = [wi - lr * (gi / n + l2 * wi) for wi, gi in zip(w, g)]
    return w, n


def main():
    out_path = sys.argv[1]
    T0 = time.time()
    official = P.load_official(P.SAIR_DEFAULT)
    man = {c['challenge_id']: c['initial_relators'] for c in json.load(open(
        os.path.join(P.SAIR_DEFAULT, 'competition/tools/verifier/data/manifest.json')))['challenges']}
    board = {c['challengeId']: c['currentBestLength'] for c in json.load(gzip.open(P.BOARD))['data']['items']}
    rows_all, collection, bad = P.collect_rows(official, man, board)
    at_rec = [p for p in rows_all if p['at_record']]
    humps = [p for p in at_rec if max(p['raw']) - p['raw'][0] >= 6]
    print('collected', collection['rows_verified'], 'at record', len(at_rec), 'hump', len(humps),
          round(time.time() - T0, 1), flush=True)
    steps = []
    for i, p in enumerate(humps):
        for t, m in enumerate(p['moves']):
            s = p['states'][t]
            kids = [P.apply_move(s, j) for j in range(14)]
            F = [feats(c) for c in kids]
            steps.append({'row': p['row'], 't': t, 'move': m, 'climb': F[m]['raw'] > P.tot(s), 'F': F})
        if i % 10 == 0:
            print('  feats', i, p['row'], round(time.time() - T0, 1), flush=True)
    # Test A
    for nm, kf in KEYS.items():
        for r in steps:
            ks = [kf(f) for f in r['F']]
            r['rank_' + nm] = mid_rank(ks, r['move'])
    testA = {nm: summary(steps, 'rank_' + nm) for nm in KEYS}
    base = testA['K0_P2>P1m>raw']
    verdictA = {}
    for nm in ('K1_P2>-mult>P1m>raw', 'K2_P2>-cap1>P1m>raw', 'K3_P2>-cap2>P1m>raw'):
        d_cl = testA[nm]['climbing']['top3'] - base['climbing']['top3']
        d_all = testA[nm]['all_steps']['top3'] - base['all_steps']['top3']
        verdictA[nm] = {'d_top3_climbing': round(d_cl, 3), 'd_top3_all': round(d_all, 3),
                        'survives': d_cl >= 0.05 and d_all >= -0.02}
    # how often is P2 tied between the record child and its best-ranked sibling (plateau)?
    tie = 0
    for r in steps:
        pm = r['F'][r['move']]['P2']
        if sum(1 for f in r['F'] if f['P2'] == pm) > 1 and min(f['P2'] for f in r['F']) == pm:
            tie += 1
    print('testA', json.dumps(verdictA), flush=True)
    # Test B
    rows = sorted({r['row'] for r in steps})
    allf = [f for r in steps for f in r['F']]
    mu = [sum(f[k] for f in allf) / len(allf) for k in FEATS]
    sd = [max(1e-9, math.sqrt(sum((f[k] - mu[i]) ** 2 for f in allf) / len(allf))) for i, k in enumerate(FEATS)]
    splits = []
    for seed in range(5):
        rng = random.Random(1000 + seed)
        rr = rows[:]
        rng.shuffle(rr)
        half = set(rr[:len(rr) // 2])
        for fold in (0, 1):
            train = [r for r in steps if (r['row'] in half) == (fold == 0)]
            test = [r for r in steps if (r['row'] in half) != (fold == 0)]
            w, npairs = train_logistic(train, mu, sd)
            for r in test:
                ks = [(sum(wi * (f[k] - mu[i]) / sd[i] for i, (wi, k) in enumerate(zip(w, FEATS))), f['raw'])
                      for f in r['F']]
                r['rank_learn'] = mid_rank(ks, r['move'])
            sl, sb = summary(test, 'rank_learn'), summary(test, 'rank_K0_P2>P1m>raw')
            splits.append({'seed': seed, 'fold': fold, 'train_steps': len(train), 'pairs': npairs,
                           'weights': {k: round(wi, 3) for k, wi in zip(FEATS, w)},
                           'learn': sl, 'K0': sb})
            print('  split', seed, fold, 'learn top3 climb', sl['climbing']['top3'], 'K0', sb['climbing']['top3'],
                  'all', sl['all_steps']['top3'], sb['all_steps']['top3'], round(time.time() - T0, 1), flush=True)

    def avg(key, part):
        return round(sum(s[key][part]['top3'] for s in splits) / len(splits), 3)
    verdictB = {'learn_top3_climbing': avg('learn', 'climbing'), 'K0_top3_climbing': avg('K0', 'climbing'),
                'learn_top3_all': avg('learn', 'all_steps'), 'K0_top3_all': avg('K0', 'all_steps')}
    verdictB['survives'] = (verdictB['learn_top3_climbing'] >= verdictB['K0_top3_climbing'] + 0.05 and
                            verdictB['learn_top3_all'] >= verdictB['K0_top3_all'] - 0.02)
    out = {'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'doc': __doc__,
           'collection': collection, 'hump_paths': len(humps), 'steps': len(steps),
           'climbing_steps': sum(1 for r in steps if r['climb']),
           'record_child_tied_on_P2_with_a_sibling_at_min': tie,
           'testA': testA, 'verdictA': verdictA, 'testB_splits': splits, 'verdictB': verdictB,
           'wall_s': round(time.time() - T0, 1)}
    json.dump(out, open(out_path, 'w'), indent=1)
    print('verdictA', json.dumps(verdictA))
    print('verdictB', json.dumps(verdictB))
    print('wall', out['wall_s'])


if __name__ == '__main__':
    main()
```
</details>
