"""
RH Phase 5 — Data Preparation Script
=====================================
Regenerates missing data files and produces all spacing-ratio sequences
needed to complete Phase 5 in Claude Desktop + CAILculator MCP.

What this script does:
  1. Regenerates rh_zeros.json and rh_gaps.json via mpmath if missing
  2. Part A: generates GUE Wigner surmise seed 3 spacing ratios at n=499
  3. Part B: computes actual zeros 500-599 spacing ratios (for mean ratio)
             generates Poisson controls (seeds 1-3) for zeros 500-599
             generates GUE controls (seeds 1-3) for zeros 500-599
  4. Writes phase5_data_prep_summary.json with all parameters for the handoff

Usage:
  python rh_phase5_data_prep.py

Requirements:
  pip install mpmath numpy
"""

import json
import math
import os
import numpy as np

try:
    import mpmath
    HAS_MPMATH = True
except ImportError:
    HAS_MPMATH = False


# ---------------------------------------------------------------------------
# Data loading / generation
# ---------------------------------------------------------------------------

def load_or_generate_zeros(n=1000):
    """Load rh_zeros.json if present; otherwise regenerate via mpmath."""
    if os.path.exists("rh_zeros.json"):
        print("  Loading existing rh_zeros.json")
        with open("rh_zeros.json") as f:
            return json.load(f)

    if not HAS_MPMATH:
        raise RuntimeError(
            "rh_zeros.json is missing and mpmath is not installed.\n"
            "Run: pip install mpmath"
        )

    print(f"  Regenerating rh_zeros.json via mpmath (mp.dps=25, n={n})...")
    mpmath.mp.dps = 25
    zeros = [float(mpmath.zetazero(i + 1).imag) for i in range(n)]
    write_json(zeros, "rh_zeros.json")
    return zeros


def compute_gaps(sequence):
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def compute_spacing_ratios(gaps):
    """r_n = min(g_n, g_{n+1}) / max(g_n, g_{n+1}) for consecutive gap pairs."""
    return [
        min(gaps[i], gaps[i + 1]) / max(gaps[i], gaps[i + 1])
        for i in range(len(gaps) - 1)
    ]


# ---------------------------------------------------------------------------
# Synthetic gap generators
# ---------------------------------------------------------------------------

def sample_poisson_gaps(n, mean, seed):
    """Exponential(mean) gaps — Poisson process baseline."""
    rng = np.random.default_rng(seed)
    return rng.exponential(scale=mean, size=n).tolist()


def sample_gue_wigner_gaps(n, mean, seed):
    """
    GUE Wigner surmise: P(s) = (32/pi^2) * s^2 * exp(-4s^2/pi)
    Equivalent to: y = s^2 ~ Gamma(shape=1.5, scale=pi/4), s = sqrt(y)
    Unscaled mean = 1; scale samples so sample mean matches target.
    """
    rng = np.random.default_rng(seed)
    y = rng.gamma(shape=1.5, scale=math.pi / 4, size=n)
    s = np.sqrt(y)
    s = s * (mean / float(np.mean(s)))
    return s.tolist()


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    n = len(data) if isinstance(data, list) else ""
    print(f"  Written: {filename}  ({n} values)")


def mean_of(values):
    return sum(values) / len(values)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("RH Phase 5 — Data Preparation")
    print("=" * 60)

    # --- Step 1: Load / regenerate zeros and gaps ---
    print("\n[1] Zero and gap data")
    zeros = load_or_generate_zeros(1000)
    gaps_all = compute_gaps(zeros)

    if not os.path.exists("rh_gaps.json"):
        write_json(gaps_all, "rh_gaps.json")
    else:
        print("  rh_gaps.json already present")

    # --- Step 2: Part A — GUE seed 3 at n=499 ---
    print("\n[2] Part A — GUE Wigner surmise seed 3 at n=499")
    gaps_499 = gaps_all[:499]
    mean_gap_499 = mean_of(gaps_499)
    print(f"  Actual mean gap (first 499): {mean_gap_499:.6f}")

    gue_s3_gaps = sample_gue_wigner_gaps(499, mean_gap_499, seed=3)
    gue_s3_ratios = compute_spacing_ratios(gue_s3_gaps)
    mean_ratio_gue_s3 = mean_of(gue_s3_ratios)
    write_json(gue_s3_ratios, "phase5a_gue_seed3_ratios.json")
    print(f"  GUE seed 3 mean spacing ratio: {mean_ratio_gue_s3:.4f}")
    print(f"  n ratios: {len(gue_s3_ratios)}")

    # --- Step 3: Part B — zeros 500-599 (0-indexed: 499-598) ---
    print("\n[3] Part B — Zeros 500-599 (indices 499-598)")
    zeros_b = zeros[499:599]   # 100 zeros
    gaps_b = compute_gaps(zeros_b)  # 99 gaps
    ratios_b = compute_spacing_ratios(gaps_b)  # 98 ratios
    mean_gap_b = mean_of(gaps_b)
    mean_ratio_b = mean_of(ratios_b)

    print(f"  Zero range: {zeros_b[0]:.4f} to {zeros_b[-1]:.4f}")
    print(f"  Mean gap (zeros 500-599): {mean_gap_b:.6f}")
    print(f"  Actual mean spacing ratio: {mean_ratio_b:.4f}")
    write_json(ratios_b, "phase5b_actual_ratios.json")

    # --- Step 4: Part B Poisson controls ---
    print("\n[4] Part B — Poisson controls (seeds 1-3)")
    poisson_summary = []
    for seed in [1, 2, 3]:
        p_gaps = sample_poisson_gaps(99, mean_gap_b, seed=seed)
        p_ratios = compute_spacing_ratios(p_gaps)
        mr = mean_of(p_ratios)
        fname = f"phase5b_poisson_seed{seed}_ratios.json"
        write_json(p_ratios, fname)
        print(f"  Seed {seed} mean ratio: {mr:.4f}")
        poisson_summary.append({"seed": seed, "mean_ratio": round(mr, 4), "file": fname})

    # --- Step 5: Part B GUE controls ---
    print("\n[5] Part B — GUE Wigner surmise controls (seeds 1-3)")
    gue_summary = []
    for seed in [1, 2, 3]:
        g_gaps = sample_gue_wigner_gaps(99, mean_gap_b, seed=seed)
        g_ratios = compute_spacing_ratios(g_gaps)
        mr = mean_of(g_ratios)
        fname = f"phase5b_gue_seed{seed}_ratios.json"
        write_json(g_ratios, fname)
        print(f"  Seed {seed} mean ratio: {mr:.4f}")
        gue_summary.append({"seed": seed, "mean_ratio": round(mr, 4), "file": fname})

    # --- Step 6: Write prep summary ---
    summary = {
        "script": "rh_phase5_data_prep.py",
        "purpose": "All missing sequences for RH Phase 5 completion — ready for CAILculator MCP",
        "chavez_parameters": {
            "alpha": 1.0,
            "dimension_param": 2,
            "pattern_id": 1,
            "dimensions": [1, 2, 3, 4, 5]
        },
        "part_a": {
            "description": "GUE seed 3 at n=499 — completes Part A (seeds 1 and 2 already done)",
            "mean_gap_n499": round(mean_gap_499, 6),
            "gue_seed3": {
                "file": "phase5a_gue_seed3_ratios.json",
                "n_ratios": len(gue_s3_ratios),
                "mean_ratio_precomputed": round(mean_ratio_gue_s3, 4)
            },
            "previously_completed": {
                "actual_zeros_n499": {"chavez_symmetry": 75.7, "mean_ratio": 0.616},
                "actual_zeros_n999": {"chavez_symmetry": 76.3, "mean_ratio": 0.617},
                "poisson_seed1": {"chavez_symmetry": 68.8},
                "poisson_seed2": {"chavez_symmetry": 69.4},
                "poisson_seed3": {"chavez_symmetry": 68.6},
                "gue_seed1":    {"chavez_symmetry": 76.3},
                "gue_seed2":    {"chavez_symmetry": 75.5}
            }
        },
        "part_b": {
            "description": "Higher zeros 500-599 controls — completes Part B",
            "zero_index_range": "499-598 (0-indexed)",
            "zero_range": [round(zeros_b[0], 4), round(zeros_b[-1], 4)],
            "mean_gap": round(mean_gap_b, 6),
            "actual_zeros_500_599": {
                "file": "phase5b_actual_ratios.json",
                "n_ratios": len(ratios_b),
                "mean_ratio_precomputed": round(mean_ratio_b, 4),
                "chavez_symmetry_previously_recorded": 78.3
            },
            "poisson_controls": poisson_summary,
            "gue_controls": gue_summary
        }
    }
    write_json(summary, "phase5_data_prep_summary.json")

    # --- Step 7: Print CAILculator task list ---
    print("\n" + "=" * 60)
    print("READY FOR CAILCULATOR MCP")
    print("=" * 60)
    print("\nRun Chavez Transform on these files (alpha=1.0, dim_param=2, pattern=1):")
    print("\n  Part A (1 file):")
    print("    phase5a_gue_seed3_ratios.json    -> record chavez_symmetry")
    print("\n  Part B (7 files):")
    print("    phase5b_actual_ratios.json        -> record chavez_symmetry (confirm 78.3%)")
    print("    phase5b_poisson_seed1_ratios.json -> record chavez_symmetry")
    print("    phase5b_poisson_seed2_ratios.json -> record chavez_symmetry")
    print("    phase5b_poisson_seed3_ratios.json -> record chavez_symmetry")
    print("    phase5b_gue_seed1_ratios.json     -> record chavez_symmetry")
    print("    phase5b_gue_seed2_ratios.json     -> record chavez_symmetry")
    print("    phase5b_gue_seed3_ratios.json     -> record chavez_symmetry")
    print("\nAll mean ratios are precomputed in phase5_data_prep_summary.json.")
    print("=" * 60)


if __name__ == "__main__":
    main()
