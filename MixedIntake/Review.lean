import Mathlib

/-!
Four-file review, 5 September 2026, Jeromie Beasley corpus.
Original FCS/AK files remain separate. These are scoped algebraic checks, not
proofs of all prose claims. The Euler layer bound is a premise; full planarity
and arboricity are not encoded. No cosmological identification, optical-needle
theorem, full YB entropy bound, or fixed-cumulant impossibility is claimed.
This revision repairs three errors reported by the actual compiler: explicit
finite-index reduction, an already completed tactic, and Boolean precedence.
-/
noncomputable section
open scoped BigOperators
namespace MixedReview

def logQuadratic (a b c x : ℝ) := a*x^2 + b*x + c

theorem real_logquadratic_odds (a b c L : ℝ) :
    logQuadratic a b c 0 - logQuadratic a b c L = -L*(a*L+b) := by
  unfold logQuadratic
  ring

theorem real_logquadratic_zero_iff (a b c L : ℝ) (hL : L ≠ 0) :
    logQuadratic a b c 0 - logQuadratic a b c L = 0 ↔ b = -a*L := by
  rw [real_logquadratic_odds]
  constructor
  · intro h
    have hh : a*L+b = 0 := (mul_eq_zero.mp h).resolve_left (neg_ne_zero.mpr hL)
    linarith
  · intro h
    rw [h]
    ring

/-- The variance matters as well as the mean. -/
theorem gaussian_mean_variance (L mu variance : ℝ) (hv : variance ≠ 0) :
    (-(0-mu)^2/(2*variance)) - (-(L-mu)^2/(2*variance)) =
      L*(L-2*mu)/(2*variance) := by
  field_simp
  ring

theorem third_filling_sign (a b L : ℝ) (h : 3*b = -2*a*L) :
    3*(-L*(a*L+b)) = -a*L^2 := by
  linear_combination -L*h

theorem common_mean_different_gaussian_odds :
    (4 : ℚ)*(4-2*1)/(2*1) = 4 ∧
    (4 : ℚ)*(4-2*1)/(2*2) = 2 := by norm_num

def law0 : Fin 5 → ℚ := ![24/625,154/625,269/625,154/625,24/625]
def law1 : Fin 5 → ℚ := ![241/6250,1537/6250,2693/6250,1539/6250,240/6250]

theorem laws_normalized : (∑ i, law0 i) = 1 ∧ (∑ i, law1 i) = 1 := by
  norm_num [law0, law1, Fin.sum_univ_succ]

theorem laws_positive : (∀ i, 0 < law0 i) ∧ (∀ i, 0 < law1 i) := by
  constructor <;> intro i <;> fin_cases i <;> norm_num [law0, law1]

theorem laws_same_first_two_moments :
    (∑ i, (i.val : ℚ)*law0 i) = 2 ∧
    (∑ i, (i.val : ℚ)*law1 i) = 2 ∧
    (∑ i, (i.val : ℚ)^2*law0 i) = 24/5 ∧
    (∑ i, (i.val : ℚ)^2*law1 i) = 24/5 := by
  norm_num [law0, law1, Fin.sum_univ_succ]

theorem laws_different_endpoint_odds :
    law0 0 / law0 4 = 1 ∧ law1 0 / law1 4 = 241/240 := by
  change (24/625 : ℚ)/(24/625) = 1 ∧ (241/6250 : ℚ)/(240/6250) = 241/240
  norm_num

/-- This is strict < 67/40, unlike the original weak threshold. -/
theorem strict_granularity (p q : ℕ) (hq : q < 43) (h : 40*p < 67*q) :
    3*p ≤ 5*q := by omega

theorem strict_threshold_sharp : 40*72 < 67*43 ∧ 5*43 < 3*72 := by omega

/-- The substantive floor hypothesis must be supplied independently. -/
theorem floor_exclusion_conditional (p q : ℕ) (hfloor : 16*q ≤ 9*p) :
    ¬ 9*p < 16*q := by omega

theorem density_le_score (m n r t : ℝ) (hm : 0 ≤ m) (hn : 0 < n)
    (hr : 0 ≤ r) (ht : 0 ≤ t) (hnt : t < n) :
    m/n ≤ (m+r)/(n-t) := by
  apply (div_le_div_iff₀ hn (sub_pos.mpr hnt)).2
  nlinarith [mul_nonneg hm ht, mul_nonneg hr (le_of_lt hn)]

theorem product_density_adds (m1 n1 m2 n2 : ℚ) (hn1 : n1 ≠ 0) (hn2 : n2 ≠ 0) :
    (m1*n2+n1*m2)/(n1*n2) = m1/n1+m2/n2 := by
  field_simp <;> ring

/-- This uses a specified lower bound, not an assumed graph construction. -/
theorem katz_tao_product_budget (k : ℕ) (score : ℝ)
    (hlower : (k : ℝ)*(7/6) ≤ score) (hupper : score ≤ 67/40) : k ≤ 1 := by
  by_contra h
  have hk : 2 ≤ k := by omega
  have hkr : (2 : ℝ) ≤ k := by exact_mod_cast hk
  nlinarith

/-- Arithmetic countermodel only; no feasible forcing graph is asserted. -/
theorem density_not_score_monotonicity :
    (1 : ℚ)/10 < 20/100 ∧
    (20 : ℚ)/100 < (1+19)/10 := by norm_num

section Braid
variable {R : Type*} [CommRing R]

def phaseDefect (a b k x y z : R) : R :=
  k*(x*y+(x+b)*z+(y+a)*(z+a)-y*z-x*(z+a)-(x+b)*(y+b))

theorem phase_defect_expansion (a b k x y z : R) :
    phaseDefect a b k x y z =
      k*((a+b)*(z-x)+(a-b)*y+a^2-b^2) := by
  unfold phaseDefect
  ring

/-- In ZMod d these are exponent congruences; the character interpretation is separate. -/
theorem phase_defect_zero_iff (a b k : R) :
    (∀ x y z : R, phaseDefect a b k x y z = 0) ↔
    k*(a+b)=0 ∧ k*(a-b)=0 := by
  constructor
  · intro h
    have h0 := h 0 0 0
    have hy := h 0 1 0
    have hz := h 0 0 1
    simp only [phaseDefect] at h0 hy hz
    constructor
    · linear_combination hz-h0
    · linear_combination hy-h0
  · rintro ⟨hp,hm⟩ x y z
    unfold phaseDefect
    linear_combination (z-x)*hp+(y+a+b)*hm

theorem unshifted_phase_braids (k x y z : R) : phaseDefect 0 0 k x y z = 0 := by
  unfold phaseDefect
  ring
end Braid

theorem odd_field_shift_constraint {F : Type*} [Field F]
    (a b k : F) (hk : k ≠ 0) (h2 : (2:F) ≠ 0)
    (h : k*(a+b)=0 ∧ k*(a-b)=0) : a=0 ∧ b=0 := by
  have hp : a+b=0 := (mul_eq_zero.mp h.1).resolve_left hk
  have hm : a-b=0 := (mul_eq_zero.mp h.2).resolve_left hk
  have ha : 2*a=0 := by linear_combination hp+hm
  have hb : 2*b=0 := by linear_combination hp-hm
  exact ⟨(mul_eq_zero.mp ha).resolve_left h2, (mul_eq_zero.mp hb).resolve_left h2⟩

/-- Planarity is not encoded; its Euler inequalities and edge cover are premises. -/
theorem trianglefree_two_layer_bound (N edges e1 e2 : ℤ)
    (hcover : edges ≤ e1+e2) (h1 : e1 ≤ 2*N-4) (h2 : e2 ≤ 2*N-4) :
    edges ≤ 4*N-8 := by omega

theorem inflated_join_exceeds_capacity (n r : ℤ) (hn : 1 ≤ n) (hr : 4 ≤ r) :
    4*(r*n)-8 < r^2*n := by
  have hh : 0 ≤ (r-4)*(r*n) :=
    mul_nonneg (by omega) (mul_nonneg (by omega) (by omega))
  nlinarith

theorem closing_edges_budget (n c : ℤ)
    (h : 16*(n-1)+c ≤ 4*(4*n)-8) : c ≤ 8 := by omega

theorem nine_closures_excluded (n : ℤ) : 4*(4*n)-8 < 16*(n-1)+9 := by omega

theorem total_edge_test_boundary (n : ℤ) :
    (22*n ≤ 24*n-12 ↔ 6 ≤ n) := by omega

def cycle7Adj (i j : Fin 7) : Bool :=
  decide ((i.val+1)%7=j.val ∨ (j.val+1)%7=i.val)

theorem cycle7_trianglefree :
    ∀ i j k : Fin 7, (cycle7Adj i j && cycle7Adj j k && cycle7Adj k i) = false := by
  decide

theorem inflated_cycle7_trianglefree :
    ∀ x y z : Fin 7 × Fin 4,
    (cycle7Adj x.1 y.1 && cycle7Adj y.1 z.1 && cycle7Adj z.1 x.1) = false := by
  intro x y z
  exact cycle7_trianglefree x.1 y.1 z.1

theorem seven_fibre_counts :
    7*4=28 ∧ 7*6=42 ∧ 7*16=112 ∧ 42+112=154 ∧
    6*28-12=156 ∧ 4*28-8=104 ∧ 104<112 := by omega

end MixedReview

#print axioms MixedReview.real_logquadratic_odds
#print axioms MixedReview.real_logquadratic_zero_iff
#print axioms MixedReview.gaussian_mean_variance
#print axioms MixedReview.third_filling_sign
#print axioms MixedReview.common_mean_different_gaussian_odds
#print axioms MixedReview.laws_normalized
#print axioms MixedReview.laws_positive
#print axioms MixedReview.laws_same_first_two_moments
#print axioms MixedReview.laws_different_endpoint_odds
#print axioms MixedReview.strict_granularity
#print axioms MixedReview.strict_threshold_sharp
#print axioms MixedReview.floor_exclusion_conditional
#print axioms MixedReview.density_le_score
#print axioms MixedReview.product_density_adds
#print axioms MixedReview.katz_tao_product_budget
#print axioms MixedReview.density_not_score_monotonicity
#print axioms MixedReview.phase_defect_expansion
#print axioms MixedReview.phase_defect_zero_iff
#print axioms MixedReview.unshifted_phase_braids
#print axioms MixedReview.odd_field_shift_constraint
#print axioms MixedReview.trianglefree_two_layer_bound
#print axioms MixedReview.inflated_join_exceeds_capacity
#print axioms MixedReview.closing_edges_budget
#print axioms MixedReview.nine_closures_excluded
#print axioms MixedReview.total_edge_test_boundary
#print axioms MixedReview.cycle7_trianglefree
#print axioms MixedReview.inflated_cycle7_trianglefree
#print axioms MixedReview.seven_fibre_counts
