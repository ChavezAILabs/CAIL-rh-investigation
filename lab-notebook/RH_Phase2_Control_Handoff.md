# Experiment RH Phase 2 — ZDTP Discriminability Control Test

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-04
**Roadmap Reference:** Phase 3 (Riemann Hypothesis Connection) — Phase 2 follow-on to RH-1
**Prerequisite:** RH Phase 1 complete (`rh_experiment_results.json`)

---

## Objective

Phase 1 found that the first 16 Riemann zero imaginary parts, packed into a 16D sedenion vector, achieve **98.7% ZDTP convergence** — matching deterministic sequences (Powers of 2, Fibonacci). The gap sequence scores 83.8% on Chavez conjugation symmetry, placing it in the GUE/prime range.

**The open question:** Is the 98.7% ZDTP score *specific* to Riemann zeros, or does ZDTP score any monotone-increasing sequence in the same range that high?

This experiment resolves that question by running ZDTP and Chavez Transform on three synthetic control sequences — all in the range (14, 1419), all 16 elements — alongside the actual first 16 Riemann zeros. If the controls also score ~98%, ZDTP is measuring range properties, not Riemann zero structure. If the controls score lower, the 98.7% is genuinely discriminating.

---

## Background: Phase 1 Bifurcation Finding

| Metric | Dataset | Score | Category |
|---|---|---|---|
| Chavez conjugation symmetry | Riemann zero gaps (99 pts) | 83.8% | GUE / structured prime range |
| ZDTP convergence | Zero positions (16D vector) | **98.7%** | Deterministic sequence territory |
| Chavez conjugation symmetry | Random float baseline | 0.0% | Clean null |

Two structural axes measuring different things:
- **Chavez symmetry** = local relational structure (bilateral symmetry in gaps)
- **ZDTP convergence** = global positional stability (how absolute values transmit through sedenion dimensional layers)

The 98.7% on positions is the striking result. This experiment tests whether it reflects genuine Riemann zero structure.

---

## Actual Dataset

**Source:** `rh_zeros.json` (1,000 zeros, already computed)
**Input for this experiment:** First 16 values from `rh_zeros.json`

Approximate values (mpmath mp.dps=25):

```
[14.1347, 21.0220, 25.0109, 30.4249, 32.9351,
 37.5862, 40.9187, 43.3271, 48.0052, 49.7738,
 52.9703, 56.4462, 59.3470, 60.8318, 65.1125, 67.0798]
```

Load these from `rh_zeros.json` rather than typing manually — use the first 16 elements.

---

## Synthetic Control Sequences

All controls are 16-element sequences constrained to the range (14, 1419). Generate each synthetically — do not use the Riemann zero data. The goal is plausible alternative sequences that a naive ZDTP analysis might score equally well.

### Control A: Growth Formula with Noise

Approximate the zero distribution using the asymptotic formula y ≈ 2πn/log(n) for n = 1..16, then add 10% Gaussian noise. This gives the same global growth shape as the actual zeros, with randomized local structure.

```
a(n) = 2 * pi * n / log(n)   for n = 1..16
a(n) += gaussian_noise(mean=0, sigma=0.10 * a(n))   (10% noise)
```

Fix a random seed for reproducibility (seed = 42). Record the exact 16 values used.

**Rationale:** Tests whether the growth profile of Riemann zeros (not their precise positions) is what ZDTP detects. If ZDTP scores Control A ~98.7%, it is only seeing the sub-linear growth shape, not Riemann-specific structure.

### Control B: Poisson Gaps (Exponential Distribution)

Simulate a sequence where consecutive gaps follow an exponential distribution matching the overall mean zero spacing, but without any growth structure or GUE correlations:

```
Start at 14.13
gaps ~ Exponential(mean = 1.42)  [matching average zero spacing across all 1,000 zeros]
Accumulate: b(n) = b(n-1) + gap(n)
```

Mean ≈ 1.42 is the mean gap for the full 1,000-zero dataset ((1419.42 - 14.13) / 999 ≈ 1.406). Fix random seed = 42. Record the exact 16 values used.

**Rationale:** Exponential gaps with the correct mean spacing preserve global density statistics but discard all GUE pair correlations and long-range rigidity. If ZDTP scores this high, it is detecting mean gap rate only.

### Control C: Uniform (Linear Growth)

Evenly spaced 16 points from 14.13 to the 16th actual Riemann zero's position (~67.08):

```
c(n) = 14.13 + (67.08 - 14.13) * (n - 1) / 15
for n = 1, 2, ..., 16
```

No randomness — fully deterministic, perfectly regular. Spans the same range as the actual first 16 zeros.

**Rationale:** The simplest possible monotone sequence in the same range. If ZDTP scores this ~98.7%, the high convergence result is uninformative — any evenly-spaced sequence would score as high. If ZDTP scores this significantly lower, the actual zeros have structure beyond mere linear spacing.

---

## Analysis Steps

### Step 1: ZDTP — Actual First 16 Riemann Zeros

Load `rh_zeros.json`, extract first 16 values. Pack into a 16D vector and run ZDTP:

- Dimensions: [16, 32, 64]
- All six gateways (Master, Multi-modal, Discontinuous, Diagonal, Orthogonal, Incremental)

Record:
- Convergence score per gateway
- Overall convergence score
- Gateway ordering (which leads)
- Classification (high / moderate / low)

This re-validates the Phase 1 result on 16 values only (Phase 1 used the full 1,000 — this is 16D-specific).

### Step 2: Chavez Transform — Actual First 16 Riemann Zeros

Same 16 values. Run Chavez Transform:

- alpha: 1.0, dimension_param: 2, pattern_id: 1
- dimensions: 1, 2, 3, 4, 5

Record: CV, conjugation symmetry, dimensional persistence, transform values at each dimension.

### Step 3: Generate Control A + Run ZDTP and Chavez

Generate Control A using the formula above (seed = 42). Record the 16 values.

Run:
1. ZDTP (same parameters as Step 1) — record all six gateway scores and overall convergence
2. Chavez Transform (same parameters as Step 2) — record CV, symmetry, persistence

### Step 4: Generate Control B + Run ZDTP and Chavez

Generate Control B (Poisson gaps, seed = 42). Compute mean gap of actual first 16 zeros first, use that as lambda. Record the 16 values.

Run ZDTP and Chavez Transform (same parameters).

### Step 5: Generate Control C + Run ZDTP and Chavez

Generate Control C (uniform linear). No randomness.

Run ZDTP and Chavez Transform (same parameters).

### Step 6: Compile Comparison Table

After all runs, fill in:

| Sequence | ZDTP Overall | Chavez Symmetry | Chavez CV | Notes |
|---|---|---|---|---|
| Actual Riemann zeros (16) | ? | ? | ? | From rh_zeros.json |
| Control A: Growth + noise | ? | ? | ? | Seed 42 |
| Control B: Poisson gaps | ? | ? | ? | Seed 42 |
| Control C: Uniform | ? | ? | ? | Deterministic |

---

## Results Template

```json
{
  "experiment_id": "RH_CTRL_2026_001",
  "date": "2026-03-04",
  "objective": "Test whether ZDTP 98.7% on Riemann zeros is discriminating vs. synthetic controls",
  "parameters": {
    "alpha": 1.0,
    "dimension_param": 2,
    "pattern_id": 1,
    "zdtp_dimensions": [16, 32, 64],
    "chavez_dimensions": [1, 2, 3, 4, 5],
    "n_elements": 16,
    "range": [14.1347, 1419.4225],
    "random_seed": 42
  },
  "analyses": {
    "actual_zeros": {
      "source": "rh_zeros.json, first 16 values",
      "values": null,
      "zdtp": {
        "overall_convergence": null,
        "gateway_scores": {
          "master": null, "multimodal": null, "discontinuous": null,
          "diagonal": null, "orthogonal": null, "incremental": null
        },
        "gateway_ordering": null
      },
      "chavez": {
        "cv": null,
        "conjugation_symmetry": null,
        "dimensional_persistence": null,
        "transform_values": [null, null, null, null, null]
      }
    },
    "control_a_growth_noise": {
      "formula": "2*pi*n/log(n) + N(0, 0.10 * 2*pi*n/log(n)), seed=42",
      "values": null,
      "zdtp": {
        "overall_convergence": null,
        "gateway_scores": {
          "master": null, "multimodal": null, "discontinuous": null,
          "diagonal": null, "orthogonal": null, "incremental": null
        }
      },
      "chavez": {
        "cv": null,
        "conjugation_symmetry": null,
        "dimensional_persistence": null
      }
    },
    "control_b_poisson_gaps": {
      "formula": "Exponential(mean=1.42), gaps accumulated from 14.13, seed=42",
      "lambda_used": 1.42,
      "values": null,
      "zdtp": {
        "overall_convergence": null,
        "gateway_scores": {
          "master": null, "multimodal": null, "discontinuous": null,
          "diagonal": null, "orthogonal": null, "incremental": null
        }
      },
      "chavez": {
        "cv": null,
        "conjugation_symmetry": null,
        "dimensional_persistence": null
      }
    },
    "control_c_uniform": {
      "formula": "14.13 + (67.08 - 14.13) * (n-1) / 15, n=1..16 (14.13 to 16th zero ~67.08)",
      "values": null,
      "zdtp": {
        "overall_convergence": null,
        "gateway_scores": {
          "master": null, "multimodal": null, "discontinuous": null,
          "diagonal": null, "orthogonal": null, "incremental": null
        }
      },
      "chavez": {
        "cv": null,
        "conjugation_symmetry": null,
        "dimensional_persistence": null
      }
    }
  },
  "key_findings": {
    "discriminability": null,
    "which_controls_match_zeros": null,
    "which_controls_diverge": null,
    "interpretation": null
  }
}
```

---

## Key Questions to Answer

1. **Is ZDTP discriminating?** Does the actual Riemann zero sequence score significantly higher than all three controls? "Significant" = more than 2–3 percentage points above the highest control.

2. **Which control is hardest to distinguish?** If Control C (uniform) scores nearly as high as the actual zeros, ZDTP may be detecting monotone growth, not Riemann structure. If all controls score below 90%, the 98.7% is a strong discriminator.

3. **Does Chavez symmetry distinguish better or worse than ZDTP?** Phase 1 showed the two metrics measure different axes. This test reveals whether Chavez symmetry is a better or worse discriminator than ZDTP for this type of sequence.

4. **Does the gateway ordering change across controls?** In Phase 1, S1 (Master) led for actual zeros. Do controls show a different leading gateway? A change in gateway ordering suggests different structural properties.

5. **Does CV ≈ 0.146 hold for all controls?** CV is expected to be transform-invariant. If controls show significant deviation, something unusual is happening with the 16-element sample size.

---

## The Discriminating Result — What It Means for Phase 2

This is the binary decision point for the entire Phase 2 roadmap:

**If Controls A and C also reach ~98.7%:**
ZDTP is detecting monotone growth, not zero-specific structure. The Phase 1 result is a range/growth artifact. Phase 2 needs to be reframed — the annihilation topology work cannot use ZDTP convergence as evidence for Riemann zero algebraic structure.

**If only the actual zeros score ~98.7% while controls are significantly lower:**
The zeros carry algebraic structure beyond their growth rate. This is the stronger result for the AIEX-001 conjecture. The annihilation topology work is then hunting for *why* — what it is about the precise positions of Riemann zeros that survives 16D→32D→64D transmission when control sequences with the same growth profile do not.

That answer shapes everything in Phase 2. If the zeros are special, the annihilation topology work is hunting for why. If they're not, Phase 2 needs to be reframed.

| Outcome | Interpretation | Phase 2 Direction |
|---|---|---|
| Zeros >> all controls | 98.7% is genuinely discriminating | Annihilation topology: hunt for structural mechanism |
| Zeros ≈ Control A (growth formula) | ZDTP detects growth profile only | Reframe: test with zero-centered / gap-normalized inputs |
| Zeros ≈ Control C (uniform) | ZDTP detects linear spacing | Reframe: result is monotonicity artifact |
| Zeros ≈ Control B (exponential) | ZDTP detects mean gap rate | Reframe: test with shuffled zeros to isolate spacing |
| All controls near 98% | Phase 1 result is uninformative | Major reframe required before Phase 2 |

---

## Files in This Directory

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 Riemann zeros (use first 16) |
| `rh_gaps.json` | 999 gaps (for computing mean gap lambda in Control B) |
| `rh_experiment_results.json` | Phase 1 results (reference) |
| `RH_Experiment_Results_Summary.md` | Phase 1 human-readable summary |
| `RH_Phase2_Control_Handoff.md` | This document |
| `Experimental_Roadmap.md` | Full research roadmap |
| `CLAUDE.md` | Repository guidance |
