import UPGBlockFeedback

/-!
# Projector motion metric bridge

Finite exact algebra connecting retained/hidden coupling, the projector
commutator, and the zero-time feedback Gram. This file deliberately stops
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

/-- Coupling energy vanishes exactly when the rectangular coupling block
vanishes. -/
theorem couplingEnergy_eq_zero_iff (B : Matrix r h ℝ) :
    couplingEnergy B = 0 ↔ B = 0 := by
  constructor
  · intro hE
    ext i j
    have hle : (B i j) ^ 2 ≤ couplingEnergy B := by
      unfold couplingEnergy
      exact Finset.single_le_sum
        (fun i' _ => Finset.single_le_sum
          (fun j' _ => sq_nonneg (B i' j')) (Finset.mem_univ j))
        (Finset.mem_univ i)
    rw [hE] at hle
    have hz : (B i j) ^ 2 = 0 := le_antisymm hle (sq_nonneg (B i j))
    exact (sq_eq_zero_iff.mp hz)
  · intro hB
    subst B
    simp [couplingEnergy]

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
exactly the trace of the zero-time feedback Gram. No factor-of-two convention
is hidden here: this is one oriented cross block only. -/
theorem projector_cross_energy_eq_memory_trace
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ) :
    (∑ i, ∑ j,
      (projectorCommutator A B D (Sum.inl i) (Sum.inr j)) ^ 2)
      = Matrix.trace (memoryAtZero B) := by
  rw [trace_memoryAtZero_eq_couplingEnergy]
  simp [couplingEnergy, projectorCommutator_inl_inr]

/-- Zero projector commutator is equivalent to zero cross-sector coupling
energy. -/
theorem projectorCommutator_eq_zero_iff_couplingEnergy_eq_zero
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ) :
    projectorCommutator A B D = 0 ↔ couplingEnergy B = 0 := by
  rw [projectorCommutator_eq_zero_iff, couplingEnergy_eq_zero_iff]

end UPGFeedback

#print axioms UPGFeedback.trace_memoryAtZero_eq_couplingEnergy
#print axioms UPGFeedback.couplingEnergy_eq_zero_iff
#print axioms UPGFeedback.projectorCommutator_inl_inr
#print axioms UPGFeedback.projectorCommutator_inr_inl
#print axioms UPGFeedback.projector_cross_energy_eq_memory_trace
#print axioms UPGFeedback.projectorCommutator_eq_zero_iff_couplingEnergy_eq_zero
