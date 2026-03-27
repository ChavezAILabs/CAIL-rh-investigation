# Phase 25 Results — AIEX-001a Multiplicative Embedding (6D Projected)
## Chavez AI Labs LLC · March 25, 2026

**Status:** COMPLETE
**Script:** `rh_phase25_aiex001a_6d.py`
**Output:** `phase25_results.json`

## Headline

AIEX-001a introduced: F(σ+it) = ∏_p exp_sed(t·log p·r_p). Perfect sigma symmetry
around σ=½ in both criticality measure and ZDTP proxy.

## Key Results

| sigma | Mean ZDTP |
|---|---|
| 0.2 | 0.099 |
| 0.3 | 0.119 |
| 0.4 | 0.162 |
| **0.5** | **0.242** |
| 0.6 | 0.162 |
| 0.7 | 0.119 |
| 0.8 | 0.099 |

Exact bilateral symmetry around σ=½ (σ=0.3=σ=0.7, σ=0.4=σ=0.6 to 6 decimal places).
Functional equation symmetry is baked into the multiplicative design, not imposed.

## CAILculator Results

- ZDTP difference (σ=½ − σ=0.6): **84.0% conjugation symmetry**
- Bilateral zero confidence: **95%, 39 symmetric pairs**
- compute_high_dimensional: F(ρ₁) NOT a zero divisor (correct — target is locus)

## Open Issue

F×F* = ‖F‖²·e₀ is the sedenion alternative law identity — not a criticality condition.
Full 16D embedding needed. → Phase 26.
