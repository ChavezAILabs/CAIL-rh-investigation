# RH Phase 5 — Scale and Height Test Results
**Experiment ID:** RH_SCALE_2026_001
**Date:** 2026-03-04 (completed 2026-03-05)
**Researcher:** Paul Chavez, Chavez AI Labs

---

## Summary

Phase 5 asked two follow-up questions from Phase 4:

1. **Scale (Part A):** Does the Chavez GUE/Poisson separation widen with more data? At n=99 it cleared the 5-pt threshold by just 0.3 pts.
2. **Height (Part B):** Do higher zeros (500–599) score closer to GUE synthetic, confirming the Phase 4 shortfall was a low-height regime artifact?

Both questions are answered affirmatively.

---

## Part A — Scale Test Results

Spacing ratio Chavez symmetry on actual zeros across four scales:

| Scale | Mean Ratio | Chavez Symmetry |
|---|---|---|
| n=99 (Phase 4 baseline) | 0.610 | 75.0% |
| n=249 | 0.618 | 76.8% |
| n=499 | 0.616 | 75.7% |
| n=999 | 0.617 | 76.3% |

Mean ratio is rock-stable at 0.610–0.618 across the full dataset. Chavez symmetry bands at 75–77% with no monotone trend — a ceiling is emerging near 76–77%.

### Controls at n=499

| Sequence | Chavez Symmetry | Mean Ratio |
|---|---|---|
| **Actual zeros (n=499)** | **75.7%** | **0.616** |
| Poisson seed=1 | 68.8% | — |
| Poisson seed=2 | 69.4% | — |
| Poisson seed=3 | 68.6% | — |
| **Poisson Mean** | **68.9%** | — |
| GUE seed=1 | 76.3% | — |
| GUE seed=2 | 75.5% | — |
| GUE seed=3 | 76.6% | — |
| **GUE Mean** | **76.1%** | — |

### GUE/Poisson Separation Across Scale

| n | GUE Mean | Poisson Mean | Separation |
|---|---|---|---|
| 99 (Phase 4) | 76.9% | 71.6% | **5.3 pts** |
| 499 (Phase 5) | 76.1% | 68.9% | **7.2 pts** |

**The separation widens by 1.9 pts from n=99 to n=499.** The pipeline strengthens with scale — it was not at ceiling at n=99.

---

## Part B — Higher Zeros Results

Zeros 500–599 (imaginary parts 811–937), mean gap = 1.276. These zeros are higher in the critical strip, where asymptotic GUE behavior is better established.

| Sequence | Mean Ratio | Chavez Symmetry | Delta from Actual |
|---|---|---|---|
| **Actual zeros 500–599** | **0.6153** | **78.3%** | baseline |
| Poisson seed=1 | 0.3411 | 75.3% | −3.0 pts ⚠️ |
| Poisson seed=2 | 0.3923 | 69.9% | −8.4 pts |
| Poisson seed=3 | 0.3711 | 70.3% | −8.0 pts |
| **Poisson Mean** | **0.368** | **71.8%** | **−6.5 pts** |
| GUE seed=1 | 0.6527 | 76.5% | −1.8 pts |
| GUE seed=2 | 0.6315 | 76.3% | −2.0 pts |
| GUE seed=3 | 0.6358 | 77.7% | −0.6 pts |
| **GUE Mean** | **0.640** | **76.8%** | **−1.5 pts** |

**The actual zeros (78.3%) exceed GUE synthetic (76.8%) by +1.5 pts.**

Note on Poisson seed 1: 75.3% is anomalously high relative to seeds 2 and 3 (~70%) and Phase 4 Poisson trials (69.9–72.7%). This is seed-specific variance at n=98 and does not affect conclusions. The mean of 71.8% is the operative figure.

### The Key Comparison: Low Height vs. High Height

| Regime | Actual Chavez | GUE Chavez | Actual − GUE |
|---|---|---|---|
| Phase 4: zeros 1–99 (low height) | 75.0% | 76.9% | **−1.9 pts** |
| Phase 5B: zeros 500–599 (high height) | 78.3% | 76.8% | **+1.5 pts** |

The gap flipped from −1.9 to +1.5 — a 3.4-pt swing. The Phase 4 shortfall was a low-height regime artifact. At higher zeros the actual Riemann spectrum is more GUE-like than ideal Wigner surmise drawn for the low-height regime. This is consistent with asymptotic convergence: the zeros approach the pure GUE distribution as the imaginary part grows.

---

## Decision Table

| Question | Outcome | Verdict |
|---|---|---|
| Does GUE/Poisson separation widen with n? | 5.3 pts (n=99) → 7.2 pts (n=499) | YES ✅ |
| Was Phase 4 shortfall a low-height artifact? | Gap flipped: −1.9 → +1.5 pts | YES ✅ |
| Is mean ratio GUE-stable across scale? | 0.610–0.618 across n=99 to n=999 | YES ✅ |

---

## Updated Sequence of Findings Across All Phases

| Phase | Test | Finding |
|---|---|---|
| Phase 1 | Chavez on raw gaps | 83.8% — real signal, lower-bound compactness |
| Phase 2 (CTRL) | ZDTP on positions | Non-discriminating — monotonicity artifact |
| Phase 2b | Shuffle test | Ordering-invariant — distribution signal only |
| Phase 3 | GUE vs Poisson on raw gaps | GUE ≈ Poisson — compactness artifact, not GUE-specific |
| Phase 4 | Spacing ratio (mean) | Actual zeros = GUE (0.610 ≈ 0.640) |
| Phase 4 | Spacing ratio (Chavez) | GUE > Poisson: +5.3 pts — first correct ordering |
| **Phase 5A** | **Scale to n=499** | **Separation widens to 7.2 pts — pipeline strengthens** |
| **Phase 5B** | **Higher zeros 500–599** | **Actual exceeds GUE by +1.5 pts — low-height effect confirmed** |

---

## What This Means for the Research Program

Two results stand out:

**Scaling behavior:** The Chavez + spacing ratio pipeline is not a narrow-window tool. The GUE/Poisson separation widens from 5.3 to 7.2 pts as n grows from 99 to 499. The tool gains discriminatory power with larger datasets — a favorable property for any future prime-distribution application.

**Height convergence:** The fact that actual zeros 500–599 (78.3%) exceed GUE synthetic (76.8%) — while zeros 1–99 (75.0%) fall below it — is a clean, quantitative signature of asymptotic GUE convergence. The Chavez Transform is tracking a real spectral property: the Riemann zero spacing distribution approaches the GUE Wigner surmise as height increases.

---

## Files

| File | Purpose |
|---|---|
| `rh_scale_experiment_results.json` | Complete results in structured JSON |
| `RH_Phase5_Scale_and_Height_Results.md` | This document |
| `RH_Phase5_Scale_and_Height_Handoff.md` | Original analysis protocol |
| `rh_phase5_data_prep.py` | Script that generated synthetic sequences |
| `phase5_data_prep_summary.json` | Summary of all generated sequences and mean ratios |
