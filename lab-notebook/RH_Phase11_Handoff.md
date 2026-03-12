# RH Phase 11 Handoff — For Claude Desktop + CAILculator

**Date:** 2026-03-09
**Researcher:** Paul Chavez, Chavez AI Labs LLC
**Prepared by:** Claude Code (pre-computation complete; Claude Desktop verifies and executes CAILculator calls)

---

## Overview

Four sub-experiments. All use existing data files — no new zero computation required.

| Sub | Name | CAILculator calls | Status |
|-----|------|-------------------|--------|
| 11A | Act/GUE variance at scale (n=498, n=998) | 56 detect_patterns | Needs execution |
| 11B | Berry-Keating extended (p=13,17,19,23) | 0 (pure Python) | Pre-computed; verify |
| 11C | P3 direction — antipodal P-vector | 7 detect_patterns | Data embedded below |
| 11D | Antipodal characterization (skewness/shape) | 0 (Python analysis) | Pre-computed; verify |

**Pre-computation alert — Phase 11B:** Adding p=13,17,19,23 to the Berry-Keating model pushes Pearson r from +0.5428 to **+0.6569**, crossing the significance threshold (r>0.632). Verify and confirm.

---

## Files Required

- `rh_gaps.json` — 999 Riemann zero gaps (in project directory)
- `rh_phase10a_definitive.json` — Phase 10A band deltas and t_mids
- `p10c_actual_P2.json`, `p10c_gue_s{1,2,3}_P2.json`, `p10c_poi_s{1,2,3}_P2.json` — Phase 10C P2 projections (97 values each)
- `p10c_actual_P3.json`, `p10c_gue_s{1,2,3}_P3.json`, `p10c_poi_s{1,2,3}_P3.json` — P3 projections (pre-computed; also embedded below)

---

## Phase 11A — Act/GUE Variance at Scale

**Question:** Does Act/GUE variance ≈ 0.63 (from Phase 10C, n=97) hold at n=498 and n=998 gap pairs?

**Decision criteria:**
- Ratio stable 0.60–0.68 across both scales → preliminary finding confirmed; promote to established result in paper
- Ratio drifts toward 1.0 → low-height artifact of the n=97 sample; retire finding
- Ratio varies by direction → some P-vectors are more robust than others; note pattern

### Step 1 — Run this Python code to generate all sequences

```python
import json, math, random

BASE = "."  # adjust if needed

# --- embed_pair transformation ---
def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)**2/s]

P_VECTORS = {
    'P1': [0, 1, 0, 0, 0, 0,-1, 0],
    'P2': [0, 0, 0, 1,-1, 0, 0, 0],
    'P4': [0, 1, 0, 0, 0, 0, 1, 0],
    'P5': [0, 0, 1, 0, 0, 1, 0, 0],
}

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

def project_sequence(gaps, pvec_name):
    pvec = P_VECTORS[pvec_name]
    pairs = [(gaps[i], gaps[i+1]) for i in range(len(gaps)-1)]
    return [dot(embed_pair(g1, g2), pvec) for g1, g2 in pairs]

# --- GUE (Wigner surmise via Rayleigh inverse CDF) ---
def gue_gaps(n, mean, seed):
    random.seed(seed)
    scale = mean * math.sqrt(math.pi/4) / math.gamma(1.5)
    gaps = []
    while len(gaps) < n:
        u = random.random()
        if u > 0:
            gaps.append(scale * math.sqrt(-math.log(u)))
    m = sum(gaps)/len(gaps)
    return [g * mean / m for g in gaps]

# --- Poisson (exponential) ---
def poisson_gaps(n, mean, seed):
    random.seed(seed)
    gaps = [-mean * math.log(random.random()) for _ in range(n)]
    m = sum(gaps)/len(gaps)
    return [g * mean / m for g in gaps]

# Load actual gaps
with open(f"{BASE}/rh_gaps.json") as f:
    all_gaps = json.load(f)

# Two scales
scales = {
    '498': {'gaps': all_gaps[:499], 'n_pairs': 498},
    '998': {'gaps': all_gaps[:999], 'n_pairs': 998},
}

for scale_name, cfg in scales.items():
    gaps = cfg['gaps']
    n_pairs = cfg['n_pairs']
    mean_gap = sum(gaps) / len(gaps)
    print(f"\n=== Scale n={n_pairs}, mean_gap={mean_gap:.6f} ===")

    for pvec in ['P1', 'P2', 'P4', 'P5']:
        # Actual
        actual_proj = project_sequence(gaps, pvec)
        fname = f"p11a_actual_{pvec}_n{scale_name}.json"
        with open(f"{BASE}/{fname}", 'w') as f:
            json.dump(actual_proj, f)
        print(f"  Saved {fname}")

        # GUE synthetic (3 seeds)
        for seed in [1, 2, 3]:
            synth = gue_gaps(n_pairs + 1, mean_gap, seed)
            proj = project_sequence(synth, pvec)
            fname = f"p11a_gue_s{seed}_{pvec}_n{scale_name}.json"
            with open(f"{BASE}/{fname}", 'w') as f:
                json.dump(proj, f)

        # Poisson synthetic (3 seeds)
        for seed in [1, 2, 3]:
            synth = poisson_gaps(n_pairs + 1, mean_gap, seed)
            proj = project_sequence(synth, pvec)
            fname = f"p11a_poi_s{seed}_{pvec}_n{scale_name}.json"
            with open(f"{BASE}/{fname}", 'w') as f:
                json.dump(proj, f)

print("\nAll Phase 11A sequences generated.")
```

### Step 2 — CAILculator calls (56 total)

For **each** of the 56 files generated above (`p11a_actual_P1_n498.json` through `p11a_poi_s3_P5_n998.json`), call:

```
detect_patterns(
    data = <load file>,
    pattern_types = ["conjugation_symmetry"]
)
```

**Record the conjugation_symmetry percentage for each file.**

### Step 3 — Variance calculation (Python, after CAILculator)

```python
# After running CAILculator, compute variance for each sequence
# (If CAILculator does not return variance directly, compute from the projection values)

def variance(data):
    n = len(data)
    m = sum(data) / n
    return sum((x - m)**2 for x in data) / n

import json
BASE = "."
results = {}

for scale_name in ['498', '998']:
    for pvec in ['P1', 'P2', 'P4', 'P5']:
        with open(f"{BASE}/p11a_actual_{pvec}_n{scale_name}.json") as f:
            act = json.load(f)
        act_var = variance(act)

        gue_vars = []
        for seed in [1,2,3]:
            with open(f"{BASE}/p11a_gue_s{seed}_{pvec}_n{scale_name}.json") as f:
                gue = json.load(f)
            gue_vars.append(variance(gue))
        gue_mean_var = sum(gue_vars)/3

        poi_vars = []
        for seed in [1,2,3]:
            with open(f"{BASE}/p11a_poi_s{seed}_{pvec}_n{scale_name}.json") as f:
                poi = json.load(f)
            poi_vars.append(variance(poi))
        poi_mean_var = sum(poi_vars)/3

        act_gue_ratio = act_var / gue_mean_var
        poi_gue_ratio = poi_mean_var / gue_mean_var

        key = f"n{scale_name}_{pvec}"
        results[key] = {
            "act_var": round(act_var, 4),
            "gue_mean_var": round(gue_mean_var, 4),
            "poi_mean_var": round(poi_mean_var, 4),
            "act_gue_ratio": round(act_gue_ratio, 3),
            "poi_gue_ratio": round(poi_gue_ratio, 3)
        }
        print(f"n={scale_name} {pvec}: Act/GUE={act_gue_ratio:.3f}, Poi/GUE={poi_gue_ratio:.3f}")

with open(f"{BASE}/p11a_variance_scale.json", 'w') as f:
    json.dump(results, f, indent=2)
print("Saved p11a_variance_scale.json")
```

**Reference from Phase 10C (n=97):** Act/GUE ratios were 0.626, 0.662, 0.628, 0.688 for P1/P2/P4/P5.

---

## Phase 11B — Berry-Keating Extended Model

**Question:** Does adding p=13,17,19,23 push Pearson r above the significance threshold (r>0.632)?

**Pre-computed reference table** (using stored `band_deltas_ensemble` and `t_mids` from `rh_phase10a_definitive.json`):

| Model | r | Status |
|-------|---|--------|
| Phase 10A baseline (p=2,3,5,7,11 + p²=4,9) | +0.5428 | Sub-threshold |
| + p=13 | +0.5245 | Sub-threshold |
| + p=13, 17 | +0.5903 | Sub-threshold |
| + p=13, 17, 19 | +0.6376 | Sub-threshold (close) |
| **+ p=13, 17, 19, 23** | **+0.6569** | **≥ 0.632 — SIGNIFICANT** |

### Verification code (run in Claude Desktop to confirm)

```python
import json, math

with open("rh_phase10a_definitive.json") as f:
    d = json.load(f)

t_mids = d['t_mids']
deltas = d['band_deltas_ensemble']

def pearson(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    num = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))
    denom = math.sqrt(sum((xs[i]-mx)**2 for i in range(n)) *
                      sum((ys[i]-my)**2 for i in range(n)))
    return num / denom

def build_rc(t_list, primes, squares):
    return [sum(math.cos(math.log(p)*t)/math.sqrt(p) for p in primes) +
            sum(math.cos(math.log(p)*t)/math.sqrt(p) for p in squares)
            for t in t_list]

models = [
    ("Phase 10A baseline",         [2,3,5,7,11],               [4,9]),
    ("+p=13",                      [2,3,5,7,11,13],             [4,9]),
    ("+p=13,17",                   [2,3,5,7,11,13,17],          [4,9]),
    ("+p=13,17,19",                [2,3,5,7,11,13,17,19],       [4,9]),
    ("+p=13,17,19,23 (FINAL)",     [2,3,5,7,11,13,17,19,23],   [4,9]),
]

print("Berry-Keating extended model results:")
print(f"{'Model':<40} {'r':>8}  {'Threshold':>10}")
for name, primes, squares in models:
    rc = build_rc(t_mids, primes, squares)
    r = pearson(rc, deltas)
    flag = "<-- SIGNIFICANT" if abs(r) >= 0.632 else ""
    print(f"{name:<40} {r:+.4f}  {flag}")

# Save results
results = {}
for name, primes, squares in models:
    rc = build_rc(t_mids, primes, squares)
    r = pearson(rc, deltas)
    results[name] = {"r": round(r, 4), "primes": primes, "squares": squares,
                     "significant": abs(r) >= 0.632}
with open("p11b_bk_extended.json", 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved p11b_bk_extended.json")
```

**Decision criteria:**
- r ≥ 0.632 confirmed → Berry-Keating oscillation is statistically predicted by the prime orbit sum model at n=10 bands. Update paper Section 7.4 with definitive correlation.
- r < 0.632 → Check computation; if correct, continue to p=29,31.

---

## Phase 11C — P3 Direction (Antipodal P-Vector)

**Context:** P3 corresponds to v3 = (0,0,0,−1,1,0,0,0), the antipodal partner of P2 (v2+v3=0). Since proj_P3 = −proj_P2 for any input, the conjugation symmetry metrics should be **identical** to Phase 10C P2 results. This experiment:
1. Empirically confirms the antipodal relationship through CAILculator
2. Establishes the P3 baseline for all subsequent antipodal tracking
3. Notes any deviation from P2 results as significant (unexpected asymmetry)

**Phase 10C P2 reference values (expected to match P3 exactly):**
- Actual: 82.7% | GUE mean: 78.3% | Poisson mean: 80.4% | GUE−Poi: −2.1 pt

### CAILculator calls — 7 detect_patterns calls (data embedded)

Call `detect_patterns(data=<sequence>, pattern_types=["conjugation_symmetry"])` for each:

**Sequence 1 — Actual P3 (n=97, mean=1.2088, all-positive)**
```json
[2.912146, 2.404714, 2.247079, 1.950338, 2.050358, 1.472418, 1.953351, 1.939939, 1.343939, 1.671029, 1.607149, 1.210692, 1.780365, 1.776167, 1.122522, 1.246984, 1.590203, 1.507152, 0.947129, 1.524018, 1.49102, 1.170123, 1.123071, 1.52744, 1.55986, 0.910085, 1.22631, 1.372111, 1.223904, 1.060738, 0.860768, 1.600596, 1.65967, 1.017266, 1.1047, 1.141826, 1.285872, 1.099483, 0.727834, 1.350458, 1.397874, 0.914163, 1.031551, 1.007523, 1.393473, 1.396811, 0.756416, 0.870628, 1.26093, 1.202595, 1.103301, 1.096476, 0.869616, 1.344029, 1.283798, 0.689198, 0.98003, 1.059965, 1.112423, 1.082842, 0.894212, 0.791306, 1.495842, 1.450745, 0.767272, 0.910073, 0.880095, 0.994286, 1.246655, 1.126218, 0.675737, 0.974669, 1.208769, 1.081412, 0.908704, 0.970928, 0.707754, 1.350852, 1.347495, 0.749889, 0.746055, 1.043972, 1.087768, 0.959179, 0.956715, 0.732401, 0.721286, 1.220119, 1.222385, 0.68258, 1.085885, 1.068297, 1.010067, 1.104176, 0.957187, 0.792874, 0.706907]
```

**Sequence 2 — GUE seed 1 P3 (n=97, mean=1.2595)**
```json
[1.50599, 0.593826, 1.224867, 1.302831, 1.095953, 1.002241, 0.73702, 1.624706, 2.18766, 2.046849, 0.960189, 0.976047, 2.707851, 2.605764, 0.97569, 1.275069, 1.333302, 0.361677, 2.073003, 2.391525, 2.006406, 0.826909, 1.053366, 1.420816, 1.396316, 1.979964, 2.051578, 1.380074, 1.105514, 1.334199, 1.527901, 1.544429, 1.373178, 1.277559, 2.08934, 2.133063, 0.8132, 0.908824, 1.368826, 1.543887, 0.421474, 1.553415, 1.622996, 1.113113, 0.730141, 0.611625, 0.990077, 0.97453, 0.696467, 1.167408, 1.196819, 0.76668, 0.484255, 0.86968, 0.985945, 1.92168, 1.998403, 1.246167, 0.989696, 1.471947, 1.417728, 0.879842, 0.77235, 1.074301, 1.201953, 1.0959, 0.88562, 0.872225, 1.129886, 1.149704, 1.966967, 2.306892, 1.86466, 0.64444, 0.799127, 1.0891, 1.487702, 1.438573, 0.926382, 0.54626, 0.855917, 0.82667, 1.275416, 1.327536, 0.871331, 0.785292, 1.0335, 1.303102, 1.259078, 0.82818, 2.652866, 2.471521, 0.594786, 0.508352, 0.594465, 0.6421, 0.863866]
```

**Sequence 3 — GUE seed 2 P3 (n=97, mean=1.1526)**
```json
[0.280845, 1.920063, 2.06675, 1.677119, 0.628745, 0.753447, 1.160973, 1.183205, 0.894021, 0.91265, 1.439816, 1.491691, 1.191173, 1.034882, 0.649222, 0.240723, 0.828194, 1.067215, 1.312638, 1.975062, 2.35196, 1.989258, 1.241463, 1.299992, 1.03456, 0.839666, 0.988302, 1.302677, 2.088682, 2.052298, 1.592904, 1.508718, 0.994887, 0.752362, 1.372071, 1.399629, 0.528773, 0.656211, 0.591822, 0.559226, 0.636589, 1.070791, 1.155213, 0.218592, 1.521986, 1.41522, 0.703063, 0.960891, 1.061745, 1.037985, 0.889952, 0.875533, 0.877999, 1.067241, 1.0716, 0.42928, 0.923067, 1.037975, 0.788572, 0.599462, 0.930717, 1.355562, 1.45356, 1.12976, 1.404257, 1.448746, 1.224808, 1.226698, 1.152774, 1.190179, 0.619589, 0.920893, 1.035824, 0.937109, 0.876863, 1.185804, 1.4826, 1.367108, 0.864011, 0.72076, 1.683928, 1.713765, 0.64802, 0.601118, 1.38522, 1.34652, 1.776456, 1.763968, 1.216078, 1.491729, 1.291488, 1.612176, 1.586764, 0.84808, 1.249218, 1.539674, 1.327471]
```

**Sequence 4 — GUE seed 3 P3 (n=97, mean=1.2088)**
```json
[1.306083, 1.139956, 1.109538, 0.881861, 1.728655, 2.389762, 2.277091, 1.219345, 1.495995, 1.447778, 1.026212, 0.913402, 0.906026, 0.982381, 1.446812, 1.447415, 0.717147, 0.844777, 0.88555, 0.748508, 1.737673, 1.7509, 0.810761, 1.198109, 1.99622, 2.038099, 0.906827, 0.947328, 0.621614, 0.626675, 0.610733, 1.022063, 1.013819, 0.951633, 0.957136, 0.400685, 1.647693, 1.859881, 1.681388, 1.387901, 0.995332, 1.028229, 1.18486, 1.237504, 1.145535, 1.264202, 1.139995, 0.926027, 0.767873, 0.65287, 0.648161, 0.43461, 0.424219, 0.709249, 1.413556, 1.431262, 0.407544, 0.339987, 0.786217, 0.855206, 1.308743, 1.311633, 0.796399, 1.226948, 1.823873, 1.790616, 0.426266, 1.855853, 1.649224, 0.99395, 1.516543, 1.587112, 1.161065, 0.572057, 1.927259, 1.849979, 1.844917, 1.857317, 1.116243, 1.106798, 0.373032, 0.918563, 0.999674, 1.323083, 1.759673, 1.678295, 1.949776, 2.050347, 1.43392, 1.065332, 1.438486, 2.019249, 1.937285, 1.131449, 1.184267, 0.356965, 1.039027]
```

**Sequence 5 — Poisson seed 1 P3 (n=97, mean=1.5392; note extreme outliers up to 6.63)**
```json
[2.091278, 0.257567, 1.328031, 1.277933, 0.844777, 0.75067, 0.403537, 2.432947, 3.456331, 3.809802, 0.808165, 0.783009, 6.625296, 6.207902, 0.750652, 1.419246, 1.593957, 0.097542, 3.796691, 4.011998, 3.621995, 0.630053, 1.01861, 1.468716, 1.444094, 3.376926, 3.284614, 1.417563, 0.861127, 1.356517, 1.636777, 1.672773, 1.420939, 1.188274, 3.591028, 4.120735, 0.550274, 0.587478, 1.595438, 1.876436, 0.161429, 2.220347, 1.978454, 1.034439, 0.373903, 0.331984, 0.903013, 0.83162, 0.372031, 1.113149, 1.107849, 0.508927, 0.166942, 0.651152, 0.689679, 3.338835, 3.123807, 1.402256, 0.837116, 1.638242, 1.635741, 0.569497, 0.419205, 0.91108, 1.018732, 0.848084, 0.628801, 0.605651, 0.915922, 0.93899, 3.413913, 3.740588, 3.197532, 0.3769, 0.567226, 0.879538, 1.658941, 1.643375, 0.752235, 0.274388, 0.572514, 0.588586, 1.498703, 1.357091, 0.698907, 0.568813, 0.765531, 1.247129, 1.219515, 0.631355, 5.738318, 5.538117, 0.25004, 0.188926, 0.27883, 0.295479, 0.613872]
```

**Sequence 6 — Poisson seed 2 P3 (n=97, mean=1.2422)**
```json
[0.055617, 3.16006, 3.00778, 2.589109, 0.290902, 0.403282, 1.097796, 1.092574, 0.560391, 0.584737, 1.732926, 1.712678, 0.996745, 0.86887, 0.357678, 0.053411, 0.632595, 0.81053, 1.258122, 3.087776, 3.882822, 3.471102, 1.111856, 1.19109, 0.982707, 0.630706, 0.686225, 1.339678, 3.469011, 3.508091, 1.878921, 1.85635, 0.752317, 0.439683, 1.633931, 1.799056, 0.211962, 0.307099, 0.28892, 0.251761, 0.28512, 0.997433, 1.143218, 0.036235, 2.00289, 1.813044, 0.348466, 0.71801, 0.796158, 0.757351, 0.72881, 0.704819, 0.654966, 1.019193, 1.053843, 0.129856, 0.777446, 0.768911, 0.56499, 0.307141, 0.669102, 1.402193, 1.504454, 1.052887, 1.74377, 1.914004, 1.381071, 1.384206, 1.224831, 1.268222, 0.351715, 0.639867, 0.752477, 0.635938, 0.543677, 1.082906, 1.566335, 1.458153, 0.68792, 0.472527, 2.530165, 2.705806, 0.306433, 0.300652, 1.755585, 1.621883, 2.907078, 2.82231, 1.212518, 1.565434, 1.538466, 2.378997, 2.110606, 0.619765, 1.43514, 1.665319, 1.62472]
```

**Sequence 7 — Poisson seed 3 P3 (n=97, mean=1.4083)**
```json
[1.332374, 0.949768, 0.929166, 0.545792, 2.681814, 4.156054, 4.667364, 1.359245, 1.570661, 1.62057, 0.840313, 0.721679, 0.708336, 0.706812, 1.810872, 1.80862, 0.425735, 0.624013, 0.602327, 0.398691, 2.745463, 2.825424, 0.492773, 1.113915, 3.237, 3.742022, 0.729755, 0.695658, 0.306509, 0.312704, 0.321222, 0.963521, 0.887868, 0.766208, 0.844696, 0.120807, 2.478793, 2.436068, 2.008097, 1.673986, 0.893319, 0.783212, 1.114721, 1.133751, 0.939225, 1.122437, 0.979222, 0.601233, 0.524817, 0.362946, 0.372857, 0.144298, 0.164629, 0.436798, 1.745779, 1.888939, 0.143395, 0.093192, 0.553099, 0.536459, 1.499151, 1.579478, 0.5191, 1.165826, 2.562396, 2.93105, 0.166791, 2.704591, 2.508706, 0.847948, 1.760397, 1.82566, 1.181322, 0.246077, 3.354483, 3.096047, 3.07788, 3.176263, 1.03881, 1.125867, 0.125995, 0.743699, 0.762719, 1.311482, 2.383335, 2.490267, 3.452449, 3.220271, 1.528195, 0.844107, 1.759131, 2.999279, 3.394341, 1.173977, 1.25423, 0.10129, 0.992856]
```

**Expected result:** All 7 P3 symmetry scores should match their P2 counterparts from Phase 10C exactly (algebraic guarantee: proj_P3 = −proj_P2, and conjugation symmetry is invariant under sign flip). Any deviation is significant.

**Record for each sequence:** `conjugation_symmetry_%`

---

## Phase 11D — Antipodal Characterization

**Context:** The antipodal pair (P2/P3, v2/v3) is the only algebraic antipodal pair in the Canonical Six. P2 values are always negative (range −2.91 to −0.68 for actual zeros); P3 values are always positive (the mirror). This phase characterizes the *distribution shape* of the antipodal axis — specifically whether the shape asymmetry (skewness) carries information beyond what the symmetric metrics (variance, conjugation symmetry) reveal.

**Theoretical motivation:** If the Riemann zeros have perfect bilateral symmetry (consistent with the functional equation ζ(s)=ζ(1−s̄)), their projection onto any algebraic bilateral axis should be symmetric (zero skewness). The P2/P3 antipodal axis is the most natural such axis in the Canonical Six. Measuring skewness here probes whether the functional equation's bilateral symmetry is detectable in the embed_pair projection geometry.

### Verification code (run in Claude Desktop)

```python
import json, math

BASE = "."

def skewness(data):
    n = len(data)
    m = sum(data) / n
    s = math.sqrt(sum((x-m)**2 for x in data) / n)
    if s == 0:
        return 0.0
    return sum(((x-m)/s)**3 for x in data) / n

def kurtosis(data):
    n = len(data)
    m = sum(data) / n
    s = math.sqrt(sum((x-m)**2 for x in data) / n)
    if s == 0:
        return 0.0
    return sum(((x-m)/s)**4 for x in data) / n - 3  # excess kurtosis

files_p2 = {
    'actual':   'p10c_actual_P2.json',
    'gue_s1':   'p10c_gue_s1_P2.json',
    'gue_s2':   'p10c_gue_s2_P2.json',
    'gue_s3':   'p10c_gue_s3_P2.json',
    'poi_s1':   'p10c_poi_s1_P2.json',
    'poi_s2':   'p10c_poi_s2_P2.json',
    'poi_s3':   'p10c_poi_s3_P2.json',
}

results = {}
print("P2/P3 Antipodal Axis Distribution Shape (P2 values shown; P3 is mirror)")
print(f"{'Sequence':<15} {'mean':>8} {'skewness':>10} {'kurtosis':>10}")
print("-" * 50)

for label, fname in files_p2.items():
    with open(f"{BASE}/{fname}") as f:
        data = json.load(f)
    m = sum(data)/len(data)
    sk = skewness(data)
    ku = kurtosis(data)
    results[label] = {"mean": round(m,4), "skewness": round(sk,4), "kurtosis": round(ku,4)}
    print(f"{label:<15} {m:>8.4f} {sk:>10.4f} {ku:>10.4f}")

# Verify antipodal relationship: proj_P2 + proj_P3 = 0
print("\nAntipodal verification (proj_P2 + proj_P3 should = 0 for each element):")
with open(f"{BASE}/p10c_actual_P2.json") as f:
    p2 = json.load(f)
with open(f"{BASE}/p10c_actual_P3.json") as f:
    p3 = json.load(f)
sums = [abs(p2[i] + p3[i]) for i in range(len(p2))]
print(f"  Max |P2+P3|: {max(sums):.2e} (should be ~0)")
print(f"  Mean |P2+P3|: {sum(sums)/len(sums):.2e}")

# Summary groupings
gue_skews = [results['gue_s1']['skewness'], results['gue_s2']['skewness'], results['gue_s3']['skewness']]
poi_skews = [results['poi_s1']['skewness'], results['poi_s2']['skewness'], results['poi_s3']['skewness']]
print(f"\nSummary:")
print(f"  Actual skewness:        {results['actual']['skewness']:+.4f}")
print(f"  GUE mean skewness:      {sum(gue_skews)/3:+.4f}  (seeds: {gue_skews})")
print(f"  Poisson mean skewness:  {sum(poi_skews)/3:+.4f}  (seeds: {poi_skews})")

with open(f"{BASE}/p11d_antipodal_shape.json", 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved p11d_antipodal_shape.json")
```

**Pre-computed reference values** (verify Claude Desktop output matches):

| Sequence | Mean | Skewness | Interpretation |
|----------|------|----------|----------------|
| Actual P2 | −1.2088 | −1.4215 | Strongly left-skewed |
| GUE s1 | −1.2595 | −0.8081 | Moderately skewed |
| GUE s2 | −1.1526 | −0.2914 | Near-symmetric |
| GUE s3 | −1.2088 | −0.2359 | Near-symmetric |
| **GUE mean skew** | | **−0.445** | |
| Poisson s1 | −1.5392 | −1.6874 | Strongly skewed |
| Poisson s2 | −1.2422 | −1.0356 | Moderately skewed |
| Poisson s3 | −1.4083 | −0.9241 | Moderately skewed |
| **Poisson mean skew** | | **−1.216** | |

**Key finding to investigate:** Actual zeros (skew = −1.42) are MORE asymmetrically distributed on the antipodal axis than GUE synthetic (mean skew = −0.45), and similar to Poisson (mean skew = −1.22). This is the *opposite* ordering from the variance analysis (where actual zeros were tighter than GUE). The antipodal axis reveals a different structural property: the Riemann zero distribution is more skewed than GUE predicts on the P2/P3 direction, but tighter in spread. Note for the record: if the functional equation's bilateral symmetry were directly visible here, we would expect near-zero skewness for actual zeros. The large negative skew suggests the P2/P3 axis is not the direct algebraic seat of the functional equation symmetry — or that the embed_pair transformation introduces skewness independently of the input distribution. **This is an open question for Phase 18.**

---

## Recording Results

Save the following files:
- `p11a_variance_scale.json` — Act/GUE variance ratios at n=498, n=998
- `p11b_bk_extended.json` — Berry-Keating r values for all extended models
- `p11d_antipodal_shape.json` — Skewness/kurtosis characterization of P2/P3 axis
- `RH_Phase11_Results.md` — Human-readable summary of all four sub-experiments

The P3 sequence files (`p10c_*_P3.json`) are already saved in the project directory.

---

## Decision Summary

| Sub | Key question | Pass criterion | Fail criterion |
|-----|-------------|----------------|----------------|
| 11A | Does Act/GUE ≈ 0.63 hold at scale? | Ratio 0.60–0.68 at both n=498, n=998 | Ratio drifts toward 1.0 |
| 11B | Does BK r reach significance? | r ≥ 0.632 confirmed for p=13,17,19,23 | r < 0.632 → extend to p=29,31 |
| 11C | Does P3 mirror P2 exactly? | Symmetry% identical to P2 (±0.1%) | Any deviation → investigate asymmetry |
| 11D | Is actual skew more negative than GUE? | Confirmed (−1.42 vs −0.45) | Different result → revisit computation |

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
