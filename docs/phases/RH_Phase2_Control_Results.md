# RH Phase 2 — ZDTP Discriminability Control Test: Results
**Experiment ID:** RH_CTRL_2026_001  
**Date:** 2026-03-04  
**Researcher:** Paul Chavez, Chavez AI Labs

---

## Summary Table

| Sequence | ZDTP Score | Chavez Sym. | S1 Lead? | Notes |
|---|---|---|---|---|
| **Actual Riemann zeros** | **98.69%** | **60.1%** | ✅ Yes (629.6) | From rh_zeros.json, first 16 |
| Control A: Growth + 10% noise | 97.52% | 66.7% | ❌ No (S2 leads: 322.2) | Sub-range: peaks at ~33 not 67 |
| Control B: Poisson gaps | 98.81% | 68.1% | ❌ No (S3B/S4 lead: 358.0) | Compressed range, slow spread |
| Control C: Uniform linear | 98.84% | 57.9% | ✅ Yes (587.2) | Perfectly spaced, same range |

---

## Finding 1: ZDTP Does Not Discriminate

**Verdict: ZDTP convergence is NOT a discriminating metric for Riemann-specific structure at n=16.**

All four sequences score in the narrow band 97.5–98.8%. The range is only 1.3 percentage points across actual zeros and all three controls. This is well within noise — not a significant difference.

The handoff document set the threshold at "more than 2–3 percentage points above the highest control." The actual zeros score **98.69%** while Control C (uniform, fully deterministic) scores **98.84%** — the uniform sequence scores *higher* than the actual zeros.

**Interpretation:** At n=16, ZDTP convergence is measuring the norm (magnitude) and general smoothness of the vector, not Riemann-specific structure. Any monotone sequence in this range will score ~98%. The Phase 1 result of 98.7% was a range/monotonicity artifact.

---

## Finding 2: Gateway Ordering — One Discriminating Signal

While overall convergence scores are indistinguishable, **gateway ordering is different**:

| Sequence | Leading Gateway | 2nd | Pattern |
|---|---|---|---|
| Actual zeros | **S1** (629.6) | S2 (623.8) | Monotone descent S1→S5 |
| Control A (noise) | **S2** (322.2) | S1 (315.2) | S2 > S1, irregular |
| Control B (Poisson) | **S3B/S4** (358.0) | S2 (357.6) | S3B=S4 lead, flat top |
| Control C (uniform) | **S1** (587.2) | S2 (584.1) | Monotone descent, matches zeros pattern |

The actual zeros and Control C (uniform) both show the same S1→S2→S3A→S3B=S4→S5 monotone descent pattern. Controls A and B show disrupted ordering. This suggests **gateway ordering pattern = S1 monotone descent is sensitive to smooth, regularly-spaced growth** — which both actual zeros and uniform spacing have. The noise (A) and stochastic gaps (B) disrupt this pattern.

**This is a weak discriminating signal:** It distinguishes smooth from noisy sequences, not Riemann from non-Riemann.

---

## Finding 3: Chavez Symmetry Also Does Not Discriminate (at n=16)

All four Chavez symmetry scores cluster in 57.9–68.1%:
- Actual zeros: **60.1%** — *lowest* of the group
- Control B (Poisson): **68.1%** — highest
- Control A (growth+noise): **66.7%**
- Control C (uniform): **57.9%**

Interestingly, the actual Riemann zeros score *lower* on conjugation symmetry than all three controls at n=16. The noisy and Poisson sequences score higher. This is the opposite of what discrimination would require.

Note: The Phase 1 result of 83.8% was on **gaps** (99 data points). This n=16 test runs on **raw positions** (16 points). The n=16 sample is too small for meaningful Chavez analysis; conjugation symmetry requires sufficient points to establish the bilateral structure. This is a sample-size limitation, not a structural one.

---

## Methodological Conclusions

### What Phase 2 Reveals About Phase 1

1. **The 98.7% ZDTP result is a baseline property**, not a Riemann-specific signal. Any monotone sequence of 16 positive values will achieve ~98% ZDTP convergence at these magnitudes. The metric is appropriate for detecting structural *transitions* (regime detection) but not for characterizing the algebraic structure of a specific 16-element sequence.

2. **The meaningful Phase 1 results are in the gap analysis** — specifically, the Chavez conjugation symmetry of 83.8% on 99 gaps. That measurement survives because it uses a large enough n and operates on gap differences (which remove the monotone growth artifact).

3. **Gateway ordering (S1 monotone descent)** is a real pattern shared by actual zeros and uniform spacing, and disrupted by noise and Poisson gaps. This may reflect the *smoothness* of zero growth relative to the uniform baseline, but it is not Riemann-specific.

---

## Revised Hierarchy Table

```
METRIC: Chavez Conjugation Symmetry (gaps, n≥99)
─────────────────────────────────────────────────
Deterministic (Powers of 2, Fibonacci)    ~96–98%
Sophie Germain primes (gaps)               88.5%
Riemann zero gaps                          83.8%   ← Confirmed Phase 1
General primes / structured sequences    ~78–84%
─────────────────────────────────────────────────
Random baseline                             0.0%

METRIC: ZDTP Convergence (n=16 positions)
─────────────────────────────────────────────────
ALL monotone sequences in range [14, 67]  ~97–99%  ← Non-discriminating
─────────────────────────────────────────────────
```

---

## Phase 2 Decision Point (from Handoff Document)

The handoff document specified:

> **If Controls A and C also reach ~98.7%:** ZDTP is detecting monotone growth, not zero-specific structure. The Phase 1 result is a range/growth artifact. Phase 2 needs to be reframed.

**Controls B and C both exceeded 98.7%.** The Phase 2 reframe is triggered.

---

## Reframed Phase 2 Direction

### What to Test Instead

The gap-based Chavez analysis (83.8%) is the real signal. To test whether *that* signal is discriminating:

1. **Shuffle test:** Take the actual 99 gaps, shuffle them randomly, and re-run Chavez. If symmetry drops significantly from 83.8%, the ordering of the gaps (not just the gap distribution) carries structure. This is the correct Phase 2 discriminability test.

2. **Synthetic gap sequences at n=99:** Generate 99 Poisson-distributed gaps with mean 1.41 and run Chavez symmetry. Compare to actual zero gaps at 83.8%.

3. **Scale invariance check (Phase 1 spec):** Run Chavez on first 100 zeros' gaps, first 500, all 999. Does 83.8% hold across scales? Scale stability would be a strong discriminating signal.

The annihilation topology work (AT-1/AT-2) can proceed in parallel — it is independent of whether ZDTP convergence at n=16 is discriminating.

---

## Immediate Next Steps

- [ ] Run shuffle test on actual zero gaps (discriminability of gap ordering)
- [ ] Run Chavez on 99 Poisson gaps (same mean) — does 83.8% hold for random gaps?
- [ ] Scale invariance: Chavez symmetry at n=100, n=500, n=999 gaps
- [ ] Proceed with AT-1 literature check: Biss-Dugger-Isaksen
- [ ] Update CLAUDE.md: ZDTP convergence at n=16 is not a discriminating metric
