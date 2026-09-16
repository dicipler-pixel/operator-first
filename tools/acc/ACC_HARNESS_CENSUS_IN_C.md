# HARNESS v2 census, embedded in the C enumerator

The v2 design doc names this as the next engineering target:

> "embed the cheap HARNESS census directly inside that C proposal loop. Then the 14
> labelled responses cost almost nothing extra, because the enumerator is already
> generating those 14 children."

`ac_harness_census_v1.c` does exactly that. The BFS already calls `apply()` fourteen times
per state to expand it; the labelled response is harvested from those same proposals. No
second pass, no recomputation.

**Correction to the design doc:** `ac_corridor_v1.c` is present in this repo at
`tools/acc/ac_corridor_v1.c`. It did not need recovering from the integrity package.

## Exact agreement with the Python reference

`ac-02842`, cap 14 — every record compared field by field against
`compound_eye_harness_acc_v2.py`:

| | Python | C | differing records |
|---|---|---|---|
| interior census | 180 | 180 | **0** |
| boundary census | 1,440 | 1,440 | **0** |

Same state sets, same `outcome_by_move` / `boundary_outcome_by_move` codes, same
`delta_total_by_move`, same exponent ledgers. **1,620 of 1,620 identical.**

The calibration result reproduces in C unchanged:

    lowest exits                : 16
    distinct labelled channels  : 16
    distinct R/D/S/U histograms : 1     -> (1 R, 0 D, 6 S, 7 U)

So the count-only eye sees one class and the labelled eye separates all sixteen, measured
independently on the C side.

## Cost

`ac-02842`, cap 18, 106,800 states:

| | time |
|---|---|
| Python HARNESS v2 | **588.18 s** |
| C census + JSONL emit | **0.65 s** |
| C census, output discarded | 0.63 s |

**~900x.** And the census is genuinely free: 0.65 s with full JSONL emission versus 0.63 s
without, so the labelled 14-channel record plus ledger plus lengths costs about **3%** over
the bare enumeration. The design doc's prediction holds — because the children were already
being generated, the only added work is a few integer ops per child.

## The wall, measured

`ac-02842`, cap 19 — the full 23,609,984-state component, censused end to end:

    121.1 s        ~195,000 states/second, each with all 14 labelled channels

The Python reference runs at ~182 states/second (106,800 states in 588 s). Extrapolated to
the same component that is **~36 hours** against **two minutes** — about 1,070x per state.

The component size matches the independent enumerations exactly (23,609,984), so the census
pass is not trading correctness for speed.

That is what makes the staged architecture affordable at the wall. The Census layer is no
longer the bottleneck anywhere in the run order; the deep eyes on collision cells are, which
is exactly where the design wants the cost to sit.

## Division of labour, unchanged

The Python harness stays the reference implementation, the verifier and the deep-eye
analyzer — Magnus, Fox, path holonomy, multiscale retina. The C census is the Census layer
only: exact state, lengths, imbalance, exponent ledger, and the labelled 14-move response.
Collision cells get handed back to Python for escalation.

## The non-negotiable rule is preserved

Every C record carries the exact freely-reduced ordered pair as text, so the Python side can
re-derive and re-check anything. Channel codes route attention. They never prune and never
certify. Only exact replay, exact component closure, exact target meet, or an explicitly
scoped obstruction may do that.
