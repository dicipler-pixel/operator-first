import Mathlib

/-!
# Mixed-file audit, 5 September 2026
Jeromie Beasley's four-file review. These statements do NOT formalize a full
biplanarity theorem, quantum-circuit Schmidt growth, Gaussian approximation
error, or attainability of arithmetic Kakeya scores. They isolate the exact
algebra and counterexamples that the surrounding claims must respect.
-/
noncomputable section
open scoped BigOperators
namespace OperatorFirst.MixedAudit

/-- Real rather than integer log-quadratic data; no normalization assumed. -/
def logQuadratic (a b c x : ℝ) : ℝ := a*x^2 + b*x + c

theorem real_logodds (a b c L : ℝ) :
    logQuadratic a b c 0 - logQuadratic a b c L = -L*(a*L+b) := by
  unfold logQuadratic
  ring

theorem real_zero_iff_center (a b c L : ℝ) (hL : L ≠ 0) :
    logQuadratic a b c 0 - logQuadratic a b c L = 0 ↔ b = -a*L := by
  rw [real_logodds]
  constructor
  · intro h
    have h' : a*L+b=0 := (mul_eq_zero.mp h).resolve_left (neg_ne_zero.mpr hL)
    linarith
  · intro h
    rw [h]
    ring

theorem real_third_filling (a b L : ℝ) (h : 3*b = -2*a*L) :
    3*(-L*(a*L+b)) = -a*L^2 := by
  nlinarith [mul_eq_mul_left_iff.mpr (Or.inl h : 3*b = -2*a*L ∨ L = 0)]

/-- A noncentral Gaussian shape can have nonzero extreme log-odds. -/
theorem gaussian_offcenter_control :
    logQuadratic (-1) 3 0 0 - logQuadratic (-1) 3 0 4 = 4 := by
  norm_num [logQuadratic]

/-- Two normalized finite laws with equal first two moments but unequal endpoint odds.
Their independent-mode realizability is established separately, not here. -/
def law0 : Fin 5 → ℚ := ![240/6250,1540/6250,2690/6250,1540/6250,240/6250]
def law1 : Fin 5 → ℚ := ![241/6250,1537/6250,2693/6250,1539/6250,240/6250]

theorem laws_positive : (∀ i, 0 < law0 i) ∧ (∀ i, 0 < law1 i) := by
  constructor <;> intro i <;> fin_cases i <;> norm_num [law0, law1]

theorem laws_normalized : (∑ i, law0 i)=1 ∧ (∑ i, law1 i)=1 := by
  norm_num [law0,law1,Fin.sum_univ_succ]

theorem laws_same_mean :
    (∑ i : Fin 5, (i.val : ℚ)*law0 i)=2 ∧
    (∑ i : Fin 5, (i.val : ℚ)*law1 i)=2 := by
  norm_num [law0,law1,Fin.sum_univ_succ]

theorem laws_same_second_moment :
    (∑ i : Fin 5, (i.val : ℚ)^2*law0 i)=24/5 ∧
    (∑ i : Fin 5, (i.val : ℚ)^2*law1 i)=24/5 := by
  norm_num [law0,law1,Fin.sum_univ_succ]

theorem laws_distinct_endpoint_odds :
    law0 0 / law0 4 = 1 ∧ law1 0 / law1 4 = 241/240 ∧
    law0 0 / law0 4 ≠ law1 0 / law1 4 := by
  change (240/6250 : ℚ)/(240/6250)=1 ∧
    (241/6250 : ℚ)/(240/6250)=241/240 ∧
    (240/6250 : ℚ)/(240/6250) ≠ (241/6250)/(240/6250)
  norm_num

/-- Rational-score interpretation requires positive denominators. -/
theorem granularity_guarded (p q : ℕ) (hq0 : 0 < q) (hq : q < 40)
    (h : (p : ℚ)/q ≤ 67/40) : (p : ℚ)/q ≤ 5/3 := by
  have hqp : (0 : ℚ) < q := by exact_mod_cast hq0
  have hpq : (40 : ℚ)*p ≤ 67*q := by
    have := (div_le_iff₀ hqp).mp h
    linarith
  have hint : 40*p ≤ 67*q := by exact_mod_cast hpq
  have hsmall : 3*p ≤ 5*q := by omega
  apply (div_le_iff₀ hqp).mpr
  have hsmall' : (3 : ℚ)*p ≤ 5*q := by exact_mod_cast hsmall
  linarith

/-- Matching the target at q=40, not strictly improving it. -/
theorem target_threshold_control :
    (5/3 : ℚ) < 67/40 ∧ (67/40 : ℚ) ≤ 67/40 := by norm_num

/-- The original 'below_floor_excluded' premise is satisfiable. -/
theorem floor_premise_is_consistent : (9 : ℕ)*1 < 16*1 := by decide

theorem product_density (m1 n1 m2 n2 : ℚ) (h1 : n1 ≠ 0) (h2 : n2 ≠ 0) :
    (m1*n2+n1*m2)/(n1*n2) = m1/n1+m2/n2 := by
  field_simp
  <;> ring

/-- The edge density is a lower bound, not a comparison with a prior full score. -/
theorem score_above_density (m r n t : ℚ)
    (hm : 0 ≤ m) (hr : 0 ≤ r) (ht : 0 ≤ t) (hfree : t < n) :
    m/n ≤ (m+r)/(n-t) := by
  have hn : 0 < n := lt_of_le_of_lt ht hfree
  rw [div_le_div_iff₀ hn (sub_pos.mpr hfree)]
  nlinarith [mul_nonneg hm ht, mul_nonneg hr (le_of_lt hn)]

/-- Counts alone permit a smaller full score while density rises. NOT a forcing witness. -/
theorem density_does_not_compare_full_scores :
    (3/4 : ℚ) < 24/16 ∧ ((3+5)/4 : ℚ) > (24+6)/16 := by norm_num

theorem eventual_score_exclusion (score m n copies bound : ℚ)
    (hscore : copies*m/n ≤ score) (hbound : bound < copies*m/n) :
    bound < score := lt_of_lt_of_le hbound hscore

/-- Scalar arithmetic after applying the two planar triangle-free bounds. -/
theorem two_layer_capacity (e e1 e2 N : ℤ)
    (hcover : e ≤ e1+e2) (h1 : e1 ≤ 2*N-4) (h2 : e2 ≤ 2*N-4) :
    e ≤ 4*N-8 := by omega

theorem four_inflation_exceeds_capacity (n : ℤ) :
    ¬ (16*n ≤ 16*n-8) := by omega

theorem inflation_exceeds_capacity (r n : ℤ) (hr : 4 ≤ r) (hn : 0 ≤ n) :
    ¬ (r^2*n ≤ 4*r*n-8) := by
  have hprod : 0 ≤ r*n*(r-4) :=
    mul_nonneg (mul_nonneg (by omega) hn) (by omega)
  nlinarith

/-- Nine restored joins already exceed the capacity; not a sufficiency claim at eight. -/
theorem ninth_closing_edge_obstruction (n k : ℤ) (hk : 9 ≤ k) :
    ¬ (16*(n-1)+k ≤ 16*n-8) := by omega

theorem whole_graph_count_control :
    (88 : ℤ)>84 ∧ (110 : ℤ)>108 ∧ (132 : ℤ)=132 ∧ (154 : ℤ)<156 := by omega

section Phase
variable {R : Type*} [CommRing R]

def braidPhaseDifference (k a b x y z : R) : R :=
  k*(x*y+(x+b)*z+(y+a)*(z+a)-y*z-x*(z+a)-(x+b)*(y+b))

theorem phase_difference_factorization (k a b x y z : R) :
    braidPhaseDifference k a b x y z =
      k*(a+b)*(z-x) + k*(a-b)*y + k*(a-b)*(a+b) := by
  unfold braidPhaseDifference
  ring

/-- Use R=ZMod d for equality of root-of-unity exponents. -/
theorem phase_compatibility_iff (k a b : R) :
    (∀ x y z, braidPhaseDifference k a b x y z = 0) ↔
      k*(a+b)=0 ∧ k*(a-b)=0 := by
  constructor
  · intro h
    have h0 := h 0 0 0
    have hz := h 0 0 1
    have hy := h 0 1 0
    rw [phase_difference_factorization] at h0 hz hy
    constructor
    · linear_combination hz-h0
    · linear_combination hy-h0
  · rintro ⟨hs,hd⟩ x y z
    rw [phase_difference_factorization, hs, hd]
    ring

theorem unshifted_phase_braids (k x y z : R) :
    braidPhaseDifference k 0 0 x y z = 0 := by
  unfold braidPhaseDifference
  ring
end Phase

/-- A count increase need not have a finite minimum entropy increase. This is only
an exact weighted-probability control, not a continuity theorem for entropy. -/
theorem extra_channel_weight_control (e : ℝ) (he0 : 0 < e) (he1 : e < 1) :
    0 < e ∧ 0 < 1-e ∧ (1-e)+e=1 := by
  exact ⟨he0, sub_pos.mpr he1, by ring⟩

end OperatorFirst.MixedAudit

#print axioms OperatorFirst.MixedAudit.real_logodds
#print axioms OperatorFirst.MixedAudit.real_zero_iff_center
#print axioms OperatorFirst.MixedAudit.real_third_filling
#print axioms OperatorFirst.MixedAudit.gaussian_offcenter_control
#print axioms OperatorFirst.MixedAudit.laws_positive
#print axioms OperatorFirst.MixedAudit.laws_normalized
#print axioms OperatorFirst.MixedAudit.laws_same_mean
#print axioms OperatorFirst.MixedAudit.laws_same_second_moment
#print axioms OperatorFirst.MixedAudit.laws_distinct_endpoint_odds
#print axioms OperatorFirst.MixedAudit.granularity_guarded
#print axioms OperatorFirst.MixedAudit.target_threshold_control
#print axioms OperatorFirst.MixedAudit.floor_premise_is_consistent
#print axioms OperatorFirst.MixedAudit.product_density
#print axioms OperatorFirst.MixedAudit.score_above_density
#print axioms OperatorFirst.MixedAudit.density_does_not_compare_full_scores
#print axioms OperatorFirst.MixedAudit.eventual_score_exclusion
#print axioms OperatorFirst.MixedAudit.two_layer_capacity
#print axioms OperatorFirst.MixedAudit.four_inflation_exceeds_capacity
#print axioms OperatorFirst.MixedAudit.inflation_exceeds_capacity
#print axioms OperatorFirst.MixedAudit.ninth_closing_edge_obstruction
#print axioms OperatorFirst.MixedAudit.whole_graph_count_control
#print axioms OperatorFirst.MixedAudit.phase_difference_factorization
#print axioms OperatorFirst.MixedAudit.phase_compatibility_iff
#print axioms OperatorFirst.MixedAudit.unshifted_phase_braids
#print axioms OperatorFirst.MixedAudit.extra_channel_weight_control
