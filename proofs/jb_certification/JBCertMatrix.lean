/-!
# JB certification — matrix specialisations

`JB-PROJ-001` for invertible matrices in the paper's conventions, and `JB-PROJ-002`, the
Kronecker mixed-product kernel with its projector consequence (the finite algebra under
Proposition 7 of *What Transport Keeps*; the normalised-stress formula itself is not stated
here because it needs the Frobenius norm and is fenced until that layer is formalised).
-/
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Data.Matrix.Kronecker
import JBCertCore

open Matrix
open scoped Kronecker

namespace JBCert

variable {K : Type*} [Field K] {n : Type*} [Fintype n] [DecidableEq n]

/-- `JB-PROJ-001` (matrices, Theorem 3 convention). Rows are `1 × n` matrices and
columns `n × 1`, so `ℓ * x` is the `1 × 1` pairing `ℓᵀ x`. With `xₙ₊₁ = A xₙ` and
`ℓₙ₊₁ᵀ = ℓₙᵀ A⁻¹` (that is `ℓₙ₊₁ = A⁻ᵀ ℓₙ`), the pairing is conserved for invertible `A`. -/
theorem pairing_conserved_dual (ℓ : Matrix (Fin 1) n K) (x : Matrix n (Fin 1) K)
    (A : Matrix n n K) (hA : IsUnit A.det) :
    (ℓ * A⁻¹) * (A * x) = ℓ * x := by
  rw [Matrix.mul_assoc, ← Matrix.mul_assoc A⁻¹, Matrix.nonsing_inv_mul A hA, Matrix.one_mul]

/-- `JB-PROJ-001` (matrices, handoff convention `ℓ ↦ ℓ M`, `z ↦ M⁻¹ z`). -/
theorem pairing_conserved_matrix (ℓ : Matrix (Fin 1) n K) (z : Matrix n (Fin 1) K)
    (M : Matrix n n K) (hM : IsUnit M.det) :
    (ℓ * M) * (M⁻¹ * z) = ℓ * z := by
  rw [Matrix.mul_assoc, ← Matrix.mul_assoc M, Matrix.mul_nonsing_inv M hM, Matrix.one_mul]

/-- Theorem 3, moving coordinate change `x' = S⁻¹ x`, `ℓ'ᵀ = ℓᵀ S`. -/
theorem pairing_gauge_invariant_matrix (ℓ : Matrix (Fin 1) n K) (x : Matrix n (Fin 1) K)
    (S : Matrix n n K) (hS : IsUnit S.det) :
    (ℓ * S) * (S⁻¹ * x) = ℓ * x :=
  pairing_conserved_matrix ℓ x S hS

section Kronecker

variable {l m l' p q p' : Type*} [Fintype m] [Fintype q]

/-- `JB-PROJ-002` (Kronecker mixed product), in the handoff's orientation
`(A ⊗ B)(C ⊗ D) = (A C) ⊗ (B D)`. -/
theorem kronecker_mixed_product (A : Matrix l m K) (B : Matrix p q K)
    (C : Matrix m l' K) (D : Matrix q p' K) :
    (A ⊗ₖ B) * (C ⊗ₖ D) = (A * C) ⊗ₖ (B * D) :=
  (Matrix.mul_kronecker_mul A C B D).symm

variable {r : Type*} [Fintype r]

/-- Projector consequence: a Kronecker product of idempotents is idempotent.
No spectral, norm or convergence statement is attached. -/
theorem kronecker_idempotent (P : Matrix n n K) (Q : Matrix r r K)
    (hP : P * P = P) (hQ : Q * Q = Q) :
    (P ⊗ₖ Q) * (P ⊗ₖ Q) = P ⊗ₖ Q := by
  rw [kronecker_mixed_product, hP, hQ]

end Kronecker

end JBCert
