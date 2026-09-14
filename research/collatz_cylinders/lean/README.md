# Lean formalization — 2-adic counting lemma

`Cylinder.lean` formalizes the number-theoretic core of
[`../TWO_ADIC_COUNTING_LEMMA_v2.md`](../TWO_ADIC_COUNTING_LEMMA_v2.md).

## Build

```
lean Cylinder.lean
```

That is the whole build. **The file imports nothing** — no Mathlib, no Std,
no `lake`. It is Lean 4 core only, so it compiles anywhere a Lean toolchain
exists and needs no package download.

This was not an aesthetic choice. The pinned toolchain and the Mathlib cache
are both unreachable from the build environment used here, and the available
disk would not hold a Mathlib build. Writing against core turned a blocked
task into a checkable one.

## What is proved

Eight theorems, no `sorry`, no `admit`, no `native_decide`.

| Theorem | Statement |
|---|---|
| `odd_mul`, `odd_one` | odd × odd is odd |
| `odd_pow` | every power of an odd number is odd |
| `odd_add_odd_even` | odd + odd is even |
| `even_or_odd` | every natural is even or odd |
| `odd_inv` | **an odd `m` is invertible mod `2^s`, for every `s`** |
| `two_dvd_of_odd_mul` | `m` odd and `2 ∣ m*d` gives `2 ∣ d` |
| `pow_two_dvd_of_odd_mul` | **`m` odd and `2^s ∣ m*d` gives `2^s ∣ d`** |

The two bold results are the pillars. `odd_inv` is proved by lifting the
inverse one bit at a time: given `m * m' = 1 + c * 2^s`, either `c` is even and
`m'` already works one bit higher, or `c` is odd and `m' + 2^s` works, because
`c + m` is then a sum of two odd numbers. `pow_two_dvd_of_odd_mul` is the
injectivity half — an odd multiplier carries no powers of two, so it cancels.

`odd_pow` is not decoration: the n-step Syracuse law applies the counting
lemma with multiplier `3^(t+1)` at step `t`, and oddness is the lemma's only
hypothesis. `odd_pow` discharges that check at every step, which is why the
induction never degrades.

## Trust base

```
'CollatzCylinder.odd_inv'                depends on axioms: [propext, Quot.sound]
'CollatzCylinder.odd_pow'                depends on axioms: [propext, Quot.sound]
'CollatzCylinder.pow_two_dvd_of_odd_mul' depends on axioms: [propext, Quot.sound]
```

Note what is absent: **`Classical.choice`**. These proofs are constructive, and
the trust base is strictly smaller than the usual
`[propext, Classical.choice, Quot.sound]`.

## What is NOT proved

The counting theorem itself. `Cylinder.lean` states it precisely in its
closing section along with the three-step route from the pillars to the count,
and says which step consumes the `j < K` hypothesis and why that hypothesis is
sharp. It is stated in a comment, not as a `sorry`, so nothing in this file can
be mistaken for a result it does not have.

## What this does not claim

Nothing about the Collatz conjecture. Nothing about any individual orbit. The
target is a counting statement about an ensemble of lifts — `k` ranging over a
window — exactly as the `eoc-lean-verification` development is careful to say
of its own `q = 1` result.

---

Author: Jeromie N. Beasley (statement, direction, research).
Formalization assistance: AI.
