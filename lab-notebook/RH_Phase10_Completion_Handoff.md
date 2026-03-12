# RH Phase 10 Completion Handoff

**Date:** 2026-03-09
**Phase:** 10B + 10C
**Prerequisite:** Run both prep scripts in terminal before opening Claude Desktop.

---

## Pre-Session: Run Prep Scripts

Open a terminal in `C:\dev\projects\Experiments_January_2026\Primes_2026\` and run:

```
python rh_phase10b_prep.py
python rh_phase10c_prep.py
```

**10B prep output** (~2–5 min, O(N²) with early cutoff):
- `p10b_empirical_ralpha.json` — 750 R(α) values from 10,000 zeros
- `p10b_gue_ralpha.json` — 750 GUE theoretical values
- `p10b_poisson_ralpha.json` — 750 Poisson values (flat 1.0)
- `p10b_prep_summary.json` — check for `low_count_bins` (should be near 0 with 10k zeros)

**10C prep output** (~5 sec):
- 28 JSON files: `p10c_{dist}_{seed}_{P}.json` where dist∈{actual,gue,poi}, seed∈{s1,s2,s3}, P∈{P1,P2,P4,P5}

---

## Phase 10B — R(α) with 10,000 Zeros

**Goal:** Establish the legitimate separation record at Δα=0.02, n=750. Phase 9B-ii got 33.9 pts but with only 1,000 zeros and 27 sparse bins — that result was spurious. With 10k zeros, bins should be dense. Predicted: 18–22 pt separation.

**Context:** Prior validated record is **14.7 pts** (Phase 9B-i, Δα=0.05, n=300, 1k zeros).

### Step 1 — Analyze three R(α) sequences

```
analyze_dataset(data=<load p10b_empirical_ralpha.json>, label="Empirical R(alpha) 10k zeros")
analyze_dataset(data=<load p10b_gue_ralpha.json>, label="GUE theoretical R(alpha)")
analyze_dataset(data=<load p10b_poisson_ralpha.json>, label="Poisson flat R(alpha)")
```

Record for each: conjugation_symmetry%, CV, transform_value.

### Step 2 — Compute separation

- Primary separation: Poisson symmetry% − Empirical symmetry%
- Secondary: GUE symmetry% − Empirical symmetry%
- Compare to Phase 8B record (12.5 pt) and Phase 9B-i validated record (14.7 pt)

### Step 3 — Sample R(α) values check

From `p10b_prep_summary.json`, verify:
- `R_empirical_05` ≈ 0.60–0.65 (should match Montgomery-Dyson, GUE theory = 0.595)
- `R_empirical_10` ≈ 0.98–1.02 (near Poisson at α=1)
- `low_count_bins` near 0 (validates the 10k zeros are sufficient)

### Decision Framework

| Separation | Verdict |
|-----------|---------|
| > 20 pt | **New series record** — confirms Δα=0.02 scaling law; predicted result achieved |
| 15–20 pt | **Solid extension** — scaling law holds; use for Phase 11 paper section |
| < 14.7 pt | **Unexpected** — investigate bin quality and normalization; check `low_count_bins` |

---

## Phase 10C — Color Group P-Vector Survey (GUE/Poisson Baselines)

**Goal:** Complete the discrimination table. We have actual zero results; need GUE and Poisson baselines for all four P-vectors.

**Actual zeros (already done):**
| P-vector | Actual% |
|----------|---------|
| P1 (g2−g7) | 79.6% |
| P2 (g4−g5) | 82.7% |
| P4 (g2+g7) | 80.7% |
| P5 (g3+g6) | **64.6%** ← anomaly |

**embed_pair(g1,g2)** = [g1, g2, g1-g2, g1·g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)²/s] where s=g1+g2.

**Hypotheses from Phase 9A:**
- P5 GUE ≈ 52%, P5 Poisson ≈ 78% → P5 is level-repulsion discriminant (26 pt separation expected)
- P1/P2/P4 GUE ≈ Poisson ≈ 78–83% → these directions are not discriminating

### Step 4 — Run 24 detect_patterns calls

**GUE seeds 1–3:**
```
detect_patterns(data=<load p10c_gue_s1_P1.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_gue_s1_P2.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_gue_s1_P4.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_gue_s1_P5.json>, pattern_types=["conjugation_symmetry"])
```
Repeat for seeds 2 and 3 (12 calls total for GUE).

**Poisson seeds 1–3:**
```
detect_patterns(data=<load p10c_poi_s1_P1.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_poi_s1_P2.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_poi_s1_P4.json>, pattern_types=["conjugation_symmetry"])
detect_patterns(data=<load p10c_poi_s1_P5.json>, pattern_types=["conjugation_symmetry"])
```
Repeat for seeds 2 and 3 (12 calls total for Poisson).

### Step 5 — Build Discrimination Table

Record all results and fill in:

| P-vector | Actual% | GUE mean% | Poisson mean% | Δ(actual−GUE) | Δ(GUE−Poisson) |
|----------|---------|-----------|---------------|--------------|----------------|
| P1 | 79.6% | ? | ? | ? | ? |
| P2 | 82.7% | ? | ? | ? | ? |
| P4 | 80.7% | ? | ? | ? | ? |
| P5 | 64.6% | ? | ? | ? | ? |

### Decision Framework

| P5 GUE−Poisson separation | Verdict |
|--------------------------|---------|
| > 20 pt | **Strong discriminant confirmed** — P5 direction is primary level-repulsion probe |
| 15–20 pt | **Moderate discriminant** — P5 useful but weaker than Phase 9A suggested |
| < 10 pt | **Unexpected** — check synthetic generation mean-matching |

For P1/P2/P4: GUE−Poisson separation < 5 pt expected (non-discriminating directions confirmed).

### Actual vs GUE ordering

- P5: actual (64.6%) should be close to GUE (~52%) — both significantly below Poisson (~78%)
- P1/P2/P4: actual should be near GUE and near Poisson (no discrimination)

---

## Step 6 — Save Results

After all CAILculator calls, save the complete results as:

**`RH_Phase10_Completion_Results.md`** — fill in both tables (10B separation, 10C discrimination table)

**`rh_phase10_completion_results.json`** with structure:
```json
{
  "phase": "10B+10C",
  "date": "2026-03-09",
  "phase_10b": {
    "n_zeros": 10000,
    "delta_alpha": 0.02,
    "n_bins": 750,
    "empirical_symmetry": <value>,
    "gue_symmetry": <value>,
    "poisson_symmetry": <value>,
    "gue_poisson_separation": <value>,
    "low_count_bins": <from prep summary>
  },
  "phase_10c": {
    "actual": {"P1": 79.6, "P2": 82.7, "P4": 80.7, "P5": 64.6},
    "gue": {"P1": {"s1":?, "s2":?, "s3":?, "mean":?}, ...},
    "poisson": {"P1": {"s1":?, "s2":?, "s3":?, "mean":?}, ...},
    "discrimination_table": [...]
  }
}
```

---

## Background Context

**Phase 10 status entering this session:**
- 10A ✓ COMPLETE: r=+0.543 (5-prime BK model), sub-threshold (p=0.105); all 10 bands positive delta
- 10B ⏸ NOW EXECUTING: rh_zeros_10k.json ready (10,000 zeros, computed 2026-03-09, 334.5 min)
- 10C ⚠ COMPLETING: actual zeros done; GUE/Poisson baselines pending

**Series records:**
- GUE/Poisson separation: 14.7 pt (Phase 9B-i, Δα=0.05, n=300) ← 10B aims to break this
- P5 discriminant: GUE ~52% vs Poisson ~78% ← 10C to confirm with proper baselines
- Berry-Keating r: +0.543 (Phase 10A, sub-threshold)

**Scaling law:** 6.9 pt (n=30) → 12.5 pt (n=150) → 14.7 pt (n=300). At n=750, predicted: 18–22 pt.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
