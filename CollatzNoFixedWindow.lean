import Mathlib

/-!
# Collatz route control: no universal bounded Terras descent window

This module records a negative theorem that protects the formal Collatz branch
from a recurring false route: no fixed bounded number of Terras steps can force
every sufficiently large positive integer below its starting value.

The obstruction is the family `2^L - 1`.  For its first `L` Terras steps it
shadows the 2-adic odd-branch fixed point `-1` and satisfies the exact formula

`T^j(2^L - 1) = 3^j * 2^(L-j) - 1`,  for `j <= L`.

Those finite shadow segments can be arbitrarily long.  Therefore neither an
exact fixed-step descent claim nor a bounded-window descent claim can be the
global Collatz closure mechanism.

This is a route-exclusion theorem, not a proof of the Collatz conjecture.  It
also does not formalize the stronger external no-go theorem for all bounded
finite-state multiplicative potentials.
-/

namespace CollatzRouteNoGo

/-- Terras normalization: perform exactly one division by two per step. -/
def terras (n : ℕ) : ℕ :=
  if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- Standard forward iteration of the Terras map. -/
def terrasIter : ℕ → ℕ → ℕ
  | 0, n => n
  | k + 1, n => terras (terrasIter k n)

/-- Elementary growth fact used to choose a Mersenne witness beyond any cutoff. -/
theorem self_lt_two_pow (n : ℕ) : n < 2 ^ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [pow_succ]
      have hp : 0 < 2 ^ n := by positivity
      omega

/-- Exact Mersenne shadow formula for every depth before the binary tail is
exhausted. -/
theorem mersenne_shadow (L : ℕ) : ∀ j, j ≤ L →
    terrasIter j (2 ^ L - 1) = 3 ^ j * 2 ^ (L - j) - 1 := by
  intro j
  induction j with
  | zero =>
      intro _
      simp [terrasIter]
  | succ j ih =>
      intro hj
      have hjL : j < L := by omega
      have hprev := ih (by omega)
      rw [terrasIter, hprev]
      have hsplit : L - j = (L - (j + 1)) + 1 := by omega
      let A : ℕ := 3 ^ j * 2 ^ (L - (j + 1))
      have hA : 0 < A := by
        dsimp [A]
        positivity
      have htwo : 3 ^ j * 2 ^ (L - j) = 2 * A := by
        dsimp [A]
        rw [hsplit, pow_succ]
        ring
      have hthree : 3 ^ (j + 1) * 2 ^ (L - (j + 1)) = 3 * A := by
        dsimp [A]
        rw [pow_succ]
        ring
      rw [htwo, hthree]
      unfold terras
      rw [if_neg (by omega : ¬ (2 * A - 1) % 2 = 0)]
      omega

/-- Every point of the Mersenne shadow segment stays at or above its starting
integer. -/
theorem mersenne_shadow_nondec (L j : ℕ) (hj : j ≤ L) :
    2 ^ L - 1 ≤ terrasIter j (2 ^ L - 1) := by
  rw [mersenne_shadow L j hj]
  have hp : 2 ^ j ≤ 3 ^ j := Nat.pow_le_pow_left (by norm_num) j
  have hsplit : 2 ^ j * 2 ^ (L - j) = 2 ^ L := by
    rw [← pow_add]
    congr 1
    omega
  have hmain : 2 ^ L ≤ 3 ^ j * 2 ^ (L - j) := by
    calc
      2 ^ L = 2 ^ j * 2 ^ (L - j) := hsplit.symm
      _ ≤ 3 ^ j * 2 ^ (L - j) := Nat.mul_le_mul hp (le_refl _)
  omega

/-- For every bounded window and every cutoff, there is a seed beyond the
cutoff whose entire window fails to descend below the seed. -/
theorem no_fixed_descent_window_witness (B N₀ : ℕ) :
    ∃ n, N₀ ≤ n ∧ ∀ t ≤ B, n ≤ terrasIter t n := by
  let L := B + N₀ + 1
  let n := 2 ^ L - 1
  refine ⟨n, ?_, ?_⟩
  · have hpow : L < 2 ^ L := self_lt_two_pow L
    dsimp [L, n] at *
    omega
  · intro t ht
    dsimp [n]
    apply mersenne_shadow_nondec L t
    dsimp [L]
    omega

/-- No universal bounded-window strict-descent assertion can hold above any
fixed cutoff. -/
theorem no_universal_bounded_window_descent (B N₀ : ℕ) :
    ¬ (∀ n : ℕ, N₀ ≤ n → ∃ t : ℕ, t ≤ B ∧ terrasIter t n < n) := by
  rintro h
  obtain ⟨n, hn, hwindow⟩ := no_fixed_descent_window_witness B N₀
  obtain ⟨t, htB, hdrop⟩ := h n hn
  exact (Nat.not_lt_of_ge (hwindow t htB)) hdrop

/-- In particular, fixing one exact step count `K` cannot make all sufficiently
large seeds strictly descend. -/
theorem no_universal_fixed_step_descent (K N₀ : ℕ) :
    ¬ (∀ n : ℕ, N₀ ≤ n → terrasIter K n < n) := by
  rintro h
  obtain ⟨n, hn, hwindow⟩ := no_fixed_descent_window_witness K N₀
  exact (Nat.not_lt_of_ge (hwindow K (le_refl K))) (h n hn)

/-- Concrete guard against the old fixed-five-step genre. -/
theorem five_step_strict_descent_false :
    ¬ (∀ n : ℕ, 2 ≤ n → terrasIter 5 n < n) := by
  exact no_universal_fixed_step_descent 5 2

end CollatzRouteNoGo

#print axioms CollatzRouteNoGo.mersenne_shadow
#print axioms CollatzRouteNoGo.mersenne_shadow_nondec
#print axioms CollatzRouteNoGo.no_fixed_descent_window_witness
#print axioms CollatzRouteNoGo.no_universal_bounded_window_descent
#print axioms CollatzRouteNoGo.no_universal_fixed_step_descent
#print axioms CollatzRouteNoGo.five_step_strict_descent_false
