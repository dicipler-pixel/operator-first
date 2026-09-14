import CollatzAlignment

/-!
# Collapse cylinder law

This module joins the two exact finite constraints already proved for an
accelerated Collatz valuation prefix:

* the binary realization cylinder supplied by an odd terminal state; and
* the Archimedean survival window supplied by the positive power gap.

The resulting theorem is finite and conditional. It does not assert global
Collatz convergence or exclude infinite compatible branches.
-/

namespace CollatzCollapseCylinder

open CollatzBarrier CollatzAlignment

/-- **Collapse cylinder law, exact finite form.**

A realized valuation prefix with an odd terminal state lies in its exact
binary phase cylinder. At a coefficient-contracting endpoint, survival above
the initial seed is equivalent to membership in the exact power-gap window.
The conjunction keeps realization and survival logically distinct. -/
theorem realized_cylinder_and_survival_window
    (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j))
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j) :
    (∃ k : ℕ,
      3 ^ j * x 0 + correction a j =
        2 ^ prefixSum a j + 2 ^ (prefixSum a j + 1) * k) ∧
    (x 0 ≤ x j ↔
      (2 ^ prefixSum a j - 3 ^ j) * x 0 ≤ correction a j) := by
  exact ⟨exact_terminal_phase a x j hstep hodd,
    collatz_prefix_survival_iff_gap_finite a x j hstep hpow⟩

/-- If the exact survival window ends below a cutoff `N`, every realized
surviving seed in the cylinder is below `N`. This is the finite collapse
statement: the cylinder has empty intersection with the surviving seed tail
`{n | N ≤ n}`. -/
theorem surviving_realizer_below_cutoff
    (a x : ℕ → ℕ) (j N : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j))
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j)
    (hgap : 0 < 2 ^ prefixSum a j - 3 ^ j)
    (hcertificate :
      correction a j <
        (2 ^ prefixSum a j - 3 ^ j) * N)
    (hstay : x 0 ≤ x j) :
    x 0 < N ∧
      ∃ k : ℕ,
        3 ^ j * x 0 + correction a j =
          2 ^ prefixSum a j + 2 ^ (prefixSum a j + 1) * k := by
  have hwindow :
      (2 ^ prefixSum a j - 3 ^ j) * x 0 ≤ correction a j :=
    (collatz_prefix_survival_iff_gap_finite a x j hstep hpow).mp hstay
  have hstrict :
      (2 ^ prefixSum a j - 3 ^ j) * x 0 <
        (2 ^ prefixSum a j - 3 ^ j) * N :=
    lt_of_le_of_lt hwindow hcertificate
  have hseed : x 0 < N := (Nat.mul_lt_mul_left hgap).mp hstrict
  exact ⟨hseed, exact_terminal_phase a x j hstep hodd⟩

/-- Equivalent exclusion form: no realized prefix can both survive and start
at or above a cutoff certified beyond its power-gap window. -/
theorem no_surviving_realizer_at_or_above_cutoff
    (a x : ℕ → ℕ) (j N : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j))
    (hpow : 3 ^ j ≤ 2 ^ prefixSum a j)
    (hgap : 0 < 2 ^ prefixSum a j - 3 ^ j)
    (hcertificate :
      correction a j <
        (2 ^ prefixSum a j - 3 ^ j) * N) :
    ¬ (N ≤ x 0 ∧ x 0 ≤ x j) := by
  rintro ⟨hlarge, hstay⟩
  have hsmall :=
    (surviving_realizer_below_cutoff a x j N hstep hodd hpow hgap
      hcertificate hstay).1
  exact (Nat.not_lt_of_ge hlarge) hsmall

end CollatzCollapseCylinder

#print axioms CollatzCollapseCylinder.realized_cylinder_and_survival_window
#print axioms CollatzCollapseCylinder.surviving_realizer_below_cutoff
#print axioms CollatzCollapseCylinder.no_surviving_realizer_at_or_above_cutoff
