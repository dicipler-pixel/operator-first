import Mathlib.Tactic

/- Algebraic certificates only. No assertion of exact Mordell--Weil rank,
   novelty of a published family, or infinitude for an unresolved equation. -/
namespace DiophantineEye

def surface (a b c x y z : ℤ) : ℤ := z^2 + (y^2+a)*z + x^3 + b*x + c

theorem discriminant_identity (a b c x y z : ℤ) :
    4 * surface a b c x y z =
      (2*z+y^2+a)^2 - ((y^2+a)^2 - 4*(x^3+b*x+c)) := by
  unfold surface
  ring

-- Published by Epoch, March 2026. This is an independently checked reproduction.
theorem epoch_polynomial_family (t : ℤ) :
    surface 0 1 1 (-108*t^4-24*t^2-2) (36*t^3+2*t)
      (648*t^6+288*t^4+50*t^2+3) = 0 := by
  unfold surface
  ring

theorem epoch_congruence_family (u s : ℤ) (h : u^3+930*s=368) :
    surface (-1) 0 2 (u*s) (s+2) (-31*s^2+4*s-1) = 0 := by
  have hi : surface (-1) 0 2 (u*s) (s+2) (-31*s^2+4*s-1) =
      s^3*(u^3+930*s-368) := by unfold surface; ring
  rw [hi, h]
  ring

-- Numerators of x=N/(4q²), y=3(1-u²)/(2q), w=3uN/(2q³), q=1+u².
-- The rational section identity after multiplying by 16q^6.
theorem circle_section_cleared (u : ℚ) :
    36*u^2*(u^4-34*u^2+1)^2
      -81*(1-u^2)^4*(1+u^2)^2
      +(u^4-34*u^2+1)^3
      +16*(u^4-34*u^2+1)*(1+u^2)^4
      +64*(1+u^2)^6 = 0 := by ring

theorem circle_denominator_positive (u : ℚ) : 0 < 1+u^2 := by positivity

theorem pell_norm_preserved (A x v r s : ℤ) (h : r^2-A*s^2=1) :
    (A*s*x+r*v)^2-A*(r*x+s*v)^2 = v^2-A*x^2 := by
  calc
    (A*s*x+r*v)^2-A*(r*x+s*v)^2 =
        (r^2-A*s^2)*(v^2-A*x^2) := by ring
    _ = v^2-A*x^2 := by rw [h]; ring

-- Grechuk--Agbanwa tangent identity, independently formalized algebraic part.
theorem tangent_identity (m r s d : ℤ) :
    4*m*(m+r*s+s^2*d) = (2*m+r*s)^2+s^2*(4*m*d-r^2) := by ring

end DiophantineEye

#print axioms DiophantineEye.discriminant_identity
#print axioms DiophantineEye.epoch_polynomial_family
#print axioms DiophantineEye.epoch_congruence_family
#print axioms DiophantineEye.circle_section_cleared
#print axioms DiophantineEye.circle_denominator_positive
#print axioms DiophantineEye.pell_norm_preserved
#print axioms DiophantineEye.tangent_identity
