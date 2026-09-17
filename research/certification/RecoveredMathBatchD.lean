import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Recovered math batch D

Finite-difference mechanics kernels, a stronger rank-one metric control,
and a discrete Lyapunov monotonicity theorem.

These statements certify ordinary mathematics only. They do not certify a
physical interpretation of the recovered framework.
-/

namespace RecoveredMathBatchD

/-! ## 1. Difference-quotient kernels for the oscillator kinetic term -/

/-- Exact finite-difference quotient for the quadratic kinetic term.
The derivative `m*v` is recovered in the limit `h -> 0`; this theorem itself
is the exact algebraic identity before taking that limit. -/
theorem quadratic_kinetic_difference_quotient
    (m v h : ℝ) (hh : h ≠ 0) :
    (((1 / 2 : ℝ) * m * (v + h) ^ 2) -
      ((1 / 2 : ℝ) * m * v ^ 2)) / h =
      m * v + (1 / 2 : ℝ) * m * h := by
  field_simp [hh]
  ring

/-- Exact finite-difference quotient for a squared-distance Lyapunov term. -/
theorem squared_distance_difference_quotient
    (x x0 h : ℝ) (hh : h ≠ 0) :
    (((x + h - x0) ^ 2) - ((x - x0) ^ 2)) / h =
      2 * (x - x0) + h := by
  field_simp [hh]
  ring

/-! ## 2. Stronger rank-one / outer-product degeneracy control -/

/-- The rank-one outer-product matrix built from `(a,b)` annihilates the
perpendicular vector `(-b,a)`. This is stronger than just saying its
determinant vanishes. -/
theorem outer_product_annihilates_perp (a b : ℝ) :
    (a * a * (-b) + a * b * a = 0) ∧
    (a * b * (-b) + b * b * a = 0) := by
  constructor <;> ring

/-- If `(a,b)` is not the zero pair, then the perpendicular vector `(-b,a)`
is also nonzero. Combined with `outer_product_annihilates_perp`, this gives
an explicit nontrivial kernel vector. -/
theorem perp_vector_nonzero_of_pair_nonzero
    (a b : ℝ) (h : a ≠ 0 ∨ b ≠ 0) :
    (-b ≠ 0) ∨ (a ≠ 0) := by
  rcases h with ha | hb
  · exact Or.inr ha
  · exact Or.inl (neg_ne_zero.mpr hb)

/-- Concrete singular-kernel statement for a nonzero two-component gradient. -/
theorem nonzero_outer_product_has_nontrivial_kernel
    (a b : ℝ) (h : a ≠ 0 ∨ b ≠ 0) :
    ((a * a * (-b) + a * b * a = 0) ∧
     (a * b * (-b) + b * b * a = 0)) ∧
    ((-b ≠ 0) ∨ (a ≠ 0)) := by
  exact ⟨outer_product_annihilates_perp a b,
    perp_vector_nonzero_of_pair_nonzero a b h⟩

/-! ## 3. Discrete Lyapunov monotonicity -/

/-- If a scalar sequence never increases from one step to the next, then every
later value is bounded above by the initial value. This is the exact safe core
behind using `V_{n+1} ≤ V_n` as a Lyapunov-style monotonicity condition. -/
theorem stepwise_nonincreasing_le_initial
    (V : ℕ → ℝ) (hstep : ∀ n, V (n + 1) ≤ V n) :
    ∀ n, V n ≤ V 0 := by
  intro n
  induction n with
  | zero => exact le_rfl
  | succ n ih =>
      have hs : V (n + 1) ≤ V n := hstep n
      exact le_trans hs ih

/-- If every step is strictly decreasing, then every positive-index value is
strictly below the initial value. This still does not imply convergence to a
particular equilibrium without additional hypotheses. -/
theorem stepwise_strict_decrease_below_initial
    (V : ℕ → ℝ) (hstep : ∀ n, V (n + 1) < V n) :
    ∀ n, 0 < n → V n < V 0 := by
  intro n hn
  cases n with
  | zero => simp at hn
  | succ n =>
      exact lt_of_lt_of_le (hstep n)
        (stepwise_nonincreasing_le_initial V (fun k => (hstep k).le) n)

#print axioms RecoveredMathBatchD.quadratic_kinetic_difference_quotient
#print axioms RecoveredMathBatchD.squared_distance_difference_quotient
#print axioms RecoveredMathBatchD.outer_product_annihilates_perp
#print axioms RecoveredMathBatchD.perp_vector_nonzero_of_pair_nonzero
#print axioms RecoveredMathBatchD.nonzero_outer_product_has_nontrivial_kernel
#print axioms RecoveredMathBatchD.stepwise_nonincreasing_le_initial
#print axioms RecoveredMathBatchD.stepwise_strict_decrease_below_initial

end RecoveredMathBatchD
