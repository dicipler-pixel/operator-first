import UPGBlockFeedback

/-!
# Projector motion metric bridge

Finite exact algebra connecting retained/hidden coupling, the projector
commutator, and the zero-time feedback Gram.  This file deliberately stops
before any spacetime or physical-sector identification.
-/

open Matrix BigOperators

namespace UPGFeedback

variable {r h : Type*} [Fintype r] [Fintype h] [DecidableEq r] [DecidableEq h]

/-- Squared Frobenius energy of a rectangular real matrix. -/
def couplingEnergy (B : Matrix r h ℝ) : ℝ :=
  ∑ i, ∑ j, (B i j) ^ 2

/-- The retained-sector feedback Gram has trace equal to the total squared
retained/hidden coupling. -/
theorem trace_memoryAtZero_eq_couplingEnergy (B : Matrix r h ℝ) :
    Matrix.trace (memoryAtZero B) = couplingEnergy B := by
  simp [memoryAtZero, couplingEnergy, Matrix.trace, Matrix.mul_apply,
    Matrix.transpose_apply, pow_two]

/-- The retained-to-hidden block of `[H,P]` is exactly `-B`. -/
theorem projectorCommutator_inl_inr
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ)
    (i : r) (j : h) :
    projectorCommutator A B D (Sum.inl i) (Sum.inr j) = - B i j := by
  rw [projectorCommutator_eq_blocks]
  simp

/-- The hidden-to-retained block of `[H,P]` is exactly `Bᵀ`. -/
theorem projectorCommutator_inr_inl
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ)
    (i : h) (j : r) :
    projectorCommutator A B D (Sum.inr i) (Sum.inl j) = B j i := by
  rw [projectorCommutator_eq_blocks]
  simp

/-- The squared energy in one cross block of the projector commutator is
exactly the trace of the zero-time feedback Gram.  No factor-of-two convention
is hidden here: this is one oriented cross block only. -/
theorem projector_cross_energy_eq_memory_trace
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ) :
    (∑ i, ∑ j,
      (projectorCommutator A B D (Sum.inl i) (Sum.inr j)) ^ 2)
      = Matrix.trace (memoryAtZero B) := by
  rw [trace_memoryAtZero_eq_couplingEnergy]
  simp [couplingEnergy, projectorCommutator_inl_inr]

/-- Zero projector motion in the commutator sense is equivalent to zero
coupling energy. -/
theorem projectorCommutator_eq_zero_iff_couplingEnergy_eq_zero
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ) :
    projectorCommutator A B D = 0 ↔ couplingEnergy B = 0 := by
  rw [projectorCommutator_eq_zero_iff]
  constructor
  · intro hB
    subst B
    simp [couplingEnergy]
  · intro hE
    have hK : memoryAtZero B = 0 := by
      apply (memoryAtZero_eq_zero_iff B).2
      ext i j
      have htrace : Matrix.trace (memoryAtZero B) = 0 := by
        rw [trace_memoryAtZero_eq_couplingEnergy, hE]
      have hdiag := congrArg (fun M : Matrix r r ℝ => M i i)
        ((memoryAtZero_eq_zero_iff B).2 ?_)
      · simpa using hdiag
      · ext i' j'
        by_contra hne
        have hsquare_pos : 0 < (B i' j') ^ 2 := sq_pos_of_ne_zero hne
        have hterm_le : (B i' j') ^ 2 ≤ couplingEnergy B := by
          unfold couplingEnergy
          exact Finset.single_le_sum (fun x hx =>
            Finset.single_le_sum (fun y hy => sq_nonneg (B x y)) (Finset.mem_univ j'))
            (Finset.mem_univ i')
        rw [hE] at hterm_le
        linarith
    exact (memoryAtZero_eq_zero_iff B).1 hK

end UPGFeedback

#print axioms UPGFeedback.trace_memoryAtZero_eq_couplingEnergy
#print axioms UPGFeedback.projectorCommutator_inl_inr
#print axioms UPGFeedback.projectorCommutator_inr_inl
#print axioms UPGFeedback.projector_cross_energy_eq_memory_trace
#print axioms UPGFeedback.projectorCommutator_eq_zero_iff_couplingEnergy_eq_zero
