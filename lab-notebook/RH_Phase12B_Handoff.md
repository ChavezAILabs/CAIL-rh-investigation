# RH Phase 12B — Skewness Artifact Test
## Handoff Document

**Date:** 2026-03-09
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Depends on:** Phase 11D (skewness anomaly), Phase 10C (embed_pair protocol)
**Status:** COMPLETE — self-contained Python analysis (no CAILculator required)

---

## Question

Phase 11D found that actual Riemann zeros have P2 projection skewness = -1.42,
versus GUE synthetic skewness = -0.45. Is this a genuine structural property of
the Riemann zeros, or an artifact of the embed_pair transformation?

---

## Key Mathematical Setup

embed_pair(g1, g2) = [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
P2 = [0, 0, 0, 1, -1, 0, 0, 0]

P2 projection simplifies to:
  P2(g1, g2) = g1*g2/(g1+g2) - (g1+g2)/2
             = -(g1^2 + g2^2) / (2*(g1+g2))

This is always <= 0 for positive gaps. Large gaps dominate the g^2 term,
so right-skewed gap distributions (occasional large gaps) produce more
negatively-skewed P2 projections.

---

## Test Design

Run `rh_phase12b_prep.py`. No CAILculator calls needed — all statistical moments
computed directly in Python.

Five distributions, each producing 97 P2 projection values (from 97 consecutive
gap pairs out of 98 gaps):

| Distribution | Purpose |
|---|---|
| Actual (first 98 gaps) | Reference — Phase 11D result |
| GUE Wigner surmise (5 seeds) | Prior-phase comparison |
| Poisson Exponential (5 seeds) | Prior-phase comparison |
| **Gaussian N(mu, sigma) (5 seeds)** | KEY control: symmetric input, mean+std matched |
| Uniform [lo, hi] (5 seeds) | KEY control: near-zero raw skewness |

Verdict rule:
- Gaussian P2 skew near -1.42 → ARTIFACT (distribution shape alone explains it)
- Gaussian P2 skew near -0.45 (GUE) → GENUINE (actual zeros have extra skewness)
- Intermediate → PARTIAL

---

## Results

Run output from `rh_phase12b_prep.py`:

| Distribution | Raw gap skew | P2 skew | P2 kurtosis |
|---|---|---|---|
| Actual | +1.4237 | **-1.4215** | 3.016 |
| GUE (5 seeds avg) | +0.6125 | -0.3714 | -0.311 |
| Poisson (5 seeds avg) | +1.6624 | -1.1887 | 1.034 |
| **Gaussian (5 seeds avg)** | **+0.2725** | **-0.2244** | 0.048 |
| Uniform (5 seeds avg) | -0.0699 | +0.6005 | -0.413 |

---

## Verdict: NOT AN ARTIFACT — but root cause identified

**Gaussian control gives P2 skew = -0.22**, close to GUE's -0.37 and far from
actual's -1.42. The embed_pair + P2 transformation does NOT inherently produce
large negative skewness for symmetric inputs.

**Root cause**: The P2 projection approximately negates and amplifies raw gap
skewness. The pattern is clear:

| Raw gap skew | P2 skew |
|---|---|
| ~0.00 (Uniform) | ~+0.60 (near zero, flipped) |
| ~0.27 (Gaussian) | ~-0.22 |
| ~0.61 (GUE) | ~-0.37 |
| ~1.42 (Actual) | ~-1.42 |
| ~1.66 (Poisson) | ~-1.19 |

The actual Riemann zero gaps have raw skewness +1.42 — more right-skewed than
GUE (0.61) but slightly less than Poisson (1.66). Large gaps are more common
in the actual zero spectrum than the Wigner surmise predicts. The P2 formula
amplifies this into -1.42 projection skewness.

---

## New Structural Finding

Reconciling Phase 10C and Phase 11D:
- **Tighter P2 variance** (Act/GUE ~ 0.65-0.75): consecutive gaps more similar
  to each other than GUE predicts — stronger typical level repulsion
- **More right-skewed P2**: occasional large gaps, heavier right tail than GUE

These are compatible. Actual Riemann zeros show BOTH:
1. Stronger typical repulsion (narrower gap distribution near the mode)
2. Heavier right tail (occasional large gaps beyond GUE's Gaussian cutoff)

This is consistent with the actual zero spectrum being "more ordered than GUE
on average but with occasional outliers" — a subtle deviation from pure Wigner
surmise behavior.

---

## Implication for Phase 11D

The Phase 11D conclusion "two orthogonal structural properties" stands, but
requires reinterpretation:

- Property 1 (variance): actual zeros have tighter consecutive-gap similarity
  than GUE — this is a projection space property, still valid
- Property 2 (skewness): this is NOT independent of the gap distribution shape.
  It reflects actual zeros having heavier right-tailed gaps than GUE. The two
  properties are orthogonal in the PROJECTION space but are both downstream of
  the raw gap distribution structure.

The Phase 18 open question ("is skewness a transformation artifact?") is now
answered: NOT an artifact, but NOT a mysterious new property either — it is
a consequence of actual gaps being more right-skewed than Wigner surmise.

---

## Files

| File | Contents |
|---|---|
| `rh_phase12b_prep.py` | Analysis script (self-contained) |
| `p12b_results.json` | Full results in structured JSON |
| `RH_Phase12B_Handoff.md` | This document |
| `RH_Phase12B_Results.md` | Results summary |
