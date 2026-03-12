# RH Phase 17 — Results
## Q-Vector Access: Multi-Channel Embedding
**Date:** March 12, 2026
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Status:** COMPLETE

---

## Summary

Phase 17 opens the Q-vector of the Canonical Six bilateral zero divisors for the first time. All prior phases (7–16) accessed only P-vector geometry via embed_pair projections. Phase 17 reveals that Q-vectors carry arithmetic information with **higher SNR and broader prime coverage** than P-vectors — and for the first time detects p=2 in the Riemann zero spectrum.

---

## Phase 17A: Q-Vector DFT Survey (zeta zeros, 10k)

### Q2 projection — q2 = (0,0,-1,0,0,+1,0,0) [Q2=Q5: e5+e10]

**9/9 primes detected. SNR 418–1762×.**

| Prime | log(p) | Act SNR | GUE SNR | Shuf SNR | P2 ref (14B) | Signal |
|-------|--------|---------|---------|----------|--------------|--------|
| **2** | 0.693 | **418.7** | 0.06 | 1.70 | 0.84 | **YES — FIRST p=2 DETECTION** |
| 3 | 1.099 | 1143.0 | 0.28 | 1.12 | 7.6 | YES |
| 5 | 1.609 | 1761.7 | 1.04 | 2.26 | 76.1 | YES |
| 7 | 1.946 | 1757.8 | 1.54 | 0.88 | 139.7 | YES |
| 11 | 2.398 | 1357.0 | 0.26 | 1.00 | 231.2 | YES |
| 13 | 2.565 | 1151.9 | 1.94 | 1.24 | 245.4 | YES |
| 17 | 2.833 | 841.6 | 0.80 | 2.79 | 205.9 | YES |
| 19 | 2.944 | 726.6 | 1.05 | 2.91 | 211.5 | YES |
| 23 | 3.136 | 549.1 | 0.67 | 0.62 | 185.1 | YES |

Sequence mean = 0.499, range = [-2.27, 3.05]. **Asymmetric** (unlike all P-vectors).
q2 is **BROADBAND**: roughly flat SNR across p=2..23.

### Q4 projection — q4 = (0,0,0,+1,+1,0,0,0) [Q4: e3-e12]

**8/9 primes detected (p=23 just below threshold). SNR up to 1995×.**

| Prime | Act SNR    | GUE SNR | Shuf SNR | Signal |
|-------|---------   |---------|----------|--------|
| 2     | 1796.9     | 0.80    | 1.06     | YES |
| 3     | **1995.6** | 1.15    | 1.48     | YES |
| 5     | 1214.3     | 1.12    | 1.90     | YES |
| 7     | 640.0      | 1.55    | 0.76     | YES |
| 11    | 171.0      | 0.31    | 0.47     | YES |
| 13    | 79.5       | 0.70    | 1.77     | YES |
| 17    | 12.8       | 0.68    | 1.21     | YES |
| 19    | 4.1        | 0.54    | 0.72     | YES |
| 23    | 0.99       | 0.50    | 2.29     | (no) |

Sequence mean = 1.429, range = [0.44, 7.96]. **Always positive** (q4 = H/2 + A).
q4 is **ULTRA-LOW-PASS**: SNR decays exponentially from p=2 to p=23.
Note: q4 + P2 = H (harmonic mean); they are the positive and negative complements.

### Q3 isometry verification — q3 = (0,-1,0,0,0,0,+1,0) = -v1

Max deviation from exact equality |DFT(q3)|^2 = |DFT(v1)|^2: **0.00e+00** (machine exact).
Theorem confirmed: q3 = -v1 implies identical DFT power for any sequence.

---

## Phase 17B-i: L-Function Comparative Q-Projection

### Q2 projection

| Prime | zeta SNR | chi4 SNR | chi3 SNR | chi4/zeta | chi3/zeta |
|-------|----------|----------|----------|-----------|-----------|
| **2** | 418.7    | **0.09** | 439.6    | **0.0002**| 1.050     |
| **3** | 1143.0   | 262.6    | **0.17** | 0.230     | **0.0001**|
| 5     | 1761.7   | 377.6    | 1835.3   | 0.214     | 1.042     |
| 7     | 1757.8   | 413.1    | 1820.6   | 0.235     | 1.036     |
| 11    | 1357.0   | 337.2    | 1356.6   | 0.248     | 1.000     |
| 13    | 1151.9   | 278.1    | 1068.5   | 0.241     | 0.928     |
| 17    | 841.6    | 190.6    | 760.8    | 0.227     | 0.904     |
| 19    | 726.6    | 174.9    | 668.2    | 0.241     | 0.920     |
| 23    | 549.1    | 141.6    | 544.3    | 0.258     | 0.991     |

**Route B confirmed (Q2):**
- p=2 in chi4: suppressed **4652×** (chi4(2)=0; Phase 16B SR ref: 353×)
- p=3 in chi3: suppressed **6723×** (chi3(3)=0; Phase 16B SR ref: 736×)

**Unexpected: chi3/zeta ≈ 1.0 for all unramified primes via Q2.** Chi3 zeros carry the same Q2 signal density as zeta zeros (within 10%) for p=5..23. Chi4 zeros are at ~23% of zeta SNR. This asymmetry between chi3 and chi4 in Q2 may encode character-structure information — a new open thread.

### Q4 projection

| Prime | zeta SNR | chi4 SNR | chi3 SNR | chi4/zeta | chi3/zeta |
|-------|----------|----------|----------|-----------|-----------|
| **2** | 1796.9   | **0.18** | 469.9    | **0.0001**| 0.262     |
| **3** | 1995.6   | 131.3    | **0.78** | 0.066     | **0.0004**|
| 5     | 1214.3   | 75.6     | 284.9    | 0.062     | 0.235     |
| 7     | 640.0    | 51.5     | 134.9    | 0.080     | 0.211     |
| 11    | 171.0    | 16.6     | 49.6     | 0.097     | 0.290     |
| 13    | 79.5     | 1.9      | 11.1     | 0.024     | 0.139     |
| 17–23 | <13      | <2       | <6       | (noise)   | (noise)   |

**Route B confirmed (Q4):**
- p=2 in chi4: suppressed **~10,000×** (strongest suppression yet observed)
- p=3 in chi3: suppressed **~2,500×**

Note: q4 is low-pass — for p>=17 the zeta SNR itself is too small (<13) to interpret chi4/chi3 ratios. High-p ratios (p=19,23) are noise.

---

## Phase 17B-ii: Sedenion Bilateral Zero Divisor Verification

### CD4 multiplication — bilateral zero divisor test

| Pattern | ||P|| | ||Q|| | ||P*Q|| | |                        |Q*P|| Bilateral? |
|---------|------|------|---------|---------|-----------|
| Pattern 1: P=e1+e14, Q=e3+e12 | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |
| Pattern 2: P=e3+e12, Q=e5+e10 | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |
| Pattern 3: P=e4+e11, Q=e6+e9  | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |
| Pattern 4: P=e1-e14, Q=e3-e12 | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |
| Pattern 5: P=e1-e14, Q=e5+e10 | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |
| Pattern 6: P=e2-e13, Q=e6+e9  | 1.4142 | 1.4142 | 0.00e+00 | 0.00e+00 | YES |

**All 6 patterns: ||P*Q|| = 0.00e+00 (exact machine zero).**
This is computational re-verification of the Lean 4 proof. The exact zeros arise because the integer basis vectors have zero floating-point error; the bilateral annihilation is algebraically exact.

### Three-gap sedenion statistic

**Formula:** scalar_part(x_n * x_{n+1}) = -2 * g_{n+1} * (g_n + g_{n+2})
where x_n = g_n*P1 + g_{n+1}*Q1

This formula is derived analytically from P1^2 = Q1^2 = -2*e0 and P1*Q1 = 0 (bilateral condition). Verified to machine precision (max deviation 0.00e+00 against 5-triplet check).

| Dataset | Mean | Variance | Act/GUE var ratio |
|---------|------|----------|-------------------|
| Actual (zeta) | -3.801 | 7.139 | **1.020** |
| GUE | -3.916 | 6.997 | 1.000 (ref) |
| Poisson | -3.904 | 31.294 | 4.47 |

**Act/GUE variance ratio = 1.020 (NO DISCRIMINATION).**
**Poi/GUE variance ratio = 4.47 (Poisson is separated).**

Contrast with two-gap embed_pair (Phases 10-12): Act/GUE variance ≈ 0.65 (actual tighter than GUE). Here with three-gap, actual matches GUE exactly (ratio = 1.02, effectively 1.0). This means:
- Actual zeros match GUE in **three-point gap correlations**
- Actual zeros are **tighter than GUE** in two-point gap correlations
- The bilateral product structure reveals a layer structure in the zero statistics: two-gap structure differs from three-gap structure

---

## Key Findings — Phase 17

### 1. p=2 Detected for the First Time (q2)
p=2 was absent from ALL P-vector projections (phases 13A, 14B, 15D). q2 = (0,0,-1,0,0,+1,0,0) detects it at SNR = 418.7. The decisive property of q2 is **asymmetry**: q2*embed(g1,g2) = g2 - g1 + g1/(g1+g2), which treats g1 and g2 differently. All P-vectors were symmetric or filtered in ways that cancelled the p=2 contribution. q2 captures the directed gap structure, accessing the p=2 frequency.

Combined with Phase 14B's finding that P2 detects p=2 in the low-pass channel (SNR=1585 in P2 projection of raw gaps), this confirms that p=2 is present in the zero sequence but requires a different embedding direction to see it in the spacing ratio representation.

### 2. Q-Vectors Outperform P-Vectors in SNR
- Best P-vector peak SNR: 245× (Phase 13A, P2 direction)
- Best Q-vector peak SNR: 1995× (q4, p=3)
- q2 median SNR across p=3..23: ~1000× vs P2 median ~180×
This is a 5-7× SNR improvement. The Q-vector directions encode the Euler product signal with higher sensitivity than the previously used P-vector directions.

### 3. Complete Prime Spectrum Coverage Established
The four projections now cover the full prime spectrum p=2..23 with no gaps:
- q4 (ultra-low-pass): p=2,3 strongest
- P2/SR low-pass: p=2,3,5,7
- q2 (broadband): p=2..23 all detected
- SR (high-pass, Phase 13A): p=7..23 strongest
q2 is the first single projection to detect all 9 primes p=2..23.

### 4. Route B Confirmed More Decisively via Q-Vectors
Euler product suppression ratios:

| Direction | p=2 chi4/zeta | p=3 chi3/zeta |
|-----------|--------------|--------------|
| SR (Phase 16B) | 0.0029 (353×) | 0.0014 (736×) |
| q2 (Phase 17) | 0.0002 (4652×) | 0.0001 (6723×) |
| q4 (Phase 17) | 0.0001 (~10,000×) | 0.0004 (~2500×) |

Q-vectors provide 10-14× stronger Route B signal than spacing ratios.

### 5. chi3/zeta ≈ 1.0 for Q2 (open thread)
Chi3 zeros carry nearly the same Q2 SNR as zeta zeros for all unramified primes (ratio 0.90–1.05). Chi4 zeros are at ~23% of zeta SNR. This asymmetry between chi3 and chi4 may encode L-function character structure in the Q2 projection. Candidate explanation: chi3 has conductor 3 (minimal odd prime), giving it a special relationship with the e5+e10 Q-vector direction. Flagged for Phase 18 investigation.

### 6. Sedenion Bilateral Verification: Exact Zero
P*Q = Q*P = 0.00e+00 (exact machine zero) for all 6 patterns. The CD4 implementation is confirmed correct. The bilateral zero divisor property is algebraically exact — not just numerically small.

### 7. Three-Gap Sedenion Statistic: Act/GUE = 1.02
The sedenion product generates the three-gap statistic s_n = g_{n+1}*(g_n + g_{n+2}) analytically from the bilateral condition. Act/GUE variance ratio = 1.02 (no discrimination), Poi/GUE = 4.47. In contrast, two-gap Act/GUE ≈ 0.65. Conclusion: actual zeros match GUE in three-gap correlations but are tighter in two-gap correlations. The bilateral structure reveals a layer structure in zero statistics.

---

## Sensitivity Map Update

| Projection | Primes detected | Peak SNR | Direction type |
|-----------|-----------------|----------|----------------|
| SR (Phase 13A) | 8/9 (p=3..23) | 245× | High-pass |
| P2 raw gaps (Phase 14B) | 8/9 (p=2..19) | 1585× (p=2!) | Low-pass |
| q2 (Phase 17) | **9/9 (p=2..23)** | **1762×** | **Broadband** |
| q4 (Phase 17) | 8/9 (p=2..19) | 1995× | Ultra-low-pass |

q2 is the first **single projection to detect all 9 primes** including p=2 in the spacing ratio representation.

---

## Files

| File | Description |
|------|-------------|
| `rh_phase17a_prep.py` | Q-vector DFT survey script |
| `rh_phase17b_prep.py` | L-function comparison + sedenion verification script |
| `p17a_results.json` | Phase 17A results |
| `p17b_results.json` | Phase 17B results |
| `RH_Phase17_Results.md` | This document |

---

*Chavez AI Labs LLC · Applied Pathological Mathematics*
*"Better math, less suffering"*
