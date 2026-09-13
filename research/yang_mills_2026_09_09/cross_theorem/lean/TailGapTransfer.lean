import SchurCongruence

/-!
# Nonuniform hidden-tail budget -> retained gap

This file isolates the finite scalar inequality needed after the exact Schur
congruence.  Think of `base` as the retained quadratic form on a test vector,
`tail i` as the adverse contribution of hidden sector `i`, and `scale` as the
positive normalization (typically a squared norm).

The key point is deliberately one-sided: to lower-bound

`base - ∑ i, tail i`

we only need an upper bound on each adverse tail contribution.  We do not need
an absolute-value bound unless that is the only estimate available.  The tail
budgets may be completely nonuniform; only their total enters the surviving
gap.

This is finite algebra only.  It does not prove the Yang--Mills polymer
activity/locality estimate, a volume-uniform spectral gap, a continuum limit,
or Osterwalder--Schrader reconstruction.  Those remain separate analytic
obligations.
-/

open scoped BigOperators

namespace CrossTheorem

variable {ι : Type*} [Fintype ι] [DecidableEq ι]

/-- Heterogeneous one-sided tail budgets add with no uniform-allocation
assumption.  Each component may consume a different amount of the total
budget. -/
theorem nonuniform_tail_sum_le
    (tail eps : ι → ℝ) (scale : ℝ)
    (htail : ∀ i, tail i ≤ eps i * scale) :
    (∑ i, tail i) ≤ (∑ i, eps i) * scale := by
  calc
    (∑ i, tail i) ≤ ∑ i, eps i * scale := by
      exact Finset.sum_le_sum (fun i _ => htail i)
    _ = (∑ i, eps i) * scale := by
      rw [Finset.sum_mul]

/-- **Nonuniform gap transfer.**  If the retained/base form has lower margin
`δ * scale` and hidden component `i` contributes at most `eps i * scale`, then
a margin `δ - ∑ eps i` survives after subtracting all hidden contributions.
No equal split such as `eps i = δ / #ι` is required. -/
theorem gap_transfer_of_nonuniform_tail
    (base : ℝ) (tail eps : ι → ℝ) (δ scale : ℝ)
    (hbase : δ * scale ≤ base)
    (htail : ∀ i, tail i ≤ eps i * scale) :
    (δ - ∑ i, eps i) * scale ≤ base - ∑ i, tail i := by
  have hsum : (∑ i, tail i) ≤ (∑ i, eps i) * scale :=
    nonuniform_tail_sum_le tail eps scale htail
  calc
    (δ - ∑ i, eps i) * scale =
        δ * scale - (∑ i, eps i) * scale := by ring
    _ ≤ base - ∑ i, tail i := by linarith

/-- A strictly positive retained margin follows whenever the total heterogeneous
tail budget is strictly smaller than the base gap and the normalization is
strictly positive. -/
theorem positive_gap_of_nonuniform_tail
    (base : ℝ) (tail eps : ι → ℝ) (δ scale : ℝ)
    (hscale : 0 < scale)
    (hbase : δ * scale ≤ base)
    (htail : ∀ i, tail i ≤ eps i * scale)
    (hbudget : (∑ i, eps i) < δ) :
    0 < base - ∑ i, tail i := by
  have hmargin : 0 < (δ - ∑ i, eps i) * scale :=
    mul_pos (sub_pos.mpr hbudget) hscale
  exact lt_of_lt_of_le hmargin
    (gap_transfer_of_nonuniform_tail base tail eps δ scale hbase htail)

/-- Existing absolute-value/norm estimates can feed the sharper one-sided
transfer immediately.  This adapter makes explicit that absolute control is
sufficient but not logically necessary. -/
theorem gap_transfer_of_absolute_tail
    (base : ℝ) (tail eps : ι → ℝ) (δ scale : ℝ)
    (hbase : δ * scale ≤ base)
    (htail : ∀ i, |tail i| ≤ eps i * scale) :
    (δ - ∑ i, eps i) * scale ≤ base - ∑ i, tail i := by
  apply gap_transfer_of_nonuniform_tail base tail eps δ scale hbase
  intro i
  exact le_trans (le_abs_self (tail i)) (htail i)

end CrossTheorem

#print axioms CrossTheorem.nonuniform_tail_sum_le
#print axioms CrossTheorem.gap_transfer_of_nonuniform_tail
#print axioms CrossTheorem.positive_gap_of_nonuniform_tail
#print axioms CrossTheorem.gap_transfer_of_absolute_tail
