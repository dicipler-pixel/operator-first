# Lean formalization — the 2-adic counting lemma

`Cylinder.lean` proves the counting lemma of
[`../TWO_ADIC_COUNTING_LEMMA_v2.md`](../TWO_ADIC_COUNTING_LEMMA_v2.md).

## Build

```
lean Cylinder.lean
```

That is the whole build. **The file imports nothing** — no Mathlib, no Std, no
`lake`. Lean 4 core only, so it compiles wherever a toolchain exists and
downloads nothing.

That was not an aesthetic choice. The pinned toolchain and the Mathlib cache
are both unreachable from this build environment and the available disk would
not hold a Mathlib build. Writing against core turned a blocked task into a
checkable one.

## The main theorem

```lean
theorem count_val2 {m : Nat} (hm : Odd2 m) (a j K : Nat) (hjK : j < K) :
    cntFrom (hit a m (2 ^ (j + 1)) (2 ^ j)) 0 (2 ^ K) = 2 ^ (K - j - 1)
```

In words: for `m` odd and `j < K`, exactly `2^(K-j-1)` of the `k` in `[0, 2^K)`
give `a + m*k` a 2-adic valuation of exactly `j`.

Valuation is not defined as a function. `hit a m (2^(j+1)) (2^j) k` is the
exact modular condition `(a + m*k) % 2^(j+1) = 2^j`, which says `2^j` divides
the value and `2^(j+1)` does not — and which already forces the value to be
nonzero, so nothing is swept under a `padicValNat 2 0 = 0` convention.

## Structure of the proof

| Result | Role |
|---|---|
| `odd_inv` | an odd `m` is invertible mod `2^s`, for every `s` |
| `pow_two_dvd_of_odd_mul` | `2^s ∣ m*d` with `m` odd gives `2^s ∣ d` |
| `dvd_of_add_mod_eq` | if adding `y` preserves the residue mod `M`, then `M ∣ y` |
| `hit_periodic` | the predicate has period `M` |
| `cntFrom_blocks` | over `q` whole periods the count is `q` times the count over one |
| `hit_unique` | at most one solution per window — from `pow_two_dvd_of_odd_mul` |
| `hit_exists` | at least one solution per window — from `odd_inv` |
| `count_one_window` | so exactly one |
| `count_val2` | `j < K` makes `[0, 2^K)` exactly `2^(K-j-1)` whole windows |

`odd_inv` is proved by lifting the inverse one bit at a time: given
`m * m' = 1 + c·2^s`, either `c` is even and `m'` already works a bit higher,
or `c` is odd and `m' + 2^s` works, because `c + m` is then a sum of two odds.

`odd_pow` (every power of an odd number is odd) is also proved. It is not
decoration: the n-step Syracuse law applies this lemma with multiplier
`3^(t+1)` at step `t`, and oddness is the lemma's only hypothesis, which is why
that induction never degrades.

## Where `j < K` is used, and why it is sharp

Only in `count_val2`, to write `2^K = 2^(j+1) · 2^(K-j-1)`. Below that bound
the window is shorter than one period, the count is 0 or 1, and no closed form
in `(K, j)` exists. Two kernel-checked instances in the file exhibit both
outcomes at `j = K`.

## Sanity checks

A theorem can be true and still say the wrong thing. Six `example`s at the end
are decided by the **kernel** (`decide`, never `native_decide`) on concrete
numbers — four confirming the formula, two exhibiting the sharpness. They fail
the build if the statement drifts.

There is no `sorry`, no `admit`, and no `native_decide` in any proof.

## Trust base

```
'CollatzCylinder.odd_inv'                depends on axioms: [propext, Quot.sound]
'CollatzCylinder.pow_two_dvd_of_odd_mul' depends on axioms: [propext, Quot.sound]
'CollatzCylinder.hit_unique'             depends on axioms: [propext, Quot.sound]
'CollatzCylinder.hit_exists'             depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzCylinder.count_val2'             depends on axioms: [propext, Classical.choice, Quot.sound]
```

The two pillars and uniqueness are **constructive** — no `Classical.choice`.
The existence half pulls it in, so the main theorem sits on the standard Lean
trust base rather than a smaller one. Stated rather than hidden.

## What is NOT done

- **The n-step Syracuse digit law** (§4 of the note). It applies this lemma
  once per step with multiplier `3^(t+1)`; `odd_pow` is the hypothesis check it
  needs. Not formalized.
- **The bridge to Mathlib's `padicValNat`.** The deferred statement in
  `eoc-lean-verification`'s `CylinderDigitCounting.lean` is this lemma at
  `j = q - 1` after reducing `B = 2B'`. Stating it in their parametrisation
  needs `padicValNat`, hence Mathlib, which cannot be built here. The
  mathematical content is proved; the translation is not written.

## What this does not claim

Nothing about the Collatz conjecture. Nothing about any individual orbit. This
is a counting statement about an ensemble of lifts — `k` ranging over a window
— exactly as the `eoc-lean-verification` development is careful to say of its
own `q = 1` result.

---

Author: Jeromie N. Beasley (statement, direction, research).
Formalization assistance: AI.
