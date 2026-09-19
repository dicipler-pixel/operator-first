/-
Copyright (c) 2026 Jeromie N. Beasley. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Jeromie N. Beasley
-/
module

public import Mathlib.LinearAlgebra.Matrix.SchurComplement

/-! # Congruence form of the Schur complement

`Mathlib/LinearAlgebra/Matrix/SchurComplement.lean` relates a block matrix to its Schur complement
through invertibility, `⅟`, and determinants. This file adds the remaining classical statement: a
symmetric block matrix is *congruent* to the block diagonal matrix formed by its Schur complement
and its invertible corner, via block triangular elimination.

This is the algebraic step underlying Sylvester's law of inertia, since congruence preserves
inertia while the block diagonal form exposes it.

## Main results

* `Matrix.fromBlocks_transpose_mul_self_mul_eq_of_invertible₂₂`: the congruence identity.
-/

@[expose] public section

variable {m n α : Type*}

namespace Matrix

open scoped Matrix

section CommRing

variable [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n] [CommRing α]

/-- The lower block triangular matrix eliminating the off-diagonal block of a symmetric block
matrix whose `₂₂` corner is invertible. -/
def schurElim (B : Matrix m n α) (D : Matrix n n α) [Invertible D] :
    Matrix (m ⊕ n) (m ⊕ n) α :=
  fromBlocks 1 0 (-(⅟D * Bᵀ)) 1

theorem transpose_schurElim (B : Matrix m n α) (D : Matrix n n α) [Invertible D]
    [Invertible Dᵀ] (hD : Dᵀ = D) :
    (schurElim B D)ᵀ = fromBlocks 1 (-(B * ⅟D)) 0 1 := by
  have h : (⅟D * Bᵀ)ᵀ = B * ⅟D := by
    rw [transpose_mul, transpose_transpose, transpose_invOf, hD]
  simp [schurElim, fromBlocks_transpose, h]

/-- **Congruence form of the Schur complement.** Block triangular elimination carries the symmetric
block matrix `[A B; Bᵀ D]`, with `D` invertible and symmetric, to the block diagonal matrix whose
corners are the Schur complement `A - B * ⅟D * Bᵀ` and `D` itself.

Congruence preserves inertia, so this identity is what lets an inertia computation for the block
matrix be read off the Schur complement. -/
theorem fromBlocks_transpose_mul_self_mul_eq_of_invertible₂₂
    (A : Matrix m m α) (B : Matrix m n α) (D : Matrix n n α)
    [Invertible D] [Invertible Dᵀ] (hD : Dᵀ = D) :
    (schurElim B D)ᵀ * fromBlocks A B Bᵀ D * schurElim B D =
      fromBlocks (A - B * ⅟D * Bᵀ) 0 0 D := by
  have hBD : B * ⅟D * D = B := by
    rw [Matrix.mul_assoc, invOf_mul_self, Matrix.mul_one]
  have hDB : D * (⅟D * Bᵀ) = Bᵀ := by
    rw [← Matrix.mul_assoc, mul_invOf_self, Matrix.one_mul]
  rw [transpose_schurElim B D hD]
  simp [schurElim, fromBlocks_multiply, sub_eq_add_neg, hBD, hDB]

end CommRing

end Matrix
