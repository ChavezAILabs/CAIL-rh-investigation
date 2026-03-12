# Berry-Keating BK Significance — Re-Verification Handoff

**Date:** 2026-03-09
**Purpose:** Phase 11B reported BK r=0.7338 (significant). Phase 12C cannot
reproduce this from stored data (ceiling r=0.5793, sub-threshold). This handoff
re-runs the BK computation from scratch with explicit data capture.

---

## Background

Phase 10A stored the BK correlation result: r=0.5428 (stored as `best_model_B_r`
in `rh_phase10a_definitive.json`).

Phase 11B (Claude Desktop) claimed r=0.6135 for the base model and r=0.7338 for
the 9-prime extended model, with first significance crossing at +p=13,17.

Diagnostic test (Phase 12C + diagnostic script) tried all combinations of:
- y variables: band_deltas_ensemble, band_deltas_seed1, actual_sr_symmetry
- x variables: rc_full (stored), rc_p2 (stored), recomputed R_c (base), recomputed R_c (9-prime)

Result: maximum r from any stored-data combination = 0.5793. Phase 11B r values
are not reproducible from `rh_phase10a_definitive.json`.

---

## Re-Verification Protocol (Claude Desktop + CAILculator)

### Step 1: Load authoritative band data

Load `rh_phase10a_definitive.json`. Extract and confirm:
- t_mids: [125, 317, 470, 612, 747, 875, 1002, 1124, 1244, 1361]
- actual_sr_symmetry: [0.7402, 0.7705, 0.7310, 0.7475, 0.7362, 0.7517,
                       0.7140, 0.7815, 0.7790, 0.7368]
- gue_ensemble_mean: 0.71346
- band_deltas_ensemble: [0.0267, 0.0570, 0.0176, 0.0341, 0.0227, 0.0382,
                         0.0005, 0.0680, 0.0656, 0.0233]

### Step 2: Define the R_c model exactly

For each prime p in the set, R_c(t) contributes:
  (1/sqrt(p)) * cos(log(p) * t)  +  (1/p) * cos(log(p^2) * t)

Evaluate at each of the 10 t_mids. This gives a 10-vector R_c.

### Step 3: Compute Pearson r at each prime step

Build R_c incrementally. At each step, compute Pearson r between:
  x = R_c vector (10 values)
  y = band_deltas_ensemble (10 values)

Report r at each step:

| Step | Primes | r | Significant? (>0.632) |
|---|---|---|---|
| Base | [2,3,5,7,11] | ? | ? |
| +p=13 | [2,3,5,7,11,13] | ? | ? |
| +p=13,17 | +17 | ? | ? |
| +p=13,17,19 | +19 | ? | ? |
| +p=13,17,19,23 | +23 | ? | ? |

### Step 4: Save all R_c vectors and r values to JSON

Save as `p_bk_reverif.json`:
```json
{
  "t_mids": [...],
  "band_deltas_ensemble": [...],
  "steps": [
    {
      "primes": [2, 3, 5, 7, 11],
      "rc_vector": [...],
      "r": ...,
      "significant": ...
    },
    ...
  ]
}
```

### Step 5: Compare to Phase 11B claims

| Model | Phase 11B r | Re-verification r | Match? |
|---|---|---|---|
| Base [2,3,5,7,11] | 0.6135 | ? | ? |
| +p=13,17 | 0.6793 | ? | ? |
| +p=23 (full) | 0.7338 | ? | ? |

---

## Expected Outcomes

**If re-verification matches Phase 11B (r~0.69-0.73):**
- Identify the discrepancy source (likely: Phase 12C used a slightly different
  R_c formula or normalization)
- BK significance confirmed; update CLAUDE.md

**If re-verification matches Phase 12C (peak r~0.58, sub-threshold):**
- Phase 11B significance was an error in that session
- Retract significance claim; update CLAUDE.md and paper draft

---

## Current Status

Phase 11B BK significance: **PROVISIONAL — retracted pending this re-verification**

Verified result from stored data (Phase 12C): **peak r=0.579, sub-threshold**
