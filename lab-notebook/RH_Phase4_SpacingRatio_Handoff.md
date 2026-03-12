# RH Phase 4 — Spacing Ratio GUE Fingerprint Test

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-04
**Experiment ID:** RH_SR_2026_001
**Prerequisite:** RH Phase 3 complete (rh_gue_experiment_results.json)

---

## Why This Experiment

Phase 3 showed that Chavez conjugation symmetry on raw gap values cannot distinguish GUE from Poisson — both score ~79–80%, while actual zeros score 83.4%. The signal turned out to be lower-bound compactness (the actual gaps have a floor near 0.72), not GUE eigenvalue statistics.

The problem: raw gap values lose ordering information, and the Chavez measure is ordering-invariant (Phase 2b confirmed this). GUE's key distinguishing feature — pair correlations, level repulsion — is visible only in statistics that use consecutive gap relationships.

**The spacing ratio statistic** solves this:

```
rₙ = min(gₙ, gₙ₊₁) / max(gₙ, gₙ₊₁)
```

where gₙ is the n-th gap. Each rₙ compares two adjacent gaps. The ratio is always in [0, 1]:
- rₙ → 1 means two consecutive gaps are nearly equal in size (regular, GUE-like)
- rₙ → 0 means one gap is much larger than the other (irregular, Poisson-like)

**Why this separates GUE from Poisson:**
- **GUE**: level repulsion pushes gaps to be more uniform in size. Consecutive gaps tend to be similar → rₙ distribution peaks toward 1, mean ~0.60
- **Poisson**: exponential gaps have high variance; consecutive gaps are often mismatched → rₙ distribution piled near 0, mean ~0.39

**Why this works with Chavez:** The spacing ratio is ordering-dependent (requires consecutive pairs) — it captures exactly what raw gap values miss. If Chavez symmetry on rₙ values scores GUE higher than Poisson, and actual zeros match GUE, that is the GUE fingerprint.

**Important:** The spacing ratio does not require unfolding (normalizing by local density) — a known source of artifacts. It is a clean, artifact-resistant GUE test.

---

## Datasets

| File | Contents |
|---|---|
| `rh_gaps.json` | 999 actual zero gaps |

Use first 99 gaps → compute 98 spacing ratios (each ratio requires two adjacent gaps).

All synthetic sequences: generate 99 gaps → compute 98 ratios. Same process.

**Key parameters:**
- Actual n=99 gap mean: 2.25
- All synthetic controls use mean=2.25
- n for Chavez input: 98 ratio values (not 99)

---

## Analysis Steps

### Step 1: Compute Actual Spacing Ratios + Chavez Baseline

Load `rh_gaps.json`, take first 99 values. Compute 98 spacing ratios:

```
for i in 0..97:
    r[i] = min(gaps[i], gaps[i+1]) / max(gaps[i], gaps[i+1])
```

Record the 98 ratio values. Note the mean and range.

Run Chavez Transform on the 98 ratio values:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: CV, conjugation symmetry, dimensional persistence, transform values.

---

### Step 2: Poisson Spacing Ratios — 3 trials

Generate 99 gaps from Exponential(mean=2.25), seeds 1, 2, 3. Compute 98 spacing ratios from each. Run Chavez Transform on each ratio sequence.

Record: symmetry per trial, mean across 3 trials, mean ratio value per trial.

---

### Step 3: GUE Wigner Surmise Spacing Ratios — 3 trials

Generate 99 gaps from the GUE Wigner surmise P(s) = (32/π²)s²exp(−4s²/π), scaled to mean=2.25. Seeds 1, 2, 3. Compute 98 spacing ratios from each. Run Chavez Transform.

Record: symmetry per trial, mean across 3 trials, mean ratio value per trial.

---

### Step 4: Compile and Interpret

---

## Results Template

```json
{
  "experiment_id": "RH_SR_2026_001",
  "date": "2026-03-04",
  "statistic": "spacing ratio r_n = min(g_n, g_{n+1}) / max(g_n, g_{n+1})",
  "n_gaps": 99,
  "n_ratios": 98,
  "analyses": {
    "actual_zeros": {
      "mean_ratio": null,
      "ratio_range": [null, null],
      "chavez_symmetry": null,
      "cv": null,
      "transform_values": [null, null, null, null, null]
    },
    "poisson_exp_mean225": {
      "trials": [
        {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_actual": null
    },
    "gue_wigner_mean225": {
      "trials": [
        {"seed": 1, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 2, "mean_ratio": null, "chavez_symmetry": null},
        {"seed": 3, "mean_ratio": null, "chavez_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_actual": null
    }
  }
}
```

---

## Decision Framework

| Outcome | Interpretation |
|---|---|
| Actual ≈ GUE >> Poisson (>5 pts) | **GUE fingerprint confirmed** — Chavez detects GUE spacing regularity via the ratio statistic |
| Actual > GUE > Poisson (all >3 pts) | GUE partially detected; actual zeros more regular than ideal GUE predicts |
| GUE ≈ Poisson, actual above both | Same situation as Phase 3 — ratio statistic also fails to separate; need pair correlation |
| All three similar | Chavez symmetry is insensitive to this statistic at n=98 |
| Actual < GUE or Actual < Poisson | Unexpected — would indicate actual zero gaps are less regular than synthetic |

**Expected mean ratio values (theoretical):**
- GUE: ~0.60 (gaps more uniform → higher ratios)
- Poisson: ~0.39 (high gap variance → more mismatched consecutive pairs)
- Actual zeros: unknown — if GUE-like, should be closer to 0.60

The mean ratio itself is a quick pre-check: if actual zeros cluster near GUE's 0.60, that alone confirms GUE spacing regularity before Chavez runs.

---

## Files in This Directory

| File | Purpose |
|---|---|
| `rh_gaps.json` | 999 zero gaps (use first 99) |
| `rh_gue_experiment_results.json` | Phase 3 results (GUE ≈ Poisson on raw gaps) |
| `RH_Phase3_GUE_Results.md` | Phase 3 full results |
| `RH_Phase4_SpacingRatio_Handoff.md` | This document |
| `CLAUDE.md` | Repository guidance |
