# RH Phase 10 — Multi-Prime Berry-Keating, 10k-Zero R(α), Color Group Survey

## Handoff Document for Claude Desktop + CAILculator MCP

**Researcher:** Paul Chavez, Chavez AI Labs
**Date:** 2026-03-08
**Experiment ID:** RH_MP_2026_001
**Prerequisite:** RH Phase 9 complete (`rh_phase9_results.json`)

---

## Context: What Phase 9 Established

Three validated findings drive Phase 10:

1. **R(α) ultra-fine separation record: 14.7 pts at n=300 (Δα=0.05).** Scaling is real. The n=750 attempt (33.9 pts) was spurious — 27 sparse bins with 1,000 zeros. 10,000+ zeros unlock Δα=0.02 legitimately.

2. **Berry-Keating correlation: r≈0.35–0.50 (p=2 term only).** Two independent runs confirm weak-to-moderate correlation with correct direction. The single-prime model is insufficient. Multi-prime R_c with p=2,3,5,7,11 is the necessary next step.

3. **P5 conjugation symmetry discriminates GUE from Poisson:** actual zeros and GUE both score ~52% on the (e₂+e₅) P-vector projection; Poisson scores ~78%. The bilateral zero count was an artifact; the symmetry score is a real geometric finding. Color Group 2 internal split (P2=83% vs P5=52% on actual zeros) warrants full characterization.

---

## DATA PREPARATION — Required Before CAILculator Session

**10B requires 10,000 Riemann zeros.** Run this Python script before the analysis session:

```python
import mpmath
import json

mpmath.mp.dps = 25

# Load existing 1,000 zeros
with open('rh_zeros.json', 'r') as f:
    zeros_existing = json.load(f)

print(f"Existing zeros: {len(zeros_existing)}")
print(f"Computing zeros 1001-10000...")

zeros_new = []
for n in range(1001, 10001):
    z = float(mpmath.im(mpmath.zetazero(n)))
    zeros_new.append(z)
    if n % 500 == 0:
        print(f"  Computed zero {n}: {z:.6f}")

zeros_10k = zeros_existing + zeros_new

with open('rh_zeros_10k.json', 'w') as f:
    json.dump(zeros_10k, f)

print(f"Saved {len(zeros_10k)} zeros to rh_zeros_10k.json")
print(f"Range: {zeros_10k[0]:.4f} to {zeros_10k[-1]:.4f}")
```

Save output as `rh_zeros_10k.json`. This computation may take 10–20 minutes. Run it first, then proceed with the CAILculator session.

Also compute 10,000-zero gaps and save:

```python
gaps_10k = [zeros_10k[i+1] - zeros_10k[i] for i in range(len(zeros_10k)-1)]
with open('rh_gaps_10k.json', 'w') as f:
    json.dump(gaps_10k, f)
print(f"Saved {len(gaps_10k)} gaps to rh_gaps_10k.json")
```

---

## Experiment 10A — Multi-Prime Berry-Keating Correlation (Primary)

### Background

The Berry-Keating explicit formula predicts that at finite height t, the zero spacing statistics deviate from asymptotic GUE by prime-orbit corrections:

```
R_c(t) = Σ_{p prime} (1/√p) · cos(log(p) · t)
         + Σ_{p prime} (1/p) · cos(2·log(p) · t)   [prime square terms]
```

Phase 9C tested only the p=2 first-order term, capturing ~12–25% of variance. The full model with five primes (p=2,3,5,7,11) plus their squares should capture the dominant oscillation structure at heights t=14–1419.

**Amplitudes (first-order terms):**
- p=2: A=1/√2 ≈ 0.7071, log(2) ≈ 0.6931
- p=3: A=1/√3 ≈ 0.5774, log(3) ≈ 1.0986
- p=5: A=1/√5 ≈ 0.4472, log(5) ≈ 1.6094
- p=7: A=1/√7 ≈ 0.3780, log(7) ≈ 1.9459
- p=11: A=1/√11 ≈ 0.3015, log(11) ≈ 2.3979

**Amplitudes (prime square terms — second order):**
- p²=4: A=1/2=0.5000, log(4)=2·log(2) ≈ 1.3863
- p²=9: A=1/3=0.3333, log(9)=2·log(3) ≈ 2.1972

### Step 1: Compute Band Deltas (Actual − GUE)

For each of the 10 height bands, compute the Chavez conjugation symmetry on spacing ratios (98 ratios from 99 gaps) for actual zeros and GUE synthetic (seed 1, mean-matched).

Use `rh_zeros.json` (existing 1,000 zeros). Bands as defined in Phase 6:

| Band | Zero indices | Approx height |
|---|---|---|
| 1 | 1–100 | t=14–237 |
| 2 | 101–200 | t=238–396 |
| 3 | 201–300 | t=398–542 |
| 4 | 301–400 | t=544–680 |
| 5 | 401–500 | t=682–811 |
| 6 | 501–600 | t=812–937 |
| 7 | 601–700 | t=940–1063 |
| 8 | 701–800 | t=1064–1184 |
| 9 | 801–900 | t=1185–1302 |
| 10 | 901–1000 | t=1303–1419 |

For each band:
1. Extract 100 zeros → 99 gaps → 98 spacing ratios rₙ = min(gₙ,gₙ₊₁)/max(gₙ,gₙ₊₁)
2. Compute band mean gap
3. Run Chavez Transform (alpha=1.0, dimension_param=2, pattern_id=1, dimensions=1–5)
4. Generate GUE Wigner surmise gaps (mean=band_mean_gap, seed=1) → 98 ratios → Chavez Transform
5. Delta = actual_symmetry − gue_symmetry

Record all 10 deltas.

### Step 2: Compute Multi-Prime R_c at Band Midpoints

Band midpoints (t_mid):

| Band | t_mid |
|---|---|
| 1 | 125 |
| 2 | 317 |
| 3 | 470 |
| 4 | 612 |
| 5 | 747 |
| 6 | 875 |
| 7 | 1002 |
| 8 | 1124 |
| 9 | 1244 |
| 10 | 1361 |

For each t_mid, compute:

```
R_c_full(t) = 0.7071·cos(0.6931·t)      [p=2]
            + 0.5774·cos(1.0986·t)      [p=3]
            + 0.4472·cos(1.6094·t)      [p=5]
            + 0.3780·cos(1.9459·t)      [p=7]
            + 0.3015·cos(2.3979·t)      [p=11]
            + 0.5000·cos(1.3863·t)      [p²=4]
            + 0.3333·cos(2.1972·t)      [p²=9]
```

Also compute the single-prime version for comparison:
```
R_c_p2(t) = cos(0.6931·t)    [p=2 only, unweighted — matches Phase 9C]
```

### Step 3: Pearson Correlation

Compute Pearson r between:
- **Model A**: R_c_p2 (10 values) vs band deltas (10 values) — replication of Phase 9C
- **Model B**: R_c_full (10 values) vs band deltas (10 values) — full multi-prime model

Record: r, p-value, r² for both models.

**Significance threshold at n=10:** r > 0.632 gives p < 0.05 (two-tailed).

### Decision Framework — 10A

| Outcome | Interpretation |
|---|---|
| Model B r > 0.632 | **Berry-Keating confirmed** — prime-orbit corrections statistically explain bilateral symmetry deviation |
| Model B r = 0.5–0.63 | Strong improvement over single-prime but sub-threshold; add p=13,17 in Phase 11 |
| Model B r ≈ Model A r | Higher-order primes not contributing at these heights; mechanism is p=2 dominated |
| Model B r < Model A r | Multi-prime sum partially cancels at these heights; phase interference — try different amplitude weighting |
| Bands 3 and 8 still anomalous | Those bands may have specific prime resonances; investigate individually |

---

## Experiment 10B — R(α) with 10,000 Zeros

### Prerequisite

`rh_zeros_10k.json` must exist (see Data Preparation above).

### Protocol

Compute empirical R(α) from all 10,000 zeros at three grid densities:

**Mean spacing for 10,000 zeros:**
Δ = (γ₁₀₀₀₀ − γ₁) / 9999 (compute from actual data)

**Grid 10B-i: Δα=0.05, n=300 (α=0.05 to 15.0)**

Compute empirical R(α) with window ±0.025. Record bin pair counts — with 10,000 zeros expect ~250× more pairs per bin than at n=1,000. All bins should have > 1,000 pairs: no sparsity issues.

Apply Chavez Transform to GUE theoretical (sinc² formula), Poisson (flat 1.0), empirical zeros.

**Grid 10B-ii: Δα=0.02, n=750 (α=0.02 to 15.0)**

Compute empirical R(α) with window ±0.010. This is the grid that gave 33.9 pts spuriously with 1,000 zeros (27 sparse bins). With 10,000 zeros all bins should be well-populated.

Apply Chavez Transform to all three sequences.

**Grid 10B-iii: Δα=0.01, n=1500 (α=0.01 to 15.0)**

Push to the finest grid attempted in the series. Window ±0.005. Record minimum bin count. If any bins have < 50 pairs, flag as potentially unreliable — this grid may require 100,000 zeros for clean computation.

Apply Chavez Transform to GUE theoretical and Poisson only (skip empirical if bins are sparse).

### Step 4: Compile 10B Results

| Grid | n | GUE Sym | Poisson Sym | Empirical Sym | Separation | Min bin count |
|---|---|---|---|---|---|---|
| Phase 9B baseline | 300 | ~93.8% | 100.0% | ~86.5% | 14.7 pts | — |
| 10B-i (Δα=0.05) | 300 | | | | | |
| 10B-ii (Δα=0.02) | 750 | | | | | |
| 10B-iii (Δα=0.01) | 1500 | | | | — |

**Key question:** Does 10B-ii produce legitimate separation >> 14.7 pts with no sparse bins?

**Secondary question:** Does the GUE theoretical symmetry continue its slow decline (96.7% → 94.1% → 93.8% → 93.6%) or has it asymptoted?

### Decision Framework — 10B

| Outcome | Interpretation |
|---|---|
| 10B-ii separation > 20 pts, no sparse bins | **New record confirmed** — R(α) at Δα=0.02 is a legitimate 20+ pt discriminator |
| 10B-ii separation 15–20 pts | Clean improvement over Phase 9B; data bottleneck resolved |
| 10B-ii ≈ 14.7 pts | Separation saturating at n=300; finer grids don't add more structure |
| GUE theoretical still declining | No asymptote yet; even finer grids will continue increasing separation |
| GUE theoretical stable | Natural bilateral symmetry ceiling of sinc² function identified |

---

## Experiment 10C — Color Group P-Vector Direction Survey

### What This Tests

Phase 9A revealed a Color Group 2 internal split: P2 (e₃−e₄) scored 83% and P5 (e₂+e₅) scored 52% on actual Riemann zero gap projections. These are both Color Group 2 patterns but behave oppositely. Phase 8A's pre-probe gave the full actual zero picture. Phase 10C adds the Poisson comparison to complete the discrimination table.

### Step 5: All P-Vector Projections — GUE and Poisson

Project consecutive gap pairs (gₙ, gₙ₊₁) from first 99 gaps onto each P-vector:
- P1 (e₁−e₆): subtract components at positions 1 and 6
- P2 (e₃−e₄): subtract components at positions 3 and 4
- P3/P6 (e₃+e₄, antipodal): add components — same result by definition
- P4 (e₁+e₆): add components at positions 1 and 6
- P5 (e₂+e₅): add components at positions 2 and 5

For **GUE synthetic** (Wigner surmise, mean=2.25, seeds 1, 2, 3):
- Generate 99 gaps → 98 consecutive pairs → project onto each P-vector → detect_patterns
- Record: conjugation symmetry per P-vector per seed; compute mean across 3 seeds

For **Poisson synthetic** (Exponential mean=2.25, seeds 1, 2, 3):
- Same protocol

### Step 6: Build Full Discrimination Table

| P-Vector | Color Group | Actual Sym | GUE Mean Sym | Poisson Mean Sym | GUE/Poisson Gap | Discriminates? |
|---|---|---|---|---|---|---|
| P1 (e₁−e₆) | CG1 | 79.1% | | | | |
| P2 (e₃−e₄) | CG2 | 83.0% | | | | |
| P4 (e₁+e₆) | CG1 | 78.9% | | | | |
| P5 (e₂+e₅) | CG2 | 52.0% | ~52% | ~78% | ~26 pts | Yes |

**Key questions:**
1. Do P1 and P4 (Color Group 1 pair) also discriminate GUE from Poisson — or do they score similarly across all three?
2. Does P2 (Color Group 2 partner to P5) discriminate GUE from Poisson — or does it score similarly to Poisson (~83%)?
3. Is P5 the only level-repulsion-sensitive direction, or are others?

### Step 7: Color Group Discrimination Map

After completing the table, classify each P-vector direction:

| Classification | Definition | Expected candidates |
|---|---|---|
| Level-repulsion sensitive | GUE/Poisson gap > 10 pts | P5 confirmed; others unknown |
| Level-repulsion insensitive | GUE/Poisson gap < 5 pts | P1, P4 likely (CG1 pair similar to each other) |
| Riemann-specific | Actual differs from GUE (same direction) | None confirmed yet |

### Decision Framework — 10C

| Outcome | Interpretation |
|---|---|
| Only P5 discriminates GUE/Poisson | The (e₂+e₅) direction is uniquely level-repulsion sensitive among Canonical Six |
| P5 + one other discriminate | Multiple sedenion directions encode level repulsion; Color Group structure partially maps to it |
| All directions discriminate similarly | Level repulsion is isotropic in the Canonical Six projection space |
| CG1 pair (P1, P4) score identically on all three sequences | Color Group 1 geometry confirmed as level-repulsion-insensitive |
| CG2 internal split confirmed (P2 high, P5 low across all sequences) | Color Group 2 contains one sensitive and one insensitive direction — internal asymmetry is a structural property |

---

## Results Template

```json
{
  "experiment_id": "RH_MP_2026_001",
  "date": "2026-03-08",
  "phases": {
    "10A_multi_prime_berry_keating": {
      "band_deltas": [null, null, null, null, null, null, null, null, null, null],
      "band_t_mids": [125, 317, 470, 612, 747, 875, 1002, 1124, 1244, 1361],
      "rc_p2_only": [null, null, null, null, null, null, null, null, null, null],
      "rc_full_5prime": [null, null, null, null, null, null, null, null, null, null],
      "model_A_p2_only": {"pearson_r": null, "p_value": null, "r_squared": null},
      "model_B_full": {"pearson_r": null, "p_value": null, "r_squared": null},
      "improvement": null,
      "berry_keating_confirmed": null
    },
    "10B_r_alpha_10k_zeros": {
      "zero_count": 10000,
      "mean_spacing": null,
      "grids": {
        "delta_005_n300": {
          "gue_sym": null, "poisson_sym": null, "empirical_sym": null,
          "separation": null, "min_bin_count": null
        },
        "delta_002_n750": {
          "gue_sym": null, "poisson_sym": null, "empirical_sym": null,
          "separation": null, "min_bin_count": null
        },
        "delta_001_n1500": {
          "gue_sym": null, "poisson_sym": null, "empirical_sym": null,
          "separation": null, "min_bin_count": null, "sparse_warning": null
        }
      },
      "new_record": null
    },
    "10C_color_group_survey": {
      "actual_zeros": {
        "P1": 79.1, "P2": 83.0, "P4": 78.9, "P5": 52.0
      },
      "gue_mean": {
        "P1": null, "P2": null, "P4": null, "P5": null
      },
      "poisson_mean": {
        "P1": null, "P2": null, "P4": null, "P5": null
      },
      "gue_poisson_gap": {
        "P1": null, "P2": null, "P4": null, "P5": null
      },
      "level_repulsion_sensitive_directions": null,
      "cg2_internal_split_confirmed": null
    }
  },
  "key_findings": {
    "10A": null,
    "10B": null,
    "10C": null,
    "combined": null
  }
}
```

---

## Cumulative Separation Record

| Phase | Method | n | Separation | Status |
|---|---|---|---|---|
| 5 | Spacing ratios | 499 | 7.2 pts | Validated |
| 8B | R(α) fine | 150 | 12.5 pts | Validated |
| 9B | R(α) ultra-fine | 300 | 14.7 pts | Validated |
| **10B-ii target** | **R(α) Δα=0.02** | **750** | **>20 pts predicted** | **Pending** |

---

## Files Referenced

| File | Purpose |
|---|---|
| `rh_zeros.json` | 1,000 zeros (10A band analysis) |
| `rh_zeros_10k.json` | 10,000 zeros (10B — generate via data prep script) |
| `rh_gaps_10k.json` | 9,999 gaps (generate alongside zeros) |
| `rh_phase9_results.json` | Phase 9 baseline |
| `rh_height_band_results.json` | Phase 6 band reference |
| `RH_Phase10_Handoff.md` | This document |
| `RH_Investigation_Roadmap.md` | Full roadmap |

---

## After the Session

Save as `rh_phase10_results.json` and `RH_Phase10_Results.md`.
Update `RH_Investigation_Roadmap.md` Phase 10 row.

**If 10A r > 0.632:** Berry-Keating confirmed — add to `ChavezTransform_Paper_Draft.md` Section 7 immediately. This is the paper's strongest theoretical result.

**If 10B-ii produces > 20 pt clean separation:** Document the scaling law from n=30 (6.9 pts) through n=750 (20+ pts) as a figure for the paper.

**If 10C confirms CG2 internal split:** The Color Group geometry has an observable asymmetry in level-repulsion sensitivity — first geometric characterization of GUE structure in sedenion projection space.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
