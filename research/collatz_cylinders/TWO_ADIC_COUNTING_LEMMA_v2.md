# An exact 2-adic counting lemma, and the exact n-step Syracuse digit law

*v2 — adds §4, the n-step theorem the lemma was wanted for.*

**Status:** elementary, complete, and machine-checked numerically. Offered
because a published Lean development explicitly defers exactly this statement.

## 1. The lemma

> **Lemma.** Let `m` be an odd integer, `a ∈ ℤ`, and `0 ≤ j < K`. Then
>
> ```
> #{ k ∈ [0, 2^K) : ν₂(a + m·k) = j }  =  2^(K−j−1).
> ```

Here `ν₂` is the 2-adic valuation. The hypothesis `j < K` is necessary, not
cosmetic — see §3.

### Proof

`ν₂(n) = j` holds exactly when `n ≡ 2^j (mod 2^(j+1))`. Note this condition
already forces `n ≠ 0`, since `2^j ≢ 0 (mod 2^(j+1))`, so the valuation is
everywhere defined on the set being counted.

Because `m` is odd it is invertible modulo `2^(j+1)`, so

```
k ⟼ a + m·k   (mod 2^(j+1))
```

is a bijection of `ℤ/2^(j+1)`. Hence exactly one residue class of `k` modulo
`2^(j+1)` satisfies `a + m·k ≡ 2^j (mod 2^(j+1))`.

Since `j + 1 ≤ K`, the interval `[0, 2^K)` is a union of `2^K / 2^(j+1)`
complete residue classes modulo `2^(j+1)`, so that one class contributes

```
2^K / 2^(j+1) = 2^(K−j−1)
```

values of `k`. ∎

The whole content is that an odd multiplier is invertible 2-adically, so an
affine progression equidistributes over residues mod `2^(j+1)` — and that a
window of length `2^K` sees each class exactly `2^(K−j−1)` times once
`j + 1 ≤ K`.

## 2. Sharpness: the behaviour at `j ≥ K`

For `j ≥ K` the formula `2^(K−j−1)` is not even an integer, and the true count
is not given by any closed form in `(a, m, K, j)`. What *is* true:

> **Proposition.** For `j ≥ K` and `m` odd,
> `#{ k ∈ [0, 2^K) : ν₂(a + m·k) = j } ∈ {0, 1}`.

*Proof.* `m` is invertible mod `2^j`, so `k ↦ a + m·k (mod 2^j)` is injective on
any set of at most `2^j` consecutive integers. Since `2^K ≤ 2^j`, it is
injective on `[0, 2^K)`. The condition `ν₂ = j` is a condition modulo
`2^(j+1)`, which refines the condition modulo `2^j`, so at most one `k` can
satisfy it. ∎

Which of `0` or `1` occurs depends on `a` and `m` and is not determined by the
residue of `a` modulo `2^K`. So `j < K` is exactly the range in which the count
is a function of `(K, j)` alone — below it the answer is uniform, at or above it
the answer depends on information the window does not carry.

## 3. Relation to `EOC/TaoLike/CylinderDigitCounting.lean`

The Lean development `innerlightr-wq/eoc-lean-verification` proves the `q = 1`
case of a one-step cylinder digit law and states, in that file's own header:

> *The general-`q` case (`P(next digit = q) = 2^{-q}` exactly, for every `q`)
> requires a genuinely new 2-adic counting lemma not otherwise present in this
> repository; it is deferred with a complete proof sketch to
> `ROUND3_DEFERRED_THEOREMS.md` rather than forced through this round.*

Its proved theorem is

```lean
theorem card_filter_padicValNat_affine_eq_one (B C K : ℕ)
    (hBpos : 0 < B) (hB : Even B) (hC : Odd C) (hK : 1 ≤ K) :
    ((Finset.range (2 ^ K)).filter (fun k => padicValNat 2 (B + 2 * C * k) = 1)).card
      = 2 ^ (K - 1)
```

**This is the `j = 0` case of the Lemma.** Write `B = 2B′`. Then
`B + 2Ck = 2(B′ + Ck)`, so

```
ν₂(B + 2Ck) = 1 + ν₂(B′ + Ck),
```

and therefore `ν₂(B + 2Ck) = 1 ⟺ ν₂(B′ + Ck) = 0`. Apply the Lemma with
`a = B′`, `m = C` (odd by hypothesis), `j = 0`; the side condition `j < K`
becomes `K ≥ 1`, which is their `hK`. The count is `2^(K−0−1) = 2^(K−1)`,
exactly their conclusion.

**The deferred general-`q` statement**, in their own parametrisation, is the
Lemma at `j = q − 1`:

> For `B > 0` even, `C` odd, and `1 ≤ q ≤ K`,
> ```
> #{ k ∈ [0, 2^K) : ν₂(B + 2·C·k) = q } = 2^(K−q).
> ```

This is the exact finite-counting form of `P(next digit = q) = 2^(−q)`, for
every `q` in the range the window can resolve. The bound `q ≤ K` is the
translated form of `j < K` and is sharp by §2.

## 3b. Numerical verification of the lemma

All checks apply `ν₂` directly; no result is taken on trust from the algebra.

| check | trials | mismatches |
|---|---|---|
| Lemma, `j < K`, random `(a, m, K, j)` | 2,000 | 0 |
| general-`q` in the `(B, C)` parametrisation, `1 ≤ q ≤ K` | 3,000 | 0 |
| eoc's `q = 1` claim against brute force | 4,000 | 0 |
| Lemma at `j = 0` reproducing eoc's claim | 4,000 | 0 |
| sweep `K ∈ [1,9]`, `j ∈ [0, K+1]`, 60 random `(a,m)` per cell | — | 0 for `j < K` |
| boundary `q > K`: observed counts | 1,500 | only `0` or `1`, never more |

`verify.py` reproduces every row.


## 4. The payoff: the n-step law is exact, up to a sharp budget

The lemma was wanted because it makes the *joint* law of several consecutive
digits computable. It turns out the local laws assemble with **no error term at
all**, until a resolution budget is spent — and then they fail completely.

Write `Syr(N) = (3N+1)/2^{ν₂(3N+1)}` for odd `N`, and let
`a_t(N) = ν₂(3·Syr^t(N) + 1)` be the digit at step `t`.

> **Theorem.** Let `n ≥ 1` and `q_1, …, q_n ≥ 1`, and put `S = q_1 + ⋯ + q_n`.
> If `S ≤ K − 1` then
>
> ```
> #{ odd N ∈ [1, 2^K) : a_t(N) = q_{t+1} for t = 0, …, n−1 }  =  2^(K−1−S).
> ```
>
> Since there are `2^(K−1)` odd `N` in the range, this says the first `n` digits
> are **exactly** i.i.d. `Geom(2)` on the cylinder — the joint probability is
> exactly `∏ 2^{−q_i}`, with no error term.
>
> If `S > K − 1` the formula fails for **every** digit vector.

### Proof

Induction on `n`, applying the Lemma once per step.

*Base.* `N` odd means `N = 2j+1` with `j ∈ [0, 2^{K−1})`, and
`3N + 1 = 6j + 4 = 2(3j + 2)`, so `a_0 = 1 + ν₂(3j + 2)`. Hence `a_0 = q_1` iff
`ν₂(3j + 2) = q_1 − 1`. The Lemma with `a = 2`, `m = 3` (odd), `j`-index
`q_1 − 1`, window `2^{K−1}` gives `2^{(K−1)−(q_1−1)−1} = 2^{K−1−q_1}`, and its
side condition `q_1 − 1 < K − 1` is exactly `q_1 ≤ K − 1`.

*Step.* `a_0 = q_1` pins `N` to a single residue class mod `2^{q_1+1}` (because
`3` is invertible), so `N = c + 2^{q_1+1}k` with `k` ranging over a window of
size `2^{K−q_1−1}`. Writing `3c + 1 = 2^{q_1}(1 + 2u)`,

```
3N + 1 = 2^{q_1}·(1 + 2u + 6k),   so   Syr(N) = A + 6k,  A = 1 + 2u odd.
```

Then with `3A + 1 = 2B`,

```
3·Syr(N) + 1 = 3A + 1 + 18k = 2(B + 9k),   so   a_1 = 1 + ν₂(B + 9k),
```

and `a_1 = q_2` iff `ν₂(B + 9k) = q_2 − 1`. Apply the Lemma again, now with
odd multiplier `m = 9`, on a window of size `2^{K−q_1−1}`: the count is
`2^{K−q_1−1−q_2}`, and the side condition `q_2 − 1 < K − q_1 − 1` is exactly
`q_1 + q_2 ≤ K − 1`.

Iterating, step `t` presents the Lemma with odd multiplier `3^{t+1}` on a window
shortened by the digits already spent. **Every multiplier is a power of 3, hence
odd, which is the only hypothesis the Lemma needs** — this is why the argument
never degrades. Each step consumes exactly `q_t` bits of the window, so the
argument runs precisely as long as `S ≤ K − 1`. ∎

### What the budget means

Each step spends `q_t` bits, and the digits average `2` bits apiece
(`E[Geom(2)] = 2`, confirmed numerically at `2.00` to three places). So a
`K`-bit cylinder resolves about `(K−1)/2` Syracuse steps before the law stops
holding — and the failure is not a gradual loss of accuracy but a cliff.

This is worth stating plainly, because it locates the difficulty precisely:

- the digits are **not approximately independent** on a cylinder, they are
  **exactly** independent while the window can still resolve them;
- the error in any approximate mixing statement is therefore **entirely a
  budget-exhaustion effect**, not a defect in the local structure;
- consequently, buying more steps requires more initial resolution — `n` steps
  need roughly `2n` bits — and no sharpening of the local law can avoid that,
  since the local law is already exact.

### Numerical check

Exhaustive over all odd `N < 2^K` — not sampled.

| K | n | vectors with `S ≤ K−1` | exact | off | vectors with `S > K−1` | match formula |
|---|---|---|---|---|---|---|
| 14 | 4 | 715 | 715 | 0 | 378 | 0 |
| 14 | 5 | 1287 | 1287 | 0 | 1093 | 0 |
| 16 | 4 | 1365 | 1365 | 0 | 576 | 0 |
| 16 | 5 | 3003 | 3003 | 0 | 1941 | 0 |
| 18 | 4 | 2380 | 2380 | 0 | 834 | 0 |
| 18 | 5 | 6188 | 6188 | 0 | 3214 | 0 |

and `K = 8 … 17` for `n = 1, 2, 3`, all exact inside the budget, no exceptions.
`verify_nstep.py` reproduces the table.

### Relation to Tao's Proposition 1.9

Tao's Proposition 1.9 (arXiv:1909.03562) bounds `d_TV(a⃗^(n)(𝐍), Geom(2)^n)` by
`≪ 2^{−c₁ n}` for a random `𝐍` whose residue is approximately uniform mod
`2^{n'}` with `n' ≥ (2 + c₀)n`. The `n' ≳ 2n` there and the `S ≤ K − 1` here are
the same budget seen from two sides: his hypothesis buys the resolution that
this theorem shows is exactly what the argument consumes. The statement above is
not a substitute for his — it is exact but conditional on a cylinder and capped
at the budget, where his is approximate but survives past it.


## 5. What this does not claim

- It is **elementary**. The proof is two lines of 2-adic invertibility; nothing
  here is deep, and the interest is entirely in *where it is needed*.
- It says nothing about any individual Collatz orbit. It is a statement about a
  **lift ensemble** — the parameter `k` ranging over a window — exactly as the
  eoc file is careful to say of its own `q = 1` result.
- §4 shows the local laws assemble **exactly** on a cylinder, up to the budget.
  It does **not** follow that anything is thereby known about an individual
  orbit: every statement here is about `N` ranging over a window, and a single
  predetermined seed is not a window.
- Nothing here is claimed to be new. The `n`-step law is the kind of statement
  that may well be folklore or implicit in the literature; it is written out
  because a current Lean development needed the `q = 1` case and deferred the
  rest.
- It is **not formalized in Lean**. The statement is given in a form intended to
  drop into `CylinderDigitCounting.lean`, but the formalization has not been
  written.

## Attribution

The `q = 1` theorem, the surrounding cylinder-lift framework, and the precise
statement of what was deferred are the work of the authors of
`innerlightr-wq/eoc-lean-verification`. This note supplies the deferred counting
lemma and the reduction; it claims nothing else.

No part of this note uses the root-conjugacy, donor-restoration,
coordinate-transport, divisibility, period or companion-restoration ideas of
Robert Sneiderman (ACC-P000002), so no such citation is claimed.
