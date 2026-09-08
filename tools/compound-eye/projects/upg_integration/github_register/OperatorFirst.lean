/-
SCRIPT: OPERATORFIRST-01

Machine-checked statements from the operator-first corpus.
Jeromie Beasley -- https://doi.org/10.5281/zenodo.22124938

  Part I   the commutator identity  [S+K, S-K] = -2 [S,K], and reciprocity
  Part II  the duality relation     D^2 + V^2 = 1

Single module on purpose: everything lives in this one file so the library has
no subdirectory to go missing.
-/

import Mathlib

namespace OperatorFirst

/-! # Part I -- warm-up: the commutator identity and reciprocity -/

/-! ## T1 — the commutator identity -/

section CommutatorIdentity

variable {R : Type*} [Ring R]

/-- The additive commutator `a*b - b*a`. -/
def comm (a b : R) : R := a * b - b * a

/-- **T1.**  Split an element as `C = S + K` with transpose-partner
`Cᵀ = S - K`.  The commutator of `C` with `Cᵀ` is `-2` times the commutator of
the two parts: in the paper's notation, `[C, Cᵀ] = -2 [S, K]`. -/
theorem comm_add_sub (S K : R) : comm (S + K) (S - K) = -(2 * comm S K) := by
  show (S + K) * (S - K) - (S - K) * (S + K) = -(2 * (S * K - K * S))
  noncomm_ring

/-- **Corollary.**  `C = S + K` is normal exactly when `S` and `K` commute.

The forward direction is the only place `h2` is spent, and it is genuinely
needed: in a ring of characteristic two `-2x = 0` for every `x`, so
`[C, Cᵀ] = 0` says nothing.  Real and complex matrices satisfy `h2`. -/
theorem normal_iff_comm_zero (h2 : ∀ x : R, (2 : R) * x = 0 → x = 0) (S K : R) :
    comm (S + K) (S - K) = 0 ↔ comm S K = 0 := by
  rw [comm_add_sub]
  constructor
  · intro h
    apply h2
    rw [← neg_neg (2 * comm S K), h, neg_zero]
  · intro h
    rw [h, mul_zero, neg_zero]

end CommutatorIdentity

/-! ## T2 — reciprocity -/

section Reciprocity

variable {n : Type*} [Fintype n] {α : Type*} [CommRing α]

/-- If `B` is symmetric and `V` is `B`-symmetric, the product `B * V` is
symmetric.

Note which hypotheses are absent.  The paper states this with `B` symmetric
positive definite; positivity, definiteness and invertibility are all unused —
the conclusion needs only `Bᵀ = B`. -/
theorem transpose_mul_of_symm {B V : Matrix n n α} (hB : Bᵀ = B)
    (hV : Vᵀ * B = B * V) : (B * V)ᵀ = B * V := by
  rw [Matrix.transpose_mul, hB, hV]

/-- **T2.**  Reciprocity in the paper's own form: the round-trip quantity is
symmetric in the two probe vectors, for every pair of vectors. -/
theorem reciprocity {B V : Matrix n n α} (hB : Bᵀ = B) (hV : Vᵀ * B = B * V)
    (x y : n → α) : x ⬝ᵥ (B * V) *ᵥ y = y ⬝ᵥ (B * V) *ᵥ x := by
  calc x ⬝ᵥ (B * V) *ᵥ y
      = x ⬝ᵥ (B * V)ᵀ *ᵥ y := by rw [transpose_mul_of_symm hB hV]
    _ = y ⬝ᵥ (B * V) *ᵥ x := Matrix.dotProduct_transpose_mulVec _ _ _

end Reciprocity

/-! # Part II -- the duality relation -/

open scoped ComplexInnerProductSpace
open ComplexConjugate

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- Fringe visibility: the modulus of the overlap of the two marker states. -/
noncomputable def visibility (u v : E) : ℝ := ‖⟪u, v⟫‖

/-- Which-way distinguishability. -/
noncomputable def distinguishability (u v : E) : ℝ :=
  Real.sqrt (1 - visibility u v ^ 2)

/-- The Gram matrix of the two marker states. -/
noncomputable def gram (u v : E) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![⟪u, u⟫, ⟪u, v⟫; ⟪v, u⟫, ⟪v, v⟫]

/-- An overlap times its swap is the squared visibility. This is where the
conjugate symmetry of the inner product enters. -/
theorem inner_mul_inner_swap (u v : E) :
    ⟪u, v⟫ * ⟪v, u⟫ = ((‖⟪u, v⟫‖ ^ 2 : ℝ) : ℂ) := by
  rw [← inner_conj_symm v u, RCLike.mul_conj]
  push_cast
  ring

/-- The Gram determinant, written out. -/
theorem gram_det (u v : E) :
    (gram u v).det = ⟪u, u⟫ * ⟪v, v⟫ - ⟪u, v⟫ * ⟪v, u⟫ := by
  rw [gram, Matrix.det_fin_two_of]

/-- **The Gram identity.** For unit markers the determinant of the Gram matrix
is exactly `1 - V²`. -/
theorem gram_det_of_unit (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    (gram u v).det = ((1 - visibility u v ^ 2 : ℝ) : ℂ) := by
  rw [gram_det, inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K, hu, hv,
      inner_mul_inner_swap, visibility]
  push_cast
  ring

/-- **Cauchy–Schwarz.** The visibility of a pair of unit markers never exceeds
one. This is the theorem that makes `D` real. -/
theorem visibility_le_one (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    visibility u v ≤ 1 := by
  have h : ‖⟪u, v⟫‖ ≤ ‖u‖ * ‖v‖ := norm_inner_le_norm u v
  rw [hu, hv, one_mul] at h
  exact h

/-- The Gram determinant of unit markers is non-negative — Cauchy–Schwarz again,
in the form the square root needs. -/
theorem one_sub_visibility_sq_nonneg (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    0 ≤ 1 - visibility u v ^ 2 := by
  have h0 : 0 ≤ visibility u v := norm_nonneg _
  have h1 : visibility u v ≤ 1 := visibility_le_one u v hu hv
  nlinarith

/-- **The duality relation.** For a pure marker, `D² + V² = 1`. -/
theorem duality (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    distinguishability u v ^ 2 + visibility u v ^ 2 = 1 := by
  rw [distinguishability, Real.sq_sqrt (one_sub_visibility_sq_nonneg u v hu hv)]
  ring

/-- `D²` is the Gram determinant. The duality relation is the statement that a
`2 × 2` determinant equals one minus an overlap. -/
theorem gram_det_eq_distinguishability_sq (u v : E) (hu : ‖u‖ = 1)
    (hv : ‖v‖ = 1) :
    (gram u v).det = ((distinguishability u v ^ 2 : ℝ) : ℂ) := by
  have h : distinguishability u v ^ 2 = 1 - visibility u v ^ 2 := by
    have hd := duality u v hu hv
    linarith
  rw [gram_det_of_unit u v hu hv, h]

/-- Perfect fringes: identical markers carry no which-way information. -/
theorem visibility_self (u : E) (hu : ‖u‖ = 1) : visibility u u = 1 := by
  rw [visibility, inner_self_eq_norm_sq_to_K, hu]
  norm_num

/-- The tight trap: `V = 1` forces `D = 0`. -/
theorem distinguishability_self (u : E) (hu : ‖u‖ = 1) :
    distinguishability u u = 0 := by
  rw [distinguishability, visibility_self u hu]
  norm_num

/-- The loose trap: orthogonal markers give full which-way information and no
fringes. -/
theorem distinguishability_of_orthogonal (u v : E) (h : ⟪u, v⟫ = 0) :
    distinguishability u v = 1 := by
  rw [distinguishability, visibility, h]
  norm_num

end OperatorFirst
