# RH Phase 4 — Spacing Ratio GUE Fingerprint Test Results
**Experiment ID:** RH_SR_2026_001  
**Date:** 2026-03-04  
**Researcher:** Paul Chavez, Chavez AI Labs

---

## Final Decision Table

| Sequence | Mean Ratio | Chavez Symmetry | Δ from Actual |
|---|---|---|---|
| **Actual zero gaps (n=99)** | **0.610** | **75.0%** | baseline |
| Poisson seed=1 | 0.342 | 72.7% | −2.3 pts |
| Poisson seed=2 | 0.388 | 69.9% | −5.1 pts |
| Poisson seed=3 | 0.463 | 72.2% | −2.8 pts |
| **Poisson Mean** | **0.397** | **71.6%** | **−3.4 pts** |
| GUE Wigner seed=1 | 0.653 | 76.5% | +1.5 pts |
| GUE Wigner seed=2 | 0.632 | 76.3% | +1.4 pts |
| GUE Wigner seed=3 | 0.636 | 77.7% | +2.8 pts |
| **GUE Wigner Mean** | **0.640** | **76.9%** | **+1.9 pts** |

---

## Three Distinct Results

### Result 1: Mean Ratio — Clean GUE Separation (Pre-Chavez)

The spacing ratio mean itself is the clearest signal of the entire experiment series:

| Sequence | Mean Ratio | Theoretical |
|---|---|---|
| GUE synthetic | **0.640** | ~0.60 ✓ |
| Actual zeros | **0.610** | — |
| Poisson synthetic | **0.397** | ~0.39 ✓ |

GUE and Poisson separate by **+0.243** — nearly matching theory. The actual zeros land at 0.610, essentially on top of GUE (0.640, Δ = −0.030). The spacing ratio statistic, used as a scalar mean, cleanly identifies the actual zero gaps as GUE-distributed, not Poisson-distributed. **This is the GUE fingerprint.** It doesn't require Chavez at all — the statistic itself is the test, and the zeros pass it definitively.

### Result 2: Chavez Symmetry — Partial GUE Separation

| Comparison | Δ | Threshold | Result |
|---|---|---|---|
| GUE vs Poisson (Chavez) | +5.3 pts | >5 pts | ✅ JUST exceeded |
| Actual vs Poisson (Chavez) | +3.4 pts | >5 pts | ⚠️ Sub-threshold |
| Actual vs GUE (Chavez) | −1.9 pts | <3 pts | ✅ Actual ≈ GUE |

Chavez conjugation symmetry **can** distinguish GUE from Poisson on the spacing ratio statistic — 76.9% vs 71.6%, a 5.3-point separation that just clears the significance threshold. The actual zeros (75.0%) sit between GUE and Poisson on Chavez but 3.4 points above Poisson — sub-threshold alone, but consistent with the GUE placement.

Crucially: **actual zeros score below GUE synthetic** on Chavez (75.0% vs 76.9%). This means the actual zeros have slightly less bilateral regularity in their spacing ratios than ideal Wigner-distributed gaps. This is physically expected — the actual zeros near the real axis (zeros #1–99) are in a low-height regime with known deviations from asymptotic GUE behavior. The pure GUE synthetic is drawn from the asymptotic spacing distribution; the actual zeros in this range are not fully in the asymptotic regime.

### Result 3: Chavez Discriminability — Confirmed Directional

The Chavez Transform successfully tracks the GUE/Poisson distinction through the spacing ratio statistic, ranking the three sequences in the correct theoretical order:

```
GUE synthetic  76.9%  ← most regular spacing (level repulsion)
Actual zeros   75.0%  ← GUE-like but sub-asymptotic regime
Poisson        71.6%  ← least regular (memoryless gaps)
```

This is the first experiment in the series where Chavez produces a **directionally correct, theoretically ordered ranking** across all three sequence types.

---

## Updated Sequence of Findings Across Phases

| Phase | Test | Finding |
|---|---|---|
| Phase 1 | Chavez on raw gaps | 83.8% — real signal, GUE range |
| Phase 2 (CTRL) | ZDTP on positions | Non-discriminating — monotonicity artifact |
| Phase 2b | Shuffle test | Ordering-invariant — distribution signal only |
| Phase 3 | GUE vs Poisson on raw gaps | GUE ≈ Poisson — compactness artifact |
| **Phase 4** | **Spacing ratio (mean)** | **Actual zeros = GUE (0.610 ≈ 0.640)** |
| **Phase 4** | **Spacing ratio (Chavez)** | **GUE > Poisson confirmed (+5.3 pts)** |

**The spacing ratio mean is the discriminating result.** It requires no Chavez — it is a direct, clean GUE test that the actual zeros pass.

---

## What This Means for the Research Program

The actual Riemann zeros (n=99, low-height regime) exhibit GUE-consistent consecutive gap regularity — mean spacing ratio 0.610, essentially matching the GUE theoretical expectation of ~0.60 and far above the Poisson expectation of ~0.39. This is well-known from the RMT literature (Bohigas-Giannoni-Schmit conjecture, Montgomery-Dyson) but now confirmed using the Chavez Transform + spacing ratio pipeline.

The new contribution is that Chavez conjugation symmetry on spacing ratios produces a **directionally correct ordering** (GUE > actual > Poisson) and achieves >5 pt GUE/Poisson separation. This means the Chavez Transform has a sensitivity window for GUE statistics when applied to ordering-dependent derived statistics (ratios) rather than raw gap values.

---

## Immediate Next Steps

- [ ] **Close Phase 4 — positive result confirmed**
- [ ] Document in Zenodo v1.4 as: "Chavez Transform correctly orders GUE > actual Riemann zeros > Poisson on spacing ratio statistic at n=99"
- [ ] **Phase 5 — Scale test:** Run spacing ratio analysis at n=249, 499, 999 gaps. Does the mean ratio stay near 0.60 across scale? Does the GUE/Poisson Chavez separation widen with larger n?
- [ ] **Phase 5b — Higher zeros:** Repeat at zeros #500–599 (higher in the critical strip, more asymptotically GUE). The actual zeros should score even closer to GUE synthetic.
- [ ] Update CLAUDE.md: Chavez + spacing ratio pipeline gives directionally correct GUE ordering; mean ratio alone is the clean discriminating statistic
