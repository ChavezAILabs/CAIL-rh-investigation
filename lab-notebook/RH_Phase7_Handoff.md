# RH Phase 7 — Pair Correlation and Canonical Six Pattern Sensitivity

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-08
**Experiment ID:** RH_PC_2026_001
**Prerequisite:** RH Phases 1–6 complete

---

## Overview

Phase 7 contains two experiments run in sequence.

**7A — Pair Correlation Function (Direct Montgomery-Dyson Test)**
Apply Chavez Transform to the pair correlation function R(α) itself — the function Montgomery proved matches GUE. No prior work applies Chavez to R(α). This is the most direct test of Montgomery-Dyson available in this pipeline.

**7B — Canonical Six Pattern Sensitivity**
Run all six Canonical Six patterns (pattern_id 1–6) on the same Riemann zero dataset. Measure which patterns are most sensitive to GUE structure and whether the Color Group tripartite structure (1,4 / 2,5 / 3,6) appears in the results.

The Canonical Six are the framework-independent bilateral zero divisors — the only ones that survive both Cayley-Dickson and Clifford algebra settings. Phase 7B tests whether individual patterns within the Canonical Six have differential sensitivity to the algebraic structure of the Riemann zeros.

---

## Background: The Gram Matrix of the Canonical Six

The five distinct P-vector images of the Canonical Six lie on the E8 lattice first shell (‖v‖² = 2, Lean 4 proven). Because all norms are equal, the projection matrix cannot be built from norms alone. The natural spectral object is the **5×5 Gram matrix G** where Gᵢⱼ = vᵢ · vⱼ.

**P-vector coordinates (8D):**

| Pattern | P-vector |
|---|---|
| 1 | v₁ = (0, 1, 0, 0, 0, 0, −1, 0) |
| 2 | v₂ = (0, 0, 0, 1, −1, 0, 0, 0) |
| 3 | v₃ = (0, 0, 0, −1, 1, 0, 0, 0) — antipodal to v₂ |
| 4 | v₄ = (0, 1, 0, 0, 0, 0, 1, 0) |
| 5 | v₅ = (0, 0, 1, 0, 0, 1, 0, 0) |
| 6 | (shares index set with Pattern 3; v₃ image) |

**Gram matrix G (5×5, vᵢ·vⱼ):**

```
G = [[ 2,  0,  0,  0,  0],
     [ 0,  2, -2,  0,  0],
     [ 0, -2,  2,  0,  0],
     [ 0,  0,  0,  2,  0],
     [ 0,  0,  0,  0,  2]]
```

**Eigenvalues of G: {0, 2, 2, 2, 4}**

The zero eigenvalue arises from the antipodal pair (v₂, v₃): they are linearly dependent (v₃ = −v₂), reducing the rank. The eigenvalue 4 reflects their combined 2D span. The three 2s correspond to the three independent directions (v₁, v₄, v₅).

This eigenvalue sequence {0, 2, 2, 2, 4} is the natural spectral fingerprint of the Canonical Six geometry. It is recorded here as a structural reference for future theoretical comparison; Chavez Transform is not applied directly (n=5 is below the minimum useful window of ~50 points).

---

## Experiment 7A — Pair Correlation Function

### What R(α) Is

The pair correlation function measures how zero pairs are distributed by their normalized separation α. Montgomery (1973) proved:

```
R(α) = 1 − (sin πα / πα)²    [GUE prediction]
R(α) = 1                      [Poisson prediction — no level repulsion]
```

For actual Riemann zeros, Odlyzko confirmed R(α) matches GUE to extraordinary precision.

Applying Chavez Transform to R(α) as a sequence tests whether the transform detects the sinc² oscillatory structure that encodes GUE level repulsion — the deepest level of the Montgomery-Dyson coincidence.

### Datasets

| Sequence | Description | Length |
|---|---|---|
| GUE theoretical | R(α) = 1 − (sin πα / πα)² at α = 0.5, 1.0, 1.5, ..., 15.0 | 30 values |
| Poisson | R(α) = 1.0 at same α values | 30 values (constant) |
| Empirical zeros | Pair correlation computed from first 1,000 zeros at same α values | 30 values |

**Files needed:** `rh_zeros.json` (1,000 zero imaginary parts)

### Step 1: Generate GUE Theoretical R(α)

Compute R(α) = 1 − (sin(πα) / (πα))² at:
α = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0

Note: at α = 0 the formula gives 0 (complete level repulsion); the sequence starts at α = 0.5 to avoid the singularity.

Apply Chavez Transform to these 30 R(α) values:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: CV, conjugation symmetry, dimensional persistence, transform values [d1..d5].

### Step 2: Generate Poisson R(α)

Poisson prediction: R(α) = 1.0 for all α > 0. This is a flat sequence of 30 ones.

Apply Chavez Transform to the 30-value flat sequence:
- Same parameters as Step 1

Record: CV, conjugation symmetry, dimensional persistence, transform values.

Note: a flat constant sequence has no bilateral structure — conjugation symmetry is expected to be near 0% or structurally degenerate. This establishes the baseline for "no level repulsion."

### Step 3: Compute Empirical Pair Correlation from Actual Zeros

Load `rh_zeros.json` (first 1,000 zeros). The empirical pair correlation at scale α is estimated by counting zero pairs with normalized separation near α.

**Protocol for each α value in the grid:**

1. Compute the mean zero spacing Δ = (γ₁₀₀₀ − γ₁) / 999 ≈ 1.405
2. For each pair (γᵢ, γⱼ) with i < j and |γᵢ − γⱼ| / Δ ∈ [α − 0.25, α + 0.25]:
   count the pair
3. Normalize: R_empirical(α) = count / (N × 0.5 × window_width)
   where N = 1000, window_width = 0.5

This yields 30 empirical R(α) values.

Apply Chavez Transform to these 30 values:
- Same parameters as Steps 1–2

Record: CV, conjugation symmetry, dimensional persistence, transform values.

### Step 4: Compile 7A Results

| Sequence | CV | Symmetry | Persistence | Transform d1 | Delta vs GUE |
|---|---|---|---|---|---|
| GUE theoretical R(α) | | | | | baseline |
| Poisson R(α) = flat | | | | | |
| Empirical zeros R(α) | | | | | |

**Key question:** Is GUE/Poisson separation on R(α) larger than the 7.2 pts achieved with spacing ratios (Phase 5)?

**Decision framework:**

| Outcome | Interpretation |
|---|---|
| Empirical ≈ GUE >> Poisson (>10 pts) | **Montgomery-Dyson confirmed via Chavez** — strongest result in the series |
| Empirical ≈ GUE >> Poisson (>7.2 pts) | Pair correlation more discriminating than spacing ratios — upgrade confirmed |
| Separation similar to Phase 5 (5–7 pts) | Spacing ratios and pair correlation carry similar Chavez-detectable structure |
| GUE ≈ Poisson | Chavez is insensitive to R(α) oscillation at n=30; increase α grid density in Phase 8 |
| Empirical diverges from GUE | Unexpected — empirical R(α) computation may need refinement |

---

## Experiment 7B — Canonical Six Pattern Sensitivity

### What This Tests

The standard Chavez Transform uses pattern_id = 1 (the first Canonical Six pattern). All six patterns are framework-independent bilateral zero divisors, but they have different geometric structures (different P-vector directions, different Color Group assignments). Phase 7B asks:

- Do the six patterns produce different Chavez symmetry scores on Riemann zero data?
- Does the Color Group tripartite structure (pairs 1,4 / 2,5 / 3,6) appear as a grouping in the scores?
- Is pattern_id = 1 genuinely the optimal choice, or does another pattern produce stronger GUE discrimination?

**Color Group structure (from Canonical Six v1.3):**

| Color Group | Patterns | P-vectors |
|---|---|---|
| Color Group 1 | Patterns 1, 4 | v₁, v₄ — differ only in sign of one component |
| Color Group 2 | Patterns 2, 5 | v₂, v₅ |
| Color Group 3 | Patterns 3, 6 | v₃ — antipodal to v₂ |

If the E8 tripartite structure is relevant to the zero spectrum, Color Group pairs should score more similarly to each other than across groups.

### Dataset

Use the spacing ratio sequence from Phase 4 — 98 spacing ratios computed from the first 99 zero gaps. This is the dataset that produced the first correct GUE ordering (Phase 4) and the strongest GUE signal (Phase 5). It is the optimal input for this sensitivity test.

File: `rh_gaps.json` — take first 99 gaps, compute 98 spacing ratios: rₙ = min(gₙ, gₙ₊₁) / max(gₙ, gₙ₊₁)

### Step 5: Run All Six Patterns on Actual Zero Spacing Ratios

For each pattern_id in {1, 2, 3, 4, 5, 6}:

Apply Chavez Transform to the 98 spacing ratios:
- alpha: 1.0, dimension_param: 2, **pattern_id: [current]**, dimensions: 1–5

Record per pattern: CV, conjugation symmetry, dimensional persistence, transform values [d1..d5].

### Step 6: Run All Six Patterns on GUE Synthetic (3 seeds)

Generate GUE spacing ratios: 99 GUE gaps (Wigner surmise, mean=2.25, seeds 1, 2, 3) → 98 ratios each.

For each pattern_id in {1, 2, 3, 4, 5, 6}, run on the seed-1 GUE sequence (use seed 1 as representative):
- Record: conjugation symmetry per pattern

### Step 7: Compile Pattern Sensitivity Table

| Pattern | Color Group | Actual Symmetry | GUE Symmetry | Delta (actual−GUE) |
|---|---|---|---|---|
| 1 | CG1 | | | |
| 2 | CG2 | | | |
| 3 | CG3 | | | |
| 4 | CG1 | | | |
| 5 | CG2 | | | |
| 6 | CG3 | | | |

**Key questions:**

1. Do Color Group pairs (1,4), (2,5), (3,6) score closer to each other than across groups?
2. Which pattern produces the largest GUE/actual delta? (Most sensitive to zero structure)
3. Which pattern produces the smallest GUE/actual delta? (Least sensitive)
4. Is pattern_id = 1 optimal, or should a different pattern be the new default for RH work?

**Decision framework:**

| Outcome | Interpretation |
|---|---|
| Color Group pairs cluster (within-pair gap < across-group gap) | **E8 tripartite structure visible in zero spectrum** — significant |
| All six patterns score identically | Pattern choice is irrelevant; zero structure is pattern-agnostic |
| One pattern clearly dominates | That pattern has privileged sensitivity to RH structure; update default |
| Antipodal patterns (2,3 — v₂ and v₃) score very differently | Zero spectrum distinguishes antipodal directions; geometric sensitivity confirmed |

---

## Results Template

```json
{
  "experiment_id": "RH_PC_2026_001",
  "date": "2026-03-08",
  "phases": {
    "7A_pair_correlation": {
      "alpha_grid": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
                     5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0,
                     10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0],
      "n_values": 30,
      "gue_theoretical": {
        "r_alpha_values": null,
        "chavez_symmetry": null,
        "cv": null,
        "transform_values": [null, null, null, null, null]
      },
      "poisson_flat": {
        "r_alpha_values": null,
        "chavez_symmetry": null,
        "cv": null,
        "transform_values": [null, null, null, null, null]
      },
      "empirical_zeros": {
        "n_zeros_used": 1000,
        "mean_spacing_delta": null,
        "r_alpha_values": null,
        "chavez_symmetry": null,
        "cv": null,
        "transform_values": [null, null, null, null, null]
      },
      "gue_poisson_separation_pts": null,
      "empirical_vs_gue_delta": null
    },
    "7B_pattern_sensitivity": {
      "dataset": "spacing_ratios_n98_from_first99_gaps",
      "gram_matrix_eigenvalues": [0, 2, 2, 2, 4],
      "patterns": {
        "pattern_1": {
          "color_group": 1,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        },
        "pattern_2": {
          "color_group": 2,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        },
        "pattern_3": {
          "color_group": 3,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        },
        "pattern_4": {
          "color_group": 1,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        },
        "pattern_5": {
          "color_group": 2,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        },
        "pattern_6": {
          "color_group": 3,
          "actual_symmetry": null,
          "gue_symmetry_seed1": null,
          "delta": null,
          "cv": null,
          "transform_values": [null, null, null, null, null]
        }
      },
      "color_group_clustering": null,
      "optimal_pattern": null,
      "antipodal_pair_23_different": null
    }
  },
  "key_findings": {
    "7A": null,
    "7B": null,
    "combined": null
  }
}
```

---

## Files Referenced

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 Riemann zero imaginary parts |
| `rh_gaps.json` | 999 zero gaps (use first 99 → 98 spacing ratios) |
| `rh_spacing_ratio_results.json` | Phase 4 baseline (pattern_id=1, actual=75.0%, GUE=76.9%) |
| `RH_Phase5_Scale_and_Height_Results.md` | Phase 5 baseline (7.2 pt separation at n=499) |
| `RH_Phase7_Handoff.md` | This document |
| `RH_Investigation_Roadmap.md` | Full RH roadmap with Phase 7 design |

---

## After the Session

Save results as `rh_phase7_results.json` (use template above).
Save human-readable summary as `RH_Phase7_Results.md`.
Update `RH_Investigation_Roadmap.md` Phase 7 row with key findings and set status to Complete.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
