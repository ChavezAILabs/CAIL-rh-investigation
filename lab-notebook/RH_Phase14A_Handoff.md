# RH Phase 14A -- 20-Band Chavez Symmetry BK Correlation: Handoff

**Date:** 2026-03-09
**For:** Claude Desktop + CAILculator MCP
**Data file:** `p14a_band_sequences.json`

---

## Objective

Compute Chavez conjugation symmetry for 20 height bands (actual zeros + GUE synthetic),
then correlate band_deltas with R_c(t_mid) to test BK significance at 20-band resolution.

Phase 12C found r=0.579 at 10 bands (threshold 0.632). With 20 bands, threshold drops
to 0.444 — potentially crossable with the correct statistic (Chavez conjugation symmetry).

---

## Data

File `p14a_band_sequences.json` contains:
- 20 bands (k=0..19), each with 500 zeros
- `actual_sr`: 498 spacing ratios for actual zeros
- `gue_sr`: spacing ratios for 5 GUE synthetic seeds (seed1..seed5)
- `t_mid`, `mean_gap`, `n_ratios` per band

---

## Protocol

### Step 1: Chavez Transform per band

For each band k=0..19:
1. Load `bands[k].actual_sr` — 498 spacing ratios
2. Run Chavez Transform: alpha=1.0, dimension_param=2, pattern_id=1
3. Record `conjugation_symmetry` → `actual_sym[k]`

For each band k=0..19 and each seed s in {seed1..seed5}:
1. Load `bands[k].gue_sr.seed{s}` — 498 GUE spacing ratios
2. Run Chavez Transform (same parameters)
3. Record `conjugation_symmetry` → `gue_sym[k][s]`

### Step 2: Compute band deltas

```
gue_mean[k] = mean(gue_sym[k][s] for s in {1..5})
band_delta[k] = actual_sym[k] - gue_mean[k]
```

### Step 3: Correlate with R_c

R_c values (9-prime BK formula) per band are pre-computed in `p14a_band_summary.json`:
```
rc_9prime = [-0.4116, 1.4343, -0.8424, 2.4231, 2.0344, 1.1700, 1.1239,
              0.2047, -0.9004, -0.7365, 0.3555, 0.0094, -1.5023, -0.4909,
              1.1344, -0.9580, 1.4338, 1.8417, -0.8304, 0.6344]
```

Compute Pearson r between `band_delta` (20 values) and `rc_9prime` (20 values).

Significance threshold: |r| > 0.444 (n=20, p<0.05, two-tailed)

### Step 4: Save results

Save as `p14a_results.json`:
```json
{
  "actual_sym": [<20 values>],
  "gue_sym": {"k0": {"seed1":..., "seed2":..., ...}, ...},
  "gue_mean_per_band": [<20 values>],
  "band_delta": [<20 values>],
  "rc_9prime": [<20 values>],
  "pearson_r": <value>,
  "significant": <true/false>,
  "threshold": 0.4438
}
```

---

## Expected Comparison

| Metric | Phase 12C (10-band) | Phase 14A (20-band target) |
|---|---|---|
| Statistic | Chavez conjugation symmetry | Chavez conjugation symmetry |
| n bands | 10 | 20 |
| Significance threshold | 0.632 | 0.444 |
| Best r found | 0.579 | ? |

Phase 12C used `band_deltas_ensemble` from `rh_phase10a_definitive.json` (heights 14-1419,
first 1,000 zeros). Phase 14A uses all 10,000 zeros (heights 14-9878), which includes
the full oscillatory range of R_c. If signal strength holds, 20-band resolution gives
a realistic path to significance.

---

## Band Reference Table

| Band | t_mid | n_ratios | mean_gap | R_c(9p) |
|---|---|---|---|---|
| 0 | 412.7 | 498 | 1.597 | −0.412 |
| 1 | 1116.1 | 498 | 1.216 | +1.434 |
| 2 | 1700.7 | 498 | 1.123 | −0.842 |
| 3 | 2248.5 | 498 | 1.069 | +2.423 |
| 4 | 2773.9 | 498 | 1.032 | +2.034 |
| 5 | 3283.0 | 498 | 1.003 | +1.170 |
| 6 | 3779.0 | 498 | 0.982 | +1.124 |
| 7 | 4265.9 | 498 | 0.963 | +0.205 |
| 8 | 4743.9 | 498 | 0.947 | −0.900 |
| 9 | 5214.5 | 498 | 0.935 | −0.737 |
| 10 | 5679.2 | 498 | 0.923 | +0.356 |
| 11 | 6138.1 | 498 | 0.913 | +0.009 |
| 12 | 6592.3 | 498 | 0.904 | −1.502 |
| 13 | 7041.7 | 498 | 0.894 | −0.491 |
| 14 | 7487.1 | 498 | 0.886 | +1.134 |
| 15 | 7928.7 | 498 | 0.880 | −0.958 |
| 16 | 8367.3 | 498 | 0.875 | +1.434 |
| 17 | 8802.3 | 498 | 0.866 | +1.842 |
| 18 | 9234.8 | 498 | 0.861 | −0.830 |
| 19 | 9664.0 | 498 | 0.857 | +0.634 |
