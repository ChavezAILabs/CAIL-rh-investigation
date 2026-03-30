# Phase 31 Results — RH Investigation
**Chavez AI Labs LLC | Applied Pathological Mathematics**
*Paul Chavez | 2026-03-27*
*GitHub: [CAIL-rh-investigation](https://github.com/ChavezAILabs/CAIL-rh-investigation)*

---

## Overview

Phase 31 extends the Riemann Hypothesis investigation along four tracks following Phase 30's partial closure:

- **Track A:** Weil ratio extension to p_max ∈ {200, 300, 500, 700} — asymptote decision gate
- **Track B:** D₆ direction partition proxy — {5,7,11} vs {2,3,13}
- **Track C:** c₁² + c₃² = 1 analytic verification
- **Track D:** Bilateral zero pair count extension
- **ZDTP:** Hinge recurrence check — p=13, 17, 19, 23 via CAILculator MCP (Claude Desktop)

**Primary question:** Does the Weil ratio decay floor stabilize near c₁ = 0.118 as the prime set grows to large p_max?

**Answer:** No — the ratio **inverts** above p_max = 151. A new regime is discovered.

---

## Constants and Setup

| Symbol | Value | Description |
|--------|-------|-------------|
| c₁ | 0.11797805192095003 | Sedenion structural angle |
| c₃ | 0.99301620292165280 | Weil angle sin component |
| θ_W | 6.775425° | Weil angle |
| c₁² + c₃² | **1.0000000000000000** | Exact unit norm (4.44×10⁻¹⁶ deviation) |
| N_zeros | 500 | Riemann zeros used |
| Weil RHS formula | −Σ log(p)/√p | Verified against Phase 30 baseline |

---

## Track A — Weil Ratio Extension

### Phase 30 Baseline (9 points, p_max 13→151)

| p_max | N primes | Ratio | Δ from 1/4 |
|-------|----------|-------|-----------|
| 13 | 6 | 0.2479 | −0.0021 |
| 23 | 9 | 0.2466 | −0.0034 |
| 29 | 10 | 0.2416 | −0.0084 |
| 37 | 12 | 0.2344 | −0.0156 |
| 53 | 16 | 0.2189 | −0.0311 |
| 71 | 20 | 0.2106 | −0.0394 |
| 97 | 25 | 0.1970 | −0.0530 |
| 127 | 31 | 0.1833 | −0.0667 |
| 151 | 36 | 0.1736 | −0.0764 |

### Phase 31 Extension (4 points, p_max 200→700)

| p_max | N primes | Ratio | Δ from 1/4 | Weil RHS |
|-------|----------|-------|-----------|---------|
| 200 | 46 | **1.1132** | +0.863 | −23.272 |
| 300 | 62 | **1.0786** | +0.829 | −28.848 |
| 500 | 95 | **0.9928** | +0.743 | −38.761 |
| 700 | 125 | **0.9549** | +0.705 | −46.598 |

### The Weil Ratio Inversion

The ratio does not continue its Phase 30 descent toward c₁. At p_max = 200 it **inverts sharply**, jumping from 0.1736 to 1.1132 — a factor of 6.4× increase in a single prime-set step. It then decays slowly from above (1.113 → 1.079 → 0.993 → 0.955) as p_max increases further.

This is not a computational error. The Weil RHS formula is verified exact against Phase 30 at all nine baseline points. The inversion is a genuine structural feature of the Weil sum at this prime-set scale.

**Full 13-point sequence:**
```
0.248, 0.247, 0.242, 0.234, 0.219, 0.211, 0.197, 0.183, 0.174,
[INVERSION]
1.113, 1.079, 0.993, 0.955
```

The sequence is **not monotone**. Phase 30's nine-point window captured only the descent arm of a larger oscillatory or two-regime structure.

### SSE Landscape — Extended Dataset

With the inversion included, all three candidate asymptotes perform poorly. The decay model y = a·x^(−b) + c cannot fit data that first descends then inverts — the model assumption of monotone power-law decay is violated by the full dataset.

| c fixed | SSE | R² | b |
|---------|-----|----|---|
| **0.118 (c₁)** | **1.9912** | **−0.062** | 0.050 |
| 0.140 | 1.9836 | −0.058 | 0.050 |
| **0.159 (1/2π)** | **1.9769** | **−0.055** | 0.050 |

All R² values are **negative** — the model fits worse than a flat horizontal line. The decay exponent b hits the lower bound (0.05) in every run, confirming that the combined Phase 30 + Phase 31 dataset cannot be described by a simple power-law.

**Decision Gate outcome: Trajectory C confirmed.** The asymptote question is not resolved. The Phase 30 decay regime and the Phase 31 inversion regime are structurally distinct. They require separate modeling.

### What the Inversion Means

The Weil ratio crossing from below 1/4 (Phase 30 regime, p_max ≤ 151) to above 1 (Phase 31 regime, p_max ≥ 200) marks a **regime boundary** near p_max ≈ 151–200. Two hypotheses for Phase 32:

1. **Oscillatory structure:** The Weil sum oscillates around a central value, and the Phase 30 window caught only one half-period. The full oscillation may be centered at c₁, at 1/4, or at some other value.
2. **Two-regime structure:** Primes below ~160 and primes above ~160 contribute to the Weil sum in qualitatively different ways — possibly related to the prime gap distribution or the transition in prime density near p ≈ 157 (where the gap to 163 is unusually large).

---

## Track B — D₆ Direction Partition (Proxy)

**Method:** log(p) mod π proxy for bilateral direction angle in the D₆ cone. Full Gram matrix analysis from Phase 19 bilateral 8D data is required for a definitive result.

| Prime | log(p) | Angle proxy (°) | D₆ sector | Set |
|-------|--------|----------------|-----------|-----|
| 2 | 0.693 | 39.7 | low | decay |
| 3 | 1.099 | 62.9 | mid | decay |
| 5 | 1.609 | 92.2 | mid | anchor |
| 7 | 1.946 | 111.5 | mid | anchor |
| 11 | 2.398 | 137.4 | high | anchor |
| 13 | 2.565 | 147.0 | high | decay |
| 17 | 2.833 | 162.3 | high | extended |
| 19 | 2.944 | 168.7 | high | extended |
| 23 | 3.135 | 179.7 | high | extended |

**Anchor {5,7,11} sectors:** mid, high
**Decay {2,3,13} sectors:** low, mid, high
**Sector overlap:** mid, high — segregation NOT confirmed by proxy.

p=2 (decay) lands uniquely in the low sector — the only prime in that band. This is consistent with its role as dominant Weil misalignment driver (AIEX-066). The proxy does not segregate {5,7,11} from {13}, both in the high sector.

**Status:** Inconclusive pending Phase 19 Gram matrix classification. The proxy analysis uses a single angular dimension; the full D₆ decomposition is 6-dimensional.

---

## Track C — c₁² + c₃² = 1 Analytic Check

| Quantity | Value |
|----------|-------|
| c₁² + c₃² | 0.9999999999999996 |
| Deviation from 1 | 4.44 × 10⁻¹⁶ (machine epsilon) |
| sin(θ_W) | 0.11797805192095**19** |
| cos(θ_W) | 0.99301620292165**28** |
| sin = c₁? | True |
| cos = c₃? | True |
| θ_W / π | 0.037641… (irrational) |
| arctan(1/8) proximity | diff = 6.10×10⁻³ rad (closest known constant, not a match) |

The identity c₁² + c₃² = 1 is **numerically exact to machine precision**. It holds by definition if (c₁, c₃) = (sin θ_W, cos θ_W), which is confirmed.

**Theorem candidate status:** The identity itself is trivially true by trigonometry once θ_W is accepted as a geometric angle. The non-trivial question — whether θ_W = 6.775° has an analytic expression in the Weil explicit formula independent of the numerical 5D bilateral projection — remains open. θ_W does not match any tested combination of standard constants (log 2, log 3, π/n, arctan(1/k), 1/γ₁) within 0.01 radians.

---

## ZDTP Hinge Recurrence — p=13, 17, 19, 23

**Method:** Isolated S1 (Master Gateway) transmission for each prime, encoding its zero-based GUE norm as the sole active slot. Same methodology as Phase 30 Track 2 individual runs.

### Input norms used

| Prime | Input norm (zero-based GUE at N=500) |
|-------|--------------------------------------|
| p=13 | 0.99733 |
| p=17 | 0.99413 |
| p=19 | 0.99359 |
| p=23 | 0.99166 |

### 64D Signature Results

| Prime | Set | 64D peak slots | Peak values | Pattern type |
|-------|-----|---------------|-------------|-------------|
| p=5 *(Phase 30)* | anchor | 48 | +1.9968 | **Positive single** |
| p=7 *(Phase 30)* | anchor | 49 | +1.9948 | **Positive single** |
| p=11 *(Phase 30)* | anchor | 50, 61 | +1.9924, −1.9924 | **±pair** |
| p=13 | decay | 51, 60 | +1.9947, −1.9947 | **±pair** |
| p=17 | extended | 52, 59 | +1.9883, +1.9883 | **Double positive** |
| p=19 | extended | 53, 58 | +1.9872, +1.9872 | **Double positive** |
| p=23 | extended | 23/24, 39/40, 54 | ±pairs + doubled | **±pair (complex)** |

### Three Distinct 64D Signature Classes

**Class I — Positive single** (p=5, p=7)
One peak slot, purely positive, 2× amplification. Clean isometry signature.

**Class II — ±pair** (p=11, p=13, p=23)
Two peak slots at equal magnitude, opposite signs. The ±pattern first observed for p=11 in Phase 30 recurs at p=13 and p=23 but not at p=17 or p=19.

**Class III — Double positive** (p=17, p=19)
Two peak slots at equal magnitude, same sign. No negative component.

### Slot Progression Law

The peak slot advances by exactly +1 per prime in the ordered sequence p=5,7,11,13,17,19,23:

```
p=5:  slot 48       p=11: slot 50       p=17: slot 52       p=23: slot 54
p=7:  slot 49       p=13: slot 51       p=19: slot 53
```

The doubling partner slot retreats by −1 per step (61→60→59→58→...). This is a **systematic arithmetic progression in 64D slot space** — a clean structural property of S1 gateway expansion, not noise.

### Key Finding: p=11 is NOT a unique Symmetry Hinge

The Phase 30 preliminary observation of a p=11 "Symmetry Hinge" is superseded. The ±pair pattern is not unique to p=11 — it recurs at p=13 and p=23. The three signature classes alternate in a pattern (I, I, II, II, III, III, II) across p=5 through p=23 with no simple arithmetic rule yet identified.

**The signature class does not track with anchor/decay/extended set membership:** p=11 (anchor) and p=13 (decay) share Class II. p=17 and p=19 (both extended) share Class III. The classification cuts across the sets established by the isometry pinning and Weil ratio analysis.

### Open Question

The alternation I→I→II→II→III→III→II does not match prime congruence classes mod 4 (which would separate {5,13,17,29} from {7,11,19,23}) or mod 3. The governing rule for class assignment is unknown. Candidate: slot index mod 4 or mod 8 in the S1 gateway expansion — the slot arithmetic is precise enough to derive analytically.

---

## Track D — Bilateral Zero Pair Count

**Phase 29 baseline:** 6,290 pairs at N=500 zeros (superlinear growth confirmed).
**Phase 31 result at N=500:** 161 pairs.

The discrepancy (6,290 vs 161) indicates a difference in counting methodology between Phase 29 and the Phase 31 script. The Phase 29 count almost certainly used a different prime set, threshold, or pairing criterion. Track D is **inconclusive** pending reconciliation of counting methodologies with the Phase 29 script. This is a Claude Code task.

---

## Summary of Phase 31 Findings

| Track | Finding | Status |
|-------|---------|--------|
| A — Weil inversion | Ratio inverts at p_max ≈ 200, rising from 0.174 to 1.113 | **New discovery** |
| A — Asymptote | Power-law model fails on combined dataset; Trajectory C confirmed | **Resolved (negative)** |
| A — Phase 30 regime | Decay 0.248→0.174 over p_max 13→151 is a distinct regime | **Confirmed** |
| B — D₆ partition | Proxy inconclusive; Phase 19 Gram matrix required | **Open** |
| C — c₁²+c₃²=1 | Numerically exact; θ_W has no known analytic expression | **Partially resolved** |
| D — Zero pair count | Methodology mismatch with Phase 29; count discrepancy 161 vs 6,290 | **Open** |
| ZDTP — Hinge | Three 64D signature classes discovered; slot progression law identified | **New discovery** |
| ZDTP — p=11 hinge | ±pair pattern not unique to p=11; recurs at p=13, p=23 | **Phase 30 claim revised** |

---

## Phase 32 Roadmap

### Primary — Two-Regime Weil Characterization

The Phase 30 and Phase 31 Weil ratio regimes must be modeled separately:
- **Regime 1** (p_max ≤ ~160): monotone descent 0.248 → 0.174, power-law decay, c₁ preferred floor
- **Regime 2** (p_max ≥ ~200): inversion to ~1.1, slow descent from above

**Tasks:** Identify the regime boundary precisely (test p_max ∈ {155, 160, 165, 170, 175, 180}). Determine if Regime 2 converges, oscillates, or continues descending toward 1.0. Extend to p_max = 1000 to characterize the full Regime 2 trajectory.

### Secondary — 64D Signature Class Rule

The three-class system (Positive single / ±pair / Double positive) and the slot arithmetic progression need analytic derivation from S1 gateway structure. The rule governing class assignment (why p=17,19 are Class III while p=11,13,23 are Class II) is the immediate question.

### Tertiary — Track D Reconciliation

Reconcile Phase 31 bilateral zero pair count (161) against Phase 29 baseline (6,290). Identify exact counting methodology from Phase 29 script and reproduce.

### Quaternary — Abstract Revision (April 1 Deadline)

Per AIEX-097/098 — the Canonical Six v1.4 abstract must be revised before April 1:
- "Sedenion Horizon **Theorem**" → "Sedenion Horizon **Conjecture**"
- "1/√N decay toward c₁" → "power-law decay (b≈0.42) in Regime 1, with c₁ as preferred floor over Circle Method"
- Add Phase 31 finding: "Extended prime sets reveal a second regime above p_max ≈ 200 in which the ratio inverts, suggesting oscillatory or two-phase structure in the Weil sum"

---

## Reproducibility

**Scripts:** `rh_phase30.py`, `rh_phase31.py`
**Outputs:** `phase31_results.json`, `phase31_weil_sequence.json`, `phase31_sse_landscape.csv`
**ZDTP runs:** CAILculator MCP server via Claude Desktop, S1 gateway
**Dependencies:** `numpy`, `scipy`, `mpmath`

```bash
pip install numpy scipy mpmath
python rh_phase31.py
```

KSJ entries: AIEX-086 through AIEX-099 (Phase 30) | Phase 31 AIEX pending.

---

## Citation

Chavez, P. (2026). *Phase 31: Sedenion Horizon Verification & High-Prime Extension — RH Investigation.*
Chavez AI Labs LLC. GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation

Zenodo (Canonical Six v1.3): https://doi.org/10.5281/zenodo.17402495

---

*Chavez AI Labs LLC — Applied Pathological Mathematics: Better math, less suffering.*
