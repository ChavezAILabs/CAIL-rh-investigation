# CAIL-rh-investigation

**Chavez AI Labs — Riemann Hypothesis Empirical Investigation**

An open science research project applying the **Chavez Transform** and **sedenion zero divisor analysis** to empirically probe the structure of the Riemann Hypothesis. Phases 1–29 (empirical/spectral), Phases 30–42 (First Ascent: algebraic structure), Phases 43–47 (Second Ascent: sedenionic forcing argument), Phase 48 (γₙ-scaling of ZDTP convergence), Phase 49 (Discriminant Scan and Structured Sparsity), Phase 50 (The Arithmetic Boundary), and Phase 51 (The Beyond-GUE Asymptote) complete. Built on Lean 4-verified algebraic foundations (Canonical Six, Chavez Transform convergence, Bilateral Collapse Theorem, RH Forcing Architecture).

---

## Overview

This repository contains all data, analysis scripts, results, and formal proofs from an ongoing empirical and algebraic investigation into the structure of the Riemann zeta function's nontrivial zeros.

The investigation is grounded in two novel tools:

* **Chavez Transform** — Uses zero divisor structure from Cayley-Dickson algebras (sedenions, 16D+) to analyze numerical sequences across hypercomplex dimensions. Formally verified in Lean 4 (convergence and stability theorems).
* **ZDTP (Zero Divisor Transmission Protocol)** — Lossless dimensional transmission (16D→32D→64D) with six canonical gateway analyses.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space, formally established in the companion paper (v1.3, Feb 26, 2026).

---

## Key Results

### Empirical Phases (1–29)

**Route B Confirmed (Phase 16):** The log-prime spectral signal in Riemann zero gaps is **arithmetic** in origin — it tracks the Euler product of the specific L-function, not a universal GUE property. Decisive evidence: p=2 suppressed 353× in χ₄ zeros; p=3 suppressed 736× in χ₃ zeros. Eliminates Route C (GUE universality).

**Q-Vector Access (Phase 17):** First detection of p=2 in the nontrivial zero spectrum (SNR=418× via q2 projection). 9/9 primes p=2..23 detected in a single projection. Route B re-confirmed 10–14× more decisively.

**E8 Root Geometry (Phases 18D–18E):** All 48 bilateral pairs embed as E8 first-shell roots (norm²=2). Canonical Six bilateral root set forms (A₁)⁶ root system in a 6D subspace of E8. Full bilateral family spans 45 distinct E8 directions (D₆ minus 15 "both-negative" roots).

**Berry-Keating Sedenion Hamiltonian (Phase 28):** AIEX-001a F(σ+it) = ∏_p exp_sed(t·log p·r_p) is identified as the Berry-Keating xp Hamiltonian in 16D sedenion space. r_p is the missing sedenion direction Berry-Keating (1999) lacked. Tr_BK < 0 at 383/500 zeros (76.6%), binomial p=2.56×10⁻³⁴ (Phase 29).

**Bilateral Collapse Theorem (Phase 18B) — Lean 4 Proven:**
> **(a·P₁ + b·Q₁) · (b·P₁ + c·Q₁) = −2·b·(a+c)·e₀**

Zero sorry stubs. Co-authored with Aristotle (Harmonic Math). See [`lean/BilateralCollapse.lean`](lean/BilateralCollapse.lean).

### The First Ascent — Algebraic Structure (Phases 30–42)

**AIEX-001a Operator Established (Phases 30–35):** The multiplicative sedenion embedding F(σ+it) = ∏_p exp_sed(t·log p·r_p/‖r_p‖) confirmed as the Berry-Keating Hamiltonian in 16D. Gate I2 PASS confirmed hermiticity of F on the (A₁)⁶ Canonical Six subspace. Universal Bilateral Annihilation theorem confirmed: product_norm=0 for all 50 computed F vectors across all 6 gateways.

**Universal Rank Invariant (Phases 36–42):** Norm² inner products on any Canonical Six basis produce rank=4 (6-basis) or rank=12 (60-basis) regardless of basis choice — a universal invariant. ZDTP convergence found to increase systematically with γₙ (first γ-correlated observable outside the norm² class). The Weil ratio c₁=0.118, bilateral symmetry constants c₂≈0.990, c₃≈0.993 established machine-exact.

**Lean 4 Status (Phases 30–42):** Bilateral Collapse Theorem formally verified (zero sorry stubs). Lean 4 local environment established (`rh_investigation` Lake project). 36 bilateral zero-divisor proofs and 18 commutator vanishing theorems in merged file.

### The Second Ascent — Sedenionic Forcing Argument (Phases 43–47)

**The Central Epiphany (Phase 43 — Paul Chavez):** σ=1/2 is not a boundary condition. It is the **fixed scalar component of a sedenionic spinor**:

$$\psi(t) = 0.5 \cdot e_0 + \sum_k \Psi_k(t) \cdot B_k$$

where B_k ∈ {e₃, e₅, e₆, e₉, e₁₀, e₁₂} (Canonical Six bivectors). This reframes the investigation from operator-theoretic to field-theoretic.

**Mirror Wobble Theorem (Phase 44) — Machine Exact:**
$$F_{\text{mirror}}(t, \sigma) = F_{\text{original}}(t, 1-\sigma), \quad \text{error} = 0.00 \times 10^0$$

The sedenion embedding structurally encodes the Riemann Functional Equation. σ=0.5 is the unique fixed point of σ→1−σ. Universal Rank 6 confirmed at matched N across σ={0.4, 0.5, 0.6}.

**Commutator Theorem (Phase 45) — Machine Exact:**
$$[F(t,\sigma), F(t,1-\sigma)]_{\text{sed}} = 2(\sigma - 0.5) \cdot [u_{\text{antisym}}, F_{\text{base}}(t)], \quad \text{error} = 1.46 \times 10^{-16}$$

where u_antisym = (e₄−e₅)/√2. The sedenion commutator vanishes **if and only if σ=0.5**. Forcing pressure P_total(σ,N) grows O(N), diverging for any σ≠0.5 as N→∞.

**Kernel Structure (Phase 46) — Machine Exact:**
$$\|[u_{\text{antisym}}, x]\| = 2 \times \text{dist}(x, \ker(L))$$

All 14 nonzero singular values of the commutator map L are exactly 2.0. ker(L) = span{e₀, u_antisym} — the minimum possible 2D kernel, fully explained by trivial algebraic necessities.

**Gap Closure (Phase 47) — Local Proof + Numerical Seal:**
F_base(t) exits the kernel quadratically: h″(0) = 50.67 > 0. Derivative at t=0 has components exclusively in Canonical Six directions. Confirmed over 10,000 tested values t∈[0.001,10000] with **zero violations**.

### The Third Ascent — Discriminants and Surrogates (Phases 48–49)

**γₙ-scaling and Multi-Pattern Invariance (Phase 48):** ZDTP convergence oscillates in log(γ) with a stable frequency $C \approx 1.55$ and period $\approx 4.05$ log-units. The Chavez Transform (CT) scalar (5.0435 for 12 zeros) is a robust invariant across all Canonical Six patterns, confirming the stability of the convergence baseline.

**The σ-Discriminant (Phase 49):** Off-line zeros ($\sigma=0.4$) produce a +13.7% CT scalar rise (5.7357 vs 5.0435), establishing that Riemann zeros sit at a local minimum of sedenion convergence tension on the critical line.

**The Structured Sparsity Inequality (Phase 49):** ZDTP distinguishes the arithmetic structure of Riemann zeros from statistical models.
> **Poisson (2.62) < RH Actual (2.87) < GUE Surrogate (3.08)**
Riemann zeros are more structured than random chaos but less constrained than pure eigenvalue repulsion. ZDTP serves as a true arithmetic discriminant.

**Prime Commutator Algebra (Phase 49):** Non-commutative interaction $[r_5, r_{13}] = 2e_5 - 2e_{10} - 2e_{15}$ verified. Prime root vector algebra is mediated by the S2/S3A zero divisor subspace.

**The Repulsion Paradox (Phase 50):** Sedenion convergence is **non-monotonic** with respect to eigenvalue repulsion ($\beta$). While $\beta=2$ (GUE) elevates convergence, weak repulsion ($0 < \beta < 1.5$) actually reduces structural stability compared to random (Poisson) models. RH zeros sit in a unique "High Repulsion" regime ($\beta \approx 1.8$).

**The Prime 13 Hub (Phase 50):** Prime 13 acts as a bilateral regulator, forming **Zero Divisor Pairs** with Primes 2 and 3 ($r_2 \times r_{13} = 0$, $r_3 \times r_{13} = 0$). Lower-prime interference is suppressed through these vanishing Interactions.

**Asymptotic Persistence (Phase 51 — DEPRECATED):** The original "asymptotic persistence" signal (0.9334 at $n=10,000$) was identified as a **data leakage hallucination** originating from Phase 49 Poisson surrogates. The Phase 51 results are formally deprecated.

**The Global Forcing Validation (Phase 52):** Investigation re-anchored to Phase 48 ground truth. Global $\sigma$-scan at true $\gamma_{10000} \approx 9877.78$ confirms **$\sigma$-Discriminant symmetry** (95.9% conjugation symmetry) and $E_8$ shell proximity near $|v|^2 = 16.0$. Trajectory at $n=5,000$ recovered ($C=0.9577$), confirming structural stability at high energy.

### The Four-Step Forcing Argument — Current Status

| Step | Statement | Status |
|------|-----------|--------|
| 1 | Mirror Theorem: F_mirror(t,σ) = F_orig(t,1−σ) | ✅ Machine exact (error=0.00e+00) |
| 2 | Commutator Theorem: [F(t,σ),F(t,1−σ)] = 2(σ−0.5)·[u_antisym,F_base(t)] | ✅ Machine exact (error=1.46e-16) |
| 3 | ‖[u_antisym, F_base(t)]‖ > 0 for all t≠0 | ✅ Local proof (h″(0)=50.67) + 0/10,000 numerical |
| 4 | P_total(σ,N) diverges O(N) as N→∞ | ✅ Confirmed (N=10→4.07, N=100→42.59) |

**Lean 4 formal verification:** F_base_not_in_kernel and critical_line_uniqueness proved. All helper lemmas closed. See [`lean/RHForcingArgument.lean`](lean/RHForcingArgument.lean) (883 lines).

**Sorry closure — March 30, 2026 (Aristotle, Harmonic Math):**
Five lemmas closed using a two-prime surrogate for F_base: `F_base(t) = cos(t·log 2)·e₀ + sin(t·log 2)·e₃ + sin(t·log 3)·e₆`. Incommensurability of log 2/log 3 (proved via `log2_div_log3_irrational`) ensures h(t) = sin(t·log 2)² + sin(t·log 3)² vanishes only at t=0, closing `analytic_isolation` and `local_quadratic_exit`. All closed theorems depend only on standard axioms (propext, Classical.choice, Quot.sound).

**Final sorry count: 1 (intentional)**
- `commutator_theorem_stmt` — refactored to a named hypothesis taking `mirror_symmetry` (the sedenionic lift of ζ(s)=ζ(1−s)) as explicit parameter. This is Paper 2's primary target.

**What is now formally proved:** Conditional on the mirror symmetry hypothesis, σ=1/2 is the unique value for which the commutator vanishes for all t≠0. The forcing argument is complete; the one open bridge is precisely named and scoped.

---

## Repository Structure

```
CAIL-rh-investigation/
├── papers/                          # Companion paper (Canonical Six v1.3)
├── lean/                            # Lean 4 formal verification
│   ├── RHForcingArgument.lean       # NEW: Complete forcing argument (492 lines, Lean 4.28)
│   ├── BilateralCollapse.lean       # Bilateral Collapse Theorem (zero sorry stubs)
│   └── README.md                    # Lean file index and sorry status
├── data/
│   ├── primes/                      # Prime datasets (Sophie Germain, safe primes, gaps)
│   └── riemann/                     # Riemann zero datasets (1k, 10k, χ₃, χ₄, χ₅, χ₇, χ₈)
├── results/                         # All phase result JSON files (Phases 1–47)
│   ├── phase43c_wobble_results.json
│   ├── phase43c_zdtp_signatures_wobble.json
│   ├── phase46_results.json
│   └── phase47_results.json
├── scripts/                         # Python analysis scripts
├── docs/
│   ├── CAILCULATOR_NUMERICAL_RECORD.md  # CAILculator run summaries (AIEX-086–220); KSJ source of truth
│   ├── CAILCULATOR_PHASE_43_47_OUTPUTS.md  # Full raw CAILculator outputs, Phases 43–47
│   ├── phase48_cailculator_open_science.md  # Phase 48 verbatim CAILculator returns (12 zeros + CT)
│   ├── findings_summary.md          # Cumulative results summary
│   ├── roadmap.md                   # Research roadmap
│   ├── aiex_001_hilbert_polya.md    # AIEX-001 conjecture writeup
│   └── phases/                      # Per-phase result writeups
├── lab-notebook/                    # Experiment design documents
├── PHASES_30_47_SUMMARY.md          # Summary of First and Second Ascents
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
| 13 | Log-prime DFT spectral | 8/9 primes detected (p=3..23), SNR 7–245×; controls flat |
| 14 | Per-band analysis | Actual > GUE all 20 bands (t=8.18, p≪0.001) |
| 15 | Geometry & corrections | Antipodal isometry = theorem; Weyl orbit spectral split confirmed |
| **16** | **L-function comparison** | **Route B CONFIRMED; Route C ELIMINATED** |
| **17** | **Q-vector access** | **First p=2 detection; 9/9 primes in single projection; Route B re-confirmed 10–14× stronger** |
| **18A** | **Conductor survey** | **χ₃/Q2 ≈ 1.0 anomaly confirmed conductor-specific to conductor 3** |
| **18B** | **Three-gap layer structure** | **Bilateral Collapse Theorem — Lean 4 proven, zero sorry stubs** |
| **18C** | **AIEX-001 operator construction** | **Filter Bank Corollary; s→1−s ↔ s_α₄ candidate map; 6D = 5D fixed ⊕ 1D antisymmetric** |
| **18D** | **Framework-independence probe** | **All 48 bilateral pairs on E8 first shell; 45 E8 directions; (A₁)⁶ is Canonical-Six-specific** |
| **18E** | **E8 root geometry** | **(A₁)⁶ root system; 6D subspace; three P⊥Q orthogonality types** |
| **18F** | **2-adic tower / Heegner** | **Heegner selectivity: q2 elevates exactly ℚ(√−3) and ℚ(√−2); character-specific** |
| **19T1** | **45-direction classification** | **Bilateral set = D₆ minus 15 "both-negative" roots; 60 A₂ sub-systems** |
| **19T2** | **Annihilation topology** | **Universal Bilateral Orthogonality theorem; (A₁)⁶ necessary but not sufficient for canonical status** |
| **19T3** | **AIEX-001 operator** | **H₅⊕H₁ block structure; equivariance forces critical-line zeros into 5D; at most ONE off-line zero** |
| **20B** | **Explicit v(ρ) embedding** | **v(ρ)=f₅D(t)+(σ−½)·u_antisym; 4/4 tests pass; forcing ⟺ Linear Independence {tₙ·log p} over ℚ** |
| **20C–20D** | **Scale to N=100 + Diophantine** | **4,950 pairs, 0 proportional; near-miss analysis; closest pair identified** |
| **21A** | **Simple spectrum** | **NULL — simple spectrum not forced by AIEX-001 algebra; two inter-block zero divisor pairs discovered** |
| **21B** | **q₃ bilateral hub** | **q₃ (p=13) is unique bilateral hub: q₃×q₂=0 AND q₃×q₄=0; primes {2,3,13} algebraically entangled** |
| **21C** | **Target 2 formal closure** | **Target 2 CLOSED. No algebraic path constrains H₅ eigenvalues. Remaining route: GSH or Schanuel** |
| **22** | **Weil-Gram Bridge** | **G5 positive definite (λ_min=10.46). "Systematic collapse" failure mode RULED OUT** |
| **23T1** | **Algebraic closure survey** | **12-vector finite subalgebra {q₂,q₃,q₄}; 94.4% conjugation symmetry (investigation record at time)** |
| **23T2** | **λ_min trajectory** | **λ_min grows linearly R²=0.9999: 10.46→54.84 (N=100→500)** |
| **23T3** | **Weil explicit formula** | **S(N) 99.3% aligned with Weil RHS; 12.1%±0.6% residual (structural)** |
| **24T1** | **Windowed Weil identity** | **12% Weil angle is STRUCTURAL — T-invariant; windowing cannot reduce angle** |
| **24T2** | **Bilateral triple module** | **L_q₃ nilpotent (rank=6); Avenue 4 CLOSED** |
| **25** | **AIEX-001a: multiplicative embedding** | **F(σ+it)=∏_p exp_sed(t·log p·r_p); perfect σ symmetry baked in** |
| **26** | **AIEX-001a: full 16D** | **F×F*=‖F‖²·e₀ (sedenion alternative law); ‖F‖² minimized at σ=½** |
| **27** | **Gateway anisotropy** | **ALGEBRAIC IDENTITY: p∈{5,7,11} → ‖F×r_p‖/‖F‖=1.000±0.000 (machine exact) for ALL t,σ** |
| **28** | **Berry-Keating Hamiltonian** | **AIEX-001a = Berry-Keating xp Hamiltonian in 16D. r_p is the missing sedenion direction** |
| **29** | **Berry-Keating burst** | **Three conjectures confirmed at N=500. Tr_BK<0 at 76.6%, p=2.56×10⁻³⁴** |
| **30–35** | **First Ascent: AIEX-001a operator** | **Gate I2 PASS (hermiticity); Universal Bilateral Annihilation confirmed; Weil ratio c₁=0.118 machine-exact** |
| **36–42** | **First Ascent: rank invariant** | **Universal rank invariant (rank=4/12 basis-independent); ZDTP convergence increases with γₙ** |
| **43** | **Sedenionic spinor definition** | **Paul's epiphany: σ=1/2 = scalar spine of spinor ψ(t)=0.5·e₀+Σ Ψₖ(t)·Bₖ. Field-theoretic reframing** |
| **44** | **Mirror Wobble Theorem** | **F_mirror(t,σ)=F_orig(t,1−σ), error=0.00e+00. Functional equation encoded in sedenion geometry. Universal Rank 6** |
| **45** | **Commutator Theorem** | **[F(t,σ),F(t,1−σ)]=2(σ−0.5)·[u_antisym,F_base(t)], error=1.46e-16. P_total diverges O(N)** |
| **46** | **Kernel structure** | **ker(L)=span{e₀,u_antisym}; ‖[u,x]‖=2·dist(x,ker) exactly; all 14 singular values=2.0** |
| **47** | **Gap closure** | **h″(0)=50.67>0 (local proof); 0/10,000 violations (numerical seal); derivative in Canonical Six directions** |
| **48** | **γₙ-scaling of ZDTP convergence** | **Oscillatory in log(γ), C≈1.55, period≈4.05 log-units; asymptote ~0.927 (NOT 1.0); S3B=S4 universal; CT=5.0435** |
| **49** | **Discriminant scan & surrogates** | **Poisson < RH < GUE inequality; σ=0.4 shift (+13.7%); first prime commutator [r₅, r₁₃] mapped** |
| **50** | **The Arithmetic Boundary** | **Repulsion Paradox (non-monotonicity); RH Actual matches beta ≈ 1.8; Prime 13 acts as bilateral hub/sink** |
| **51** | **The Beyond-GUE Asymptote** | **DEPRECATED — Data leakage from Phase 49 surrogates (0.9334 hallucination)** |
| **52** | **The Global Forcing Validation** | **Re-anchored to P48; σ-Discriminant verified (95.9% symmetry); E8 shell near 16.0** |

---

## Lean 4 Formal Verification

All Lean 4 proofs co-authored with **Aristotle (Harmonic Math)** — <https://harmonic.fun/>

| File | Contents | Status |
|------|----------|--------|
| `canonical_six_bilateral_zero_divisors_cd4_cd5_cd6.lean` | 18 bilateral ZD theorems, 18 commutator theorems (CD4/CD5/CD6) | ✅ Zero sorry stubs |
| `ChavezTransform_Specification_aristotle.lean` | Kernel definitions, Theorems 1–3, 5–6 (convergence, stability) | ✅ Zero sorry stubs |
| `BilateralCollapse.lean` | Bilateral Collapse Theorem: (a·P₁+b·Q₁)·(b·P₁+c·Q₁)=−2·b·(a+c)·e₀ | ✅ Zero sorry stubs |
| `canonical_six_parents_of_24_phase4.lean` | E8 first-shell, Weyl orbit (ω₁), 24-element family generation, framework independence | ✅ Zero sorry stubs |
| `RHForcingArgument.lean` | Complete forcing argument: 36 bilateral ZD proofs, 18 commutator theorems, Mirror Theorem, Commutator Theorem, Exact Identity, F_base_not_in_kernel, critical_line_uniqueness. Two-prime surrogate F_base (log 2, log 3). **883 lines, Lean 4.28.0.** | ⚠️ 1 intentional sorry (commutator_theorem_stmt — bridge to Paper 2). All other lemmas closed by Aristotle (March 30, 2026). |

**Open stubs (pending Mathlib):** G₂ Lie-theoretic invariance, E₆×A₂ confinement, Viazovska sphere-packing connection, concrete sedenionic lift of F_base.

---

## Canonical Six — Algebraic Foundation

12 zero divisor patterns in 16D sedenion space exhibit dimensional persistence (16D through 256D). These split 50/50:

* **Canonical Six (6)**: Framework-independent — work identically in both Cayley-Dickson and Clifford algebras. Only 3.6% of all 168 sedenion zero divisors.
* **Framework-dependent (6)**: Persist in Cayley-Dickson only; fail in Clifford (norm ≈ √8).

The Canonical Six are the minimal generating set for the complete 24-element bilateral zero divisor family in 16D. Their 5 distinct P-vector images lie on the E8 lattice first shell and form a single Weyl orbit (dominant weight ω₁) — Lean 4 proven.

**Paper:** *Framework-Independent Zero Divisor Patterns in Higher-Dimensional Cayley-Dickson Algebras: Discovery and Verification of The Canonical Six* — Paul Chavez, Chavez AI Labs; formal verification co-author: Aristotle (Harmonic Math).
DOI: [10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495)

---

## Data

### Prime Datasets (`data/primes/`)
* `sg_germain_primes.json` — 1,171 Sophie Germain primes
* `sg_safe_primes.json`, `sg_germain_gaps.json`, `sg_safe_gaps.json`, `primes.json`

### Riemann Zero Datasets (`data/riemann/`)
* `rh_zeros.json` — 1,000 zeros (mpmath dps=25)
* `rh_zeros_10k.json` — 10,000 zeros
* `zeros_chi3_2k.json`, `zeros_chi4_2k.json` — χ₃, χ₄ zeros to t=2000
* `zeros_chi5_phase18a.json`, `zeros_chi7_phase18a.json`, `zeros_chi8_phase18a.json`
* `zeros_chi8b_3_phase18f.json` — Kronecker(+8/·) zeros

### Phase Results (`results/`)
* `phase43c_wobble_results.json` — Wobble Test (σ=0.4/0.5/0.6, N=50 matched)
* `phase43c_zdtp_signatures_wobble.json` — Per-gateway ZDTP signatures
* `phase46_results.json` — Kernel structure, singular values, commutator matrix
* `phase47_results.json` — Local proof (h″(0)=50.67), fine-grid scan, gap closure
* `phase48_zdtp_spotcheck.json` — 12 CAILculator ZDTP runs (n=1..5000); oscillatory convergence, S3B=S4 universal
* `phase48_spotcheck_prep.json` — F-vectors for 12 strategic zeros; input to CAILculator
* `phase48_results.json` — Phase 48 summary: C≈1.55, asymptote~0.927, CT=5.0435

---

## Dependencies

```
Python 3.8+
numpy, scipy, matplotlib, pandas
sympy, mpmath, primesieve
python-flint (v0.8.0) — Dirichlet L-function zeros
```

Chavez Transform and ZDTP computations via the **CAILculator MCP server** (see [ChavezAILabs/CAILculator](https://github.com/ChavezAILabs/CAILculator)).

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

*Last updated: March 31, 2026 — Phase 52 complete: Re-anchored to P48; σ-Discriminant verified at n=10,000 (95.9% symmetry); E8 shell proximity (~16.0) confirmed. Phase 51 deprecated due to surrogate leakage. KSJ: 252 entries (AIEX-241–252).*
