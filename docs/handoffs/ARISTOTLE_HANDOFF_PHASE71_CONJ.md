# RH Investigation — Phase 71 Part 2 Aristotle Prompt
**Chavez AI Labs | Applied Pathological Mathematics**
**Date:** April 16, 2026
**Prepared by:** Claude Desktop + Gemini CLI (proof attempt record)
**Mission:** Discharge the `riemannZeta_conj` axiom — prove it as a theorem from Mathlib
infrastructure. This upgrades Phase 71 Part 2 from 2 non-standard axioms to 1.

---

## Context

Phase 71 Part 2 builds at:

```
lake build → 8,036 jobs · 0 errors · 0 sorries  (verified April 16, 2026)

#print axioms riemann_hypothesis
→ [propext, riemann_critical_line, Classical.choice, Quot.sound]

#print axioms riemannZeta_quadruple_zero
→ [propext, riemannZeta_conj, Classical.choice, Quot.sound]

#print axioms quadruple_critical_line_characterization
→ [propext, Classical.choice, Quot.sound]
```

Two non-standard axioms in the full stack:
1. `riemann_critical_line` — the Riemann Hypothesis (main chain, untouched)
2. `riemannZeta_conj` — Schwarz reflection for ζ (Branch B, independent)

This handoff targets **`riemannZeta_conj` only**. The main chain is not modified.

---

## The Target

Replace this axiom in `EulerProductBridge.lean`:

```lean
-- CURRENT (axiom):
axiom riemannZeta_conj (s : ℂ) (hs : s ≠ 1) :
    riemannZeta (starRingEnd ℂ s) = starRingEnd ℂ (riemannZeta s)
```

With a proved theorem:

```lean
-- TARGET (theorem, 0 sorries):
theorem riemannZeta_conj (s : ℂ) (hs : s ≠ 1) :
    riemannZeta (starRingEnd ℂ s) = starRingEnd ℂ (riemannZeta s) := by
  ...
```

**Success axiom footprint:**
```
#print axioms riemannZeta_conj
→ [propext, Classical.choice, Quot.sound]

#print axioms riemannZeta_quadruple_zero
→ [propext, Classical.choice, Quot.sound]
```

---

## Build Configuration

### `lean-toolchain`
```
leanprover/lean4:v4.28.0
```

### `lake-manifest.json` (key entries — do not change)
```
rev: "8f9d9cff6bd728b17a24e163c9402775d9e6a365"
inputRev: "v4.28.0"
```

### `lakefile.toml` — no changes needed
All 12 files already registered. `EulerProductBridge` is file 12.

---

## Stack State — Do Not Modify Files 1–11

| # | File | Status |
|---|---|---|
| 1–9 | Foundation files | ✅ Locked |
| 10 | `ZetaIdentification.lean` | ✅ Locked |
| 11 | `RiemannHypothesisProof.lean` | ✅ Locked |
| 12 | `EulerProductBridge.lean` | ⚠️ **Active — target file for this handoff** |

All changes go in `EulerProductBridge.lean` only.

---

## Confirmed Mathlib Infrastructure (Phase 71 Audit)

All of these exist in Mathlib v4.28.0 — confirmed by audit and Gemini CLI:

| Theorem / Object | File | Signature |
|---|---|---|
| `differentiableAt_riemannZeta` | `LSeries/RiemannZeta.lean` | `s ≠ 1 → DifferentiableAt ℂ riemannZeta s` |
| `riemannZeta_eulerProduct_exp_log` | `LSeries/RiemannZeta.lean` | `1 < s.re → cexp(∑' p, -log(1-p^{-s})) = riemannZeta s` |
| `exp_conj` | `Analysis/Complex/Exponential.lean:173` | `exp(conj s) = conj(exp s)` |
| `conj_tsum` | `Analysis/Complex/Basic.lean:568` | `conj(∑' a, f a) = ∑' a, conj(f a)` |
| `log_conj` | `SpecialFunctions/Complex/Log.lean:123` | `x.arg ≠ π → log(conj x) = conj(log x)` |
| `cpow_conj` | `SpecialFunctions/Pow/Complex.lean:234` | `x.arg ≠ π → conj(x)^s = conj(x^(conj s))` |
| `star_sub` | Mathlib | `star(r - s) = star r - star s` |
| `star_div` | Mathlib | `star(x / y) = star x / star y` |
| `star_star` | Mathlib | `star(star r) = r` |
| `Filter.Tendsto.congr` | Mathlib | `(∀ x, f₁ x = f₂ x) → Tendsto f₁ l₁ l₂ → Tendsto f₂ l₁ l₂` |
| `conjLIE` | Mathlib | `ℂ ≃ₗᵢ[ℝ] ℂ` (complex conjugation as LinearIsometryEquiv) |

---

## Proof Strategy — Two Steps

### Step 1: `riemannZeta_conj_of_re_gt_one` (Re(s) > 1 case)

Prove via the Euler product. For Re(s) > 1, `riemannZeta_eulerProduct_exp_log` gives:
```
cexp(∑' p, −log(1 − p^{−s})) = riemannZeta s
```
Conjugate both sides using `exp_conj` + `conj_tsum` + `log_conj` + `cpow_conj`:
```
riemannZeta(conj s) = conj(riemannZeta s)    for Re(s) > 1
```

Branch cut conditions needed:
- `(p : ℂ).arg ≠ π` — true since p is a positive prime (arg = 0)
- `(1 − p^{−s}).arg ≠ π` — true for Re(s) > 1 since `|p^{−s}| = p^{-Re(s)} < 1`,
  placing `1 − p^{−s}` in the right half-plane

This step is straightforward and already partially scaffolded by Gemini CLI.

### Step 2: `riemannZeta_conj` — Extension to all s ≠ 1

**The mathematical argument:**

Let f₁(s) = riemannZeta(star s) and f₂(s) = star(riemannZeta s).

Both are analytic on ℂ \ {1}:
- f₁: composition of `riemannZeta` (analytic by `differentiableAt_riemannZeta`) with
  `starRingEnd ℂ` (anti-holomorphic) — the composition s ↦ star(riemannZeta(star s))
  is analytic because star s is anti-holomorphic and then `riemannZeta` is holomorphic
- f₂: `star ∘ riemannZeta` — anti-holomorphic composition

Both agree on `{s | 1 < s.re}` (open, connected) by Step 1.

Identity principle: two analytic functions agreeing on an open connected set agree
everywhere on their shared domain of analyticity.

**Lean path — `DifferentiableAt.star_comp_star` helper lemma:**

Gemini CLI established this key lemma and confirmed it nearly compiles:

```lean
/-- If f is differentiable at (star s), then s ↦ star(f(star s)) is differentiable at s.
    Proof: the derivative of s ↦ star(f(star s)) is star(f'(star s)), via
    the limit definition and the isometric properties of star. -/
theorem DifferentiableAt.star_comp_star {f : ℂ → ℂ} {s : ℂ}
    (hf : DifferentiableAt ℂ f (star s)) :
    DifferentiableAt ℂ (fun z => star (f (star z))) s := by
  apply HasDerivAt.differentiableAt (f' := star (deriv f (star s)))
  rw [hasDerivAt_iff_tendsto_slope]
  let F (h : ℂ) := (star (f (star (s + h))) - star (f (star s))) / h
  let G (h : ℂ) := star ((f (star s + star h) - f (star s)) / star h)
  apply tendsto_congr (f₁ := F) (f₂ := G)
  · refine eventually_nhdsWithin_iff.mpr (eventually_of_forall fun h hh => ?_)
    unfold F G
    rw [star_add, star_sub, star_div, star_star]
  -- Show G h → star L
  -- h_map: starRingEnd ℂ maps nhdsWithin 0 {0}ᶜ to nhdsWithin 0 {0}ᶜ
  have h_map : Tendsto (starRingEnd ℂ) (nhdsWithin 0 {0}ᶜ) (nhdsWithin 0 {0}ᶜ) := by
    have h_bij : Function.Bijective (starRingEnd ℂ) := by
      constructor
      · intro x y h; simpa using congr_arg star h
      · intro y; exact ⟨star y, star_star y⟩
    rw [show ({0}ᶜ : Set ℂ) = (starRingEnd ℂ) ⁻¹' {0}ᶜ by
          ext x; simp [starRingEnd_apply]]
    exact conjLIE.toHomeomorph.tendsto_nhdsWithin_preimage
      (by simp [starRingEnd_apply, conjLIE])
  convert (hf.hasDerivAt.tendsto_slope.comp h_map) using 1
  · ext h
    simp only [Function.comp_apply, starRingEnd_apply, slope, G]
    rw [star_star]
  · simp
```

**If `DifferentiableAt.star_comp_star` compiles**, then `riemannZeta_conj` follows via
`eqOn_of_preconnected_of_eventuallyEq` (or `AnalyticOn.eq_of_frequently_eq`):

```lean
theorem riemannZeta_conj (s : ℂ) (hs : s ≠ 1) :
    riemannZeta (starRingEnd ℂ s) = starRingEnd ℂ (riemannZeta s) := by
  let f₁ : ℂ → ℂ := fun z => riemannZeta (starRingEnd ℂ z)
  let f₂ : ℂ → ℂ := fun z => starRingEnd ℂ (riemannZeta z)
  let U : Set ℂ := {z | z ≠ 1}
  -- 1. Both analytic on U
  have hf₁ : AnalyticOnNhd ℂ f₁ U := fun z hz => by
    apply DifferentiableAt.star_comp_star
    exact differentiableAt_riemannZeta (by simp [starRingEnd_apply, hz])
  have hf₂ : AnalyticOnNhd ℂ f₂ U := fun z hz =>
    (differentiableAt_riemannZeta hz).analyticAt.star_comp  -- or appropriate lemma
  -- 2. They agree on {s | 1 < s.re} ⊆ U (open, connected)
  have h_agree : ∀ z : ℂ, 1 < z.re → f₁ z = f₂ z :=
    fun z hz => riemannZeta_conj_of_re_gt_one z hz
  -- 3. Identity principle: {s | 1 < s.re} accumulates at s
  apply eqOn_of_preconnected_of_eventuallyEq
    (isPreconnected_compl_singleton 1)
    hf₁ hf₂ hs
  · -- Frequently equal near s via the half-plane
    rw [Filter.EventuallyEq, eventually_nhdsWithin_iff]
    exact eventually_of_forall (fun z hz => h_agree z hz)
```

**Alternative: search for `Complex.eq_on_open_of_differentiableOn` or similar.**
Mathlib may have a more direct identity principle lemma. Search before attempting
the `eqOn_of_preconnected_of_eventuallyEq` route.

---

## Key Mathlib Searches (Before Writing Proofs)

Run these checks in `EulerAudit.lean` before writing the proofs:

```lean
-- Identity principle candidates:
#check @AnalyticOn.eq_of_frequently_eq
#check @eqOn_of_preconnected_of_eventuallyEq
#check @Complex.eq_on_open_of_differentiableOn

-- conjLIE homeomorphism:
#check @conjLIE
#check @LinearIsometryEquiv.toHomeomorph
#check @Homeomorph.tendsto_nhdsWithin_preimage

-- AnalyticOnNhd for anti-holomorphic functions:
#check @AnalyticAt.comp_star
#check @DifferentiableAt.analyticAt

-- Filter:
#check @Filter.Tendsto.congr
#check @tendsto_congr
#check @nhdsWithin_star  -- may not exist; use conjLIE instead
```

---

## Tasks

### Task 1 — Confirm `riemannZeta_conj_of_re_gt_one`

Verify the Re(s)>1 case builds cleanly. This is the Euler product conjugation step.
It should be straightforward given the confirmed Mathlib infrastructure.

Report the exact proof if it differs from the strategy above.

### Task 2 — Prove `DifferentiableAt.star_comp_star`

This is the core new lemma. The Gemini CLI proof attempt is provided above.
The main issue was `h_map` — specifically `conjLIE.toHomeomorph.tendsto_nhdsWithin_preimage`.

If `conjLIE.toHomeomorph.tendsto_nhdsWithin_preimage` does not have the right signature,
try:
```lean
-- Alternative h_map approaches:
exact conjLIE.isometry.toHomeomorph.tendsto_nhdsWithin ...
-- or:
exact (Homeomorph.comp_continuous conjLIE.toHomeomorph).tendsto_nhdsWithin_proper ...
-- or construct directly from:
-- conjLIE.continuous.continuousAt and the fact that conjLIE 0 = 0
```

### Task 3 — Prove `riemannZeta_conj`

Using `DifferentiableAt.star_comp_star` and the identity principle.

Search for the cleanest Mathlib identity principle lemma first. If none fits cleanly,
fall back to `eqOn_of_preconnected_of_eventuallyEq` as scaffolded above.

### Task 4 — Axiom footprint verification

After all three tasks compile with 0 sorries:

```lean
#print axioms riemannZeta_conj
-- Target: [propext, Classical.choice, Quot.sound]

#print axioms riemannZeta_quadruple_zero
-- Target: [propext, Classical.choice, Quot.sound]

#print axioms riemann_hypothesis
-- Must remain: [propext, riemann_critical_line, Classical.choice, Quot.sound]
-- riemann_hypothesis MUST NOT change
```

**If `riemannZeta_conj` cannot be proved from current Mathlib:**
Keep it as a named axiom. Report precisely which step failed and what would be
needed. Do NOT introduce `sorry`.

---

## Files to Upload

Upload from `CAIL-rh-investigation/lean/` (canonical local path):

| File | Notes |
|---|---|
| `RHForcingArgument.lean` | Locked — upload as-is |
| `MirrorSymmetryHelper.lean` | Locked — upload as-is |
| `MirrorSymmetry.lean` | Locked — upload as-is |
| `UnityConstraint.lean` | Locked — upload as-is |
| `NoetherDuality.lean` | Locked — upload as-is |
| `UniversalPerimeter.lean` | ⚠️ FULL 138-LINE VERSION — always send local copy |
| `AsymptoticRigidity.lean` | Locked — upload as-is |
| `SymmetryBridge.lean` | Locked — upload as-is |
| `PrimeEmbedding.lean` | Locked — upload as-is |
| `ZetaIdentification.lean` | Locked — upload as-is |
| `RiemannHypothesisProof.lean` | Locked — upload as-is |
| `EulerAudit.lean` | Audit file — upload as-is |
| `EulerProductBridge.lean` | ⚠️ TARGET — current version with `riemannZeta_conj` as axiom |
| `lakefile.toml` | No changes needed |
| `lean-toolchain` | `leanprover/lean4:v4.28.0` |
| `lake-manifest.json` | Unchanged |

---

## Standing Orders

- **Do not modify files 1–11.** Only `EulerProductBridge.lean` changes.
- **Zero new sorries.** If `riemannZeta_conj` cannot close, keep the named axiom
  and document what failed. Do not introduce `sorry` anywhere.
- **`riemann_hypothesis` axiom footprint must not change.** Verify verbatim.
- **Do not upgrade Mathlib.** Pin to `v4.28.0` / rev `8f9d9cff6bd728b17a24e163c9402775d9e6a365`.
- **`set_option maxHeartbeats 800000`** on `EulerProductBridge.lean`.
- **`UniversalPerimeter.lean`:** Always send the full 138-line local version.

---

## What to Report

1. **Task 1 result:** `riemannZeta_conj_of_re_gt_one` proof — success or failure with exact error
2. **Task 2 result:** `DifferentiableAt.star_comp_star` — proof term if closed, or precise
   failure point with what was tried
3. **Task 3 result:** `riemannZeta_conj` — theorem or axiom, with proof term if proved
4. **Task 4:** `#print axioms` output verbatim for all three theorems
5. **Full build:** `lake build` job count · error count · sorry count

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 71 Part 2 — riemannZeta_conj discharge attempt*
*April 16, 2026*
*GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation*
*Zenodo: https://doi.org/10.5281/zenodo.17402495*
