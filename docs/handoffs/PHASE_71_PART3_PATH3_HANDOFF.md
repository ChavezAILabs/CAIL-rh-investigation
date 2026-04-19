# Phase 71 Part 3 — Path 3 Handoff
**Chavez AI Labs | CAIL-RH Investigation | April 17, 2026**
**Produced by:** Claude Code (claude-sonnet-4-6) at session end
**Status:** Mathlib audit COMPLETE. Proof strategy AGREED. Lean code NOT yet written.

---

## 0. What This Document Is

Paul and Claude Code completed the full Path 3 Mathlib infrastructure audit during
the April 17, 2026 session. The session ended before any Lean code was written.
This document captures every audit finding, the agreed proof plan, and the one
outstanding item to resolve at the start of the next session. The next Claude Code
session can pick this up directly and begin writing Lean without re-running any audits.

---

## 1. Target Theorem (Revised)

The original handoff (`PHASE_71_PART3_CLAUDE_CODE_HANDOFF.md`, Section 3) targeted:
```lean
theorem xi_real_on_critical_line (t : ℝ) :
    (riemannXi (1/2 + t * Complex.I)).im = 0
```

**`riemannXi` is ABSENT from Mathlib v4.28.0.** Paul and Claude agreed to reframe
Path 3 to target Mathlib's `completedRiemannZeta` (= Λ(s)) instead. The revised target:

```lean
-- Section: "completedRiemannZeta real on critical line (Phase 71 Part 3, Path 3)"
-- File: EulerProductBridge.lean
-- Expected footprint: [propext, Classical.choice, Quot.sound]

theorem completedRiemannZeta_real_on_critical_line (t : ℝ) :
    (completedRiemannZeta ((1 : ℂ)/2 + ↑t * Complex.I)).im = 0
```

This is mathematically equivalent: Λ(s) = π^{−s/2}·Γ(s/2)·ζ(s) and
ξ(s) = (1/2)·s·(s−1)·Λ(s). Both are real on the critical line; proving it for Λ
avoids introducing a local definition.

---

## 2. Complete Mathlib Audit Results

All greps run against:
`AsymptoticRigidity_aristotle/.lake/packages/mathlib/Mathlib/`

### 2A. riemannXi / completedRiemannZeta

| Name | Status | Location |
|---|---|---|
| `riemannXi` | **ABSENT** | — |
| `completedRiemannZeta` | **FOUND** | `NumberTheory/LSeries/RiemannZeta.lean:67` |
| `completedRiemannZeta₀` | FOUND | `NumberTheory/LSeries/RiemannZeta.lean:63` |

```lean
-- Definition:
def completedRiemannZeta (s : ℂ) : ℂ := completedHurwitzZetaEven 0 s
-- (= π^(-s/2) · Γ(s/2) · ζ(s), i.e., Λ(s) in classical notation)
```

### 2B. Completed Functional Equation

```lean
-- FOUND — unconditional (no hypotheses)
theorem completedRiemannZeta_one_sub (s : ℂ) :
    completedRiemannZeta (1 - s) = completedRiemannZeta s
-- Location: NumberTheory/LSeries/RiemannZeta.lean:105
```

```lean
-- Also FOUND — entire function version
theorem completedRiemannZeta₀_one_sub (s : ℂ) :
    completedRiemannZeta₀ (1 - s) = completedRiemannZeta₀ s
-- Location: NumberTheory/LSeries/RiemannZeta.lean:99
```

**`completedRiemannZeta_conj` — ABSENT.** No conjugation lemma for Λ in Mathlib.

### 2C. Gamma_conj

```lean
-- FOUND — unconditional
theorem Gamma_conj (s : ℂ) : Gamma (conj s) = conj (Gamma s)
-- Location: Analysis/SpecialFunctions/Gamma/Basic.lean:357
-- No hypotheses. Works for all s : ℂ.
```

### 2D. cpow_conj

```lean
-- FOUND — requires x.arg ≠ π
theorem cpow_conj (x : ℂ) (n : ℂ) (hx : x.arg ≠ π) : x ^ conj n = conj (conj x ^ n)
-- Location: Analysis/SpecialFunctions/Pow/Complex.lean:234
```

**For π:** `(↑π : ℂ).arg = 0` by `Complex.arg_ofReal_of_nonneg (le_of_lt Real.pi_pos)`.
So `(↑π : ℂ).arg ≠ Real.pi` since `Real.pi > 0`.
And `conj (↑π : ℂ) = (↑π : ℂ)` since π is a real cast.
Therefore for `x = (↑π : ℂ)`: `(↑π : ℂ) ^ (conj n) = conj ((↑π : ℂ) ^ n)`.

### 2E. conj_tsum

```lean
-- FOUND — unconditional
theorem conj_tsum (f : α → ℂ) : conj (∑'[L] a, f a) = ∑'[L] a, conj (f a)
-- Location: Analysis/Complex/Basic.lean:568
```

### 2F. Gammaℝ Infrastructure

```lean
-- Definition (Analysis/SpecialFunctions/Gamma/Deligne.lean:43)
noncomputable def Gammaℝ (s : ℂ) := π ^ (-s / 2) * Gamma (s / 2)

-- Key lemma FOUND: Gammaℝ ≠ 0 when Re(s) > 0
lemma Gammaℝ_ne_zero_of_re_pos {s : ℂ} (hs : 0 < re s) : Gammaℝ s ≠ 0
-- Location: Analysis/SpecialFunctions/Gamma/Deligne.lean:66

-- Zero characterization FOUND
lemma Gammaℝ_eq_zero_iff {s : ℂ} : Gammaℝ s = 0 ↔ ∃ n : ℕ, s = -(2 * n)
-- Zeros at s = 0, -2, -4, -6, ... (the "trivial zero" positions)
-- This means: for s = 1/2 + t·I (Re(s)=1/2 > 0), Gammaℝ s ≠ 0 always.

-- Bridge to riemannZeta FOUND
lemma riemannZeta_def_of_ne_zero {s : ℂ} (hs : s ≠ 0) :
    riemannZeta s = completedRiemannZeta s / Gammaℝ s
-- Location: NumberTheory/LSeries/RiemannZeta.lean:144
```

### 2G. arg_ofReal

```lean
-- FOUND
theorem arg_ofReal_of_nonneg {x : ℝ} (hx : 0 ≤ x) : arg x = 0
-- Location: Analysis/SpecialFunctions/Complex/Arg.lean:216
```

### 2H. Summary Table

| Ingredient | Status | Notes |
|---|---|---|
| `riemannXi` | ABSENT | Use `completedRiemannZeta` instead |
| `completedRiemannZeta_one_sub` | FOUND | Unconditional |
| `completedRiemannZeta_conj` | ABSENT | Must prove (plan below) |
| `Gamma_conj` | FOUND | Unconditional |
| `cpow_conj` | FOUND | Requires `x.arg ≠ π`; OK for `x = ↑π` |
| `conj_tsum` | FOUND | Unconditional |
| `Gammaℝ` def | FOUND | `π^(-s/2) * Gamma(s/2)` |
| `Gammaℝ_ne_zero_of_re_pos` | FOUND | Sufficient for critical line |
| `riemannZeta_def_of_ne_zero` | FOUND | Bridge Λ ↔ ζ |
| `arg_ofReal_of_nonneg` | FOUND | For π condition |
| `riemannZeta_conj` | IN STACK | Phase 71 Part 2, `EulerProductBridge.lean` |

---

## 3. Proof Plan (Three Lemmas)

All three lemmas go in `EulerProductBridge.lean` under a new section:
```lean
/-! ================================================================
    Path 3: completedRiemannZeta Real on Critical Line (Phase 71 Part 3)
    ================================================================ -/
```

### Lemma 1: Gammaℝ_conj

```lean
private lemma Gammaℝ_conj (s : ℂ) :
    Gammaℝ (starRingEnd ℂ s) = starRingEnd ℂ (Gammaℝ s) := by
  simp only [Gammaℝ_def]
  rw [map_mul]
  congr 1
  · -- Goal: (↑π) ^ (-(starRingEnd ℂ s) / 2) = starRingEnd ℂ ((↑π) ^ (-s / 2))
    -- starRingEnd ℂ (-s/2) = -(starRingEnd ℂ s)/2
    have h_neg_div : starRingEnd ℂ (-s / 2) = -(starRingEnd ℂ s) / 2 := by
      simp [map_neg, map_div₀]
    rw [← h_neg_div]
    -- cpow_conj: (↑π) ^ conj n = conj (conj (↑π) ^ n)
    -- Since conj (↑π) = ↑π, this gives (↑π) ^ conj n = conj ((↑π) ^ n)
    have h_arg : (↑π : ℂ).arg ≠ Real.pi := by
      rw [Complex.arg_ofReal_of_nonneg (le_of_lt Real.pi_pos)]
      exact (ne_of_gt Real.pi_pos).symm
    have h_conj_pi : starRingEnd ℂ (↑π : ℂ) = (↑π : ℂ) := by
      simp [starRingEnd_apply, Complex.conj_ofReal]
    rw [starRingEnd_apply, Complex.cpow_conj _ _ h_arg, h_conj_pi,
        ← starRingEnd_apply]
  · -- Goal: Gamma ((starRingEnd ℂ s) / 2) = starRingEnd ℂ (Gamma (s / 2))
    have h_div : starRingEnd ℂ (s / 2) = (starRingEnd ℂ s) / 2 := by
      simp [map_div₀]
    rw [← h_div, starRingEnd_apply, Complex.Gamma_conj, ← starRingEnd_apply]
```

**Note:** The exact simp lemmas for `starRingEnd` on div and neg may need adjustment
during compilation. Key facts: `map_neg`, `map_div₀`, `map_ofNat` (for the `2`).

### Lemma 2: completedRiemannZeta_conj

```lean
theorem completedRiemannZeta_conj {s : ℂ} (hs_re : 0 < s.re) (hs1 : s ≠ 1) :
    completedRiemannZeta (starRingEnd ℂ s) = starRingEnd ℂ (completedRiemannZeta s) := by
  have hs0 : s ≠ 0 := by intro h; simp [h] at hs_re
  have hs0' : starRingEnd ℂ s ≠ 0 := by
    intro h
    apply hs0
    have := congr_arg (starRingEnd ℂ) h
    simp at this; exact this
  have hs1' : starRingEnd ℂ s ≠ 1 := by
    intro h; apply hs1
    have := congr_arg (starRingEnd ℂ) h
    simp at this; exact this
  have hs_conj_re : 0 < (starRingEnd ℂ s).re := by
    simp [starRingEnd_apply, Complex.conj_re]; exact hs_re
  -- Gammaℝ nonvanishing
  have hG : Gammaℝ s ≠ 0 := Gammaℝ_ne_zero_of_re_pos hs_re
  have hG' : Gammaℝ (starRingEnd ℂ s) ≠ 0 := Gammaℝ_ne_zero_of_re_pos hs_conj_re
  -- Λ(s) = ζ(s) * Γℝ(s)
  have hΛ : completedRiemannZeta s = riemannZeta s * Gammaℝ s :=
    (div_eq_iff hG).mp (riemannZeta_def_of_ne_zero hs0).symm
  have hΛ' : completedRiemannZeta (starRingEnd ℂ s) =
             riemannZeta (starRingEnd ℂ s) * Gammaℝ (starRingEnd ℂ s) :=
    (div_eq_iff hG').mp (riemannZeta_def_of_ne_zero hs0').symm
  -- Apply conjugation to each factor
  rw [hΛ', riemannZeta_conj s hs1, Gammaℝ_conj s, ← map_mul, ← hΛ]
```

### Lemma 3: completedRiemannZeta_real_on_critical_line

```lean
theorem completedRiemannZeta_real_on_critical_line (t : ℝ) :
    (completedRiemannZeta ((1 : ℂ)/2 + ↑t * Complex.I)).im = 0 := by
  set s := (1 : ℂ)/2 + ↑t * Complex.I with hs_def
  -- s ≠ 1 (re s = 1/2 ≠ 1)
  have hs1 : s ≠ 1 := by
    intro h
    have := congr_arg Complex.re h
    simp [hs_def] at this
  -- Re(s) = 1/2 > 0
  have hs_re : (0 : ℝ) < s.re := by simp [hs_def]
  -- conj(s) = 1 - s (arithmetic on critical line)
  have h_conj : starRingEnd ℂ s = 1 - s := by
    apply Complex.ext
    · simp [hs_def, starRingEnd_apply, Complex.conj_re, Complex.add_re,
            Complex.mul_re, Complex.ofReal_re, Complex.I_re, Complex.I_im]
      ring
    · simp [hs_def, starRingEnd_apply, Complex.conj_im, Complex.add_im,
            Complex.mul_im, Complex.ofReal_im, Complex.I_re, Complex.I_im]
      ring
  -- Λ(conj s) = conj(Λ(s))
  have h_conj_zeta : completedRiemannZeta (starRingEnd ℂ s) =
                     starRingEnd ℂ (completedRiemannZeta s) :=
    completedRiemannZeta_conj hs_re hs1
  -- Λ(conj s) = Λ(1-s) = Λ(s)
  have h_sym : completedRiemannZeta (starRingEnd ℂ s) = completedRiemannZeta s := by
    rw [h_conj, completedRiemannZeta_one_sub]
  -- Therefore Λ(s) = conj(Λ(s)), so Im = 0
  have h_real : completedRiemannZeta s = starRingEnd ℂ (completedRiemannZeta s) := by
    rw [← h_conj_zeta, h_sym]
  -- z = conj(z) ↔ z.im = 0
  have : (completedRiemannZeta s).im = -(completedRiemannZeta s).im := by
    conv_lhs => rw [h_real]
    simp [starRingEnd_apply, Complex.conj_im]
  linarith
```

---

## 4. Open Issue Before Writing Lean

**One outstanding item:** Confirm that `Gammaℝ`, `Gammaℝ_ne_zero_of_re_pos`, and
`riemannZeta_def_of_ne_zero` are in scope from `EulerProductBridge.lean`.

These are in:
- `Gammaℝ` def: `Mathlib.Analysis.SpecialFunctions.Gamma.Deligne`
- `riemannZeta_def_of_ne_zero`: `Mathlib.NumberTheory.LSeries.RiemannZeta`

The current file imports `ZetaIdentification`, which imports through:
`PrimeEmbedding → SymmetryBridge → ... → (various Mathlib imports)`

The import chain was being traced when the session ended. The tool call to check
`NumberTheory.LSeries.HurwitzZeta`'s imports was rejected due to session limits.

**Resolution at session start:**
```bash
# Run in EulerProductBridge.lean after opening -- if Gammaℝ not found, add:
import Mathlib.Analysis.SpecialFunctions.Gamma.Deligne
# or check if it arrives via the existing chain with:
grep -rn "Deligne\|Gammaℝ" .lake/packages/mathlib/Mathlib/NumberTheory/LSeries/HurwitzZeta.lean
```

If `Gammaℝ` is NOT transitively imported, add `open Complex` and import `Deligne`
explicitly at the top of `EulerProductBridge.lean`. This is a two-line fix.

---

## 5. Implementation Checklist

When resuming, execute in this order:

- [ ] **Step 0:** Resolve import scope (5 min) — run the grep above or attempt to
  reference `Gammaℝ` in a scratch `#check` block in the file
- [ ] **Step 1:** Write `Gammaℝ_conj` (private lemma) — compile, fix any simp issues
- [ ] **Step 2:** Write `completedRiemannZeta_conj` — compile
- [ ] **Step 3:** Write `completedRiemannZeta_real_on_critical_line` — compile
- [ ] **Step 4:** `lake build` → report jobs / errors / sorries
- [ ] **Step 5:** Add to `axiom_check.lean`:
  ```lean
  #print axioms completedRiemannZeta_real_on_critical_line
  ```
  Run `lake env lean axiom_check.lean`. Expected: `[propext, Classical.choice, Quot.sound]`
- [ ] **Step 6:** Verify `#print axioms riemann_hypothesis` unchanged:
  `[propext, riemann_critical_line, Classical.choice, Quot.sound]`
- [ ] **Step 7:** KSJ extract_insights → Paul approves → commit_aiex
- [ ] Proceed to Path 4 audit

---

## 6. Prime Directives (from PHASE_71_PART3_CLAUDE_CODE_HANDOFF.md — unchanged)

1. **Frozen files:** Only `EulerProductBridge.lean` is editable (files 1–11, ChavezTransform frozen)
2. **Do not discharge `riemann_critical_line`** with sorry or any tactic
3. **Do not re-axiomatize** `bilateral_collapse_continuation`, `euler_sedenion_bridge`, or `prime_exponential_identification`
4. **`set_option maxHeartbeats 800000`** on all arithmetic-heavy lemmas
5. **Do not push to GitHub** — Paul pushes manually after phase concludes

---

## 7. Expected Build State After Path 3

```
lake build → ~8,051 jobs · 0 errors · 0 sorries

#print axioms completedRiemannZeta_real_on_critical_line
→ [propext, Classical.choice, Quot.sound]

#print axioms riemann_hypothesis
→ [propext, riemann_critical_line, Classical.choice, Quot.sound]  ← UNCHANGED
```

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 71 Part 3 · Path 3 Handoff · April 17, 2026 · @aztecsungod*
