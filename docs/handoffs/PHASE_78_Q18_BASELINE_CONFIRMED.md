# Phase 78 Q-18: Baseline Confirmed ✓

> ⚠ **Correction pending.** This document is retained for the record; it
> carries three defects since verified against source, all in
> [`CORRECTIONS.md`](../../CORRECTIONS.md): the "0.433 chance" figure below is
> quoted against both ε=0.5 and ε=1.0, but it is only correct at ε=0.5 — true
> chance at ε=1.0 is 0.7607 (C-007); "z=8.42 significance (5-sigma
> equivalent)" conflates a Monte-Carlo effect size with a significance level —
> achieved significance is p < 2×10⁻⁴ (C-007); and the Scale Law section's
> "sub-√N scaling suggests the signal... carries structural information" is
> the earliest instance of a misreading corrected in C-001 — the z growth is
> the null tightening as 1/√N, not the detector strengthening. Moved into the
> repository 2026-09-08 (was previously outside version control) so these
> citations are verifiable.

**Chavez AI Labs LLC — Applied Pathological Mathematics**  
**Date:** August 23, 2026  
**Status:** Q-17 Detector Encoding baseline reproduced and verified

---

## Executive Summary

**The Q-17 Detector Encoding baseline (AIEX-741) is confirmed exact:**

```
Detector:  z = 8.42  |  AUC = 0.8661 (δ=0.5)  |  Precision = 0.831 vs 0.433 chance
Grid:      t ∈ [10, 240], 46,001 points, Δt = 0.005
Zeros:     γ₁–γ₁₀₁ (101 Riemann zeros)
Identity:  c_S2 + c_S6 = -2·Σₚ(log p/√p)cos(t·log p)  [residual 1.776e-15]
```

**Source:** `phase77_q17_results.json` (June 12, 2026) + live validation via CAILculator v2.1.4

---

## Baseline Details

### Detector Encoding Specification
- **Purpose:** Realize the full k=1 explicit-formula 6-prime zero detector as two signed readings
- **Infrastructure:** Gateway Linear Law (Phase 76) over the Canonical Six
- **Inputs:**
  - u₂ support {3,5,10,12} ← w_p·cos(t·ln p), p ∈ {2,3,11,13}
  - u₆ support {6,9} ← w_p·cos(t·ln p), p ∈ {5,7}
  - pos0 = σ, pos1 = t (retained), pos2 = 0 (zeroed for purity)
  - All other slots = 0
- **Weighting:** w_p = log p / √p

### Performance Metrics
| Metric | Value | Notes |
|--------|-------|-------|
| **z-score (T1)** | 8.42 | p < 2e-4; value-at-zeros statistic |
| **ROC AUC (δ=0.5)** | 0.8661 | Point is "positive" if within 0.5 units of a zero |
| **ROC AUC (δ=0.25)** | 0.8095 | Stricter proximity threshold |
| **Peak precision (ε=0.5)** | 0.831 | Greedy local-maxima to zero matching |
| **Peak precision (ε=1.0)** | 0.974 | Looser match radius |
| **Peak recall (ε=0.5)** | 0.634 | Detects 63.4% of zeros (77 of 121 maxima) |
| **Honest baseline** | 0.433 chance | Random prediction within ε=1.0 of mean gap |

**Interpretation:** At 101 Riemann zeros (mean gap ~2.28), a random prediction within distance 1.0 lands near a zero ~88% of the time (spurious precision 0.433). The detector achieves **0.831 precision** (ratio 1.92× above random), with **z=8.42** significance (5-sigma equivalent).

---

## Scale Law

The signed-channel signature strengthens with sample size:

| Zeros | c_S2 (documented) | Detector | √N prediction |
|-------|-------------------|----------|---------------|
| 31 | z=3.62 | — | — |
| 101 | z=4.92 | **z=8.42** | 6.53 (undershot) |

Sub-√N scaling suggests the signal is not purely statistical but carries structural information.

---

## Identity Verification

**The Detector Encoding identity is exact:**

```
c_S2(D(t)) + c_S6(D(t)) = -2 · Σₚ (log p/√p)·cos(t·log p)
```

where p ∈ {2, 3, 5, 7, 11, 13} and D(t) is the Detector Encoding input.

- **Residual:** 1.776e-15 (machine precision, 46,001-point sweep)
- **Verification:** Live CAILculator v2.1.4 call at γ₁ (AIEX-741 + live_validation.json)
- **Theory:** Direct consequence of the Gateway Linear Law (Phase 76)
- **Lean target:** `detector_channel_identity` (candidate lemma over `GatewayLinearLaw.lean`, standard axioms)

---

## Q-18: Ensemble Improvement Target

**Challenge:** Design a multi-gateway detector ensemble that beats **z=8.42 / AUC=0.8661**.

### Candidate Directions

1. **Per-gateway explicit-formula weighting**  
   - Exploit the different signal strengths across all six gateways (not just S2/S6)
   - Gateway-specific w_p calibration based on Phase 77 per-gateway z-scores
   - Test whether aggregation improves the 6.53→8.42 gap

2. **S4/S5 sign structure**  
   - Class B gateways (S1, S4, S5) are t-dominated; Class A (S2, S3, S6) are bounded oscillators
   - S4/S5 support {1,3,12,14} and {1,5,10,14} contain odd-indexed slots (time-reversal sensitive)
   - Hypothesis: signed readings of Class B encode additional zero structure beyond Class A

3. **Higher prime truncations**  
   - Current: k=1 truncation of the von Mangoldt explicit formula (6 primes)
   - Test k=2 truncation (up to p=13+17=30 or similar)
   - Verify whether encoding constraint (16D dimensionality) admits higher-order prime sets

4. **Clifford framework variant**  
   - Phase 77 used Cayley-Dickson products (non-associative)
   - S2 is bilateral in **both** Cayley-Dickson and Clifford algebras (unique among the Canonical Six)
   - Test whether Clifford-frame reading of S2 + weighted ensemble outperforms CD

### Methodology
- **Honest-baseline discipline** (AIEX-742): Random prediction baseline is z-dependent
- **Live CAILculator v2.1.4 validation:** Every claimed improvement must validate against the live MCP server
- **KSJ capture protocol:** All candidate designs, results, and reasoning → KSJ with `extract_insights` before `commit_aiex`

---

## CAILculator Status

### Current State
- **Version:** v2.1.4 (Engine v2.0 High-Precision)
- **Build:** 8,061 jobs · 0 errors · 1 sorry (by design)
- **Input validation:** Hardened (CHANGELOG, Aug 21–22 audit)
  - Added `_parse_numeric_data()` helper
  - Rejects NaN/Inf with clear `ValueError`
  - **Note:** Server process has NOT restarted; fix is in editable install but not live
- **MCP Protocol:** Still pre-2.0 (ksj-mcp upgraded to 2.0, CAILculator pending)

### Action Items Before Q-18 Runs
1. **Restart CAILculator server** to load input-validation hardening
2. **Plan MCP 2.0 upgrade** (parallel to Q-18 empirical work, not blocking)
3. **Confirm Detector Encoding input schema** with live server (sanity check)

---

## Sequencing for Phase 78

### Immediate (Today)
1. ✓ Baseline confirmed
2. Restart CAILculator server
3. Design Q-18 candidate ensembles (2–3 directions)

### Week 1
4. Run C (high zeros, γ₁–γ₂₅₁ or beyond) with honest-baseline methodology
5. Q-18 candidate evaluations (live CAILculator validation)
6. KSJ extractions and Paul approval per candidate

### Week 2+
7. v1.4 abstract draft (unblocked by empirical work)
8. MCP 2.0 upgrade and schema documentation
9. Lean infrastructure (SedenionProduct.lean, Q-16 e₀-transparency, detector_channel_identity lemma)

---

## Key References

| Artifact | Source | Purpose |
|----------|--------|---------|
| `phase77_q17_results.json` | June 12, 2026 | Baseline z=8.42 |
| `phase77_q17_live_validation.json` | June 12, 2026 | Live MCP validation |
| `phase77_q17_signed_channel.py` | Source script | Reproducible implementation |
| AIEX-741 | KSJ (June 12) | Discovery narrative |
| AIEX-742 | KSJ (June 12) | Honest-baseline methodology |
| `RH_PHASE_77_RESULTS.md` | June 12/17, 2026 | Full Q-14/Q-15/Q-17 context |

---

**Chavez AI Labs LLC**  
*Applied Pathological Mathematics — Better math, less suffering*  
*Phase 78 Opening — August 23, 2026*
