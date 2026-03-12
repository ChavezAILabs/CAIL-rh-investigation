"""
RH Phase 10C Data Preparation
Generates GUE (Wigner surmise) and Poisson synthetic gap sequences,
applies embed_pair 8D projection, then dot-products with Canonical Six
P-vectors P1, P2, P4, P5.

Output: 28 JSON files — 4 actual + 12 GUE + 12 Poisson
Each file contains 96 scalar values (97 gap pairs → 96 projections).
Wait: 98 gaps → 97 consecutive pairs → 97 embed_pair vectors → 97 dot products.
"""

import json
import math
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Load actual gaps ---
with open(os.path.join(script_dir, 'rh_gaps.json'), 'r') as f:
    all_gaps = json.load(f)

# First 98 gaps (from first 99 zeros) → 97 consecutive pairs
gaps_actual = all_gaps[:98]
N_GAPS  = len(gaps_actual)   # 98
N_PAIRS = N_GAPS - 1         # 97
mean_gap = sum(gaps_actual) / len(gaps_actual)

print(f"Actual gaps: {N_GAPS}, mean={mean_gap:.6f}")
print(f"Consecutive pairs: {N_PAIRS}")

# --- P-vectors (Canonical Six v1.3, 8D) ---
# embed_pair(g1,g2) = [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
# Indexing:          [ 0   1    2       3          4          5     6       7        ]
P_VECTORS = {
    'P1': [0,  1,  0,  0,  0,  0, -1,  0],   # v1 = (0,1,0,0,0,0,-1,0)  g2-g7
    'P2': [0,  0,  0,  1, -1,  0,  0,  0],   # v2 = (0,0,0,1,-1,0,0,0)  g4-g5
    'P4': [0,  1,  0,  0,  0,  0,  1,  0],   # v4 = (0,1,0,0,0,0,1,0)   g2+g7
    'P5': [0,  0,  1,  0,  0,  1,  0,  0],   # v5 = (0,0,1,0,0,1,0,0)   g3+g6
}

def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1 - g2, g1*g2/s, (g1+g2)/2.0, g1/s, g2/s, (g1-g2)**2/s]

def dot(v, w):
    return sum(a*b for a, b in zip(v, w))

def project_sequence(gaps, p_vec):
    """Project 97 consecutive gap pairs onto P-vector. Returns list of 97 scalars."""
    result = []
    for i in range(len(gaps) - 1):
        emb = embed_pair(gaps[i], gaps[i+1])
        result.append(dot(emb, p_vec))
    return result

# --- Wigner surmise sampler (GUE) ---
# P(s) = (pi/2) * s * exp(-pi*s^2/4), mean=1
# Equivalent to Rayleigh(scale=sqrt(2/pi))
# Sample via inverse CDF: s = sqrt(-4/pi * log(1-u)) = sqrt(-4/pi * log(u))
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)  # Rayleigh scale for Wigner surmise
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0:
            continue
        # Rayleigh inverse CDF: x = scale * sqrt(-2 * log(u))
        x = scale * math.sqrt(-2.0 * math.log(u))
        samples.append(x * mean)   # scale to target mean
    return samples

# --- Poisson sampler ---
def sample_poisson(n, mean, seed):
    rng = random.Random(seed)
    # Exponential inverse CDF: x = -mean * log(u)
    return [-mean * math.log(rng.random() or 1e-300) for _ in range(n)]

# --- Project actual gaps ---
print("\nProjecting actual gaps...")
for p_name, p_vec in P_VECTORS.items():
    proj = project_sequence(gaps_actual, p_vec)
    out = os.path.join(script_dir, f'p10c_actual_{p_name}.json')
    with open(out, 'w') as f:
        json.dump(proj, f)
    print(f"  p10c_actual_{p_name}.json  ({len(proj)} values)")

# --- Generate synthetics and project ---
print()
for dist_name, sampler in [('gue', sample_wigner), ('poi', sample_poisson)]:
    for seed in [1, 2, 3]:
        gaps_syn = sampler(N_GAPS, mean_gap, seed)
        syn_mean = sum(gaps_syn) / len(gaps_syn)
        print(f"{dist_name.upper()} seed {seed}: mean={syn_mean:.4f} (target {mean_gap:.4f})")

        for p_name, p_vec in P_VECTORS.items():
            proj = project_sequence(gaps_syn, p_vec)
            out = os.path.join(script_dir, f'p10c_{dist_name}_s{seed}_{p_name}.json')
            with open(out, 'w') as f:
                json.dump(proj, f)
            print(f"  p10c_{dist_name}_s{seed}_{p_name}.json  ({len(proj)} values)")

# --- Save summary ---
summary = {
    "phase": "10C",
    "n_gaps": N_GAPS,
    "n_pairs": N_PAIRS,
    "mean_gap_actual": mean_gap,
    "p_vectors": P_VECTORS,
    "distributions": {
        "gue": "Wigner surmise Rayleigh(sqrt(2/pi)), scaled to mean_gap, seeds 1-3",
        "poisson": "Exponential(mean_gap), seeds 1-3"
    },
    "files": {
        "actual": [f"p10c_actual_{p}.json" for p in P_VECTORS],
        "gue": [f"p10c_gue_s{s}_{p}.json" for s in [1,2,3] for p in P_VECTORS],
        "poisson": [f"p10c_poi_s{s}_{p}.json" for s in [1,2,3] for p in P_VECTORS]
    }
}
with open(os.path.join(script_dir, 'p10c_prep_summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nDone. 28 JSON files created.")
print(f"  Actual:  4 files (p10c_actual_{{P}}.json)")
print(f"  GUE:    12 files (p10c_gue_s{{1,2,3}}_{{P}}.json)")
print(f"  Poisson: 12 files (p10c_poi_s{{1,2,3}}_{{P}}.json)")
print(f"  Summary: p10c_prep_summary.json")
print(f"\nReady for Phase 10C CAILculator detect_patterns calls.")
