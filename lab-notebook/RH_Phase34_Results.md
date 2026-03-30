# Phase 34 Results — RH Investigation
**Chavez AI Labs LLC | Applied Pathological Mathematics**
*Paul Chavez | 2026-03-27*
*GitHub: [CAIL-rh-investigation](https://github.com/ChavezAILabs/CAIL-rh-investigation)*

---

## Overview

Phase 34 tested the c₁ asymptote hypothesis (AIEX-116) at N_zeros up to 10,000 and characterized the full 2D (N_primes, N_zeros) Weil ratio surface.

**Primary finding: AIEX-116 is REFUTED.**

The 6-prime Weil ratio does not converge to c₁ as N_zeros → ∞. It crosses below c₁ near N_zeros≈4900 and continues declining. The Phase 33 fit (N_zeros ≤ 1000) was extrapolating too far — the 1/√N model with c∞≈c₁ does not hold beyond N_zeros=1000. All asymptote fits give c∞ well below c₁ (0.058–0.087), or zero (power law).

**c₁ is a crossing point in N_zeros, just as it is in N_primes (Phase 32 and Phase 33).**

---

## Track V1 — Formula Verification

All 5 checks PASS. dps=15 zeros from `rh_zeros_10k.json` match dps=25 ratios to machine precision (diff=0.00 at all N_zeros tested). Phase 34 uses `rh_zeros_10k.json` for all N_zeros > 1000.

---

## Track E1 — 6-Prime c₁ Asymptote Test (PRIMARY)

**Finding: AIEX-116 REFUTED. The 6-prime ratio crosses c₁ at N_zeros≈4900 and continues declining.**

| N_zeros | Ratio    | vs c₁     |
|---------|----------|-----------|
| 1000    | 0.152656 | +0.034678 |
| 2000    | 0.135405 | +0.017427 |
| 3000    | 0.127180 | +0.009202 |
| **5000**    | **0.117545** | **−0.000433** |
| 7500    | 0.111105 | −0.006873 |
| 10000   | 0.106783 | −0.011195 |

The ratio crosses below c₁ between N_zeros=3000 (ratio=0.127) and N_zeros=5000 (ratio=0.118). Exact crossing: approximately **N_zeros≈4960** (linear interpolation).

### Model Fits

| Model | Parameters | R² | c∞ | |c∞ − c₁| |
|-------|-----------|-----|-----|----------|
| Power law (a·N^(−b)) | a=0.441, b=0.155 | 0.9979 | 0 (decays) | — |
| 1/√N + c∞ | A=2.112, c∞=0.0871 | 0.9948 | 0.0871 | 0.0309 |
| Power+offset (A·N^(−b)+c∞) | A=0.685, b=0.286, c∞=0.0577 | 0.9999 | 0.0577 | 0.0603 |
| Log-decay | a=−0.0197 | 0.9905 | — | — |

**Decision gate NOT MET** for any model. The best-fit c∞ values (0.058–0.087) are 25–50% below c₁=0.118. The power+offset model (R²=0.9999) is the best overall fit and gives c∞=0.058 — barely above zero.

### Diagnosis of Phase 33 Error

Phase 33 fit the 1/√N model to N_zeros ∈ {50,100,200,300,500,750,1000} and obtained c∞=0.1197≈c₁. This was an extrapolation artifact: the 1/√N model is not the true functional form, and the curvature only becomes visible at N_zeros > 1000. The power law (pure decay to 0) describes the full range N=50→10,000 better than any finite-asymptote model.

**The c₁ asymptote hypothesis is refuted. The 6-prime Weil ratio decays toward 0 (or a value well below c₁) as N_zeros → ∞.**

---

## Track E2 — 36-prime and 62-prime Asymptote Comparison

Both prime sets also show continued decline through N_zeros=10,000 with no convergence toward c₁.

**36 primes (p_max=151):**

| N_zeros | Ratio    | vs c₁     |
|---------|----------|-----------|
| 1000    | 0.123487 | +0.005509 |
| 2000    | 0.109863 | −0.008115 |
| 5000    | 0.096023 | −0.021955 |
| 10000   | 0.087249 | −0.030729 |

c∞ (1/√N model) = 0.072 (vs c₁=0.118); c∞ (power+offset) = 0.048. Both well below c₁.

**62 primes (p_max=300):**

| N_zeros | Ratio    | vs c₁     |
|---------|----------|-----------|
| 1000    | 0.107197 | −0.010781 |
| 2000    | 0.096559 | −0.021419 |
| 5000    | 0.084818 | −0.033160 |
| 10000   | 0.077220 | −0.040758 |

c∞ (power+offset) = 0.029. Already well below c₁ throughout the scan.

**Conclusion:** All three prime sets show monotone decline through N_zeros=10,000 with no finite asymptote near c₁. The ratio decays toward zero (or a small positive value) in all cases. c₁ is a crossing point in N_zeros as well as N_primes.

---

## Track S1 — Surface Characterization: a(N_p) and b(N_p)

Full table of power-law parameters ratio(N_p, N_z) ≈ a(N_p) · N_z^(−b(N_p)):

| N_primes | p_max | N=100  | N=200  | N=500  | N=1000 | a      | b      | R²     |
|----------|-------|--------|--------|--------|--------|--------|--------|--------|
| 6        | 13    | 0.2479 | 0.2097 | 0.1733 | 0.1527 | 0.6461 | 0.2103 | 0.9968 |
| 15       | 47    | 0.2216 | 0.1943 | 0.1629 | 0.1443 | 0.5243 | 0.1873 | 0.9997 |
| 36       | 151   | 0.1736 | 0.1581 | 0.1364 | 0.1235 | 0.3474 | 0.1498 | 0.9987 |
| 62       | 300   | 0.1424 | 0.1303 | 0.1181 | 0.1072 | 0.2488 | 0.1212 | 0.9978 |
| 95       | 499   | 0.1157 | 0.1099 | 0.1027 | 0.0947 | 0.1718 | 0.0848 | 0.9882 |
| 168      | 1000  | 0.0889 | 0.0858 | 0.0825 | 0.0779 | 0.1151 | 0.0553 | 0.9804 |

Phase 33 values (6p, 36p, 62p) confirmed by recomputation. Three new prime sets added.

### Functional Form of a(N_p)

| Model | R² | Formula |
|-------|----|---------|
| **Log-decay** | **0.9925** | −0.1679·log(N_p) + 0.9549 |
| 1/√N_p | 0.9428 | 1.6202/√N_p + 0.0345 |
| Power law | 0.9069 | 1.957·N_p^(−0.525) |

Best: **log-decay** (R²=0.9925). a(N_p) ≈ −0.168·log(N_p) + 0.955.

### Functional Form of b(N_p)

| Model | R² | Formula |
|-------|----|---------|
| **Log-decay** | **0.9668** | −0.0475·log(N_p) + 0.3082 |
| 1/√N_p | 0.8421 | 0.4391/√N_p + 0.0514 |
| Power law | 0.8330 | 0.502·N_p^(−0.387) |

Best: **log-decay** (R²=0.9668). b(N_p) ≈ −0.0475·log(N_p) + 0.308.

### b ∝ 1/log(N_p)? — NOT confirmed

The ratio b·log(N_p) is not constant: 0.377 (6p), 0.507 (15p), 0.537 (36p), 0.500 (62p), 0.386 (95p), 0.284 (168p). The hypothesis from the Phase 35 Preview (b ∝ 1/log N_p giving a doubly-indexed surface) does not hold. The log-decay model is better, but not cleanly proportional.

---

## Track S2 — Surface Reconstruction and Residuals

Using power-law fits a(N_p)=1.957·N_p^(−0.525) and b(N_p)=0.502·N_p^(−0.387):

| Max |residual| | Mean |residual| | Median |residual| |
|---------------|----------------|----------------|
| 0.0176 | 0.0055 | 0.0046 |

The largest residuals occur at small N_p (6p, 15p) and large N_zeros. The power-law surface model is an adequate approximation (mean error 0.5%) but not exact — log-decay in N_p would reduce residuals.

**Systematic pattern:** The power-law surface model **over-predicts** for small N_p (6p, 15p) and **under-predicts** for large N_p (95p, 168p). This is consistent with a(N_p) being better described by log-decay than by power law.

---

## Track B1 — b(N_p) Weyl Equidistribution Probe

### Discrepancy of {log p mod 2π} for each prime set

| N_primes | D*_N   | L² disc | |Weil_RHS| | log(pmax) | b      |
|----------|--------|---------|-----------|-----------|--------|
| 6        | 0.5918 | 0.5405  | 4.014     | 2.565     | 0.2103 |
| 15       | 0.3872 | 0.6396  | 9.581     | 3.850     | 0.1873 |
| 36       | 0.2859 | 0.7862  | 19.397    | 5.017     | 0.1498 |
| 62       | 0.3975 | 0.8945  | 28.848    | 5.680     | 0.1212 |
| 95       | 0.4805 | 0.9861  | 38.761    | 6.213     | 0.0848 |
| 168      | 0.3118 | 0.9284  | 56.574    | 6.905     | 0.0553 |

### Correlations with b

| Predictor | R² | Flag |
|-----------|-----|------|
| **\|Weil_RHS\|** | **0.9755** | *** R²>0.95 — strongest |
| **log(N_p)** | **0.9668** | *** R²>0.95 |
| **log(pmax)** | **0.9557** | *** R²>0.95 |
| 1/√N_p | 0.8421 | |
| L² discrepancy | 0.8867 | |
| D*_N | 0.2025 | (weak — non-monotone) |

**Key finding: b correlates most strongly with |Weil_RHS| (R²=0.976).**

The star discrepancy D*_N does NOT correlate well with b (R²=0.20) — the Weyl equidistribution hypothesis in its simplest form (b ∝ D*_N) is not supported. However, |Weil_RHS| = Σ log(p)/√p is essentially the weighted count of prime frequencies — as more primes are added, |Weil_RHS| grows and b decreases. The physical interpretation: prime sets with more total frequency content (larger Σ log(p)/√p) require more zeros to cancel, and thus decay more slowly.

**Phase 35 implication:** The rate of cancellation of the BK trace as N_zeros → ∞ is governed by the total weight Σ log(p)/√p, not by the geometric distribution of {log p mod 2π}. The decay law may follow from a weighted Weyl sum rather than classical discrepancy.

---

## Track P1 — c₁ Euler Product Probe

One candidate within 0.005 of c₁=0.11798:

| Expression | Value | \|val − c₁\| |
|-----------|-------|------------|
| D/C = [Σ log(p)/p^(3/2)] / [Σ (log p)²/√p] | 0.11496 | 0.00301 |

Where: D = Σ_{p≤13} log(p)/p^(3/2) = 0.8260, C = Σ_{p≤13} (log p)²/√p = 7.1845.

**Assessment:** D/C = 0.115 is within 0.003 of c₁=0.118 — close but not exact (2.5% discrepancy). No combination of the natural Euler product sums {W, A, B, C, D, E, F, G, Mertens} reproduces c₁ to better than 0.003. The c₁ constant does not appear to have a simple closed-form expression in terms of 6-prime Euler product sums.

Given that AIEX-116 has been refuted (c₁ is not the asymptote), the motivating question for P1 is weakened. The D/C coincidence may be numerical, not structural.

---

## Track P2 — Weil Truncation Fraction

Ratios of 6-prime to larger BK traces at N_zeros=500:

| N_primes | p_max | Ratio (N=500) | ratio/ratio_48p |
|----------|-------|---------------|----------------|
| 6        | 13    | 0.173349      | 1.363          |
| 12       | 37    | 0.167002      | 1.313          |
| 24       | 89    | 0.150856      | 1.186          |
| 48       | 223   | 0.127227      | 1.000          |

ratio(6p)/ratio(48p) = **1.363** — significantly larger than 1.

The ratio(6p)/ratio(48p) is NOT c₁ or c₁². At N_zeros=500, the 6-prime BK trace actually yields a **higher** Weil ratio than the 48-prime set — because the Weil_RHS denominator grows faster than the mean trace numerator as primes are added. The "truncation fraction" interpretation breaks down: adding primes reduces both numerator and denominator, but the ratio declines because the denominator grows faster.

**The ratio(6p) is not a c₁-fraction of ratio(48p) at any fixed N_zeros tested.**

---

## Summary of Phase 34 Findings

| Finding | Status | Impact |
|---------|--------|--------|
| AIEX-116: c∞(6 primes) = c₁ | **REFUTED** | c₁ is NOT the 6-prime N_zeros→∞ asymptote |
| 6-prime ratio crosses c₁ at N_zeros≈4960 | **NEW** | c₁ is a crossing point in N_zeros too |
| All prime sets decline past c₁ as N_zeros→∞ | **CONFIRMED** | Ratio → 0 (or ≪c₁) in all cases |
| Power law best single-variable model | **CONFIRMED** | R²≈0.999 for N_zeros range 100→10000 |
| a(N_p) follows log-decay in N_p | **NEW** | Best model R²=0.993 |
| b(N_p) follows log-decay in N_p | **NEW** | Best model R²=0.967 |
| b ∝ 1/log(N_p) — NOT confirmed | **NEW** | b·log(N_p) not constant |
| b correlates with \|Weil_RHS\| (R²=0.976) | **NEW** | Strongest predictor; governs decay rate |
| D/C ≈ c₁ to 0.003 | **NEW — WEAK** | Only near-match in Euler probe; not exact |
| Weil truncation ratio ≠ c₁ | **CONFIRMED** | ratio(6p)/ratio(48p)=1.36 at N=500 |

### The c₁ Geometry — Revised Picture

c₁ = sin(θ_W) = 0.11798 locates a **crossing level** on the full (N_primes, N_zeros) surface:
- **In N_primes** (fixed N_zeros=500): ratio crosses c₁ at p_max≈306 (Phase 32)
- **In N_zeros** (fixed N_primes=6): ratio crosses c₁ at N_zeros≈4960 (Phase 34)
- **On the surface**: c₁ marks a diagonal level curve in (log N_primes, log N_zeros) space

The ratio does NOT converge to c₁ — it crosses through c₁ from above and continues declining toward zero (or a much smaller positive value). c₁ marks a threshold on the surface, not an asymptote.

### Implications for the Sedenion Horizon Conjecture

The Sedenion Horizon Conjecture (Phase 29) claimed the Weil ratio converges to c₁. Phase 32 showed c₁ is a crossing point in N_primes. Phase 34 confirms this in N_zeros as well. The conjecture as stated is not supported by any data in the range tested (N_zeros up to 10,000, N_primes up to 168).

**What c₁ IS:** A constant that appears naturally in the ZDTP 64D structure (Phase 31) and marks a specific level on the Weil ratio surface. Its geometric/algebraic role is not the asymptote of the ratio.

### Implications for the Paper (April 1)

1. Remove the Sedenion Horizon Conjecture from the abstract (or demote to "c₁ appears as a crossing-level constant")
2. Do not add the Phase 33 footnote about c∞≈c₁ — Phase 34 refutes it
3. **Add:** c₁ marks a diagonal level curve on the full (N_primes, N_zeros) surface — N_zeros-crossing near N≈5000 for 6-prime set

---

## Reproducibility

**Script:** `rh_phase34.py`
**Zero source:** `rh_zeros.json` (1000 zeros, dps=25) and `rh_zeros_10k.json` (10000 zeros, dps=15)
**Runtime:** ~3 minutes

**Outputs:**
- `phase34_formula_verification.json` — V1/E0 checks
- `phase34_c1_asymptote_test.json` — E1 6-prime extended scan
- `phase34_asymptote_comparison.json` — E2 36/62-prime scans
- `phase34_surface_parameters.json` — S1 a(N_p), b(N_p) fits
- `phase34_surface_residuals.json` — S2 reconstructed surface
- `phase34_b_predictor_analysis.json` — B1 discrepancy analysis
- `phase34_c1_euler_probe.json` — P1 Euler product candidates
- `phase34_weil_truncation.json` — P2 truncation fractions

```bash
pip install numpy scipy
python rh_phase34.py
```

---

## Citation

Chavez, P. (2026). *Phase 34: c₁ Asymptote Test + 2D Surface Fit — RH Investigation.*
Chavez AI Labs LLC. GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation

---

*Chavez AI Labs LLC — Applied Pathological Mathematics: Better math, less suffering.*
