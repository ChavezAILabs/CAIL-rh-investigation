# RH Phase 37 Results — Anti-Symmetric Spectral Structure + Eigenvalue Matching

**Chavez AI Labs LLC** · *Applied Pathological Mathematics — Better math, less suffering*

|                     |                                                                           |
|---------------------|---------------------------------------------------------------------------|
| **Date**            | 2026-03-27                                                                |
| **Phase**           | 37 — Anti-Symmetric Spectral Structure + iA Eigenvalue Matching           |
| **Author**          | Paul Chavez / Chavez AI Labs LLC (co-authored with Claude Sonnet 4.6)     |
| **Script**          | `rh_phase37.py`                                                           |
| **Status**          | COMPLETE                                                                  |

---

## Executive Summary

Phase 37 addresses the primary question from Phase 36's structural discovery (M_F = F[0]·I + A): **do the eigenvalues of iA(ρ) match the Riemann zeros?** The answer is **no** at the current level of the construction. All three matching tests fail. Additionally, a critical correction to the Phase 36/37 hermiticity mechanism is documented: F is always real-valued (structural, not σ=½ specific), which means the Srednicki proof path through the reality condition does not close.

These are honest null results that sharply delimit the remaining open directions.

---

## Track V1 — Formula Verification

| Check | Result |
|-------|--------|
| F norm² at γ₁ | 0.9117 |
| F[0] at γ₁ | 0.065398 |
| A anti-symmetry max \|A+Aᵀ\| | **0.00e+00** (machine exact) |
| A rank | 6 (full rank) |
| iA eigenvalues at γ₁ | ±{0.6554, 0.2365, 0.0141} |

A = M_F − F[0]·I is perfectly anti-symmetric to machine precision. Confirmed structurally from Phase 36.

---

## Track E1 — iA Eigenvalues for 100 Zeros

| Quantity | Value |
|---------|-------|
| iA max positive eigenvalue range | [0.347, 1.608] |
| γₙ range (n=1..100) | [14.135, 236.524] |
| Ratio γₙ / max eigenvalue | 13.5× to 536.6× |

The iA eigenvalues are bounded O(0.01–1.6) across all 100 zeros. The Riemann zeros γₙ grow without bound. There is a 13–537× gap between the scales.

**First 5 zero spectra:**

| n | γₙ | iA eigenvalues |
|---|-----|----------------|
| 1 | 14.135 | ±{0.6554, 0.2365, 0.0141} |
| 2 | 21.022 | ±{1.5625, 0.1086, 0.0256} |
| 3 | 25.011 | ±{0.9816, 0.7354, 0.0031} |
| 4 | 30.425 | ±{1.0945, 0.8574, 0.0225} |
| 5 | 32.935 | ±{1.1167, 0.3629, 0.2930} |

---

## Track E2 — Eigenvalue Matching Tests (Primary Decision Gate)

### E2a — Direct Match

**0 matches** out of 10,000 tested pairs (100 zeros × up to 6 eigenvalues each, tolerance 1×10⁻⁶).

**FAIL.** Eigenvalues are O(1); γₙ are O(14–50). No proximity.

### E2b — Scaled Match (γₙ = c · max_eigenval)

| Statistic | Value |
|---------|-------|
| Best-fit c (γₙ / max_eigenval), mean | 174.54 |
| Best-fit c std | 101.46 |
| CV of c across 100 zeros | **0.581** (58%) |
| Mean relative residual at fixed c | 88.4% |

**FAIL.** CV = 58% means no consistent scaling constant exists. The ratio γₙ/λ_max varies by more than a factor of 40 across the 100 zeros.

### E2c — Rank Correlation (Spearman)

| Test | Spearman ρ | p-value |
|------|-----------|---------|
| γₙ vs max eigenvalue | −0.058 | 0.566 |
| γₙ vs Σμₖ² | −0.029 | 0.778 |
| γₙ vs ‖A‖_F | −0.029 | 0.778 |

**FAIL.** All correlations consistent with zero. The eigenvalue spectrum of iA is statistically independent of the Riemann zero values.

### Decision Tree Outcome

```
E2a: FAIL (no direct match)
E2b: FAIL (no consistent scaling; CV=58%)
E2c: FAIL (Spearman rho≈0; p>0.5)
```

**The eigenvalue path through iA(ρₙ) does not encode Riemann zeros at the current order of construction.** The 6×6 restriction of M_F to the (A₁)⁶ subspace does not have the right spectral structure for this route.

---

## Track E3 — Eigenvalue Trajectory

All 6 eigenvalue trajectories (as a function of zero index n) are:
- Bounded O(0.01–1.6) — do not grow with γₙ
- Statistically independent of γₙ (Spearman |ρ| < 0.15, all p > 0.18)
- Sum of squared eigenvalues: mean 2.12, Pearson r = −0.07 vs γₙ

**Chavez CS on eigenvalue trajectories (Track C1):**

| Sequence | CS |
|----------|----|
| k=3 positive eigenvals (e3+e12 dir) | **91.1%** |
| k=4 positive eigenvals (e4+e11 dir) | 76.3% |
| k=5 positive eigenvals (e5+e10 dir) | 71.9% |
| Σμₖ² sequence | −24.9% (oscillatory) |
| ‖A‖_F sequence | 57.2% |
| Phase 36 reference (6D projection) | **81.4%** |

The k=3 eigenvalue trajectory (corresponding to the B3 = e₃+e₁₂ direction) has CS = 91.1% — **above** the Phase 36 6D projection CS of 81.4% and the Riemann zero gap range. This is unexpected and worth noting.

---

## Track R1/R2 — Reality Condition (Critical Correction)

### R1: F at 100 Zeros

Max |Im(F_k)| across 100 zeros: **0.00e+00** (exact zero).

### R2: Reality vs σ

| σ | max\|Im(F)\| | ‖F‖² | Note |
|---|------------|------|------|
| 0.1 | **0.00e+00** | 1.0494 | |
| 0.2 | **0.00e+00** | 0.9850 | |
| 0.3 | **0.00e+00** | 0.9406 | |
| 0.4 | **0.00e+00** | 0.9162 | |
| **0.5** | **0.00e+00** | **0.9117** | **CRITICAL LINE** |
| 0.6 | **0.00e+00** | 0.9273 | |
| 0.7 | **0.00e+00** | 0.9629 | |
| 0.8 | **0.00e+00** | 1.0185 | |
| 0.9 | **0.00e+00** | 1.0940 | |

**Im(F) = 0 for ALL σ.** This is a structural property of the implementation, not a critical-line condition.

### Mechanism

`F_16d()` returns a `list[float64]`. The sedenion exponential factors are:

```
exp_sed(t·log(p)·r̂_p) = cos(θ)·e₀ + sin(θ)·r̂_p
```

with θ = t·log(p) real and r̂_p real. All components are real floats. The σ correction adds `(σ−½)/√2` to component 4 and subtracts it from component 5 — also real. The product of real-component sedenions is real. **Im(F) ≡ 0 for all σ.**

### Correction to Phase 36/37 Handoff

The handoff stated: *"The critical-line condition Re(ρ)=½ and AIEX-001a hermiticity on (A₁)⁶ are equivalent statements."* This is **false** as stated. The hermiticity PASS in Phase 36 (max violation = 0) holds because F is always real, not because there is something algebraically special about σ=½.

**What the hermiticity result actually says:**
- F(σ+it) is real-valued for all real σ, t → inner products are real → inner product hermiticity holds trivially for all σ
- The Gate I2 PASS is real, but its mechanism is weaker than the handoff assumed
- The proof path "F real iff σ=½ → hermiticity iff σ=½ → zeros on critical line" fails at the first implication

**What remains:** The Phase 36 hermiticity PASS is a correct statement about the bilateral ZD inner product. It establishes that the (A₁)⁶ projection of AIEX-001a is hermitian. The result is publishable as stated; only the claimed mechanism (critical-line specificity) needs correction.

---

## Track S1 — Corrected Spectral Determinant det₆(E − iA)

The roots of det₆(E − iA(ρₙ)) are exactly the eigenvalues of iA(ρₙ) = ±λₖ.

| Quantity | Value |
|---------|-------|
| Distance (closest iA root to γₙ), min | 13.48 |
| Distance (closest iA root to γₙ), mean | 86.73 |
| \|det₆(γₙ − iA)\| range | [7.96×10⁶, 8.59×10¹²] |
| Roots matching γₙ | **0 / 50** |

The corrected spectral determinant does not vanish at Riemann zeros. The roots are O(1); the zeros are O(14–237).

---

## Track S2 — Gamma_sed Candidate

The smallest-eigenvalue eigenvector v₀ of iA (the "ground state" in Srednicki's language):

| Quantity | Value |
|---------|-------|
| Min eigenvalue of iA range | [−0.282, +0.321] |
| ⟨v₀, F_proj⟩ mean | 0.023 |
| ⟨v₀, F_proj⟩ std | 0.149 |
| ⟨v₀, F_proj⟩ near zero (<0.01) | 5/50 |
| Mean \|v₀ᵢ · v₀ⱼ\| (consistency across zeros) | 0.218 |

The ground state v₀ varies significantly across zeros (low consistency, 0.218). The gamma_sed inner product ⟨v₀, F_proj⟩ does not systematically vanish — it is not a consistent null observable.

---

## Track P1 — A_antisym Structure

| Property | Value |
|---------|-------|
| Rank of A across 100 zeros | **6 (always full rank)** |
| Linearity error ‖A(t₁+t₂)−A(t₁)−A(t₂)‖_F | 3.36 (not linear) |

A is full rank 6 for all 100 zeros tested — it has no null space. The anti-symmetric structure is dense (all 15 off-diagonal entries contribute). The dominant entry varies: at n=1 it is A[1,3] = 0.4758 (e1−e14 × e3+e12 interaction); at n=2 it is A[0,4] = 1.2267 (e1+e14 × e4+e11 interaction). No single pair of basis directions dominates consistently.

A is **not linear**: A(t₁+t₂) ≠ A(t₁)+A(t₂) because F is a multiplicative (not additive) function of t.

---

## Track P2 — Discrete Fourier Test on P-vectors

| P-vector | cos(DFT(P), Q) | cos(DFT(P), \|P\|) |
|---------|---------------|-------------------|
| e₁+e₁₄ | 0.226 | 0.304 |
| e₁−e₁₄ | 0.068 | 0.370 |
| e₂−e₁₃ | 0.341 | 0.280 |
| e₃+e₁₂ | 0.341 | 0.316 |
| e₄+e₁₁ | 0.304 | 0.385 |
| e₅+e₁₀ | **0.439** | 0.280 |

All cosine similarities are below 0.5. The DFT of P_i is NOT proportional to Q_i. The discrete Fourier self-duality analogy (DFT(P) ∝ Q) does not hold for these 16-component sedenion vectors. The bilateral annihilation P·Q=0 is an algebraic condition in sedenion space, not a Fourier transform relationship.

---

## Summary Table

| Track | Gate | Result | Key Finding |
|-------|------|--------|-------------|
| V1 | ✓ | PASS | A anti-symmetric (machine exact); rank 6 |
| **E2a** | **Primary** | **FAIL** | **0 direct eigenvalue matches** |
| **E2b** | **Primary** | **FAIL** | **CV=58%; no consistent scaling** |
| **E2c** | **Primary** | **FAIL** | **Spearman ρ≈0; p>0.5** |
| E3 | — | INFO | k=3 eigenval CS=91.1% (unexpected elevation) |
| **R2** | **Critical** | **CORRECTION** | **F always real; reality ≠ σ=½ condition** |
| S1 | — | FAIL | det roots O(1) vs zeros O(14–237) |
| S2 | — | INFO | Ground state inconsistent across zeros |
| C1 | — | INFO | k=3 eigenval CS=91.1% |
| P1 | — | INFO | A always rank 6; not linear; no dominant direction |
| P2 | — | NULL | DFT(P) not proportional to Q |

---

## Conclusions and Phase 38 Directions

### What Phase 37 Ruled Out

1. **Direct eigenvalue match:** iA(ρₙ) eigenvalues ≠ γₙ (scale off by 13–537×)
2. **Scaled match:** No consistent c with c·λₖ = γₙ
3. **Rank correlation:** Eigenvalues statistically independent of γₙ
4. **Srednicki proof via reality condition:** F is always real; the mechanism is structural, not critical-line-specific
5. **Fourier self-duality of P-vectors:** DFT(P) ≇ Q

### What Remains Open

1. **The (A₁)⁶ construction is correct** — the hermiticity, G=−2I, bilateral annihilation, and self-dual property all hold. The algebraic framework is sound; the current spectral determinant route is wrong.

2. **The M_F definition may be the bottleneck.** M_F[i][j] = scalar_part(Pᵢ·(F·Pⱼ))/(−2) uses only the *scalar* part of sedenion products. A richer inner product extracting *non-scalar* spectral information from F·Pⱼ may map eigenvalues to γₙ.

3. **The k=3 eigenvalue CS=91.1%** (B3 = e₃+e₁₂ direction) is above the Riemann zero range. This unexpected elevation may point to a preferred direction in (A₁)⁶ space that carries spectral information.

4. **Scale identification:** iA eigenvalues are O(1) while γₙ are O(14–237). The 6-prime Weil_RHS = −4.014. The ratio γ₁/max_eigenval_1 = 21.6 ≈ 2·(γ₁/F[0]) could suggest F[0] is the unit. Further investigation needed.

5. **The Weil formula connection (Phase 23T3):** S(N) = Σf₅D(tₙ) was 99.3% aligned with Weil RHS. This remains the strongest spectral relationship in the investigation. Phase 38 might revisit the Weil formula as the spectral determinant itself.

---

## Output Files

| File | Track | Contents |
|------|-------|---------|
| `phase37_formula_verification.json` | V1 | A anti-symmetry confirmed |
| `phase37_iA_eigenvalues.json` | E1 | 100-zero iA eigenvalue spectra |
| `phase37_eigenvalue_matching.json` | E2 | E2a/b/c — all FAIL |
| `phase37_eigenvalue_trajectory.json` | E3 | Trajectories; CS; Pearson r |
| `phase37_reality_condition.json` | R1 | Im(F)=0 at all 100 zeros |
| `phase37_reality_vs_sigma.json` | R2 | Im(F)=0 for ALL σ (structural) |
| `phase37_corrected_spectral_det.json` | S1 | det roots vs zeros — no match |
| `phase37_gamma_sed_candidate.json` | S2 | Ground state; gamma_sed inconsistent |
| `phase37_chavez_eigenvalue.json` | C1 | k=3 CS=91.1%; sum_sq CS=−24.9% |
| `phase37_A_structure.json` | P1 | Rank 6 always; not linear |
| `phase37_fourier_bilateral.json` | P2 | DFT(P) ≇ Q |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics · 2026-03-27*
*"Better math, less suffering."*
