/-
  An exact 2-adic counting lemma, formalized.

  Self-contained: this file imports NOTHING. No Mathlib, no Std. Every lemma
  below is proved from Lean 4 core, so the result depends on no library and
  carries no axioms beyond Lean's own.

  The statement being formalized (see ../TWO_ADIC_COUNTING_LEMMA_v2.md):

      For m odd, a : Nat, and j < K,
        #{ k < 2^K : v2 (a + m*k) = j }  =  2^(K-j-1)

  where v2 n = j is expressed, without defining a valuation, as the exact
  modular condition

        n % 2^(j+1) = 2^j

  which is equivalent to "2^j divides n but 2^(j+1) does not", and which
  already forces n ≠ 0.

  Author: Jeromie N. Beasley (statement, direction).
  Formalization assistance: AI.
-/

namespace CollatzCylinder

/-- `Odd2 m` : `m` is an odd natural number. Stated as an existential so that
    core `Nat` arithmetic can use the witness directly. -/
def Odd2 (m : Nat) : Prop := ∃ c, m = 2 * c + 1

theorem odd_one : Odd2 1 := ⟨0, rfl⟩

theorem odd_mul {m n : Nat} (hm : Odd2 m) (hn : Odd2 n) : Odd2 (m * n) := by
  obtain ⟨a, rfl⟩ := hm
  obtain ⟨b, rfl⟩ := hn
  exact ⟨2 * a * b + a + b, by simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]; omega⟩

/-- Every power of an odd number is odd. The `n`-step law needs exactly this,
    since the multiplier at step `t` is `3 ^ (t+1)`. -/
theorem odd_pow {m : Nat} (hm : Odd2 m) : ∀ n, Odd2 (m ^ n)
  | 0 => odd_one
  | n + 1 => by
      rw [Nat.pow_succ]
      exact odd_mul (odd_pow hm n) hm

/-- The sum of two odd numbers is even. This is the whole engine of the
    inverse construction below. -/
theorem odd_add_odd_even {c m : Nat} (hc : Odd2 c) (hm : Odd2 m) :
    ∃ d, c + m = 2 * d := by
  obtain ⟨x, rfl⟩ := hc
  obtain ⟨y, rfl⟩ := hm
  exact ⟨x + y + 1, by omega⟩

/-- A natural number is even or odd. -/
theorem even_or_odd (n : Nat) : (∃ c, n = 2 * c) ∨ Odd2 n := by
  induction n with
  | zero => exact Or.inl ⟨0, rfl⟩
  | succ k ih =>
      cases ih with
      | inl h => obtain ⟨c, rfl⟩ := h; exact Or.inr ⟨c, rfl⟩
      | inr h => obtain ⟨c, rfl⟩ := h; exact Or.inl ⟨c + 1, by omega⟩

/--
  **An odd number is invertible modulo every power of two.**

  Proved by induction on the exponent, lifting the inverse one bit at a time:
  if `m * m' = 1 + c * 2^s` then either `c` is even and `m'` already works
  modulo `2^(s+1)`, or `c` is odd and `m' + 2^s` works, because `c + m` is then
  a sum of two odd numbers and hence even.

  This is the only number-theoretic input the counting lemma needs, and it is
  where "m is odd" is used.
-/
theorem odd_inv (m : Nat) (hm : Odd2 m) : ∀ s, ∃ m' c, m * m' = 1 + c * 2 ^ s
  | 0 => by
      obtain ⟨x, rfl⟩ := hm
      exact ⟨1, 2 * x, by simp; omega⟩
  | s + 1 => by
      obtain ⟨m', c, hmc⟩ := odd_inv m hm s
      rcases even_or_odd c with ⟨d, rfl⟩ | hc
      · -- c even: the same inverse already works one bit further up
        refine ⟨m', d, ?_⟩
        rw [hmc, Nat.pow_succ]
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      · -- c odd: lift the inverse by 2^s; c + m is a sum of two odds, so even
        obtain ⟨d, hd⟩ := odd_add_odd_even hc hm
        refine ⟨m' + 2 ^ s, d, ?_⟩
        have h1 : m * (m' + 2 ^ s) = 1 + (c + m) * 2 ^ s := by
          rw [Nat.mul_add, hmc, Nat.add_mul, Nat.add_assoc]
        rw [h1, hd, Nat.pow_succ]
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]

/-- If `m` is odd and `2` divides `m * d`, then `2` divides `d`. -/
theorem two_dvd_of_odd_mul {m d : Nat} (hm : Odd2 m) (h : 2 ∣ m * d) : 2 ∣ d := by
  obtain ⟨c, rfl⟩ := hm
  rcases even_or_odd d with ⟨e, rfl⟩ | ⟨e, rfl⟩
  · exact ⟨e, rfl⟩
  · exfalso
    obtain ⟨q, hq⟩ := h
    have : (2 * c + 1) * (2 * e + 1) = 2 * (2 * c * e + c + e) + 1 := by
      simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]; omega
    omega

/--
  **2-adic cancellation.** An odd multiplier carries no powers of two, so it
  can be cancelled from a divisibility by `2 ^ s`.

  This is the injectivity half of the counting lemma: it is what forces two
  solutions in the same window to coincide.
-/
theorem pow_two_dvd_of_odd_mul {m : Nat} (hm : Odd2 m) :
    ∀ s d, 2 ^ s ∣ m * d → 2 ^ s ∣ d
  | 0, _, _ => Nat.one_dvd _
  | s + 1, d, h => by
      have h2 : (2 : Nat) ∣ m * d := Nat.dvd_trans ⟨2 ^ s, by rw [Nat.pow_succ]; omega⟩ h
      obtain ⟨e, rfl⟩ := two_dvd_of_odd_mul hm h2
      have hse : 2 ^ s ∣ m * e := by
        obtain ⟨q, hq⟩ := h
        refine ⟨q, ?_⟩
        have : 2 * (m * e) = 2 * (2 ^ s * q) := by
          rw [Nat.pow_succ] at hq
          simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc] at hq ⊢
          omega
        omega
      obtain ⟨f, rfl⟩ := pow_two_dvd_of_odd_mul hm s e hse
      exact ⟨f, by rw [Nat.pow_succ]; simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]⟩


/-!
## What remains

The two pillars above are the number-theoretic content. What is left is
combinatorial: turning "exactly one residue class solves it" into a count.

**Target (not yet proved).** For `m` odd, `a : Nat`, and `j < K`:

    #{ k < 2^K : (a + m * k) % 2^(j+1) = 2^j }  =  2^(K - j - 1)

The route, each step resting on a lemma already proved here:

1. `odd_inv` gives `m'` with `m * m' = 1 + c * 2^(j+1)`, so the affine map
   `k ↦ a + m * k` is invertible modulo `2^(j+1)`: SOME `r` in each window of
   `2^(j+1)` consecutive `k` solves the congruence.
2. `pow_two_dvd_of_odd_mul` gives uniqueness: if two `k` in one window solve
   it, then `2^(j+1)` divides `m` times their difference, hence divides the
   difference, hence they coincide. Exactly ONE `r` per window.
3. `j < K` means `[0, 2^K)` is exactly `2^(K-j-1)` whole windows of size
   `2^(j+1)`. One solution each gives `2^(K-j-1)`.

Step 3 is where `j < K` is used and is precisely why the hypothesis is not
cosmetic: at `j ≥ K` the interval is shorter than one window, the count is
0 or 1, and no closed form in `(K, j)` exists. See §2 of the note.

**Then the n-step law.** The Syracuse digit argument applies the counting
lemma once per step, with multiplier `3^(t+1)` at step `t`. `odd_pow` above
is exactly the hypothesis check for every one of those steps: a power of an
odd number is odd, and oddness is the lemma's only hypothesis. That is why
the induction never degrades.

**This file claims nothing about the Collatz conjecture.** It is a counting
statement about an ensemble of lifts, not about any individual orbit.
-/

end CollatzCylinder

-- Trust base check. Core `Nat` only: no Mathlib, no classical choice.
#print axioms CollatzCylinder.odd_inv
#print axioms CollatzCylinder.odd_pow
#print axioms CollatzCylinder.pow_two_dvd_of_odd_mul
