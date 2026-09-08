import Mathlib

/- Finite algebraic certificates for the combined paper. Standard identities
   are formalized as dependencies, not counted as new physical laws. -/
namespace ElementalFoundations

section Peirce
variable {R : Type*} [Ring R]
def cross (h p : R) : R := (1-p)*h*p+p*h*(1-p)

theorem cross_expansion (h p : R) :
    cross h p = h*p+p*h-(p*h*p+p*h*p) := by
  unfold cross
  noncomm_ring

theorem cross_commutator (h p : R) (hp : p*p=p) :
    p * cross h p - cross h p * p = p*h-h*p := by
  have hpph : p*p*h=p*h := by rw [hp]
  have hhpp : h*p*p=h*p := by rw [mul_assoc, hp]
  have hpphp : p*p*h*p=p*h*p := by rw [hp]
  have hphpp : p*h*p*p=p*h*p := by rw [mul_assoc (p*h), hp]
  calc
    p * cross h p - cross h p * p =
      p*p*h-h*p*p-2*(p*p*h*p)+2*(p*h*p*p) := by
        unfold cross
        noncomm_ring
    _ = p*h-h*p := by rw [hpph, hhpp, hpphp, hphpp]; noncomm_ring

theorem cross_zero_iff_commutes (h p : R) (hp : p*p=p) :
    cross h p=0 ↔ p*h=h*p := by
  constructor
  · intro hf
    have q := cross_commutator h p hp
    rw [hf, mul_zero, zero_mul, sub_self] at q
    exact sub_eq_zero.mp q.symm
  · intro hc
    have hphp : p*h*p = p*h := by
      rw [hc, mul_assoc, hp]
      exact hc.symm
    rw [cross_expansion, hphp, hc]
    noncomm_ring
end Peirce

def characteristic (s x : ℝ) : ℝ := x^2-s*x-1
def denominator (s x : ℝ) : ℝ := (characteristic s x)^2+(x-s)^2
def transmission (s x : ℝ) : ℝ := (x-s)^2 / denominator s x
def isolatedStrength (s : ℝ) : ℝ := 1/(s^2+4)

theorem centered_characteristic (s x : ℝ) :
    characteristic s (x+s/2)=x^2-(s^2+4)/4 := by
  unfold characteristic
  ring

theorem denominator_positive (s x : ℝ) : 0 < denominator s x := by
  by_cases h : x-s=0
  · have hx : x=s := sub_eq_zero.mp h
    subst x
    norm_num [denominator, characteristic]
  · have q := sq_pos_of_ne_zero h
    have z := sq_nonneg (characteristic s x)
    unfold denominator
    linarith

theorem denominator_expansion (s x : ℝ) :
    denominator s x = x^4-2*s*x^3+2+(s^2-1)*(x^2+1) := by
  unfold denominator characteristic
  ring

theorem mirror_transmission (x : ℝ) :
    transmission (-1) x = transmission 1 (-x) := by
  unfold transmission denominator characteristic
  congr 1 <;> ring

theorem initial_plus : transmission 1 0 = 1/2 := by
  norm_num [transmission, denominator, characteristic]

theorem initial_minus : transmission (-1) 0 = 1/2 := by
  norm_num [transmission, denominator, characteristic]

theorem isolated_optical_equal : isolatedStrength 1 = isolatedStrength (-1) := by
  norm_num [isolatedStrength]

theorem plus_later : transmission 1 (1/10) = 8100/19981 := by
  norm_num [transmission, denominator, characteristic]

theorem minus_later : transmission (-1) (1/10) = 12100/20021 := by
  norm_num [transmission, denominator, characteristic]

theorem later_distinct : transmission 1 (1/10) ≠ transmission (-1) (1/10) := by
  rw [plus_later, minus_later]
  norm_num

-- These identities certify the algebraic remainder. The manuscript uses
-- positivity and ordinary continuity to take the derivative limit.
theorem plus_first_order_remainder (x : ℝ) :
    2*denominator 1 x*(transmission 1 x-1/2+x) =
      x^2*(2+2*x-5*x^2+2*x^3) := by
  have hd := ne_of_gt (denominator_positive 1 x)
  unfold transmission
  field_simp
  unfold denominator characteristic
  ring

theorem minus_first_order_remainder (x : ℝ) :
    2*denominator (-1) x*(transmission (-1) x-1/2-x) =
      x^2*(2-2*x-5*x^2-2*x^3) := by
  have hd := ne_of_gt (denominator_positive (-1) x)
  unfold transmission
  field_simp
  unfold denominator characteristic
  ring

theorem no_conductance_only_predictor :
    ¬ ∃ f : ℝ → ℝ, ∀ s : ℝ, s=1 ∨ s=(-1) →
      f (transmission s 0)=transmission s (1/10) := by
  rintro ⟨f,h⟩
  have hp := h 1 (Or.inl rfl)
  have hm := h (-1) (Or.inr rfl)
  rw [initial_plus] at hp
  rw [initial_minus] at hm
  exact later_distinct (hp.symm.trans hm)

end ElementalFoundations

#print axioms ElementalFoundations.cross_expansion
#print axioms ElementalFoundations.cross_commutator
#print axioms ElementalFoundations.cross_zero_iff_commutes
#print axioms ElementalFoundations.centered_characteristic
#print axioms ElementalFoundations.denominator_positive
#print axioms ElementalFoundations.denominator_expansion
#print axioms ElementalFoundations.mirror_transmission
#print axioms ElementalFoundations.initial_plus
#print axioms ElementalFoundations.initial_minus
#print axioms ElementalFoundations.isolated_optical_equal
#print axioms ElementalFoundations.plus_later
#print axioms ElementalFoundations.minus_later
#print axioms ElementalFoundations.later_distinct
#print axioms ElementalFoundations.plus_first_order_remainder
#print axioms ElementalFoundations.minus_first_order_remainder
#print axioms ElementalFoundations.no_conductance_only_predictor
