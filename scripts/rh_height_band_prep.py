"""
RH Height Band Survey — Data Preparation Script
================================================
Tests whether actual Riemann zeros increasingly exceed GUE synthetic
on Chavez conjugation symmetry as height grows.

10 non-overlapping bands of 100 zeros each (99 gaps -> 98 spacing ratios).
Bands 1 and 6 have existing results (Phase 4 and Phase 5B respectively).
This script generates the 8 missing bands.

Batches (to respect Claude Desktop session limits):
  Batch A: Bands 2-5  — 4 actual + 12 GUE = 16 CAILculator runs
  Batch B: Bands 7-10 — 4 actual + 12 GUE = 16 CAILculator runs

Naming: rh_hb{N}_actual_ratios.json
        rh_hb{N}_gue_seed{S}_ratios.json

Usage:
  python rh_height_band_prep.py
"""

import json
import math
import os
import numpy as np


# ---------------------------------------------------------------------------
# Known results from Phase 4 and Phase 5B (pre-filled, no CAILculator needed)
# ---------------------------------------------------------------------------

KNOWN_RESULTS = {
    1: {
        "zero_indices": "0-99",
        "chavez_symmetry_actual": 75.0,
        "gue_mean_symmetry": 76.9,
        "delta_actual_minus_gue": -1.9,
        "mean_ratio_actual": 0.610,
        "source": "Phase 4 (RH_SR_2026_001)"
    },
    6: {
        "zero_indices": "499-598",
        "chavez_symmetry_actual": 78.3,
        "gue_mean_symmetry": 76.8,
        "delta_actual_minus_gue": +1.5,
        "mean_ratio_actual": 0.6153,
        "source": "Phase 5B (RH_SCALE_2026_001)"
    }
}

# Bands to generate (all except 1 and 6)
NEW_BANDS = [2, 3, 4, 5, 7, 8, 9, 10]

BATCH_A = [2, 3, 4, 5]   # 16 CAILculator runs
BATCH_B = [7, 8, 9, 10]  # 16 CAILculator runs


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def band_indices(band_num):
    """Return (start, end) zero indices for a given band number (1-indexed)."""
    start = (band_num - 1) * 100
    return start, start + 100   # 100 zeros -> slice [start:end]


def compute_gaps(sequence):
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def compute_spacing_ratios(gaps):
    return [
        min(gaps[i], gaps[i + 1]) / max(gaps[i], gaps[i + 1])
        for i in range(len(gaps) - 1)
    ]


def mean_of(values):
    return sum(values) / len(values)


def sample_gue_wigner_gaps(n, mean, seed):
    """GUE Wigner surmise P(s) = (32/pi^2)*s^2*exp(-4s^2/pi), scaled to target mean."""
    rng = np.random.default_rng(seed)
    y = rng.gamma(shape=1.5, scale=math.pi / 4, size=n)
    s = np.sqrt(y)
    s = s * (mean / float(np.mean(s)))
    return s.tolist()


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    n = len(data) if isinstance(data, list) else ""
    print(f"    {filename}  ({n} values)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 62)
    print("RH Height Band Survey — Data Preparation")
    print("=" * 62)

    # Load zeros
    if not os.path.exists("rh_zeros.json"):
        raise FileNotFoundError("rh_zeros.json not found. Run rh_phase5_data_prep.py first.")
    with open("rh_zeros.json") as f:
        zeros = json.load(f)
    print(f"\nLoaded {len(zeros)} Riemann zeros.")

    band_summary = {}

    # Seed in known results
    for band_num, info in KNOWN_RESULTS.items():
        start, end = band_indices(band_num)
        zeros_b = zeros[start:end]
        gaps_b = compute_gaps(zeros_b)
        mean_gap = mean_of(gaps_b)
        band_summary[band_num] = {
            **info,
            "height_range": [round(zeros_b[0], 2), round(zeros_b[-1], 2)],
            "mean_gap": round(mean_gap, 6),
            "n_ratios": 98,
            "status": "COMPLETE — existing result",
            "files": "existing"
        }

    # Generate new bands
    for band_num in NEW_BANDS:
        start, end = band_indices(band_num)
        zeros_b = zeros[start:end]
        gaps_b = compute_gaps(zeros_b)          # 99 gaps
        ratios_b = compute_spacing_ratios(gaps_b)  # 98 ratios
        mean_gap = mean_of(gaps_b)
        mean_ratio = mean_of(ratios_b)

        batch = "A" if band_num in BATCH_A else "B"
        print(f"\nBand {band_num} (Batch {batch}): zeros {start+1}-{end}")
        print(f"  Height range: {zeros_b[0]:.2f} to {zeros_b[-1]:.2f}")
        print(f"  Mean gap: {mean_gap:.6f}  |  Mean ratio (actual): {mean_ratio:.4f}")
        print(f"  Writing files:")

        actual_file = f"rh_hb{band_num}_actual_ratios.json"
        write_json(ratios_b, actual_file)

        gue_files = []
        gue_mean_ratios = []
        for seed in [1, 2, 3]:
            gue_gaps = sample_gue_wigner_gaps(99, mean_gap, seed=seed)
            gue_ratios = compute_spacing_ratios(gue_gaps)
            mr = mean_of(gue_ratios)
            gue_mean_ratios.append(round(mr, 4))
            fname = f"rh_hb{band_num}_gue_seed{seed}_ratios.json"
            write_json(gue_ratios, fname)
            gue_files.append(fname)

        band_summary[band_num] = {
            "zero_indices": f"{start}-{end-1}",
            "height_range": [round(zeros_b[0], 2), round(zeros_b[-1], 2)],
            "mean_gap": round(mean_gap, 6),
            "mean_ratio_actual_precomputed": round(mean_ratio, 4),
            "gue_seed_mean_ratios_precomputed": gue_mean_ratios,
            "n_ratios": len(ratios_b),
            "batch": batch,
            "status": "PENDING — needs CAILculator",
            "actual_file": actual_file,
            "gue_files": gue_files,
            "chavez_symmetry_actual": None,
            "gue_mean_symmetry": None,
            "delta_actual_minus_gue": None
        }

    # Write summary
    summary = {
        "experiment": "RH Height Band Survey",
        "objective": "Track actual - GUE Chavez delta as function of zero height",
        "chavez_parameters": {
            "alpha": 1.0, "dimension_param": 2, "pattern_id": 1, "dimensions": [1,2,3,4,5]
        },
        "known_anchor_points": {
            "band_1":  {"height_approx": "14-237",   "delta": -1.9, "source": "Phase 4"},
            "band_6":  {"height_approx": "811-937",  "delta": +1.5, "source": "Phase 5B"}
        },
        "batch_a_files": [f"rh_hb{n}_{t}" for n in BATCH_A
                          for t in ["actual_ratios.json",
                                    "gue_seed1_ratios.json",
                                    "gue_seed2_ratios.json",
                                    "gue_seed3_ratios.json"]],
        "batch_b_files": [f"rh_hb{n}_{t}" for n in BATCH_B
                          for t in ["actual_ratios.json",
                                    "gue_seed1_ratios.json",
                                    "gue_seed2_ratios.json",
                                    "gue_seed3_ratios.json"]],
        "bands": {str(k): v for k, v in sorted(band_summary.items())}
    }
    with open("rh_height_band_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n  rh_height_band_summary.json")

    # Print CAILculator task lists
    print("\n" + "=" * 62)
    print("CAILCULATOR TASK LIST")
    print("Chavez Transform: alpha=1.0, dim_param=2, pattern_id=1")
    print("=" * 62)

    for batch, bands in [("A", BATCH_A), ("B", BATCH_B)]:
        print(f"\n--- Batch {batch} ({len(bands)*4} runs) ---")
        for n in bands:
            s = band_summary[n]
            print(f"  Band {n} | height {s['height_range'][0]:.0f}-{s['height_range'][1]:.0f}"
                  f" | mean gap {s['mean_gap']:.4f}"
                  f" | actual mean ratio {s['mean_ratio_actual_precomputed']:.4f}")
            print(f"    rh_hb{n}_actual_ratios.json         -> chavez_symmetry")
            print(f"    rh_hb{n}_gue_seed1_ratios.json      -> chavez_symmetry")
            print(f"    rh_hb{n}_gue_seed2_ratios.json      -> chavez_symmetry")
            print(f"    rh_hb{n}_gue_seed3_ratios.json      -> chavez_symmetry")

    print("\n" + "=" * 62)
    print("Anchor points (no CAILculator needed):")
    print("  Band 1: actual=75.0%  GUE=76.9%  delta=-1.9  (Phase 4)")
    print("  Band 6: actual=78.3%  GUE=76.8%  delta=+1.5  (Phase 5B)")
    print("=" * 62)


if __name__ == "__main__":
    main()
