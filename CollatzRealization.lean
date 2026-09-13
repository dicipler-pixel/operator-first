import CollatzAlignment

/-!
# Exact finite Collatz realization cylinders

The barrier inequalities constrain survival.  This module records the separate
realization constraint forced by an exact finite valuation prefix.  It does not
claim that every algebraically admissible word is realized, nor that the finite
constraints exclude an infinite orbit.
-/

namespace CollatzRealization

open CollatzBarrier
open CollatzAlignment

/-- An exact finite valuation prefix whose endpoint is odd forces the initial
seed into the corresponding binary phase cylinder.  The statement is written
as an exact remainder identity to avoid hiding any invertibility argument. -/
theorem exact_terminal_phase_mod
    (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j)) :
    (3 ^ j * x 0 + correction a j) % 2 ^ (prefixSum a j + 1) =
      (2 ^ prefixSum a j) % 2 ^ (prefixSum a j + 1) := by
  rcases exact_terminal_phase a x j hstep hodd with ⟨k, hk⟩
  rw [hk]
  simp [Nat.add_mod]

/-- If every state through depth `k` is odd and the exact step equations hold,
then the *same initial seed* satisfies every finite prefix phase cylinder up to
that depth.  This is the formal finite nesting/compatibility statement; no
infinite realization conclusion is drawn. -/
theorem all_prefix_phase_cylinders
    (a x : ℕ → ℕ) (k : ℕ)
    (hstep : ∀ i < k, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : ∀ j ≤ k, Odd (x j)) :
    ∀ j ≤ k,
      (3 ^ j * x 0 + correction a j) % 2 ^ (prefixSum a j + 1) =
        (2 ^ prefixSum a j) % 2 ^ (prefixSum a j + 1) := by
  intro j hj
  apply exact_terminal_phase_mod a x j
  · intro i hi
    exact hstep i (lt_of_lt_of_le hi hj)
  · exact hodd j hj

/-- At a contractive prefix, an actually realized odd-to-odd prefix must satisfy
both independent finite constraints: the exact binary phase cylinder and the
exact survival barrier.  This theorem only packages two already-derived facts;
it does not infer global convergence. -/
theorem realized_survival_layer
    (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j))
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j) :
    ((3 ^ j * x 0 + correction a j) % 2 ^ (prefixSum a j + 1) =
      (2 ^ prefixSum a j) % 2 ^ (prefixSum a j + 1)) ∧
    (x 0 ≤ x j ↔
      (2 ^ prefixSum a j - 3 ^ j) * x 0 ≤ correction a j) := by
  exact ⟨exact_terminal_phase_mod a x j hstep hodd,
    collatz_prefix_survival_iff_gap_finite a x j hstep hpow⟩

end CollatzRealization

#print axioms CollatzRealization.exact_terminal_phase_mod
#print axioms CollatzRealization.all_prefix_phase_cylinders
#print axioms CollatzRealization.realized_survival_layer
