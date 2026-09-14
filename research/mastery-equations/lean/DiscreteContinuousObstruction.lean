import Mathlib.Topology.LocallyConstant.Basic

/-!
# Discrete-continuous obstruction

Corrected descendant of the archived crossing-number question:
a continuous observable from a preconnected parameter space into a discrete
codomain cannot change value.  In particular, a globally continuous
natural-number crossing count cannot climb `0, 1, 2, ...` without leaving the
continuous/discrete hypotheses (for example at a wall/stratum or jump).
-/

namespace OperatorFirst.DiscreteContinuous

/-- A continuous map from a preconnected space into a discrete space is
constant on pairs of points. -/
theorem continuous_to_discrete_eq
    {I D : Type*} [TopologicalSpace I] [PreconnectedSpace I]
    [TopologicalSpace D] [DiscreteTopology D]
    (f : I → D) (hf : Continuous f) (x y : I) :
    f x = f y := by
  have hloc : IsLocallyConstant f :=
    (IsLocallyConstant.iff_continuous f).2 hf
  exact hloc.apply_eq_of_preconnectedSpace x y

/-- Function-level form of the same obstruction. -/
theorem continuous_to_discrete_eq_const
    {I D : Type*} [TopologicalSpace I] [PreconnectedSpace I]
    [TopologicalSpace D] [DiscreteTopology D]
    (f : I → D) (hf : Continuous f) (x : I) :
    f = Function.const I (f x) := by
  funext y
  exact continuous_to_discrete_eq f hf y x

/-- Natural-number specialization: a continuous integer-valued crossing count
on a preconnected parameter space is constant. -/
theorem continuous_crossing_number_constant
    {I : Type*} [TopologicalSpace I] [PreconnectedSpace I]
    (cn : I → ℕ) (hcn : Continuous cn) (x y : I) :
    cn x = cn y := by
  exact continuous_to_discrete_eq cn hcn x y

end OperatorFirst.DiscreteContinuous

#print axioms OperatorFirst.DiscreteContinuous.continuous_to_discrete_eq
#print axioms OperatorFirst.DiscreteContinuous.continuous_to_discrete_eq_const
#print axioms OperatorFirst.DiscreteContinuous.continuous_crossing_number_constant
