import MatrixResolvedBoundary
import Mathlib.Data.Matrix.Block

/-!
# Finite symmetric Schur block congruence

This module formalizes only the finite block-algebra step underlying an inertia
transfer.  It does not assert an eigenvalue-count theorem, infinite-dimensional
Schur/Feshbach theory, representation completeness, or a Yang--Mills gap.
-/

open Matrix

namespace CrossTheorem

variable {r h : Type*} [Fintype r] [Fintype h] [DecidableEq r] [DecidableEq h]

/-- Symmetric real block matrix. -/
def symBlock (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D : Matrix h h ℝ) :
    Matrix (Sum r h) (Sum r h) ℝ :=
  Matrix.fromBlocks A B B.transpose D

/-- Lower triangular Schur elimination matrix. -/
def schurElim (B : Matrix r h ℝ) (R : Matrix h h ℝ) :
    Matrix (Sum r h) (Sum r h) ℝ :=
  Matrix.fromBlocks 1 0 (-(R * B.transpose)) 1

/-- Finite Schur complement with an explicit hidden inverse `R`. -/
def schurComplement (A : Matrix r r ℝ) (B : Matrix r h ℝ)
    (R : Matrix h h ℝ) : Matrix r r ℝ :=
  A - B * R * B.transpose

/-- Exact block congruence.  Under two-sided inverse and symmetry hypotheses for
`R` and `D`, triangular elimination sends the symmetric block matrix to the
block diagonal matrix with Schur complement and hidden block.

This is the algebraic step needed before any Sylvester-inertia transfer. -/
theorem schur_congruence
    (A : Matrix r r ℝ) (B : Matrix r h ℝ) (D R : Matrix h h ℝ)
    (hDR : D * R = 1)
    (hRD : R * D = 1)
    (hDsymm : D.transpose = D)
    (hRsymm : R.transpose = R) :
    (schurElim B R).transpose * symBlock A B D * schurElim B R =
      Matrix.fromBlocks (schurComplement A B R) 0 0 D := by
  ext i j
  cases i <;> cases j <;>
    simp [schurElim, symBlock, schurComplement, Matrix.fromBlocks_multiply,
      Matrix.transpose_fromBlocks, Matrix.transpose_mul, hDR, hRD, hDsymm, hRsymm,
      Matrix.mul_assoc] <;>
    ring_nf

/-- The explicit elimination matrix has an explicit inverse when no spectral
assumption beyond the displayed algebra is needed. -/
def schurElimInv (B : Matrix r h ℝ) (R : Matrix h h ℝ) :
    Matrix (Sum r h) (Sum r h) ℝ :=
  Matrix.fromBlocks 1 0 (R * B.transpose) 1

/-- The elimination change of variables is genuinely invertible. -/
theorem schurElim_mul_inv
    (B : Matrix r h ℝ) (R : Matrix h h ℝ) :
    schurElim B R * schurElimInv B R = 1 := by
  ext i j
  cases i <;> cases j <;>
    simp [schurElim, schurElimInv, Matrix.fromBlocks_multiply] <;>
    ring

/-- Reverse inverse identity. -/
theorem schurElimInv_mul
    (B : Matrix r h ℝ) (R : Matrix h h ℝ) :
    schurElimInv B R * schurElim B R = 1 := by
  ext i j
  cases i <;> cases j <;>
    simp [schurElim, schurElimInv, Matrix.fromBlocks_multiply] <;>
    ring

end CrossTheorem

#print axioms CrossTheorem.schur_congruence
#print axioms CrossTheorem.schurElim_mul_inv
#print axioms CrossTheorem.schurElimInv_mul
