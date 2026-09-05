import Mathlib

/-! Finite probability controls. Not an independent-mode realizability theorem,
not a uniform approximation theorem, and not a gravitational identification. -/
open scoped BigOperators
noncomputable section
namespace OperatorFirst.FCSMoments

def law (t : ℝ) : Fin 4 → ℝ := ![1/4-t,1/4+3*t,1/4-3*t,1/4+t]
def moment (p : Fin 4 → ℝ) (k : ℕ) : ℝ := ∑ i, (i.val : ℝ)^k * p i

theorem law_positive (t : ℝ) (ht : |t| < 1/12) : ∀ i, 0 < law t i := by
  have hb := abs_lt.mp ht
  intro i
  fin_cases i <;> simp [law] <;> linarith

theorem law_normalized (t : ℝ) : moment (law t) 0 = 1 := by
  norm_num [moment, law, Fin.sum_univ_succ]
  ring

theorem law_mean (t : ℝ) : moment (law t) 1 = 3/2 := by
  norm_num [moment, law, Fin.sum_univ_succ]
  ring

theorem law_second_moment (t : ℝ) : moment (law t) 2 = 7/2 := by
  norm_num [moment, law, Fin.sum_univ_succ]
  ring

theorem law_third_central_moment (t : ℝ) :
    (∑ i : Fin 4, ((i.val : ℝ)-3/2)^3 * law t i) = 6*t := by
  norm_num [law, Fin.sum_univ_succ]
  ring

theorem unequal_endpoints (t : ℝ) (ht : t ≠ 0) : law t 0 ≠ law t 3 := by
  change 1/4-t ≠ 1/4+t
  intro h
  apply ht
  linarith

/-- Finite support matters: four moments determine all four weights.
This is an actual injectivity statement, not merely an example. -/
theorem four_moments_determine_law (p q : Fin 4 → ℝ)
    (h0 : moment p 0 = moment q 0) (h1 : moment p 1 = moment q 1)
    (h2 : moment p 2 = moment q 2) (h3 : moment p 3 = moment q 3) : p = q := by
  norm_num [moment, Fin.sum_univ_succ] at h0 h1 h2 h3
  change p 0+(p 1+(p 2+p 3)) = q 0+(q 1+(q 2+q 3)) at h0
  change p 1+(2*p 2+3*p 3) = q 1+(2*q 2+3*q 3) at h1
  change p 1+(4*p 2+9*p 3) = q 1+(4*q 2+9*q 3) at h2
  change p 1+(8*p 2+27*p 3) = q 1+(8*q 2+27*q 3) at h3
  funext i
  fin_cases i
  · change p 0 = q 0; linarith
  · change p 1 = q 1; linarith
  · change p 2 = q 2; linarith
  · change p 3 = q 3; linarith

theorem first_two_moments_not_injective :
    moment (law 0) 0 = moment (law (1/24)) 0 ∧
    moment (law 0) 1 = moment (law (1/24)) 1 ∧
    moment (law 0) 2 = moment (law (1/24)) 2 ∧ law 0 ≠ law (1/24) := by
  refine ⟨by rw [law_normalized,law_normalized],
    by rw [law_mean,law_mean], by rw [law_second_moment,law_second_moment], ?_⟩
  intro h
  have he := congrFun h 0
  norm_num [law] at he

end OperatorFirst.FCSMoments
#print axioms OperatorFirst.FCSMoments.law_positive
#print axioms OperatorFirst.FCSMoments.law_normalized
#print axioms OperatorFirst.FCSMoments.law_mean
#print axioms OperatorFirst.FCSMoments.law_second_moment
#print axioms OperatorFirst.FCSMoments.law_third_central_moment
#print axioms OperatorFirst.FCSMoments.unequal_endpoints
#print axioms OperatorFirst.FCSMoments.four_moments_determine_law
#print axioms OperatorFirst.FCSMoments.first_two_moments_not_injective
