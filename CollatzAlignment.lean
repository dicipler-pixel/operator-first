import CollatzBarrier

namespace CollatzAlignment

open CollatzBarrier

theorem collatz_prefix_survival_iff_gap_finite (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j) :
    x 0 ≤ x j ↔
      (2 ^ prefixSum a j - 3 ^ j) * x 0 ≤ correction a j := by
  apply survival_iff_gap (p := 2 ^ prefixSum a j) (q := 3 ^ j)
      (B := correction a j)
  · positivity
  · exact hpow
  · exact affine_prefix_identity_finite a x j hstep

theorem exact_terminal_phase (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j)) :
    ∃ k : ℕ,
      3 ^ j * x 0 + correction a j =
        2 ^ prefixSum a j + 2 ^ (prefixSum a j + 1) * k := by
  rcases hodd with ⟨k, hk⟩
  refine ⟨k, ?_⟩
  have h := affine_prefix_identity_finite a x j hstep
  calc
    3 ^ j * x 0 + correction a j = 2 ^ prefixSum a j * x j := h.symm
    _ = 2 ^ prefixSum a j * (2 * k + 1) := by rw [hk]
    _ = 2 ^ prefixSum a j + 2 ^ (prefixSum a j + 1) * k := by
      rw [pow_succ]
      ring

end CollatzAlignment
