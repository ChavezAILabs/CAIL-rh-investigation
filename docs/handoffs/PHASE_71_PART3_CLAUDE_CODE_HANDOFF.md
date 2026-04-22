# Phase 71 Part 3 — Claude Code Handoff
**Chavez AI Labs | CAIL-RH Investigation | April 17, 2026**
**Author:** Claude Desktop (strategy) → Claude Code (execution)

---

## 0. Prime Directives (non-negotiable)

Before touching anything, internalize these from `CLAUDE.md`:

1. **Frozen files — DO NOT MODIFY:** Files 1–11 in the import chain, and `ChavezTransform_genuine.lean` (file 14). The only editable file is `EulerProductBridge.lean` (file 12). Create a new file only if explicitly decided below, and discuss with Paul first.
2. **Do not discharge `riemann_critical_line`** with `sorry`, `native_decide`, or any tactic. It is RH itself.
3. **Do not re-axiomatize** `bilateral_collapse_continuation`, `euler_sedenion_bridge`, or `prime_exponential_identification`. All three are theorems.
4. **Do not attempt** `mirror_op_is_automorphism` — it is FALSE.
5. **Every arithmetic-heavy lemma** gets `set_option maxHeartbeats 800000`.
6. **Report `#print axioms riemann_hypothesis` verbatim** after every successful build.
7. **Expected footprint throughout:** `[propext, riemann_critical_line, Classical.choice, Quot.sound]` for `riemann_hypothesis`. New theorems in Paths 3/4/5 should have footprint `[propext, Classical.choice, Quot.sound]` (no `riemann_critical_line`).
8. **Build sequence:** Edit canonical at `CAIL-rh-investigation/lean/EulerProductBridge.lean`, copy to `AsymptoticRigidity_aristotle/`, then `lake build`. Paul runs `lake build` in PowerShell — you can `cat` files and edit but do not invoke `lake` from bash (per CLAUDE.md build protocol).

---

## 1. Starting State

**Build baseline (April 16, 2026):** 8,037 jobs · 0 errors · 0 sorries
**Axiom footprint:** `[propext, riemann_critical_line, Classical.choice, Quot.sound]`

**Already proved in the stack (available for use in Path 3):**
- `riemannZeta_conj : ∀ s ≠ 1, riemannZeta (conj s) = conj (riemannZeta s)` — Phase 71 Part 2, in `EulerProductBridge.lean` or adjacent. Footprint `[propext, Classical.choice, Quot.sound]`.
- `riemannZeta_quadruple_zero` — V₄ orbit {s, s̄, 1−s, 1−s̄}.
- `quadruple_critical_line_characterization` — s₀ = 1−s̄₀ ↔ Re(s₀)=1/2.
- `riemannZeta_ne_zero_of_re_eq_zero` — Phase 71 Part 1.
- `riemannZeta_zero_symmetry` — Phase 70.

**Known Mathlib infrastructure (from CLAUDE.md Phase 71 audit):**
- `Gamma_conj`, `cos_conj`, `exp_conj` — unconditional
- `cpow_conj`, `log_conj` — require `x.arg ≠ π`
- `conj_tsum` — available
- `riemannZeta_one_sub` — functional equation
- `riemannZeta_eulerProduct_tprod`, `riemannZeta_eulerProduct_exp_log` — require `1 < s.re`
- `Complex.Gamma` — present
- `hadamard_three_lines` — in `Analysis.Complex.Hadamard`

---

## 2. Execution Order

Execute **Path 3 first** to completion (or to a clean handoff point), then Path 4, then Path 5. Do not parallelize. Report after each path.

---

## 3. PATH 3 — Pólya-Xi ξ(s) real on critical line (HIGH)

### 3.1 Target

```lean
theorem xi_real_on_critical_line (t : ℝ) :
    (riemannXi (1/2 + t * Complex.I)).im = 0
```

### 3.2 Mathlib audit — execute FIRST, report BEFORE writing any Lean proof

Run these greps inside the Mathlib source tree (adjust path — typically `~/.lake/packages/mathlib/Mathlib/` or the project's `.lake/packages/mathlib/Mathlib/`):

```bash
# A. Does ξ / completedRiemannZeta exist by any name?
grep -rn "riemannXi\|completedRiemannZeta\|riemann_xi\|RiemannXi" <mathlib-path>/NumberTheory/
grep -rn "def.*Xi\|def.*completed" <mathlib-path>/NumberTheory/LSeries/

# B. Functional equation of the completed zeta?
grep -rn "completedRiemannZeta_one_sub\|riemannXi.*one_sub\|xi.*functional" <mathlib-path>/NumberTheory/

# C. Real-coefficient / real-on-real properties?
grep -rn "Gamma_ofReal\|Gamma_conj" <mathlib-path>/Analysis/SpecialFunctions/Gamma/

# D. cpow conjugation — confirm signature
grep -rn "cpow_conj\|Complex.cpow_conj" <mathlib-path>/
```

**Report format:**
```
PATH 3 AUDIT RESULT:
- riemannXi / completedRiemannZeta: [found as <name> in <file:line> | absent]
- completed functional equation: [found | absent]
- Gamma_conj signature: <paste the exact declaration>
- cpow_conj signature: <paste the exact declaration>
- conj_tsum signature: <paste the exact declaration>
```

**Stop here and report.** Do not proceed to 3.3 until Paul confirms.

### 3.3 Proof strategy (write AFTER audit)

The proof runs via the chain:
```
conj(ξ(s)) = ξ(conj s)       [Step A — conjugation compatibility]
           = ξ(1 − s)         [Step B — at s = 1/2+it, conj s = 1−s]
           = ξ(s)             [Step C — functional equation ξ(s) = ξ(1−s)]
∴ ξ(s) = conj(ξ(s)) ⟹ Im(ξ(s)) = 0
```

**Step A decomposition.** If ξ is defined as `(1/2)·s·(s−1)·π^(−s/2)·Γ(s/2)·ζ(s)`:
- `conj(1/2) = 1/2` — real
- `conj(s · (s−1)) = conj(s) · (conj(s) − 1)` — `map_mul`, `map_sub`
- `conj(π^(−s/2)) = π^(−conj(s)/2)` — needs `cpow_conj` with `(π : ℂ).arg = 0 ≠ π`. Use `Real.pi_pos` → `Complex.arg_ofReal_of_pos` → arg = 0.
- `conj(Γ(s/2)) = Γ(conj(s)/2)` — `Gamma_conj`
- `conj(ζ(s)) = ζ(conj(s))` — `riemannZeta_conj` (already in stack; requires `s ≠ 1`)

**Side condition for Step A:** `s ≠ 1`. At `s = 1/2 + t·I`, `s = 1 ↔ t = 0 ∧ 1/2 = 1`, false. So `s ≠ 1` is trivial at the target.

**Step B.** `conj(1/2 + t·I) = 1/2 − t·I = 1 − (1/2 + t·I)`. Pure arithmetic:
```lean
example (t : ℝ) : starRingEnd ℂ (1/2 + t * Complex.I) = 1 - (1/2 + t * Complex.I) := by
  simp [Complex.ext_iff, Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im,
        Complex.I_re, Complex.I_im, Complex.ofReal_re, Complex.ofReal_im,
        starRingEnd_apply, Complex.conj_re, Complex.conj_im]
  ring
```

**Step C — functional equation.** Two sub-cases:
- **If Mathlib provides** `completedRiemannZeta_one_sub` or `riemannXi_one_sub`: use it directly. ξ is a trivial multiple of Λ (if ξ = (1/2)·s·(s−1)·Λ(s) and Mathlib's `completedRiemannZeta` is defined as `π^(-s/2)·Γ(s/2)·ζ(s)`), so symmetrizing the prefactor `s·(s−1) = (1−s)·(1−(1−s)) = (1−s)·s` follows by `ring`.
- **If Mathlib does not provide it:** Prove ξ(s) = ξ(1−s) from `riemannZeta_one_sub` directly. The explicit form:
  ```
  ξ(s)   = (1/2)·s·(s−1)·π^(−s/2)·Γ(s/2)·ζ(s)
  ξ(1−s) = (1/2)·(1−s)·(−s)·π^(−(1−s)/2)·Γ((1−s)/2)·ζ(1−s)
        = (1/2)·s·(s−1)·π^(−(1−s)/2)·Γ((1−s)/2)·ζ(1−s)        [ring on the algebraic prefactor]
  ```
  Then use `riemannZeta_one_sub`:
  `ζ(1−s) = 2·(2π)^(−s)·Γ(s)·cos(πs/2)·ζ(s)`
  and the Legendre duplication + reflection to show equality of the remaining factors. This is non-trivial — if this branch is needed, STOP and discuss with Paul before proceeding.

### 3.4 File placement

- If ξ is in Mathlib: add `xi_real_on_critical_line` and supporting lemmas to `EulerProductBridge.lean` under a new section `-- Pólya-Xi on critical line (Phase 71 Part 3, Path 3)`. No new file.
- If ξ must be defined locally: still place it in `EulerProductBridge.lean`. Do NOT create a new file without Paul's approval.

### 3.5 Checkpoints

After writing the proof:
1. `lake build` → report jobs / errors / sorries.
2. Add to `axiom_check.lean`:
   ```lean
   #print axioms xi_real_on_critical_line
   ```
3. Run `lake env lean axiom_check.lean`. Expected: `[propext, Classical.choice, Quot.sound]`.
4. Report `#print axioms riemann_hypothesis` — must be unchanged.

---

## 4. PATH 4 — de Bruijn-Newman structural mapping (MEDIUM)

### 4.1 Mathlib audit

```bash
grep -rn "deBruijn\|Newman\|deBruijnNewman\|de_bruijn" <mathlib-path>/
grep -rn "heat.*kernel\|gaussian_convolution" <mathlib-path>/Analysis/
grep -rn "hadamardThreeLines\|hadamard_three_lines" <mathlib-path>/Analysis/Complex/
```

**Report format:**
```
PATH 4 AUDIT RESULT:
- deBruijn-Newman in Mathlib: [present/absent]
- Heat kernel / Gaussian convolution: [list findings]
- hadamardThreeLines exact name and signature: <paste>
```

### 4.2 Formal statements (candidate)

Do NOT try to prove Λ = 0. Target is a named theorem expressing the structural parallel. These two are re-namings of already-proved results, safe to add:

```lean
/-- The sedenion energy lower bound is the structural analogue of Λ ≥ 0
    (Rodgers–Tao 2019). Energy ≥ 1 corresponds to Λ ≥ 0. -/
theorem sedenion_energy_floor_is_deBruijn_lower_bound_analogue :
    ∀ (t : ℝ) (σ : ℝ), energy t σ ≥ 1 :=
  unity_constraint_absolute

/-- The energy minimum at σ = 1/2 corresponds to Λ = 0 ↔ RH.
    This gives the structural isomorphism of the two framings. -/
theorem sedenion_energy_minimum_iff_critical_line :
    ∀ σ : ℝ, (∀ t : ℝ, energy t σ = 1) ↔ σ = 1/2 := by
  intro σ
  constructor
  · intro h
    have h0 := h 0
    -- energy t σ = 1 + (σ − 1/2)², so (σ − 1/2)² = 0 ↔ σ = 1/2
    sorry -- replace with proof from energy_expansion + pow_eq_zero_iff
  · intro hσ t
    simp [energy, hσ]  -- exact form depends on energy definition
    ring
```

Check the actual definition of `energy` in `UnityConstraint.lean` (file 4, frozen — read only). Use `energy_expansion` if it exists. The sorry above is a placeholder — write the real proof once you have the definition in view.

**Placement:** `EulerProductBridge.lean`, new section `-- de Bruijn-Newman structural map (Phase 71 Part 3, Path 4)`.

### 4.3 Checkpoint

1. `lake build` → report.
2. `#print axioms sedenion_energy_floor_is_deBruijn_lower_bound_analogue` — expect `[propext, Classical.choice, Quot.sound]`.
3. Report `#print axioms riemann_hypothesis` — must be unchanged.

---

## 5. PATH 5 — Argument Principle audit (LOW, AUDIT ONLY)

### 5.1 Run audit — no Lean code

```bash
grep -rn "windingNumber\|winding_number" <mathlib-path>/
grep -rn "argumentPrinciple\|argument_principle" <mathlib-path>/
grep -rn "meromorphicOn\|MeromorphicOn" <mathlib-path>/
grep -rn "Function.divisor\|Divisor.*Complex" <mathlib-path>/
grep -rn "Jensen.*formula\|jensen" <mathlib-path>/Analysis/Complex/
ls <mathlib-path>/Analysis/Complex/CauchyIntegral*
ls <mathlib-path>/Analysis/Complex/RemovableSingularity*
```

### 5.2 Report format

```
PATH 5 AUDIT RESULT (Mathlib v4.28.0):
- windingNumber: [present at <file:line> | absent]
- argumentPrinciple: [present | absent]
- MeromorphicOn infrastructure: [summary of findings]
- Divisor/order-of-zero infrastructure: [summary]
- Jensen's formula: [present | absent]
- N(T) formal definition: [absent (expected) | found at ...]
- Partial building blocks that could support N(T): [list]
- Recommended action: [pursue / defer to future phase / blocked]
```

### 5.3 No Lean writes

Do not add any theorem, definition, or file for Path 5. Pure audit.

---

## 6. KSJ protocol

After each path's build verification:
1. Run `extract_insights` on the path's results (build stats, axiom footprints, key lemmas, audit findings).
2. Present the full extraction to Paul for approval.
3. Only after Paul's explicit approval: `commit_aiex`.
4. Never auto-commit.

---

## 7. Final handoff

After all three paths conclude (or reach a clean stopping point):
1. Full `lake build` on `AsymptoticRigidity_aristotle/` → report.
2. Full `axiom_check.lean` output → paste verbatim.
3. `git status` — list modified files.
4. Do NOT push to GitHub. Paul pushes manually.
5. Do NOT submit to Aristotle until Paul confirms local build is clean across all three paths.

---

## 8. If you get stuck

- Path 3 Step C falls into the non-trivial branch (Mathlib has no `completedRiemannZeta_one_sub`): STOP, report, wait for Paul.
- Any build breaks a frozen file: STOP, report which file, do not attempt repair.
- `#print axioms riemann_hypothesis` gains an axiom: STOP immediately. Something is wrong.
- Any tactic or `sorry` ends up dispatched against `riemann_critical_line`: STOP. Revert.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 71 Part 3 · Claude Code Handoff · April 17, 2026 · @aztecsungod*
