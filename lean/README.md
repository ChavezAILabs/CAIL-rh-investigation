# Lean 4 Formal Verification Files

Formal verification of zero divisor patterns and the RH sedenionic forcing argument using Harmonic Math's Aristotle proof assistant.

**Canonical Six proofs: v1.3 — February 26, 2026 | Zero sorry stubs in all Canonical Six theorems.**
**RH Forcing Argument: v1.0 — March 30, 2026 | 1 intentional sorry (`commutator_theorem_stmt` — documented open bridge).**

---

## Formal Verification Co-Authorship

All Lean 4 proofs in this repository were co-authored with Aristotle (Harmonic Math).
`Co-authored-by: Aristotle (Harmonic) <aristotle-harmonic@harmonic.fun>`
https://harmonic.fun/

---

## Files

### RH Forcing Argument (New — March 2026)

#### RHForcingArgument.lean
- **Status:** ⚠️ 1 intentional sorry — `commutator_theorem_stmt`. All other theorems fully closed.
- **Lean version:** leanprover/lean4:v4.28.0 / Mathlib 4.28.0
- **Lines:** 883
- **Session:** Claude Desktop + Gemini + Aristotle (Harmonic Math), March 29–30, 2026
- **Contents:**

  **Part 1 — Algebraic foundation (zero sorry stubs):**
  - Complete recursive CDQ type with all algebraic instances
  - All six Canonical Six patterns (P1–P6, Q1–Q6)
  - 36 bilateral zero-divisor proofs across CD4/CD5/CD6 via `native_decide`
  - 18 commutator vanishing theorems derived from bilateral property

  **Part 2 — Sedenion forcing (concrete multiplication):**
  - `Sed = EuclideanSpace ℝ (Fin 16)`
  - Concrete sedenion multiplication via `sedMulSign`/`sedMulTarget` tables
  - Concrete real-analytic definition of F_base (two-prime surrogate):
    ```
    F_base(t) = cos(t·log 2)·e₀ + sin(t·log 2)·e₃ + sin(t·log 3)·e₆
    ```
  - `Ker = span{e₀, u_antisym}` shown closed and nonempty (proved, no sorry)

  **Part 3 — Main theorems (proved, no sorry in proof bodies):**
  - `log2_div_log3_irrational`: log₃(2) ∉ ℚ — proved via mod 2 / unique prime factorization
  - `local_quadratic_exit`: h(0)=0, h′(0)=0, h″(0)=2log²2+2log²3≈3.375>0
  - `analytic_isolation`: h(t)=0 only at t=0 — from irrationality of log₃(2)
  - `Ker_coord_eq_zero`: span{e₀, u_antisym} has zero coords at all indices except 0, 4, 5
  - `F_base_mem_Ker_imp_h_zero`: F_base(t)∈Ker forces both sin terms to vanish
  - `commutator_exact_identity`: MᵀM = 8·(I − P_Ker); all 14 nonzero singular values = 2 (closed March 29 via `native_decide` over ℚ)
  - `F_base_not_in_kernel`: proved via `IsClosed.mem_iff_infDist_zero` + `analytic_isolation`
  - `critical_line_uniqueness`: proved via `smul_eq_zero` + `commutator_exact_identity` + `F_base_not_in_kernel`

  **1 remaining sorry (intentional):**
  - `commutator_theorem_stmt` — refactored to a named hypothesis taking `mirror_symmetry` (the sedenionic lift of ζ(s)=ζ(1−s)) as an explicit parameter. This is the open bridge connecting the concrete sedenionic operator to the Riemann zeta function. `critical_line_uniqueness` depends on this via `sorryAx` only.

  **Axiom budget (verified via `#print axioms`):**
  - All closed theorems: `propext`, `Classical.choice`, `Quot.sound` only
  - `critical_line_uniqueness`: `sorryAx` only via the intentional bridge

- **What is formally proved:** Conditional on the mirror symmetry hypothesis, σ=1/2 is the unique value for which the sedenion commutator [F(t,σ), F(t,1−σ)] vanishes for all t≠0.
- **Use this file if:** Verifying the RH sedenionic forcing argument or extending toward the zeta function lift.

#### SedenionForcing.lean
- **Status:** Preserved scaffold — sorry stubs throughout (`F` defined as `sorry`)
- **Lean version:** leanprover/lean4:v4.24.0
- **Lines:** 151
- **Contents:** Early draft of the forcing argument structure. Defines the same key objects (`u_antisym`, `F`, `F_base`, `F_mirror`, `Ker`) and states the main theorems as sorry stubs. Precursor to RHForcingArgument.lean.
- **Use this file if:** Studying the evolution of the forcing argument formalization, or as a minimal scaffold for alternative proof strategies.

#### lean-toolchain
- Specifies `leanprover/lean4:v4.28.0` for the RH forcing argument project.

---

### Canonical Six — v1.3 Files (February 2026)

#### canonical_six_bilateral_zero_divisors_cd4_cd5_cd6.lean
- **Status:** ✅ Complete — zero sorry stubs
- **Contents:**
  - All 6 Canonical Six patterns proven as bilateral zero divisors in CD4, CD5, CD6 (18 theorems)
  - Vanishing commutators for all 6 patterns across CD4, CD5, CD6 (18 theorems)
- **Proof tactics:** `native_decide` / `decide+kernel`
- **Use this file if:** Verifying core bilateral zero divisor claims

#### e8_weyl_orbit_unification.lean
- **Status:** ✅ Complete — zero sorry stubs
- **Contents:**
  - Theorem_1a: All 5 P-vector images have squared norm 2 (E₈ first shell membership)
  - Theorem_1b: Antipodal pair v₂ + v₃ = 0, connected by simple reflection s_α₄
  - Theorem_1c: All 5 P-vector images form a single Weyl orbit with dominant weight ω₁
- **Use this file if:** Investigating the E₈ connection

#### canonical_six_parents_of_24_phase4.lean
- **Status:** ✅ Complete — zero sorry stubs
- **Contents:**
  - `All_ZDs_Generated`: every member of the 24-element bilateral zero divisor family has both components either in `allCanonicalVectors` or proportional to a product of two canonical vectors
  - `CandidatePairs_Length_Final`: exactly 72 candidate pairs enumerated
  - `CanonicalSix_Satisfies_Conditions`: Canonical Six satisfy conjugate-closed and boundary-free structural conditions
- **Proof tactic:** `native_decide`
- **Use this file if:** Investigating the generation structure of the 24-element family

#### g2_family_24_investigation.lean
- **Status:** Core results complete; G₂ invariance stub open pending Mathlib
- **Contents:**
  - G₂ Lie-theoretic invariance investigation
  - Family structure analysis for the 24-element bilateral zero divisor set
- **Open stub:** G₂ representation theory requires Mathlib library development
- **Use this file if:** Investigating G₂ symmetry or the 24-element family structure

#### master_theorem_scaffold_phase5.lean
- **Status:** Core verified; three open stubs pending Mathlib development
- **Contents:**
  - Master scaffold integrating all verified components from phases 1–4
  - Open stubs: G₂ invariance, E₆×A₂ confinement, Viazovska sphere-packing connection
- **Note:** Open stubs are not refutations. They require library infrastructure not yet available in Mathlib.
- **Use this file if:** Building toward a unified master theorem or extending toward G₂/E₆ theory

---

### RH Investigation — Phase 18B

#### BilateralCollapse.lean
- **Status:** ✅ Complete — zero sorry stubs, builds successfully (`lake build`, exit 0)
- **Verified by:** Aristotle (Harmonic Math) — full build confirmed independently
- **Build time:** ~1487s (due to `exact?` search tactics; all goals closed)
- **Contents:**
  - **`bilateral_collapse`** (main theorem): For any scalars a, b, c ∈ ℚ,
    `(a • P1 4 + b • Q1 4) * (b • P1 4 + c • Q1 4) = scalar 4 ((-2) * b * (a + c))`
    All 15 vector components of the product vanish by algebra; result is pure scalar.
  - **`scalar_channel`**: Existence corollary — the product lies in the scalar channel.
  - **`Pattern1_CD4`**: P1 4 and Q1 4 are bilateral zero divisors.
  - **`p1_sq` / `q1_sq`**: P1 4 * P1 4 = Q1 4 * Q1 4 = −2 (sedenion imaginary unit property).
- **Context:** Phase 18B. Establishes that the bilateral sedenion product collapses to a pure scalar channel — algebraic foundation for the AIEX-001 Hilbert-Pólya conjecture.
- **Use this file if:** Verifying the Bilateral Collapse Theorem or building toward the AIEX-001 operator construction.

---

### Chavez Transform

#### ChavezTransform_Specification_aristotle.lean
- **Status:** ✅ Complete — zero sorry stubs
- **Contents:**
  - Formal definition of the Chavez Transform kernel `K(P,Q,x,α,d)` over 16D sedenion space (`CD4`)
  - Bilateral kernel `K_Z(P,Q,x) = ‖P·x‖² + ‖x·Q‖² + ‖Q·x‖² + ‖x·P‖²`
  - **Theorem 1 (`chavez_transform_convergence`):** Transform of any bounded, integrable function on [−5,5] is finite
  - **Theorem 2 (`chavez_transform_stability`):** Stability bound `|C[f]| ≤ M · ‖f‖₁`
  - Helper theorems: Bilateral Kernel Bound (Thm 5), Distance Decay Bound (Thm 6), Dimensional Weight Bound (Thm 3)
- **Use this file if:** Verifying the mathematical foundations of the Chavez Transform operator

---

### v1.2 Files (Preserved for Reproducibility)

#### dc08bbac-primary.lean
- **Status:** Preserved from v1.2 (superseded by v1.3 files)
- **Foundation:** Rational-based (ℚ) Cayley-Dickson construction | **Lines:** 822
- **Use this file if:** Reproducing v1.2 results or comparing against v1.3 proofs

#### c038a2e4-alternative.lean
- **Status:** Preserved from v1.2 (foundational properties only)
- **Foundation:** Real-based (ℝ) Cayley-Dickson construction | **Lines:** 283
- **Use this file if:** Prefer ℝ-based approach or need alternative methodological baseline

---

## Verification Scope Summary

### Canonical Six (v1.3 — zero sorry stubs)
- ✅ All 6 Canonical Six patterns as bilateral zero divisors in CD4, CD5, CD6
- ✅ Vanishing commutators for all 6 patterns across all 3 dimensions
- ✅ E₈ first shell membership for all 5 P-vector images
- ✅ Single Weyl orbit unification (dominant weight ω₁)
- ✅ Antipodal pair v₂ + v₃ = 0 via simple reflection s_α₄
- ✅ Canonical Six as minimal generating set for the 24-element family
- ✅ Exactly 72 candidate pairs enumerated
- ✅ Framework independence (Clifford vs. Cayley-Dickson)
- ✅ Dimensional persistence through CD6 (256D)

### RH Forcing Argument (v1.0 — 1 intentional sorry)
- ✅ 36 bilateral zero-divisor proofs across CD4/CD5/CD6
- ✅ 18 commutator vanishing theorems
- ✅ `log2_div_log3_irrational` — log₃(2) ∉ ℚ
- ✅ `commutator_exact_identity` — all 14 singular values = 2; ker(L) = span{e₀, u_antisym}
- ✅ `local_quadratic_exit` — h″(0) = 2log²2 + 2log²3 > 0
- ✅ `analytic_isolation` — h(t) = 0 only at t = 0
- ✅ `F_base_not_in_kernel` — F_base(t) ∉ Ker for all t ≠ 0
- ✅ `critical_line_uniqueness` — σ=1/2 unique, conditional on `mirror_symmetry`
- ⚙️ `commutator_theorem_stmt` — intentional sorry; named hypothesis encoding ζ(s)=ζ(1−s) in sedenionic form. Open bridge to the Riemann zeta function.

### Open Stubs (pending Mathlib — not refutations)
- ○ G₂ Lie-theoretic invariance
- ○ E₆×A₂ confinement
- ○ Viazovska sphere-packing connection
- ○ Concrete sedenionic lift of F and F_base from the Riemann zeta function

---

## Technical Details

| | Canonical Six (v1.3) | RH Forcing (v1.0) |
|---|---|---|
| Lean version | leanprover/lean4:v4.24.0 | leanprover/lean4:v4.28.0 |
| Mathlib commit | f897ebcf72cd16f89ab4577d0c826cd14afaafc7 | Mathlib 4.28.0 |
| Arithmetic foundation | ℚ (exact) | ℝ + EuclideanSpace |
| Primary tactics | `native_decide`, `decide+kernel` | `native_decide`, `nlinarith`, `norm_num` |
| Sorry count | 0 | 1 (intentional) |

---

## Paper Reference

**Canonical Six:**
"Framework-Independent Zero Divisor Patterns in Higher-Dimensional Cayley-Dickson Algebras: Discovery and Verification of The Canonical Six" — v1.3, February 26, 2026
DOI: https://doi.org/10.5281/zenodo.17402495
