import Mathlib

/-!
# Recovered math batch A

Exact finite/algebraic kernels extracted from the recovered October framework note.
These theorems certify only the mathematics written here. They do not certify
any particle, cosmological, zeta, or resonance interpretation.
-/

namespace RecoveredMathBatchA

/-! ## A1. Discrete 3-6-9 kernels -/

/-- The positive integer-valued kernel used in the recovered note. -/
def kappa (n : ℕ) : ℕ := 3 ^ n + 6 ^ n + 9 ^ n

/-- The signed kernel has to live in `ℤ` because subtraction is genuine. -/
def lambda (n : ℕ) : ℤ := (3 : ℤ) ^ n + (6 : ℤ) ^ n - (9 : ℤ) ^ n

/-- `kappa` is strictly positive for every natural index. -/
theorem kappa_pos (n : ℕ) : 0 < kappa n := by
  unfold kappa
  positivity

/-- Exact initial values. -/
theorem kappa_zero : kappa 0 = 3 := by
  norm_num [kappa]

theorem kappa_one : kappa 1 = 18 := by
  norm_num [kappa]

theorem lambda_zero : lambda 0 = 1 := by
  norm_num [lambda]

theorem lambda_one : lambda 1 = 0 := by
  norm_num [lambda]

theorem lambda_two : lambda 2 = -36 := by
  norm_num [lambda]

theorem lambda_three : lambda 3 = -486 := by
  norm_num [lambda]

/-- A recurrence-style expansion that follows directly from `pow_succ`. -/
theorem kappa_succ_expansion (n : ℕ) :
    kappa (n + 1) = 3 * 3 ^ n + 6 * 6 ^ n + 9 * 9 ^ n := by
  simp [kappa, pow_succ]
  ring

/-- The corresponding signed expansion for `lambda`. -/
theorem lambda_succ_expansion (n : ℕ) :
    lambda (n + 1) =
      3 * (3 : ℤ) ^ n + 6 * (6 : ℤ) ^ n - 9 * (9 : ℤ) ^ n := by
  simp [lambda, pow_succ]
  ring

/-! ## A2. Mass / energy ansatz algebra -/

/-- Real-valued copy of `kappa` used only for scalar model algebra. -/
def kappaR (n : ℕ) : ℝ := (kappa n : ℝ)

/-- If a model *defines* `m = hbar*f0/c^2*kappa`, then multiplying by `c^2`
recovers `hbar*f0*kappa`, provided `c` is nonzero. This is algebra only. -/
theorem mass_ansatz_energy_identity
    (hbar f0 c : ℝ) (n : ℕ) (hc : c ≠ 0) :
    (hbar * f0 / c ^ 2 * kappaR n) * c ^ 2 =
      hbar * f0 * kappaR n := by
  field_simp [hc]

/-- Positivity of the declared mass ansatz under positive scalar inputs. -/
theorem mass_ansatz_pos
    (hbar f0 c : ℝ) (n : ℕ)
    (hh : 0 < hbar) (hf : 0 < f0) (hc : c ≠ 0) :
    0 < hbar * f0 / c ^ 2 * kappaR n := by
  have hkNat : 0 < kappa n := kappa_pos n
  have hk : 0 < kappaR n := by
    exact_mod_cast hkNat
  have hc2 : 0 < c ^ 2 := sq_pos_of_ne_zero hc
  positivity

/-! ## A3. Phase-envelope decomposition -/

/-- Multiplying a complex envelope by a pure phase leaves its norm unchanged. -/
theorem pure_phase_preserves_norm (V : ℂ) (theta : ℝ) :
    ‖V * Complex.exp (Complex.I * (theta : ℂ))‖ = ‖V‖ := by
  rw [norm_mul, Complex.norm_exp]
  simp

/-- The same fact stated for absolute value. -/
theorem pure_phase_preserves_abs (V : ℂ) (theta : ℝ) :
    Complex.abs (V * Complex.exp (Complex.I * (theta : ℂ))) = Complex.abs V := by
  simpa [Complex.norm_def] using pure_phase_preserves_norm V theta

/-! ## A4. Finite admissible-path sums -/

variable {ι : Type*} [DecidableEq ι]

/-- Finite sum over an explicitly declared admissible class. -/
def pathSum (s : Finset ι) (phase : ι → ℝ) : ℂ :=
  s.sum (fun γ => Complex.exp (Complex.I * (phase γ : ℂ)))

/-- Every individual phase factor in the finite path sum has norm one. -/
theorem path_phase_unit_norm (x : ℝ) :
    ‖Complex.exp (Complex.I * (x : ℂ))‖ = 1 := by
  rw [Complex.norm_exp]
  simp

/-- Triangle bound: a finite sum of unit phases has norm at most its cardinality. -/
theorem pathSum_norm_le_card (s : Finset ι) (phase : ι → ℝ) :
    ‖pathSum s phase‖ ≤ (s.card : ℝ) := by
  unfold pathSum
  calc
    ‖∑ γ ∈ s, Complex.exp (Complex.I * (phase γ : ℂ))‖
        ≤ ∑ γ ∈ s, ‖Complex.exp (Complex.I * (phase γ : ℂ))‖ := by
            exact norm_sum_le _ _
    _ = ∑ γ ∈ s, (1 : ℝ) := by
          apply Finset.sum_congr rfl
          intro γ hγ
          exact path_phase_unit_norm (phase γ)
    _ = (s.card : ℝ) := by simp

/-- If two phase assignments agree on the admissible set, their sums agree. -/
theorem pathSum_congr_on
    (s : Finset ι) (phase₁ phase₂ : ι → ℝ)
    (h : ∀ γ ∈ s, phase₁ γ = phase₂ γ) :
    pathSum s phase₁ = pathSum s phase₂ := by
  unfold pathSum
  apply Finset.sum_congr rfl
  intro γ hγ
  rw [h γ hγ]

#print axioms RecoveredMathBatchA.kappa_pos
#print axioms RecoveredMathBatchA.kappa_zero
#print axioms RecoveredMathBatchA.kappa_one
#print axioms RecoveredMathBatchA.lambda_zero
#print axioms RecoveredMathBatchA.lambda_one
#print axioms RecoveredMathBatchA.lambda_two
#print axioms RecoveredMathBatchA.lambda_three
#print axioms RecoveredMathBatchA.kappa_succ_expansion
#print axioms RecoveredMathBatchA.lambda_succ_expansion
#print axioms RecoveredMathBatchA.mass_ansatz_energy_identity
#print axioms RecoveredMathBatchA.mass_ansatz_pos
#print axioms RecoveredMathBatchA.pure_phase_preserves_norm
#print axioms RecoveredMathBatchA.pure_phase_preserves_abs
#print axioms RecoveredMathBatchA.path_phase_unit_norm
#print axioms RecoveredMathBatchA.pathSum_norm_le_card
#print axioms RecoveredMathBatchA.pathSum_congr_on

end RecoveredMathBatchA
