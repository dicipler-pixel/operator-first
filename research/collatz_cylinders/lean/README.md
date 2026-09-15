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

A theorem can be true and still say the wrong thing. Fourteen `example`s at the end are decided by the **kernel** (`decide`, never
`native_decide`) on concrete numbers: four confirming the counting formula, two
exhibiting the sharpness at `j = K`, two confirming the first-digit law — among the 32 odd `N`
below 64, exactly 8 have first digit 2 and exactly 4 have first digit 3 — and
six confirming the n-step law on concrete digit vectors of length 1, 2 and 3,
with two different odd multipliers. They fail the build if a statement drifts.

There is no `sorry`, no `admit`, and no `native_decide` in any proof.

## Trust base

```
'CollatzCylinder.odd_inv'                depends on axioms: [propext, Quot.sound]
'CollatzCylinder.pow_two_dvd_of_odd_mul' depends on axioms: [propext, Quot.sound]
'CollatzCylinder.hit_unique'             depends on axioms: [propext, Quot.sound]
'CollatzCylinder.hit_exists'             depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzCylinder.count_val2'             depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzCylinder.digit_eq_hit'           depends on axioms: [propext, Quot.sound]
'CollatzCylinder.count_first_digit'      depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzCylinder.cntFrom_reindex'        depends on axioms: [propext, Quot.sound]
'CollatzCylinder.syr_step'               depends on axioms: [propext, Quot.sound]
'CollatzCylinder.count_sdig'             depends on axioms: [propext, Classical.choice, Quot.sound]
'CollatzCylinder.count_syracuse_digits'  depends on axioms: [propext, Classical.choice, Quot.sound]
```

The two pillars and uniqueness are **constructive** — no `Classical.choice`.
The existence half pulls it in, so the main theorem sits on the standard Lean
trust base rather than a smaller one. Stated rather than hidden.

## Step one of the n-step law

```lean
theorem count_first_digit (p K' : Nat) (hp : p < K') :
    cntFrom (fun j => (3 * (2 * j + 1) + 1) % 2 ^ (p + 2) == 2 ^ (p + 1)) 0 (2 ^ K')
      = 2 ^ (K' - p - 1)
```

Among the `2^K'` odd numbers `N = 2j+1` below `2^(K'+1)`, exactly `2^(K'-p-1)`
have first Syracuse digit `p+1`. Writing `q = p+1`, that is `2^(K'-q)` out of
`2^K'` — the first digit is **exactly** `Geom(2)` on the cylinder, with no
error term, for every `q` the window can resolve.

This is the `n = 1` case of the n-step law, and the exact finite-counting form
of the statement deferred in `eoc-lean-verification`'s
`CylinderDigitCounting.lean`.

The bridge is `digit_eq_hit`: since `3N+1 = 2(3j+2)`, the first digit being
`p+1` is the same as `2 + 3j` having valuation exactly `p`. The factor of two
is stripped by `two_mod_two_mul` and what remains has multiplier `3` — odd,
which is the only hypothesis `count_val2` needs. Digits are never expressed
through a valuation *function*; the condition stays an exact modular one.

## The n-step law — proved

```lean
theorem count_syracuse_digits (ps : List Nat) (R : Nat) :
    cntFrom (fun j => sdig (2 + 3 * j) ps) 0 (2 ^ (budget ps + R)) = 2 ^ R
```

Parametrise the odd numbers as `N = 2j+1`. Among the `2^(budget ps + R)`
values of `j`, exactly `2^R` give `N` the Syracuse digit vector
`p₁+1, …, pₙ+1`. With `S = Σ(pᵢ+1)` and `K = S + R` this is §4 of the note:
`2^(K−S)` of the `2^K` odd numbers in the window, **exactly**, no error term.

Phrasing the window as `S + R` rather than `K` makes the budget structural.
`R` is literally the resolution left over, so the over-budget case is not false
but *unstatable* — which is the sharp behaviour the note describes, expressed
in the type rather than as a side condition.

`sdig` defines the digit vector by structural recursion on the digit list, so
no termination proof is needed and **`Syr` is never defined as a function**.
Each digit stays an exact modular condition; the divisions are exact wherever
they are reached (`v / 2^p` only after `v % 2^(p+1) = 2^p` is checked, `/ 2`
only on `3·odd + 1`), and where a check fails `&&` short-circuits so the value
is never used. The convention-free design survives all the way to the end.

The induction is one `count_val2` per digit, carried by:

| | |
|---|---|
| `cntFrom_reindex` | fixing a digit replaces the window by a progression, shortened by exactly the bits that digit spent |
| `strip` | a value of valuation `p` factors as `2^p · odd` |
| `syr_step` | on the reindexed window the value is `2^p · (A + 2m·k)`, `A` odd |
| `syr_next` | with `3A+1 = 2B` the next form is `B + (3m)·k` |
| `odd_three_mul` | `3m` is odd, so the next step's hypothesis holds |

At step `t` the multiplier is `3^(t+1)`, always odd, which is the counting
lemma's only hypothesis. That is exactly why the induction never degrades.

## What is NOT done

- **A bridge from `sdig` to a `Syr`-based definition.** `sdig` is proved to be
  the right predicate by construction and checked on concrete vectors, but
  nothing here defines `Syr` and proves the two agree. Anyone wanting the
  statement in terms of an explicit Syracuse map would have to add that.
- ~~**The induction to `n` steps.**~~ Fixing the first digit pins `N` to one
  residue class mod `2^(q₁+1)` (`hit_unique`, proved), so the survivors are
  again an arithmetic progression, and on it `Syr` takes the form `A + 6k`
  with `A` odd — the next digit is governed by `count_val2` with multiplier
  `9`, and at step `t` by `3^(t+1)`, always odd (`odd_pow`, proved).

  Done — see above.
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
