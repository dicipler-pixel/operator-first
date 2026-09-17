/-
GLOBAL CONTROLLER / FAST-SLOW KERNEL

This file formalizes only an elementary mathematical core suggested by the
"global controller" research idea. It does NOT formalize cosmology, artificial
intelligence, thermodynamic gravity, superluminal signalling, or a physical
identification of a cosmological constant.

The model is a scalar quadratic consistency penalty with a relaxation step.
Theorems establish:
  * nonnegativity and exact zero set of the penalty;
  * the exact error update under relaxation;
  * contraction for 0 <= gamma <= 1;
  * a larger admissible relaxation rate contracts the same scalar residual at
    least as much as a smaller one.

These statements are intended as a finite kernel for later operator/projector
and fast-slow generalizations.
-/

import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

namespace OperatorFirst.GlobalConstraint

/-- Squared deviation from a target state. -/
def quadraticError (x target : ℝ) : ℝ := (x - target) ^ 2

/-- A nonnegative weighted consistency penalty when `w >= 0`. -/
def weightedPenalty (w x target : ℝ) : ℝ := w * quadraticError x target

/-- One explicit relaxation step toward the target. -/
def relax (γ x target : ℝ) : ℝ := x - γ * (x - target)

/-- Squared consistency error is always nonnegative. -/
theorem quadraticError_nonneg (x target : ℝ) : 0 ≤ quadraticError x target := by
  exact sq_nonneg (x - target)

/-- A nonnegative weight gives a nonnegative consistency penalty. -/
theorem weightedPenalty_nonneg (w x target : ℝ) (hw : 0 ≤ w) :
    0 ≤ weightedPenalty w x target := by
  exact mul_nonneg hw (quadraticError_nonneg x target)

/-- With a strictly positive weight, zero penalty is equivalent to exact target matching. -/
theorem weightedPenalty_eq_zero_iff (w x target : ℝ) (hw : 0 < w) :
    weightedPenalty w x target = 0 ↔ x = target := by
  constructor
  · intro h
    have hw0 : w ≠ 0 := ne_of_gt hw
    have hsq : quadraticError x target = 0 := by
      exact (mul_eq_zero.mp h).resolve_left hw0
    rw [quadraticError] at hsq
    nlinarith
  · intro h
    subst h
    simp [weightedPenalty, quadraticError]

/-- Exact residual update for one relaxation step. -/
theorem relax_error (γ x target : ℝ) :
    relax γ x target - target = (1 - γ) * (x - target) := by
  simp [relax]
  ring

/-- Exact squared-error update for one relaxation step. -/
theorem relax_quadraticError (γ x target : ℝ) :
    quadraticError (relax γ x target) target =
      (1 - γ) ^ 2 * quadraticError x target := by
  rw [quadraticError, relax_error, quadraticError]
  ring

/-- Any relaxation rate in `[0,1]` cannot increase the scalar consistency error. -/
theorem relax_contracts (γ x target : ℝ) (hγ0 : 0 ≤ γ) (hγ1 : γ ≤ 1) :
    quadraticError (relax γ x target) target ≤ quadraticError x target := by
  rw [relax_quadraticError]
  have hfactor : (1 - γ) ^ 2 ≤ 1 := by
    nlinarith
  have herr : 0 ≤ quadraticError x target := quadraticError_nonneg x target
  calc
    (1 - γ) ^ 2 * quadraticError x target
        ≤ 1 * quadraticError x target := mul_le_mul_of_nonneg_right hfactor herr
    _ = quadraticError x target := by ring

/-- If two admissible rates act on the same residual, the larger rate leaves no
more squared error after one step. This is the precise finite meaning used here
for a "faster" controller; it is not a claim about signal propagation speed. -/
theorem larger_rate_contracts_at_least_as_much
    (γslow γfast x target : ℝ)
    (hslow0 : 0 ≤ γslow)
    (hrates : γslow ≤ γfast)
    (hfast1 : γfast ≤ 1) :
    quadraticError (relax γfast x target) target ≤
      quadraticError (relax γslow x target) target := by
  rw [relax_quadraticError, relax_quadraticError]
  have hfast0 : 0 ≤ γfast := le_trans hslow0 hrates
  have hsum : 0 ≤ 2 - γfast - γslow := by
    nlinarith
  have hdiff : 0 ≤ γfast - γslow := sub_nonneg.mpr hrates
  have hprod : 0 ≤ (γfast - γslow) * (2 - γfast - γslow) :=
    mul_nonneg hdiff hsum
  have hfactor : (1 - γfast) ^ 2 ≤ (1 - γslow) ^ 2 := by
    nlinarith
  have herr : 0 ≤ quadraticError x target := quadraticError_nonneg x target
  exact mul_le_mul_of_nonneg_right hfactor herr

/-- Strictly positive rate below one gives strict contraction away from the target. -/
theorem relax_strict_contracts
    (γ x target : ℝ)
    (hγ0 : 0 < γ)
    (hγ1 : γ < 1)
    (hne : x ≠ target) :
    quadraticError (relax γ x target) target < quadraticError x target := by
  rw [relax_quadraticError]
  have herr : 0 < quadraticError x target := by
    rw [quadraticError]
    exact sq_pos_of_ne_zero (sub_ne_zero.mpr hne)
  have hfactor0 : 0 ≤ (1 - γ) ^ 2 := sq_nonneg _
  have hfactor1 : (1 - γ) ^ 2 < 1 := by
    nlinarith
  calc
    (1 - γ) ^ 2 * quadraticError x target
        < 1 * quadraticError x target :=
          mul_lt_mul_of_pos_right hfactor1 herr
    _ = quadraticError x target := by ring

end OperatorFirst.GlobalConstraint

#print axioms OperatorFirst.GlobalConstraint.quadraticError_nonneg
#print axioms OperatorFirst.GlobalConstraint.weightedPenalty_nonneg
#print axioms OperatorFirst.GlobalConstraint.weightedPenalty_eq_zero_iff
#print axioms OperatorFirst.GlobalConstraint.relax_error
#print axioms OperatorFirst.GlobalConstraint.relax_quadraticError
#print axioms OperatorFirst.GlobalConstraint.relax_contracts
#print axioms OperatorFirst.GlobalConstraint.larger_rate_contracts_at_least_as_much
#print axioms OperatorFirst.GlobalConstraint.relax_strict_contracts
