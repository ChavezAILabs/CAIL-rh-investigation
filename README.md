# CAIL-rh-investigation

**Chavez AI Labs — Riemann Hypothesis Empirical Investigation**

An open science research project applying the **Chavez Transform** and **sedenion zero divisor analysis** to empirically probe the structure of the Riemann Hypothesis. Phases 1–16 complete. Formally verified in Lean 4.

---

## Overview

This repository contains all data, analysis scripts, results, and formal proofs from an ongoing empirical investigation into the arithmetic and spectral structure of the Riemann zeta function's nontrivial zeros.

The investigation is grounded in two novel tools:

- **Chavez Transform** — Uses zero divisor structure from Cayley-Dickson algebras (sedenions, 16D+) to analyze numerical sequences across hypercomplex dimensions. Formally verified in Lean 4 (convergence and stability theorems).
- **ZDTP (Zero Divisor Transmission Protocol)** — Lossless dimensional transmission (16D→32D→64D) with six canonical gateway analyses.

The algebraic foundation is the **Canonical Six** — six framework-independent bilateral zero divisor patterns in 16D sedenion space, formally established in the companion paper (v1.3, Feb 26, 2026).

### Key Result: Route B Confirmed (Phase 16)

The log-prime spectral signal detected in Riemann zero gaps is **arithmetic** in origin (tracks the Euler product of the specific L-function), not statistical (not a universal GUE property). Decisive evidence:

- p=2 suppressed 353× in χ₄ zeros (χ₄(2)=0, ramified prime)
- p=3 suppressed 736× in χ₃ zeros (χ₃(3)=0, ramified prime)
- All other primes present in both — exactly matching Euler product structure

This eliminates Route C (GUE universality) and strongly supports AIEX-001: a Hilbert-Pólya operator in sedenion space.

---

## Repository Structure

```
CAIL-rh-investigation/
├── papers/                          # Companion paper (Canonical Six v1.3)
├── lean/                            # Lean 4 formal verification (co-authored with Aristotle, Harmonic Math)
├── data/
│   ├── primes/                      # Prime datasets (Sophie Germain, safe primes, gaps)
│   └── riemann/                     # Riemann zero datasets (1k, 10k, χ₃, χ₄)
├── results/                         # All phase result JSON files (Phases 1–16)
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

**Fully verified (zero sorry stubs):** bilateral zero divisors, vanishing commutators, E8 first shell membership, Weyl orbit unification, 24-element family generation, framework independence, Chavez Transform convergence and stability.

**Open stubs (pending Mathlib):** G₂ Lie-theoretic invariance, E₆×A₂ confinement, Viazovska sphere-packing connection.

Lean 4 proofs co-authored with **Aristotle (Harmonic Math)** — `aristotle-harmonic@harmonic.fun` — https://harmonic.fun/

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
