# CAIL-rh-investigation

**Chavez AI Labs — Riemann Hypothesis Empirical Investigation**

An open science research project applying the **Chavez Transform** and **sedenion zero divisor analysis** to empirically probe the structure of the Riemann Hypothesis. Phases 1–17, 18A–18F, Phase 19 Threads 1–3, Phases 20B–20D, Phase 21A–21C, Phases 22–24, and Phases 25–29 (AIEX-001a) complete. Built on Lean 4-verified algebraic foundations (Canonical Six, Chavez Transform convergence).

---

## Overview

This repository contains all data, analysis scripts, results, and formal proofs from an ongoing empirical investigation into the arithmetic and spectral structure of the Riemann zeta function's nontrivial zeros.

The investigation is grounded in two novel tools:

- **Chavez Transform** — Uses zero divisor structure from Cayley-Dickson algebras (sedenions, 16D+) to analyze numerical sequences across hypercomplex dimensions. Formally verified in Lean 4 (convergence and stability theorems).
- **ZDTP (Zero Divisor Transmission Protocol)** — Lossless dimensional transmission (16D→32D→64D) with six canonical gateway analyses.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space, formally established in the companion paper (v1.3, Feb 26, 2026).

### Key Results

**Route B Confirmed (Phase 16):** The log-prime spectral signal in Riemann zero gaps is **arithmetic** in origin — it tracks the Euler product of the specific L-function, not a universal GUE property. Decisive evidence:

- p=2 suppressed 353× in χ₄ zeros (χ₄(2)=0, ramified prime)
- p=3 suppressed 736× in χ₃ zeros (χ₃(3)=0, ramified prime)
- All other primes present in both — exactly matching Euler product structure

This eliminates Route C (GUE universality) and strongly supports AIEX-001: a Hilbert-Pólya operator in sedenion space.

**Q-Vector Access (Phase 17):** First probe of the Q-vector component of the Canonical Six bilateral zero divisors. Results:

- **p=2 detected for the first time** — SNR=418× via the q2 projection (all P-vector projections missed p=2 due to high-pass filter symmetry)
- **9/9 primes p=2..23 detected in a single projection** — q2 is the first broadband channel covering the full prime spectrum
- Q-vectors outperform P-vectors by **5–7× in SNR** (peak 1995× vs 245×)
- Route B re-confirmed with **10–14× stronger suppression** than Phase 16 (p=2 in χ₄: ~10,000×)
- **Layer structure discovered**: actual zeros match GUE in three-gap correlations (Act/GUE = 1.02) but are tighter in two-gap correlations (0.65) — the bilateral product structure reveals this distinction *(Phase 18B refinement: 1.02 is a global-average artifact; see Phase 18B)*

**E8 Root Geometry (Phase 18E):** Complete structural analysis of the 8-root bilateral zero divisor set {v1, q3, v2, v3, v4, v5, q2, q4}:

- All 8 roots lie on the E8 first shell (norm² = 2); Gram matrix entries ∈ {−2, 0, +2}
- The complete set spans a **6D subspace** of 8D E8 space (P-vectors alone span 4D; q2, q4 add 2 new independent dimensions)
- Root system classification: **(A₁)⁶** — 6 mutually orthogonal A₁ factors, each a ±root pair
- P⊥Q orthogonality has three types: degenerate (P=Q, Pattern 1), genuinely orthogonal (Patterns 2–5), antipodal (P=−Q, Pattern 6)
- Only Pattern 6 corresponds to a genuine W(E8) Weyl reflection; Patterns 2–5 require ≥2 Weyl steps

**chi3/Q2 Anomaly Resolved (Phase 18A):** Conductor survey across χ₃, χ₄, χ₅, χ₇, χ₈ (conductors 3, 4, 5, 7, 8):

- The χ₃/ζ Q2 SNR ratio ≈ 1.0 (Phase 17) is **conductor-specific to conductor 3** — χ₄, χ₅, χ₇, χ₈ all return to the expected ~0.1–0.3 range
- Route B ramified prime suppression confirmed for all 5 L-functions (ratio ≈ 0.000 at each ramified prime)
- The q2 = e5+e10 sedenion direction has a structural alignment with conductor-3 L-functions not shared by other conductors tested

**Bilateral Collapse Theorem (Phase 18B) — Lean 4 Proven:** For Pattern 1 bilateral zero divisor pair (P1, Q1) and any scalars a, b, c ∈ ℚ:

> **(a·P1 + b·Q1) · (b·P1 + c·Q1) = −2·b·(a+c)·e0**

All 15 sedenion vector components are zero by algebra — a structural consequence of the bilateral ZD property, not a property of any specific input sequence. **Formally verified in Lean 4 with zero sorry stubs** by Aristotle (@Aristotle-Harmonic, Harmonic Math). See [`lean/BilateralCollapse.lean`](lean/BilateralCollapse.lean).

Additional Phase 18B findings:
- The Phase 17 two-gap/three-gap "layer structure" (Act/GUE 0.65 → 1.02) was a formula-family contrast (embed_pair P2 harmonic mean vs. sedenion scalar), not a pure scale transition. Within the product family s_n^(k), the Act/GUE transition occurs at **k=2**, not k=3.
- Three-gap statistic is strongly height-dependent; per-window normalization required for clean comparison (resolved in Phase 18C Q5).
- CAILculator confirms actual Riemann three-gap sequence sits between Poisson and GUE on both transform magnitude and conjugation symmetry — consistent with Act/GUE = 1.065.
- Log-prime DFT on three-gap scalar: p=2 SNR = 837× (exceeds q2 Phase 17 SNR of 418×).

**E8 First-Shell Universality (Phase 18D):** Framework-independence structural probe — full 48-member bilateral zero divisor family mapped into E8 space:

- **All 48 bilateral pairs** (6 canonical, 42 CD-specific) embed as E8 first-shell roots (norm² = 2) — universal property of the bilateral condition
- Full family spans **45 distinct E8 root directions** (P∪Q); 26 distinct Q-directions (8 known from Phase 18E, 18 new)
- The Phase 18E **(A₁)⁶ root set is Canonical-Six-P-vector-specific** — it does not extend to the full bilateral family; framework-independence has a geometric consequence
- **AIEX-001 sharpened:** H's (A₁)⁶ geometric domain is tied specifically to the Canonical Six — they are not merely algebraically special within the bilateral family, but geometrically special
- Enumeration confirmed against Lean ground truth (`Count_Unique_ZDs_Is_24`, `native_decide`)
- **Open question:** What root system or sub-lattice do the 45 E8 directions form?

**Heegner Selectivity of q2 (Phase 18F):** The 2-adic tower of real primitive Dirichlet characters terminates at chi8 — no real primitive character of conductor 2^k (k ≥ 4) exists (theorem, confirmed computationally). The companion test between the two real primitive characters of conductor 8 reveals:

- **chi8a** = Kronecker(−8/·), field ℚ(√−2): Q2 mean ratio **0.298** — **elevated**
- **chi8b** = Kronecker(+8/·), field ℚ(√2): Q2 mean ratio **0.148** ≈ chi4 — not elevated

Combined with Phase 18A (chi3, field ℚ(√−3), Q2≈1.0), the Q2 projection selects exactly the L-functions of **ℚ(√−3) and ℚ(√−2)** — both Heegner-number imaginary quadratic fields of class number 1 with known deep connections to E8/E6 Lie algebra structure. ℚ(i) (D=−4, also Heegner, class number 1) is **not** elevated, ruling out class number alone as the discriminating property. The elevation is character-specific, not conductor-level. Route B (p=2 suppression) confirmed for chi8b independently.

**45-Direction Classification (Phase 19 Thread 1):** The full bilateral P∪Q direction set has an exact characterization:

- The 45 bilateral directions = **D₆ minus its 15 "both-negative" roots** — a clean, minimal description
- The set lives entirely in 6D (8D positions 1..6 only; position 7 is completely excluded)
- Every index pair (i,j) with i<j in {1..6} has exactly 3 of 4 sign combos; the missing one is always (−eᵢ, −eⱼ)
- **Clifford Cl(7,0) pass** (via CAILculator `CliffordElement`, Beta v7+): all 1080 closure-failure pair products are 100% mixed grade-0+grade-2; all 15 Cl(6,0) bivectors appear equally → bilateral set is bivector-saturating
- **60 distinct A₂ sub-systems** within the bilateral set → the Eisenstein integer / ℚ(√−3) Heegner connection has a direct geometric expression (A₂ = root system of Eisenstein integers)
- **0 complete D₄ sub-systems** → the ℚ(√−2)/D₄ connection requires a different geometric mechanism
- **Canonical Six (A₁)⁶ have pure Clifford grade structure** (only grade-0 or grade-2, never mixed) — cleanly distinguishing them from the 42 CD-specific bilateral directions within D₆

**Open question generated:** Why does the sedenion Cayley-Dickson construction systematically forbid "both-negative" roots? This is the algebraic question underlying the exact D₆-minus-15 characterization, and may be the key to understanding the full bilateral zero divisor structure.

**AIEX-001 Candidate Statement (Phase 18C):** First formal statement of the operator construction target:

- **Filter Bank Corollary:** The `embed_pair` kernel decomposes prime spectral content into two complementary channels: P-projections form a narrow-band high-pass filter (p≥7); Q-projections form a broadband/low-pass filter covering the full Euler product including p=2. Confirmed from synthesis of Phases 13A, 14B, 15D, 17A.
- **Bilateral Constraint Correspondence (Q3):** The functional equation symmetry s→1−s is proposed to correspond to the E8 Weyl reflection s_α4 (Theorem_1b, Lean 4, zero sorry stubs). Structural parallel: both impose codimension-1 midpoint constraints — fixed hyperplane {x[4]=x[5]} in ℝ⁸ and critical line Re(s)=½ respectively. The 6D bilateral subspace decomposes under s_α4 as **5D fixed** (all bilateral roots except v2/v3) ⊕ **1D antisymmetric** (the v2/v3 antipodal direction). Lean 4 target: `aiex001_functional_equation_correspondence`.
- **Q4 Layer 1:** CAILculator distinguishes χ₃ from ζ Q2 sequences via bilateral zero structure (122 vs 101 pairs, 21% excess in χ₃) — candidate conductor-3 fingerprint. Transform magnitude nearly identical (0.985 ratio).
- **Phase 19 Thread 3 (AIEX-001 operator construction, March 23):** H₅ ⊕ H₁ block structure confirmed by equivariance. Theorem: critical-line zeros embed purely in 5D (no assumptions). Consistency constraint proves at most ONE zero can be off the critical line. H₅ = H_A ⊕ H_B ⊕ H_C block structure from (A₁)⁶ Gram matrix; Block B = Heegner channel (Q2 selectivity for ℚ(√−3) and ℚ(√−2)). Missing step named: `aiex001_critical_line_forcing` (simple spectrum conjecture). Lean 4 status: 6 verified, 2 partial, 1 open.

**Weil-Gram Bridge (Phase 22):** The Gram matrix G5 of the first 100 zero images v(ρₙ) in the 5D fixed subspace is **positive definite** (λ_min=10.46, cond=4.40). λ_min grows linearly to 54.84 at N=500 (R²=0.9999, Phase 23 Thread 2). Zero images span the full 5D subspace with geometric margin — the "systematic collapse" failure mode for strong injectivity is formally ruled out. Only the "specific Diophantine coincidence" failure mode remains (addressed by GSH+Schanuel). CAILculator: diagonal norm Chavez 73.8% vs random 92.9% — **inverted**, GUE clustering signature; ZDTP signed inner products NULL (62.6% vs 63.8%) — sorting pairwise inner products discards sequential level-repulsion structure.

**Weil Explicit Formula Alignment (Phase 23 Thread 3, Phase 24 Thread 1):** The partial Weil sum S(N)=Σf₅D(tₙ) grows ~N^0.77 and is **99.3% aligned with the Weil RHS direction** (= −f₅D(0)) at all N. Residual ratio stabilizes at **12.1% ± 0.6%** (Weil angle locked at 6.8°). Windowed version (Phase 24 Thread 1): Gaussian window T=50..500 gives 11.8–12.0% at N=500 — **the 12% Weil angle is STRUCTURAL**, not a test-function artifact. Block C (p=2) dominates the orthogonal component (Res_C=5.73 vs Res_A=4.15, Res_B=2.87 at N=500). The RHS direction is T-invariant (RHS_T = −(T√π/2)·f₅D(0) for all T) — windowing cannot reduce the angle. GUE suppression confirmed: P(N)/N → 1.270 vs theoretical 1.365 (7% deficit, consistent across Phases 22, 23T2, 23T3).

**12-Vector Finite Subalgebra (Phase 23 Thread 1, Phase 24 Thread 2):** The bilateral sub-triple {q₂, q₃, q₄} (primes {3,13,2}) has a **finite closure of exactly 12 vectors** in 4 generations (0/144 products escape), while the full 6-root closure diverges (6→17→81→878+). CAILculator: 94.4% conjugation symmetry and 95% bilateral zero confidence — both investigation records at time. Left-multiplication by q₃ (L_q₃) on the 12-vector closure is **nilpotent** (all eigenvalues = 0, rank = 6); centralizer = full matrix algebra; [H₅, L_q₃]=0 is vacuously true and imposes no constraints. Avenue 4 CLOSED.

**AIEX-001a: Multiplicative Sedenion Embedding (Phases 25–28):** New formulation F(σ+it) = ∏_p exp_sed(t·log p·r_p) introduced. Key discoveries:

- **Perfect σ symmetry** (Phase 25): ZDTP proxy 0.242 at σ=½ vs 0.162 at σ=0.6; exact bilateral symmetry (σ=0.3=σ=0.7 to 6 decimal places) — functional equation symmetry baked into the multiplicative design.
- **Algebraic identity** (Phase 27): Primes p ∈ {5,7,11} satisfy ‖F×r_p‖/‖F‖ = **1.000 ± 0.000** for ALL t and σ (machine precision). Only p={2,13} (bilateral triple) discriminate. Result is an exact consequence of the sedenion root index structure.
- **AIEX-001a = Berry-Keating xp Hamiltonian** (Phase 28): F(t) = e^{iH_BK·t} where t = BK time, log p = dilation factor, r_p = sedenion direction. The sedenion root direction r_p is exactly what Berry-Keating (1999) was missing to close their program. Evidence: Tr_BK = Σ_p (log p/√p)·cos(t·log p) is negative at **90/100 zeros** vs 35/100 midpoints; mean/Weil_RHS ≈ 0.248; ℏ_sed = 11.19 ± 1.71 (constant, not growing — sedenion Planck constant); V_BK peaks at σ=½ (unimodal maximum at critical line).

**Berry-Keating Burst: Three Conjectures Confirmed (Phase 29):** 500-zero test:
- **Conjecture 29.1 (Weil Negativity):** Ratio mean Tr_BK/Weil_RHS stable at 0.240–0.250 across 6–11 prime sets. Tr_BK < 0 at 383/500 zeros (76.6%), binomial p=2.56×10⁻³⁴.
- **Conjecture 29.2 (Constant Uncertainty):** ℏ_sed = 11.19 ± 1.71, slope = −0.0002 (R²=0.000) — constant, not growing.
- **Conjecture 29.3 (Bilateral Prime Isometry):** p=5,7,11 → ‖F×r_p‖/‖F‖ = 1.000 ± 0.000 for all 50 zeros (machine exact). FIRST regime detection method agreement in 29-phase investigation (HMM=sideways, structural=TRANSITIONAL, agreement=0.70).

---

## Repository Structure

```
CAIL-rh-investigation/
├── papers/                          # Companion paper (Canonical Six v1.3)
├── lean/                            # Lean 4 formal verification (co-authored with Aristotle, Harmonic Math)
├── data/
│   ├── primes/                      # Prime datasets (Sophie Germain, safe primes, gaps)
│   └── riemann/                     # Riemann zero datasets (1k, 10k, χ₃, χ₄)
├── results/                         # All phase result JSON files (Phases 1–17, 18A–18F, 19T1–3, 20B–20D, 21A–21C, 22–24, 25–29)
├── scripts/                         # Python analysis scripts
├── docs/
│   ├── findings_summary.md          # Cumulative results summary
│   ├── roadmap.md                   # Research roadmap
│   ├── aiex_001_hilbert_polya.md    # AIEX-001 conjecture writeup
│   └── phases/                      # Per-phase result writeups
├── lab-notebook/                    # Experiment design documents (pre-registration style)
└── supplemental/                    # Supporting data, converted files
```

---

## Phases Summary

| Phase | Topic | Key Finding |
|-------|-------|-------------|
| 1–2 | Setup & controls | Chavez symmetry baseline; ZDTP non-discriminating for monotone sequences |
| 3 | GUE fingerprint | GUE/Poisson indistinguishable via raw gap symmetry |
| 4 | Spacing ratios | First correct GUE ordering; Montgomery-Dyson confirmed (mean ratio 0.610) |
| 5 | Scale & height | GUE/Poisson separation widens with n; height-stable |
| 6 | Height band survey | Berry-Keating connection; oscillatory delta; variance ratio 5.75× |
| 7–9 | R(α) pair correlation | 14.7 pt GUE/Poisson separation (series record); 1D invariance theorem |
| 10 | P-vector survey | No P-vector discriminates GUE/Poisson via conjugation symmetry; variance ratio is real signal |
| 11–12 | Variance & skewness | Act/GUE variance ratio height-dependent; P2 skewness tracks raw gap skew |
| 13 | Log-prime DFT spectral | **8/9 primes detected (p=3..23), SNR 7–245×**; controls flat |
| 14 | Per-band analysis | Actual > GUE all 20 bands (t=8.18, p≪0.001); SR/P2 filter complementarity |
| 15 | Geometry & corrections | Antipodal isometry = theorem; Weyl orbit spectral split confirmed |
| **16** | **L-function comparison** | **Route B CONFIRMED; Route C ELIMINATED** |
| **17** | **Q-vector access** | **First p=2 detection; 9/9 primes in single projection; Route B re-confirmed 10–14× stronger** |
| **18E** | **E8 root geometry** | **(A₁)⁶ root system; 6D subspace; three P⊥Q orthogonality types; only Pattern 6 is a genuine Weyl reflection** |
| **18A** | **Conductor survey** | **χ₃/Q2 ≈ 1.0 anomaly confirmed conductor-specific to conductor 3; Route B suppression confirmed for χ₅, χ₇, χ₈** |
| **18B** | **Three-gap layer structure** | **Bilateral Collapse Theorem — Lean 4 proven, zero sorry stubs (@Aristotle-Harmonic); n-gap transition at k=2; Phase 17 layer structure was formula-family contrast, not scale transition** |
| **18C** | **AIEX-001 operator construction** | **Filter Bank Corollary stated; s→1−s ↔ s_α4 candidate map; 6D subspace decomposes as 5D fixed ⊕ 1D antisymmetric under s_α4; χ₃ bilateral zero excess (21%) as conductor-3 fingerprint** |
| **18D** | **Framework-independence structural probe** | **E8 first-shell universality: all 48 bilateral pairs on first shell; full family spans 45 E8 directions; (A₁)⁶ is Canonical-Six-specific — Canonical Six are geometrically special within bilateral family** |
| **18F** | **2-adic tower: chi8 companion test** | **Tower-termination theorem: no real primitive character of conductor 16 exists. Heegner selectivity: q2 elevates exactly ℚ(√−3) and ℚ(√−2) among tested fields; ℚ(i) not elevated despite also being Heegner class-number-1. CHARACTER-SPECIFIC result.** |
| **19 Thread 1** | **45-direction E8 root system classification** | **Bilateral set = D₆ minus 15 "both-negative" roots. Lives in 6D (pos. 1..6 only; pos. 7 excluded). Every index pair has exactly 3 of 4 sign combos; missing = always (−,−). Clifford Cl(7,0): 100% mixed grade products; 60 A₂ sub-systems (Eisenstein/ℚ(√−3) connection); 0 D₄ sub-systems; Canonical Six have pure grade structure.** |
| **19 Thread 2** | **Annihilation Topology AT-1** | **Universal Bilateral Orthogonality theorem: ⟨P_8D, Q_8D⟩ = 0 for all 48 bilateral pairs. All give pure grade-2 in Cl(7,0). No direct basis annihilation (0/240 basis pairs). (A₁)⁶ membership necessary but not sufficient for canonical status (20 pairs satisfy it; only 6 are canonical). Canonical/CD-specific split requires Clifford sedenion construction (Cl(8)).** |
| **19 Thread 3** | **AIEX-001 operator construction** | **H₅ ⊕ H₁ block structure; equivariance forces critical-line zeros into 5D (theorem, no assumptions); consistency constraint: at most ONE off-critical-line zero; H₅ = H_A ⊕ H_B ⊕ H_C (Heegner channel = Block B); missing step named: `aiex001_critical_line_forcing` (publishable conjecture). Lean 4: 6 verified, 2 partial, 1 open.** |
| **20B** | **Explicit v(ρ) embedding** | **Formula: v(ρ)=f₅D(t)+(σ−½)·u_antisym; f₅D=Σ_p(log p/√p)·cos(t·log p)·r_p. ALL 4 TESTS PASS (n=1..15): v⁻=0, non-degeneracy, strong injectivity (105 pairs, 0 proportional), equivariance. Reduction complete: aiex001_critical_line_forcing ⟺ Linear Independence of {tₙ·log p} over ℚ (Schanuel + Grand Simplicity Hypothesis).** |
| **20C** | **Scale to n=100 + 9-prime** | **4,950 pairs, 0 proportional — strong injectivity holds. Max |cos θ|=0.993 (6-prime)/0.996 (9-prime), still growing slowly (decelerating). Near-prop alert: ρ₅₄&ρ₉₈ (0.9928). Structural theorem: v₂=u_antisym is RESERVED for functional equation; (A₁)⁶ natural prime capacity = 6 primes (p=2..13). 9-prime cross-block extension does not strengthen injectivity.** |
| **20D** | **Near-miss Diophantine analysis** | **Closest pair (ρ₅₄,ρ₉₈), |cos θ|=0.9928. Ratio spread 125× tighter than generic (2.711 vs 339.6) but NOT near 0 — not a Diophantine resonance. Block A (p=7,11,13) is the failure mode. No prime has |frac(Δt/log p)| < 5%. Consistent with Linear Independence Conjecture; near-proportionality is pure multi-prime amplitude coincidence.** |
| **21A** | **Simple spectrum investigation** | **NULL RESULT — simple spectrum is NOT forced by the AIEX-001 algebra. H₅=I₅ satisfies all constraints (self-adjoint, block-diagonal, equivariant). Gram eigenvalues {0,1,1,1,1,2}; 4D unconstrained eigenspace. [H₅,G]=0 cannot derive simple spectrum. Surprise: two inter-block zero divisor pairs (q₃×q₂=0, q₃×q₄=0) discovered, leading to Phase 21B.** |
| **21B** | **q₃ multi-partner bilateral hub** | **q₃ (p=13) is the unique bilateral hub in the 6-root set: q₃×q₂=0 AND q₃×q₄=0 (both bilateral, both in Phase 18D family). Triple product identity: q₂×q₄ = 2×sign_partner(q₃) — explains anomalous norm²=8. Primes {2,3,13} are algebraically entangled via q₃. v₁ (p=7), v₄ (p=11), v₅ (p=5) have no bilateral partners within the 6-root set.** |
| **21C** | **Target 2 formal closure** | **Target 2 FORMALLY CLOSED. Two independent mechanisms: (1) Interpretation A (module map) ILL-DEFINED — 32/36 root×basis products escape the 5D fixed subspace; (2) bilateral structure does NOT propagate to embeddings (0/105 zero products among f₅D(tᵢ)·f₅D(tⱼ)). No algebraic path constrains H₅ eigenvalues. Remaining route to unconditional RH via AIEX-001: Grand Simplicity Hypothesis or Schanuel's Conjecture.** |
| **22** | **Weil-Gram Bridge** | **G5 (5×5 Gram matrix) positive definite: λ_min=10.46, cond=4.40. Zero images span full 5D fixed subspace. λ_min grows linearly to 54.84 at N=500 (Phase 23T2). "Systematic collapse" failure mode RULED OUT. CAILculator: diagonal norm Chavez inverted (zeros 73.8% vs random 92.9% — GUE clustering); ZDTP signed inner products NULL (sorted pairwise discards sequential GUE structure).** |
| **23 Thread 1** | **Algebraic closure survey** | **Full 6-root closure diverges (6→17→81→878+); no finite sedenion subalgebra; Avenue 4 CLOSED. Bilateral sub-triple {q₂,q₃,q₄} (primes {3,13,2}) has FINITE closure of exactly 12 vectors in 4 generations. CAILculator: 94.4% conjugation symmetry and 95% bilateral zero confidence — both investigation records at time. Primes {2,3,13} are the only finite-closure sub-triple; algebraically distinguished from {5,7,11}.** |
| **23 Thread 2** | **λ_min(G5) trajectory** | **λ_min grows linearly R²=0.9999: 10.46 (N=100) → 54.84 (N=500); Marchenko-Pastur consistent. GUE spacing signature on diagonal norm Chavez: GUE=0.657, zeros=0.660 (nearly identical), random=0.632. 7% GUE suppression in P(N)/N confirmed.** |
| **23 Thread 3** | **Weil explicit formula** | **S(N)=Σf₅D(tₙ) grows ~N^0.77; 99.3% aligned with Weil RHS (= −f₅D(0)) at all N. Residual ratio stabilizes at 12.1% ± 0.6% (Weil angle 6.8°). f₅D not Schwartz-class → Weil sum diverges formally. P(N)/N → 1.270 vs theoretical 1.365 (7% GUE suppression). CAILculator: 98.7% conjugation symmetry on residual ratio — highest in entire investigation.** |
| **24 Thread 1** | **Windowed Weil identity** | **12% Weil angle is STRUCTURAL. Gaussian window T=50..500: residual ratio 11.8–12.0% at N=500 (power-law exponent ≈ 0 = constant model). RHS direction T-invariant: RHS_T = −(T√π/2)·f₅D(0) — windowing cannot reduce the angle. Block C (p=2) dominates orthogonal component (Res_C=5.73 vs Res_A=4.15, Res_B=2.87).** |
| **24 Thread 2** | **Bilateral triple module action** | **12-vector closure IS CLOSED (0/144 products escape). L_q₃ (left-multiplication by q₃) is NILPOTENT (all 12 eigenvalues = 0, rank=6). Centralizer = full matrix algebra; [H₅,L_q₃]=0 vacuously true — imposes no constraints on H₅ eigenvalues. Avenue CLOSED definitively. G12 eigenvalues: {0×4, 1×4, 2×4} = G6 pattern doubled.** |
| **25** | **AIEX-001a: multiplicative 6D embedding** | **New formulation F(σ+it) = ∏_p exp_sed(t·log p·r_p). Perfect σ symmetry around σ=½: ZDTP 0.242 at σ=½ vs 0.162 at σ=0.6 (exact bilateral; σ=0.3=σ=0.7 to 6 decimal places). Functional equation symmetry baked into multiplicative design, not imposed. ZDTP diff: 84.0% conjugation, 95% bilateral confidence.** |
| **26** | **AIEX-001a: full 16D sedenion embedding** | **F×F* = ‖F‖²·e₀ ALWAYS (sedenion alternative law identity — not a criticality condition). ‖F‖² minimized at σ=½ by functional equation symmetry alone; not yet zero-specific. Per-zero sigma* scattered (6/20 in [0.45,0.55]). Discrimination=0.0183. Gateway anisotropy needed → Phase 27.** |
| **27** | **Gateway anisotropy** | **ALGEBRAIC IDENTITY (machine precision): p∈{5,7,11} satisfy ‖F×r_p‖/‖F‖ = 1.000 ± 0.000 for ALL t and σ — exact consequence of sedenion root index structure. Only p={2,13} (bilateral triple) discriminate. p=2 DOWN at zeros (0.924 vs 0.959); p=13 UP at zeros (1.097 vs 1.071). Zeros produce more gateway anisotropy — resonances that break bilateral symmetry.** |
| **28** | **Berry-Keating sedenion Hamiltonian** | **AIEX-001a IS the Berry-Keating xp Hamiltonian in 16D sedenion space. F(t)=e^{iH_BK·t}; r_p is the missing sedenion direction Berry-Keating (1999) lacked. Tr_BK < 0 at 90/100 zeros vs 35/100 midpoints; mean/Weil_RHS ≈ 0.248; ℏ_sed = 11.31 ± 2.93 (constant); V_BK peaks at σ=½ (unimodal). Zeros = moments of destructive prime interference in sedenion geometry.** |
| **29** | **Berry-Keating burst: 500 zeros** | **Three conjectures confirmed. 29.1 (Weil Negativity): ratio 0.240–0.250 stable across 6–11 prime sets; Tr_BK < 0 at 383/500 (76.6%), binomial p=2.56×10⁻³⁴. 29.2 (Constant Uncertainty): ℏ_sed=11.19±1.71, slope=−0.0002 (R²=0.000). 29.3 (Bilateral Prime Isometry): p=5,7,11 → identity holds to machine precision. FIRST regime detection method agreement in 29-phase investigation (HMM=sideways, structural=TRANSITIONAL, agreement=0.70).** |

---

## Canonical Six — Algebraic Foundation

12 zero divisor patterns in 16D sedenion space exhibit dimensional persistence (16D through 256D). These split 50/50:

- **Canonical Six (6)**: Framework-independent — work identically in both Cayley-Dickson and Clifford algebras. Only 3.6% of all 168 sedenion zero divisors.
- **Framework-dependent (6)**: Persist in Cayley-Dickson only; fail in Clifford (norm ≈ √8).

The Canonical Six are the minimal generating set for the complete 24-element bilateral zero divisor family in 16D. Their 5 distinct P-vector images lie on the E8 lattice first shell and form a single Weyl orbit (dominant weight ω₁) — Lean 4 proven.

**Paper:** *Framework-Independent Zero Divisor Patterns in Higher-Dimensional Cayley-Dickson Algebras: Discovery and Verification of The Canonical Six* — Paul Chavez, Chavez AI Labs; formal verification co-author: Aristotle (Harmonic Math).
DOI: [10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495)

---

## Lean 4 Formal Verification

See [`lean/README.md`](lean/README.md) for full details.

All Lean 4 proofs in this repository are co-authored with **Aristotle (@Aristotle-Harmonic, Harmonic Math)** — https://harmonic.fun/

**Fully verified (zero sorry stubs):**
- Bilateral zero divisors and vanishing commutators (all 6 Canonical Six patterns, CD4–CD6)
- E8 first shell membership, Weyl orbit unification (dominant weight ω₁)
- 24-element family generation, framework independence classification
- Chavez Transform convergence and stability theorems
- **Bilateral Collapse Theorem** (`bilateral_collapse`): (a·P1 + b·Q1)·(b·P1 + c·Q1) = −2·b·(a+c)·e0 — proven by Aristotle, independently verified (`lake build`, exit 0)

**Open stubs (pending Mathlib):** G₂ Lie-theoretic invariance, E₆×A₂ confinement, Viazovska sphere-packing connection.

---

## Data

### Prime Datasets (`data/primes/`)
- `sg_germain_primes.json` — 1,171 Sophie Germain primes (range 2–99,839)
- `sg_safe_primes.json` — corresponding safe primes
- `sg_germain_gaps.json`, `sg_safe_gaps.json` — gap sequences
- `primes.json` — general prime dataset

### Riemann Zero Datasets (`data/riemann/`)
- `rh_zeros.json` — 1,000 zeros (mpmath dps=25, range 14.13–1419.42)
- `rh_zeros_10k.json` — 10,000 zeros (mpmath dps=15, range 14.13–9877.78)
- `rh_gaps.json`, `rh_gaps_10k.json` — gap sequences
- `zeros_chi4_2k.json` — 2,092 χ₄ zeros to t=2000 (python-flint)
- `zeros_chi3_2k.json` — 1,893 χ₃ zeros to t=2000 (python-flint)
- `zeros_chi5_phase18a.json` — 1,500 χ₅ zeros to t≈1549 (python-flint, Phase 18A)
- `zeros_chi7_phase18a.json` — 1,500 χ₇ zeros to t≈1480 (python-flint, Phase 18A)
- `zeros_chi8_phase18a.json` — 1,500 χ₈ zeros to t≈1449 (python-flint, Phase 18A)
- `zeros_chi8b_3_phase18f.json` — 1,500 Kronecker(+8/·) zeros to t≈1456 [dirichlet_char(8,3), Phase 18F]

---

## Dependencies

```
Python 3.8+
numpy, scipy, matplotlib, pandas
sympy, mpmath, primesieve
python-flint (v0.8.0) — Dirichlet L-function zeros (100× faster than mpmath)
```

Chavez Transform and ZDTP computations run via the **CAILculator MCP server** (see [ChavezAILabs/CAILculator](https://github.com/ChavezAILabs)).

---

## Citation

```bibtex
@misc{chavez2026cail,
  author       = {Paul Chavez},
  title        = {CAIL-rh-investigation: Empirical Investigation of Riemann Hypothesis Structure Using Sedenion Zero Divisor Analysis},
  year         = {2026},
  publisher    = {GitHub},
  organization = {Chavez AI Labs},
  url          = {https://github.com/ChavezAILabs/CAIL-rh-investigation},
  license      = {CC BY 4.0}
}
```

---

## License

[CC BY 4.0](LICENSE) — Paul Chavez, Chavez AI Labs, 2026.
Lean 4 files co-authored with Aristotle (Harmonic Math); both authors credited under CC BY 4.0.
