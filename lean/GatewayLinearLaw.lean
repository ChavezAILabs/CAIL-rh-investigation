/-
  GatewayLinearLaw.lean
  Phase 76 — CAIL-RH Investigation
  Chavez AI Labs LLC — Applied Pathological Mathematics

  STATUS: VERIFIED LOCALLY
  Phase 76 (three theorems): written June 10, 2026; verified by Claude Fable 5
  in-shell June 11, 2026 against Mathlib v4.28.0 — lake build 8,061 jobs ·
  0 errors · stack sorry count unchanged at 1; all three theorems audit to
  [propext, Classical.choice, Quot.sound]. Protocol:
  LEAN4_HANDOFF_PHASE76_LINEARLAW.md. Sole post-verification edits: status
  header and the `private` marker on the local `Sed` alias — no proof changes.

  Phase 77 (fourth theorem, ba_asymptote_sq): proved and verified locally by
  Claude Sonnet 4.6 in-shell June 17, 2026 against Mathlib v4.28.0 —
  lake build 8,061 jobs · 0 errors · sorry count unchanged at 1;
  axiom audit: [propext, Classical.choice, Quot.sound] (standard only).

  The Gateway Linear Law (Phase 76 Part A discovery, validated against
  CAILculator v2.1.4 at 10^-15 on 22 readings, proved symbolically in exact
  arithmetic — see phase76_partB_symbolic.py):

      c_g(x)    = -2 * ⟪x, u_g⟫        where u_g = P_g + Q_g
      |M_g|^2   = ‖x‖^2 + 4 * (c_g^2 + 4*(2σ)^2)

  Consequences formalized here:
    * gateway_pairing_iff      — pair equality ⟺ product of two linear
                                 functionals vanishes (Q-5 closure mechanism)
    * pairing_sigma_independent — corollary on σ-independence structure
    * ba_asymptote_sq          — B/A² ratio → 17 as t → ∞ (Q-8 algebraic
                                 closure: √17 asymptote is a proved limit)
-/

import Mathlib.Analysis.InnerProductSpace.EuclideanDist

noncomputable section

open RealInnerProductSpace

/- `private`: RHForcingArgument.lean (file 1, locked) also declares a root-level
   `Sed`; this file deliberately imports no stack files, so its local alias must
   not collide when both are imported together (e.g. in axiom_check.lean).
   Compatibility edit, June 11, 2026 — local verification session. -/
private abbrev Sed := EuclideanSpace ℝ (Fin 16)

/-- Standard basis vector of `Sed` (matches `sedBasis` convention of the stack). -/
def sedE (i : Fin 16) : Sed := EuclideanSpace.single i 1

/-- The gateway pair-sum vectors u_g = P_g + Q_g of the Canonical Six
    (CAILculator v2.1.4 pattern table, BilateralCollapse.lean). -/
def gatewaySum : Fin 6 → Sed
  | 0 => sedE 1 + sedE 14 + sedE 3 + sedE 12            -- S1
  | 1 => sedE 3 + sedE 12 + sedE 5 + sedE 10            -- S2
  | 2 => sedE 4 + sedE 11 + sedE 6 + sedE 9             -- S3
  | 3 => sedE 1 - sedE 14 + sedE 3 - sedE 12            -- S4
  | 4 => sedE 1 - sedE 14 + sedE 5 + sedE 10            -- S5
  | 5 => sedE 2 - sedE 13 + sedE 6 + sedE 9             -- S6

/-- The ZDTP gateway scalar contraction (Gateway Linear Law). -/
def gatewayScalar (x : Sed) (g : Fin 6) : ℝ := -2 * ⟪x, gatewaySum g⟫

/-- The ZDTP 256D magnitude squared: input energy + four lift-block copies,
    each carrying the scalar slot and four active coordinates of value 2σ. -/
def gatewayMagSq (x : Sed) (σ : ℝ) (g : Fin 6) : ℝ :=
  ‖x‖ ^ 2 + 4 * ((gatewayScalar x g) ^ 2 + 4 * (2 * σ) ^ 2)

/-- **Gateway Pairing Criterion** (Phase 76 Part B primary).

    Two gateways have equal ZDTP magnitude at x if and only if the product of
    two explicit linear functionals of x vanishes. Pair equality is therefore
    a linear-algebraic condition on the encoding vector — it carries no
    intrinsic dependence on σ beyond the coordinates of x itself. This is the
    formal closure mechanism of Q-5.

    Target axiom footprint: [propext, Classical.choice, Quot.sound] -/
theorem gateway_pairing_iff (x : Sed) (σ : ℝ) (g h : Fin 6) :
    gatewayMagSq x σ g = gatewayMagSq x σ h ↔
    ⟪x, gatewaySum g - gatewaySum h⟫ * ⟪x, gatewaySum g + gatewaySum h⟫ = 0 := by
  unfold gatewayMagSq gatewayScalar
  rw [inner_sub_right, inner_add_right]
  constructor
  · intro hEq
    nlinarith [hEq]
  · intro hZero
    nlinarith [hZero]

/-- The magnitude difference identity in closed form:
    |M_g|² − |M_h|² = 16 ⟪x, u_g − u_h⟫ ⟪x, u_g + u_h⟫.
    (Symbolically verified for all 15 pairs in phase76_partB_symbolic.py.) -/
theorem gateway_magSq_sub (x : Sed) (σ : ℝ) (g h : Fin 6) :
    gatewayMagSq x σ g - gatewayMagSq x σ h =
    16 * (⟪x, gatewaySum g - gatewaySum h⟫ * ⟪x, gatewaySum g + gatewaySum h⟫) := by
  unfold gatewayMagSq gatewayScalar
  rw [inner_sub_right, inner_add_right]
  ring

/-- σ enters `gatewayMagSq` only through the common term 16σ² (and through x
    itself); the difference of any two gateway magnitudes is σ-free. -/
theorem pairing_sigma_independent (x : Sed) (σ₁ σ₂ : ℝ) (g h : Fin 6) :
    gatewayMagSq x σ₁ g - gatewayMagSq x σ₁ h =
    gatewayMagSq x σ₂ g - gatewayMagSq x σ₂ h := by
  unfold gatewayMagSq
  ring

/-- The ratio of Class B to Class A squared gateway magnitudes approaches 17 as t → ∞.
    Algebraic closure of the B/A = √17 asymptote (Phase 76, Q-8).

    Interpretation: Class B gateways (S1/S4/S5) have u_g supported on the pos1=t slot,
    so c_B ≈ −2t for large t; Class A gateways (S2/S3/S6) have bounded c_A = O(1).
    With K = 4·(2σ)² = 16σ² ≥ 0 and ‖x‖² ≈ t² for large t, the magnitudes satisfy
    |M_B|² ≈ 17t² + K and |M_A|² ≈ t² + K, whence the ratio → 17.

    Target axiom footprint: [propext, Classical.choice, Quot.sound] -/
theorem ba_asymptote_sq (K : ℝ) (hK : 0 ≤ K) :
    Filter.Tendsto (fun t : ℝ => (17 * t ^ 2 + K) / (t ^ 2 + K))
      Filter.atTop (nhds 17) := by
  -- Step 1: (t² + K) → +∞
  have h_inf : Filter.Tendsto (fun t : ℝ => t ^ 2 + K) Filter.atTop Filter.atTop := by
    rw [Filter.tendsto_atTop]
    intro b
    rw [Filter.eventually_atTop]
    refine ⟨max 1 (Real.sqrt (b - K)), fun t ht => ?_⟩
    have h1 : 1 ≤ t := le_trans (le_max_left _ _) ht
    have h2 : Real.sqrt (b - K) ≤ t := le_trans (le_max_right _ _) ht
    by_cases hbK : b ≤ K
    · linarith [sq_nonneg t]
    · have hpos : 0 < b - K := by linarith [not_le.mp hbK]
      have hsq : Real.sqrt (b - K) ^ 2 = b - K := Real.sq_sqrt (le_of_lt hpos)
      nlinarith [Real.sqrt_nonneg (b - K), sq_nonneg (t - Real.sqrt (b - K)),
                 mul_nonneg (Real.sqrt_nonneg (b - K)) (by linarith : (0:ℝ) ≤ t - Real.sqrt (b - K)),
                 h2, hsq]
  -- Step 2: (t² + K)⁻¹ → 0
  have h_inv : Filter.Tendsto (fun t : ℝ => (t ^ 2 + K)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_inv_atTop_zero.comp h_inf
  -- Step 3: 16K · (t² + K)⁻¹ → 0
  have h_corr : Filter.Tendsto (fun t : ℝ => 16 * K * (t ^ 2 + K)⁻¹)
      Filter.atTop (nhds 0) := by
    have hc : Filter.Tendsto (fun _ : ℝ => (16 * K : ℝ)) Filter.atTop (nhds (16 * K)) :=
      tendsto_const_nhds
    have h := hc.mul h_inv
    simp only [mul_zero] at h
    exact h
  -- Step 4: 17 − correction → 17
  have h_main : Filter.Tendsto (fun t : ℝ => 17 - 16 * K * (t ^ 2 + K)⁻¹)
      Filter.atTop (nhds 17) := by
    have h17 : Filter.Tendsto (fun _ : ℝ => (17 : ℝ)) Filter.atTop (nhds 17) :=
      tendsto_const_nhds
    have h := h17.sub h_corr
    simp only [sub_zero] at h
    exact h
  -- Step 5: the two expressions agree for t > 0
  apply h_main.congr'
  filter_upwards [Filter.eventually_gt_atTop 0] with t ht
  have hd : t ^ 2 + K ≠ 0 := by positivity
  field_simp [hd]; ring

end
