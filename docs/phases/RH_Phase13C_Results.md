# RH Phase 13C -- Act/GUE P2 Variance Ratio vs BK R_c: RESULTS

**Date:** 2026-03-09
**Status: COMPLETE -- NULL**
**Verdict: P2 VARIANCE RATIO HEIGHT-CONFOUNDED -- no BK oscillation detectable**

---

## Question

Does the Act/GUE P2-projection variance ratio per height band correlate with R_c(t)?

---

## Results

### 10-Band

| Band | t_mid | act_var | gue_var | Ratio | R_c (9p) |
|---|---|---|---|---|---|
| 0 | 716.8 | 0.0671 | 0.0849 | **0.790** | +0.38 |
| 1 | 1968 | 0.0216 | 0.0549 | 0.394 | +2.20 |
| 2 | 3025 | 0.0187 | 0.0441 | 0.423 | +0.19 |
| 3 | 4020 | 0.0172 | 0.0423 | 0.406 | +1.21 |
| 4 | 4978 | 0.0163 | 0.0385 | 0.423 | +0.31 |
| 5 | 5907 | 0.0155 | 0.0361 | 0.428 | -0.55 |
| 6 | 6816 | 0.0149 | 0.0349 | 0.427 | +0.68 |
| 7 | 7707 | 0.0144 | 0.0351 | 0.412 | -0.42 |
| 8 | 8584 | 0.0136 | 0.0315 | 0.433 | +0.67 |
| 9 | 9449 | 0.0139 | 0.0338 | 0.411 | -0.47 |

**Peak r = 0.412 (p=2 only). All 9-prime sets: r near 0. No significance crossing.**

### 20-Band: same conclusion, r ranges from -0.31 to +0.28.

---

## Diagnosis: Height Confound

The variance is driven by mean gap size, not BK oscillation:

```
act_var:  0.089 (band 0, t_mid=413) → 0.013 (band 19, t_mid=9664)   -- monotone decrease
gue_var:  0.114                     → 0.034                          -- monotone decrease
ratio:    0.78 (band 0) → 0.40 (bands 1-19, flat)                   -- one step, then flat
```

Band 0 is a structural outlier (low height, large gaps, high variance). After band 0,
the ratio converges to ~0.40-0.43 with small fluctuations -- not the oscillatory
pattern that R_c predicts.

The P2 projection value is P2(g1,g2) = -(g1^2 + g2^2)/(2(g1+g2)), which scales
quadratically with gap size. As height increases and mean gap shrinks from ~1.6 to ~0.86,
both act_var and gue_var shrink together, keeping the ratio nearly constant.
**R_c oscillates; variance ratio does not -- no correlation is possible.**

### Why the p=2-only r=0.41 appeared

With 10 bands, R_c(t, p=2 only) = (1/sqrt(2))*cos(log(2)*t) + 0.5*cos(2*log(2)*t).
This is a very slow oscillation (period ~9 in t) that looks quasi-random at 10 points.
The r=0.41 for p=2 only is consistent with noise at n=10.

---

## Phase 13 Summary: What Works for BK Detection

| Method | Phase | Result | Notes |
|---|---|---|---|
| Chavez conjugation symmetry delta per band | 12C | r=0.579 sub-threshold | CAILculator required |
| DFT power at log-prime frequencies | **13A** | **SNR 7-245x** | **DEFINITIVE** |
| Mean spacing ratio delta per band | 13B | r=0.28 null | Ordering-blind |
| P2 variance ratio per band | 13C | r~0 null | Height-confounded |

**The spectral approach (Phase 13A) is the correct test for BK prime-orbit structure.**
Band-level Pearson r is fundamentally limited:
- Only 10-20 data points against a noisy, multi-prime signal
- Within-band structure is destroyed by averaging
- Height confound dominates variance-based statistics

Phase 13A uses all 9,998 ratios with exact frequency targeting -- vastly more power.
The log-prime signal at SNR 100-245x in Phase 13A is the definitive BK result.

---

## Next Phase 13 Directions

**Phase 13D (proposed):** Per-band DFT SNR vs height
- Compute DFT power at top log-prime frequencies (p=7,11,13) within each height band
- Does SNR track R_c? This connects Phase 13A (spectral) and Phase 13C (BK correlation)
- 20 bands x DFT = 20-point correlation, better grounded than mean/variance

**Phase 14 (proposed):** 20-band Chavez symmetry handoff to Claude Desktop
- The right statistic (Chavez) at increased resolution (20 bands)
- Chavez symmetry delta is ordering-sensitive; established in Phases 6 and 12C
- With n=20 and threshold 0.444, significance is reachable if signal strength holds

---

## Files

| File | Purpose |
|---|---|
| `rh_phase13c_prep.py` | Analysis script |
| `p13c_results.json` | Full results JSON |
| `RH_Phase13C_Results.md` | This document |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
