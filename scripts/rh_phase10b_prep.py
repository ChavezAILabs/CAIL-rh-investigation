"""
RH Phase 10B Data Preparation
Computes pair correlation R(alpha) sequences from rh_zeros_10k.json.
Produces empirical, GUE theoretical, and Poisson sequences for CAILculator.

Grid: delta_alpha=0.02, alpha=0.02 to 15.00, n=750 bins
"""

import json
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# --- Load zeros ---
with open(os.path.join(script_dir, 'rh_zeros_10k.json'), 'r') as f:
    zeros = json.load(f)

zeros = sorted(zeros)
N = len(zeros)
print(f"Loaded {N} zeros, range {zeros[0]:.4f} to {zeros[-1]:.4f}")

# --- Parameters ---
DELTA_ALPHA = 0.02
ALPHA_MAX   = 15.00
N_BINS      = int(ALPHA_MAX / DELTA_ALPHA)   # 750
alpha_centers = [DELTA_ALPHA * (k + 0.5) for k in range(N_BINS)]

print(f"Grid: delta_alpha={DELTA_ALPHA}, n_bins={N_BINS}, alpha range [{alpha_centers[0]:.3f}, {alpha_centers[-1]:.3f}]")

# --- Empirical R(alpha) ---
# For each reference zero gamma_i, compute local mean spacing:
#   Delta_i = 2*pi / log(gamma_i / (2*pi))
# For each pair (i, j) with j > i, compute normalized separation:
#   s_ij = (gamma_j - gamma_i) / Delta_i
# Histogram into bins; normalize so Poisson baseline = 1.

print("Computing empirical pair correlation R(alpha)...")

counts = [0] * N_BINS

for i in range(N):
    gamma_i = zeros[i]
    mean_spacing = 2.0 * math.pi / math.log(gamma_i / (2.0 * math.pi))
    max_raw_gap  = ALPHA_MAX * mean_spacing

    j = i + 1
    while j < N and (zeros[j] - zeros[i]) <= max_raw_gap:
        s = (zeros[j] - zeros[i]) / mean_spacing
        bin_k = int(s / DELTA_ALPHA)
        if 0 <= bin_k < N_BINS:
            counts[bin_k] += 1
        j += 1

    if i % 1000 == 0:
        print(f"  Progress: {i}/{N} zeros processed")

# Normalize: counts[k] / (N * DELTA_ALPHA) gives R(alpha)
# (Poisson would yield ~1.0 throughout)
R_empirical = [counts[k] / (N * DELTA_ALPHA) for k in range(N_BINS)]

# Sanity check: report a few key values
for alpha_check in [0.5, 1.0, 2.0]:
    k = int(alpha_check / DELTA_ALPHA) - 1
    if 0 <= k < N_BINS:
        print(f"  R({alpha_check:.1f}) = {R_empirical[k]:.4f}  (GUE theory: {1 - (math.sin(math.pi*alpha_check)/(math.pi*alpha_check))**2:.4f})")

# Bin quality check: flag bins with low counts
low_bins = sum(1 for c in counts if c < 10)
print(f"  Bins with count < 10: {low_bins} / {N_BINS}")

# --- GUE Theoretical R(alpha) ---
# R_GUE(alpha) = 1 - (sin(pi*alpha) / (pi*alpha))^2
R_gue = []
for alpha in alpha_centers:
    if alpha < 1e-10:
        R_gue.append(0.0)
    else:
        sinc = math.sin(math.pi * alpha) / (math.pi * alpha)
        R_gue.append(1.0 - sinc**2)

# --- Poisson R(alpha) ---
R_poisson = [1.0] * N_BINS

# --- Save ---
out_empirical = os.path.join(script_dir, 'p10b_empirical_ralpha.json')
out_gue       = os.path.join(script_dir, 'p10b_gue_ralpha.json')
out_poisson   = os.path.join(script_dir, 'p10b_poisson_ralpha.json')
out_summary   = os.path.join(script_dir, 'p10b_prep_summary.json')

with open(out_empirical, 'w') as f: json.dump(R_empirical, f)
with open(out_gue,       'w') as f: json.dump(R_gue, f)
with open(out_poisson,   'w') as f: json.dump(R_poisson, f)

summary = {
    "phase": "10B",
    "n_zeros": N,
    "zero_range": [zeros[0], zeros[-1]],
    "delta_alpha": DELTA_ALPHA,
    "n_bins": N_BINS,
    "alpha_range": [alpha_centers[0], alpha_centers[-1]],
    "low_count_bins": low_bins,
    "sample_values": {
        "R_empirical_05": R_empirical[int(0.5/DELTA_ALPHA)-1],
        "R_empirical_10": R_empirical[int(1.0/DELTA_ALPHA)-1],
        "R_gue_05":       R_gue[int(0.5/DELTA_ALPHA)-1],
        "R_gue_10":       R_gue[int(1.0/DELTA_ALPHA)-1],
    }
}
with open(out_summary, 'w') as f: json.dump(summary, f, indent=2)

print(f"\nDone.")
print(f"  {out_empirical}  ({N_BINS} values)")
print(f"  {out_gue}        ({N_BINS} values)")
print(f"  {out_poisson}    ({N_BINS} values)")
print(f"  {out_summary}")
print(f"\nReady for Phase 10B CAILculator calls.")
