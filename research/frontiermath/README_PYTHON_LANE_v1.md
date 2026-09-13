# FrontierMath (ell=3, r=9) — Python lane

Work assigned to this lane by `CLAUDE_FRONTIERMATH_ATLAS_RAMANUJAN_TRACE.md`
in `FrontierMath_3Rank9_Mixer500_v4_1_Pass01.zip`:

> Claude/Python: implement and control-test the F3 rank increment plus
> separating-dual-witness routine; trace candidate sources; preserve failures.

    python3 research/frontiermath/run_controls_v1.py
    python3 -m unittest discover -s research/frontiermath

## No certificate was written

There are no nine generators in hand. Producing them is the target, not an
omitted input. The highest 3-rank on record in this package is 8. Nothing here
reaches the gate, so no `epoch_certificate` row exists and no certificate file
was created.

## What is exact here

**The F3 witness layer** (`f3_witness_v1.py`) implements the equivalence

    g not in W  <=>  rank[W|g] = rank(W)+1  <=>  exists chi: chi(W)=0, chi(g)=1

as exact arithmetic mod 3, together with the transport rule `chi -> T^(-T) chi`
under a coordinate change `v -> T v`, and the theorem-safe skew-adjoint test
`A^T B + B A = 0 (mod 3)`. The separating dual character is returned as an
independently re-checkable object, not merely a rank verdict.

Because the generators have exact order 3, coefficients `0,1,2` exhaust every
possible relation. The `3^9 = 19683` sweep is therefore a complete independence
proof rather than a bounded integer search.

**The class-group engine** (`bqf_class_group_v1.py`) is a real arithmetic
engine, not a stand-in. Reduction and composition are exact integer operations;
composition is ideal multiplication in the order of discriminant `D`, reduced to
Hermite normal form. It is validated against 39 classical class numbers and
against the group axioms (identity, inverse, associativity, closure) on 149
class groups. It **refuses** any discriminant too large to enumerate honestly.

## Controls

| Control | Result | How |
|---|---|---|
| C0 `Delta=-23` | h=3, `Cl=Z/3`, form `(2,1,3)` has exact order 3, 3-rank 1 | recomputed exactly here |
| C1 `Delta=-3321607` | h=567, exponent 63, `|Cl[3]|=27`, 3-rank 3, invariant factors `Z/63 x Z/3 x Z/3` | recomputed exactly here |
| C2 Elkies rank-16 | 3-rank 8 | **carried from the ledger, not recomputed** |
| C3 Elkies rank-17 | imaginary 3-rank 8, real 3-rank 7, allocation `17=7+8+2` | **carried from the ledger, not recomputed** |

C1's full invariant-factor structure follows from three exact measurements:
`h = 567 = 7 * 3^4`, 3-rank 3 forces the 3-part to be `Z/9 x Z/3 x Z/3`, and the
exponent is 63. The element-order profile
`{1:1, 3:26, 7:6, 9:54, 21:156, 63:324}` matches `Z/63 x Z/3 x Z/3` exactly.

## Stated constants, re-derived exactly

- Rank-16: `-3D` equals the stated field discriminant `-217541503961543485618350976479`, which is `1 mod 4`.
- Rank-17: `b = 27m` holds; `m = 2195745961 * 413891567044514092637683` holds and **both factors are prime**, so `m` is provably squarefree; `m = 3 mod 4`, hence `-m` is a fundamental discriminant; `3` does not divide `m`, so `3m` is squarefree; the stated real radicand equals `3m`; `17 = 7+8+2`.

## Limitations preserved, not papered over

- The Elkies discriminants are near `10^29`. Exact reduced-form enumeration is
  `O(|D|)` and cannot touch them. Their class groups need PARI, Sage or Magma.
  The engine raises rather than guessing.
- The sixteen form triples of the rank-16 boundary and their eight-vector
  relation basis are **absent from the ledger**. The historical 16-by-8
  dependency witness is therefore not reproduced here, and was not invented.
- The eight order-3 forms of the `D=3321607` historical run are likewise absent.
  Only the invariant-factor structure is reproducible, and that is what was
  reproduced.
- No class-group coordinates were synthesised anywhere in this lane.

## Rejoin point

This layer consumes exact F3 coordinate vectors and returns, for each candidate
ninth class, the rank increment and a separating dual row `chi` with `chi*W = 0`
and `chi*g = 1`. It begins only once a class-group engine supplies those
coordinates.
