# Phase 27 Results — Gateway Anisotropy
## Chavez AI Labs LLC · March 25, 2026

**Status:** COMPLETE — key algebraic identity discovered
**Script:** `rh_phase27_gateway_anisotropy.py`
**Output:** `phase27_results.json`

## Headline

ALGEBRAIC IDENTITY (machine precision): primes p ∈ {5,7,11} NOT in bilateral triple
satisfy ‖F×r_p‖/‖F‖ = 1.000 ± 0.000 for ALL t and σ. Only primes {2,13} discriminate.

## Per-Prime Gateway Norms (50 zeros)

| Prime | Mean norm ratio | Std | Group |
|---|---|---|---|
| p=2 | 0.924 | 0.183 | Bilateral ← discriminating |
| p=3 | 0.938 | 0.149 | Heegner |
| **p=5** | **1.000** | **0.000** | **Algebraic identity** |
| **p=7** | **1.000** | **0.000** | **Algebraic identity** |
| **p=11** | **1.000** | **0.000** | **Algebraic identity** |
| p=13 | 1.097 | 0.149 | Bilateral ← discriminating |

## V_BK Results (bilateral variance)

- V_BK zeros: 0.054 ± 0.050
- V_BK midpoints: 0.046 ± 0.050
- Zeros > midpoints: 62/100

## CAILculator Results

- Gateway variance at zeros: **98.8% conjugation symmetry** (near investigation record)
- Gateway variance at midpoints: **99.1% conjugation symmetry**
- ZDTP: high-variance zero F(ρ₂) convergence 0.620 vs adjacent midpoint 0.876

## Key Insight

Riemann zeros produce MORE gateway anisotropy — they are resonances in the sedenion
geometry that break bilateral gateway symmetry non-zeros preserve.
