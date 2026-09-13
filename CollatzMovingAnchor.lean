import CollatzRealization

/-!
# Exact Collatz phase cylinders -> moving-anchor interface

`CollatzRealization` proves that every actually realized finite odd-to-odd
valuation prefix places the *same initial seed* in an exact binary phase
cylinder modulo `2^(A_j+1)`.  This file isolates the logical bridge needed for
a pointwise obstruction.

For each depth `j`, suppose `anchor j` is any certified lower bound for every
natural seed in that phase cylinder.  Then an infinite realized odd-to-odd
orbit would force all of those moving anchors to stay below its fixed initial
seed.  Consequently, if the anchors escape every finite bound, no fixed seed
can realize all prefixes.

The escape premise is intentionally left explicit.  This file does not prove
moving-anchor anti-concentration, arbitrary-word nonrealizability, exclusion of
cycles, or the Collatz conjecture.  It formalizes exactly where such a new
pointwise arithmetic input would enter.
-/

namespace CollatzMovingAnchor

open CollatzBarrier
open CollatzRealization

/-- The exact phase cylinder forced at depth `j` by terminal oddness. -/
def phaseCylinder (a : ℕ → ℕ) (j seed : ℕ) : Prop :=
  (3 ^ j * seed + correction a j) % 2 ^ (prefixSum a j + 1) =
    (2 ^ prefixSum a j) % 2 ^ (prefixSum a j + 1)

/-- Any actually realized finite odd-to-odd prefix lies in its exact phase
cylinder. -/
theorem realized_prefix_mem_phaseCylinder
    (a x : ℕ → ℕ) (j : ℕ)
    (hstep : ∀ i < j, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : Odd (x j)) :
    phaseCylinder a j (x 0) := by
  exact exact_terminal_phase_mod a x j hstep hodd

/-- If `anchor j` lower-bounds every seed in the depth-`j` cylinder, then one
fixed seed lying in every cylinder bounds the entire moving-anchor sequence. -/
theorem fixed_seed_bounds_phase_anchors
    (a : ℕ → ℕ) (anchor : ℕ → ℕ) (seed : ℕ)
    (hmin : ∀ j n, phaseCylinder a j n → anchor j ≤ n)
    (hseed : ∀ j, phaseCylinder a j seed) :
    ∀ j, anchor j ≤ seed := by
  intro j
  exact hmin j seed (hseed j)

/-- Contrapositive pointwise interface: if certified phase anchors escape every
finite bound, no single natural seed can lie in all exact phase cylinders. -/
theorem phase_anchor_escape_excludes_fixed_seed
    (a : ℕ → ℕ) (anchor : ℕ → ℕ)
    (hmin : ∀ j n, phaseCylinder a j n → anchor j ≤ n)
    (hEscape : ∀ B : ℕ, ∃ j, B < anchor j) :
    ¬ ∃ seed : ℕ, ∀ j, phaseCylinder a j seed := by
  rintro ⟨seed, hseed⟩
  obtain ⟨j, hj⟩ := hEscape seed
  have hle : anchor j ≤ seed := hmin j seed (hseed j)
  exact (not_lt_of_ge hle) hj

/-- An infinite odd-to-odd realization of one valuation sequence would keep any
certified phase-anchor lower bounds uniformly below the initial seed.  This is
the exact finite-to-pointwise compatibility statement behind the moving-anchor
bottleneck. -/
theorem infinite_realization_bounds_phase_anchors
    (a x : ℕ → ℕ) (anchor : ℕ → ℕ)
    (hmin : ∀ j n, phaseCylinder a j n → anchor j ≤ n)
    (hstep : ∀ i, 2 ^ a i * x (i + 1) = 3 * x i + 1)
    (hodd : ∀ j, Odd (x j)) :
    ∀ j, anchor j ≤ x 0 := by
  intro j
  apply hmin j (x 0)
  exact realized_prefix_mem_phaseCylinder a x j
    (fun i _ => hstep i) (hodd j)

/-- Therefore an escaping moving-anchor lower bound excludes an infinite
odd-to-odd realization of that valuation sequence.  The theorem consumes the
escape property; it does not manufacture it. -/
theorem phase_anchor_escape_excludes_infinite_realization
    (a : ℕ → ℕ) (anchor : ℕ → ℕ)
    (hmin : ∀ j n, phaseCylinder a j n → anchor j ≤ n)
    (hEscape : ∀ B : ℕ, ∃ j, B < anchor j) :
    ¬ ∃ x : ℕ → ℕ,
      (∀ i, 2 ^ a i * x (i + 1) = 3 * x i + 1) ∧
      (∀ j, Odd (x j)) := by
  rintro ⟨x, hstep, hodd⟩
  obtain ⟨j, hj⟩ := hEscape (x 0)
  have hle : anchor j ≤ x 0 :=
    infinite_realization_bounds_phase_anchors a x anchor hmin hstep hodd j
  exact (not_lt_of_ge hle) hj

end CollatzMovingAnchor

#print axioms CollatzMovingAnchor.realized_prefix_mem_phaseCylinder
#print axioms CollatzMovingAnchor.fixed_seed_bounds_phase_anchors
#print axioms CollatzMovingAnchor.phase_anchor_escape_excludes_fixed_seed
#print axioms CollatzMovingAnchor.infinite_realization_bounds_phase_anchors
#print axioms CollatzMovingAnchor.phase_anchor_escape_excludes_infinite_realization
