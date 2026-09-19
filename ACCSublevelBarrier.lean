import ACCFrontier

/-!
# Target-outside sublevel barrier theorem

This file isolates the abstract theorem needed for an ACC Proof Track
submission about exact elementary bottleneck lower bounds.

It does not claim the Andrews--Curtis conjecture, or any particular numerical
barrier.  Numerical instances require an independently checked finite
sublevel component and a proof/certificate that the target is absent from it.
-/

namespace ACCSublevelBarrier

variable {State Move : Type}

/-- If a path starts in a cap-closed set C and ends at a target outside C,
then some visited state has height strictly above the cap. -/
theorem target_outside_forces_peak
    (step : State → Move → State)
    (height : State → ℕ)
    (C : Set State)
    (B : ℕ)
    {start target : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hclosed : ∀ s ∈ C, ∀ m, height (step s m) ≤ B → step s m ∈ C)
    (htarget : target ∉ C)
    (hrun : ACCWell.run step start ms = target) :
    ∃ s ∈ ACCWell.trace step start ms, B < height s := by
  by_contra hno
  push Not at hno
  have hfinal : ACCWell.run step start ms ∈ C :=
    ACCWell.run_mem_of_bounded_trace step height C B ms hstart hclosed hno
  have ht : target ∈ C := by
    simpa [hrun] using hfinal
  exact htarget ht

/-- Stronger edge form: any path to a target outside C traverses an actual
directed first-exit edge from C whose target height exceeds the cap. -/
theorem target_outside_forces_above_cap_edge
    (step : State → Move → State)
    (height : State → ℕ)
    (C : Set State)
    (B : ℕ)
    {start target : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hclosed : ∀ s ∈ C, ∀ m, height (step s m) ≤ B → step s m ∈ C)
    (htarget : target ∉ C)
    (hrun : ACCWell.run step start ms = target) :
    ∃ e ∈ ACCFrontier.edgeTrace step start ms,
      e.1 ∈ C ∧ step e.1 e.2 ∉ C ∧ B < height (step e.1 e.2) := by
  have hout : ACCWell.run step start ms ∉ C := by
    intro h
    apply htarget
    simpa [hrun] using h
  exact ACCFrontier.cap_closed_exit_forces_above_cap_edge
    step height C B ms hstart hclosed hout

end ACCSublevelBarrier

#print axioms ACCSublevelBarrier.target_outside_forces_peak
#print axioms ACCSublevelBarrier.target_outside_forces_above_cap_edge
