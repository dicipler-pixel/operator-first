import Mathlib

/-!
# AtlasFormalCore v0.1

Finite theorem kernels extracted from the Operator-First Atlas cards.

This file is intentionally narrower than the English card captions.  Each theorem
formalizes only the exact finite algebraic statement named in its docstring.
It does NOT certify the physical readings, measured exponents, continuum limits,
or genericity claims attached to those cards.

Prepared offline from the 90-card Atlas recovery package.  No repository files
are modified by this file.
-/

set_option autoImplicit false
noncomputable section

namespace AtlasFormal

/-! ## B2 / B64 — symmetric-skew commutator identity -/

section Noncommutative
variable {R : Type*} [Ring R]

/-- B2/B64 algebraic kernel.
If `H = S + K` and its transpose-side expression is `S - K`, then the
normality commutator is exactly `-2 [S,K]` before taking any norm. -/
theorem symmetric_skew_commutator_identity (S K : R) :
    (S + K) * (S - K) - (S - K) * (S + K) =
      -2 * (S * K - K * S) := by
  noncomm_ring

/-- The commuting direction of B2: if the symmetric and skew sectors commute,
the corresponding normality commutator vanishes. -/
theorem symmetric_skew_commute_gives_zero (S K : R) (hSK : S * K = K * S) :
    (S + K) * (S - K) - (S - K) * (S + K) = 0 := by
  rw [symmetric_skew_commutator_identity, hSK]
  simp

/-! ## B31 — projector tangents are purely cross-subspace -/

/-- Tangency to `P²=P` implies the occupied diagonal block vanishes. -/
theorem tangent_occupied_block (P D : R) (hP : P * P = P)
    (hD : P * D + D * P = D) : P * D * P = 0 := by
  have h := congrArg (fun X : R => P * X) hD
  have he : P * (P * D + D * P) = P * D + P * D * P := by
    rw [mul_add, ← mul_assoc P P D, hP, ← mul_assoc]
  rw [he] at h
  exact add_left_cancel (show P * D + P * D * P = P * D + 0 by simpa using h)

/-- The complementary diagonal block also vanishes. -/
theorem tangent_empty_block (P D : R) (hP : P * P = P)
    (hD : P * D + D * P = D) : (1 - P) * D * (1 - P) = 0 := by
  have hz := tangent_occupied_block P D hP hD
  calc
    (1 - P) * D * (1 - P) = D - (P * D + D * P) + P * D * P := by noncomm_ring
    _ = 0 := by rw [hD, hz]; simp

/-- B31 invariant kernel: every tangent to the idempotent manifold consists
exactly of its two cross-subspace blocks. -/
theorem tangent_split (P D : R) (hP : P * P = P)
    (hD : P * D + D * P = D) :
    D = P * D * (1 - P) + (1 - P) * D * P := by
  have hz := tangent_occupied_block P D hP hD
  calc
    D = P * D + D * P := hD.symm
    _ = P * D + D * P - (P * D * P + P * D * P) := by rw [hz]; simp
    _ = P * D * (1 - P) + (1 - P) * D * P := by noncomm_ring

end Noncommutative

/-! ## B16 — rank-one projector distance remembers angle, not orientation -/

/-- Squared Frobenius distance between the two real rank-one projector matrices
`uuᵀ` and `vvᵀ`, written in coordinates. -/
def rankOneProjectorFrobSq (x y u v : ℝ) : ℝ :=
  (x*x - u*u)^2 + 2*(x*y - u*v)^2 + (y*y - v*v)^2

/-- B16 finite kernel: for unit vectors, half the squared projector distance is
`1 - <u,v>²`.  This is the algebraic content of `sin² θ`; orientation has dropped
out because the inner product is squared. -/
theorem rankOne_projector_distance (x y u v : ℝ)
    (hxy : x^2 + y^2 = 1) (huv : u^2 + v^2 = 1) :
    rankOneProjectorFrobSq x y u v / 2 = 1 - (x*u + y*v)^2 := by
  calc
    rankOneProjectorFrobSq x y u v / 2 =
        ((x^2 + y^2)^2 + (u^2 + v^2)^2) / 2 - (x*u + y*v)^2 := by
          unfold rankOneProjectorFrobSq
          ring
    _ = 1 - (x*u + y*v)^2 := by rw [hxy, huv]; norm_num

/-! ## B32 — two-dimensional Gram saturation -/

/-- Lagrange's identity in the exact normalization used by a two-direction
metric/curvature pair.  It is the algebraic saturation kernel behind B32. -/
theorem gram2_saturation (a b c d : ℝ) :
    4 * (((a^2 + b^2)/2) * ((c^2 + d^2)/2) - ((a*c + b*d)/2)^2) =
      (a*d - b*c)^2 := by
  ring

/-! ## B48 — scalar Schur complement kernel -/

/-- The 1×1 block instance of the Schur-complement determinant identity.
The general block determinant theorem requires matrix invertibility machinery;
this theorem certifies the algebraic seam used by the card. -/
theorem scalar_schur_complement (a b c d : ℝ) (hd : d ≠ 0) :
    a*d - b*c = d * (a - b * d⁻¹ * c) := by
  field_simp [hd]
  <;> ring

/-! ## B51 — reciprocal quartic reduction -/

/-- B51 algebraic reduction.  Dividing a reciprocal quartic by `t²` and setting
`u = t + 1/t` lowers it to a quadratic. -/
theorem reciprocal_quartic_reduction (a b c t : ℝ) (ht : t ≠ 0) :
    a*t^2 + b*t + c + b/t + a/t^2 =
      a*(t + 1/t)^2 + b*(t + 1/t) + (c - 2*a) := by
  field_simp [ht]
  <;> ring

/-! ## B57 — null length does not imply zero motion in an indefinite form -/

/-- Minimal indefinite quadratic form used only to certify the logical
possibility behind B57. -/
def indefiniteQ (x y : ℝ) : ℝ := x^2 - y^2

/-- A nonzero direction can be null for an indefinite form.  This does not by
itself construct a moving biorthogonal projector; it certifies the obstruction
to inferring `motion = 0` from `length = 0` once positivity is lost. -/
theorem indefinite_null_direction_exists :
    indefiniteQ 1 1 = 0 ∧ (1 : ℝ) ≠ 0 := by
  norm_num [indefiniteQ]

/-! ## B60 — one-complex-line dimension arithmetic -/

/-- Arithmetic kernel of B60: if the complex tangent dimension `k(n-k)` is one,
both factors are one. -/
theorem tangent_dimension_one_factors (k q : ℕ) (h : k * q = 1) :
    k = 1 ∧ q = 1 := by
  exact ⟨Nat.eq_one_of_mul_eq_one_right h, Nat.eq_one_of_mul_eq_one_left h⟩

/-! ## B61 — the Bohr rod fixes inverse mass scaling -/

/-- Exact algebra behind `a₀ m = ħ/(α c)`. -/
theorem bohr_rod (hbar alpha m c : ℝ)
    (ha : alpha ≠ 0) (hm : m ≠ 0) (hc : c ≠ 0) :
    (hbar / (alpha * m * c)) * m = hbar / (alpha * c) := by
  field_simp [ha, hm, hc]
  <;> ring

/-! ## B66 — Gram squareness -/

open Matrix

/-- B66 exact Gram determinant identity for a square real matrix. -/
theorem gram_det_is_square {n : Type*} [Fintype n] [DecidableEq n]
    (X : Matrix n n ℝ) :
    (X.transpose * X).det = X.det ^ 2 := by
  rw [Matrix.det_mul, Matrix.det_transpose]
  ring

/-! ## B68 — chiral symmetry pairs eigenvectors -/

section Chiral
variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- Finite algebraic kernel of B68.  An operator anticommuting with a chiral
involution sends a `λ` eigenvector to a `-λ` eigenvector after applying the
chiral map.  Nonzeroness of the partner needs an additional injectivity/
involution hypothesis on `Γ`. -/
theorem chiral_eigenvalue_pair
    (D Γ : Module.End ℝ V)
    (hanti : D.comp Γ = -(Γ.comp D))
    (v : V) (lam : ℝ) (hv : D v = lam • v) :
    D (Γ v) = (-lam) • Γ v := by
  have h := congrArg (fun F : Module.End ℝ V => F v) hanti
  simpa [LinearMap.comp_apply, hv] using h

end Chiral

/-! ## B74 — turning inequality -/

/-- Exact inequality behind the B74 turning-point argument. -/
theorem refraction_turning_barrier (g s C : ℝ)
    (hg : 0 ≤ g) (hs : s^2 ≤ 1) (hC : g * s^2 = C) :
    C ≤ g := by
  nlinarith [mul_nonneg hg (sq_nonneg s)]

/-! ## B85 — rank-one bilinear determinant is a negative square -/

/-- B85 exact negative-square identity. -/
theorem rank_one_complex_realpart_det (x y s t : ℝ) :
    (x^2 - y^2) * (s^2 - t^2) - (x*s - y*t)^2 =
      -(x*t - y*s)^2 := by
  ring

/-- Consequently the determinant cannot be positive. -/
theorem rank_one_complex_realpart_not_definite (x y s t : ℝ) :
    (x^2 - y^2) * (s^2 - t^2) - (x*s - y*t)^2 ≤ 0 := by
  rw [rank_one_complex_realpart_det]
  exact neg_nonpos.mpr (sq_nonneg _)

/-! ## B90 — exact local normal forms, not the genericity claim -/

/-- The positive-semidefinite tangency normal form. -/
def hermitianSoft (t : ℝ) : ℝ := t^2

/-- The corresponding local line-element factor is linear in `|t|`. -/
theorem hermitian_soft_lapse (t : ℝ) :
    Real.sqrt (hermitianSoft t) = |t| := by
  simpa [hermitianSoft] using Real.sqrt_sq_eq_abs t

/-- The crossing normal form used on the indefinite side. -/
def openSoft (t : ℝ) : ℝ := t

/-- A simple crossing really has two sides. -/
theorem open_soft_crosses : openSoft (-1) < 0 ∧ 0 < openSoft 1 := by
  norm_num [openSoft]

/-- Its absolute-value lapse is a square-root normal form. -/
def openLapse (t : ℝ) : ℝ := Real.sqrt |t|

/-- Squaring the open lapse recovers the first-order zero.  The statement that
this is the *generic* non-Hermitian exponent requires separate transversality
hypotheses and is intentionally not claimed here. -/
theorem open_lapse_square (t : ℝ) : (openLapse t)^2 = |t| := by
  exact Real.sq_sqrt (abs_nonneg t)

end AtlasFormal

#print axioms AtlasFormal.symmetric_skew_commutator_identity
#print axioms AtlasFormal.tangent_split
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
