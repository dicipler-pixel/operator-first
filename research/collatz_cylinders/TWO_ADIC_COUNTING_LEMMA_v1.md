# An exact 2-adic counting lemma for affine progressions

**Status:** elementary, complete, and machine-checked numerically. Offered
because a published Lean development explicitly defers exactly this statement.

## The lemma

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

## 4. Numerical verification

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

## 5. What this does not claim

- It is **elementary**. The proof is two lines of 2-adic invertibility; nothing
  here is deep, and the interest is entirely in *where it is needed*.
- It says nothing about any individual Collatz orbit. It is a statement about a
  **lift ensemble** — the parameter `k` ranging over a window — exactly as the
  eoc file is careful to say of its own `q = 1` result.
- The independence of successive digits, and whether the resulting local laws
  assemble into a statement about orbits, are separate questions and are not
  addressed here.
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
