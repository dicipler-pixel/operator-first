import LightBridges
import OpticalMetric
import Rigidity

/-! Finite completion steps for the light paper. These statements concern the
specified scalar response model, not a derivation of Maxwell or a general
identification of optical response with transport rigidity. -/
set_option autoImplicit false
noncomputable section
namespace LightCompletion

/-- Equal field metrics need not have equal static polarizabilities. -/
theorem same_metric_different_static_response :
    LightConstitutive.transitionMetric 1 1 = LightConstitutive.transitionMetric 2 2 ∧
    LightConstitutive.polarizability 1 1 0 = 2 ∧
    LightConstitutive.polarizability 2 2 0 = 4 := by
  norm_num [LightConstitutive.transitionMetric, LightConstitutive.polarizability]

def twoPoleZero (a b A B : ℝ) : ℝ := (A*b+B*a)/(A+B)

/-- The tune-out is strictly between the two squared-gap poles. -/
theorem two_pole_zero_between (a b A B : ℝ)
    (hab : a < b) (hA : 0 < A) (hB : 0 < B) :
    a < twoPoleZero a b A B ∧ twoPoleZero a b A B < b := by
  have hp : 0 < A+B := add_pos hA hB
  unfold twoPoleZero
  constructor
  · apply (lt_div_iff₀ hp).2
    nlinarith
  · apply (div_lt_iff₀ hp).2
    nlinarith

/-- Clearing the two explicitly nonzero response denominators. -/
theorem two_pole_numerator (a b A B y : ℝ)
    (ha : a-y ≠ 0) (hb : b-y ≠ 0) :
    A/(a-y)+B/(b-y) = (A*b+B*a-(A+B)*y)/((a-y)*(b-y)) := by
  field_simp
  <;> ring

/-- Unique response zero away from the two poles. -/
theorem two_pole_zero_iff (a b A B y : ℝ)
    (hs : A+B ≠ 0) (ha : a-y ≠ 0) (hb : b-y ≠ 0) :
    A/(a-y)+B/(b-y) = 0 ↔ y = twoPoleZero a b A B := by
  rw [two_pole_numerator a b A B y ha hb, div_eq_zero_iff]
  simp only [mul_ne_zero ha hb, or_false]
  unfold twoPoleZero
  rw [eq_div_iff hs]
  constructor <;> intro h <;> nlinarith [h]

/-- The positive-residue two-pole model really attains the interior zero. -/
theorem two_pole_tuneout (a b A B : ℝ)
    (hab : a < b) (hA : 0 < A) (hB : 0 < B) :
    A/(a-twoPoleZero a b A B)+B/(b-twoPoleZero a b A B)=0 := by
  have h := two_pole_zero_between a b A B hab hA hB
  exact (two_pole_zero_iff a b A B _ (ne_of_gt (add_pos hA hB))
    (ne_of_lt (sub_neg.mpr h.1)) (ne_of_gt (sub_pos.mpr h.2))).2 rfl

/-- Calibration denominator increases with the field metric. -/
theorem calibration_product_strict (g h eta k : ℝ)
    (hg : 0 ≤ g) (hgh : g < h) (he : 0 < eta) (hk : 0 < k) :
    (g+eta)*(1+k*g) < (h+eta)*(1+k*h) := by
  have hh : 0 ≤ h := le_trans hg (le_of_lt hgh)
  have hp : 0 < (h-g)*(1+k*(h+g+eta)) :=
    mul_pos (sub_pos.mpr hgh) (by positivity)
  nlinarith [hp]

/-- The natural scalar field-Jacobian choice s_min^2=g cannot be proportional
to 1+k*g at two distinct nonnegative metric values with a fixed regulator.
This excludes that choice only, not every possible transport operator. -/
theorem no_fixed_calibration_for_field_jacobian (g h eta k c : ℝ)
    (hg : 0 ≤ g) (hgh : g < h) (he : 0 < eta) (hk : 0 < k)
    (hc : c ≠ 0)
    (h1 : 1/(g+eta)=c*(1+k*g))
    (h2 : 1/(h+eta)=c*(1+k*h)) : False := by
  have dg : g+eta ≠ 0 := ne_of_gt (by positivity)
  have dh : h+eta ≠ 0 := ne_of_gt (by linarith)
  have e1 := (div_eq_iff dg).1 h1
  have e2 := (div_eq_iff dh).1 h2
  have eqp : c*((g+eta)*(1+k*g)) = c*((h+eta)*(1+k*h)) := by
    nlinarith [e1,e2]
  have eq := mul_left_cancel₀ hc eqp
  exact (ne_of_lt (calibration_product_strict g h eta k hg hgh he hk)) eq

end LightCompletion
