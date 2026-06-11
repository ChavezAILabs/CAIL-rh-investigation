/-
  GatewayLinearLaw.lean
  Phase 76 — CAIL-RH Investigation
  Chavez AI Labs LLC — Applied Pathological Mathematics

  STATUS: VERIFIED LOCALLY (written June 10, 2026; verified by Claude Fable 5
  in-shell June 11, 2026 against Mathlib v4.28.0 — lake build 8,061 jobs ·
  0 errors · stack sorry count unchanged at 1; all three theorems audit to
  [propext, Classical.choice, Quot.sound]. Protocol:
  LEAN4_HANDOFF_PHASE76_LINEARLAW.md. Sole post-verification edits: this status
  header and the `private` marker on the local `Sed` alias — no proof changes.)

  The Gateway Linear Law (Phase 76 Part A discovery, validated against
  CAILculator v2.1.4 at 10^-15 on 22 readings, proved symbolically in exact
  arithmetic — see phase76_partB_symbolic.py):

      c_g(x)    = -2 * ⟪x, u_g⟫        where u_g = P_g + Q_g
      |M_g|^2   = ‖x‖^2 + 4 * (c_g^2 + 4*(2σ)^2)

  Consequences formalized here:
    * gateway_pairing_iff      — pair equality ⟺ product of two linear
                                 functionals vanishes (Q-5 closure mechanism)
    * pairing_sigma_independent — corollary on σ-independence structure
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

end
