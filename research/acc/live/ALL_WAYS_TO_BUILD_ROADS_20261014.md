# Every way we know to get a road: what we have, what is broken, what we have never tried (14 Oct 2026)

Status words:
- DONE (works, run to a fixpoint);
- RAN (tried, no gain, with scope);
- BROKEN (did not run as we thought);
- NEW (never tried).

## A. Splice: combine roads we already hold
| Way | Tool | Status |
|---|---|---|
| Overlap splice (two roads pass within 2 moves) | `tools/acc/overlap_splice.py` | DONE |
| Class splice, orientation splice | Git's tools | DONE |
| Road DP: exact shortcuts between any two states on a road | `tools/acc/ops/` (session 2) | DONE. It gave our 00071 tie |
| Tail meet: exact 13-move finish from every state, to (x,y) and (y,x) | partner, `orows/tailmeet.py` | DONE on 27 rows, 0 gains |
| Foreign meet: borrow another row's finish through a shared state | `upgh/foreign_meet.py`, partner fm2 | DONE (9 shorter, 0 ties) |
| Global webs: height, Stable, recognition, twist | `upgh/height_web.py`, `stable_web.py`, `recognition_web.py`, `twist_web.py` | DONE. Our best tool (31 ties + 1 beat). Moves only when NEW roads arrive |

## B. Extend / transfer: move a road to another row
| Way | Tool | Status |
|---|---|---|
| 16 symmetries, twin rows | `twin_lookup.py`, `crossrow.py` | DONE |
| Nielsen twist (automorphism of F2), exact transfer (P6) | `twist_web.py` | DONE |
| Join onto a known trajectory (multi-target bidirectional) | `ladder_law/join_bidi.c` | RAN on the doubling ladders (+4 over the k1 records). Not run cross-ladder |
| Ladder frame maps and frame finishes | `ladder_rows.py` | DONE (XXYxy) |

## C. Search: find a new body
| Way | Tool | Status |
|---|---|---|
| Beam: H, P2, DUAL two eyes, BAL, NOISE/SEED, CLIMB, MACROS, C16 finish | `optimality/acc_beam.c` | **BROKEN 6-14 Oct on the container.** The cached binary ignored P2/DUAL/ELITE/NOISE/SEED/CLIMB. Fixed 14 Oct 02:20Z. Re-running: the real engine now finds 00669 at 45 (the plain beam found 64) and 03975 at 50 (plain: none) |
| Exact capped BFS, rising caps | `acc_capped.c` (+ Bob's disk-backed capbfs8/9) | DONE; certificates in `catalog/` |
| Meet in the middle, capped forward and backward balls | `acc_opt` / partner MITM | DONE (scoped misses) |
| Mid-restart: beam from every state of our road | `mr_lane.py` | RAN, but on the plain binary since 6 Oct, so redo the important rows |
| Best-first, priority = length + w·depth (P000011) | `acc_bestfirst.c` | RAN, w = 8/12/16, 60M nodes: nothing <= record on 00009 / 00018 |
| **Substitution supermoves**: search over cyclic words, splicing one relator into the other wherever letters cancel; one action = many elementary moves; ~1600x more efficient greedy search | Caltech AC-SolverX (ICML 2026, `github.com/Math-AI-Caltech/acsolverx`) | **NEW.** We never searched in cyclic-word space. Our beams pay for every rotation inside the search |
| Learned policy/value (PPO + Dual-Ring Transformer, solves 610/1190 MS; 100+ previously open MS rows) | AC-SolverX `ppo_checkpoints/610model` (weights and stored solve paths) | **NEW.** Not used. Its stored paths may convert to roads |
| Datasets as donors: AC-19 (exhaustive enumeration), AC-1M (automorphism game) | AC-SolverX `data/` | PARTLY: AC-1M was matched to unsolved rows on 1 Oct, AC-19 never |

## D. Shorten: polish a road
| Way | Tool | Status |
|---|---|---|
| Window-14 exact replacement, fixpoint, commute cleanup | `acc_window.c`, `fixpoint_shorten.py`, `commute_clean.py` | DONE (gave the 2 beat pairs on constructed roads) |
| Universal move identities (P7) | Kernel | DONE |
| Stable via (y,x) + [15,15]; yx_shortcut | `yx_shortcut.py`, `stable_web.py` | DONE (299 completed misses listed) |

## E. Construct: mathematics
| Way | Tool | Status |
|---|---|---|
| BS doubling P1 (2^(n+1)), (n+1)-block P2, step-2 finA2 | `bs_doubling*.py`, `fable_build.py`, `loop_macro.py` | DONE (now beaten by memcon) |
| **memcon's construction**: records ≈ 2^n + 10·2^(n/2) on 5 ladders, partly on 2 more | — | **NEW and OPEN.** Exponent-sum bound: about 2^n multiplications are unavoidable, so their roads have almost no rotations. Matches the "plan in cyclic space, pay rotations cleverly" idea in C |

## F. Reverse-engineer from data
| Way | Status |
|---|---|
| Ladder law (affine, then 2^(n+1)+c, then memcon's 2^n + c·2^(n/2)); top-team holdings; record histories | DONE today (`TOP_TEAMS_METHODS_BESTGUESS_20261014T0030Z.md`) |
| Isospectral families (which row families moved by the same law) | DONE today: only the 5 + 2 MS ladders |
| Board-map clustering (t-SNE/UMAP) | DONE 6 Oct: solved rows cluster, 4x enrichment |

## G. Guess / random
| Way | Status |
|---|---|
| Noisy seeded beams, new lineages | **BROKEN on the container** (seeds were ignored). Session 1's seeds 13-19 ran elsewhere and worked |
| Random restarts, climb-then-collapse (Bob) | RAN, scoped |

## The obvious things we were missing (found today)
1. **The beam binary.** A week of "dual-P2 / seeded" lanes on the container were plain beams. Re-run the high-value rows with the real engine.
2. **Cyclic-space planning** (substitution supermoves) with cheapest-rotation realization. Never built. It is the best match for memcon's "almost no rotations" signature.
3. **Public learned solvers and data** (AC-SolverX weights, stored solve paths, AC-19). Not mined.
4. The ACC Drive hub has not been re-inventoried since 1 Oct (see `HUB_INVENTORY_20261014.md` once written).

## Addendum 03:05Z: other people's GitHubs, read (read only, never run)

Searched GitHub for "Andrews-Curtis" (25 repos; the SAIR-relevant ones are below). Paper hosts (arxiv, easychair, sciencedirect) are blocked by this environment's network policy; GitHub and Drive work.

| Repo | What it does | Use to us |
|---|---|---|
| Math-AI-Caltech/acsolverx (ICML 2026, "Two-Hump") | PPO transformer over **substitution supermoves**: rotate both relators, multiply, store in least rotation. Beam W 1024. Data: 1190MS benchmark, AC-19, AC-1M (CC BY 4.0). | The 610model's stored paths index the **AC-19 training set**, not SAIR rows. Running its beam on 1190MS needs JAX. Probably the method of team "AC-Solver =D" (#2). |
| ElliotSteffen/ACSolverES | Greedy search with substitutions plus **automorphism change of variables (COV)**: apply a Nielsen automorphism (e.g. x -> x y) to both relators mid-search. Solves all 640 of a GS benchmark. | **NEW to us.** Multiplications and inversions transfer one for one under an automorphism. A rotation by a letter becomes a conjugation by its image, so it costs that image's length. The end state (phi^-1(x), phi^-1(y)) needs a short Nielsen finish. Not tried anywhere in our lanes. |
| nahomar/andrews-curtis-solver (team nahom, 10th AC / 9th Stable) | C++: ball16/17 lookup, macro beam, power macros, splice, rebeam, window shortcuts, GS class-distance oracle, lineage-cap beam; RL guides. | Same family as ours. Their log agrees with our verdicts: windows r5/r6 give **no gain** on near-misses; **width saturates** (W 60k and W 100k gave 0 beats); noise is useless at small budget. Lineage-cap diversity and GS-oracle settings help only for **route diversity**. "Local polishing cannot close a 2.5x global gap; needs a different route." |
| proof_track/ms_lisitsa_ak3_20260928 (ours, 28 Sep) + Lisitsa 2024/2025 | Lisitsa's MS_n(w*) family **is our XXYxy ladder** (second relator ABabA = XYxyX ~ XXYxy). Archive roads n=3..9, with the second relator fixed throughout. | Lengths about 2^(n+4) (MS(9) 8,634 vs record 710), so not memcon's source. One idea is new: **fixed-second-relator search** (Lisitsa's Conjecture 3). It is a one-relator search: state = r0 only, moves 0, 2, 3, 6-9. |
| Robby955/ac-square-divisibility | Explicit constructions for G(p,s) = (u^2 y^-(2s+1), u y^p u y^-s u^-1 y^-p), Lean + SAIR-id paths. | Only G(1,1) is a SAIR row (ac/sac-04359, 08327, 09594, up to symmetry). No lever. |
| ph4ge/ac-detour-width | Lean: detour width (peak length) is independent of graph distance. | Confirms roads must climb; no roads. |
| Amey-Thakur, alejandrozarco (ms14), joe-carr-data (certificates), HkHk2Prod/AlphaAC | Baseline search / length-14 certificates / AlphaZero prototype. | No record-level roads. |
| rosie-0525/acc-challenge (team Catsitter) | Listed by search, but not reachable from here (add_repo: not found). | Unknown. |

**"New OpenAI ideas"**: a web search turned up no public OpenAI or GPT-based ACC work. The one LLM study (OpenReview) finds LLMs rarely produce correct paths. Top teams' gains look like **constructions + search in a different space** (substitution / change of variables), not chat-model path generation.

**What we still have not tried, from this read:**
1. COV frames: search phi(start) for a few elementary Nielsen automorphisms phi, then map back. The cost changes only through conjugations and the finish.
2. Fixed-second-relator one-relator search on the five exponential ladders (the r1 = ABabA-type rows).
3. Lineage-cap beam (nahomar's lc60p8 / lc20p4) for route diversity on gap-1 rows; our acc_beam has DIV but no lineage cap.
