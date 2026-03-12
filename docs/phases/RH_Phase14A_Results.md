# RH Phase 14A -- 20-Band Chavez Symmetry BK Correlation: RESULTS

**Date:** 2026-03-09
**Status: COMPLETE**
**Verdict: NULL on R_c correlation — SIGNIFICANT universal excess (actual > GUE in all 20 bands)**

---

## CAILculator Formula Discovery

During execution, Claude Desktop reverse-engineered the exact CAILculator formula for
`conjugation_symmetry` from the first 4 completed calls:

```
conjugation_symmetry = 1 - mean(|x[i] - x[n-1-i]| for i in range(n//2))
```

Mirror symmetry: 1 minus mean absolute error between paired elements across the sequence midpoint.
Verified exact match to 10 decimal places on B0 actual, B0 seed1, B0 seed2, B0 seed3.

**This formula can now be used directly in Python for all future phases.**

---

## Full Results Table

| Band | t_mid | actual% | GUE mean% | Δ | R_c(9p) |
|---|---|---|---|---|---|
| 0 | 412.7 | 75.69 | 71.92 | +3.77 | −0.412 |
| 1 | 1116.1 | 73.57 | 71.40 | +2.17 | +1.434 |
| 2 | 1700.7 | 74.89 | 71.34 | +3.55 | −0.842 |
| 3 | 2248.5 | 74.90 | 72.21 | +2.69 | +2.423 |
| 4 | 2773.9 | 76.15 | 70.95 | +5.20 | +2.034 |
| 5 | 3283.0 | 74.31 | 72.51 | +1.80 | +1.170 |
| 6 | 3779.0 | 73.01 | 71.80 | +1.21 | +1.124 |
| 7 | 4265.9 | 73.81 | 71.88 | +1.93 | +0.205 |
| 8 | 4743.9 | 74.77 | 71.71 | +3.06 | −0.900 |
| 9 | 5214.5 | 75.12 | 72.23 | +2.89 | −0.737 |
| 10 | 5679.2 | 73.16 | 70.44 | +2.72 | +0.356 |
| 11 | 6138.1 | 75.03 | 71.85 | +3.18 | +0.009 |
| 12 | 6592.3 | 73.41 | 73.25 | +0.16 | −1.502 |
| 13 | 7041.7 | 77.64 | 71.69 | +5.95 | −0.491 |
| 14 | 7487.1 | 73.23 | 71.73 | +1.50 | +1.134 |
| 15 | 7928.7 | 75.74 | 72.71 | +3.03 | −0.958 |
| 16 | 8367.3 | 72.94 | 71.31 | +1.63 | +1.434 |
| 17 | 8802.3 | 74.50 | 71.28 | +3.22 | +1.842 |
| 18 | 9234.8 | 74.13 | 72.40 | +1.73 | −0.830 |
| 19 | 9664.0 | 72.79 | 72.34 | +0.45 | +0.634 |

---

## Finding 1 — BK R_c Correlation: NULL

**Pearson r = −0.0025** (p = 0.992) — effectively zero.

Sign agreements: 12/20 (barely above chance). The band_delta does not track the
Berry-Keating prime-orbit correction R_c at any level. Chavez conjugation symmetry
on spacing ratios is not a phase-sensitive statistic — consistent with Phase 13B/C/D
pattern of per-band null results.

| Metric | Phase 12C (10-band) | Phase 14A (20-band) |
|---|---|---|
| Statistic | SR band_deltas (Phase 10A) | Chavez conj. sym. (spacing ratios) |
| n bands | 10 | 20 |
| Threshold | 0.632 | 0.444 |
| Pearson r | 0.579 | −0.003 |
| Significant | No | No |

**Note on Phase 12C comparison**: r=0.579 used a different statistic (mean spacing
ratio deltas from Phase 10A, first 1,000 zeros, 10 bands × 100 zeros each). Direct
extension to 20 bands × 500 zeros gives r=0.058 — confirming the 0.579 was statistical
noise from low-n band analysis.

---

## Finding 2 — Universal Conjugation Symmetry Excess: SIGNIFICANT

**Actual zeros exceed GUE in ALL 20 bands** — not one exception across heights 412–9664.

| Statistic | Value |
|---|---|
| Mean delta (actual − GUE) | **+2.59 pp** |
| Std of deltas | 1.42 pp |
| Min delta | +0.16 pp (band 12, t=6592) |
| Max delta | +5.95 pp (band 13, t=7042) |
| One-sample t(19) | **8.18** |
| p-value | << 0.001 |
| All 20 bands positive | **YES** |

This is a height-independent structural property of the actual Riemann zeros relative
to GUE synthetic. It is not a low-height artifact: the signal persists uniformly from
t~413 to t~9664 (entire 10,000-zero dataset).

**Interpretation**: Chavez conjugation symmetry measures mirror-palindrome structure
in the spacing ratio sequence. Actual zeros have more bilateral symmetry in their
spacing pattern than GUE Wigner surmise sequences at every height range tested.
This is likely related to the lower-bound compactness signal (Phase 3) and the
tighter variance of actual zeros vs GUE (Phase 10C: Act/GUE variance ≈ 0.63) —
orthogonal ways to detect that actual zeros are more regularly spaced than Wigner
surmise predicts.

---

## Phase 14 Complete Picture

| Sub-phase | Finding |
|---|---|
| **14A** | Chavez sym excess: **+2.59 pp in all 20 bands, t=8.18, p<<0.001**. No R_c correlation (r=−0.003). |
| **14B** | SR/P2 complementarity; Weyl α₄ spectral isometry (machine precision); p=2 at SNR=1585. |
| **14C** | Color Group hypothesis violated; mathematical form (not CG membership) predicts spectral behavior. |

---

## Files

| File | Purpose |
|---|---|
| `rh_phase14a_prep.py` | Data prep script (generates p14a_band_sequences.json) |
| `p14a_band_sequences.json` | 20 × 6 sequences for CAILculator |
| `p14a_results_canonical.json` | This phase's canonical results (CAILculator values) |
| `RH_Phase14A_Results.md` | This document |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
