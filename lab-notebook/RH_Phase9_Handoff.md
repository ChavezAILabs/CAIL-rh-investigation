# RH Phase 9 — P-Vector Projection, Ultra-Fine Pair Correlation, and Negative Delta

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-08
**Experiment ID:** RH_UF_2026_001
**Prerequisite:** RH Phase 8 complete (`rh_phase8_results.json`); P-vector projection test complete (pre-Phase 9 probe)

---

## Context: What Phase 8 and the Pre-Phase 9 Probe Established

**Phase 8 findings:**

1. **12.5 pt separation** on fine-grid R(α) at n=150 (Δα=0.1) — new series record.
2. **1D invariance theorem confirmed encoding-independent** — all 6 patterns identical for any 1D real array.
3. **Systematic negative delta confirmed** across three experiments (actual zeros consistently below GUE synthetic).

**Pre-Phase 9 P-vector projection probe (critical new finding):**

Manual projection of Riemann gap pairs (gₙ, gₙ₊₁) onto each Canonical Six P-vector in 8D space revealed:

| Projection | Direction | Conjugation Symmetry | Notes |
|---|---|---|---|
| P1 | e₁ − e₆ | 79.1% | Color Group 1 |
| P2 | e₃ − e₄ | 83.0% | Color Group 2 |
| P3 | e₃ + e₄ (antipodal) | — | = P6 by definition |
| P4 | e₁ + e₆ | 78.9% | Color Group 1 |
| P5 | e₂ + e₅ | **52.0%** + **758 bilateral zeros (95% confidence)** | Color Group 2 |
| P6 | = P3 | — | Antipodal pair |

**Color Group 1 clustering confirmed:** P1 and P4 score 79.1% and 78.9% (0.2 pt spread) — nearly identical, consistent with their shared e₁ component.

**P5 anomaly — the primary Phase 9 finding to characterize:** Projection onto (e₂+e₅) produces a qualitatively different result. 758 bilateral zero-crossing pairs at 95% confidence. This is not a symmetry score — it is algebraic annihilation behavior. The Riemann gap pairs, when projected onto the (e₂+e₅) sedenion direction, produce structured near-cancellation events. This is the first empirical hint of the annihilation mechanism proposed in AIEX-001.

**The critical unanswered question:** Does GUE synthetic produce a similar P5 anomaly? If yes — a GUE property. If no — specific to actual Riemann zeros.

Phase 9 has three experiments in priority order: characterize the P5 anomaly, push the R(α) separation record, and map the negative delta structure across height bands.

---

## Experiment 9A — P5 Anomaly Characterization (Primary)

### What Was Found

The (e₂+e₅) P-vector projection of Riemann gap pairs produced 758 bilateral zero-crossing pairs at 95% confidence and 52.0% conjugation symmetry — a qualitatively different result from all other projections (78–83%). This is the first empirical signal in the series that resembles algebraic annihilation rather than statistical structure.

### Step 1: GUE Control — P5 Projection

Generate 3 GUE synthetic gap sequences (Wigner surmise, mean=2.25, seeds 1, 2, 3). For each: compute 98 consecutive gap pairs → project onto (e₂+e₅) direction → run detect_patterns.

Record per seed: conjugation symmetry, bilateral zero count, confidence level.

**This is the decisive test.** If GUE synthetic also produces ~758 bilateral zeros on P5 at similar confidence: P5 anomaly is a GUE property — interesting but not Riemann-specific. If GUE produces substantially fewer (< 200): P5 anomaly is specific to actual Riemann zeros — potentially the first annihilation-like signal tied to the zero spectrum.

### Step 2: Poisson Control — P5 Projection

Generate 3 Poisson gap sequences (Exponential mean=2.25, seeds 1, 2, 3). Project onto (e₂+e₅) → detect_patterns. Record: conjugation symmetry, bilateral zero count.

### Step 3: All 6 Projections — GUE Synthetic (seed 1)

For completeness, run all 6 P-vector projections on GUE seed 1 (same protocol as the pre-Phase 9 probe on actual zeros).

| Projection | GUE Sym | GUE Bilateral Zeros | Actual Sym | Actual Bilateral Zeros | Delta |
|---|---|---|---|---|---|
| P1 (e₁−e₆) | | | 79.1% | 0 | |
| P2 (e₃−e₄) | | | 83.0% | 0 | |
| P4 (e₁+e₆) | | | 78.9% | 0 | |
| P5 (e₂+e₅) | | | 52.0% | 758 | |

### Step 4: P5 on R(α) Fine-Grid Data

Project the fine-grid R(α) consecutive pairs (R(αₙ), R(αₙ₊₁)) onto the (e₂+e₅) direction. Use the Phase 8B dataset (n=150, Δα=0.1) → 149 consecutive pairs → 149 projected values. Run detect_patterns.

Also run P1 and P4 on R(α) pairs as comparison (Color Group 1 control).

**Key question:** Does the P5 anomaly appear in the pair correlation function data, or is it specific to raw gap pairs?

### Decision Framework — 9A

| Outcome | Interpretation |
|---|---|
| GUE bilateral zeros << 758 (< 200) | **P5 anomaly is Riemann-specific** — actual zeros have annihilation-like structure in (e₂+e₅) direction not present in GUE; AIEX-001 mechanism active |
| GUE bilateral zeros ≈ 758 | P5 anomaly is a GUE property — both zero spectrum and GUE produce it; constrains but does not eliminate AIEX-001 |
| Poisson also produces high bilateral zeros | P5 detects general gap pair structure, not GUE-specific |
| P5 on R(α) also anomalous | The annihilation signal exists in the pair correlation function itself — deep result |
| Color Group 1 (P1, P4) score identically on GUE | CG1 clustering is robust and encoding-independent |

---

## Experiment 9B — Ultra-Fine Pair Correlation R(α)

### Motivation

Phase 8B used Δα=0.1 (n=150) and achieved 12.5 pt separation. The discriminating power concentrates in the sinc² onset region (α=0.1 to ~2.0) where level repulsion drives R(α) from near-zero to ~1. A finer grid samples this region more densely, giving the bilateral kernel more bilateral structure to work with.

**Phase 9A runs two sub-experiments:**
- **9A-i**: Δα=0.05, n=300 (α=0.05 to 15.0)
- **9A-ii**: Δα=0.02, n=750 (α=0.02 to 15.0)

This tests whether the separation record continues scaling with grid density, and identifies the saturation point if one exists.

### Dataset

Files: `rh_zeros.json` (1,000 zeros). Empirical R(α) computed from all 1,000 zeros using adaptive window:
- For 9A-i (Δα=0.05): window = ±0.025 per α value
- For 9A-ii (Δα=0.02): window = ±0.010 per α value

Note: at very fine grid spacing the window is narrow and pair counts per bin may be sparse (~20–50 pairs per bin at n=1,000 zeros). Record per-bin pair counts alongside R(α) values — if counts fall below 10 at any α, flag those bins as low-confidence. This identifies whether 10,000+ zeros are needed for the empirical arm.

### Step 1: GUE Theoretical — 9A-i (Δα=0.05, n=300)

Compute R(α) = 1 − (sin(πα) / (πα))² at:
α = 0.05, 0.10, 0.15, ..., 15.0 (300 values)

Apply Chavez Transform:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: CV, conjugation symmetry, transform values [d1..d5].

### Step 2: Poisson — 9A-i

R(α) = 1.0 at all 300 α values. Apply Chavez Transform. Record.

### Step 3: Empirical Zeros — 9A-i

Compute empirical R(α) from `rh_zeros.json` at 300 α values (window ±0.025).
Record pair counts per bin. Apply Chavez Transform. Record.

### Step 4: GUE Theoretical — 9A-ii (Δα=0.02, n=750)

Compute R(α) = 1 − (sin(πα) / (πα))² at:
α = 0.02, 0.04, 0.06, ..., 15.0 (750 values)

Apply Chavez Transform. Record.

### Step 5: Poisson — 9A-ii

R(α) = 1.0 at all 750 values. Apply Chavez Transform. Record.

### Step 6: Empirical Zeros — 9A-ii

Compute empirical R(α) at 750 α values (window ±0.010). Record pair counts.
Apply Chavez Transform. Record.

### Step 7: Compile 9A Results

| Grid | n | GUE Sym | Poisson Sym | Empirical Sym | Separation | Δ Phase 8B |
|---|---|---|---|---|---|---|
| Δα=0.1 (Phase 8B baseline) | 150 | 94.1% | 100.0% | 87.5% | 12.5 pts | — |
| Δα=0.05 (9A-i) | 300 | | | | | |
| Δα=0.02 (9A-ii) | 750 | | | | | |

**Key question:** Does separation scale with n? Is there a saturation point?

**Secondary question:** Does the GUE theoretical symmetry score change significantly between grids? (Phase 8B: 96.7% at n=30 → 94.1% at n=150 — a decrease. Does it continue decreasing with finer grids?)

### Decision Framework — 9A

| Outcome | Interpretation |
|---|---|
| Separation continues scaling (>15 pts at n=300) | R(α) fine-grid is the strongest Chavez discriminator; predict separation at n=750 and document scaling law |
| Separation plateaus (~12.5 pts at n=300) | Pipeline saturating at current zero count; 10,000+ zeros needed for further gains |
| Separation decreases | Empirical R(α) becomes noisier at very fine grids with n=1,000 zeros; low-confidence bins are the bottleneck |
| Empirical pair counts < 10 at many bins | Document the minimum zero count needed for stable fine-grid computation; flag for Phase 10 with Odlyzko mega-zeros |

---

## Experiment 9C — Systematic Negative Delta: Height Band Characterization

### Motivation

The negative delta (actual zeros below GUE synthetic) has been confirmed across three experiments. The mechanism proposed is Berry-Keating prime-orbit corrections R_c = Σ cos(log p × t) — finite-height oscillatory corrections that systematically distort the zero spectrum away from pure GUE.

Phase 6 already measured the oscillatory Berry-Keating pattern at band resolution (10 bands × 100 zeros, height t=14–1419). That experiment used spacing ratio Chavez symmetry per band. The negative delta was visible in that data: most bands showed actual below GUE (mean delta −1.51 pts across all bands, Band 7 as outlier at −5.4 pts).

Phase 9B connects those two threads: **does the magnitude of the negative delta per band track the Berry-Keating R_c correction amplitude?**

If yes: the negative delta is not random noise — it has a specific phase structure determined by the prime spectrum. That would be the most direct empirical Berry-Keating result in the series.

### Berry-Keating R_c Background

At height t, the prime-orbit correction is:
```
R_c(t) = Σ_{primes p} A_p · cos(log(p) · t + φ_p)
```

At t~1000, N_eff ≈ 1.1 — corrections are large and non-averaging (Phase 6 established this). The dominant contributing primes are small: p=2,3,5,7,11... At these heights, cos(log(2)·t) oscillates with period 2π/log(2) ≈ 9.06. This means R_c changes sign roughly every 4.5 height units.

### Dataset

Use the 10 height bands from Phase 6:

| Band | Height Range | Zeros | Phase 6 Delta |
|---|---|---|---|
| 1 | 14–237 | 1–100 | −1.9 |
| 2 | 238–396 | 101–200 | +0.2 |
| 3 | 398–542 | 201–300 | −3.7 |
| 4 | 544–680 | 301–400 | −2.0 |
| 5 | 682–811 | 401–500 | −3.2 |
| 6 | 812–937 | 501–600 | +1.5 |
| 7 | 940–1063 | 601–700 | −5.4 |
| 8 | 1064–1184 | 701–800 | +1.4 |
| 9 | 1185–1302 | 801–900 | +1.1 |
| 10 | 1303–1419 | 901–1000 | −3.1 |

For each band: extract 100 zeros → 99 gaps → 98 spacing ratios. Apply Chavez Transform (pattern_id=1). Generate GUE synthetic (Wigner surmise, mean-matched to band mean gap, seed 1). Compute delta (actual − GUE).

### Step 9: Per-Band Spacing Ratio Analysis

For each of the 10 bands:
1. Extract zeros[band_start..band_end] from `rh_zeros.json`
2. Compute 99 gaps → 98 spacing ratios
3. Compute band mean gap (for GUE mean-matching)
4. Run Chavez Transform on 98 ratios: alpha=1.0, dimension_param=2, pattern_id=1, dimensions=1–5
5. Generate GUE Wigner surmise gaps (mean=band_mean_gap, seed 1) → 98 ratios → Chavez Transform
6. Record: actual symmetry, GUE symmetry, delta

### Step 10: Compute R_c Phase per Band

For each band, compute the dominant prime-orbit correction phase using the band midpoint height t_mid:

```
R_c_dominant(t) = cos(log(2) · t_mid)    [p=2 term, dominant at t~100-1400]
```

Record R_c_dominant per band alongside the actual delta.

| Band | t_mid | R_c_dominant = cos(log2 × t_mid) | Actual Delta | Correlation? |
|---|---|---|---|---|
| 1 | ~125 | | | |
| 2 | ~317 | | | |
| 3 | ~470 | | | |
| 4 | ~612 | | | |
| 5 | ~747 | | | |
| 6 | ~875 | | | |
| 7 | ~1002 | | | |
| 8 | ~1124 | | | |
| 9 | ~1244 | | | |
| 10 | ~1361 | | | |

### Step 11: Correlation Test

Compute the Pearson correlation coefficient between:
- R_c_dominant values (10 band values)
- Actual delta values (10 band values)

**Key question:** Is there a statistically significant correlation between the prime-orbit correction phase and the measured negative delta magnitude?

### Decision Framework — 9B

| Outcome | Interpretation |
|---|---|
| Strong positive correlation (r > 0.6) | **Berry-Keating mechanism confirmed at bilateral symmetry level** — prime-orbit corrections directly drive the negative delta oscillation |
| Moderate correlation (0.3 < r < 0.6) | Partial Berry-Keating signature; higher-order prime terms (p=3,5,...) needed for full model |
| Near-zero correlation | Negative delta is height-independent; arithmetic structure breaks GUE symmetry uniformly regardless of prime-orbit phase |
| Strong negative correlation | Phase relationship is inverted; mechanism exists but sign convention needs checking |

---

## Results Template

```json
{
  "experiment_id": "RH_UF_2026_001",
  "date": "2026-03-08",
  "phases": {
    "9A_ultra_fine_pair_correlation": {
      "grids": {
        "delta_alpha_005_n300": {
          "gue_theoretical": {"chavez_sym": null, "cv": null},
          "poisson_flat": {"chavez_sym": null, "cv": null},
          "empirical_zeros": {
            "chavez_sym": null,
            "cv": null,
            "min_bin_pair_count": null,
            "low_confidence_bins": null
          },
          "separation_pts": null
        },
        "delta_alpha_002_n750": {
          "gue_theoretical": {"chavez_sym": null, "cv": null},
          "poisson_flat": {"chavez_sym": null, "cv": null},
          "empirical_zeros": {
            "chavez_sym": null,
            "cv": null,
            "min_bin_pair_count": null,
            "low_confidence_bins": null
          },
          "separation_pts": null
        }
      },
      "scaling_law": null,
      "saturation_detected": null
    },
    "9B_negative_delta_characterization": {
      "bands": [
        {"band": 1, "t_mid": 125, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 2, "t_mid": 317, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 3, "t_mid": 470, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 4, "t_mid": 612, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 5, "t_mid": 747, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 6, "t_mid": 875, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 7, "t_mid": 1002, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 8, "t_mid": 1124, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 9, "t_mid": 1244, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null},
        {"band": 10, "t_mid": 1361, "rc_dominant": null, "actual_sym": null, "gue_sym": null, "delta": null}
      ],
      "pearson_r_delta_vs_rc": null,
      "berry_keating_confirmed": null
    }
  },
  "key_findings": {
    "9A": null,
    "9B": null,
    "combined": null
  }
}
```

---

## Development Requirement: CAILculator vector_data Input

**This is not an experiment — it is a specification for the next CAILculator development sprint.**

Phase 7B and 8A confirmed that the 1D invariance theorem is encoding-independent. The only path to Color Group / E8 geometry activation is a kernel-level change: a new `vector_data` input type accepting n×2 (or n×k) arrays, where each row is a multi-dimensional vector processed by each Canonical Six pattern as a genuine vector projection rather than a scalar contraction.

**Specification:**
- Input: n×2 array where row i is [g_i, g_{i+1}] (consecutive gap pair as 2D vector)
- Each pattern applies its P-vector projection to the 2D vector, not to a scalar
- Output: per-pattern transform values, conjugation symmetry, CV
- Expected behavior: patterns within same Color Group produce similar values; patterns across Color Groups produce different values

**Validation test once implemented:**
Run on 98 gap pairs from zeros 1–99, all 6 patterns. If values differ across patterns, the invariance is broken. Check Color Group clustering. Run same test on GUE synthetic. Compare.

This development sprint unlocks Phase 10's primary experiment.

---

## Cumulative Separation Record

| Phase | Method | n | Separation |
|---|---|---|---|
| 5 | Spacing ratios | 499 | 7.2 pts |
| 7A | R(α) coarse | 30 | 6.9 pts |
| 8B | R(α) fine | 150 | **12.5 pts** |
| 9A-i | R(α) ultra-fine | 300 | predicted 14–16 pts |
| 9A-ii | R(α) ultra-fine | 750 | predicted 16–20 pts |

---

## Files Referenced

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 zeros (9A empirical; 9B band analysis) |
| `rh_gaps.json` | 999 gaps |
| `rh_phase8_results.json` | Phase 8 baseline — 12.5 pt record, systematic negative delta |
| `rh_height_band_results.json` | Phase 6 band data — Berry-Keating oscillation reference |
| `RH_Phase9_Handoff.md` | This document |
| `RH_Investigation_Roadmap.md` | Full roadmap |

---

## After the Session

Save as `rh_phase9_results.json` (template above).
Save summary as `RH_Phase9_Results.md`.
Update `RH_Investigation_Roadmap.md` Phase 9 row.

**If 9B yields r > 0.6:** the Berry-Keating R_c mechanism is empirically confirmed at bilateral symmetry level. This is a paper-quality result — add to ChavezTransform_Paper_Draft.md Section 7 immediately.

**If 9A separation exceeds 15 pts:** document the scaling law and project the zero count needed for 20 pt separation.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
