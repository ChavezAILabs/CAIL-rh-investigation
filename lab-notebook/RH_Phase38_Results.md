# RH Phase 38 Results -- Richer Inner Product + Scale + Weil Formula Revisit

**Chavez AI Labs LLC** · *Applied Pathological Mathematics -- Better math, less suffering*

|                     |                                                                              |
|---------------------|------------------------------------------------------------------------------|
| **Date**            | 2026-03-27                                                                   |
| **Phase**           | 38 -- Richer M~_F + Scale Investigation + Weil Spectral + Reality Proof      |
| **Author**          | Paul Chavez / Chavez AI Labs LLC (co-authored with Claude Sonnet 4.6)        |
| **Script**          | `rh_phase38.py`                                                              |
| **Status**          | COMPLETE                                                                     |

---

## Executive Summary

Phase 38 addresses the four open directions from Phase 37. The primary finding is a **partial success on Gate M1**: replacing the scalar projection with a full sedenion norm brings eigenvalues from O(0.01-1.6) up to O(18-60) -- inside the low-gamma range. The scale problem is solved. However, the correlation problem (Spearman rho near 0, CV=0.50) persists. All other gates are null or negative. The most important structural result is Track A1: Im(F)=0 is proven universal (algebraic property of Cayley-Dickson, not E8-specific), definitively closing the reality-condition proof path.

---

## Track V1 -- Formula Verification

| Quantity | Value |
|---------|-------|
| F[0] at gamma_1 | 0.065397 |
| max \|A+A^T\| | 0.00e+00 |
| iA eigenvalues at gamma_1 | {-0.6554, -0.2365, -0.0141, +0.0141, +0.2365, +0.6554} |
| F[0]/lambda_max at gamma_1 | 0.0998 (~1/10, not ~1/2) |

Baseline confirmed. Note: the handoff's conjecture "lambda_max ~ F[0]/2" is already falsified at gamma_1 (ratio is ~1/10, not 1/2).

---

## Track M1 -- Three Richer M~_F Definitions (PRIMARY)

### Gate M1: Scale Check

| Definition | lambda_max range (50 zeros) | gamma range | CV | Spearman rho | p |
|-----------|---------------------------|-------------|-----|-------------|---|
| Scalar (Phase 37) | [0.35, 1.61] | [14.1, 143.1] | 0.58 | -0.058 | 0.57 |
| **Full norm^2** | **[18.6, 59.6]** | [14.1, 143.1] | 0.503 | -0.062 | 0.67 |
| **Non-scalar norm** | **[18.0, 59.0]** | [14.1, 143.1] | 0.505 | -0.023 | 0.87 |
| Best single component (k=12) | [1.28, 3.30] | [14.1, 143.1] | 0.419 | +0.225 | -- |

**Gate M1: PARTIAL PASS.** The full norm^2 and non-scalar norm definitions bring eigenvalues into the O(14-60) range -- overlapping the lower portion of the gamma range. This is a 10-30x scale improvement over Phase 37.

**However:** CV = 0.50 (same order as Phase 37's 0.58) and Spearman rho ~ 0. The eigenvalues are now at the right scale but remain statistically independent of the gamma values. The scale problem is solved; the spectral correlation problem is not.

### Single Component Scan (k=1..15)

All 15 non-scalar components give CV ~ 0.42-0.52 and |rho| < 0.24. No single component discriminates. Best component k=12 (e12 direction): CV=0.419, rho=0.225. Component k=15 shows highest Spearman in M2 diagonal analysis (rho=0.588, n=10).

### Decision Tree

```
Gate M1 (scale): PARTIAL PASS -- eigenvalues now O(18-60), overlapping low-gamma range
Gate M1 (correlation): FAIL -- Spearman rho~0, CV~0.50; no spectral matching
Decision: richer inner product solves scale; correlation requires different approach
Phase 39 direction: why does norm^2 give right scale? Is there a normalization that gives correlation?
```

---

## Track M2 -- Non-Scalar Component Structure

For 10 zeros, all 36 (i,j) product vectors Pᵢ·(F·Pⱼ) were computed in full 16D.

### Component Variance (summed over all 36 pairs)

All 16 components (k=0..15) have roughly equal total variance (range: 8.84-11.13). The scalar component k=0 is NOT dominant -- it is mid-range (10.46). Non-scalar components are not suppressed.

Top 5 non-scalar components by variance: **k=1, k=14, k=6, k=9, k=15**

Note: k=1 and k=14 are tied (both variance=11.13); k=6 and k=9 are tied (both 10.87). These mirror the (A1)^6 basis symmetry (e1+e14, e6+e9 directions appear in Phase 18E root geometry).

### Diagonal Correlation with gamma (n=10)

| Component | Spearman rho |
|-----------|-------------|
| k=15 | **+0.588** (highest) |
| k=6, k=9 | +0.188, -0.042 |
| k=1, k=14 | +0.152, +0.127 |
| k=0 (scalar) | -- (not tested; this is the Phase 36 M_F) |

Component k=15 shows elevated diagonal correlation with gamma (rho=0.588 at n=10, but n=10 is small). Worth examining in Phase 39.

**Finding:** All components carry comparable information. The scalar projection (Phase 36 M_F) is not uniquely poor -- it is representative of a uniformly distributed spectral content across all 16 components. The bottleneck is not WHICH component is used but HOW spectral content is aggregated.

---

## Track S1 -- F[0]/lambda_max Ratio (Scale Relationship)

| Statistic | Value |
|---------|-------|
| F[0]/lambda_max mean | -0.0359 |
| F[0]/lambda_max std | 0.3745 |
| CV | **10.44** |
| Theorem candidate (CV < 0.1)? | **NO** |
| Spearman(F[0], lambda_max) | -0.165, p=0.100 |
| Spearman(ratio, gamma_n) | +0.127, p=0.207 |

**Gate S1: FAIL.** The ratio F[0]/lambda_max is not structurally bounded. It changes sign across zeros (F[0] is sometimes negative), rendering the ~1/10 observation at gamma_1 a coincidence. The conjecture "lambda_max ~ F[0]/2" was falsified even at the baseline (ratio is 0.0998, not 0.5).

First 5 ratios: [0.0998, -0.2352, -0.1779, +0.3241, -0.0044]. No convergence pattern.

---

## Track S2 -- gamma from M_F Combinations

All tested combinations of F[0] and lambda_max give R² < 0 (worse than predicting the mean):

| Formula | Best-fit c | R² |
|---------|-----------|-----|
| gamma ~ c * F[0] | -40.92 | -5.22 |
| gamma ~ c * lambda_max | +145.47 | -0.49 |
| gamma ~ c * (F[0]+lambda_max) | +142.85 | -0.68 |
| gamma ~ c * F[0]^2/lambda_max | +362.04 | -3.90 |
| gamma ~ c * F[0]*lambda_max | -54.11 | -5.22 |
| gamma ~ c / lambda_max | +104.83 | **-0.33** (best) |

**All FAIL.** The best fit (c/lambda_max) explains negative variance. Neither F[0] nor lambda_max nor their combinations carry gamma information. The M_F scalar matrix is spectrally blind to the Riemann zeros at all tested combinations.

---

## Track E1 -- e3+e12 Preferred Direction

The Phase 37 k=3 eigenvalue CS=91.1% was on the **sorted iA eigenvalue trajectory**. This track tests whether B3=e3+e12 is special in the column norm of F*P_j.

### Column Norm² CS across 100 zeros

| Column j | Basis vector | CS(||F*Pj||^2) | CS(scalar part) |
|---------|-------------|----------------|-----------------|
| 0 | e1+e14 | **+0.154** (max) | 0.573 |
| 1 | e1-e14 | -0.958 | 0.598 |
| 2 | e2-e13 | +0.027 | 0.738 |
| **3** | **e3+e12 (B3)** | **-0.811** | 0.551 |
| 4 | e4+e11 | -0.103 | 0.690 |
| 5 | e5+e10 (q2) | +0.027 | 0.613 |

**B3 is NOT the highest CS direction for column norms.** The maximum CS is at e1+e14 (0.154), but all column CS values are low (range -0.958 to +0.154). The B3 direction column shows NEGATIVE CS (-0.811).

The Phase 37 k=3 CS=91.1% was an artifact of the eigenvalue SORTING (eigenvalues of iA are sorted by magnitude; the k=3 position after sorting has a specific role in the spectrum). It is not a property of the e3+e12 sedenion direction itself.

Spearman(B3 column norm, gamma): rho=-0.085, p=0.40 -- no correlation.
Spearman(B5/q2 column norm, gamma): rho=-0.051, p=0.62 -- no correlation.

**Conclusion:** The B3=e3+e12 elevation is not a geometric property of that direction in the product space. It was a sorting artifact in the eigenvalue trajectory. Direction 2 of Phase 38 is CLOSED.

---

## Track W1 -- Weil Formula Spectral Revisit

### S(N)/Weil_RHS Convergence

| N | S(N) | S(N)/Weil_RHS |
|---|------|--------------|
| 10 | -17.70 | 4.41 |
| 20 | -29.65 | 7.39 |
| 50 | -56.77 | 14.14 |
| 100 | -99.52 | 24.79 |
| 200 | -168.38 | 41.95 |
| 500 | -347.91 | **86.67** |

**Gate W1: FAIL.** S(N)/Weil_RHS grows without bound (approximately linearly with N). It does NOT converge to 1.

### Clarification of Phase 23T3 "99.3% Alignment"

The Phase 23T3 result was a **conjugation symmetry measurement** on the ratio sequence, not convergence of the absolute ratio to 1. The CS of the ratio sequence at Phase 23T3 was measured on the oscillatory structure of the ratio around its mean -- this is a different question from whether the ratio approaches 1.

The Weil formula convergence interpretation (left-side sum approaching the prime sum) does NOT hold with f5D(t) as the test function. This is consistent with Phase 24T1's finding that f5D is not Schwartz-class and the windowed Weil sum diverges formally.

Spearman(f5D(tn), gamma_n): rho=+0.286, p=0.004 -- mild positive correlation (first hint of signal).

---

## Track W2 -- f5D vs gamma; Spectral Determinant det5D

| Fit | R² |
|----|-----|
| f5D ~ c * gamma | -0.52 |
| f5D ~ c * log(gamma) | -0.13 |

**No monotone relationship** between f5D(tn) and gamma_n. f5D ranges from -2.64 to +0.73 (mostly negative: 90/100 values negative), while gamma grows from 14 to 237. f5D is an oscillating function, not a monotone proxy for gamma.

### det5D(E) = ∏(E - f5D(tn))

| E | log\|det5D(E)\| | min\|E - f5D\| |
|---|----------------|----------------|
| Weil_RHS = -4.014 | 106.77 | 1.376 (far) |
| 0 | **-29.70** | **0.011 (near zero!)** |
| 0.5 * Weil_RHS | -18.67 | 0.032 |
| 2 * Weil_RHS | 194.44 | 5.390 |

The spectral determinant det5D(E) has a root near E=0 (min|E-f5D|=0.011 -- one of the 100 f5D values is near 0). E=Weil_RHS is NOT a root (min distance 1.376). The f5D values cluster near 0 by coincidence of the oscillation, not by spectral structure.

**Gate W1 partial check:** det5D(Weil_RHS) is large (log=106.77) -- Weil_RHS is NOT a root of the spectral determinant.

CS of f5D(tn) sequence (n=1..100): 0.103 -- consistent with an oscillating sequence with no conjugation structure.

---

## Track A1 -- Reality Characterization (Critical Closure)

### Test: 20 random 16D unit vector sets as r_p

| Trial | max |Im(F)| |
|-------|------------|
| All 20 | **0.000000e+00** |

**Im(F) = 0 for ALL 20 random root sets.** The reality of F is universal -- it holds for ANY real-valued r_p vectors, regardless of E8 geometry.

### Mechanism (Theorem)

The sedenion exponential factor is:
```
exp_sed(theta * r_hat) = cos(theta) * e0 + sin(theta) * r_hat
```
with theta = t*log(p) real and r_hat a real-component 16D vector. The product of any number of real-component sedenions under Cayley-Dickson multiplication is always real-component (the recursion c1 = a1*b1 - conj(b2)*a2, c2 = b2*a1 + a2*conj(b1) preserves real-component inputs). This is a property of the algebra structure, not of E8 or any particular root direction.

**Theorem (Phase 38):** For any set of real-valued r_p vectors and any real t and sigma, F_16d(t, sigma) has Im(F_k) = 0 for all k. The reality condition is universally satisfied by all real-input AIEX-001a constructions.

**Consequence:** The proof path "F real iff sigma=1/2 -> hermiticity iff sigma=1/2 -> zeros on critical line" fails at the FIRST implication for any choice of r_p, not just the E8 choice. The hermiticity PASS is structurally trivial for the entire class of real-input sedenion operators, not just AIEX-001a.

---

## Summary Table

| Track | Gate | Result | Key Finding |
|-------|------|--------|-------------|
| V1 | -- | PASS | Baseline confirmed; F[0]/lambda_max ~ 1/10 at gamma_1 |
| **M1** | **PRIMARY** | **PARTIAL PASS** | **Full norm^2: lambda_max [18-60] overlaps gamma range (scale solved); CV=0.50, rho~0 (correlation not solved)** |
| M2 | -- | INFO | All 16 components equal-variance; k=15 highest diagonal rho=0.588 (n=10) |
| S1 | -- | FAIL | F[0]/lambda_max CV=10.4, sign-changing; not a theorem |
| S2 | -- | FAIL | All gamma combinations: R^2 < 0 |
| E1 | -- | CLOSED | B3 elevation was eigenvalue-sort artifact, not a geometric property |
| W1 | -- | FAIL | S(N)/Weil_RHS grows to 86.7 at N=500; does NOT converge to 1 |
| W2 | -- | FAIL | f5D not monotone in gamma; det5D(Weil_RHS) not near zero |
| **A1** | **CRITICAL** | **THEOREM** | **Im(F)=0 universal for all real r_p; algebraic property of Cayley-Dickson** |

---

## Conclusions and Phase 39 Directions

### What Phase 38 Established

1. **Scale problem SOLVED by norm^2 definition.** M~_F[i][j] = ||Pi*(F*Pj)||^2 gives eigenvalues in [18-60], overlapping the low-gamma range. This is a 10-30x improvement over scalar M_F (Phase 37's [0.35-1.61]). The scalar projection was discarding norm information, not just spectral structure.

2. **Correlation problem UNSOLVED.** All richer definitions give CV~0.50 and Spearman rho~0. The eigenvalues are at the right scale but statistically independent of gamma values. The M_F matrix approach at the current basis size (6x6) does not encode Riemann zeros regardless of inner product definition.

3. **B3 elevation was a sort artifact.** The Phase 37 CS=91.1% on the k=3 eigenvalue trajectory was a property of eigenvalue sorting (middle eigenvalue of anti-symmetric matrix), not a property of the e3+e12 sedenion direction. Direction 2 is closed.

4. **S(N)/Weil_RHS diverges.** The Weil formula sum does not converge to the prime sum via f5D. The Phase 23T3 99.3% was a CS measurement, not absolute convergence. Direction 4 (Weil as spectral determinant) requires a different test function.

5. **Im(F)=0 is algebraically universal (Theorem).** Proven for 20 random root sets. The Cayley-Dickson recursion preserves real-component inputs. This closes the reality-condition proof path definitively and universally.

### Open Directions for Phase 39

1. **Why does norm^2 give the right scale?** M~_F[i][j] = ||Pi*(F*Pj)||^2 gives eigenvalues O(18-60). Is this a coincidence of the normalization, or is there a representation-theoretic reason? The norm^2 of a sedenion product is related to the sedenion norm (||a*b||^2 = ||a||^2 * ||b||^2 for alternative algebras). Since ||Pi||^2 = 2 and ||Pj||^2 = 2, and ||F||^2 varies in O(0.9-1.1), we get M~[i][j] <= ||Pi||^2 * ||F||^2 * ||Pj||^2 = 4 * ||F||^2 ~ 4. But the actual eigenvalues are O(20-60), larger than this bound. **The norm^2 matrix is NOT just ||Pi||^2 * ||F||^2 * ||Pj||^2 -- it contains cross-terms from the full sedenion product structure.** This cross-term structure is the spectral content.

2. **k=15 diagonal correlation (rho=0.588, n=10).** Component k=15 = e15 direction. In the sedenion structure, e15 is the last basis element. Its elevated diagonal correlation should be verified at n=100.

3. **Normalization: divide norm^2 by ||Pi||^2 * ||Pj||^2 * ||F||^2?** If the norm^2 definition is divided by the product of individual norms, the quotient would be bounded in [0,1] and might isolate the directional spectral content. This is a cosine-similarity variant of the inner product.

4. **The fundamental question:** The 6x6 matrix approach restricts to 6 eigenvalues. The Riemann zeros are countably infinite. Even if one eigenvalue matched one zero, the finite matrix cannot represent the full spectrum. Phase 39 might investigate whether there is a limiting procedure (N -> infinity analogous to the Gram matrix G5 growing) that recovers zeros.

---

## Output Files

| File | Track | Contents |
|------|-------|----------|
| `phase38_formula_verification.json` | V1 | Baseline checks |
| `phase38_richer_MF.json` | M1 | Full norm^2, non-scalar norm, component scan |
| `phase38_nonscalar_structure.json` | M2 | 16D product component analysis |
| `phase38_scale_relationship.json` | S1 | F[0]/lambda_max across 100 zeros |
| `phase38_gamma_from_MF.json` | S2 | gamma combination fits |
| `phase38_b3_analysis.json` | E1 | B3 column analysis -- elevation not confirmed |
| `phase38_weil_spectral.json` | W1 | S(N)/Weil_RHS diverges |
| `phase38_f5d_gamma.json` | W2 | f5D oscillates; no monotone gamma relationship |
| `phase38_reality_characterization.json` | A1 | Im(F)=0 universal theorem |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*"Better math, less suffering."*
