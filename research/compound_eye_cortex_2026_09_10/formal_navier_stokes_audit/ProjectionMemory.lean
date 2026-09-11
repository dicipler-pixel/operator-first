import Mathlib

/-!
# Exact hidden-sector return under projection

This is an operator-algebra identity arising naturally in the Operator-First
reduction / memory viewpoint. It does **not** prove Navier--Stokes blowup or
regularity.

If `P` is an idempotent compression (`P^2 = P`) and `A` is a full-system
operator, then the discrepancy between

  * evolve twice in the full system and project: `P A^2 P`, and
  * evolve twice only inside the compressed model: `(P A P)^2`

is exactly the out-and-back excursion through the discarded sector `1 - P`:

    P A^2 P - (P A P)^2 = P A (1 - P) A P.

This is the second-order algebraic memory term that a closed projected model
must either retain, model, or prove vanishes.
-/

set_option autoImplicit false

namespace OperatorFirstProjectionMemory

/--
Exact second-order compression identity in any (possibly noncommutative) ring.
-/
theorem second_order_hidden_return
    {R : Type*} [Ring R] (P A : R) (hP : P * P = P) :
    P * A * A * P - (P * A * P) * (P * A * P)
      = P * A * (1 - P) * A * P := by
  calc
    P * A * A * P - (P * A * P) * (P * A * P)
        = P * A * A * P - P * A * (P * P) * A * P := by
            noncomm_ring
    _ = P * A * A * P - P * A * P * A * P := by
          rw [hP]
    _ = P * A * (1 - P) * A * P := by
          noncomm_ring

#print axioms OperatorFirstProjectionMemory.second_order_hidden_return

end OperatorFirstProjectionMemory
