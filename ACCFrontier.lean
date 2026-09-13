import ACCWell

/-!
# Complete first-exit frontier theorem

This file formalizes the graph-theoretic statement needed by the ACC frontier
search.  It deliberately does **not** assume that a first cap exit increases the
height by exactly one.  For Andrews--Curtis moves that would be an additional
claim and is false in general: a legal move may jump across more than one
length level.
-/

namespace ACCFrontier

variable {State Move : Type}

/-- The directed move edges actually traversed by a finite move list. -/
def edgeTrace (step : State → Move → State) : State → List Move → List (State × Move)
  | _, [] => []
  | s, m :: ms => (s, m) :: edgeTrace step (step s m) ms

@[simp] theorem edgeTrace_nil (step : State → Move → State) (s : State) :
    edgeTrace step s [] = [] := rfl

@[simp] theorem edgeTrace_cons (step : State → Move → State) (s : State)
    (m : Move) (ms : List Move) :
    edgeTrace step s (m :: ms) =
      (s, m) :: edgeTrace step (step s m) ms := rfl

/-- If a path starts inside `C` and ends outside `C`, one of the *actual
traversed directed edges* crosses from `C` to its complement. -/
theorem final_outside_forces_crossing
    (step : State → Move → State)
    (C : Set State)
    {start : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hout : ACCWell.run step start ms ∉ C) :
    ∃ e ∈ edgeTrace step start ms,
      e.1 ∈ C ∧ step e.1 e.2 ∉ C := by
  induction ms generalizing start with
  | nil =>
      simp at hout
      exact False.elim (hout hstart)
  | cons m ms ih =>
      by_cases hnext : step start m ∈ C
      · have htail : ACCWell.run step (step start m) ms ∉ C := by
          simpa using hout
        rcases ih (start := step start m) hnext htail with ⟨e, he, hsrc, htgt⟩
        exact ⟨e, by simp [edgeTrace, he], hsrc, htgt⟩
      · exact ⟨(start, m), by simp [edgeTrace], hstart, hnext⟩

/-- If `C` is closed under every move whose target remains at height at most
`B`, then any finite path leaving `C` must traverse an actual edge whose target
height is strictly greater than `B`.

This is the correct complete-frontier statement.  It does not replace
`B < height target` by `height target = B+1` without an extra bounded-jump
hypothesis. -/
theorem cap_closed_exit_forces_above_cap_edge
    (step : State → Move → State)
    (height : State → ℕ)
    (C : Set State)
    (B : ℕ)
    {start : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hclosed : ∀ s ∈ C, ∀ m, height (step s m) ≤ B → step s m ∈ C)
    (hout : ACCWell.run step start ms ∉ C) :
    ∃ e ∈ edgeTrace step start ms,
      e.1 ∈ C ∧ step e.1 e.2 ∉ C ∧ B < height (step e.1 e.2) := by
  rcases final_outside_forces_crossing step C ms hstart hout with
    ⟨e, he, hsrc, htgt⟩
  have habove : B < height (step e.1 e.2) := by
    by_contra hnot
    have hle : height (step e.1 e.2) ≤ B := Nat.le_of_not_gt hnot
    exact htgt (hclosed e.1 hsrc e.2 hle)
  exact ⟨e, he, hsrc, htgt, habove⟩

end ACCFrontier

#print axioms ACCFrontier.final_outside_forces_crossing
#print axioms ACCFrontier.cap_closed_exit_forces_above_cap_edge
