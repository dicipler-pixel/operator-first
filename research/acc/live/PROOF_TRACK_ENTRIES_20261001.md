# Proof Track entries in the Mad Hatters hub (read 1 Oct 2026, ~03:05Z)

The owner placed 10 Proof Track entries in the Drive hub (folder "Mad Hatters ACC Shared Hub"). All of them are public (Proof Track submissions publish to the SAIR Contributor Network).
Two of them are ours, P000009 and P000010; both name the "Mad Hatters set". Both also mention a sibling note "prepared with Claude", but none is in the hub.
The gaps in numbering (P000003–P000006) are not in the hub.

| Entry | Ours? | What it establishes | Use for our Discovery work |
|---|---|---|---|
| P000001 Local-search stagnation | no | 369 of 2,000 rows made no length progress under a 64-wide, 5M-node beam; 97.8% of them were unsolved. | Cheap triage signal only. |
| P000002 Divisibility subfamily G(p,s) | no | Lean-proved explicit AC constructions for G(p,s) = (u²y^-(2s+1), u y^p u y^-s u^-1 y^-p) when p divides s or s+1. Python exporter; 50-case replay. | Check whether any unsolved pool row is G(p,s). If one is, the construction gives a first solve. Not yet checked. |
| P000007 Kernel-checked Stable certificates (ibrahimmian36/evocatus) | no | Lean checker for sac-r8-v1 with soundness proofs; the Stable conjecture end may be empty or permuted; Lemma 11 / Remark 17 formalized; AK(3) = sac-00399 has no public stable certificate. | None directly. sac-00399 (AK(3)) stays unsolved; their checker would turn any stable certificate into a kernel theorem. |
| P000008 Detour width and cycle structure (ph4ge) | no | Detour width is not a function of graph distance (witnesses ⟨x^-1,y⟩, ⟨xy,y⟩). Lean. | Background; our P000009/P000010 build on it. |
| **P000009 Detour width on two AC graphs** | **yes (Grok-prepared)** | Separates AC_word (official AC.lean, any conjugator) from AC_letter (scored verifier). On AC_word, T_N = ⟨y^N x y^-N, y⟩ has distance 1 and width 2N+2 (Lean). On AC_letter, width ≤ 2^(distance+1) (prose). Lean file `lean/acc/ACDetour.lean` @ 78849f53 in dicipler-pixel/acwindow-lean. | Framework only. |
| **P000010 Certified length wells** | **yes (GPT-prepared)** | Cap-exit theorems (Lean, `lean/acc/ACCWell.lean` @ 78849f53). Certified: H*(ac-02842) ≥ 22 (cap-21 component, 219,042,976 states, T absent). H*(ac-00002) ≥ 36. ac-00015: a forced climb to ≥31 from its length-20 state. | These rows need a high climb; do not spend short-window search on them. |
| P000011 Length as priority, not constraint | no | Hard length caps are the dominant search error. The priority f = L + 12·d solves 10/10 short rows at the exact optimum. Decision-mode IDA*: **ac-07351 has no AC path ≤ 24 within word cap 42** (exhausted). The abelianisation test is empty on the pool. | Use w≈12 priority for short-row ties. ac-07351 ≤ 24 is out (within cap 42). ac-06403 is our never-send row (the owner handles it); P000011 left it undecided. |
| P000012 ac-02089 ≡ C6 (alejandrozarco/andrews-curtis-ms14) | no | Certificate: ac-02089 is AC-equivalent to the residual class C6 (1,066 moves). Capped closures L ≤ 32 contain neither the trivial pair nor AK(3), so **ac-02089 and ac-08126 need peak ≥ 33** in their model. | Lower priority as cheap first solves: in their capped model every route peaks ≥ 33. This is a bounded exclusion, not an impossibility (Astra, 03:14Z). |
| P000013 Baumslag–Solitar doubling in MS(n,w*) | no | Explicit finish fin2(m) for (Y x^m y y X, x x Y X y), proved for all m ≥ 2. Constant-2 construction 2^(n+1)+O(n) (measured). Exponent-matrix lower bound 2M+3 multiplications through the expanded block. Step-2 variant finA2; record 111 on ac-05698. **Open: an m+O(1) finish would give ≈1.5·2^n, below every current record for large n.** | **Acted on: see below.** |
| P000014 "Tri 13Over5" ac_solver.py | no | The Contributor Network solver we already flagged: 5 of 6 swap suffixes are wrong and the code has bugs. | Do not use (see NOTE_contributor_network_solver_check_*). |

## Acted on: BS-doubling roads (credit: P000013)

`tools/acc/upgh/bs_doubling.py` is our own implementation of the published construction. It builds the rewrite loop, stops one level early and applies their fin2(m). Each road is transferred to each board row by symmetry with a paid prefix and replayed on the pinned official core.

| Row | n | AC record (k) | Our road before | BS-doubling road |
|---|---|---|---|---|
| ac-01784 | 4 | 48 (4) | 56 | 59 |
| ac-04042 | 4 | 50 (4) | 57 | 62 |
| ac-01950 | 5 | 80 (3) | 107 | 100 |
| ac-05586 | 5 | 83 (3) | 117 | 105 |
| ac-02033 | 6 | 145 (2) | 202 | 171 |
| ac-06018 | 6 | 149 (1) | 213 | 177 |
| ac-00676 | 7 | 278 (1) | 410 | 315 |
| ac-06796 | 7 | 275 (3) | 398 | 308 |
| ac-03079 | 8 | 532 (2) | 781 | 575 |
| ac-03773 | 8 | 538 (1) | 794 | 583 |
| ac-03984 | 9 | 1051 (1) | 1567 | 1109 |
| ac-06727 | 9 | 1046 (3) | 1553 | 1100 |
| ac-00106 | 10 | 2071 (2) | 3088 | 2139 |
| ac-01523 | 10 | 2079 (1) | 3103 | 2149 |

No ties yet. Two kinds of overhead remain:
1. **Level changes.** My conjugation-only rotation pays about 2(n−L) moves per level, so the total grows with n². P000013 reports O(n).
2. **Row frame.** The symmetry transfer costs 6–15 moves for prefix and finish.

**Fable task (research, direct points if it works):**
- (a) A level change in O(1) moves.
- (b) The open m+O(1) finish from (Y x^m y y X, x x Y X y). It would beat every MS(n,w*) record from n = 7 up: 14 rows × 2 tracks, 6 of them held at k = 1.

## Update 05:24Z: Fable t00312, the general step

**(1) Level change, solved in this scheme.**
- Alternate the orientations:
  - one orientation keeps r0 = W, r1 = X y x x Y, and uses move 2 with the rule Y x -> x x Y;
  - the other keeps r0 = W^-1, r1 = y x x Y X, and uses move 3 with the rule Y X -> X X Y.
- Each step is 1 multiplication plus 1 conjugation.
- A level change is a fixed 4 moves, [0,9,6,10] or [0,9,7,11], proved by induction on the level. This replaces our ~2(n-L) rotations.

**Results.**
- Canonical lengths for n = 4–10 are 52, 88, 154, 286, 544, 1060, 2086, about 2^(n+1)+3n+8. P000013 measured 50, 85, 148, 291, 539, 1064, 2078.
- All 14 rows got shorter. ac-04042 is now 53 (record 50); ac-06796 286 (275); ac-00106 2085 (2071).
- UPG-H re-verified all 28 lines (AC + Stable) on the official cores; 0 failed. They are now our best roads.
- No row is at its record.

**(2) The m+O(1) finish was not found.**
- Within fin2, the multiplication count is already within O(1) of the matrix minimum, so any saving must remove the [7]*(m-1) rotation.
- A BFS found no shortcut across that rotation of ≤ 8 moves at m = 8, or ≤ 10 at m = 16.
- This is a scoped miss; it does not show that no such finish exists.

Artifacts: research/acc/upgh/artifacts/t00312/ (bs_alt.py, notes.md, lines.txt).
