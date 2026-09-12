import Mathlib

/-!
# Projector conjugation derivative without circular dynamics assumptions

This module proves only an entrywise finite-dimensional calculus statement.
We assume differentiability data for two matrix paths `U,V` at zero and derive
the derivative of `U(t) P V(t)`. No matrix exponential, unitarity, Hamiltonian
interpretation, or spacetime claim is assumed.
-/

open Matrix
open scoped BigOperators

namespace ProjectorConjugationDerivative

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- Entrywise derivative of a finite matrix product. -/
theorem hasDerivAt_matrix_mul
    (U V : ℝ → Matrix n n ℝ) (U0 V0 KU KV : Matrix n n ℝ)
    (hU0 : U 0 = U0) (hV0 : V 0 = V0)
    (hU : ∀ i j, HasDerivAt (fun t => U t i j) (KU i j) 0)
    (hV : ∀ i j, HasDerivAt (fun t => V t i j) (KV i j) 0) :
    ∀ i j,
      HasDerivAt (fun t => (U t * V t) i j)
        ((KU * V0 + U0 * KV) i j) 0 := by
  intro i j
  simp only [Matrix.mul_apply, Matrix.add_apply]
  have hsum := HasDerivAt.fun_sum (u := Finset.univ)
    (fun k _ => (hU i k).mul (hV k j))
  simpa [hU0, hV0, Matrix.mul_apply, Finset.sum_add_distrib] using hsum

/-- First derivative of a two-sided transported projector/state matrix.
The derivative data are explicit; no relation between `U` and `V` is assumed. -/
theorem hasDerivAt_two_sided_transport
    (U V : ℝ → Matrix n n ℝ) (P KU KV : Matrix n n ℝ)
    (hU0 : U 0 = 1) (hV0 : V 0 = 1)
    (hU : ∀ i j, HasDerivAt (fun t => U t i j) (KU i j) 0)
    (hV : ∀ i j, HasDerivAt (fun t => V t i j) (KV i j) 0) :
    ∀ i j,
      HasDerivAt (fun t => (U t * P * V t) i j)
        ((KU * P + P * KV) i j) 0 := by
  intro i j
  have hUP : ∀ a b,
      HasDerivAt (fun t => (U t * P) a b)
        ((KU * P) a b) 0 := by
    intro a b
    have hconst : ∀ p q,
        HasDerivAt (fun _ : ℝ => P p q) 0 0 := by
      intro p q
      simpa using (hasDerivAt_const (x := (0 : ℝ)) (c := P p q))
    have h := hasDerivAt_matrix_mul U (fun _ => P) 1 P KU 0
      hU0 rfl hU hconst a b
    simpa using h
  have hprod := hasDerivAt_matrix_mul
    (fun t => U t * P) V P 1 (KU * P) KV
    (by simp [hU0]) hV0 hUP hV i j
  simpa [Matrix.mul_assoc] using hprod

/-- If the right transport derivative is the negative of the left derivative,
the transported projector derivative is exactly a commutator. -/
theorem hasDerivAt_conjugation_commutator
    (U V : ℝ → Matrix n n ℝ) (P K : Matrix n n ℝ)
    (hU0 : U 0 = 1) (hV0 : V 0 = 1)
    (hU : ∀ i j, HasDerivAt (fun t => U t i j) (K i j) 0)
    (hV : ∀ i j, HasDerivAt (fun t => V t i j) ((-K) i j) 0) :
    ∀ i j,
      HasDerivAt (fun t => (U t * P * V t) i j)
        ((K * P - P * K) i j) 0 := by
  intro i j
  have h := hasDerivAt_two_sided_transport U V P K (-K) hU0 hV0 hU hV i j
  simpa [sub_eq_add_neg, Matrix.mul_neg] using h

/-- A commutator-zero generator gives zero first-order projector motion under
any two-sided transport with opposite endpoint derivatives. -/
theorem hasDerivAt_conjugation_zero_of_commute
    (U V : ℝ → Matrix n n ℝ) (P K : Matrix n n ℝ)
    (hcomm : K * P = P * K)
    (hU0 : U 0 = 1) (hV0 : V 0 = 1)
    (hU : ∀ i j, HasDerivAt (fun t => U t i j) (K i j) 0)
    (hV : ∀ i j, HasDerivAt (fun t => V t i j) ((-K) i j) 0) :
    ∀ i j,
      HasDerivAt (fun t => (U t * P * V t) i j) 0 0 := by
  intro i j
  have h := hasDerivAt_conjugation_commutator U V P K hU0 hV0 hU hV i j
  have hz : K * P - P * K = 0 := by rw [hcomm, sub_self]
  rw [hz] at h
  simpa using h

end ProjectorConjugationDerivative

#print axioms ProjectorConjugationDerivative.hasDerivAt_matrix_mul
#print axioms ProjectorConjugationDerivative.hasDerivAt_two_sided_transport
#print axioms ProjectorConjugationDerivative.hasDerivAt_conjugation_commutator
#print axioms ProjectorConjugationDerivative.hasDerivAt_conjugation_zero_of_commute
