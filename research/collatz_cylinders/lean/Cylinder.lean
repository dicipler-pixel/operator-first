/-
  An exact 2-adic counting lemma, formalized.

  Self-contained: this file imports NOTHING. No Mathlib, no Std. Every lemma
  below is proved from Lean 4 core, so the result depends on no library and
  carries no axioms beyond Lean's own.

  The statement being formalized (see ../TWO_ADIC_COUNTING_LEMMA_v2.md):

      For m odd, a : Nat, and j < K,
        #{ k < 2^K : v2 (a + m*k) = j }  =  2^(K-j-1)

  where v2 n = j is expressed, without defining a valuation, as the exact
  modular condition

        n % 2^(j+1) = 2^j

  which is equivalent to "2^j divides n but 2^(j+1) does not", and which
  already forces n ≠ 0.

  Author: Jeromie N. Beasley (statement, direction).
  Formalization assistance: AI.
-/

namespace CollatzCylinder

/-- `Odd2 m` : `m` is an odd natural number. Stated as an existential so that
    core `Nat` arithmetic can use the witness directly. -/
def Odd2 (m : Nat) : Prop := ∃ c, m = 2 * c + 1

theorem odd_one : Odd2 1 := ⟨0, rfl⟩

theorem odd_mul {m n : Nat} (hm : Odd2 m) (hn : Odd2 n) : Odd2 (m * n) := by
  obtain ⟨a, rfl⟩ := hm
  obtain ⟨b, rfl⟩ := hn
  exact ⟨2 * a * b + a + b, by simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]; omega⟩

/-- Every power of an odd number is odd. The `n`-step law needs exactly this,
    since the multiplier at step `t` is `3 ^ (t+1)`. -/
theorem odd_pow {m : Nat} (hm : Odd2 m) : ∀ n, Odd2 (m ^ n)
  | 0 => odd_one
  | n + 1 => by
      rw [Nat.pow_succ]
      exact odd_mul (odd_pow hm n) hm

/-- The sum of two odd numbers is even. This is the whole engine of the
    inverse construction below. -/
theorem odd_add_odd_even {c m : Nat} (hc : Odd2 c) (hm : Odd2 m) :
    ∃ d, c + m = 2 * d := by
  obtain ⟨x, rfl⟩ := hc
  obtain ⟨y, rfl⟩ := hm
  exact ⟨x + y + 1, by omega⟩

/-- A natural number is even or odd. -/
theorem even_or_odd (n : Nat) : (∃ c, n = 2 * c) ∨ Odd2 n := by
  induction n with
  | zero => exact Or.inl ⟨0, rfl⟩
  | succ k ih =>
      cases ih with
      | inl h => obtain ⟨c, rfl⟩ := h; exact Or.inr ⟨c, rfl⟩
      | inr h => obtain ⟨c, rfl⟩ := h; exact Or.inl ⟨c + 1, by omega⟩

/--
  **An odd number is invertible modulo every power of two.**

  Proved by induction on the exponent, lifting the inverse one bit at a time:
  if `m * m' = 1 + c * 2^s` then either `c` is even and `m'` already works
  modulo `2^(s+1)`, or `c` is odd and `m' + 2^s` works, because `c + m` is then
  a sum of two odd numbers and hence even.

  This is the only number-theoretic input the counting lemma needs, and it is
  where "m is odd" is used.
-/
theorem odd_inv (m : Nat) (hm : Odd2 m) : ∀ s, ∃ m' c, m * m' = 1 + c * 2 ^ s
  | 0 => by
      obtain ⟨x, rfl⟩ := hm
      exact ⟨1, 2 * x, by simp; omega⟩
  | s + 1 => by
      obtain ⟨m', c, hmc⟩ := odd_inv m hm s
      rcases even_or_odd c with ⟨d, rfl⟩ | hc
      · -- c even: the same inverse already works one bit further up
        refine ⟨m', d, ?_⟩
        rw [hmc, Nat.pow_succ]
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
      · -- c odd: lift the inverse by 2^s; c + m is a sum of two odds, so even
        obtain ⟨d, hd⟩ := odd_add_odd_even hc hm
        refine ⟨m' + 2 ^ s, d, ?_⟩
        have h1 : m * (m' + 2 ^ s) = 1 + (c + m) * 2 ^ s := by
          rw [Nat.mul_add, hmc, Nat.add_mul, Nat.add_assoc]
        rw [h1, hd, Nat.pow_succ]
        simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]

/-- If `m` is odd and `2` divides `m * d`, then `2` divides `d`. -/
theorem two_dvd_of_odd_mul {m d : Nat} (hm : Odd2 m) (h : 2 ∣ m * d) : 2 ∣ d := by
  obtain ⟨c, rfl⟩ := hm
  rcases even_or_odd d with ⟨e, rfl⟩ | ⟨e, rfl⟩
  · exact ⟨e, rfl⟩
  · exfalso
    obtain ⟨q, hq⟩ := h
    have : (2 * c + 1) * (2 * e + 1) = 2 * (2 * c * e + c + e) + 1 := by
      simp [Nat.mul_add, Nat.mul_comm, Nat.mul_left_comm]; omega
    omega

/--
  **2-adic cancellation.** An odd multiplier carries no powers of two, so it
  can be cancelled from a divisibility by `2 ^ s`.

  This is the injectivity half of the counting lemma: it is what forces two
  solutions in the same window to coincide.
-/
theorem pow_two_dvd_of_odd_mul {m : Nat} (hm : Odd2 m) :
    ∀ s d, 2 ^ s ∣ m * d → 2 ^ s ∣ d
  | 0, _, _ => Nat.one_dvd _
  | s + 1, d, h => by
      have h2 : (2 : Nat) ∣ m * d := Nat.dvd_trans ⟨2 ^ s, by rw [Nat.pow_succ]; omega⟩ h
      obtain ⟨e, rfl⟩ := two_dvd_of_odd_mul hm h2
      have hse : 2 ^ s ∣ m * e := by
        obtain ⟨q, hq⟩ := h
        refine ⟨q, ?_⟩
        have : 2 * (m * e) = 2 * (2 ^ s * q) := by
          rw [Nat.pow_succ] at hq
          simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc] at hq ⊢
          omega
        omega
      obtain ⟨f, rfl⟩ := pow_two_dvd_of_odd_mul hm s e hse
      exact ⟨f, by rw [Nat.pow_succ]; simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]⟩

-- If adding y leaves the residue mod M unchanged, then M divides y.
theorem dvd_of_add_mod_eq {M x y : Nat} (hM : 0 < M)
    (h : (x + y) % M = x % M) : M ∣ y := by
  have h1 : M * (x / M) + x % M = x := Nat.div_add_mod x M
  have h2 : M * ((x + y) / M) + (x + y) % M = x + y := Nat.div_add_mod (x + y) M
  rw [h] at h2
  -- generalize the two products so omega sees only linear atoms
  generalize hq1 : M * (x / M) = A at h1
  generalize hq2 : M * ((x + y) / M) = B at h2
  have hAB : B = A + y := by omega
  have hle : x / M ≤ (x + y) / M := by
    apply Nat.le_of_mul_le_mul_left _ hM
    omega
  refine ⟨(x + y) / M - x / M, ?_⟩
  rw [Nat.mul_sub, hq1, hq2]
  omega

/-! ## Counting over a window -/

/-- Number of `k < n` with `P (s + k)` true: a count over the window `[s, s+n)`. -/
def cntFrom (P : Nat → Bool) (s n : Nat) : Nat :=
  ((List.range n).filter (fun k => P (s + k))).length

theorem cntFrom_zero (P : Nat → Bool) (s : Nat) : cntFrom P s 0 = 0 := rfl

theorem cntFrom_succ (P : Nat → Bool) (s n : Nat) :
    cntFrom P s (n + 1) = cntFrom P s n + (if P (s + n) then 1 else 0) := by
  unfold cntFrom
  rw [List.range_succ, List.filter_append, List.length_append]
  congr 1
  split <;> simp_all

/-- A window splits: counting `[s, s+n₁+n₂)` is counting `[s, s+n₁)` then
    `[s+n₁, s+n₁+n₂)`. -/
theorem cntFrom_add (P : Nat → Bool) (s n₁ : Nat) :
    ∀ n₂, cntFrom P s (n₁ + n₂) = cntFrom P s n₁ + cntFrom P (s + n₁) n₂
  | 0 => by simp [cntFrom_zero]
  | n + 1 => by
      rw [← Nat.add_assoc, cntFrom_succ, cntFrom_add P s n₁ n, cntFrom_succ,
          Nat.add_assoc, Nat.add_assoc]


/-- An `M`-periodic predicate: shifting the window by `M` leaves the count alone. -/
theorem cntFrom_shift (P : Nat → Bool) (M : Nat) (hP : ∀ x, P (x + M) = P x) (s n : Nat) :
    cntFrom P (s + M) n = cntFrom P s n := by
  unfold cntFrom
  have h : (fun k => P (s + M + k)) = (fun k => P (s + k)) := by
    funext k
    have e : s + M + k = (s + k) + M := by omega
    rw [e, hP]
  rw [h]

theorem cntFrom_shift_mul (P : Nat → Bool) (M : Nat) (hP : ∀ x, P (x + M) = P x) :
    ∀ q n, cntFrom P (M * q) n = cntFrom P 0 n
  | 0, n => by simp
  | q + 1, n => by
      have e : M * (q + 1) = M * q + M := Nat.mul_succ M q
      rw [e, cntFrom_shift P M hP, cntFrom_shift_mul P M hP q n]

/-- **Block decomposition.** Over `q` whole periods the count is `q` copies of
    the count over one period. -/
theorem cntFrom_blocks (P : Nat → Bool) (M : Nat) (hP : ∀ x, P (x + M) = P x) :
    ∀ q, cntFrom P 0 (M * q) = q * cntFrom P 0 M
  | 0 => by simp [cntFrom_zero]
  | q + 1 => by
      have e : M * (q + 1) = M * q + M := Nat.mul_succ M q
      rw [e, cntFrom_add, cntFrom_blocks P M hP q, Nat.zero_add,
          cntFrom_shift_mul P M hP q M, Nat.succ_mul]


/-- Nothing in the window satisfies `P`, so the count is zero. -/
theorem cntFrom_eq_zero (P : Nat → Bool) :
    ∀ n, (∀ x, x < n → P x = false) → cntFrom P 0 n = 0
  | 0, _ => rfl
  | n + 1, h => by
      rw [cntFrom_succ]
      simp only [Nat.zero_add]
      rw [cntFrom_eq_zero P n (fun x hx => h x (by omega)), h n (by omega)]
      simp

/-- Exactly one element of the window satisfies `P`, so the count is one. -/
theorem cntFrom_eq_one (P : Nat → Bool) :
    ∀ n r, r < n → P r = true → (∀ x, x < n → P x = true → x = r) → cntFrom P 0 n = 1
  | 0, _, hr, _, _ => absurd hr (by omega)
  | n + 1, r, hr, hPr, huniq => by
      rw [cntFrom_succ]
      simp only [Nat.zero_add]
      rcases Nat.lt_or_ge r n with hlt | hge
      · -- the witness is strictly inside; position n cannot also satisfy P
        have hn : P n = false := by
          cases hPn : P n with
          | false => rfl
          | true => exact absurd (huniq n (by omega) hPn) (by omega)
        rw [hn, cntFrom_eq_one P n r hlt hPr (fun x hx hPx => huniq x (by omega) hPx)]
        simp
      · -- the witness is the last position; nothing below it satisfies P
        have hrn : r = n := by omega
        subst hrn
        rw [hPr, cntFrom_eq_zero P r (fun x hx => by
          cases hPx : P x with
          | false => rfl
          | true => exact absurd (huniq x (by omega) hPx) (by omega))]
        simp

/-! ## The affine predicate -/

/-- `hit a m M t k` : the affine value `a + m*k` lands on residue `t` mod `M`. -/
def hit (a m M t k : Nat) : Bool := (a + m * k) % M == t

/-- The predicate is `M`-periodic: this is why whole windows can be counted. -/
theorem hit_periodic (a m M t : Nat) : ∀ x, hit a m M t (x + M) = hit a m M t x := by
  intro x
  unfold hit
  have e : a + m * (x + M) = a + m * x + M * m := by
    rw [Nat.left_distrib]; simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]; omega
  rw [e, Nat.add_mul_mod_self_left]

/-- **Uniqueness.** At most one `k` in a window of length `2^s` can hit `t`.
    This is `pow_two_dvd_of_odd_mul` in action: an odd multiplier cancels. -/
theorem hit_unique {m : Nat} (hm : Odd2 m) (a t s : Nat) :
    ∀ r₁ r₂, r₁ < 2 ^ s → r₂ < 2 ^ s →
      hit a m (2 ^ s) t r₁ = true → hit a m (2 ^ s) t r₂ = true → r₁ = r₂ := by
  -- a symmetric helper handles the ordered case; both orders reduce to it
  have key : ∀ x y, x ≤ y → y < 2 ^ s →
      hit a m (2 ^ s) t x = true → hit a m (2 ^ s) t y = true → x = y := by
    intro x y hxy hy hx' hy'
    unfold hit at hx' hy'
    have hx2 : (a + m * x) % 2 ^ s = t := by simpa using hx'
    have hy2 : (a + m * y) % 2 ^ s = t := by simpa using hy'
    obtain ⟨d, rfl⟩ : ∃ d, y = x + d := ⟨y - x, by omega⟩
    have e : a + m * (x + d) = a + m * x + m * d := by rw [Nat.left_distrib]; omega
    rw [e] at hy2
    have hMpos : 0 < 2 ^ s := Nat.two_pow_pos s
    have hdvd : 2 ^ s ∣ m * d := dvd_of_add_mod_eq hMpos (by rw [hy2, hx2])
    have : 2 ^ s ∣ d := pow_two_dvd_of_odd_mul hm s d hdvd
    obtain ⟨e', rfl⟩ := this
    have : 2 ^ s * e' = 0 := by
      rcases Nat.eq_zero_or_pos e' with h | h
      · simp [h]
      · exact absurd hy (by
          have : 2 ^ s * 1 ≤ 2 ^ s * e' := Nat.mul_le_mul_left _ h
          omega)
    omega
  intro r₁ r₂ h₁ h₂ p₁ p₂
  rcases Nat.le_total r₁ r₂ with h | h
  · exact key r₁ r₂ h h₂ p₁ p₂
  · exact (key r₂ r₁ h h₁ p₂ p₁).symm

/-- **Existence.** Some `k` in each window of length `2^s` hits `t`.
    This is `odd_inv` in action: the affine map is invertible mod `2^s`. -/
theorem hit_exists_aux {s m : Nat} (m' c : Nat) (hmc : m * m' = 1 + c * 2 ^ s)
    (a t : Nat) (ht : t < 2 ^ s) :
    ∃ r, r < 2 ^ s ∧ hit a m (2 ^ s) t r = true := by
  have hMpos : 0 < 2 ^ s := Nat.two_pow_pos s
  have hTa : a ≤ t + 2 ^ s * (a + 1) := by
    have h1 : 1 * (a + 1) ≤ 2 ^ s * (a + 1) := Nat.mul_le_mul_right (a + 1) hMpos
    omega
  obtain ⟨u, hu⟩ : ∃ u, t + 2 ^ s * (a + 1) = a + u := ⟨t + 2 ^ s * (a + 1) - a, by omega⟩
  refine ⟨(m' * u) % 2 ^ s, Nat.mod_lt _ hMpos, ?_⟩
  unfold hit
  have hdm : 2 ^ s * ((m' * u) / 2 ^ s) + (m' * u) % 2 ^ s = m' * u :=
    Nat.div_add_mod (m' * u) (2 ^ s)
  have e0 : m * (m' * u)
      = m * (2 ^ s * ((m' * u) / 2 ^ s) + (m' * u) % 2 ^ s) := by rw [hdm]
  have e1 : m * (m' * u)
      = 2 ^ s * (m * ((m' * u) / 2 ^ s)) + m * ((m' * u) % 2 ^ s) := by
    rw [e0, Nat.left_distrib]
    simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
  have e2 : m * (m' * u) = u + 2 ^ s * (c * u) := by
    rw [← Nat.mul_assoc, hmc, Nat.add_mul]
    simp [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
  have key : a + m * ((m' * u) % 2 ^ s) + 2 ^ s * (m * ((m' * u) / 2 ^ s))
      = a + u + 2 ^ s * (c * u) := by omega
  have step : (a + m * ((m' * u) % 2 ^ s)) % 2 ^ s = (a + u) % 2 ^ s := by
    rw [← Nat.add_mul_mod_self_left (a + m * ((m' * u) % 2 ^ s)) (2 ^ s)
          (m * ((m' * u) / 2 ^ s)), key,
        Nat.add_mul_mod_self_left]
  rw [step, ← hu, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt ht]
  simp

theorem hit_exists {m : Nat} (hm : Odd2 m) (a t s : Nat) (ht : t < 2 ^ s) :
    ∃ r, r < 2 ^ s ∧ hit a m (2 ^ s) t r = true := by
  obtain ⟨m', c, hmc⟩ := odd_inv m hm s
  exact hit_exists_aux m' c hmc a t ht

/-- **Exactly one per window.** Existence and uniqueness combine: a window of
    length `2^s` contains precisely one `k` with `a + m*k ≡ t (mod 2^s)`. -/
theorem count_one_window {m : Nat} (hm : Odd2 m) (a t s : Nat) (ht : t < 2 ^ s) :
    cntFrom (hit a m (2 ^ s) t) 0 (2 ^ s) = 1 := by
  obtain ⟨r, hrlt, hr⟩ := hit_exists hm a t s ht
  exact cntFrom_eq_one _ _ r hrlt hr
    (fun x hx hPx => hit_unique hm a t s x r hx hrlt hPx hr)

/-!
## The counting lemma

For `m` odd, `a : Nat` and `j < K`, the number of `k` in `[0, 2^K)` whose
affine image `a + m*k` has 2-adic valuation exactly `j` is `2^(K-j-1)`.

Valuation `j` is written as the exact modular condition
`(a + m*k) % 2^(j+1) = 2^j`, which says `2^j` divides the value and `2^(j+1)`
does not, and which already forces the value to be nonzero.
-/

/-- **The 2-adic counting lemma.** -/
theorem count_val2 {m : Nat} (hm : Odd2 m) (a j K : Nat) (hjK : j < K) :
    cntFrom (hit a m (2 ^ (j + 1)) (2 ^ j)) 0 (2 ^ K) = 2 ^ (K - j - 1) := by
  have hsplit : 2 ^ K = 2 ^ (j + 1) * 2 ^ (K - j - 1) := by
    rw [← Nat.pow_add]
    congr 1
    omega
  have ht : 2 ^ j < 2 ^ (j + 1) := by
    have h := Nat.two_pow_pos j
    rw [Nat.pow_succ]
    omega
  rw [hsplit,
      cntFrom_blocks _ _ (hit_periodic a m (2 ^ (j + 1)) (2 ^ j)),
      count_one_window hm a (2 ^ j) (j + 1) ht,
      Nat.mul_one]

/-!
## Sanity checks

A theorem can be true and still say the wrong thing. These instances are
evaluated by the KERNEL (`decide`, not `native_decide`), so they check that
`count_val2` means what it is claimed to mean on concrete numbers, and that
the statement is not vacuous.
-/

example : cntFrom (hit 5 3 (2 ^ 2) (2 ^ 1)) 0 (2 ^ 4) = 2 ^ (4 - 1 - 1) := by decide
example : cntFrom (hit 0 1 (2 ^ 1) (2 ^ 0)) 0 (2 ^ 5) = 2 ^ (5 - 0 - 1) := by decide
example : cntFrom (hit 7 9 (2 ^ 3) (2 ^ 2)) 0 (2 ^ 5) = 2 ^ (5 - 2 - 1) := by decide
example : cntFrom (hit 2 3 (2 ^ 1) (2 ^ 0)) 0 (2 ^ 6) = 2 ^ (6 - 0 - 1) := by decide

-- Sharpness: at j = K the count is NOT 2^(K-j-1); the hypothesis j < K is real.
example : cntFrom (hit 1 3 (2 ^ 3) (2 ^ 2)) 0 (2 ^ 2) = 1 := by decide
example : cntFrom (hit 0 3 (2 ^ 3) (2 ^ 2)) 0 (2 ^ 2) = 0 := by decide

end CollatzCylinder

-- Trust base. Core `Nat` only: no Mathlib, no classical choice.
#print axioms CollatzCylinder.odd_inv
#print axioms CollatzCylinder.pow_two_dvd_of_odd_mul
#print axioms CollatzCylinder.hit_unique
#print axioms CollatzCylinder.hit_exists
#print axioms CollatzCylinder.count_val2
