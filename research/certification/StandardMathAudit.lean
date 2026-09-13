import Mathlib

/-!
# Standard mathematics audit of recovered EFRO / SD-UFSKO kernels

This file deliberately removes project-specific names whenever the content is
standard mathematics. A theorem below certifies only the exact mathematical
kernel stated here. It does not certify a physical identification, a field
model, a cosmological interpretation, or a theory-of-everything claim.

The purpose is to separate what is structurally true from what still requires
an empirical or model-specific bridge.
-/

namespace StandardMathAudit

/-! ## 1. Energy-frequency bookkeeping -/

/-- If frequency is defined by `f = m c^2 / h`, with nonzero `h`, then
`h f = m c^2`. This is ordinary algebra, not a new physical law. -/
theorem planck_mass_frequency_consistency
    (h f m c : ℝ) (hh : h ≠ 0) (hf : f = m * c ^ 2 / h) :
    h * f = m * c ^ 2 := by
  rw [hf]
  field_simp [hh]

/-- A scalar coupling can be absorbed into an effective scalar mass parameter
purely by distributivity. This does not formalize the Dirac equation. -/
theorem effective_mass_distributivity (m eta phi psi : ℝ) :
    (m + eta * phi) * psi = m * psi + eta * phi * psi := by
  ring

/-! ## 2. Linear source superposition -/

variable {V W : Type*} [AddCommGroup V] [Module ℝ V]
  [AddCommGroup W] [Module ℝ W]

/-- Linear differential/source operators superpose sources. A Poisson equation
is a model-specific specialization of this standard linear fact. -/
theorem linear_source_superposition (L : V →ₗ[ℝ] W) (x y : V) :
    L (x + y) = L x + L y := by
  exact L.map_add x y

/-! ## 3. Best-matching / least-squares kernels -/

/-- A squared mismatch is nonnegative. -/
theorem squared_mismatch_nonnegative (x y : ℝ) :
    0 ≤ (x - y) ^ 2 := by
  exact sq_nonneg (x - y)

/-- In one dimension a squared mismatch vanishes exactly at equality. -/
theorem squared_mismatch_zero_iff (x y : ℝ) :
    (x - y) ^ 2 = 0 ↔ x = y := by
  constructor
  · intro h
    have hxy : x - y = 0 := by
      nlinarith
    linarith
  · intro h
    rw [h]
    norm_num

/-! ## 4. Finite memory/convolution kernels -/

variable {ι : Type*} [DecidableEq ι]

/-- A finite history-dependent linear memory functional. -/
def finiteMemory (s : Finset ι) (K x : ι → ℝ) : ℝ :=
  s.sum (fun i => K i * x i)

/-- The finite memory functional is additive in the history signal. -/
theorem finiteMemory_add (s : Finset ι) (K x y : ι → ℝ) :
    finiteMemory s K (fun i => x i + y i) =
      finiteMemory s K x + finiteMemory s K y := by
  unfold finiteMemory
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- A zero memory kernel contributes zero memory. -/
theorem finiteMemory_zero_kernel (s : Finset ι) (x : ι → ℝ) :
    finiteMemory s (fun _ => 0) x = 0 := by
  simp [finiteMemory]

/-! ## 5. Projector algebra -/

section Projectors

variable {R : Type*} [Ring R]

/-- The complement of an idempotent is idempotent. -/
theorem complement_of_idempotent_is_idempotent (P : R) (hP : P * P = P) :
    (1 - P) * (1 - P) = 1 - P := by
  calc
    (1 - P) * (1 - P) = 1 - P - P + P * P := by noncomm_ring
    _ = 1 - P := by rw [hP]; noncomm_ring

/-- An idempotent annihilates its algebraic complement on the right. -/
theorem idempotent_cross_right_zero (P : R) (hP : P * P = P) :
    P * (1 - P) = 0 := by
  calc
    P * (1 - P) = P - P * P := by noncomm_ring
    _ = 0 := by rw [hP]; simp

/-- An idempotent annihilates its algebraic complement on the left. -/
theorem idempotent_cross_left_zero (P : R) (hP : P * P = P) :
    (1 - P) * P = 0 := by
  calc
    (1 - P) * P = P - P * P := by noncomm_ring
    _ = 0 := by rw [hP]; simp

/-- If an operator commutes with an idempotent, its off-diagonal Peirce block
vanishes. This is the finite algebraic kernel behind many retained/hidden
subspace decompositions. -/
theorem commuting_operator_cross_block_zero
    (H P : R) (hP : P * P = P) (hcomm : H * P = P * H) :
    P * H * (1 - P) = 0 := by
  rw [← hcomm, mul_assoc, idempotent_cross_right_zero P hP, mul_zero]

end Projectors

/-! ## 6. Angular geometry -/

/-- The sine/cosine squared partition is standard Euclidean trigonometry. -/
theorem angular_partition (theta : ℝ) :
    Real.sin theta ^ 2 + Real.cos theta ^ 2 = 1 := by
  simpa [add_comm] using Real.sin_sq_add_cos_sq theta

/-! ## 7. Exact arithmetic around the recovered 14.14 convention -/

/-- `28.28` is exactly twice `14.14`. -/
theorem double_fourteen_point_fourteen :
    (2 : ℚ) * (1414 / 100 : ℚ) = (2828 / 100 : ℚ) := by
  norm_num

/-- `42.42` is exactly three times `14.14`. -/
theorem triple_fourteen_point_fourteen :
    (3 : ℚ) * (1414 / 100 : ℚ) = (4242 / 100 : ℚ) := by
  norm_num

/-- The older `28.26` value is not the exact second harmonic of `14.14`.
This is a useful bug detector: the two conventions cannot both be exact. -/
theorem old_28_26_is_not_exact_double :
    (2 : ℚ) * (1414 / 100 : ℚ) ≠ (2826 / 100 : ℚ) := by
  norm_num

/-- The exact rational gap between the decimal numbers `14.14` and
`14.134725` is `0.005275`. This proves numerical proximity only; it does not
prove anything about the Riemann zeta function or any physical frequency. -/
theorem decimal_14_134725_gap :
    |(1414 / 100 : ℚ) - (565389 / 40000 : ℚ)| = (211 / 40000 : ℚ) := by
  norm_num [abs_of_nonneg]

#print axioms StandardMathAudit.planck_mass_frequency_consistency
#print axioms StandardMathAudit.effective_mass_distributivity
#print axioms StandardMathAudit.linear_source_superposition
#print axioms StandardMathAudit.squared_mismatch_nonnegative
#print axioms StandardMathAudit.squared_mismatch_zero_iff
#print axioms StandardMathAudit.finiteMemory_add
#print axioms StandardMathAudit.finiteMemory_zero_kernel
#print axioms StandardMathAudit.complement_of_idempotent_is_idempotent
#print axioms StandardMathAudit.idempotent_cross_right_zero
#print axioms StandardMathAudit.idempotent_cross_left_zero
#print axioms StandardMathAudit.commuting_operator_cross_block_zero
#print axioms StandardMathAudit.angular_partition
#print axioms StandardMathAudit.double_fourteen_point_fourteen
#print axioms StandardMathAudit.triple_fourteen_point_fourteen
#print axioms StandardMathAudit.old_28_26_is_not_exact_double
#print axioms StandardMathAudit.decimal_14_134725_gap

end StandardMathAudit
