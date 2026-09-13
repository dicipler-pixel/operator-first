import Mathlib

/-!
# Recovered math batch C

Transmission-line algebra, entropy sign controls, and scale-recurrence kernels.
All statements are ordinary mathematics. Engineering or physical interpretations
remain separate hypotheses.
-/

namespace RecoveredMathBatchC

/-! ## E. Transmission-line algebra without hiding square-root assumptions -/

/-- Squared characteristic impedance model. -/
noncomputable def lineZsq (L C : ℝ) : ℝ := L / C

/-- Squared propagation-speed model. -/
noncomputable def lineVsq (L C : ℝ) : ℝ := 1 / (L * C)

/-- Exact relation between the squared quantities, assuming nonzero line
parameters. This avoids introducing square-root branch issues too early. -/
theorem lineZsq_div_lineVsq
    (L C : ℝ) (hL : L ≠ 0) (hC : C ≠ 0) :
    lineZsq L C / lineVsq L C = L ^ 2 := by
  unfold lineZsq lineVsq
  field_simp [hL, hC]

/-- Product identity for the squared quantities. -/
theorem lineZsq_mul_lineVsq
    (L C : ℝ) (hL : L ≠ 0) (hC : C ≠ 0) :
    lineZsq L C * lineVsq L C = 1 / C ^ 2 := by
  unfold lineZsq lineVsq
  field_simp [hL, hC]

/-- Under positive inductance and capacitance, both squared quantities are
strictly positive. -/
theorem line_squared_quantities_positive
    (L C : ℝ) (hL : 0 < L) (hC : 0 < C) :
    0 < lineZsq L C ∧ 0 < lineVsq L C := by
  constructor
  · unfold lineZsq
    positivity
  · unfold lineVsq
    positivity

/-! ## G. Entropy sign negative control -/

/-- A positive prefactor times a positive logarithmic term can become negative
when multiplied by a negative cosine. Thus such a quantity is not automatically
a nonnegative entropy. -/
theorem cosine_modifier_can_make_negative
    (k logTerm cosineTerm : ℝ)
    (hk : 0 < k) (hlog : 0 < logTerm) (hcos : cosineTerm < 0) :
    k * logTerm * cosineTerm < 0 := by
  have hprod : 0 < k * logTerm := mul_pos hk hlog
  exact mul_neg_of_pos_of_neg hprod hcos

/-- Concrete control at angle `pi`, where cosine is exactly `-1`. -/
theorem cosine_pi_entropy_control
    (k logTerm : ℝ) (hk : 0 < k) (hlog : 0 < logTerm) :
    k * logTerm * Real.cos Real.pi < 0 := by
  rw [Real.cos_pi]
  have hprod : 0 < k * logTerm := mul_pos hk hlog
  nlinarith

/-! ## I. Exact scale recurrence consequences -/

/-- A factor-three recurrence has the expected closed form. -/
theorem factor_three_recurrence_closed_form
    (f : ℕ → ℝ) (h : ∀ n, f (n + 1) = 3 * f n) :
    ∀ n, f n = (3 : ℝ) ^ n * f 0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      rw [h n, ih]
      rw [pow_succ]
      ring

/-- General constant-factor recurrence, useful for keeping scale multipliers as
free model inputs instead of baking in an interpretation. -/
theorem constant_factor_recurrence_closed_form
    (r : ℝ) (f : ℕ → ℝ) (h : ∀ n, f (n + 1) = r * f n) :
    ∀ n, f n = r ^ n * f 0 := by
  intro n
  induction n with
  | zero => simp
  | succ n ih =>
      rw [h n, ih]
      rw [pow_succ]
      ring

/-- Zero iterations act as the identity; this is the safe algebraic core behind
statements of the form `Psi_(n+k)=S^k Psi_n`. -/
theorem iterate_zero_apply {α : Type*} (S : α → α) (x : α) :
    (S^[0]) x = x := by
  simp

#print axioms RecoveredMathBatchC.lineZsq_div_lineVsq
#print axioms RecoveredMathBatchC.lineZsq_mul_lineVsq
#print axioms RecoveredMathBatchC.line_squared_quantities_positive
#print axioms RecoveredMathBatchC.cosine_modifier_can_make_negative
#print axioms RecoveredMathBatchC.cosine_pi_entropy_control
#print axioms RecoveredMathBatchC.factor_three_recurrence_closed_form
#print axioms RecoveredMathBatchC.constant_factor_recurrence_closed_form
#print axioms RecoveredMathBatchC.iterate_zero_apply

end RecoveredMathBatchC
