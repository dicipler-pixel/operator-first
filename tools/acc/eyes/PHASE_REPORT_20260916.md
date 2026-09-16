# ACC eyes — phase report, 2026-09-16

Replay authority for everything below is `eyes/replay.py`, an independent Python
implementation of moves 0–13. **The pinned SAIR verifier is not in this repo** (there is no
`competition/` directory), so nothing here is marked `official_verify_ok`. Every artifact
carries `replay_authority: "eyes/replay.py"` and must be re-replayed against the pinned
verifier before submission.

## Phase 1 — recorder

Corpus availability was checked before recording. Of the five named inputs, two exist:
the 424 training move-lists (`tools/acc/finisher_v1/training_424_finished.txt`) and this
session's own runs. **The 424 training runs could not be recorded**: the file holds move
sequences keyed by `ms-train-NNNN`, and no file anywhere in the repo carries the start
presentations for those IDs, so there is nothing to replay them from. The 922-path
`ACC_VERIFIED_SEARCH_PASS_20260915.zip`, the hub `candidates.jsonl` /
`verified_certificates.txt`, and `ACC_UNSOLVED_CLASSES_0916.json` are all absent.

Rather than record nothing, a corpus was generated: 19 record-tying certificates (the
submission set) plus 10 paths produced by `ac_shared_ball_v1` on solved rows of `|r|`=17.

**29 runs recorded, all 29 landing on the trivial presentation.** Each emits per-step
`step, move_id, move_class, len_r1, len_r2, len_total, len_delta, cyclic_reduced_len_r1/r2,
expsum_x/y_r1/r2, penultimate_proximity, canonical_state_hash, symmetry_element, verifier_ok`
to `runs/<run_id>.json`, hash-chained into `EVENTS.jsonl`.
**Chain head: `a9dd7f0cbf8e614b71d179149f3eede54a52c922efa48a16294f2ebc6c860757`.**

## Phase 2 — canonical state and rediscovery index

`canon.py` canonicalises the unordered relator pair over the full group — cyclic rotation,
inversion, the 8 signed generator permutations, relator swap, after free + cyclic reduction —
and records the element used. Verified: all four relabelings of the trivial presentation
collapse to one hash.

`STATE_INDEX.jsonl` built. Raw counts: **126 distinct canonical states, 120 seen ≥ 2 times,
38 cross-target rediscoveries, 153 same-challenge shortening candidates.**

**Those counts are not findings. They are an artifact, and Phase 3 proved it.**

## Phase 3 — splice, and what the kill condition caught

Of the 153 shortening candidates, **0 survive.** Of every splice pair attempted on raw states,
**0 pass.** The reason is structural and matters for the eye design:

> **The canonical state hash cannot be a rediscovery key for splicing.** It quotients by
> cyclic rotation, but cyclic rotation is *not free* for the AC move set — reaching a
> different rotation costs conjugation moves. A conjugation `g·r·g⁻¹` followed by cyclic
> reduction returns the same cyclic word, so **conjugation moves are invisible to the
> canonical form.**

Measured directly: **330 consecutive-step canonical-hash repeats across the corpus, 269 of
them (81%) produced by a conjugation move.** A run of *k* consecutive conjugations yields
*k*+1 steps sharing one hash with consecutive `remaining_moves` values — which is exactly the
shape of every top "candidate" the index produced (`ac-07517 remaining=[25,26,27,28,29,30]`,
`ac-00338 remaining=[9,10,11,12,13,14]`). Cutting that span out breaks the path, because the
rotation a conjugation leaves you in determines what the next concatenation produces.

The brief anticipated this — *"cyclic rotation is NOT free… never assume"* — and the kill
condition is what caught it. **153 candidates would have been promoted on the index counts
alone.** None of them replay.

Recorded: `SPLICE_PASSED_20260916.json` (empty), `SPLICE_FAILS_20260916.jsonl` (5,415 pairs,
all rejected for uncompiled transport).

**Consequence for the design:** a usable rediscovery key must be either the raw state, or a
canonical form that quotients *only* by the moves that are genuinely free (relator swap and
the signed generator permutations), keeping rotation and inversion explicit with their move
cost. The brief's canonicalisation is right for *indexing* and wrong for *splicing*; those
need to be two different keys.

## Phases 4–5

Not built. Phase 4 needs the exact corridor closure sets (AK(3) caps 15/17/18, `ac-00002`
cap 35), which are not in the repo as enumerated state sets — only as summary verdicts.
Phase 5 is explicitly last and gated on frozen inputs.

## Phase 6 — first targeted searches

All 18 target IDs named in the brief were checked against the 2026-09-16 board: **every one is
`unsolved`, `kTeams = 0`.**

The uploaded `ACC_BRANCH_ROOT_FAMILY_118.json` supersedes the brief's target list. It gives
8 groups of the family `(x²yx⁻¹y, xyⁿx⁻¹y⁻⁽ⁿ⁺¹⁾)` covering **118 rows, all still unsolved**,
each with a representative — so value per solve is the group size:

| n | representative | rows | `\|r\|` |
|---|---|---|---|
| 3 | ac-02842 | 14 | 14 |
| 4 | ac-01440 | 14 | 16 |
| 5 | ac-01223 | 14 | 18 |
| 6 | ac-02799 | **20** | 20 |
| 7 | ac-00945 | **26** | 22 |
| 8 | ac-01696 | 10 | 24 |
| 9 | ac-01834 | 10 | 26 |
| 10 | ac-04027 | 10 | 28 |

This corrects the R6/R7 valuation in `MH_ACC_RUN_20260916_v1.md`, which put them at 4 and 5
rows from symmetry alone. They are n=6 and n=7 of this family: **R6 is worth 20 rows, R7 is
worth 26.**

Searches run, shared backward ball from `(x,y)`, forward per target:

    ac-02842  cap 20  BUDGET  depth_f=71   ball depth 10  -> no path <= 79 at cap 20
    ac-02842  cap 22  BUDGET  depth_f=30
    ac-02842  cap 24  BUDGET  depth_f=16
    ac-02842  cap 26  BUDGET  depth_f=13
    ac-01440  cap 22  CLOSED  component=2,064,600  -> disconnection theorem at cap 22
    ac-01440  cap 24  BUDGET  depth_f=28

    R7 family (5 rows) cap 28  CLOSED  component=7,159,020 on ALL FIVE, identical
    R7 root      cap 30  BUDGET  depth_f=35  -> no path <= 42 at cap 30 (was 31)
    R6 family (4 rows) cap 28  BUDGET  depth_f=37 -> no path <= 44 at cap 28 (was 33)

**No first solve.** All bounds are improvements on the recorded ones.

The five R7 rows closing at *exactly* 7,159,020 states is the sharpest structural result: they
are one problem with five identifiers, which is independent confirmation of the transport map.
