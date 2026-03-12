# RH Phase 10C Standalone Handoff — Color Group P-Vector Survey

**Date:** 2026-03-09
**Self-contained:** All data generation is embedded below. No local file upload needed.

---

## Context

Actual zero results (from Phase 9A, confirmed Phase 10C):

| P-vector | Direction | Actual% |
|----------|-----------|---------|
| P1 | g2−g7 | **79.6%** |
| P2 | g4−g5 | **82.7%** |
| P4 | g2+g7 | **80.7%** |
| P5 | g3+g6 | **64.6%** ← anomaly (level-repulsion sensitive) |

**P5 is ~16 pt below P1/P2/P4.** Phase 9A showed GUE ~52% and Poisson ~78% on P5 (single seeds). This phase establishes proper 3-seed baselines.

**Hypotheses:**
- P5: GUE ~52%, Poisson ~78% → 26 pt GUE/Poisson separation (level repulsion discriminant)
- P1/P2/P4: GUE ≈ Poisson ≈ 79–83% → non-discriminating directions

---

## Step 1 — Generate Data (run this Python code)

```python
import json, math, random

# Load actual Riemann zero gaps (first 98 gaps → 97 pairs)
# If rh_gaps.json is available, load it; otherwise use these precomputed first 98 gaps:
rh_gaps_98 = [
    6.8873145, 3.9888179, 5.4140185, 2.5101855, 4.6511166, 3.3325409, 2.4083543,
    4.6780776, 1.7686816, 3.196489,  3.4759262, 2.9007963, 1.4847345, 4.2807655,
    1.9672665, 2.4665912, 2.520756,  3.637533,  1.4401494, 2.192535,  3.5730058,
    1.8251121, 2.6897816, 1.3838366, 3.6827881, 2.1594448, 1.2192902, 2.96056,
    2.4866568, 2.407687,  1.721085,  1.7219881, 3.8609244, 0.8451236, 2.4455617,
    1.9064594, 2.5641025, 2.5793421, 1.5767043, 1.3099893, 3.2598653, 2.0620203,
    1.5089843, 2.4100487, 1.2587726, 3.3595323, 1.6201669, 1.3874985, 1.9881384,
    2.8891367, 1.4217829, 2.6307551, 0.8717372, 2.0994362, 3.0882155, 1.4846825,
    1.2523964, 2.338976,  1.8417455, 2.5063595, 1.6473708, 1.9100754, 0.8174611,
    3.49956,   1.342655,  1.6872428, 1.9359735, 1.5390762, 2.2905945, 2.6673894,
    0.7243158, 1.6301389, 2.1872361, 2.6104977, 1.0530702, 2.1856701, 1.6110852,
    1.1388278, 3.2494423, 1.2288426, 1.6960773, 1.2050254, 2.5115617, 1.6702508,
    2.1143529, 1.6570568, 1.1991254, 1.6224937, 2.8980578, 1.6473225, 0.7157867,
    2.5762947, 0.9763244, 2.4381196, 1.915969,  1.9127754, 0.7370466, 1.7061689
]
# Verified: 98 values, mean=2.240395, min=0.716, max=6.887 (matches rh_gaps.json exactly)

gaps_actual = rh_gaps_98
N_GAPS = len(gaps_actual)   # 98
N_PAIRS = N_GAPS - 1        # 97
mean_gap = sum(gaps_actual) / N_GAPS
print(f"Actual gaps: {N_GAPS}, mean={mean_gap:.6f}, pairs={N_PAIRS}")

# P-vector definitions (Canonical Six v1.3, 8D)
# embed_pair index: [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
P_VECTORS = {
    'P1': [0, 1, 0, 0, 0, 0, -1,  0],
    'P2': [0, 0, 0, 1,-1, 0,  0,  0],
    'P4': [0, 1, 0, 0, 0, 0,  1,  0],
    'P5': [0, 0, 1, 0, 0, 1,  0,  0],
}

def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2.0, g1/s, g2/s, (g1-g2)**2/s]

def dot(v, w):
    return sum(a*b for a,b in zip(v,w))

def project_sequence(gaps, p_vec):
    return [dot(embed_pair(gaps[i], gaps[i+1]), p_vec) for i in range(len(gaps)-1)]

def sample_wigner(n, mean, seed):
    """Wigner surmise: Rayleigh(sqrt(2/pi)) scaled to target mean."""
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    result = []
    while len(result) < n:
        u = rng.random()
        if u > 0:
            result.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return result

def sample_poisson(n, mean, seed):
    """Exponential(mean)."""
    rng = random.Random(seed)
    return [-mean * math.log(max(rng.random(), 1e-300)) for _ in range(n)]

# Project actual gaps
print("\n=== ACTUAL ZEROS ===")
for p_name, p_vec in P_VECTORS.items():
    proj = project_sequence(gaps_actual, p_vec)
    print(f"Actual {p_name}: {len(proj)} values")
    print(f"  DATA: {json.dumps(proj)}")

# Generate and project GUE synthetics
print("\n=== GUE SYNTHETIC (Wigner surmise) ===")
for seed in [1, 2, 3]:
    gaps_gue = sample_wigner(N_GAPS, mean_gap, seed)
    gue_mean = sum(gaps_gue)/len(gaps_gue)
    print(f"\nGUE seed {seed}: mean={gue_mean:.4f} (target {mean_gap:.4f})")
    for p_name, p_vec in P_VECTORS.items():
        proj = project_sequence(gaps_gue, p_vec)
        print(f"  GUE s{seed} {p_name}: {len(proj)} values")
        print(f"  DATA: {json.dumps(proj)}")

# Generate and project Poisson synthetics
print("\n=== POISSON SYNTHETIC (Exponential) ===")
for seed in [1, 2, 3]:
    gaps_poi = sample_poisson(N_GAPS, mean_gap, seed)
    poi_mean = sum(gaps_poi)/len(gaps_poi)
    print(f"\nPoisson seed {seed}: mean={poi_mean:.4f} (target {mean_gap:.4f})")
    for p_name, p_vec in P_VECTORS.items():
        proj = project_sequence(gaps_poi, p_vec)
        print(f"  POI s{seed} {p_name}: {len(proj)} values")
        print(f"  DATA: {json.dumps(proj)}")

print("\nDone. 28 projection sequences generated.")
```

---

## Step 2 — Run 28 detect_patterns Calls

For each DATA array printed above, pass it directly to detect_patterns:

```
detect_patterns(data=<DATA array>, pattern_types=["conjugation_symmetry"])
```

Order:
1. Actual P1, P2, P4, P5 (4 calls — re-confirms known values)
2. GUE s1 P1, P2, P4, P5 (4 calls)
3. GUE s2 P1, P2, P4, P5 (4 calls)
4. GUE s3 P1, P2, P4, P5 (4 calls)
5. Poisson s1 P1, P2, P4, P5 (4 calls)
6. Poisson s2 P1, P2, P4, P5 (4 calls)
7. Poisson s3 P1, P2, P4, P5 (4 calls)

---

## Step 3 — Build Discrimination Table

Fill in all values and compute means:

| P-vector | Actual% | GUE s1 | GUE s2 | GUE s3 | GUE mean | Poi s1 | Poi s2 | Poi s3 | Poi mean | Δ(act−GUE) | Δ(GUE−Poi) |
|----------|---------|--------|--------|--------|----------|--------|--------|--------|----------|-----------|-----------|
| P1 | 79.6% | | | | | | | | | | |
| P2 | 82.7% | | | | | | | | | | |
| P4 | 80.7% | | | | | | | | | | |
| P5 | **64.6%** | | | | | | | | | | |

**Key hypotheses to verify:**
- P5 GUE mean ≈ **52%**, P5 Poisson mean ≈ **78%** → GUE−Poisson ≈ 26 pt
- P1/P2/P4: GUE mean ≈ Poisson mean (< 5 pt difference)
- P5 actual (64.6%) between GUE and Poisson → actual zeros closer to GUE than Poisson

---

## Step 4 — Save Results

**File:** `RH_Phase10C_Results.md` — fill in the discrimination table

**File:** `rh_phase10c_results.json`:
```json
{
  "phase": "10C",
  "date": "2026-03-09",
  "methodology": "embed_pair 8D projection + detect_patterns conjugation_symmetry",
  "n_pairs": 97,
  "mean_gap": 2.2404,
  "actual": {"P1": 79.6, "P2": 82.7, "P4": 80.7, "P5": 64.6},
  "gue": {
    "P1": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P2": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P4": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P5": {"s1": ?, "s2": ?, "s3": ?, "mean": ?}
  },
  "poisson": {
    "P1": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P2": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P4": {"s1": ?, "s2": ?, "s3": ?, "mean": ?},
    "P5": {"s1": ?, "s2": ?, "s3": ?, "mean": ?}
  },
  "discrimination_table": [
    {"pvector": "P1", "actual": 79.6, "gue_mean": ?, "poisson_mean": ?, "delta_act_gue": ?, "delta_gue_poi": ?},
    {"pvector": "P2", "actual": 82.7, "gue_mean": ?, "poisson_mean": ?, "delta_act_gue": ?, "delta_gue_poi": ?},
    {"pvector": "P4", "actual": 80.7, "gue_mean": ?, "poisson_mean": ?, "delta_act_gue": ?, "delta_gue_poi": ?},
    {"pvector": "P5", "actual": 64.6, "gue_mean": ?, "poisson_mean": ?, "delta_act_gue": ?, "delta_gue_poi": ?}
  ]
}
```

---

## Decision Framework

| P5 GUE−Poisson separation | Verdict |
|--------------------------|---------|
| > 20 pt | **P5 confirmed as primary level-repulsion discriminant** |
| 15–20 pt | Moderate discriminant |
| < 10 pt | Check synthetic generation / mean matching |

| P5 actual vs GUE | Verdict |
|-----------------|---------|
| Within 5 pt | **Actual zeros cluster with GUE on P5** ← expected |
| > 10 pt above GUE | 64.6% is anomalously high; actual zeros are intermediate GUE/Poisson on P5 |

Note: The Phase 9A single-seed result was GUE≈52%, actual 52%, Poisson≈78%. However Phase 10C actual showed 64.6% — notably higher than the Phase 9A 52%. This discrepancy warrants attention: Phase 9A used raw gap sequences while Phase 10C used embed_pair projections. Both methods should be tracked separately in the results.

---

**Chavez AI Labs LLC · Applied Pathological Mathematics**
*"Better math, less suffering"*
