import Mathlib

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
      have hnextTrace : step start m ∈ trace step start (m :: ms) := by
        simp [trace]
      have hnext : step start m ∈ C :=
        hclosed start hstart m (hcap _ hnextTrace)
      apply ih (start := step start m) hnext hclosed
      intro s hs
      apply hcap s
      simp [trace, hs]

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
  push_neg at hno
  have hcap : ∀ s ∈ trace step start ms, height s ≤ B := by
    intro s hs
    exact Nat.le_of_not_lt (hno s hs)
  have hfinal : run step start ms ∈ C :=
    run_mem_of_bounded_trace step height C B ms hstart hclosed hcap
  exact (Nat.not_lt_of_ge (hlower _ hfinal)) hdesc

end ACCWell

#print axioms ACCWell.run_mem_trace
#print axioms ACCWell.run_mem_of_bounded_trace
#print axioms ACCWell.descent_forces_cap_exit
