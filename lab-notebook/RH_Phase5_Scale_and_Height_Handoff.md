# RH Phase 5 — Scale Test and Higher Zeros

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-04
**Experiment ID:** RH_SCALE_2026_001
**Prerequisite:** RH Phase 4 complete (rh_spacing_ratio_results.json)

---

## Context

Phase 4 established:
- Mean spacing ratio 0.610 = GUE fingerprint on zeros 1–99 (pre-Chavez, arithmetic)
- Chavez on spacing ratios achieves correct ordering: GUE (76.9%) > actual (75.0%) > Poisson (71.6%)
- GUE/Poisson Chavez separation = 5.3 pts at n=99
- Actual zeros score 1.9 pts below GUE synthetic — expected for the low-height regime

**Two open questions this session answers:**

**Question A (Scale):** Does the Chavez GUE/Poisson separation *widen* with more data? At n=99 it just cleared the 5-pt threshold. At n=499 or n=999, does it become a stronger, cleaner signal?

**Question B (Height):** Do zeros 500–599 (higher in the critical strip, more asymptotically GUE) score closer to GUE synthetic on Chavez? The 1.9-pt gap between actual (75.0%) and GUE (76.9%) in Phase 4 should narrow if the low-height regime was the cause.

---

## Part A — Scale Test

### Dataset
`rh_gaps.json` — 999 gaps. Compute spacing ratios at four scales:
- n=99 gaps → 98 ratios (Phase 4 baseline, re-confirm)
- n=249 gaps → 248 ratios
- n=499 gaps → 498 ratios
- n=999 gaps → 998 ratios

### Step A1: Actual Zero Spacing Ratios at All Four Scales

For each scale, load first n gaps from `rh_gaps.json`, compute n−1 spacing ratios, run Chavez Transform (alpha=1.0, dimension_param=2, pattern_id=1, dimensions 1–5).

Record per scale: mean ratio, Chavez symmetry, CV.

### Step A2: GUE and Poisson Controls at n=499 (3 trials each)

To measure whether the GUE/Poisson *separation* widens with scale, run fresh controls at the largest practical scale:
- Poisson: Exponential(mean = actual mean gap of first 499 gaps — compute from data)
- GUE: Wigner surmise scaled to same mean
- Seeds 1, 2, 3 each

Record: mean ratio and Chavez symmetry per trial, means across trials.

**Key comparison:** GUE/Poisson separation at n=499 vs 5.3 pts at n=99. If it widens to 8–10+ pts, the pipeline strengthens with scale.

---

## Part B — Higher Zeros Test

### Dataset
`rh_zeros.json` — load zeros indexed 499–598 (0-indexed), i.e., the 500th through 599th zeros. Compute 99 gaps between them → 98 spacing ratios.

These zeros are higher in the critical strip (~imaginary parts 700–800 range), where the asymptotic GUE behavior is better established. Deviations from GUE in Phase 4 were attributed to the low-height regime of zeros 1–99.

### Step B1: Compute Mean Gap for Zeros 500–599

First compute: what is the mean gap between consecutive zeros in this range? This sets the mean for the synthetic controls.

### Step B2: Actual Spacing Ratios for Zeros 500–599

Compute 98 spacing ratios from the 99 gaps. Record mean ratio. Run Chavez Transform. Record symmetry and CV.

**Expected:** Mean ratio closer to GUE theoretical (~0.60) than Phase 4's 0.610 (already close), and Chavez symmetry closer to GUE synthetic (76.9%) than Phase 4's actual (75.0%).

### Step B3: GUE and Poisson Controls for Higher Zeros (3 trials each)

- Poisson: Exponential(mean = mean gap of zeros 500–599)
- GUE: Wigner surmise scaled to same mean
- Seeds 1, 2, 3 each

Record: mean ratio and Chavez symmetry per trial, means.

**Key comparison:** Does actual zeros 500–599 score closer to GUE synthetic than zeros 1–99 did? Does the 1.9-pt gap (actual vs GUE) narrow?

---

## Results Template

```json
{
  "experiment_id": "RH_SCALE_2026_001",
  "date": "2026-03-04",
  "part_a_scale_test": {
    "actual_zeros_by_scale": {
      "n99":  {"mean_ratio": null, "chavez_symmetry": null, "cv": null},
      "n249": {"mean_ratio": null, "chavez_symmetry": null, "cv": null},
      "n499": {"mean_ratio": null, "chavez_symmetry": null, "cv": null},
      "n999": {"mean_ratio": null, "chavez_symmetry": null, "cv": null}
    },
    "controls_at_n499": {
      "actual_mean_gap": null,
      "poisson": {
        "trials": [
          {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
          {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
          {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
        ],
        "mean_symmetry": null
      },
      "gue_wigner": {
        "trials": [
          {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
          {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
          {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
        ],
        "mean_symmetry": null
      },
      "gue_poisson_separation_pts": null
    }
  },
  "part_b_higher_zeros": {
    "zero_index_range": "499-598 (0-indexed), zeros 500-599",
    "actual_mean_gap": null,
    "actual_zeros_500_599": {
      "mean_ratio": null,
      "chavez_symmetry": null,
      "delta_vs_phase4_actual": null
    },
    "poisson_controls": {
      "trials": [
        {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
      ],
      "mean_symmetry": null
    },
    "gue_controls": {
      "trials": [
        {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
      ],
      "mean_symmetry": null
    },
    "actual_vs_gue_gap_pts": null,
    "comparison_to_phase4": null
  }
}
```

---

## Decision Framework

### Part A — Scale Test

| Outcome | Interpretation |
|---|---|
| GUE/Poisson separation widens (>8 pts at n=499) | Pipeline strengthens with scale — strong tool claim |
| Separation stable (~5 pts) | Tool works but doesn't improve with n — ceiling at n=99 |
| Separation narrows | Something unexpected — investigate |
| Actual zeros track toward GUE as n grows | Asymptotic GUE behavior emerging with more data |

### Part B — Higher Zeros

| Outcome | Interpretation |
|---|---|
| Actual 500–599 closer to GUE (gap < 1.9 pts) | Low-height regime explained Phase 4 shortfall — confirmed |
| Actual 500–599 farther from GUE | Unexpected — low-height was not the cause |
| Mean ratio rises above 0.610 | Zeros become more GUE-like at higher heights — asymptotic convergence |

---

## Files in This Directory

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 zero positions (use indices 499–598 for Part B) |
| `rh_gaps.json` | 999 gaps (use first 99/249/499/999 for Part A) |
| `rh_spacing_ratio_results.json` | Phase 4 results (baseline) |
| `RH_Phase4_SpacingRatio_Results.md` | Phase 4 full results |
| `RH_Phase5_Scale_and_Height_Handoff.md` | This document |
| `CLAUDE.md` | Repository guidance |
