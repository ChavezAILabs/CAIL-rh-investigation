# RH Phase 9 Results — P5 Anomaly, Ultra-Fine R(α), Berry-Keating

**Experiment ID:** RH_UF_2026_001  
**Date:** 2026-03-08  
**Researcher:** Paul Chavez, Chavez AI Labs  

---

## Experiment 9A — P5 Anomaly Characterization

### What Was Tested
The pre-Phase 9 probe found that projecting Riemann gap pairs onto the P5 = (e₂+e₅) direction produced 758 bilateral zeros at 95% confidence with only 52% conjugation symmetry. The decisive question: is this Riemann-specific, or a GUE property?

### Results

| Sequence | Bilateral Zeros | Confidence | Conj. Symmetry |
|---|---|---|---|
| **Actual Riemann** | **758** | 95% | **52.0%** |
| GUE seed 1 | 715 | 95% | — |
| GUE seed 2 | 649 | 95% | 51.9% |
| GUE seed 3 | 757 | 95% | 54.9% |
| **GUE mean** | **707** | 95% | **~52–55%** |
| Poisson seed 1 | 697 | 95% | **77.6%** |

### Verdict: P5 Anomaly Is NOT Riemann-Specific

GUE synthetic sequences produce 649–757 bilateral zeros on P5, essentially the same range as actual Riemann zeros (758). Poisson also produces 697. The P5 projection = (g_n − g_{n+1}) + g_n/(g_n+g_{n+1}) naturally oscillates with sign changes for any gap sequence — the bilateral zero detector is measuring this oscillation, which is present in all three sequence types.

### Positive Finding: Conjugation Symmetry Discriminates GUE from Poisson

While bilateral zero counts don't separate Riemann/GUE from Poisson, **conjugation symmetry does**:

- GUE and actual Riemann: ~52% (both low — consistent with level repulsion creating asymmetric gap differences)
- Poisson: 78% (higher — lacks level repulsion, gap differences more mirror-symmetric)

**This is a new discriminant:** P5 conjugation symmetry distinguishes level-repulsion statistics (GUE/RH) from independent-gap statistics (Poisson) even though bilateral zeros do not.

---

## Experiment 9B — Ultra-Fine Pair Correlation R(α)

### Setup
- Phase 8B baseline (Δα=0.1, n=150): **12.5 pt separation** (Poisson 100% − Empirical 87.5%)
- 9B-i: Δα=0.05, n=300 (α = 0.05 to 15.0)
- 9B-ii: Δα=0.02, n=750 (α = 0.02 to 15.0)

### Results

| Grid | n | GUE Sym | Poisson Sym | Empirical Sym | Separation | vs 8B |
|---|---|---|---|---|---|---|
| Δα=0.1 (8B baseline) | 150 | 94.1% | 100.0% | 87.5% | **12.5 pts** | — |
| **Δα=0.05 (9B-i)** | **300** | **92.7%** | **100.0%** | **85.3%** | **14.7 pts** | **+2.2 pts** |
| Δα=0.02 (9B-ii) | 750 | 92.5% | 100.0% | 66.1% | 33.9 pts† | — |

† The n=750 result has 27 low-confidence bins (pair count < 10) at Δα=0.02 with only 1,000 zeros. The 66.1% empirical symmetry is artificially low due to sparse bin noise. This is the data bottleneck signal: 10,000+ zeros needed for reliable Δα=0.02 computation.

### Key Findings

**NEW SERIES RECORD: 14.7 pts at n=300, Δα=0.05** — confirming scaling continues beyond Phase 8B.

The GUE theoretical symmetry is stable (94.1% → 92.7% → 92.5%) — the kernel is consistently detecting the sinc² dip asymmetry. The empirical symmetry decreases with grid density, which is real signal (finer sampling captures more structure) but becomes noise-dominated below Δα=0.05 with n=1,000 zeros.

**Scaling Law (robust range):**

| Δα | n | Separation |
|---|---|---|
| 0.1 | 150 | 12.5 pts |
| 0.05 | 300 | 14.7 pts |

Predicted: 10,000 zeros + Δα=0.02 would yield ~18–20 pts separation.

---

## Experiment 9C — Height Band Analysis / Berry-Keating

### Setup
10 height bands of 100 zeros each (zeros 1–1000), spacing ratios analyzed per band. Dominant prime-orbit correction R_c = cos(log(2) × t_mid) computed per band.

### Band Results

| Band | t_mid | R_c | Actual Sym | GUE Sym | Delta |
|---|---|---|---|---|---|
| 1 | 125.3 | +0.460 | 34.7% | 32.7% | +2.0% |
| 2 | 317.1 | +0.991 | 38.8% | 32.7% | +6.1% |
| 3 | 469.9 | +0.517 | 53.1% | 32.7% | **+20.4%** |
| 4 | 612.0 | −0.994 | 46.9% | 32.7% | +14.3% |
| 5 | 746.5 | −0.621 | 36.7% | 32.7% | +4.1% |
| 6 | 875.9 | −0.698 | 36.7% | 32.7% | +4.1% |
| 7 | 1001.3 | −0.968 | 40.8% | 32.7% | +8.2% |
| 8 | 1123.9 | +0.996 | 63.3% | 32.7% | **+30.6%** |
| 9 | 1243.8 | +0.261 | 36.7% | 32.7% | +4.1% |
| 10 | 1361.3 | +0.421 | 42.9% | 32.7% | +10.2% |

### Berry-Keating Correlation

**Pearson r(R_c vs delta) = 0.348, p = 0.325**

This is a moderate positive correlation (r=0.35) that does not reach statistical significance at n=10 bands (p=0.325 > 0.05). The direction is correct (positive R_c correlates with higher delta), but the signal is noisy.

**Verdict:** Moderate Berry-Keating signature detected. Not statistically significant at 10 bands. The bands 3 and 8 show anomalously high deltas (+20.4% and +30.6%) that don't cleanly track R_c. Higher-order prime orbit terms (p=3, 5, 7...) are likely needed for a proper R_c model. 100-zero bands are also quite noisy for symmetry estimation.

---

## Cumulative Record Summary After Phase 9

| Phase | Method | n | Separation |
|---|---|---|---|
| 5 | Spacing ratios | 499 | 7.2 pts |
| 7A | R(α) coarse | 30 | 6.9 pts |
| 8B | R(α) fine | 150 | 12.5 pts |
| **9B-i** | **R(α) ultra-fine** | **300** | **14.7 pts ← NEW RECORD** |
| 9B-ii | R(α) ultra-fine (noisy) | 750 | 33.9 pts (caveat) |

---

## Phase 10 Recommendations

**Priority 1 — Odlyzko Dataset (10,000+ zeros)**
- Δα=0.02 empirical R(α) requires 10,000+ zeros for stable bins
- Predicted: clean 20+ pt separation at Δα=0.02, n=10,000
- Use Andrew Odlyzko's published high-precision zero tables

**Priority 2 — P5 Conjugation Symmetry at Scale**
- Run P5 projection on all 1000-zero gap pairs (999 pairs → 998 projections)
- Compare conjugation symmetry: actual vs 10-seed GUE ensemble
- Test if Riemann zeros cluster distinctly below GUE on P5 conjugation symmetry

**Priority 3 — Berry-Keating with Full Prime Sum**
- Extend R_c model: R_c(t) = Σ_p cos(log(p) × t) / sqrt(p) for first 10 primes
- Re-run 9C correlation with proper multi-prime R_c
- Predicted: r > 0.6 with full prime sum (Phase 9C got r=0.35 with p=2 only)

**Priority 4 — CAILculator vector_data API**
- Implement n×k array input for native Color Group testing
- Phase 9A demonstrated Option D works; native support enables cleaner experiments

---

## Files

| File | Path |
|---|---|
| Phase 9 JSON results | `/mnt/user-data/outputs/rh_phase9_results.json` |
| Phase 9 summary | `/mnt/user-data/outputs/RH_Phase9_Results.md` |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**  
*"Better math, less suffering"*
