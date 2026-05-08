/-
  GatewayScaling.lean
  Phase 74 — CAIL-RH Investigation
  Author: Paul Chavez, Chavez AI Labs LLC
  Date: May 2026

  Formalizes the Gateway Integer Law: the 2σ coordinate scaling law empirically
  confirmed in Phase 73 (CAILculator Q-11, AIEX-620).

  Main theorem:
    gateway_integer_iff_critical_line (s : ℂ) (g : Gateway) (hs : 0 < s.re ∧ s.re < 1) :
      lift_coordinate s g ∈ ({-1, 1} : Set ℝ) ↔ s.re = 1 / 2

  Gateway type: Fin 6, corresponding to the 6 canonical prime root vectors
  S1/p=2 through S6/p=13. The 2σ law is gateway-universal (Q-11 closed,
  AIEX-620): the coordinate 2·Re(s) is the same for all six gateways.

  Algebraic derivation of lift_coordinate:
    H(s) = (s.re − 1/2) • u_antisym                     [sedenion_Hamiltonian def]
    ⟪H(s), u_antisym⟫_ℝ = (s.re − 1/2) · ‖u_antisym‖²  [real_inner_smul_left]
                         = (s.re − 1/2) · 2              [u_antisym_norm_sq]
                         = 2·s.re − 1
    lift_coordinate s g := ⟪H(s), u_antisym⟫_ℝ + 1
                         = 2·s.re                        [lift_coord_scaling]

  The gateway index g is present to anchor the type semantics (each of the six
  prime gateway directions S1–S6 is an independent measurement context) but the
  coordinate value is g-independent by Q-11 universality. See gateway_unit for
  the canonical ROOT_16D vectors defining each gateway direction.

  Strip hypothesis in gateway_integer_iff_critical_line:
    2·s.re ∈ {−1, 1} admits both s.re = 1/2 (giving 1) and s.re = −1/2 (giving −1).
    The condition 0 < s.re rules out s.re = −1/2 — the unique integer achieved
    within the strip is 1, at exactly s.re = 1/2.

  Axiom footprint: [propext, Classical.choice, Quot.sound]  (standard only)
  Tag: #phase-74-eigenvalue
-/

import SedenionicHamiltonian

noncomputable section

open Real Complex InnerProductSpace Set

/-! ## Gateway Type -/

/-- The six canonical prime gateway directions, indexed 0–5 (S1–S6).

    Chosen as Fin 6 rather than a named inductive to integrate directly with
    the existing stack infrastructure (EuclideanSpace ℝ (Fin 16), sedBasis,
    Fin.sum_univ_succ, decide tactic on finite sets). -/
abbrev Gateway := Fin 6

-- Named abbreviations for the six prime gateways (readability)
def S1 : Gateway := 0
def S2 : Gateway := 1
def S3 : Gateway := 2
def S4 : Gateway := 3
def S5 : Gateway := 4
def S6 : Gateway := 5

/-! ## Gateway Unit Vectors -/

/-- The canonical ROOT_16D prime root vector for each gateway.

    These are the sedenion basis directions along which each prime oscillates
    in the AIEX-001 embedding F(s). Indexed by Gateway = Fin 6.

    Canonical ROOT_16D assignment (Phase 63, CAIL-RH):
      S1 (p=2):  e₃ − e₁₂     support {3, 12}
      S2 (p=3):  e₅ + e₁₀     support {5, 10}
      S3 (p=5):  e₃ + e₆      support {3, 6}
      S4 (p=7):  e₂ − e₇      support {2, 7}
      S5 (p=11): e₂ + e₇      support {2, 7}
      S6 (p=13): e₆ + e₉      support {6, 9}

    Note: all six gateway unit vectors have support disjoint from u_antisym
    (support {4, 5, 10, 11}), so ⟪u_antisym, gateway_unit g⟫_ℝ = 0 for all g.
    The 2σ law therefore arises from the H(s)–u_antisym projection, not from
    any H(s)–gateway_unit projection. (See lift_coordinate.) -/
def gateway_unit (g : Gateway) : Sed :=
  match g.val with
  | 0 => sedBasis 3 - sedBasis 12    -- S1, p=2: e₃ − e₁₂
  | 1 => sedBasis 5 + sedBasis 10    -- S2, p=3: e₅ + e₁₀
  | 2 => sedBasis 3 + sedBasis 6     -- S3, p=5: e₃ + e₆
  | 3 => sedBasis 2 - sedBasis 7     -- S4, p=7: e₂ − e₇
  | 4 => sedBasis 2 + sedBasis 7     -- S5, p=11: e₂ + e₇
  | _ => sedBasis 6 + sedBasis 9     -- S6, p=13: e₆ + e₉ (only remaining case: val=5)

/-! ## Lift Coordinate -/

/-- The gateway lift coordinate: sedenion-algebraic translation of the
    CAILculator 2σ scaling law.

    Defined as the real inner product of the Sedenionic Hamiltonian H(s) with
    the tension axis u_antisym, offset by 1:

      lift_coordinate s g := ⟪H(s), u_antisym⟫_ℝ + 1

    Derivation (see lift_coord_scaling):
      ⟪H(s), u_antisym⟫_ℝ = (s.re − 1/2) · ‖u_antisym‖² = (s.re − 1/2) · 2 = 2·s.re − 1
      lift_coordinate s g  = (2·s.re − 1) + 1 = 2·s.re

    Gateway universality (Q-11, AIEX-620): the value is g-independent because
    the six gateway unit vectors all have support disjoint from u_antisym's
    support {4,5,10,11}. The g parameter anchors the type semantics; each
    gateway is a separate measurement context in the 32D CAILculator lift. -/
def lift_coordinate (s : ℂ) (_g : Gateway) : ℝ :=
  @inner ℝ Sed _ (sedenion_Hamiltonian s) u_antisym + 1

/-! ## Core Scaling Lemma -/

/-- The lift coordinate equals 2 · Re(s): the Lean statement of the 2σ law.

    Proof chain:
      unfold → ⟪(s.re − 1/2) • u_antisym, u_antisym⟫_ℝ + 1
      real_inner_smul_left  → (s.re − 1/2) · ⟪u_antisym, u_antisym⟫_ℝ + 1
      real_inner_self_eq_norm_sq → (s.re − 1/2) · ‖u_antisym‖² + 1
      u_antisym_norm_sq     → (s.re − 1/2) · 2 + 1
      ring                  → 2 · s.re

    Axiom footprint: [propext, Classical.choice, Quot.sound] -/
lemma lift_coord_scaling (s : ℂ) (g : Gateway) : lift_coordinate s g = 2 * s.re := by
  unfold lift_coordinate sedenion_Hamiltonian
  rw [real_inner_smul_left, real_inner_self_eq_norm_sq, u_antisym_norm_sq]
  ring

/-! ## Gateway Independence -/

/-- Gateway independence: the lift coordinate is the same for all six gateways.
    This is definitional — the gateway parameter is unused in lift_coordinate.
    Formally documents Q-11 universality (AIEX-620). -/
lemma lift_coord_gateway_independent (s : ℂ) (g h : Gateway) :
    lift_coordinate s g = lift_coordinate s h := by
  rfl

/-! ## Gateway Integer Law -/

/-- **Gateway Integer Law** (Phase 74 primary theorem).

    The lift coordinate is an element of {−1, 1} if and only if s lies on the
    critical line Re(s) = 1/2, for s in the critical strip 0 < Re(s) < 1.

    By lift_coord_scaling, lift_coordinate s g = 2 · Re(s). The condition
    2 · Re(s) ∈ {−1, 1} admits two solutions in ℝ:
      2 · Re(s) = 1  →  Re(s) = 1/2   ✓  (within the strip)
      2 · Re(s) = −1 →  Re(s) = −1/2  ✗  (ruled out by 0 < Re(s))

    Within the critical strip, the unique integer value achieved is 1, at
    exactly Re(s) = 1/2. The set {−1, 1} is used rather than {1} to preserve
    the Class A / Class B gateway sign structure observed empirically (AIEX-620).

    Empirical basis: CAILculator Q-11 (AIEX-620) confirms the 2σ law holds
    across all six gateways S1–S6 with precision 10⁻¹⁵.

    Axiom footprint: [propext, Classical.choice, Quot.sound] -/
theorem gateway_integer_iff_critical_line (s : ℂ) (g : Gateway) (hs : 0 < s.re ∧ s.re < 1) :
    lift_coordinate s g ∈ ({-1, 1} : Set ℝ) ↔ s.re = 1 / 2 := by
  rw [lift_coord_scaling]
  simp only [mem_insert_iff, mem_singleton_iff]
  constructor
  · rintro (h | h)
    · exfalso; linarith [hs.1]
    · linarith
  · intro h
    right; linarith

end
