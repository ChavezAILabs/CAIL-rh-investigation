# RH Investigation — Phase 76 Aristotle Handoff — GatewayLinearLaw.lean
**Chavez AI Labs LLC — Applied Pathological Mathematics**
**Date:** June 10, 2026
**Prepared by:** Claude Fable 5 (session lead) — per standing workflow, this file is
WRITTEN here and VERIFIED by Aristotle. Never reversed.
**Mission:** Compile and axiom-audit `GatewayLinearLaw.lean` as the 17th file in the stack.

---

## 1. Context

Phase 76 Part A discovered and validated (10⁻¹⁵, 22 server readings; exact symbolic proof
in `phase76_partB_symbolic.py`) the **Gateway Linear Law** of the CAILculator ZDTP lift:

```
c_g(x) = −2⟪x, P_g + Q_g⟫        |M_g|² = ‖x‖² + 4(c_g² + 4(2σ)²)
```

`GatewayLinearLaw.lean` formalizes the law's algebraic consequences. It is self-contained
over Mathlib (imports only `Mathlib.Analysis.InnerProductSpace.EuclideanDist`) and does
NOT import or modify any of files 1–16. **Files 1–16 are locked — upload as-is, including
the full 138-line `UniversalPerimeter.lean` (standing rule).**

## 2. Build configuration (unchanged, standing)

- `lean-toolchain`: `leanprover/lean4:v4.28.0`
- `lake-manifest.json`: rev `8f9d9cff6bd728b17a24e163c9402775d9e6a365`, inputRev `v4.28.0`
- Add to `lakefile.toml`: `defaultTargets += ["GatewayLinearLaw"]` and a `[[lean_lib]]`
  entry `name = "GatewayLinearLaw"`, `globs = ["GatewayLinearLaw"]`
- `set_option maxHeartbeats 800000` if `nlinarith` stalls
- Do NOT use `EuclideanSpace.norm_sq_eq_inner` or `EuclideanSpace.inner_def`
  (absent from Mathlib v4.28.0 — standing constraint since Phase 72)

## 3. Tasks

### Task 1 — `gateway_magSq_sub` and `pairing_sigma_independent`
Both should close by `unfold` + `inner_sub_right`/`inner_add_right` + `ring`. If the
inner-product rewrites resist (real inner product elaboration), try
`real_inner_sub_right` / `real_inner_add_right`, or expand via
`inner_sub_left`-side variants after `real_inner_comm`.

### Task 2 — `gateway_pairing_iff`
The provided proof uses `nlinarith` on the quadratic identity. If `nlinarith` fails:
derive from Task 1 — `a = b ↔ a − b = 0`, then `gateway_magSq_sub`, then
`mul_eq_zero`-free form: `16 * p = 0 ↔ p = 0` via `mul_eq_zero` and `(by norm_num : (16:ℝ) ≠ 0)`.
Recommended robust proof:

```lean
theorem gateway_pairing_iff (x : Sed) (σ : ℝ) (g h : Fin 6) :
    gatewayMagSq x σ g = gatewayMagSq x σ h ↔
    ⟪x, gatewaySum g - gatewaySum h⟫ * ⟪x, gatewaySum g + gatewaySum h⟫ = 0 := by
  rw [← sub_eq_zero, gateway_magSq_sub, mul_eq_zero]
  simp [(by norm_num : (16:ℝ) ≠ 0)]
```

(Place `gateway_magSq_sub` before `gateway_pairing_iff` in the file if this route is used.)

### Task 3 — Axiom audit

```
#print axioms gateway_pairing_iff
#print axioms gateway_magSq_sub
#print axioms pairing_sigma_independent
-- Target for all three: [propext, Classical.choice, Quot.sound]
```

`riemann_hypothesis` footprint must remain `[propext, riemann_critical_line,
Classical.choice, Quot.sound]` — this file cannot touch it (no imports from the stack),
verify anyway.

### Task 4 — Stretch goal (non-blocking): `ba_asymptote_sq`
```lean
-- For c : ℝ → ℝ with c t = -2*t + r t, r bounded:
-- Tendsto (fun t => (t^2 + 4*(c t)^2 + K) / t^2) atTop (𝓝 17)
```
Use `Filter.Tendsto` + `tendsto_const_div_atTop_nhds_zero_nat`-style lemmas or
`Asymptotics.isLittleO`. If it does not close cleanly, report and defer to Phase 77 —
do NOT introduce `sorry`.

## 4. Standing orders
- Zero new sorries anywhere. Zero new axioms.
- Files 1–16 untouched.
- Report: `lake build` job count · error count · sorry count, and `#print axioms`
  verbatim for the three theorems.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering.*
*Phase 76 · June 10, 2026 · github.com/ChavezAILabs/CAIL-rh-investigation*
