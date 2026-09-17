import Mathlib

/-!
QG transport/memory reconstruction: finite abstract theorems only.

These statements formalize the information-retention logic recovered from the
old spectral-memory programme. They do NOT formalize analytic spectral flow,
K-theory, APS theory, a physical clock, gauge-field dynamics, or gravity.
-/
set_option autoImplicit false
noncomputable section

namespace QGTransportMemory

/-- An observation `F` is sufficient for a target `T` when `T` factors through `F`. -/
def SufficientObservation {X Y Z : Type*} (F : X → Y) (T : X → Z) : Prop :=
  ∃ g : Y → Z, T = g ∘ F

/-- Any target that factors through an observation is constant on every observation fiber. -/
theorem sufficient_constant_on_fiber {X Y Z : Type*}
    (F : X → Y) (T : X → Z) (h : SufficientObservation F T)
    {x₁ x₂ : X} (hf : F x₁ = F x₂) : T x₁ = T x₂ := by
  rcases h with ⟨g, hg⟩
  rw [hg]
  exact congrArg g hf

/-- A collision under `F` that is separated by `T` is an exact obstruction to factorization. -/
theorem fiber_witness_obstructs_sufficiency {X Y Z : Type*}
    (F : X → Y) (T : X → Z) {x₁ x₂ : X}
    (hf : F x₁ = F x₂) (ht : T x₁ ≠ T x₂) :
    ¬ SufficientObservation F T := by
  intro h
  exact ht (sufficient_constant_on_fiber F T h hf)

/-- Once two states collide under `F`, any further post-compression still identifies them. -/
theorem collision_persists_under_postcompression {X Y Z : Type*}
    (F : X → Y) (G : Y → Z) {x₁ x₂ : X} (hf : F x₁ = F x₂) :
    (G ∘ F) x₁ = (G ∘ F) x₂ := by
  simpa [Function.comp_apply] using congrArg G hf

/-- A target-separating fiber witness remains an obstruction after every further compression. -/
theorem witness_persists_under_postcompression {X Y Z W : Type*}
    (F : X → Y) (G : Y → Z) (T : X → W) {x₁ x₂ : X}
    (hf : F x₁ = F x₂) (ht : T x₁ ≠ T x₂) :
    ¬ SufficientObservation (G ∘ F) T := by
  exact fiber_witness_obstructs_sufficiency (G ∘ F) T
    (collision_persists_under_postcompression F G hf) ht

/-- Pairing two observations is injective exactly when agreement in both forces state equality. -/
theorem paired_observation_injective_iff {X Y Z : Type*}
    (F : X → Y) (A : X → Z) :
    Function.Injective (fun x => (F x, A x)) ↔
      ∀ x y, F x = F y → A x = A y → x = y := by
  constructor
  · intro h x y hf ha
    apply h
    exact Prod.ext hf ha
  · intro h x y hp
    exact h x y (congrArg Prod.fst hp) (congrArg Prod.snd hp)

/-- Signed-event compression used as a finite model of net flow. -/
def netFlow (events : List ℤ) : ℤ := events.sum

/-- Opposite oriented events cancel in the net scalar. -/
theorem opposite_events_cancel (a : ℤ) : netFlow [a, -a] = 0 := by
  simp [netFlow]

/-- Zero net flow does not imply that the event history is empty. -/
theorem zero_net_can_have_events :
    ∃ events : List ℤ, events ≠ [] ∧ netFlow events = 0 := by
  refine ⟨[(1 : ℤ), -1], ?_, ?_⟩
  · decide
  · norm_num [netFlow]

/-- A minimal record separating an endpoint view from an ordered event history. -/
structure TransportRecord where
  endpoint : ℤ
  events : List ℤ
  deriving DecidableEq

/-- Endpoint-only compression. -/
def endpointView (r : TransportRecord) : ℤ := r.endpoint

private def forwardRecord : TransportRecord := ⟨0, [1]⟩
private def reverseRecord : TransportRecord := ⟨0, [-1]⟩

/-- Endpoint observation is non-injective: opposite histories can share the same endpoint. -/
theorem endpoint_view_not_injective : ¬ Function.Injective endpointView := by
  intro h
  have heq : forwardRecord = reverseRecord := h rfl
  have hh := congrArg TransportRecord.events heq
  norm_num [forwardRecord, reverseRecord] at hh

section MatrixCurrent
variable {n : Type*} [Fintype n]

/-- The antisymmetric transition-current record. -/
def current (T : Matrix n n ℝ) : Matrix n n ℝ := T - T.transpose

/-- Antisymmetrization is skew under transpose. -/
theorem current_skew (T : Matrix n n ℝ) :
    (current T).transpose = - current T := by
  ext i j
  simp [current]

/-- Relabel both indices by the same equivalence. -/
def relabel (e : n ≃ n) (T : Matrix n n ℝ) : Matrix n n ℝ :=
  fun i j => T (e i) (e j)

/-- The full antisymmetric current transforms covariantly under state relabeling. -/
theorem current_relabel_covariant (e : n ≃ n) (T : Matrix n n ℝ) :
    current (relabel e T) = relabel e (current T) := by
  ext i j
  simp [current, relabel]

end MatrixCurrent

/-- Circulation around one orientation of a 3-cycle. -/
def triangleCirculation (J : Matrix (Fin 3) (Fin 3) ℝ) : ℝ :=
  J 0 1 + J 1 2 + J 2 0

/-- Circulation around the reverse orientation. -/
def reverseTriangleCirculation (J : Matrix (Fin 3) (Fin 3) ℝ) : ℝ :=
  J 0 2 + J 2 1 + J 1 0

/-- For a skew current, reversing cycle orientation reverses circulation. -/
theorem reverse_triangle_circulation
    (J : Matrix (Fin 3) (Fin 3) ℝ)
    (hskew : ∀ i j, J i j = -J j i) :
    reverseTriangleCirculation J = - triangleCirculation J := by
  unfold reverseTriangleCirculation triangleCirculation
  rw [hskew 0 2, hskew 2 1, hskew 1 0]
  ring

section RankOneFrame
variable {n : Type*}

/-- Real rank-one outer product; a toy O(1) frame/projector model. -/
def realOuter (q : n → ℝ) : Matrix n n ℝ := fun i j => q i * q j

/-- A sign-frame change leaves the rank-one outer product invariant. -/
theorem sign_frame_outer_invariant (s : ℝ) (q : n → ℝ) (hs : s ^ 2 = 1) :
    realOuter (fun i => s * q i) = realOuter q := by
  ext i j
  change (s * q i) * (s * q j) = q i * q j
  calc
    (s * q i) * (s * q j) = s ^ 2 * (q i * q j) := by ring
    _ = q i * q j := by rw [hs, one_mul]

end RankOneFrame

/-- A globally nonnegative linear soft mode cannot cross zero with nonzero linear slope. -/
theorem nonnegative_linear_mode_has_zero_slope (a : ℝ)
    (h : ∀ x : ℝ, 0 ≤ a * x) : a = 0 := by
  have hp := h 1
  have hm := h (-1)
  norm_num at hp hm
  linarith

/-- By contrast, an unrestricted real linear mode can cross through zero with a sign change. -/
theorem signed_linear_crossing_exists :
    ∃ f : ℝ → ℝ, f (-1) < 0 ∧ f 0 = 0 ∧ 0 < f 1 := by
  refine ⟨fun x => x, ?_⟩
  norm_num

/-- The local square-root exponent n/2 and integrated exponent 1+n/2 differ by one. -/
theorem local_vs_integrated_exponent (n : ℝ) :
    (1 + n / 2) - (n / 2) = 1 := by
  ring

end QGTransportMemory
