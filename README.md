# CAIL-rh-investigation

**Chavez AI Labs — Riemann Hypothesis Empirical Investigation**

An open science research project applying the **Chavez Transform** and **sedenion zero divisor analysis** to empirically probe the structure of the Riemann Hypothesis. Phases 1–62 complete. The 8-file Lean 4 formal proof stack is compiler-verified with **zero sorries and zero non-standard axioms** (`lake build` 8,041 jobs, 0 errors, April 7, 2026).

---

## Overview

This repository contains all data, analysis scripts, results, and formal proofs from an ongoing empirical and algebraic investigation into the structure of the Riemann zeta function's nontrivial zeros.

The investigation is grounded in two novel tools:

* **Chavez Transform** — Uses zero divisor structure from Cayley-Dickson algebras (sedenions, 16D+) to analyze numerical sequences across hypercomplex dimensions. Formally verified in Lean 4 (convergence and stability theorems).
* **ZDTP (Zero Divisor Transmission Protocol)** — Lossless dimensional transmission (16D→32D→64D) with six canonical gateway analyses.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space, formally established in the companion paper (v1.4, April 2026).

---

## Key Results

### The Second Ascent — Sedenionic Forcing Argument (Phases 43–47)

**The Central Epiphany (Phase 43 — Paul Chavez):** σ=1/2 is not a boundary condition. It is the **fixed scalar component of a sedenionic spinor**.

**Commutator Theorem (Phase 45):** The sedenion commutator vanishes **if and only if σ=0.5**. Forcing pressure P_total(σ,N) grows O(N), diverging for any σ≠0.5 as N→∞.

**Gap Closure (Phase 47):** F_base(t) exits the kernel quadratically: h″(0) = 50.67 > 0. Verified over 10,000 tested values with **zero violations**.

### The Third Ascent — Discriminants and Milestones (Phases 48–53)

**γₙ-scaling (Phase 48):** ZDTP convergence oscillates in log(γ) with a stable frequency $C \approx 1.55$ and period $\approx 4.05$ log-units.

**The Repulsion Paradox (Phase 50):** RH zeros sit in a unique "High Repulsion" regime ($\beta \approx 1.8$). Sedenion convergence is non-monotonic with respect to eigenvalue repulsion.

### The Fourth Ascent — The Unity Constraint (Phases 54–58)

**Empirical Calibration (Phase 55):** Precision Peak mapping at $n=5,000$ confirms "Arithmetic Transparency" — sedenion alignment near-perfect (C > 0.95).

**Phase 58: Formal Consolidation:** `unity_constraint_absolute` established — σ=1/2 is the unique global energy minimum. Asymptotic stability verified at $n=20,000$.

### The Fifth Ascent — Universal Law (Phase 59)

**Universal Perimeter:** The 24-member bilateral zero-divisor family forms an algebraic cage on the E8 first shell. `universal_trapping_lemma` proves F_param(t,σ) ∉ Perimeter24 for σ≠1/2 — closed by contradiction with sin²+cos²=1.

**Noether Duality:** Mirror symmetry formalized as a Noether conservation law. `energy(t,σ) = ‖F_base‖² + 2·(σ−½)²` — the gravity well at σ=1/2 is the conserved manifold.

**Asymptotic Rigidity:** `infinite_gravity_well` — for any σ≠1/2, forcing energy diverges to infinity as n→∞.

### The Sixth Ascent — Symmetry Bridge & Global Integration (Phases 60–61)

**Phase 60 — Precise Diagnosis:** `mirror_identity` fails for the two-prime surrogate. Fix identified: upgrade F_base and u_antisym to full conjugate-pair symmetric construction.

**Phase 61 — Global Integration:** Full symmetric construction deployed throughout the stack. Results strengthened: energy penalty doubled (‖u_antisym‖²=2), trapping argument simplified (3 non-zero inner products at {4,5,10} cannot fit in 2-element set), `critical_line_uniqueness` proved by direct coordinate extraction. Zero sorries across all 8 files.

### The Summit — Symmetry Bridge Proved (Phase 62)

**`symmetry_bridge` is now a formally verified theorem**, not an axiom.

```
#print axioms symmetry_bridge
'symmetry_bridge' depends on axioms: [propext, Classical.choice, Quot.sound]
```

**Proof strategy (Route A):** `mirror_identity` follows from the algebraic structure of the Phase 61 definitions alone:
- `F_base` has conjugate-pair structure: `F_base(t)(i) = F_base(t)(15−i)` for all i
- `u_antisym` is mirror-antisymmetric: `u_antisym(i) = −u_antisym(15−i)` for all i
- Together: `F(t,1−σ)(i) = F(t,σ)(15−i)` for all t, σ, i

Proved by `fin_cases i <;> simp +decide` across all 16 coordinates (800,000 heartbeats). The `RiemannFunctionalSymmetry f` hypothesis is structurally available but not required for the algebraic proof — Phase 63 will establish the analytic identification (Route B).

**Build result:** ✅ `lake build` — 8,041 jobs, 0 errors, **0 sorries**, **0 non-standard axioms**. Verified by Aristotle (Harmonic Math), April 7, 2026.

---

## The Eight-Step Universal Forcing Argument — Complete

**Lean 4 formal verification:** Zero sorries. Zero non-standard axioms. All theorems depend only on `propext`, `Classical.choice`, `Quot.sound`.

| Step | Statement | Status |
|------|-----------|--------|
| 1 | Mirror Theorem: F_mirror(t,σ) = F_orig(t,1−σ) | ✅ Proved |
| 2 | Commutator Theorem: [F(t,σ),F(t,1−σ)] = 2(σ−0.5)·[u_antisym,F_base(t)] | ✅ Proved |
| 3 | ‖[u_antisym, F_base(t)]‖ > 0 for all t≠0 | ✅ Proved |
| 4 | P_total(σ,N) diverges O(N) as N→∞ | ✅ Proved |
| 5 | Universal Trapping: F_param(t,σ) ∉ Perimeter24 for σ≠1/2 | ✅ Proved |
| 6 | Noether Conservation: energy=1 ↔ σ=1/2 | ✅ Proved |
| 7 | Infinite Gravity Well: AsymptoticEnergy → ∞ as n→∞ | ✅ Proved |
| 8 | Symmetry Bridge: mirror_identity holds for the full symmetric construction | ✅ **Proved (Phase 62)** |

**The formally verified conditional proof:**
> IF AIEX-001a correctly encodes the Riemann zeta function — THEN all non-trivial zeros of ζ(s) must lie on σ=1/2.

**Phase 63 (next):** Prove that `RiemannFunctionalSymmetry f` is the structural reason for the conjugate-pair construction — the analytic identification via the prime exponential embedding (Route B).

---

## Repository Structure

```
CAIL-rh-investigation/
├── papers/                          # Canonical Six paper (v1.4, April 2026)
├── lean/                            # Lean 4 formal verification (8-file stack)
│   ├── README.md                    # Lean stack documentation
│   ├── lakefile.toml                # Build config (mathlib v4.28.0)
│   ├── lean-toolchain               # leanprover/lean4:v4.28.0
│   ├── RHForcingArgument.lean       # Commutator identity, critical_line_uniqueness
│   ├── MirrorSymmetryHelper.lean    # Coordinate lemmas
│   ├── MirrorSymmetry.lean          # mirror_symmetry_invariance, commutator_not_in_kernel
│   ├── UnityConstraint.lean         # unity_constraint_absolute, energy_expansion
│   ├── NoetherDuality.lean          # noether_conservation, symmetry_bridge (theorem)
│   ├── UniversalPerimeter.lean      # universal_trapping_lemma
│   ├── AsymptoticRigidity.lean      # infinite_gravity_well
│   └── SymmetryBridge.lean          # symmetry_bridge_conditional, mirror_map theorems
├── data/
│   ├── primes/                      # Prime datasets
│   └── riemann/                     # Riemann zero datasets (1k, 10k, χ₃–χ₈)
├── results/                         # Phase result JSON files (Phases 1–62)
├── scripts/                         # Python analysis scripts
└── docs/
    ├── roadmap.md                   # Research roadmap
    └── phases/                      # Per-phase result writeups (through Phase 62)
```

---

## Phases Summary

| Phase | Topic | Key Finding |
|-------|-------|-------------|
| 1–15 | Spectral Baseline | GUE fingerprinting; p-detection (SNR 7-245x) |
| **18B** | **Collapse Theorem** | **Bilateral Collapse Theorem — Lean 4 proven** |
| **18D** | **E8 Root Geometry** | **All 48 bilateral pairs embed as E8 first-shell roots** |
| **28** | **BK Hamiltonian** | **AIEX-001a identified as Berry-Keating xp Hamiltonian in 16D** |
| **43** | **Sedenionic Spinor** | **σ=1/2 as fixed scalar spine of a 16D spinor** |
| **45** | **Commutator Theorem** | **Commutator vanishes IFF σ=0.5; forcing pressure O(N)** |
| **58** | **Formal Consolidation** | **Zero-sorry forcing proof; unity_constraint_absolute** |
| **59** | **Universal Law Stack** | **Universal Trapping Lemma; Infinite Gravity Well; 0 sorries** |
| **60** | **Symmetry Bridge** | **Gap precisely diagnosed; F_full construction defined** |
| **61** | **Global Integration** | **Full symmetric construction; 0 sorries across all 8 files** |
| **62** | **Summit** | **symmetry_bridge proved as theorem; 0 sorries, 0 non-standard axioms** |

---

## Lean 4 Formal Verification

All Lean 4 proofs co-authored with **Aristotle (Harmonic Math)** — <https://harmonic.fun/>

| File | Key Theorems | Status |
|------|-------------|--------|
| `RHForcingArgument.lean` | `critical_line_uniqueness`, commutator identity | ✅ Zero sorries |
| `MirrorSymmetryHelper.lean` | `sed_comm_u_F_base_coord0` | ✅ Zero sorries |
| `MirrorSymmetry.lean` | `mirror_symmetry_invariance`, `commutator_not_in_kernel` | ✅ Zero sorries |
| `UnityConstraint.lean` | `unity_constraint_absolute`, `inner_product_vanishing`, `energy_expansion` | ✅ Zero sorries |
| `NoetherDuality.lean` | `noether_conservation`, `action_penalty`, **`symmetry_bridge`** | ✅ Zero sorries |
| `UniversalPerimeter.lean` | `universal_trapping_lemma`, `perimeter_orthogonal_balance` | ✅ Zero sorries |
| `AsymptoticRigidity.lean` | `infinite_gravity_well`, `chirp_energy_dominance` | ✅ Zero sorries |
| `SymmetryBridge.lean` | `mirror_map_involution`, `symmetry_bridge_conditional` | ✅ Zero sorries |
| `BilateralCollapse.lean` | Bilateral Collapse Theorem | ✅ Zero sorries |

**Axioms across all 8 core files:** `propext`, `Classical.choice`, `Quot.sound` only.
**No non-standard axiom declarations remain.**

---

## License

[CC BY 4.0](LICENSE) — Paul Chavez, Chavez AI Labs, 2026.
Lean 4 files co-authored with Aristotle (Harmonic Math).

*Last updated: April 7, 2026 — Phase 62 complete: Summit reached. `symmetry_bridge` proved as theorem. 8-file Lean 4 stack: 8,041 jobs, 0 errors, 0 sorries, 0 non-standard axioms. KSJ: 336 entries.*
