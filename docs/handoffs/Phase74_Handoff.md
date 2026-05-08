# Phase 74 Handoff — Gateway Integer Law & Spectral Closure
**Project:** CAIL-RH Investigation
**Status:** OPENING
**Date:** May 5, 2026
**Tag:** #phase-74-eigenvalue
**Branch:** TBD (new branch from `phase-73-spectral`)

---

## 1. Opening State (Phase 73 Closed)

```
lake build → 8,055 jobs · 0 errors · 1 sorry (spectral_implies_zeta_zero — boundary condition, by design)
Axiom footprint: [propext, riemann_critical_line, Classical.choice, Quot.sound]
GitHub: commit 4d019e7, branch phase-73-spectral (May 5, 2026)
KSJ: 631 captures through AIEX-629
```

**All Phase 73 items are closed.** `u_antisym_orthogonal_Fbase`, `Fbase_nondegeneracy`, and `SedenionicHamiltonian.lean` canonical sync are complete. Do not re-open these.

---

## 2. Phase 74 Objectives

### Primary — `gateway_integer_iff_critical_line` (Lean)
Prove the formal translation of the empirically confirmed 2σ coordinate scaling law. The correct statement requires a critical strip hypothesis to exclude the spurious `s.re = -1/2` solution (since `2 * s.re ∈ {-1, 1}` admits both `s.re = ½` and `s.re = -½`):

```lean
theorem gateway_integer_iff_critical_line (s : ℂ) (hs : 0 < s.re ∧ s.re < 1) :
    lift_coordinate s g ∈ ({-1, 1} : Set ℝ) ↔ s.re = 1 / 2
```

This flows from two Phase 72 theorems already in the stack:
- `Hamiltonian_vanishing_iff_critical_line`: H(s) = 0 ↔ Re(s) = ½
- `u_antisym_norm_sq`: ‖u_antisym‖² = 2 (the normalization that makes 2σ = 1 at σ = ½)

**Assessment:** Modest effort, but requires the `Gateway` type and `lift_coordinate` to be defined first — these are the actual first tasks of Phase 74.

**Revised Step Sequence (from Claude Code evaluation):**

1. **Define `Gateway` type as `Fin 6`** — chosen over a named inductive (`S1 | S2 | ... | S6`) because `Fin` integrates directly with existing stack infrastructure (`EuclideanSpace ℝ (Fin 16)`, `Fin.sum_univ_succ`, `sedBasis`, `decide` tactic on finite sets). A `notation` or `abbrev` block at the top of `GatewayScaling.lean` can expose S1–S6 names for readability without the coercion overhead of a named inductive.
2. **Define `lift_coordinate (s : ℂ) (g : Gateway) : ℝ`** — the sedenion projection formula. This is the algebraic content: what sedenion-algebraic computation does the 32D lift perform, and why does it return 2 * s.re? The definition must flow from the sedenion structure, not be assumed.
3. **Prove `lift_coord_scaling`** — `lift_coordinate s g = 2 * s.re`. This is the core algebraic lemma.
4. **Prove `gateway_integer_iff_critical_line`** — with strip hypothesis `hs` as above.

**Do NOT redefine `isSpectralPoint`.** The current definition (`sedenion_Hamiltonian s = 0`) is used by three proved theorems: `zeta_zero_implies_spectral`, `spectral_implies_critical_line`, and `eigenvalue_zero_mapping`. Redefining it would break all three and require reproofs. Leave `isSpectralPoint` untouched.

### Secondary — Q-12: Spectral Connection (Lean, Exploratory)
Attempt to connect `gateway_integer_iff_critical_line` to `eigenvalue_zero_mapping` via the functional calculus of H:

```
gateway_integer_iff_critical_line
    ↕  (Q-12 — the bridge to prove)
eigenvalue_zero_mapping
```

The candidate mechanism (from AIEX-592): off-critical-line coordinates are non-integer, creating a measurable commutator obstruction — "algebraic friction" — that prevents bilateral collapse. If this can be formalized, it would constitute a new characterization of why zeros must lie on the critical line.

**Critical architectural note:** The `spectral_implies_zeta_zero` sorry is a mathematical boundary condition, not a proof gap. The missing direction (H(s) = 0 → ζ(s) = 0) is false pointwise — H vanishes on the entire critical line, not only at zeros. No sedenion-algebraic argument closes this without new input that doesn't currently exist. The sorry stands by design. Q-12 is a separate question about the connection between the two theorems, not an attempt to close that sorry.

**Assessment:** Genuinely hard. Non-associativity of sedenions complicates functional calculus arguments. A formal statement of the relationship is a win even without a complete proof. Mark as exploratory — not blocking phase close.

### CAILculator — Run C: Scaling Gradient Sweep (Q-13)
Characterize the sensitivity of the 2σ law in the immediate neighborhood of the critical line:

**Protocol:**
- Tool: CAILculator v2.0.3 · ZDTP v2.0 · Profile: RHI · Precision: 10⁻¹⁵
- Fixed zero: γ₁ = 14.1347
- σ values: {0.49, 0.499, 0.5, 0.501, 0.51}
- Gateways: all six (S1–S6)
- Encoding: full F(s) prime exponential (same as Phase 73 runs)

**Questions to close:**
- How sharply do active coordinates depart from integer values as σ moves off the critical line?
- Is the transition continuous or does it have a threshold character?
- Does the departure rate match 2|σ − ½| exactly (as the 2σ law predicts), or are there higher-order corrections?

**Rationale:** Characterizes the algebraic friction gradient near the critical line. A sharp, linear departure consistent with 2|σ − ½| supports the Q-12 formal argument. Any deviation from linearity would be a new observable worth documenting.

### CAILculator — Extended γ Sweep (Q-8)
Run ZDTP on γ₁₁–γ₂₀ to determine whether the Class A/B magnitude ratio converges to exactly 4.0 asymptotically.

- Profile: RHI
- If ratio converges to 4.0: candidate Lean lemma
- If ratio stabilizes at non-integer: new structural constant to document

---

## 3. Key Files

| File | Role in Phase 74 |
|---|---|
| `GatewayScaling.lean` | **New file** — `Gateway` type, `lift_coordinate`, `lift_coord_scaling`, `gateway_integer_iff_critical_line` |
| `SpectralIdentification.lean` | Reference — `isSpectralPoint`, `eigenvalue_zero_mapping`. Do not modify. |
| `SedenionicHamiltonian.lean` | Source of `Hamiltonian_vanishing_iff_critical_line` and `u_antisym_norm_sq`. Do not modify. |
| `UnityConstraint.lean` | Canonical norm² template (`h_u_antisym_norm_sq` pattern). Reference only. |

---

## 4. Constraints (Standing)

- **Axiom footprint:** `riemann_critical_line` is the only permitted non-standard axiom. No regression.
- **`riemann_critical_line` must never be discharged** — it is the transparent statement of RH itself.
- **NoetherDuality.lean** cannot be modified without explicit confirmation.
- **Files 1–14** (all existing files) are effectively frozen — no edits without explicit discussion. New Lean work goes in `GatewayScaling.lean`.
- **Mathlib v4.28.0 constraint:** Do NOT use `EuclideanSpace.norm_sq_eq_inner` or `EuclideanSpace.inner_def`. Canonical norm² pattern: `h_u_antisym_norm_sq` from `UnityConstraint.lean`.
- **Build log:** Use `Out-File -Encoding utf8` in PowerShell; rely on `#print axioms` for definitive sorry audits.
- **KSJ:** All `extract_insights` output routes to Claude Desktop for explicit approval before `commit_aiex`. Gemini CLI does not call `commit_aiex` directly.

---

## 5. Numerical Baseline (Phase 73 Empirical Record)

| Observable | Value | Source |
|---|---|---|
| 2σ law | active_32d_coord = 2σ (exact) | AIEX-620 (Q-11 closed) |
| Integer locus | σ = ½ unique | AIEX-620 |
| Magnitude growth | μ ≈ 2.5γₙ (linear) | AIEX-621 (Q-9 closed) |
| Std/mean invariant | 0.60 ± 0.01 across γ₁–γ₁₀ | AIEX-622 (Q-10 closed) |
| B/A ratio | ~4× (3.66–4.06, asymptote unresolved) | AIEX-623 (Q-8 developing) |

---

## 6. Success Criteria

**Phase 74 closes when:**
1. `gateway_integer_iff_critical_line` proved and verified in lake build (0 new sorries, axiom footprint unchanged)
2. Run C (Scaling Gradient sweep) complete and documented
3. Q-8 extended γ sweep complete
4. GitHub pushed on new phase branch
5. KSJ captures committed with explicit approval

**Bonus (not blocking close):** Any formal progress on Q-12 spectral connection.

---

*Chavez AI Labs LLC — Applied Pathological Mathematics — Better math, less suffering*
*Phase 74 · May 5, 2026 · github.com/ChavezAILabs/CAIL-rh-investigation*
*KSJ: 631 captures through AIEX-629*
