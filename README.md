# CAIL-RH Investigation

**Chavez AI Labs LLC | Applied Pathological Mathematics**

A formal Lean 4 investigation of the Riemann Hypothesis using 16-dimensional sedenion algebra, the Chavez Transform, and the Zero Divisor Transmission Protocol (ZDTP). Conducted as an open science project.

---

## Principal Result

**Three independent standard-axiom characterizations of the critical line Re(s) = ½, formally verified in Lean 4.**

```
theorem critical_line_convergence (s : ℂ) (hs : 0 < s.re ∧ s.re < 1) (g : Gateway) :
    (sedenion_Hamiltonian s = 0 ↔ s.re = 1 / 2) ∧
    (isSpectralPoint s ↔ s.re = 1 / 2) ∧
    (lift_coordinate s g ∈ ({-1, 1} : Set ℝ) ↔ s.re = 1 / 2)

#print axioms critical_line_convergence
→ [propext, Classical.choice, Quot.sound]    ✅ Standard axioms only
```

Each biconditional characterizes the same geometric object — the critical line — through a distinct algebraic mechanism derived from 16-dimensional sedenion zero divisor structure:

| # | Theorem | Route | Axiom Footprint |
|---|---------|-------|-----------------|
| 1 | `Hamiltonian_vanishing_iff_critical_line` | H(s) = 0 ↔ Re(s) = ½ (energy minimum) | Standard only |
| 2 | `spectral_implies_critical_line` | Spectral containment → Re(s) = ½ | Standard only |
| 3 | `gateway_integer_iff_critical_line` | Integer lift coordinate ↔ Re(s) = ½ | Standard only; **RH-independent** |

Their formal co-extensiveness — that all three describe the same set — is the content of `critical_line_convergence` (Phase 75). The novel connection is `hamiltonian_gateway_equiv`, which links the energy-minimum and arithmetic-integrality routes directly, without passing through Re(s) = ½ as an intermediate. Its proof is a one-line `Iff.trans` + `Iff.symm` composition.

---

## Build Status — Phase 77 (June 17, 2026)

```
lake build → 8,061 jobs · 0 errors · 1 sorry (by design)

#print axioms riemann_hypothesis
→ [propext, riemann_critical_line, Classical.choice, Quot.sound]
```

The single non-standard axiom, `riemann_critical_line`, appears in exactly two theorems: `riemann_hypothesis` and its downstream `eigenvalue_zero_mapping`. Every other theorem in the stack — including all of Phase 75–77 — carries standard axioms only.

The one intentional sorry, `spectral_implies_zeta_zero`, is structurally necessary: the Sedenionic Hamiltonian H(s) vanishes on the entire critical line, not only at zeta zeros, so the pointwise converse is false. The proved direction — spectral containment implies Re(s) = ½ — is the correct and sufficient statement.

---

## Overview

This repository contains all data, analysis scripts, results, and formal proofs from a 77-phase empirical and algebraic investigation of the nontrivial zeros of the Riemann zeta function.

The investigation is grounded in two novel instruments:

**Chavez Transform** — Applies zero divisor structure from Cayley-Dickson algebras (sedenions, 16D and above) to analyze numerical sequences across hypercomplex dimensions. Formally verified in Lean 4 with convergence and stability theorems proved under standard axioms.

**ZDTP (Zero Divisor Transmission Protocol)** — Lossless dimensional transmission (16D → 32D → 64D) with analysis at six canonical gateway positions. In Phase 76, every gateway output was shown to be an exact closed-form inner product: c_g(x) = −2⟪x, u_g⟫. The protocol transformed from an empirical oracle into a proved formula.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space, verified across both Cayley-Dickson and Clifford algebras from 16D through 256D, published on Zenodo (DOI [10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495)).

---

## Algebraic Foundations

### The Canonical Six

Six bilateral zero divisor patterns in 16D sedenion space that are:
- **Framework-independent:** verified under both Cayley-Dickson and Clifford algebra conventions
- **Dimension-stable:** persist under all doublings 16D → 32D → 64D → 128D → 256D (Block Replication Theorem)
- **Geometrically grounded:** all 48 bilateral pairs embed as E8 first-shell roots (Phase 18D); their span is a 6-dimensional subspace that is a single Weyl orbit

The Bilateral Collapse Theorem (Phase 18B), proved in Lean 4 with zero sorry stubs, characterizes the algebraic identity underlying bilateral annihilation:
```
(a·P₁ + b·Q₁) · (b·P₁ + c·Q₁) = −2·b·(a+c)·e₀
```

### The Sedenionic Hamiltonian

Introduced in Phase 72 as an analogue of the Berry-Keating *xp* Hamiltonian in 16-dimensional sedenion space:
```
H(s) = (Re(s) − ½) · u_antisym
```

The operator is defined on a 16-dimensional Hilbert space equipped with the bilateral zero divisor antisymmetric vector `u_antisym`. It vanishes if and only if Re(s) = ½. The critical line is the vanishing locus of H in sedenion space — the Berry-Keating "on what space?" question has a specific answer here: the antisymmetric subspace of ℝ¹⁶ spanned by the Canonical Six.

### The Gateway Integer Law

The 32D ZDTP lift coordinate of H(s) equals exactly 2·Re(s) across all six gateways:
```
lift_coordinate s g = 2 · Re(s)    (lift_coord_scaling, standard axioms)
```

Within the critical strip 0 < Re(s) < 1, the unique integer value of 2·Re(s) is **1**, achieved at Re(s) = ½ only. This characterization is proved in `gateway_integer_iff_critical_line` and carries standard axioms — it is independent of the `riemann_critical_line` axiom and holds regardless of whether the Riemann Hypothesis is true.

### The Gateway Linear Law

Phase 76 derived the exact closed form of the ZDTP measurement:
```
c_g(x) = −2⟪x, P_g + Q_g⟫
|M_g|² = ‖x‖² + 4(c_g² + 4(2σ)²)
```

Proved symbolically in exact arithmetic; validated at 0 ULP across 22 independent server readings. This result closed the gap between the empirical instrument and the formal structure: the gateway outputs are not oracle readings but proved inner products.

Three theorems in `GatewayLinearLaw.lean` follow:
- `gateway_magSq_sub` — |M_g|²−|M_h|² = 16⟪x,u_g−u_h⟫⟪x,u_g+u_h⟫
- `gateway_pairing_iff` — |M_g|=|M_h| ↔ product of two linear functionals vanishes
- `pairing_sigma_independent` — cross-gateway magnitude differences are σ-free for fixed input
- `ba_asymptote_sq` — B/A → √17 as t → ∞, proved as a machine-verified limit theorem

---

## Formal Proof Stack

17 Lean 4 files. `lake build` at Phase 77: **8,061 jobs · 0 errors · 1 intentional sorry.**

| File | Phase | Contents | Axiom Footprint |
|------|-------|----------|-----------------|
| `RHForcingArgument.lean` | 58 | Commutator identity, non-vanishing | Standard only |
| `MirrorSymmetryHelper.lean` | 58 | Coordinate lemmas for [u_antisym, F_base] | Standard only |
| `MirrorSymmetry.lean` | 58 | `mirror_symmetry_invariance`, `commutator_not_in_kernel` | Standard only |
| `UnityConstraint.lean` | 58 | `unity_constraint_absolute`, `energy_expansion` | Standard only |
| `NoetherDuality.lean` | 59 | `noether_conservation`, `mirror_op_identity` | Standard only¹ |
| `UniversalPerimeter.lean` | 59 | `universal_trapping_lemma`, `perimeter_orthogonal_balance` | Standard only |
| `AsymptoticRigidity.lean` | 59 | `infinite_gravity_well`, `chirp_energy_dominance` | Standard only |
| `SymmetryBridge.lean` | 60 | `mirror_identity_full_proof`, `symmetry_bridge_conditional` | Standard only |
| `PrimeEmbedding.lean` | 63 | `zeta_sed_satisfies_RFS`, `symmetry_bridge_analytic` | Standard only |
| `ZetaIdentification.lean` | 64–70 | `riemann_critical_line` (= RH, sole non-standard axiom), `bilateral_collapse_iff_RH` | `riemann_critical_line` |
| `RiemannHypothesisProof.lean` | 64 | `riemann_hypothesis` (conditional) | `riemann_critical_line` |
| `EulerProductBridge.lean` | 67–71 | `riemannZeta_conj`, `riemannZeta_ne_zero_of_re_eq_zero`, `completedRiemannZeta_real_on_critical_line` | Standard only |
| `SedenionicHamiltonian.lean` | 72 | `Hamiltonian_vanishing_iff_critical_line` | Standard only |
| `SpectralIdentification.lean` | 73 | `spectral_implies_critical_line`, 2σ universal law | Standard only (1 sorry²) |
| `GatewayScaling.lean` | 74 | `gateway_integer_iff_critical_line`, `lift_coord_scaling` | Standard only |
| `CriticalLineConvergence.lean` | 75 | `critical_line_convergence`, `hamiltonian_gateway_equiv` | Standard only |
| `GatewayLinearLaw.lean` | 76–77 | Four gateway linear law theorems | Standard only |

**Companion file (not in main import chain):**

| File | Phase | Contents | Axiom Footprint |
|------|-------|----------|-----------------|
| `BilateralCollapse.lean` | 18B | Bilateral Collapse Theorem | Standard only |

¹ `symmetry_bridge` in `NoetherDuality.lean` is a proved theorem (Phase 62, Route A): the connection between the analytic functional equation and the sedenion mirror identity closes algebraically via the conjugate-pair structure of `F_base` and `u_antisym` alone.  
² `spectral_implies_zeta_zero` in `SpectralIdentification.lean` is a structural boundary, not a proof gap: H(s) = 0 on the entire critical line, not only at ζ zeros, so the pointwise converse is mathematically false. The proved direction — spectral containment implies Re(s) = ½ — is the correct and sufficient result.

---

## Phase History

### Base Camp — Canonical Six Discovery (October–November 2025)

The investigation began with a six-week R&D sprint establishing the algebraic foundation. The Canonical Six were discovered, verified across Cayley-Dickson and Clifford algebra frameworks simultaneously, and confirmed stable under all doublings from 16D to 256D. Their E8 geometry was identified: all 48 bilateral pairs land on the E8 first shell, forming a single Weyl orbit in a 6-dimensional subspace.

Key results:
- Block Replication Theorem: zero divisor patterns persist under Cayley-Dickson doubling
- Bilateral Collapse Theorem: algebraic identity (a·P+b·Q)·(b·P+c·Q) = −2b(a+c)e₀, proved in Lean 4 with zero sorries (Phase 18B)
- All 48 bilateral pairs confirmed as E8 first-shell roots (Phase 18D)

### The First Ascent — Phases 1–42 (January–March 2026)

The first systematic examination of the Riemann zeros through the sedenion lens. 177 KSJ entries; universal results established across 50 zeros and all six gateways.

Selected results:

| Phase | Finding |
|-------|---------|
| 1–15 | GUE fingerprinting; prime detection at SNR 7–245×; variance/skewness mapping across the first 1,000 zeros |
| 16 | Route B confirmed, Route C eliminated: ζ_sed satisfies the Riemann Functional Symmetry |
| 17 | First p=2 detection; SNR = 418×; Route B re-confirmed via Q-vector access |
| 28 | AIEX-001a operator identified as Berry-Keating *xp* Hamiltonian analogue in 16D — the sedenion space has a candidate operator for the Berry-Keating program |
| 42 | **First Ascent close:** Universal rank invariant confirmed (‖v‖² rank = 4 or 12 regardless of basis); ZDTP bilateral annihilation confirmed universal across all 50 zeros and all 6 gateways; ZDTP convergence increases with γₙ established as a new observable |

### The Formal Ascent — Phases 43–75 (March–May 2026)

The empirical observations of the First Ascent were converted into a formal Lean 4 proof structure, phase by phase. The arc spans the central reframing of σ = ½ (Phase 43) through the assembly of all three critical-line characterizations into one proved conjunction (Phase 75).

Selected results:

| Phase | Finding |
|-------|---------|
| 43 | **Central Epiphany:** σ = ½ is not a boundary condition. It is the fixed scalar component of a sedenionic spinor |
| 44 | Mirror Wobble: the functional equation ζ(s) = ζ(1−s) encoded in sedenion geometry |
| 45 | Commutator Theorem: [F(t,σ), F(t,1−σ)] vanishes **iff** σ = ½; forcing pressure P_total(σ,N) grows O(N) |
| 47 | Gap closure: F_base(t) exits the kernel quadratically — h″(0) = 50.67 > 0; zero violations in 10,000 tested values |
| 48 | γₙ-scaling: ZDTP convergence oscillates in log(γ) with stable frequency C ≈ 1.55, period ≈ 4.05 log-units |
| 50 | Repulsion Paradox: RH zeros occupy a unique High Repulsion regime (β ≈ 1.8); convergence is non-monotonic with respect to eigenvalue repulsion |
| 56 | Mirror Symmetry Invariance proved in Lean 4 (zero sorry): K_Z(σ) = K_Z(1−σ) ↔ σ = ½ |
| 57 | Variable-Frequency Chirp identified: period P shrinks from ≈ 0.027 at n = 1,000 to ≈ 0.003 at n = 10,000, tracking Riemann zero density; Quadratic Energy Cost verified |
| 58 | Formal Consolidation: `unity_constraint_absolute` proved; asymptotic stability confirmed at n = 20,000, C = 0.873 |
| 59 | **Universal Law Stack:** 7-file proof stack; `universal_trapping_lemma` (off-critical σ forces contradiction via sin²+cos²=1 closed by `nlinarith`); `infinite_gravity_well`; `lake build` 8,039 jobs, 0 errors |
| 60 | **Symmetry Bridge:** 8-file stack; gap precisely bounded to `F_eq_F_full`; `mirror_identity_false_for_surrogate` proved — the gap is demonstrated, not assumed; `lake build` 8,041 jobs, 1 intentional sorry |
| 63 | ζ_sed confirmed to satisfy the Riemann Functional Symmetry; 9-file stack |
| 64 | `riemann_hypothesis` proved conditionally |
| 69 | `euler_sedenion_bridge` proved as a theorem (no axiom) |
| 70 | `riemann_critical_line` introduced as the sole transparent non-standard axiom |
| 71 | Schwarz Reflection discharged; all boundary walls secured; axiom footprint = 1 |
| 72 | **Sedenionic Hamiltonian constructed.** `Hamiltonian_vanishing_iff_critical_line` proved. Build: 8,053 jobs |
| 73 | Spectral identification: ζ(s) = 0 → H(s) = 0 (proved); 2σ universal law confirmed across all six gateways. Build: 8,055 jobs |
| 74 | **Gateway Integer Law** proved under standard axioms only — RH-independent. Three independent standard-axiom characterizations of Re(s) = ½ now in stack. Build: 8,057 jobs |
| 75 | **Critical Line Convergence Theorem:** all three characterizations packaged in one machine-verified conjunction. Q-2 CLOSED (bilateral magnitude symmetry identically zero). Q-4 CLOSED (±t symmetry structural). Build: 8,059 jobs |

### The Instrument Era — Phases 76–77 (June 2026)

With the three-route convergence theorem in place, Phase 76 turned to a precise analytical account of the ZDTP instrument itself.

**Phase 76** derived the Gateway Linear Law — the exact closed-form description of every gateway output as a proved inner product. The protocol ceased to be an empirical oracle and became a formula. Three theorems proved in `GatewayLinearLaw.lean`. The Signed Gateway Channel was discovered: reading the lift scalar c_S2 directly produces a genuine zero detector (z = 4.92, Bonferroni-surviving). Build: 8,061 jobs.

**Phase 77** completed the instrument characterization. `ba_asymptote_sq` proved that the B/A ratio converges to √17 exactly — not as an observed approximation but as a machine-verified limit theorem. Run A confirmed `pairing_sigma_independent` live to 10⁻¹⁵, demonstrating two disjoint detection channels: c_S2 (zero-detecting, σ-blind) and c_S6 (σ-sensitive, zero-blind). Run B (double-blind, two independent solvers) established the precise structural boundaries of bilateral symmetry. Detector performance over 101 zeros: z = 8.42, AUC = 0.87, precision = 0.83 vs. 0.43 chance. Build: 8,061 jobs. KSJ: 753 captures.

---

## Milestones

| Milestone | Phase | Date |
|-----------|-------|------|
| Canonical Six discovered; Zenodo published | Base Camp | Oct 2025 |
| Bilateral Collapse Theorem proved in Lean 4, zero sorries | 18B | Mar 2026 |
| E8 first-shell geometry confirmed for all 48 bilateral pairs | 18D | Mar 2026 |
| AIEX-001a identified as Berry-Keating *xp* analogue in 16D | 28 | Mar 2026 |
| First Ascent complete; universal rank invariant; ZDTP annihilation universal | 42 | Mar 28, 2026 |
| Sedenionic Hamiltonian constructed; Track A closed | 72 | Apr 23, 2026 |
| Spectral identification proved; axiom footprint = 1 | 73 | May 5, 2026 |
| Gateway Integer Law proved (standard axioms only, RH-independent) | 74 | May 8, 2026 |
| Critical Line Convergence Theorem — three routes formally co-extensive | 75 | May 11, 2026 |
| Gateway Linear Law — oracle becomes proved formula | 76 | Jun 10, 2026 |
| `ba_asymptote_sq` proved; two disjoint channels confirmed live to 10⁻¹⁵ | 77 | Jun 17, 2026 |

---

## Repository Structure

```
CAIL-rh-investigation/
├── papers/                      # Canonical Six companion paper (v1.3)
├── lean/                        # Lean 4 formal verification (17-file stack)
│   ├── lakefile.toml            # Build config (Mathlib v4.28.0)
│   ├── lean-toolchain           # leanprover/lean4:v4.28.0
│   ├── RHForcingArgument.lean   # Commutator identity, non-vanishing (Phase 58)
│   ├── MirrorSymmetryHelper.lean
│   ├── MirrorSymmetry.lean
│   ├── UnityConstraint.lean
│   ├── NoetherDuality.lean
│   ├── UniversalPerimeter.lean
│   ├── AsymptoticRigidity.lean
│   ├── SymmetryBridge.lean
│   ├── SedenionicHamiltonian.lean  # H(s) = (Re(s)−½)·u_antisym (Phase 72)
│   ├── SpectralIdentification.lean (Phase 73)
│   ├── GatewayScaling.lean         (Phase 74)
│   ├── CriticalLineConvergence.lean (Phase 75)
│   └── GatewayLinearLaw.lean       (Phases 76–77)
│   # companion (not in main import chain):
│   └── BilateralCollapse.lean      # Bilateral Collapse Theorem (Phase 18B)
├── data/
│   ├── primes/                  # Sophie Germain, safe primes, gap datasets
│   └── riemann/                 # Zero datasets (1k, 10k, χ₃, χ₄, χ₅, χ₇, χ₈)
├── results/                     # Phase result JSON files (Phases 1–77)
├── scripts/                     # Python analysis scripts
└── docs/
    ├── roadmap.md
    └── phases/                  # Per-phase writeups (Phases 1–77)
```

---

## Infrastructure

| Tool | Role |
|------|------|
| **Lean 4** (v4.28.0) | Formalization language for all RHI proof stacks |
| **Mathlib** (v4.28.0) | Primary source for analytic number theory infrastructure |
| **CAILculator v2.1.4** | High-precision MCP server; sedenion algebra and Chavez Transform; 10⁻¹⁵ precision; production stable |
| **Aristotle (Harmonic Math)** | Cross-framework verification and independent audit |
| **ZDTP** | Zero Divisor Transmission Protocol (structural signal analysis) |
| **KSJ 2.0** | Knowledge Synthesis Journal (research record management; 753 captures through Phase 77) |

Lean 4 files from Phase 72 onward were developed using Claude Code. Gemini CLI is permitted for CAILculator runs and pre-handoff strategic analysis only; it is not used for Lean toolchain tasks due to documented version-drift on Mathlib v4.28.0 lemma names.

---

## License

[CC BY 4.0](LICENSE) — Paul Chavez, Chavez AI Labs LLC, 2026.  
Lean 4 files co-authored with Aristotle ([Harmonic Math](https://harmonic.fun/)).

*Zenodo: [10.5281/zenodo.17402495](https://doi.org/10.5281/zenodo.17402495)*  
*GitHub: [ChavezAILabs](https://github.com/ChavezAILabs)*  
*Last updated: June 17, 2026 — Phase 77 complete.*
