# RH Phase 8 — Complex Input, Fine-Grid Pair Correlation, Extended Height

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-08
**Experiment ID:** RH_CX_2026_001
**Prerequisite:** RH Phase 7 complete (`rh_phase7_results.json`)

---

## Context: What Phase 7 Established

Phase 7B proved a structural theorem: **the Chavez bilateral kernel is pattern-invariant for any real-valued 1D sequence.** All 6 Canonical Six patterns produce identical transform values to 15 decimal places on scalar input. The E8 Color Group geometry (tripartite structure 1,4 / 2,5 / 3,6) is algebraically present but invisible to 1D real input.

Phase 8 is designed to activate that geometry by changing the input structure. Three experiments, escalating in theoretical significance.

---

## Experiment 8A — Complex Gap Pair Input (Primary)

### The Key Idea

The 1D invariance theorem holds because a scalar value has no directional information — all P-vector orientations in 8D project to the same scalar. **Complex-valued input has two channels (real and imaginary).** Different P-vector directions project differently onto those two channels, breaking the invariance.

Encoding: treat each consecutive gap pair as a complex number:

```
z_n = g_n + i · g_{n+1}     for n = 1..98
```

This gives **98 complex values** from the first 99 zero gaps. The real part is the n-th gap; the imaginary part is the (n+1)-th gap. Each z_n encodes a local gap relationship — consecutive structure that the spacing ratio statistic also captures, but here preserved in 2D form rather than collapsed to a scalar ratio.

### Why This Should Break the Invariance

The Canonical Six P-vectors point in different directions in 8D space:
- v₁ = (0, 1, 0, 0, 0, 0, −1, 0)
- v₂ = (0, 0, 0, 1, −1, 0, 0, 0)
- v₃ = (0, 0, 0, −1, 1, 0, 0, 0)  ← antipodal to v₂
- v₄ = (0, 1, 0, 0, 0, 0, 1, 0)
- v₅ = (0, 0, 1, 0, 0, 1, 0, 0)

For a scalar sequence, all directions integrate to the same inner product. For complex input, the real channel projects onto some P-vector components and the imaginary channel onto others. Patterns within the same Color Group (e.g., 1 and 4) share geometric structure; patterns across Color Groups do not. This should produce different transform values per pattern — and Color Group clustering if the E8 geometry is probe-able.

### Dataset

File: `rh_gaps.json` — take first 99 gaps.

Construct 98 complex values: z_n = gaps[n] + i · gaps[n+1] for n = 0..97 (0-indexed).

For GUE synthetic: generate 99 GUE Wigner surmise gaps (mean = 2.25, seeds 1, 2, 3), construct 98 complex values the same way.

### Step 1: Complex Gap Pairs — Actual Zeros, All 6 Patterns

For each pattern_id in {1, 2, 3, 4, 5, 6}:

Apply Chavez Transform to the 98 complex gap pair values z_n:
- alpha: 1.0, dimension_param: 2, pattern_id: [current], dimensions: 1–5

Record per pattern: transform value (d1..d5), CV, conjugation symmetry.

**Critical check:** Are all 6 pattern transform values still identical? If yes, CAILculator treats complex input as scalar (takes magnitude or real part only) — document this and proceed to 8B. If values differ across patterns, the invariance is broken — run the full protocol below.

### Step 2: Complex Gap Pairs — GUE Synthetic (seed 1), All 6 Patterns

Generate GUE gaps (Wigner surmise, mean=2.25, seed 1) → 99 gaps → 98 complex pairs.

For each pattern_id in {1, 2, 3, 4, 5, 6}:
Apply Chavez Transform. Record: transform value, conjugation symmetry.

### Step 3: Compile Pattern Sensitivity Table

| Pattern | Color Group | Actual Sym | GUE Sym (seed 1) | Delta | Transform Value |
|---|---|---|---|---|---|
| 1 | CG1 | | | | |
| 2 | CG2 | | | | |
| 3 | CG3 | | | | |
| 4 | CG1 | | | | |
| 5 | CG2 | | | | |
| 6 | CG3 | | | | |

### Step 4: Color Group Clustering Analysis

Compute within-group variance and across-group variance for both actual and GUE symmetry scores.

| Color Group | Patterns | Mean Actual Sym | Mean GUE Sym |
|---|---|---|---|
| CG1 | 1, 4 | | |
| CG2 | 2, 5 | | |
| CG3 | 3, 6 | | |

**Is within-group variance < across-group variance?** If yes: Color Group clustering confirmed — E8 tripartite structure is visible in zero spacing data.

**Antipodal pair check:** Do patterns 2 and 3 (v₂ and −v₂) score differently? They must if the invariance is broken, since they point in opposite directions.

### Decision Framework — 8A

| Outcome | Interpretation |
|---|---|
| All 6 patterns still identical | CAILculator treats complex as scalar; complex input pathway needs different encoding; document and proceed to 8B |
| Patterns differ, Color Group clustering | **E8 geometry activated — first geometric result in the series** |
| Patterns differ, no Color Group clustering | Invariance broken but E8 structure not present in 1D zero data at this resolution |
| Antipodal pair (2,3) identical despite other differences | Antipodal symmetry preserved under complex encoding; constrain AIEX-001 theory |
| One pattern clearly dominates | That pattern has privileged geometric alignment with zero spacing structure |

---

## Experiment 8B — Fine-Grid Pair Correlation R(α)

### Motivation

Phase 7A used 30 R(α) values (Δα = 0.5). The sinc² curve has oscillatory structure at finer scales that those 30 points may not fully resolve. A finer grid gives the Chavez Transform more of the function's bilateral structure to work with — potentially increasing GUE/Poisson separation above the 7.2 pt Phase 5 record.

**Target:** n = 150 values at Δα = 0.1 (α = 0.1, 0.2, ..., 15.0)

### Step 5: GUE Theoretical R(α) — Fine Grid

Compute R(α) = 1 − (sin(πα) / (πα))² at:
α = 0.1, 0.2, 0.3, ..., 15.0 (150 values)

Note: include α = 1.0, 2.0, 3.0, ... where sin(πα) = 0, giving R(α) = 1.0 (peaks in the sinc² function).

Apply Chavez Transform to these 150 values:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: CV, conjugation symmetry, transform values.

### Step 6: Poisson Fine Grid

R(α) = 1.0 at all 150 α values. Apply Chavez Transform. Record.

### Step 7: Empirical Zeros Fine Grid

Load `rh_zeros.json` (1,000 zeros). Compute empirical R(α) at 150 α values using window ±0.05 (half the grid spacing):

For each α in the fine grid:
- Count zero pairs with normalized separation in [α − 0.05, α + 0.05]
- Normalize as in Phase 7A (using mean spacing Δ ≈ 1.405)

Apply Chavez Transform. Record: CV, conjugation symmetry, transform values.

### Step 8: Compile 8B Results

| Sequence | Chavez Sym | CV | Δ vs 7A |
|---|---|---|---|
| GUE theoretical (fine) | | | |
| Poisson flat (fine) | | | |
| Empirical zeros (fine) | | | |

**Key question:** Does fine-grid separation exceed 7.2 pts (Phase 5 record)?

**Decision framework:**

| Outcome | Interpretation |
|---|---|
| Separation > 7.2 pts | Fine-grid R(α) sets new record — pair correlation more powerful at higher resolution |
| Separation ≈ 7.2 pts | Pipeline at ceiling for this statistic; R(α) and spacing ratios saturate at same level |
| GUE symmetry changes significantly from 7A (96.7%) | Fine grid resolves finer oscillation structure; the sinc² bilateral depth increases with resolution |
| Empirical zeros closer to GUE on fine grid | Higher resolution reduces Berry-Keating noise; cleaner asymptotic GUE signal |

---

## Experiment 8C — Extended Height Range (Zeros 500–1000)

### Motivation

Phase 5B used zeros 500–599 (100 zeros → 98 spacing ratios) and scored 78.3% — exceeding GUE synthetic (76.8%) by +1.5 pts. We have 1,000 zeros. Zeros 500–1,000 give 500 gaps → 499 spacing ratios — a larger sample from the same height range where GUE agreement is cleanest.

The Berry-Keating oscillatory pattern (Phase 6) showed sub-band variation. A full 500-zero block from the upper half of our dataset should average over several oscillation cycles, giving a cleaner asymptotic result than the narrow 100-zero Phase 5B window.

### Step 9: Spacing Ratios, Zeros 500–1000

Load `rh_gaps.json`. Take gaps[499..998] (500 gaps, 0-indexed) → compute 499 spacing ratios:

```
r_n = min(gap_n, gap_{n+1}) / max(gap_n, gap_{n+1})    for n = 499..997
```

Apply Chavez Transform to 499 spacing ratios:
- alpha: 1.0, dimension_param: 2, pattern_id: 1, dimensions: 1–5

Record: mean ratio value, CV, conjugation symmetry, transform values.

### Step 10: GUE Synthetic — Mean-Matched to Zeros 500–1000

Compute mean gap for zeros 500–1,000 (should be close to full dataset mean ≈ 1.405 but slightly different at higher height). Generate GUE Wigner surmise gaps at that mean, seeds 1, 2, 3. Compute 499 spacing ratios from each. Run Chavez Transform.

### Step 11: Compile 8C Results

| Sequence | n | Mean Ratio | Chavez Sym | Δ vs GUE |
|---|---|---|---|---|
| Actual zeros 500–1000 | 499 | | | |
| GUE seed 1 | 499 | | | |
| GUE seed 2 | 499 | | | |
| GUE seed 3 | 499 | | | |
| GUE mean | | | | |
| Phase 5B baseline (zeros 500–599) | 98 | 0.615 | 78.3% | +1.5 |
| Phase 5A baseline (n=499 full) | 499 | 0.616 | 75.7% | +7.2 (vs Poisson) |

**Key question:** Does the upper half block (zeros 500–1,000) confirm and extend the asymptotic GUE convergence from Phase 5B?

---

## Results Template

```json
{
  "experiment_id": "RH_CX_2026_001",
  "date": "2026-03-08",
  "phases": {
    "8A_complex_gap_pairs": {
      "encoding": "z_n = gap_n + i * gap_{n+1}",
      "n_complex_values": 98,
      "invariance_broken": null,
      "patterns": {
        "pattern_1": {"color_group": 1, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null},
        "pattern_2": {"color_group": 2, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null},
        "pattern_3": {"color_group": 3, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null},
        "pattern_4": {"color_group": 1, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null},
        "pattern_5": {"color_group": 2, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null},
        "pattern_6": {"color_group": 3, "actual_sym": null, "gue_sym_seed1": null, "delta": null, "transform_value": null}
      },
      "color_group_clustering": null,
      "antipodal_pair_23_different": null,
      "optimal_pattern": null
    },
    "8B_fine_grid_pair_correlation": {
      "alpha_grid": "0.1 to 15.0, step 0.1",
      "n_values": 150,
      "phase7A_baseline_separation": 6.9,
      "gue_theoretical": {"chavez_sym": null, "cv": null},
      "poisson_flat": {"chavez_sym": null, "cv": null},
      "empirical_zeros": {"chavez_sym": null, "cv": null},
      "gue_poisson_separation_pts": null,
      "new_record": null
    },
    "8C_extended_height": {
      "zero_range": "500-1000",
      "n_spacing_ratios": 499,
      "mean_gap": null,
      "actual_zeros": {"mean_ratio": null, "chavez_sym": null},
      "gue_synthetic": {
        "seed_1": {"chavez_sym": null},
        "seed_2": {"chavez_sym": null},
        "seed_3": {"chavez_sym": null},
        "mean_sym": null
      },
      "actual_vs_gue_delta": null,
      "phase5B_baseline": "+1.5 pts at zeros 500-599 (n=98)"
    }
  },
  "key_findings": {
    "8A": null,
    "8B": null,
    "8C": null,
    "combined": null
  }
}
```

---

## Cumulative Significance Thresholds

| Metric | Current Record | Phase 8 Target |
|---|---|---|
| GUE/Poisson separation (spacing ratios) | 7.2 pts (Phase 5, n=499) | 8B: beat with fine R(α) |
| Actual vs GUE at higher zeros | +1.5 pts (Phase 5B, n=98) | 8C: confirm with n=499 |
| Pattern differentiation | 0 pts (all identical, Phase 7B) | 8A: any differentiation is progress |
| Color Group clustering | Not yet tested | 8A: within-group < across-group variance |

---

## Files Referenced

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 Riemann zeros |
| `rh_gaps.json` | 999 gaps (8A: first 99; 8C: gaps 499–998) |
| `rh_phase7_results.json` | Phase 7 baseline — all 6 patterns identical on 1D |
| `RH_Phase7_Results.md` | Phase 7 full results |
| `RH_Phase8_Handoff.md` | This document |
| `RH_Investigation_Roadmap.md` | Full roadmap |

---

## After the Session

Save as `rh_phase8_results.json` (template above).
Save summary as `RH_Phase8_Results.md`.
Update `RH_Investigation_Roadmap.md` Phase 8 row.

**If 8A breaks the invariance:** note which patterns differ and whether Color Group clustering is present. This is the primary result of Phase 8 regardless of 8B and 8C outcomes.

**If 8A does not break the invariance:** CAILculator may require a different encoding for complex input. Document the encoding used and flag for Phase 9 redesign.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
