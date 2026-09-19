import Mathlib.Data.Nat.Basic
import Mathlib.Data.List.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Tactic.Push

/-!
# Finite length-well bottleneck theorem

Abstract logic behind the computational Andrews--Curtis length-well eye.
The theorem is graph-theoretic: if a finite/explicitly checked region contains
an initial state, is closed under every move that stays below a height cap, and
contains no state below the initial height, then every descending move sequence
must leave that cap.

The file does not assert Andrews--Curtis reachability or nonreachability.
-/

namespace ACCWell

variable {State Move : Type}

/-- Execute a finite sequence of moves. -/
def run (step : State → Move → State) : State → List Move → State
  | s, [] => s
  | s, m :: ms => run step (step s m) ms

/-- List every state visited by a finite move sequence, including both ends. -/
def trace (step : State → Move → State) : State → List Move → List State
  | s, [] => [s]
  | s, m :: ms => s :: trace step (step s m) ms

@[simp] theorem run_nil (step : State → Move → State) (s : State) :
    run step s [] = s := rfl

@[simp] theorem run_cons (step : State → Move → State) (s : State) (m : Move)
    (ms : List Move) :
    run step s (m :: ms) = run step (step s m) ms := rfl

@[simp] theorem trace_nil (step : State → Move → State) (s : State) :
    trace step s [] = [s] := rfl

@[simp] theorem trace_cons (step : State → Move → State) (s : State) (m : Move)
    (ms : List Move) :
    trace step s (m :: ms) = s :: trace step (step s m) ms := rfl

/-- The initial state belongs to every visited trace. -/
theorem start_mem_trace (step : State → Move → State) (s : State) (ms : List Move) :
    s ∈ trace step s ms := by
  cases ms <;> simp [trace]

/-- The final state belongs to the visited trace. -/
theorem run_mem_trace (step : State → Move → State) (s : State) (ms : List Move) :
    run step s ms ∈ trace step s ms := by
  induction ms generalizing s with
  | nil => simp
  | cons m ms ih =>
      simp only [run_cons, trace_cons, List.mem_cons]
      exact Or.inr (ih (step s m))

/-- If every visited state remains below the cap, closure of `C` under
cap-respecting moves keeps the entire execution inside `C`. -/
theorem run_mem_of_bounded_trace
    (step : State → Move → State)
    (height : State → ℕ)
    (C : Set State)
    (B : ℕ)
    {start : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hclosed : ∀ s ∈ C, ∀ m, height (step s m) ≤ B → step s m ∈ C)
    (hcap : ∀ s ∈ trace step start ms, height s ≤ B) :
    run step start ms ∈ C := by
  induction ms generalizing start with
  | nil => simpa using hstart
  | cons m ms ih =>
      have hnextInner : step start m ∈ trace step (step start m) ms :=
        start_mem_trace step (step start m) ms
      have hnextTrace : step start m ∈ trace step start (m :: ms) := by
        simp only [trace_cons, List.mem_cons]
        exact Or.inr hnextInner
      have hnext : step start m ∈ C :=
        hclosed start hstart m (hcap _ hnextTrace)
      apply ih (start := step start m) hnext
      intro s hs
      apply hcap s
      simp only [trace_cons, List.mem_cons]
      exact Or.inr hs

/-- Closed-well bottleneck theorem.

If `C` contains `start`, every move that stays at height at most `B` remains in
`C`, and no state of `C` is lower than `start`, then any finite execution that
ends lower than `start` must visit a state above `B`. -/
theorem descent_forces_cap_exit
    (step : State → Move → State)
    (height : State → ℕ)
    (C : Set State)
    (B : ℕ)
    {start : State}
    (ms : List Move)
    (hstart : start ∈ C)
    (hclosed : ∀ s ∈ C, ∀ m, height (step s m) ≤ B → step s m ∈ C)
    (hlower : ∀ s ∈ C, height start ≤ height s)
    (hdesc : height (run step start ms) < height start) :
    ∃ s ∈ trace step start ms, B < height s := by
  by_contra hno
  push Not at hno
  have hfinal : run step start ms ∈ C :=
    run_mem_of_bounded_trace step height C B ms hstart hclosed hno
  exact (Nat.not_lt_of_ge (hlower _ hfinal)) hdesc

end ACCWell

#print axioms ACCWell.start_mem_trace
#print axioms ACCWell.run_mem_trace
#print axioms ACCWell.run_mem_of_bounded_trace
#print axioms ACCWell.descent_forces_cap_exit


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
