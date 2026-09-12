/-
SCRIPT: OPERATORFIRST-01

Statements from the operator-first corpus; verification status is tied to CI.
Jeromie Beasley -- https://doi.org/10.5281/zenodo.22124938

  Part I   the commutator identity  [S+K, S-K] = -2 [S,K], and reciprocity
  Part II  the pure-marker identity D^2 + V^2 = 1
  Part III finite Collatz valuation-word dynamics and exact contraction barriers

Single module on purpose: everything lives in this one file so the library has
no subdirectory to go missing. The definitions of D and V are mathematical;
an operational state-discrimination interpretation is a separate obligation.
-/

import Mathlib

open Matrix

namespace OperatorFirst

/-! # Part I -- warm-up: the commutator identity and reciprocity -/

section CommutatorIdentity

variable {R : Type*} [Ring R]

/-- The additive commutator `a*b - b*a`. -/
def comm (a b : R) : R := a * b - b * a

/-- The exact algebraic commutator identity, over an arbitrary ring. -/
theorem comm_add_sub (S K : R) : comm (S + K) (S - K) = -(2 * comm S K) := by
  show (S + K) * (S - K) - (S - K) * (S + K) = -(2 * (S * K - K * S))
  noncomm_ring

/-- Vanishing of the partner commutator is equivalent to commutation of the
parts, assuming multiplication by two has trivial kernel. Relating the partner
to a transpose or adjoint requires that additional identification. -/
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

section Reciprocity

variable {n : Type*} [Fintype n] {α : Type*} [CommRing α]

/-- Symmetry of the weighted probe product; positivity and invertibility are not needed. -/
theorem transpose_mul_of_symm {B V : Matrix n n α} (hB : Bᵀ = B)
    (hV : Vᵀ * B = B * V) : (B * V)ᵀ = B * V := by
  rw [Matrix.transpose_mul, hB, hV]

/-- Reciprocity for a symmetric bilinear pairing and a matched probe. -/
theorem reciprocity {B V : Matrix n n α} (hB : Bᵀ = B) (hV : Vᵀ * B = B * V)
    (x y : n → α) : x ⬝ᵥ (B * V) *ᵥ y = y ⬝ᵥ (B * V) *ᵥ x := by
  calc x ⬝ᵥ (B * V) *ᵥ y
      = x ⬝ᵥ (B * V)ᵀ *ᵥ y := by rw [transpose_mul_of_symm hB hV]
    _ = y ⬝ᵥ (B * V) *ᵥ x := Matrix.dotProduct_transpose_mulVec _ _ _

end Reciprocity

/-! # Part II -- pure-marker algebra -/

open scoped ComplexInnerProductSpace
open ComplexConjugate

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℂ E]

/-- Visibility for the stated equal-weight pure-marker model. -/
noncomputable def visibility (u v : E) : ℝ := ‖⟪u, v⟫‖

/-- Algebraic distinguishability parameter; its operational interpretation is not proved here. -/
noncomputable def distinguishability (u v : E) : ℝ :=
  Real.sqrt (1 - visibility u v ^ 2)

/-- The Gram matrix of the two marker states. -/
noncomputable def gram (u v : E) : Matrix (Fin 2) (Fin 2) ℂ :=
  !![⟪u, u⟫, ⟪u, v⟫; ⟪v, u⟫, ⟪v, v⟫]

/-- Conjugate symmetry identifies the swapped overlap product with its norm square. -/
theorem inner_mul_inner_swap (u v : E) :
    ⟪u, v⟫ * ⟪v, u⟫ = ((‖⟪u, v⟫‖ ^ 2 : ℝ) : ℂ) := by
  rw [← inner_conj_symm v u, Complex.mul_conj, Complex.normSq_eq_norm_sq]

/-- The Gram determinant, written out. -/
theorem gram_det (u v : E) :
    (gram u v).det = ⟪u, u⟫ * ⟪v, v⟫ - ⟪u, v⟫ * ⟪v, u⟫ := by
  rw [gram, Matrix.det_fin_two_of]

/-- For unit markers the Gram determinant is exactly `1 - V²`. -/
theorem gram_det_of_unit (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    (gram u v).det = ((1 - visibility u v ^ 2 : ℝ) : ℂ) := by
  rw [gram_det, inner_self_eq_norm_sq_to_K, inner_self_eq_norm_sq_to_K, hu, hv,
      inner_mul_inner_swap, visibility]
  push_cast
  ring

/-- Cauchy--Schwarz bounds the overlap of unit markers. -/
theorem visibility_le_one (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    visibility u v ≤ 1 := by
  have h : ‖⟪u, v⟫‖ ≤ ‖u‖ * ‖v‖ := norm_inner_le_norm u v
  rw [hu, hv, one_mul] at h
  exact h

/-- The square-root radicand is nonnegative for unit markers. -/
theorem one_sub_visibility_sq_nonneg (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    0 ≤ 1 - visibility u v ^ 2 := by
  have h0 : 0 ≤ visibility u v := norm_nonneg _
  have h1 : visibility u v ≤ 1 := visibility_le_one u v hu hv
  nlinarith

/-- Pure-marker identity for the definitions above; not an independent derivation of a detector law. -/
theorem duality (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    distinguishability u v ^ 2 + visibility u v ^ 2 = 1 := by
  rw [distinguishability, Real.sq_sqrt (one_sub_visibility_sq_nonneg u v hu hv)]
  ring

/-- Squared distinguishability equals the Gram determinant for unit markers. -/
theorem gram_det_eq_distinguishability_sq (u v : E) (hu : ‖u‖ = 1)
    (hv : ‖v‖ = 1) :
    (gram u v).det = ((distinguishability u v ^ 2 : ℝ) : ℂ) := by
  have h : distinguishability u v ^ 2 = 1 - visibility u v ^ 2 := by
    have hd := duality u v hu hv
    linarith
  rw [gram_det_of_unit u v hu hv, h]

/-- Identical unit markers have unit visibility. -/
theorem visibility_self (u : E) (hu : ‖u‖ = 1) : visibility u u = 1 := by
  rw [visibility, inner_self_eq_norm_sq_to_K, hu]
  norm_num

/-- Identical unit markers have zero distinguishability. -/
theorem distinguishability_self (u : E) (hu : ‖u‖ = 1) :
    distinguishability u u = 0 := by
  rw [distinguishability, visibility_self u hu]
  norm_num

/-- Orthogonal markers give unit algebraic distinguishability. -/
theorem distinguishability_of_orthogonal (u v : E) (h : ⟪u, v⟫ = 0) :
    distinguishability u v = 1 := by
  rw [distinguishability, visibility, h]
  norm_num

/-! # Part III -- finite Collatz valuation-word algebra

This section deliberately formalizes only finite prescribed words.  A list
`[a₀, ..., aₖ]` records the powers of two that one *asks* to divide after
successive odd `3n+1` moves.  The statements below do not assert that every
word is realized by an integer Collatz orbit, nor that dangerous words can or
cannot concatenate forever.  That realization problem is a separate theorem
obligation.
-/

section CollatzFiniteWords

/-- One odd-to-odd affine step over `ℚ` with prescribed two-adic exponent `a`.
For an actually realized odd Collatz step one would have `a = v₂(3n+1)`. -/
def collatzQStep (a : ℕ) (x : ℚ) : ℚ :=
  (3 * x + 1) / (2 : ℚ) ^ a

/-- Apply a finite prescribed valuation word from left to right. -/
def collatzQWord : List ℕ → ℚ → ℚ
  | [], x => x
  | a :: w, x => collatzQWord w (collatzQStep a x)

/-- Multiplicative coefficient of the affine map associated with a word. -/
def collatzWordMul : List ℕ → ℚ
  | [] => 1
  | a :: w => collatzWordMul w * (3 / (2 : ℚ) ^ a)

/-- Additive coefficient of the affine map associated with a word. -/
def collatzWordAdd : List ℕ → ℚ
  | [] => 0
  | a :: w => collatzWordMul w / (2 : ℚ) ^ a + collatzWordAdd w

/-- Every finite prescribed valuation word acts affinely over `ℚ`. -/
theorem collatzQWord_affine (w : List ℕ) (x : ℚ) :
    collatzQWord w x = collatzWordMul w * x + collatzWordAdd w := by
  induction w with
  | nil => simp [collatzQWord, collatzWordMul, collatzWordAdd]
  | cons a w ih =>
      simp only [collatzQWord]
      rw [ih]
      simp only [collatzQStep, collatzWordMul, collatzWordAdd]
      ring

/-- The exact finite-word contraction barrier.  It is defined whenever the
multiplicative coefficient is below one; the theorem below carries that
hypothesis explicitly. -/
def collatzBarrier (w : List ℕ) : ℚ :=
  collatzWordAdd w / (1 - collatzWordMul w)

/-- If the multiplicative part of a prescribed word is contracting, then the
word sends `x` below itself exactly when `x` lies above its affine barrier. -/
theorem collatzQWord_lt_self_iff_barrier_lt (w : List ℕ) (x : ℚ)
    (hmul : collatzWordMul w < 1) :
    collatzQWord w x < x ↔ collatzBarrier w < x := by
  rw [collatzQWord_affine]
  unfold collatzBarrier
  have hgap : 0 < 1 - collatzWordMul w := sub_pos.mpr hmul
  constructor
  · intro h
    apply (div_lt_iff₀ hgap).2
    linarith
  · intro h
    have hb := (div_lt_iff₀ hgap).1 h
    linarith

/-- The one-letter word `[2]` has multiplier `3/4`. -/
theorem collatzWordMul_two : collatzWordMul [2] = (3 : ℚ) / 4 := by
  norm_num [collatzWordMul]

/-- The one-letter word `[2]` has exact barrier `1`. -/
theorem collatzBarrier_two : collatzBarrier [2] = 1 := by
  norm_num [collatzBarrier, collatzWordAdd, collatzWordMul]

/-- Consequently the prescribed `a = 2` odd step contracts every rational
starting point strictly above one. -/
theorem collatzQWord_two_lt_self {x : ℚ} (hx : 1 < x) :
    collatzQWord [2] x < x := by
  norm_num [collatzQWord, collatzQStep]
  linarith

end CollatzFiniteWords

end OperatorFirst

/-! Explicit dependency reports for every theorem in this module. -/
#print axioms OperatorFirst.comm_add_sub
#print axioms OperatorFirst.normal_iff_comm_zero
#print axioms OperatorFirst.transpose_mul_of_symm
#print axioms OperatorFirst.reciprocity
#print axioms OperatorFirst.inner_mul_inner_swap
#print axioms OperatorFirst.gram_det
#print axioms OperatorFirst.gram_det_of_unit
#print axioms OperatorFirst.visibility_le_one
#print axioms OperatorFirst.one_sub_visibility_sq_nonneg
#print axioms OperatorFirst.duality
#print axioms OperatorFirst.gram_det_eq_distinguishability_sq
#print axioms OperatorFirst.visibility_self
#print axioms OperatorFirst.distinguishability_self
#print axioms OperatorFirst.distinguishability_of_orthogonal
#print axioms OperatorFirst.collatzQWord_affine
#print axioms OperatorFirst.collatzQWord_lt_self_iff_barrier_lt
#print axioms OperatorFirst.collatzWordMul_two
#print axioms OperatorFirst.collatzBarrier_two
#print axioms OperatorFirst.collatzQWord_two_lt_self
