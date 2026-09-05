/-
  SCRIPT: FCS-LEAN-01
  Machine-checked: the offset is invisible to Gaussian counting statistics.

  THE SETTING.  The paper's own identity reads the offset as a full-counting-statistics
  quantity,

        Tr K_A  =  log P(N_A = 0)  -  log P(N_A = L),

  the log-odds of the block being empty against full (Klich's counting formula).  The FCS
  literature works overwhelmingly in the regime of typical fluctuations, where P(N) is
  asymptotically Gaussian and the higher cumulants are suppressed -- that is, where
  `log P(N)` is a quadratic function of `N`.

  WHAT IS PROVED HERE.  For any log-quadratic (Gaussian) counting distribution the
  log-odds of the two extreme outcomes is exactly `-(L * (a*L + b))`, which vanishes
  exactly when the distribution is centred at half filling.  Two consequences, both
  certified below:

    * `gaussian_halffilling_zero` -- a Gaussian counting distribution centred at half
      filling has log-odds exactly zero.  So a Gaussian FCS can never produce a nonzero
      offset at half filling: every nonzero `Tr K_A` measured in the paper is a
      NON-GAUSSIAN, large-deviation effect living in the two extreme tails, not in any
      finite number of cumulants.

    * `gaussian_zero_iff_halffilling` -- and conversely, for a Gaussian distribution the
      log-odds vanishes ONLY at half filling.  This is the formal shadow of the trimer
      control of §7: away from half filling, emptiness and fullness are large deviations
      with different rates and the log-odds cannot vanish.

  WHY THIS IS WORTH CERTIFYING.  It separates two things the paper keeps apart by hand.
  The entropy response is built from the low cumulants and is screened in the interior;
  the offset is not built from any of them.  The theorem below is the reason those two
  behave differently, stated so that it cannot be argued with.

  WHAT IS NOT PROVED HERE.  That the paper's substrates actually have non-Gaussian tails
  (that is a measurement); that `P(N=0) = det(1 - C_A)` and `P(N=L) = det C_A` (that is
  determinantal algebra needing a linear-algebra library, unavailable in this sandbox);
  and anything about the two-Gaussian structure of odd-block FCS, which is an open lead,
  not a result.

  Compiled under Lean 4.9.0 with no imports.  Levels are carried as integers, as in
  OFFSET-LEAN-01; the argument is ring arithmetic and is unaffected by that choice.
-/

namespace FCS

/-- A log-quadratic ("Gaussian") counting distribution: `logP n = a*n*n + b*n + c`,
    with `n` the particle number in the block.  Only the shape matters below, so the
    normalisation `c` is carried along and cancels. -/
def logP (a b c : Int) (n : Int) : Int := a * n * n + b * n + c

/-- **The log-odds of the two extremes.**  For a log-quadratic counting distribution,
    `logP 0 - logP L = -(L * (a*L + b))`.  The normalisation drops out, as it must. -/
theorem logodds (a b c L : Int) :
    logP a b c 0 - logP a b c L = -(L * (a * L + b)) := by
  simp [logP, Int.mul_add, Int.add_mul, Int.mul_comm, Int.mul_assoc, Int.mul_left_comm]
  omega

/-- Centred at half filling: the mean `m` of the Gaussian sits at `L/2`, which for a
    log-quadratic density means `b = -(a * L)` (the vertex of `a n² + b n` is at `-b/2a`,
    so `-b/2a = L/2` is `b = -aL`).  Stated without division. -/
def CentredAtHalfFilling (a b L : Int) : Prop := b = -(a * L)

/-- **A Gaussian counting distribution centred at half filling has log-odds exactly zero.**
    Hence no Gaussian FCS can produce a nonzero offset at half filling: the paper's
    measured `Tr K_A ≠ 0` is a non-Gaussian tail effect. -/
theorem gaussian_halffilling_zero (a b c L : Int) (h : CentredAtHalfFilling a b L) :
    logP a b c 0 - logP a b c L = 0 := by
  rw [logodds]
  rw [CentredAtHalfFilling] at h
  rw [h]
  omega

/-- **And only at half filling.**  For a nonempty block, the log-odds of a Gaussian
    counting distribution vanishes precisely when it is centred at half filling.
    This is the formal shadow of the trimer control: at one-third filling the log-odds
    cannot vanish. -/
theorem gaussian_zero_iff_halffilling (a b c L : Int) (hL : L ≠ 0) :
    logP a b c 0 - logP a b c L = 0 ↔ CentredAtHalfFilling a b L := by
  rw [logodds, CentredAtHalfFilling]
  constructor
  · intro h
    have h2 : L * (a * L + b) = 0 := by omega
    have h3 : a * L + b = 0 := by
      rcases Int.mul_eq_zero.mp h2 with h4 | h4
      · exact absurd h4 hL
      · exact h4
    omega
  · intro h
    rw [h]
    omega

/-- The off-centre case made concrete: a Gaussian centred at one third of the block
    (`b = -(2*a*L)/3` in the scaled form `3*b = -(2*a*L)`) has log-odds `L*a*L/3`,
    nonzero whenever the curvature and the block are.  Written with the scale cleared. -/
theorem gaussian_third_filling (a b L : Int) (h : 3 * b = -(2 * (a * L))) :
    3 * (-(L * (a * L + b))) = -(L * (a * L)) := by
  have key : 3 * (a * L + b) = a * L := by omega
  calc 3 * (-(L * (a * L + b)))
      = -(3 * (L * (a * L + b))) := by rw [Int.mul_neg]
    _ = -(L * (3 * (a * L + b))) := by rw [Int.mul_left_comm]
    _ = -(L * (a * L)) := by rw [key]

/-!
  ### What the two theorems say together

  `Tr K_A` is the log-odds of the two extreme counting outcomes.  If the counting
  statistics were Gaussian, that number would be pinned by the mean alone: zero at half
  filling, and nonzero away from it in proportion to the displacement of the mean.  The
  paper measures a nonzero offset AT half filling, on incommensurate cuts, at seventy
  digits.  So the offset is not a property of any Gaussian approximation to the counting
  distribution, and no truncation at finite cumulant order can see it.  It lives in the
  large-deviation tails, which is the same statement as "it is not screened in the
  interior while the entropy is".
-/

end FCS

#print axioms FCS.logodds
#print axioms FCS.gaussian_halffilling_zero
#print axioms FCS.gaussian_zero_iff_halffilling
#print axioms FCS.gaussian_third_filling
