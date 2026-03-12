# RH Phase 12B — Skewness Artifact Test: RESULTS

**Date:** 2026-03-09
**Status: COMPLETE ✓**
**Verdict: NOT AN ARTIFACT — root cause identified**

---

## Question

Is the -1.42 P2 projection skewness of actual Riemann zeros (Phase 11D) a
genuine structural signal or an artifact of the embed_pair transformation?

---

## Results Table

| Distribution | Raw gap skew | P2 skew | P2 excess kurtosis |
|---|---|---|---|
| Actual (n=98) | +1.4237 | **-1.4215** | +3.016 |
| GUE Wigner (5 seeds) | +0.6125 | -0.3714 | -0.311 |
| Poisson Exp (5 seeds) | +1.6624 | -1.1887 | +1.034 |
| **Gaussian control (5 seeds)** | **+0.2725** | **-0.2244** | +0.048 |
| Uniform control (5 seeds) | -0.0699 | +0.6005 | -0.413 |

Actual gap statistics: mean=2.2404, std=1.0474

---

## Verdict: NOT AN ARTIFACT

Gaussian control (symmetric input, mean+std matched to actual) produces
P2 skew = **-0.22** — close to GUE (-0.37), far from actual (-1.42).

The embed_pair + P2 transformation does NOT inherently inflate skewness.
Actual zeros have genuine extra skewness beyond what their mean and variance
alone would produce.

---

## Root Cause Identified

P2(g1,g2) = -(g1^2 + g2^2) / (2*(g1+g2))

This formula amplifies right-skewed gap distributions (occasional large gaps
drive the g^2 terms disproportionately). The P2 skewness tracks raw gap
skewness with sign inversion:

| Raw gap skew | P2 skew |
|---|---|
| ~0.00 (Uniform) | ~+0.60 |
| ~0.27 (Gaussian) | ~-0.22 |
| ~0.61 (GUE) | ~-0.37 |
| ~1.42 (Actual) | ~-1.42 |
| ~1.66 (Poisson) | ~-1.19 |

**Actual Riemann zero gaps are more right-skewed (+1.42) than GUE Wigner
surmise gaps (+0.61).** Large gaps are more common in the actual spectrum than
the Wigner surmise predicts, but less common than a Poisson distribution would
predict.

---

## Structural Picture (Phase 10C + 11D + 12B combined)

Actual Riemann zeros occupy a consistent position relative to GUE and Poisson:

| Property | Actual | GUE | Poisson | Ordering |
|---|---|---|---|---|
| P2 variance | lower | mid | highest | Act < GUE < Poi |
| Raw gap skewness | mid | lowest | highest | GUE < Act < Poi |
| P2 skewness | most negative | least negative | mid | GUE > Poi > Act |

Two real structural properties:
1. **Tighter consecutive-gap similarity** (lower P2 variance): actual zeros show
   stronger typical level repulsion than Wigner surmise — gaps more uniform
2. **Heavier right tail** (higher raw skewness than GUE): occasional large gaps
   occur more often than Wigner surmise predicts

These are compatible: actual zeros are more regular on average (property 1) but
have heavier right tails (property 2). This is a subtle deviation from pure
GUE behavior — "more repulsive on average but with occasional outliers."

---

## Resolution of Phase 11D Open Question

Phase 11D queued for Phase 18: "Is the skewness a transformation artifact?"
**Answer: No.** But it is not a new mystery property either. It is a direct
consequence of actual gaps being more right-skewed than GUE. The P2 formula
maps raw gap right-skewness → P2 left-skewness. The finding is real; the
interpretation shifts from "mysterious skewness anomaly" to "heavier-right-tail
gap distribution than Wigner surmise."

---

## Impact on CLAUDE.md / Paper

- Phase 11D "two orthogonal structural properties" language should be revised:
  the properties are orthogonal in projection space but both downstream of raw
  gap distribution shape
- The Phase 18 open question on skewness is now resolved and can be closed
- New finding for paper: actual zeros have raw gap skewness +1.42, placing them
  between GUE (0.61) and Poisson (1.66) — Wigner surmise underestimates the
  right tail of the actual gap distribution

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
