# RH Phase 2b — Gap Sequence Discriminability Test

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-04
**Experiment ID:** RH_GAP_2026_001
**Prerequisite:** RH Phase 1 (rh_experiment_results.json) and RH Phase 2 control test (rh_ctrl_experiment_results.json) both complete

---

## Context

**Phase 1 confirmed result:** Chavez conjugation symmetry on the first 99 Riemann zero gaps = **83.8%**. This places Riemann zero gaps in the GUE/structured-prime range (78–86%), consistent with Montgomery-Dyson.

**Phase 2 control test result:** ZDTP convergence at n=16 on raw positions is non-discriminating — any monotone 16-element sequence scores ~97–99%. The meaningful metric is Chavez symmetry on gaps.

**The open question:** Is the 83.8% Chavez symmetry signal coming from the *ordering* of the gaps (i.e., the specific sequence of gap values), or just from the *distribution* of gap sizes (i.e., which gap values appear, regardless of order)? These are structurally different claims:

- If ordering matters → the sequential structure of the zero gaps carries bilateral symmetry. This is a stronger result, more consistent with AIEX-001.
- If ordering does not matter → the result reflects gap size statistics only. Weaker, but still a real signal distinguishing zeros from uniform random.

This experiment answers that question directly.

---

## Datasets

All data is pre-computed. Load from files — do not recompute zeros.

| File | Contents | Use |
|---|---|---|
| `rh_gaps.json` | 999 gaps between consecutive zeros | Primary dataset |
| `rh_zeros.json` | 1,000 zero positions | Reference only |

For all analyses in this experiment, use **the first 99 gaps from rh_gaps.json** unless otherwise specified (this matches the Phase 1 baseline).

---

## Analysis Steps

### Step 1: Re-baseline — Chavez Transform on First 99 Gaps (Unshuffled)

Load `rh_gaps.json`, take the first 99 values. Run Chavez Transform:

- alpha: 1.0, dimension_param: 2, pattern_id: 1
- dimensions: 1, 2, 3, 4, 5

This re-confirms the Phase 1 baseline in this session before any shuffling.

Record: CV, conjugation symmetry (expecting 83.8%), dimensional persistence, transform values at dims 1–5.

---

### Step 2: Shuffle Test — Chavez on Shuffled Gaps (3 trials)

Take the same 99 gaps from Step 1. Shuffle the order randomly (do not change the values — only reorder them). Run Chavez Transform on the shuffled sequence.

Repeat with **3 different random shuffles** (seeds 1, 2, 3) to get a stable estimate.

For each trial, record: conjugation symmetry.

Then compute: mean shuffled symmetry across 3 trials.

**The discriminating comparison:**
- If mean shuffled symmetry ≈ 83.8%: ordering does not matter — the signal is in gap size distribution only
- If mean shuffled symmetry < 83.8% (significantly): ordering matters — the sequential structure of the gaps carries bilateral symmetry beyond what the distribution alone provides
- Threshold: "significantly lower" = more than 5 percentage points below 83.8% (i.e., below ~79%)

---

### Step 3: Synthetic Gap Control — Exponential Distribution (3 trials)

**Mean correction (discovered in-session):** The first 99 actual zero gaps have mean = **2.246**, not 1.41. The value 1.41 is the mean of all 999 gaps. Run two sub-variants:

- **Step 3A:** Exponential(mean=1.41) — original handoff spec; structurally different distribution (smaller gaps)
- **Step 3B:** Exponential(mean=2.246) — matches actual 99-gap mean; fair comparison

Generate 99 synthetic gaps for each, run Chavez Transform (same parameters). Repeat with seeds 1, 2, 3.

Record: conjugation symmetry per trial and mean, for both 3A and 3B.

**The discriminating comparison:**
- 3B (mean-matched) is the fair comparison: if 3B symmetry < 83.8% by >5 pts, Chavez detects GUE correlations beyond exponential with the correct mean
- 3A (1.41) will differ in scale — differences may reflect scale mismatch, not GUE structure; use as secondary reference
- Threshold: "substantially lower" = more than 5 percentage points below 83.8%

---

### Step 4: Scale Invariance — Chavez on First 100, 500, and 999 Gaps

Load `rh_gaps.json`. Run Chavez Transform on three gap subsets:

- **n=99** (first 99 gaps) — Phase 1 baseline, confirm here
- **n=499** (first 499 gaps)
- **n=999** (all 999 gaps)

Same parameters for all three runs.

Record: conjugation symmetry, CV, dimensional persistence at each scale.

**The discriminating comparison:**
- If symmetry stays near 83.8% across all three scales: the result is scale-stable — a strong structural signal
- If symmetry drifts significantly: the 83.8% is a sample-size artifact of the first 99 zeros specifically

---

## Results Template

```json
{
  "experiment_id": "RH_GAP_2026_001",
  "date": "2026-03-04",
  "analyses": {
    "baseline_99_gaps": {
      "source": "rh_gaps.json, first 99 values, unshuffled",
      "chavez": {
        "cv": null,
        "conjugation_symmetry": null,
        "dimensional_persistence": null,
        "transform_values": [null, null, null, null, null]
      }
    },
    "shuffle_test": {
      "source": "rh_gaps.json, first 99 values, shuffled",
      "trials": [
        {"seed": 1, "conjugation_symmetry": null},
        {"seed": 2, "conjugation_symmetry": null},
        {"seed": 3, "conjugation_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_baseline": null
    },
    "synthetic_exponential_gaps": {
      "distribution": "Exponential(mean=1.41)",
      "n": 99,
      "trials": [
        {"seed": 1, "conjugation_symmetry": null},
        {"seed": 2, "conjugation_symmetry": null},
        {"seed": 3, "conjugation_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_baseline": null
    },
    "scale_invariance": {
      "n99":  {"chavez_symmetry": null, "cv": null, "dimensional_persistence": null},
      "n499": {"chavez_symmetry": null, "cv": null, "dimensional_persistence": null},
      "n999": {"chavez_symmetry": null, "cv": null, "dimensional_persistence": null}
    }
  },
  "key_findings": {
    "ordering_matters": null,
    "exponential_separates": null,
    "scale_stable": null,
    "interpretation": null
  }
}
```

---

## Decision Matrix

After recording all results, classify each finding:

| Test | Result | Interpretation |
|---|---|---|
| Shuffle drops >5 pts | Ordering matters | Sequential gap structure carries bilateral symmetry — stronger GUE signal |
| Shuffle stays near 83.8% | Ordering irrelevant | Signal is in gap size distribution only |
| Synthetic Exp. separates >5 pts | GUE structure detectable | Chavez symmetry distinguishes GUE gaps from exponential gaps — key discriminability result |
| Synthetic Exp. near 83.8% | Exponential suffices | 83.8% is explained by mean gap rate, not GUE correlations |
| Scale invariant across n=99/499/999 | Stable signal | 83.8% is not a small-sample artifact |
| Symmetry drifts with scale | Sample artifact | Baseline n=99 result may not generalize |

The strongest possible outcome: shuffle drops symmetry + synthetic Exp. is lower + scale invariant. That combination would mean: (1) gap ordering carries structure, (2) Chavez distinguishes GUE from Poisson, and (3) the result is not a small-n artifact. That would be a clear, discriminating result pointing toward genuine GUE algebraic structure in the zero sequence.

---

## Files in This Directory

| File | Purpose |
|---|---|
| `rh_gaps.json` | 999 zero gaps — primary input for this experiment |
| `rh_zeros.json` | 1,000 zero positions (reference) |
| `rh_experiment_results.json` | Phase 1 results (baseline: 83.8%) |
| `rh_ctrl_experiment_results.json` | Phase 2 control results (ZDTP non-discriminating) |
| `RH_Phase2b_Gap_Discriminability_Handoff.md` | This document |
| `CLAUDE.md` | Repository guidance |
