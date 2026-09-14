import UPGResolventFeedback
import Mathlib.LinearAlgebra.Matrix.PosDef

/-!
# Finite positive-response feedback criterion

This module gives a direct finite quadratic-form criterion for retained feedback.
It does not assume a Gram factorization, a resolvent representation, or a
physical interpretation.
-/

open Matrix

namespace UPGFeedback

variable {r h : Type*} [Fintype r] [Fintype h] [DecidableEq r] [DecidableEq h]

/-- A positive-definite hidden response detects every nonzero retained-hidden
coupling through the full feedback matrix. -/
theorem feedbackWith_eq_zero_iff_of_posDef
    (B : Matrix r h ℝ) (R : Matrix h h ℝ)
    (hR : R.PosDef) :
    feedbackWith B R = 0 ↔ B = 0 := by
  constructor
  · intro hfeedback
    ext i j
    have hdiag : (feedbackWith B R) i i = 0 := by
      simpa using congr_fun (congr_fun hfeedback i) i
    have hquad : (B i) ⬝ᵥ (R *ᵥ B i) = 0 := by
      simpa [feedbackWith, Matrix.mul_apply, Matrix.mulVec, dotProduct,
        Finset.mul_sum, mul_assoc] using hdiag
    by_contra hij
    have hrow : B i ≠ 0 := by
      intro hzero
      exact hij (congr_fun hzero j)
    exact (ne_of_gt (hR.dotProduct_mulVec_pos hrow)) hquad
  · intro hB
    subst B
    simp [feedbackWith]

/-- The contrapositive form used by the UPG finite feedback layer. -/
theorem nonzero_coupling_gives_nonzero_posDef_feedback
    (B : Matrix r h ℝ) (R : Matrix h h ℝ)
    (hR : R.PosDef) (hB : B ≠ 0) :
    feedbackWith B R ≠ 0 := by
  intro hzero
  exact hB ((feedbackWith_eq_zero_iff_of_posDef B R hR).mp hzero)

end UPGFeedback

#print axioms UPGFeedback.feedbackWith_eq_zero_iff_of_posDef
#print axioms UPGFeedback.nonzero_coupling_gives_nonzero_posDef_feedback
