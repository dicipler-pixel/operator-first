# ACC search — Claude Code work orders

Derived from `ACC_FURTHER_TRACING_HANDOFF_20260919.md` and
`ACC_AC_STABLE_BROAD_TEST_WAVE_20260919.md` (both 2026-09-19).

**How to use this file.** Each `W#` block below is one paste-able instruction for a
Claude Code session. Run them in order. `W0` is blocking: nothing downstream is
trustworthy until it passes. Paste the block verbatim, plus the line:

> Read `research/acc/CLAUDE_CODE_WORK_ORDERS.md` section 0 first and obey every
> invariant there. Config lives in `research/acc/config/`.

Work orders W4–W9 (the six lanes) are independent of each other and can run in
parallel sessions once W1–W3 are green.

---

## 0. Invariants — every work order inherits these

These are not style preferences. Violating any one of them silently invalidates
the run it appears in.

1. **Exact checker and heuristic selector are different programs.** A scorer may
   rank candidates. Only an exact routine may declare a distance, a closure or a
   certificate. Never let a score decide a fact.
2. **`CLOSED` is a proof obligation.** Label a set `CLOSED` only when the BFS
   frontier emptied inside the cap with no budget cutoff. A run that hit a state
   ceiling, a wall clock or an out-of-memory is `BUDGET`, and `BUDGET` is never
   upgraded to `CLOSED` later by inspection.
3. **Raw-first.** Generate and record the *complete* local candidate population
   before any pruning. Exact-deduplicate only. Each Eye's output is stored
   separately, in its own field, with its own id and version. Mixing happens
   after recording, never during.
4. **Nothing is overwritten.** Observation stores are append-only JSONL. A
   corrected value is a new record with a new timestamp, not an edit.
5. **Rejected branches are evidence.** Record the branch and the reason it was
   rejected, not just the survivors.
6. **Matched controls at equal compute.** Every mixed-shape arm runs against
   three controls on the same population and the same budget: immediate-length
   only, turn-only, bottom-score. Report all four or report nothing.
7. **A negative is bounded.** Write "no finish within <exact family and budget>",
   never "impossible". Carry the expansion count with the claim.
8. **Replay gate.** No submission claim, in any file, until a complete ordinary
   move list replays from the official challenge start to the exact ordered
   target `(x, y)` under the pinned official verifier. Ordered means `r1 = x`
   and `r2 = y`, not the pair up to swap.
9. **Do not rerun spent geometry.** `config/lanes.json` carries the closed
   interiors, the spent negatives and the do-not-repeat set. Work from stored
   boundaries. If a rerun seems necessary, say why in writing first.
10. **Status vocabulary is fixed**: `CLOSED`, `BUDGET`, `NOHIT`, `PRODUCTIVE`,
    `CERTIFIED`. `CERTIFIED` requires invariant 8.

---

## W0 — Official pins (INSTALLED, calibration GREEN)

**Do not infer any contract in this section. It is pinned, vendored and
verified.** Earlier drafts of this file asked a session to reconstruct the move
ordering and the digit convention from geometry. That was wrong: invariant
checks exist to catch corruption, not to let each session rebuild the
conventions from scratch.

### Pinned sources

SAIR repository, commit `a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e`:

| artifact | pin |
|---|---|
| `competition/tools/verifier/data/move_spec.json` | `ac-r2-v1`, `sha256:e13f57d8…e07643` |
| `competition/tools/verifier/data/stable_move_spec.json` | `sac-r8-v1`, `sha256:27ecd0eb…f4b2b0` |
| `competition/problems/ac.jsonl` | git blob `09434a6e46090e6c086afa1104b49a4f890a4855` |
| `competition/problems/stable_ac.jsonl` | git blob `001da23a60777023522944f4168a78d1bc838bb2` |

The spec hashes are **payload digests, not file digests**: `move_spec.json`
declares `"hash_covers": "moves"`, and the value is
`sha256(JCS(moves))` via the official `verifier.canon.move_spec_hash`. Hashing
the raw file gives a different number and proves nothing. `acc/moves.py`
recomputes both and refuses to load on any disagreement.

The verifier is vendored at `vendor/verifier/` with every file's git blob hash
recorded in `vendor/PROVENANCE.json` and checked identical to source. There are
no local move semantics: `acc/moves.py` delegates to `verifier.core.apply_move`.

### Encodings — fixed, not searched

Ordinary alphabet is `1=x, -1=X, 2=y, -2=Y`. The historical compact digit
shorthand is exactly `0=x, 1=X, 2=y, 3=Y`. **Do not search over alternative
digit conventions.**

### Ordinary move table (`ac-r2-v1`, 14 moves)

```
 0  r0 <- r0^-1        7  r0 <- X r0 x
 1  r1 <- r1^-1        8  r0 <- y r0 Y
 2  r0 <- r0 r1        9  r0 <- Y r0 y
 3  r0 <- r0 r1^-1    10  r1 <- x r1 X
 4  r1 <- r1 r0       11  r1 <- X r1 x
 5  r1 <- r1 r0^-1    12  r1 <- y r1 Y
 6  r0 <- x r0 X      13  r1 <- Y r1 y
```

**The set is closed under inversion**: `0` and `1` self-inverse, `2↔3`, `4↔5`,
`6↔7`, `8↔9`, `10↔11`, `12↔13`. The spec's own notes say so, the `inverse`
column is an involution, and `apply_move(apply_move(p,i), INVERSE[i]) == p` holds
for all 14 on live states. Forward and backward search share one table.

### Starts — joined, never transcribed

`config/presentations.json` is built by joining the 51 suffixes in
`config/board_102.json` against the official manifest at the pinned commit. The
join asserts, and fails hard on: 51/51 suffixes present in **both** tracks;
`initial_relators` identical for every `ac-`/`sac-` pair; manifest relators
agreeing with the independent `ac.jsonl` description text; and all 102
`instance_hash` values recomputed with `verifier.canon.instance_hash`. All four
assertions pass. AC target is the exact ordered `[[1],[2]]`; Stable target is `[]`.

### Calibration result — 22/22 PASS

`runs/W0-calibration.json`. Every number below is the handoff's, reproduced
against official rows under the official spec:

| check | result |
|---|---|
| `ac-02216 --[1,11,5,12,1]--> ac-02555` | lands exactly, peak 18, **exact distance 5** |
| depth-2 balls, both endpoints | 160 and 160, **disjoint** → no path ≤ 4 |
| `ac-02555 --[6,10,10,13,8,6,6,3,1]--> xxyxYXXy / xxYxyyXXy` | lands exactly, peak 20 |
| depth-4 balls, both endpoints | 14,475 and 14,476, **disjoint** → no path ≤ 8 |
| `ac-02555 --[19 moves]--> ac-02178` | lands exactly, peak 24 (no shortest claim) |
| K basin `0002113 / 0020213303` cap 17 | 280 `CLOSED`, target absent, 12 cheapest exits |
| H junction `0002113 / 00022130312` cap 18 | 45,856 `CLOSED`, 53,804 length-19 exits, 85 reps |
| abelianized determinant on all replays | constant ±1 |

Re-run after any change to `acc/`, the vendored verifier or the pins. A single
mismatch means stop and report — never tune a contract until numbers agree.

---

## W1 — Exact core

**Goal:** the exact checker. No heuristics in this module.

**Build** under `research/acc/acc/`:

- `words.py` — **already committed.** Signed-integer letters matching the
  official alphabet (`1=x, -1=X, 2=y, -2=Y`), letter/digit codecs, `free_reduce` (the exact state normal form),
  `cyclic_canonical` and `normalize_ordinary` (rotation + inversion + relator
  swap — for *counting boundaries only*, never as a search key),
  `abelianized_determinant`, `encode_state`/`decode_state`. Do not change its
  semantics; downstream counts depend on them.
- `moves.py` — load `config/move_spec.json` **verbatim** from the pinned SAIR
  commit. Do not hand-write the table, and do not derive it. The ordinary set is
  **closed under inversion**: `0` and `1` are self-inverse, and `2↔3`, `4↔5`,
  `6↔7`, `8↔9`, `10↔11`, `12↔13`. Backward and bidirectional search therefore use
  the same table as forward search, with the inverse taken from those pairs.
- `search.py`:
  - `capped_closure(start, cap, max_states)` → visited set, boundary list
    (states with at least one child of total length > cap), and status
    `CLOSED`/`BUDGET` per invariant 2.
  - `bidirectional_distance(a, b, max_depth)` → exact distance, or a
    disjointness certificate: balls of radius `d` from both ends, disjoint,
    therefore no path of length ≤ `2d`. Forward from `a`, inverse-moves from `b`.
  - `multi_source_ball(sources, depth, cap)`.
  - `component_graph(seeds, cap)` → basins and the cheapest exits between them.
- `store.py` — append-only JSONL, one record per candidate, sha256 per record.

`acc/moves.py` and `acc/search.py` are committed and green. Free reduction,
move application and the inverse column all come from the vendored official
verifier; nothing in `acc/` reimplements move semantics.

**Scale note.** These lanes' interiors (cap23–cap25, 10–14M states) are already
`CLOSED` in `config/lanes.json`; the handoff forbids rerunning them. Size this
module for boundary, collar and gateway work — thousands to low millions of
states — and make `max_states` a required argument so an accidental interior
rerun trips the budget instead of running for a day.

**Accept:** W0's 22-check calibration passes, plus round-trip tests: `apply_move`
then `apply_move(..., INVERSE[i])` returns the original state for all 14 moves on
1,000 random reachable states; `normalize_ordinary` is idempotent;
`encode_state`/`decode_state` round-trips.

---

## W2 — Raw-first observation layer (the Eyes)

**Goal:** record everything observable about each candidate transition, with no
scoring, no ranking, no pruning.

**Build** `acc/eyes.py`. One function per Eye, each with `id` and `version`, each
written to its **own** field. Minimum set, from what the verified corpus taught:

*Length / shape* — `total_length`, `relator_lengths`, `delta_total`,
`imbalance`, `peak_in_depth2`, `hump_height`.

*Temporal* — `move_profile_turn` (the handoff's turn signal: define it once,
version it, never redefine it in place — at thresholds 0.50 and 0.75 the teacher
corpus recovers within 5 moves at 89.7% and 94.4%), `recovers_within_5`,
`branch_width` (distinct children after exact dedup), `new_state_rate`.

*Algebraic* — `exponent_sums`, `abelianized_determinant`, `whitehead_minimal`,
`whitehead_drop`, `magnus3_residue`, `mod11_label` (lane C's ambiguity labelling).

*Structural* — `component_id`, `component_novelty`, `escape_to_lower_total`,
`gateway_distance_delta`, `suffix_proximity`.

*Stable track only* — `generator_count`, `stabilization_age`,
`destabilization_ready`, `rank2_reentry`. Keep these **out** of the AC teacher
labels.

**Critical:** the population is the *complete* set of children before pruning.
The handoff's own numbers show why: behind `ac-02555`, 1,008 primitive
transitions deduplicate to 944 exact children, of which 936 are nondecreasing —
and only 6.84% of that nondecreasing set is productive. Prune first and the
signal is gone before you measure it.

**Accept:** on the `ac-02555` junction population, reproduce exactly
1,008 → 944 → 936. Every record carries every Eye id at its declared version.

---

## W3 — Mixer and controls

**Goal:** a small, replayable shape recipe fitted *after* observation.

**Build** `acc/mixer.py`: standardize, L2 logistic fit (stdlib only — the repo
has no numpy), deterministic seed, export recipe = weights + means + stds + Eye
ids and versions + the population it was fitted on.

Report on every fit: ROC AUC, top-decile and bottom-decile rates, enrichment
over the population rate, and all three controls from invariant 6.

**Accept:** refitting the recorded `ac-02555` population reproduces the handoff's
direct-mixture fit — top 93: 25/93 = 26.88%, full population 64/936 = 6.84%,
bottom 93: 0/93, enrichment ≈ 3.93× — and the official retest on `ac-04619` /
`ac-02216` gives 24/156 = 15.38% productive at AUC ≈ 0.7206, top 10% 7/15,
bottom 10% 0/15.

**Build in the known failure.** On `ac-02216`, immediate length **beat** the
mixer in the very top slice. So the recipe is context-conditional by
construction: store one recipe per shape family per class, and always carry the
length-only control alongside it. A single universal score is a known-wrong
design here. If a fit ever beats its controls everywhere, suspect leakage
between the label and an Eye before believing it.

---

## W4 — Lane A · `ac-05710` class (6 IDs)

cap25 is `CLOSED` at 10,224,840 states. **Do not rerun the interior.**

Start from the 4,064 ordinary normalized cap26 ports. Observe *all* of them (W2)
before any selection. Mix (W3), split into shape families, then push a depth-3
and depth-4 collar on selected families **with matched controls** — the depth-2
collar over all 4,064 already returned 0 low escapes back to ≤25 outside the
original component, so depth 2 is spent and depth 3/4 is the first unspent move.

**Outcome labels:** new low component, exact suffix/reverse collision, reduced
gateway distance, basin escape, full certificate.

---

## W5 — Lane B · `ac-00719` class (8 IDs)

cap23 is `CLOSED` at 13,440,784. **Do not re-enumerate it.**

Work the component graph outward from the known low wells — the 448, 31,008 and
86,456-state components behind cap24 — using the 8,079 normalized cap24 reps as
mouths. The lane's specific question: **what does the shape look like at a
productive basin mouth versus a dead one?** Lane B supplies the productive
mouths; lane F's 504-state bubble supplies the matched dead control. Record both
under the same Eye versions so they are comparable.

---

## W6 — Lane C · `ac-02923` (1 ID, ambiguity lane)

Prior exact multi-source work through depth 4 (29,045,054 states, 0 suffix hits,
0 radius-8 hits) is spent; depth 5 is incomplete and **claims no bound**.

The unspent structure is the mod-11 labelled non-normality residue: 82 states =
**41 two-state ambiguity cells**. Run **both members of every cell** — no
tie-breaking, no picking the shorter one. Preserve raw Eye vectors for each
member. The measurement is *which member of the pair moves first* on: basin
change, gateway distance, suffix proximity. That per-cell divergence is the
lane's product, whether or not anything finishes.

---

## W7 — Lane D · `ac-02217` class (5 IDs)

cap23 `CLOSED` at 13,978,168; signed atlas hits 0; uniform depth-1..4
multi-source (30,829,180 states) already spent with 0 suffix intersections.
**Do not rerun depth 1–4 uniformly** — that is the exact search that failed.

Instead: mix the 5,085 normalized hard ports into distinct temporal-shape
families, then allocate deeper budget *per family*, each with a matched control
family at equal compute. The hypothesis under test is that budget shaped by
family beats budget spread uniformly — which only means something if the control
arms actually run.

---

## W8 — Lane E · `ac-03467` / `ac-08126` (2 IDs, symmetry pair)

Both `CLOSED` through cap22 at 10,951,472 states each, and the two exact capped
sets are **disjoint**. They are linked by the signed symmetry `y → y⁻¹`, with
exact 12-move bridges both ways (peak 14) recorded in `config/lanes.json`.

Search **one** representative deeply; run the sibling as transfer/control. A
solution found on one transports to the other with about 13 moves of overhead
after basis restoration — so a hit on either is a hit on both, *after* an exact
replay of the transported path (invariant 8).

Use `ac-03467`'s mandatory hump as a hard outcome label, not a heuristic: inside
the cap22 component the minimum total is 14 with relator lengths staying 7 and 7,
so any solution must cross total length ≥ 23 before it shortens below the start.
A candidate route that never crosses 23 is refuted, not deprioritized.

---

## W9 — Lane F · `ac-00056` class (5 IDs)

cap25 `CLOSED` at 11,427,216. The depth-2 collar off the 5,138 cap26 reps
exposed exactly one new total-25 state, and it belongs to a `CLOSED` 504-state
bubble whose 40 cap26 boundary states contract to **10 ordinary normalized
reps**. Signed finisher hits: 0.

Those 10 reps are the lane's deliverable: a *clean dead-escape control*. An
escape that looks productive by every length and turn signal and goes nowhere is
the hardest negative to come by. Observe them under the same Eye versions as
lane B's productive mouths and feed the pair into W3 as the labelled contrast.

---

## W10 — Gateway network and suffix memory

Exact geometry already proved (reuse, do not recompute): `ac-02216 → ac-02555`
distance **exactly 5**, `ac-02555 →` synthetic junction distance **exactly 9**,
both with disjoint-ball proofs. `ac-02555 → ac-02178` is a replayed 19-move
connector with **no** shortest-path claim — do not quote it as a distance.

Spent and not to be repeated blindly: ordinary suffix/reverse 852,916
expansions; signed-atlas macro 7,972; family-stratified mixture/control
19,617,819; the entire H normalized boundary 10,350,960; stochastic descent
NOHIT. All zero finishes. All bounded negatives.

The unspent asset is the trajectory audit: a 182,639-state exact suffix
dictionary, 1,980 complete paths from 922 official starts, 19,185 distinct exact
middle states contracting to 565 ordinary normalized reps and 220 signed/Nielsen
roots, with **0** compiled finishing-atlas splices. Build the splice compiler:
index the suffix dictionary by normalized rep, then test every lane's ports and
collar states against it for an exact collision. A collision is a certificate
candidate — and still goes through the replay gate before it is called one.

---

## W11 — Stable AC track

Same initial presentation as the matching `ac-` suffix (asserted identical in
W0's join); different target and different grammar.

**Load the entire official `stable_move_spec.json` (`sac-r8-v1`). Do not
implement only IDs 14–16.**

- **257** frozen move IDs, `max_rank = 8`.
- IDs **0–13** are byte-identical to the ordinary table (verified).
- ID **14** stabilizes: appends a fresh generator `k+1` as its own relator.
- IDs **15–22** destabilize relators 0–7 respectively.
- The remaining IDs are the higher-rank inversions, multiplications and
  conjugations.
- Applicability and relabelling semantics come from `vendor/verifier/stable_core.py`.
  Note its contract differs from the ordinary one: `apply_move` returns
  `(new_state, None)` or `(None, reason)` where reason is one of
  `max_rank_exceeded`, `relator_out_of_rank`, `destabilize_precondition`,
  `generator_out_of_rank`. A move that is *not applicable* is not an error to
  swallow — record it as a rejected branch with its reason (invariant 5).
- Destabilizing relator `i` requires that relator to be exactly one **positive**
  generator appearing in no other relator; surviving words are relabelled.

**Verified:** from the exact ordinary target `(x, y)`, `[16,15]` destabilizes the
`y` relator then the `x` relator and reaches the empty presentation `()`.

Rules that are easy to get wrong:
- A Stable hit is **not** an AC hit. Never report one as the other.
- Stable-only moves stay out of the AC teacher labels.
- When a Stable path returns to rank 2, record that re-entry state as an AC
  structural clue — a candidate waypoint — not as an AC result.
- If an ordinary certificate `P` is found, the paired Stable claim requires
  compiling and testing `P + [16,15]` under the pinned verifier. It is not
  implied.

---

## W12 — Board sweep (51 bases / 102 track cases)

`config/board_102.json` holds the board and the allocation rule:
**round-robin, do not siege one target.**

- **Phase A** — cheap common observation layer on all 102 cases.
- **Phase B** — retain the top mixed-shape family plus matched controls per case.
- **Phase C** — deepen only the cases that produced measurable structural
  progress.

Promote a case out of round-robin only on: exact full certificate; a new low
component outside the known well; an exact suffix/reverse-ball collision; a
reduced exact gateway distance; a stable-only path exposing a reusable rank-2
re-entry shape; or the same temporal shape firing productively in two unrelated
classes. That last one is the most valuable signal on the board — it is the only
evidence that a shape recipe generalizes rather than memorizes.

**Emit one row per base suffix, exactly this format:**

```
suffix | AC status | Stable status | population observed | best shape recipe |
control comparison | new basin? | suffix hit? | gateway change? | certificate? |
exact move list if any | replay status
```

A complete path is published as a literal challenge line **only after
independent official replay**.

---

## Appendix — the honest scoreboard

The latest Shape-Mixer/gateway tracing produced **no new complete ordinary-AC
certificate**. 19 server-verified certificates and 310 primitive moves are the
teacher corpus, not a submission claim. Every lane above is tracing and
cross-lane comparison. Write results that way.
