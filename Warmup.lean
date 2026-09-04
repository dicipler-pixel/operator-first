/-
SCRIPT: WARMUP-MATHLIB-02

Two warm-up results from "Light Keeps the Ledger" (Jeromie Beasley),
https://doi.org/10.5281/zenodo.22124938

  T1  the commutator identity   [S+K, S-K] = -2 [S,K]
      corollary                 C = S+K is normal  <->  [S,K] = 0
  T2  reciprocity               B symmetric, V B-symmetric  ->  x (BV) y = y (BV) x

Each is stated for the most general setting in which it is true: T1 for an
arbitrary ring, T2 for square matrices over any commutative ring.
-/

import Mathlib

namespace OperatorFirst

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

end OperatorFirst
