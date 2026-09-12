import Mathlib

/-!
# Two-rail relative transport: minimal topology tests

This module formalizes only group-level statements needed to separate
"two sectors" from "two independent cycles".  No physical interpretation is
assumed by the theorems.
-/

namespace TwoRailGeometry

variable {G : Type*} [Group G]

/-- Relative transport between two sector holonomies on the same closed path. -/
def relativeHolonomy (uγ um : G) : G := uγ * um⁻¹

/-- Group commutator of two independent path holonomies. -/
def commutator (u v : G) : G := u * v * u⁻¹ * v⁻¹

/-- Minimal algebraic condition imposed by a torus representation: the two
fundamental-cycle holonomies commute. -/
def torusCompatible (u v : G) : Prop := u * v = v * u

/-- A figure-eight/free-two-loop stage imposes no commutation relation at the
group level; the two generators are independent. -/
def figureEightCompatible (_u _v : G) : Prop := True

/-- Zero relative holonomy means the two rail holonomies coincide. -/
theorem relativeHolonomy_eq_one_iff (uγ um : G) :
    relativeHolonomy uγ um = 1 ↔ uγ = um := by
  constructor
  · intro h
    have h' := congrArg (fun z : G => z * um) h
    simpa [relativeHolonomy, mul_assoc] using h'
  · intro h
    subst h
    simp [relativeHolonomy]

/-- Every pair of group elements is admissible at the free figure-eight stage. -/
theorem figureEightCompatible_all (u v : G) : figureEightCompatible u v := by
  trivial

/-- Torus compatibility is strictly an additional relation beyond the free
figure-eight stage. -/
theorem torus_implies_figureEight (u v : G) (h : torusCompatible u v) :
    figureEightCompatible u v := by
  trivial

/-- If the two independent holonomies commute (the torus relation), their
commutator is trivial. -/
theorem commutator_eq_one_of_torusCompatible (u v : G)
    (h : torusCompatible u v) : commutator u v = 1 := by
  unfold torusCompatible at h
  unfold commutator
  calc
    u * v * u⁻¹ * v⁻¹ = v * u * u⁻¹ * v⁻¹ := by rw [h]
    _ = 1 := by simp

/-- Two different sectors can already have a nontrivial relative holonomy on a
single path; no second topological generator is required for this algebraic
notion. -/
theorem nontrivial_relative_of_ne (uγ um : G) (h : uγ ≠ um) :
    relativeHolonomy uγ um ≠ 1 := by
  intro h1
  exact h ((relativeHolonomy_eq_one_iff uγ um).mp h1)

end TwoRailGeometry

#print axioms TwoRailGeometry.relativeHolonomy_eq_one_iff
#print axioms TwoRailGeometry.figureEightCompatible_all
#print axioms TwoRailGeometry.torus_implies_figureEight
#print axioms TwoRailGeometry.commutator_eq_one_of_torusCompatible
#print axioms TwoRailGeometry.nontrivial_relative_of_ne
