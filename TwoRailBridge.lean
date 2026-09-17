import Mathlib

/-!
# Two-rail projector/transport bridge: gauge-safe algebra

This module formalizes only the scalar invariant shared by a rank-one projector
pair and a canonical two-level transport.  It deliberately does not identify a
full transport element with a projector pair: stabilizer/gauge data can remain.
-/

namespace TwoRailBridge

/-- For a normalized two-level state with overlap coordinate `c` and transverse
coordinate `s`, the rank-one projector separation is `s^2 = 1-c^2`. -/
theorem projector_offset_eq_transverse_sq {c s : ℝ}
    (hnorm : c^2 + s^2 = 1) :
    1 - c^2 = s^2 := by
  nlinarith

/-- If `t = 2c` is the trace of the canonical real two-level rotation, then the
same invariant can be recovered from the normalized trace. -/
theorem projector_offset_eq_trace_defect {c s t : ℝ}
    (hnorm : c^2 + s^2 = 1) (htrace : t = 2*c) :
    s^2 = 1 - (t/2)^2 := by
  rw [htrace]
  have h := projector_offset_eq_transverse_sq hnorm
  norm_num at *
  nlinarith

/-- Equal overlap magnitude gives equal projector offset.  This records the
quotient nature of projector data: sign/phase-like information is invisible. -/
theorem same_overlap_sq_same_offset {c₁ c₂ : ℝ}
    (h : c₁^2 = c₂^2) :
    1 - c₁^2 = 1 - c₂^2 := by
  rw [h]

end TwoRailBridge

#print axioms TwoRailBridge.projector_offset_eq_transverse_sq
#print axioms TwoRailBridge.projector_offset_eq_trace_defect
#print axioms TwoRailBridge.same_overlap_sq_same_offset
