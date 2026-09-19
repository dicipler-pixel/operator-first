# Finite length wells and complete first-exit frontiers in the Andrews–Curtis move graph

## Partial-result statement

Let `S` be a state space with a move map `step : S → M → S` and a height
function `h : S → ℕ`. Let `C ⊆ S` be a set containing a start state `s₀`.
Assume:

1. whenever `s ∈ C` and `h(step s m) ≤ B`, then `step s m ∈ C`;
2. every `s ∈ C` satisfies `h(s₀) ≤ h(s)`.

Then every finite move sequence beginning at `s₀` and ending at a state of
height strictly below `h(s₀)` must visit a state of height strictly greater
than `B`.

In addition, if a finite path starts in `C` and ends outside `C`, then one of
the actual directed edges traversed by that path crosses from `C` to its
complement. Under assumption (1), the target of that first-exit edge has height
strictly greater than `B`.

## Why the second theorem matters for ACC

For Andrews–Curtis search, total relator length is a natural height. Exact
enumeration can sometimes certify a capped connected component as CLOSED.
The theorem then turns the finite computation into a rigorous statement that
any later descent must cross above the cap.

The first-exit statement is deliberately stronger than a `B → B+1` shell
description: ordinary AC moves can jump by more than one unit of total relator
length. Therefore a complete frontier must include every directed edge from a
state in the closed component to any state above the cap.

## Formalization

Lean declarations:

- `ACCWell.run`
- `ACCWell.trace`
- `ACCWell.run_mem_of_bounded_trace`
- `ACCWell.descent_forces_cap_exit`
- `ACCFrontier.edgeTrace`
- `ACCFrontier.final_outside_forces_crossing`
- `ACCFrontier.cap_closed_exit_forces_above_cap_edge`

The formal theorem is abstract and does not itself assert that any particular
ACC component is closed. Concrete finite closures are separate computational
certificates.

## Scope boundary

This is a partial structural result about exhaustive finite sublevel searches.
It does not prove or disprove the Andrews–Curtis conjecture, and it does not
promote a budget-limited search to a theorem. `CLOSED` requires exhaustion of
the capped frontier.
