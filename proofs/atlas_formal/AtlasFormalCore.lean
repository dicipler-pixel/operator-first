import Mathlib

/-!
# AtlasFormalCore v0.1

Finite theorem kernels extracted from the Operator-First Atlas cards.

This file is intentionally narrower than the English card captions. Each theorem
formalizes only the exact finite algebraic statement named in its docstring.
It does NOT certify the physical readings, measured exponents, continuum limits,
or genericity claims attached to those cards.
-/

set_option autoImplicit false
noncomputable section

namespace AtlasFormal

section Noncommutative
variable {R : Type*} [Ring R]

/-- B2/B64 algebraic kernel. -/
theorem symmetric_skew_commutator_identity (S K : R) :
    (S + K) * (S - K) - (S - K) * (S + K) =
      -2 * (S * K - K * S) := by
  noncomm_ring

/-- The commuting direction of B2. -/
theorem symmetric_skew_commute_gives_zero (S K : R) (hSK : S * K = K * S) :
    (S + K) * (S - K) - (S - K) * (S + K) = 0 := by
  rw [symmetric_skew_commutator_identity, hSK]
  simp

/-- Algebraic redistribution operator behind B31. -/
def redistribution (P Ω : R) : R :=
  P * Ω * (1 - P) + (1 - P) * Ω * P

/-- Occupied-to-occupied block vanishes. -/
theorem redistribution_occupied_block (P Ω : R) (hP : P * P = P) :
    P * redistribution P Ω * P = 0 := by
  unfold redistribution
  noncomm_ring [hP]

/-- Complementary diagonal block vanishes. -/
theorem redistribution_empty_block (P Ω : R) (hP : P * P = P) :
    (1 - P) * redistribution P Ω * (1 - P) = 0 := by
  unfold redistribution
  noncomm_ring [hP]

/-- Left-to-right cross block extraction. -/
theorem redistribution_cross_left (P Ω : R) (hP : P * P = P) :
    P * redistribution P Ω * (1 - P) = P * Ω * (1 - P) := by
  unfold redistribution
  noncomm_ring [hP]

/-- Right-to-left cross block extraction. -/
theorem redistribution_cross_right (P Ω : R) (hP : P * P = P) :
    (1 - P) * redistribution P Ω * P = (1 - P) * Ω * P := by
  unfold redistribution
  noncomm_ring [hP]

/-- Exact B31 compatibility kernel. -/
theorem redistribution_eq_zero_iff_commute (P Ω : R) (hP : P * P = P) :
    redistribution P Ω = 0 ↔ P * Ω = Ω * P := by
  constructor
  · intro hF
    have hL : P * Ω * (1 - P) = 0 := by
      rw [← redistribution_cross_left P Ω hP, hF]
      simp
    have hR : (1 - P) * Ω * P = 0 := by
      rw [← redistribution_cross_right P Ω hP, hF]
      simp
    have hc : P * Ω - Ω * P = 0 := by
      calc
        P * Ω - Ω * P = P * Ω * (1 - P) - (1 - P) * Ω * P := by
          noncomm_ring [hP]
        _ = 0 := by rw [hL, hR]; simp
    exact sub_eq_zero.mp hc
  · intro hcomm
    unfold redistribution
    noncomm_ring [hP, hcomm]

end Noncommutative

/-- Squared Frobenius distance between real rank-one projectors `uuᵀ` and `vvᵀ`. -/
def rankOneProjectorFrobSq (x y u v : ℝ) : ℝ :=
  (x*x - u*u)^2 + 2*(x*y - u*v)^2 + (y*y - v*v)^2

/-- B16 finite kernel: half the squared projector distance is `1 - <u,v>²`. -/
theorem rankOne_projector_distance (x y u v : ℝ)
    (hxy : x^2 + y^2 = 1) (huv : u^2 + v^2 = 1) :
    rankOneProjectorFrobSq x y u v / 2 = 1 - (x*u + y*v)^2 := by
  calc
    rankOneProjectorFrobSq x y u v / 2 =
        (x^2 + y^2) * (u^2 + v^2) - (x*u + y*v)^2 := by
          unfold rankOneProjectorFrobSq
          ring
    _ = 1 - (x*u + y*v)^2 := by rw [hxy, huv]; ring

/-- B32: exact two-dimensional Gram saturation identity. -/
theorem gram2_saturation (a b c d : ℝ) :
    4 * (((a^2 + b^2)/2) * ((c^2 + d^2)/2) - ((a*c + b*d)/2)^2) =
      (a*d - b*c)^2 := by
  ring

/-- B48: scalar 1×1-block Schur-complement identity. -/
theorem scalar_schur_complement (a b c d : ℝ) (hd : d ≠ 0) :
    a*d - b*c = d * (a - b * d⁻¹ * c) := by
  field_simp [hd]
  <;> ring

/-- B51: reciprocal quartic reduction under `u=t+1/t`. -/
theorem reciprocal_quartic_reduction (a b c t : ℝ) (ht : t ≠ 0) :
    a*t^2 + b*t + c + b/t + a/t^2 =
      a*(t + 1/t)^2 + b*(t + 1/t) + (c - 2*a) := by
  field_simp [ht]
  <;> ring

/-- Minimal indefinite quadratic form for the logical kernel of B57. -/
def indefiniteQ (x y : ℝ) : ℝ := x^2 - y^2

/-- B57 kernel: a nonzero direction can be null once positivity is lost. -/
theorem indefinite_null_direction_exists :
    indefiniteQ 1 1 = 0 ∧ (1 : ℝ) ≠ 0 := by
  norm_num [indefiniteQ]

/-- B60 arithmetic kernel: if `k*q=1`, both factors are one. -/
theorem tangent_dimension_one_factors (k q : ℕ) (h : k * q = 1) :
    k = 1 ∧ q = 1 := by
  exact ⟨Nat.eq_one_of_mul_eq_one_right h, Nat.eq_one_of_mul_eq_one_left h⟩

/-- B61 exact algebra behind `a₀ m = ħ/(α c)`. -/
theorem bohr_rod (hbar alpha m c : ℝ)
    (ha : alpha ≠ 0) (hm : m ≠ 0) (hc : c ≠ 0) :
    (hbar / (alpha * m * c)) * m = hbar / (alpha * c) := by
  field_simp [ha, hm, hc]
  <;> ring

open Matrix

/-- B66 exact Gram determinant identity for a square real matrix. -/
theorem gram_det_is_square {n : Type*} [Fintype n] [DecidableEq n]
    (X : Matrix n n ℝ) :
    (X.transpose * X).det = X.det ^ 2 := by
  rw [Matrix.det_mul, Matrix.det_transpose]
  ring

section Chiral
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- B68 finite algebraic kernel: chiral anticommutation pairs `λ` with `-λ`. -/
theorem chiral_eigenvalue_pair
    (D Γ : Module.End ℝ V)
    (hanti : D.comp Γ = -(Γ.comp D))
    (v : V) (lam : ℝ) (hv : D v = lam • v) :
    D (Γ v) = (-lam) • Γ v := by
  have h := congrArg (fun F : Module.End ℝ V => F v) hanti
  simpa [LinearMap.comp_apply, hv] using h

end Chiral

/-- B74 exact turning inequality. -/
theorem refraction_turning_barrier (g s C : ℝ)
    (hg : 0 ≤ g) (hs : s^2 ≤ 1) (hC : g * s^2 = C) :
    C ≤ g := by
  nlinarith [mul_nonneg hg (sq_nonneg s)]

/-- B85 exact negative-square identity. -/
theorem rank_one_complex_realpart_det (x y s t : ℝ) :
    (x^2 - y^2) * (s^2 - t^2) - (x*s - y*t)^2 =
      -(x*t - y*s)^2 := by
  ring

/-- B85 sign consequence. -/
theorem rank_one_complex_realpart_not_definite (x y s t : ℝ) :
    (x^2 - y^2) * (s^2 - t^2) - (x*s - y*t)^2 ≤ 0 := by
  rw [rank_one_complex_realpart_det]
  exact neg_nonpos.mpr (sq_nonneg _)

/-- B90 positive-semidefinite tangency normal form. -/
def hermitianSoft (t : ℝ) : ℝ := t^2

/-- B90 safe kernel: the local line-element factor of the quadratic normal form is linear in `|t|`. -/
theorem hermitian_soft_lapse (t : ℝ) :
    Real.sqrt (hermitianSoft t) = |t| := by
  simpa [hermitianSoft] using Real.sqrt_sq_eq_abs t

/-- B90 crossing normal form. -/
def openSoft (t : ℝ) : ℝ := t

/-- A simple crossing has two signs. -/
theorem open_soft_crosses : openSoft (-1) < 0 ∧ 0 < openSoft 1 := by
  norm_num [openSoft]

/-- Absolute-value line-element factor for a simple crossing. -/
def openLapse (t : ℝ) : ℝ := Real.sqrt |t|

/-- B90 safe square-root kernel. Genericity requires separate transversality hypotheses. -/
theorem open_lapse_square (t : ℝ) : (openLapse t)^2 = |t| := by
  exact Real.sq_sqrt (abs_nonneg t)

end AtlasFormal

#print axioms AtlasFormal.symmetric_skew_commutator_identity
#print axioms AtlasFormal.redistribution_eq_zero_iff_commute
#print axioms AtlasFormal.rankOne_projector_distance
#print axioms AtlasFormal.gram2_saturation
#print axioms AtlasFormal.scalar_schur_complement
#print axioms AtlasFormal.reciprocal_quartic_reduction
#print axioms AtlasFormal.indefinite_null_direction_exists
#print axioms AtlasFormal.tangent_dimension_one_factors
#print axioms AtlasFormal.bohr_rod
#print axioms AtlasFormal.gram_det_is_square
#print axioms AtlasFormal.chiral_eigenvalue_pair
#print axioms AtlasFormal.refraction_turning_barrier
#print axioms AtlasFormal.rank_one_complex_realpart_det
#print axioms AtlasFormal.hermitian_soft_lapse
#print axioms AtlasFormal.open_lapse_square
