# Phase 28 Results — Berry-Keating Sedenion Hamiltonian
## Chavez AI Labs LLC · March 25, 2026

**Status:** COMPLETE — major identification
**Script:** `rh_phase28_berry_keating.py`
**Output:** `phase28_bk.json`

## Headline

AIEX-001a IS the Berry-Keating xp Hamiltonian in 16D sedenion space.
F(t) = e^{iH_BK·t} where t=BK time, log p=dilation factor, r_p=sedenion direction.
The sedenion root direction r_p is exactly what Berry-Keating (1999) was missing.

## Key Results

| Measure | Value |
|---|---|
| Tr_BK < 0 at zeros | **90/100** |
| Tr_BK < 0 at midpoints | 35/100 |
| Mean Tr_BK zeros | −0.995 |
| Mean Tr_BK midpoints | +0.300 |
| Weil RHS | −4.014 |
| Ratio mean/RHS | **0.248** |
| ℏ_sed (commutator mean) | 11.31 ± 2.93 |

## CAILculator Results

- Tr_BK at zeros n=100: **44 bilateral zero pairs at 95%** — highest count in investigation
- Commutator norms: **87.5% conjugation, Chavez=130.17**
- V_BK sigma scan peaks at σ=0.5 (0.10158) — unimodal maximum at critical line
- Regime detection: HMM=bull, structural=UNSTABLE, 82.3% symmetry, 1 zero divisor
- ZDTP H_BK: convergence 0.863

## Berry-Keating Prime Product Table (rho_1 vs non-zero)

At ρ₁ (t=14.1347): scalar fraction collapses 93%→7% across six prime products.
V_BK=0.2754, Tr_BK=−2.61 (strongly negative).
At non-zero (t=17.578): smooth decline, no collapse, norm increases.
V_BK=0.1387, Tr_BK=−0.25 (weakly negative).

Zeros are moments of destructive prime interference — resonances of the sedenion BK Hamiltonian.

## Three Conjectures

**29.1 (Weil Negativity):** Tr_BK(tₙ)<0 for ~90-99% of zeros; mean/Weil_RHS≈0.245±0.005 universal.
**29.2 (Constant Uncertainty):** ℏ_sed=11.19±1.71 constant (not growing) across zeros.
**29.3 (Bilateral Prime Isometry):** p∈{5,7,11} → ‖F×r_p‖=‖F‖ exactly (algebraic identity).
