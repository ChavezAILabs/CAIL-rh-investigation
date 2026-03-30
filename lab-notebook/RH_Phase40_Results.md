# RH Phase 40 Results -- Normalized Operator + Anti-Correlation Source + Eigenvalue Distribution

**Chavez AI Labs LLC** · *Applied Pathological Mathematics -- Better math, less suffering*

|                     |                                                                              |
|---------------------|------------------------------------------------------------------------------|
| **Date**            | 2026-03-28                                                                   |
| **Phase**           | 40 -- M_norm + Anti-Correlation + Full Eigenvalue Distribution               |
| **Author**          | Paul Chavez / Chavez AI Labs LLC (co-authored with Claude Sonnet 4.6)        |
| **Script**          | `rh_phase40.py`                                                              |
| **Status**          | COMPLETE                                                                     |

---

## Executive Summary

Phase 40 tested whether normalizing by ||F||^2 would remove the anti-correlation observed in Phase 39. The pre-flight check (Task A1) immediately falsified the normalization hypothesis: Spearman(||F||^2, gamma_n) = -0.084, p=0.41 -- not significant. The anti-correlation is directional, not amplitude-based.

Track A2 revealed a deeper finding: the Phase 39 anti-correlation (rho~-0.4 at n=10) was another small-sample artifact. At n=100, M_tilde gives rho=-0.025 (p=0.80) -- essentially zero. The "anti-correlation problem" from Phase 39 disappears with adequate sample size.

Track D1 (full eigenvalue distribution at N=60) is the primary finding: **half of the 3000 eigenvalues (median ~0) are near zero, and the distribution shape is completely wrong compared to the Riemann zero distribution.** The eigenvalues are concentrated near 0 with sparse large outliers; the zeros are distributed across [14, 236]. Additionally, M_tilde has negative eigenvalues (min = -63.3), confirming it is not positive semidefinite.

Track W1 confirms the Weyl density ceiling: 16D sedenions (60 vectors maximum) require N~820 for Weyl matching -- more than 13x the available dimension.

---

## Track V1 -- Formula Verification

| Quantity | Value |
|---------|-------|
| lambda_max at gamma_1 (M_tilde, N=6) | **21.955** |
| ||F||^2 at gamma_1 | 0.9117 |
| Phase 39 baseline | 21.955 |
| Match | TRUE |

Baseline confirmed exactly. All downstream comparisons are valid.

---

## Track A1 -- ||F||^2 vs gamma_n (Pre-flight gate)

| Quantity | Value |
|---------|-------|
| Spearman(||F||^2, gamma_n) | rho = -0.084, p = 0.41 |
| ||F||^2 range (n=100) | [0.480, 2.958] |
| ||F||^2 mean | 1.339 +/- 0.434 |

**Gate A1: FAIL.** ||F||^2 is not significantly correlated with gamma_n (rho=-0.084, p=0.41). The amplitude of F(t) does not systematically decrease as gamma increases.

**Conclusion:** The anti-correlation rho~-0.4 from Phase 39 is directional, not amplitude-based. Normalization by ||F||^2 will not remove it. Tracks A2 and N1_norm run as confirmatory only.

---

## Track A2 -- M_norm Baseline at N=6

| Operator | rho | p-value | lambda_max range |
|---------|-----|---------|-----------------|
| M_tilde | -0.025 | 0.80 | [10.9, 70.5] |
| M_norm  | +0.097 | 0.34 | [21.6, 39.0] |

**Gate A2: PASS** (rho_norm = +0.097 > -0.1), but both rhos are statistically insignificant.

**Critical observation:** M_tilde rho at n=100 is -0.025 (p=0.80) -- this is essentially zero. Phase 39 reported rho=-0.4545 for N=6 at n=10 zeros. **The Phase 39 anti-correlation at n=10 was a small-sample artifact**, analogous to the k=15 artifact (Phase 39 K1 FAIL). At adequate sample size, no statistically significant correlation exists in either direction.

---

## Track D1 -- Full Eigenvalue Distribution at N=60 (PRIMARY)

### Correlation result

| Quantity | Value |
|---------|-------|
| Spearman(lambda_max, gamma_n) | rho = -0.013, p = 0.93 |
| Mean eigenvalues above gamma_1 | 7.32 |
| Total eigenvalues analyzed | 3000 (60 evals x 50 zeros) |

At n=50, lambda_max is essentially uncorrelated with gamma (p=0.93). The anti-correlation is gone.

### Eigenvalue distribution shape

| Range | Eigenvalue count | Zero count | Ratio |
|-------|-----------------|------------|-------|
| [0, 50)     | 1554 (51.8%) | 10 (20%) | 155.4 |
| [50, 100)   |   31 ( 1.0%) | 19 (38%) |   1.6 |
| [100, 150)  |    0 ( 0.0%) | 21 (42%) |   0.0 |
| [150, 200)  |    2 ( 0.1%) |  0 ( 0%) |  inf  |
| [200, 300)  |   19 ( 0.6%) |  0 ( 0%) |  inf  |
| [300, 500)  |   24 ( 0.8%) |  0 ( 0%) |  inf  |

**The eigenvalue distribution and zero distribution have opposite shapes.** Zeros are concentrated in [14, 150]; eigenvalues are concentrated near 0 with large outliers above 200. The shapes do not match.

### Structural findings

- **Median eigenvalue: 1.8e-15 (approximately zero).** More than half of the 3000 eigenvalues are near zero, meaning M_tilde is near-rank-deficient at most zeros.
- **Minimum eigenvalue: -63.3.** M_tilde is NOT positive semidefinite. Negative eigenvalues occur structurally.
- **Maximum eigenvalue: 583.4.** Far larger than Phase 39's 374 maximum (50 zeros vs 10 zeros capture more extreme values).

**Root cause hypothesis:** The 60x60 M_tilde matrix is built from F(t) evaluated at a single zero tₙ -- a rank-deficient outer product structure. The sedenion product P_i * (F * P_j) projects F through 60 bilateral directions, but F lives in 16D sedenion space (not 60D). The effective rank of M_tilde is at most 16, generating at most 16 nonzero eigenvalues per zero -- consistent with the observation that ~7 eigenvalues are above gamma_1 and most others are near zero.

---

## Track S1 -- Correlated Subspace Selection

### Top diagonal correlations (max rho = +0.217, all non-significant)

| Rank | Vector index | rho | p-value |
|------|-------------|-----|---------|
| 1-2 | 24, 25 | +0.217 | 0.129 |
| 3-4 | 16, 17 | +0.212 | 0.140 |
| 5-8 | 34,35,48,49 | +0.146 | 0.314 |
| 9-10 | 18, 19 | +0.089 | 0.541 |

No bilateral vector has statistically significant diagonal correlation with gamma_n (all p > 0.12). The best correlation (rho=+0.217) is consistent with chance.

### Top-k subspace results

| k | rho | p-value | lambda_max range |
|---|-----|---------|-----------------|
| 6  | +0.184 | 0.202 | [21.0, 79.9] |
| 12 | +0.093 | 0.519 | [38.8, 162.1] |
| 18 | +0.049 | 0.733 | [57.6, 195.3] |

None are statistically significant. Selecting the "most correlated" vectors does not improve spectral matching beyond the sequential subspace. **Direction closed.**

---

## Track N1 -- M_norm Growing Subspace (Confirmatory)

| N (dim) | rho (M_norm) | above_gamma1 | lambda_max range |
|---------|--------------|-------------|-----------------|
| 6       | -0.024       | 1.0         | [20.6, 35.6]    |
| 12      | +0.045       | 1.3         | [45.7, 55.6]    |
| 18      | -0.061       | 1.9         | [69.6, 82.5]    |
| 30      | -0.115       | 3.3         | [118.9, 129.3]  |
| 45      | -0.059       | 5.3         | [180.1, 195.2]  |
| 60      | -0.199       | 6.3         | [240.2, 258.7]  |

All rhos are statistically insignificant (all p > 0.15). M_norm shrinks the lambda_max range relative to M_tilde (tighter spread: [240, 259] vs [186, 374]) but does not introduce positive correlation. Normalization does not improve spectral matching.

---

## Track N2 -- Normalized Eigenvalue Density

| Quantity | Value |
|---------|-------|
| Mean eigenvalues above gamma_1 (N=60) | 6.32 |
| Eigenvalue range (M_norm) | [-30.3, 258.7] |
| Negative eigenvalues | YES (min = -30.3) |

**Gate N1_norm: FAIL** (6.32 << 15 threshold).

Interval distribution for M_norm at N=60: all eigenvalues cluster in [0,50] (1573/3000) and [200,300] (50/3000), with none in [50,200]. The distribution shape is bimodal and wrong.

---

## Track W1 -- Weyl Density Target Formula

| Quantity | Value |
|---------|-------|
| Weyl N(T = gamma_100 = 236.5) | ~137 zeros |
| Phase 39 growth rate | 1/6 evals per unit N |
| **N required (Phase 39)** | **~820** |
| Max available N (16D sedenions) | 60 |
| M_norm growth rate (at N=60) | 0.105 evals/N |
| N required (M_norm) | ~1297 |

**Formula:** N_required = Weyl_N(T_target) / growth_rate_per_unit_N

**16D is fundamentally insufficient.** The maximum bilateral family in 16D sedenions has 60 vectors. Weyl density matching at T=gamma_100 requires ~820 vectors -- 13.7x more than available. Even if higher Cayley-Dickson dimensions could provide more bilateral vectors, the growth in bilateral pairs scales slowly with CD dimension.

---

## Summary Table

| Track | Gate | Result | Key Finding |
|-------|------|--------|-------------|
| **V1** | PASS | lambda_max=21.955 confirmed | Baseline matches Phase 39 exactly |
| **A1** | **FAIL** | rho=-0.084, p=0.41 | ||F||^2 not correlated with gamma_n; anti-corr is directional |
| **A2** | PASS | M_norm rho=+0.097; M_tilde rho=-0.025 | Phase 39 anti-corr was small-sample artifact (n=10) |
| **D1** | NULL | rho=-0.013 at N=60; median eval=0 | Evals concentrated near 0; shapes mismatched; M_tilde not PSD |
| **S1** | FAIL | max diag rho=+0.217 (p=0.13) | No bilateral vector has significant diagonal correlation |
| **N1_norm** | FAIL | All rhos near zero | Normalization doesn't improve spectral matching |
| **N2** | FAIL | 6.32 above gamma_1 at N=60 | Density still ~7x below Weyl target |
| **W1** | FAIL | N_required=820; max=60 | 16D sedenions fundamentally insufficient |

---

## Conclusions for Investigation Pause

### What Phase 40 Established

**The Phase 39 anti-correlation was a small-sample artifact.** rho~-0.4 at n=10 zeros, rho~-0.025 at n=100 zeros. The same pattern as k=15 (Phase 39 K1): strong correlation at n=10, near-zero at n=100.

**The eigenvalue distribution shape is wrong.** M_tilde(N=60) produces eigenvalues concentrated near zero (median~0) with large outliers. The Riemann zeros are distributed across [14, 236]. These shapes are incompatible regardless of scaling.

**M_tilde is not positive semidefinite.** Negative eigenvalues (-63 to -30 depending on normalization) appear structurally. This is a fundamental property of the norm² inner product that was not apparent from tracking only lambda_max.

**16D sedenions have an absolute density ceiling.** With 60 bilateral vectors maximum and a ~1/6 growth rate, Weyl matching at T=gamma_100 requires N~820. The 16D architecture is at least 13x short of what is needed.

### The Rank Constraint

The key structural insight from D1: at any given zero tₙ, F(tₙ) is a single 16D sedenion vector. The matrix M_tilde = [||P_i * (F * P_j)||^2] is built from this single vector. The effective information content is bounded by the dimension of sedenion space (16D), not by the number of basis vectors (60). This explains why ~half the 3000 eigenvalues are near zero: the 60x60 matrix has effective rank at most ~16 per zero.

### State at Pause (March 29, 2026)

The Srednicki N->inf scenario is viable structurally (Phase 39: lambda_max grows linearly, spans gamma range) but faces three obstacles that appear fundamental:

1. **Rank ceiling**: Effective rank ~16 per zero regardless of subspace dimension
2. **Density ceiling**: 60 max vectors vs ~820 needed for Weyl matching
3. **Distribution mismatch**: Eigenvalues concentrated near zero with outliers; zeros distributed continuously in [14, 236]

Phase 41 would need a fundamentally different construction -- either a genuinely different operator (not M_tilde), a different inner product that avoids rank collapse, or a transition to a larger algebraic structure.

---

## Output Files

| File | Track | Contents |
|------|-------|----------|
| `phase40_formula_verification.json` | V1 | Baseline eigenvalues, ||F||^2 at gamma_1 |
| `phase40_F_norm_vs_gamma.json` | A1 | ||F||^2 Spearman test (pre-flight FAIL) |
| `phase40_M_norm_baseline.json` | A2 | M_norm vs M_tilde at N=6, rho comparison |
| `phase40_full_eigenvalue_distribution.json` | D1 | Full 60x60 eigenvalue distribution, 50 zeros |
| `phase40_correlated_subspace.json` | S1 | Diagonal rho for all 60 vectors; top-k results |
| `phase40_M_norm_growing.json` | N1 | M_norm growing subspace 6->60 |
| `phase40_density_normalized.json` | N2 | Normalized density at N=60 |
| `phase40_weyl_density_target.json` | W1 | Required N formula for Weyl matching |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-28*
*"Better math, less suffering."*
