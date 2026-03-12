# RH Phase 3 — GUE Fingerprint Test

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-04
**Experiment ID:** RH_GUE_2026_001
**Prerequisite:** RH Phase 2b complete (rh_gap_experiment_results.json)

---

## Context

Three experiments completed on March 4, 2026 have established:

1. **83.8% Chavez symmetry on zero gaps is real and scale-stable** — rises to 86.2% at n=249, not a small-n artifact
2. **Ordering is irrelevant** — shuffling the gaps leaves symmetry unchanged; the signal is in the gap *size distribution*, not sequential structure
3. **ZDTP at n=16 is non-discriminating** — the 98.7% Phase 1 result was a monotonicity artifact

**The open question:** Is the 83.8% specifically detecting GUE level repulsion, or just coarse gap statistics?

GUE (Gaussian Unitary Ensemble) gap distribution differs from Poisson (exponential) in a specific, measurable way: **level repulsion**. GUE has quadratic suppression of small gaps — P(s) → 0 as s → 0 — while Poisson has maximum density at s = 0. This produces a more "balanced" gap distribution in GUE, with fewer very small and very large gaps relative to mean. If Chavez conjugation symmetry is detecting level repulsion, it should score:

```
GUE gaps > Actual zero gaps ≈ Poisson gaps
```

or more precisely:

```
Actual zero gaps ≈ GUE gaps > Poisson gaps (mean-matched)
```

This experiment tests exactly that.

---

## Datasets

| File | Contents |
|---|---|
| `rh_gaps.json` | 999 actual zero gaps — use first 99 for baseline |

All synthetic sequences are generated in-session. Use random seed 42 for all unless otherwise specified.

**Key parameter:** actual first 99 zero gaps have **mean = 2.25** (rounded from 2.246). All synthetic controls use this mean for fair comparison.

---

## Analysis Steps

### Step 1: Re-baseline — Actual 99 Zero Gaps

Load `rh_gaps.json`, take first 99 values. Run Chavez Transform:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: CV, conjugation symmetry (expecting 83.8%), transform values.

This re-confirms the baseline in this session.

---

### Step 2: Poisson Control — Exponential(mean=2.25), 3 trials

Generate 99 gaps from an Exponential distribution with **mean = 2.25** (correctly matched to actual gap mean). Seeds 1, 2, 3.

Run Chavez Transform on each gap sequence (not accumulated positions — the gap values themselves). Same parameters as Step 1.

Record: conjugation symmetry per trial, mean across 3 trials.

This is the corrected version of the Phase 2b synthetic control, which used mean=1.41 (the full 999-gap mean, a 59% mismatch). This result is the true Poisson baseline.

---

### Step 3: GUE Control — Wigner Surmise, 3 trials

Generate 99 gaps from the GUE nearest-neighbor spacing distribution (Wigner surmise):

```
P(s) = (32/π²) * s² * exp(−4s²/π)
```

This distribution has mean = 1 (normalized). To match actual gap mean of 2.25, **scale each drawn value by 2.25** after sampling.

Generation method — use whichever is available:
- **Rejection sampling**: propose s from Uniform(0, 6), accept with probability P(s)/P_max where P_max ≈ 0.64 (at s ≈ 0.79)
- **If scipy available**: use `scipy.stats` or rejection sampling from a gamma or chi-squared envelope
- **Simple approximation**: the GUE Wigner surmise is closely approximated by a scaled chi distribution with k=3 (3 degrees of freedom), mean = √(2) * Γ(2)/Γ(3/2) ≈ 1.596; scale to match mean=2.25

Seeds 1, 2, 3. Run Chavez Transform on each gap sequence. Same parameters.

Record: conjugation symmetry per trial, mean across 3 trials.

---

### Step 4: Compile and Interpret

After all steps, fill in the comparison table and apply the decision framework below.

---

## Results Template

```json
{
  "experiment_id": "RH_GUE_2026_001",
  "date": "2026-03-04",
  "gap_mean_actual_n99": 2.25,
  "analyses": {
    "baseline_actual_gaps": {
      "source": "rh_gaps.json, first 99",
      "chavez_symmetry": null,
      "cv": null,
      "transform_values": [null, null, null, null, null]
    },
    "poisson_exponential_mean225": {
      "mean": 2.25,
      "trials": [
        {"seed": 1, "chavez_symmetry": null},
        {"seed": 2, "chavez_symmetry": null},
        {"seed": 3, "chavez_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_baseline": null
    },
    "gue_wigner_surmise_mean225": {
      "distribution": "P(s) = (32/pi^2) * s^2 * exp(-4s^2/pi), scaled to mean=2.25",
      "trials": [
        {"seed": 1, "chavez_symmetry": null},
        {"seed": 2, "chavez_symmetry": null},
        {"seed": 3, "chavez_symmetry": null}
      ],
      "mean_symmetry": null,
      "delta_from_baseline": null
    }
  },
  "key_findings": {
    "poisson_separates": null,
    "gue_matches_zeros": null,
    "interpretation": null
  }
}
```

---

## Decision Framework

After recording results, apply this logic:

| Outcome | Interpretation |
|---|---|
| GUE ≈ actual zeros > Poisson (by >5 pts) | **Chavez fingerprints GUE level repulsion** — strong result; the zero gap distribution is specifically GUE-like, not just Poisson-like |
| GUE > actual zeros > Poisson (all >5 pt gaps) | Chavez detects level repulsion; actual zeros are between GUE and Poisson (possible finite-sample effect) |
| Actual zeros > GUE ≈ Poisson | Something else explains 83.8% — not level repulsion; investigate other distributional features |
| All three ≈ same score | Chavez detects only coarse gap statistics (mean/variance); level repulsion is not visible at n=99 |
| GUE < actual zeros | Unexpected — would suggest zeros have more bilateral structure than ideal GUE predicts |

**The target outcome:** GUE and actual zeros both score near 83.8%, while Poisson (exponential mean=2.25) scores significantly lower. That would confirm Chavez is detecting the GUE distributional signature — level repulsion — and that Riemann zero gaps match GUE gaps on this metric.

**Significance for AIEX-001:** If confirmed, this means the Chavez measure is detecting the same distributional property that distinguishes GUE from Poisson — quadratic level repulsion. That is the spectral signature of a Hermitian operator. It does not prove AIEX-001 (the Hilbert-Pólya conjecture in sedenion space) but it places the Chavez result in the correct spectral-theory context.

---

## Files in This Directory

| File | Purpose |
|---|---|
| `rh_gaps.json` | 999 zero gaps (use first 99) |
| `rh_gap_experiment_results.json` | Phase 2b results (baseline: 83.8%, ordering irrelevant) |
| `RH_Phase2b_Gap_Discriminability_Results.md` | Phase 2b full results |
| `RH_Phase3_GUE_Fingerprint_Handoff.md` | This document |
| `CLAUDE.md` | Repository guidance |
