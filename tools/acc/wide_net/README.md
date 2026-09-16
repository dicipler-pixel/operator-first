# ACC Wide Net — portable

Runs anywhere: Colab, CoCalc, a laptop, a box with 64 cores. **Standard library only**,
no install step, no GPU, no network.

    acc_fingerprint.py   the sweep (CLI, resumable, multiprocessing)
    ACC_WideNet.ipynb    Colab/CoCalc notebook wrapper with self-check and plot
    ac.jsonl             the 10,115-problem pool

## Why wide instead of deep

Deep search on one row answers one row. This answers the board. Two problems whose
cap-bounded components coincide are the same problem — one solve pays for both.
`ac-02842` and `ac-06556` share a cap-19 component of 23,609,984 states. The pool has
never been swept for this, and the histogram says where the multiplier is *before*
anyone spends hours climbing.

## Bounded work per row

`T_16`, the trivial component, has 129,247,304 states, so most easy rows cannot be
enumerated. Give every row a node budget instead:

* **closes under budget** → small isolated component. Hard row; size is its fingerprint.
* **exceeds budget** → giant class. Record and move on.

Cost per row is capped, the sweep is embarrassingly parallel, and the rows worth caring
about are the cheap ones.

## The cap is relative, not global

Starting lengths run 13–40. A fixed cap of 16 rejects most of the pool before any work
happens. `--delta 4` gives each row its own `|r| + 4`. Sizes compare within an `|r|`
band, which is where classes live — family members share `|r|`.

## Equal size is necessary, not sufficient

Measured: `ac-00945` and `ac-05233` have identical component size (386,320), identical
length profile, identical degree sequence — and **set intersection zero**. Isomorphic
but disjoint. The sweep emits *candidates*; `--verify` intersects the real sets and
tells you `IDENTICAL=True` (one solve pays all members) or `intersection=0` (no transfer
without an explicit symmetry map compiled to primitive moves).

## Validation

Reproduces three independently certified facts, and is a third implementation agreeing
with the hard-lane package and the C engine in this repo:

    ac-02842 cap 17 =  31,240
    ac-02842 cap 18 = 106,800
    ac-00738 cap 21 = 189,944

## Use

    python acc_fingerprint.py --pool ac.jsonl --delta 4 --budget 150000 --out fp.jsonl
    python acc_fingerprint.py --pool ac.jsonl --report fp.jsonl
    python acc_fingerprint.py --pool ac.jsonl --verify fp.jsonl --size 26664

Resumable — re-running skips rows already in `--out`, so a Colab timeout costs nothing.
Raise `--budget` for a finer small/giant split; lower it to go faster. `--workers` to
taste.
