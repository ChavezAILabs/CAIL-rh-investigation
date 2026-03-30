#!/usr/bin/env python3
"""
rh_phase31.py — Riemann Hypothesis Investigation, Phase 31
Chavez AI Labs LLC | Applied Pathological Mathematics

Sedenion Horizon Verification & High-Prime Extension
April 1 Milestone (Sophie Germain's 250th Birthday)

Tracks:
    Track A: Weil ratio decay extended to p_max in {200, 300, 500, 700}
             SSE landscape sweep — asymptote decision gate
    Track B: D6 direction partition — {5,7,11} vs {2,3,13}
    Track C: c1^2 + c3^2 = 1 analytic check
    Track D: Bilateral zero pair count extended to 750 and 1000 zeros

Inherits methodology from rh_phase30.py. All Phase 30 functions
are reproduced here for standalone execution.

ZDTP / CAILculator runs (hinge recurrence p=13,17,19,23) are
handled separately via Claude Desktop MCP server.

Usage:
    python rh_phase31.py

Outputs:
    phase31_results.json          — full numerical results
    phase31_weil_sequence.json    — Weil ratio sequence (GitHub artifact)
    phase31_sse_landscape.csv     — SSE landscape (GitHub artifact)
    phase31_summary.txt           — human-readable summary

Dependencies:
    numpy, scipy, mpmath (strongly recommended for zeros)

Author: Paul Chavez / Chavez AI Labs LLC
Date:   2026-03-27
Phase:  31
"""

import csv
import json
import time
import numpy as np
from scipy.optimize import curve_fit

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TARGET_C1    = 0.11797805192095003   # Sedenion structural angle
TARGET_C3    = 0.9930162029216528    # Weil angle sin component
WEIL_ANGLE   = np.degrees(np.arccos(TARGET_C3))  # ~6.775 degrees
C_CIRCLE     = 1.0 / (2.0 * np.pi)  # ~0.159155 — Circle Method

# Phase 30 baseline (9 points, n_primes 6→36)
P30_N_PRIMES = np.array([6, 9, 10, 12, 16, 20, 25, 31, 36], dtype=float)
P30_RATIOS   = np.array([0.2479, 0.2466, 0.2416, 0.2344, 0.2189,
                          0.2106, 0.1970, 0.1833, 0.1736], dtype=float)

# Phase 31 p_max targets
P31_TARGETS = [200, 300, 500, 700]

# ---------------------------------------------------------------------------
# Riemann zeros — load via mpmath or use Phase 30 fallback
# ---------------------------------------------------------------------------

N_ZEROS = 500

try:
    from mpmath import mp, zetazero
    mp.dps = 25
    print("[INFO] Loading 500 Riemann zeros via mpmath (this takes ~30s)...")
    ZEROS = np.array([float(zetazero(n).imag) for n in range(1, N_ZEROS + 1)])
    print(f"[INFO] Loaded {len(ZEROS)} zeros. First: {ZEROS[0]:.6f}, Last: {ZEROS[-1]:.6f}")
except ImportError:
    print("[WARN] mpmath not found. Using 20-zero fallback. Install mpmath for full results.")
    ZEROS = np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    ])
    N_ZEROS = len(ZEROS)

# ---------------------------------------------------------------------------
# Prime utilities (inherited from Phase 30)
# ---------------------------------------------------------------------------

def sieve(n):
    """Sieve of Eratosthenes — return all primes <= n."""
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return list(np.where(is_prime)[0].astype(int))

ALL_PRIMES = sieve(750)  # enough for all Phase 31 targets

# ---------------------------------------------------------------------------
# Weil ratio computation (inherited from Phase 30)
# ---------------------------------------------------------------------------

def bilateral_trace(primes, zeros=None):
    """
    Tr[B_K] at each zero: sum_{p in primes} log(p) * cos(gamma * log p)
    """
    if zeros is None:
        zeros = ZEROS[:100]
    primes = np.array(primes, dtype=float)
    traces = np.array([
        float(np.sum(np.log(primes) * np.cos(gamma * np.log(primes))))
        for gamma in zeros
    ])
    return traces

def weil_rhs(primes):
    """
    Prime-weight Weil RHS: -sum_{p} log(p) * p^(-0.5)
    Matches Phase 30 formula exactly (verified against phase30_results.json:
    p13 weil_rhs=-4.014042, p23 weil_rhs=-6.030494).
    """
    primes = np.array(primes, dtype=float)
    return float(-np.sum(np.log(primes) * primes**(-0.5)))

def compute_weil_ratio(primes, n_zeros_eval=100):
    """Compute the Weil ratio for a given prime set."""
    zeros_sub = ZEROS[:min(n_zeros_eval, N_ZEROS)]
    traces    = bilateral_trace(primes, zeros_sub)
    mean_tr   = float(np.mean(traces))
    w_rhs     = weil_rhs(primes)
    ratio     = mean_tr / w_rhs if abs(w_rhs) > 1e-12 else float('nan')
    return ratio, mean_tr, w_rhs

# ---------------------------------------------------------------------------
# Track A — Weil ratio extension to high p_max + SSE landscape
# ---------------------------------------------------------------------------

def power_law_fixed_c(c_val):
    def f(x, a, b):
        return a * x**(-b) + c_val
    return f

def power_law_free(x, a, b, c):
    return a * x**(-b) + c

def compute_sse_r2(y_true, y_pred):
    sse    = float(np.sum((y_true - y_pred)**2))
    ss_tot = float(np.sum((y_true - np.mean(y_true))**2))
    r2     = 1.0 - sse / ss_tot if ss_tot > 1e-15 else float('nan')
    return sse, r2

def fit_fixed_c(n_arr, ratio_arr, c_val):
    """Fit y = a*x^-b + c_val with grid search over p0 to avoid local minima."""
    best = {"sse": np.inf, "r2": -np.inf, "a": None, "b": None}
    for a0 in [0.1, 0.3, 0.5, 1.0]:
        for b0 in [0.2, 0.4, 0.5, 0.7, 1.0]:
            try:
                popt, _ = curve_fit(
                    power_law_fixed_c(c_val), n_arr, ratio_arr,
                    p0=[a0, b0],
                    bounds=([0.001, 0.05], [10.0, 3.0]),
                    maxfev=20000
                )
                y_pred = power_law_fixed_c(c_val)(n_arr, *popt)
                sse, r2 = compute_sse_r2(ratio_arr, y_pred)
                if sse < best["sse"]:
                    best = {"sse": sse, "r2": r2, "a": float(popt[0]), "b": float(popt[1])}
            except Exception:
                pass
    return best

def sse_landscape(n_arr, ratio_arr, c_min=0.05, c_max=0.22, n_points=35):
    """
    SSE landscape sweep across fixed-c values.
    Wider range than Gemini's 0.10-0.20 — must include sub-0.10 behavior.
    Returns list of {c, sse, r2, b} dicts and the minimum-SSE entry.
    """
    landscape = []
    c_range = np.linspace(c_min, c_max, n_points)
    for c_test in c_range:
        result = fit_fixed_c(n_arr, ratio_arr, float(c_test))
        if result["a"] is not None:
            landscape.append({
                "c":   round(float(c_test), 5),
                "sse": result["sse"],
                "r2":  result["r2"],
                "b":   result["b"],
                "a":   result["a"],
            })

    # Find minimum SSE
    if landscape:
        min_entry = min(landscape, key=lambda x: x["sse"])
        # Check if landscape is still monotone (no minimum) or has a true minimum
        sses = [e["sse"] for e in landscape]
        has_minimum = any(sses[i] < sses[i-1] and sses[i] < sses[i+1]
                          for i in range(1, len(sses)-1))
        return landscape, min_entry, has_minimum
    return landscape, None, False

def run_track_A():
    """
    Extend Weil ratio sequence to p_max in P31_TARGETS.
    Combine with Phase 30 baseline and run SSE landscape at each stage.
    """
    print("\n" + "="*65)
    print("Track A: Weil Ratio Extension to High p_max")
    print("="*65)

    # Build cumulative dataset starting from Phase 30 baseline
    all_n_primes = list(P30_N_PRIMES.astype(int))
    all_ratios   = list(P30_RATIOS)

    # Compute Phase 30 p_max cutoffs for reference
    p30_cutoffs = [13, 23, 29, 37, 53, 71, 97, 127, 151]

    extension_results = {}

    for p_max in P31_TARGETS:
        t0     = time.time()
        primes = [p for p in ALL_PRIMES if p <= p_max]
        ratio, mean_tr, w_rhs = compute_weil_ratio(primes)
        elapsed = time.time() - t0

        n_p = len(primes)
        all_n_primes.append(n_p)
        all_ratios.append(ratio)

        print(f"  p_max={p_max:4d} | N_primes={n_p:4d} | ratio={ratio:.6f} | "
              f"Δ from 1/4={ratio-0.25:+.5f} | {elapsed:.1f}s")

        extension_results[f"p{p_max}"] = {
            "p_max": p_max, "n_primes": n_p,
            "ratio": ratio, "mean_tr": mean_tr,
            "weil_rhs": w_rhs, "diff_from_quarter": ratio - 0.25,
            "elapsed_s": elapsed,
        }

    # Full combined array
    n_arr     = np.array(all_n_primes, dtype=float)
    ratio_arr = np.array(all_ratios, dtype=float)

    print(f"\n  Full sequence ({len(n_arr)} points): "
          f"{[f'{r:.4f}' for r in ratio_arr]}")
    monotone = all(ratio_arr[i] > ratio_arr[i+1] for i in range(len(ratio_arr)-1))
    print(f"  Monotone decreasing: {monotone}")

    # SSE landscape on full dataset
    print("\n  Running SSE landscape sweep (35 points, c in [0.05, 0.22])...")
    landscape, min_entry, has_minimum = sse_landscape(n_arr, ratio_arr)

    print(f"\n  {'c':>10}  {'SSE':>14}  {'R²':>10}  {'b':>8}")
    print("  " + "-"*48)
    for entry in landscape:
        marker = ""
        if abs(entry["c"] - TARGET_C1) < 0.003:
            marker = " <-- c1"
        elif abs(entry["c"] - C_CIRCLE) < 0.003:
            marker = " <-- 1/2π"
        elif min_entry and abs(entry["c"] - min_entry["c"]) < 0.001:
            marker = " <-- MIN"
        print(f"  {entry['c']:>10.5f}  {entry['sse']:>14.10f}  "
              f"{entry['r2']:>10.6f}  {entry['b']:>8.4f}{marker}")

    # Fixed-c runs at the three candidate constants
    print("\n  Fixed-c Comparison:")
    run_c1  = fit_fixed_c(n_arr, ratio_arr, TARGET_C1)
    run_pi  = fit_fixed_c(n_arr, ratio_arr, C_CIRCLE)
    run_140 = fit_fixed_c(n_arr, ratio_arr, 0.140)
    print(f"    Run A (c=c1=0.11798):  SSE={run_c1['sse']:.8f}  R²={run_c1['r2']:.6f}  b={run_c1['b']:.4f}")
    print(f"    Run B (c=1/2π=0.15915): SSE={run_pi['sse']:.8f}  R²={run_pi['r2']:.6f}  b={run_pi['b']:.4f}")
    print(f"    Run C (c=0.140):         SSE={run_140['sse']:.8f}  R²={run_140['r2']:.6f}  b={run_140['b']:.4f}")

    winner = min(
        [("Sedenion c1", run_c1["sse"]),
         ("Circle Method 1/2π", run_pi["sse"]),
         ("c=0.140", run_140["sse"])],
        key=lambda x: x[1]
    )[0]
    sse_ratio_B_A = run_pi["sse"] / run_c1["sse"] if run_c1["sse"] > 0 else float('nan')

    # Decision gate
    print("\n  DECISION GATE:")
    if has_minimum:
        if min_entry:
            print(f"    *** SSE MINIMUM DETECTED at c = {min_entry['c']:.5f} ***")
            if abs(min_entry["c"] - TARGET_C1) < 0.01:
                print("    TRAJECTORY A: Minimum near c1. Sedenion Horizon Conjecture -> STRONG.")
            elif abs(min_entry["c"] - 0.140) < 0.01:
                print("    TRAJECTORY B: Minimum near 0.140. Square-root law hypothesis gains traction.")
            else:
                print(f"    TRAJECTORY UNKNOWN: Minimum at {min_entry['c']:.5f} — new constant candidate.")
    else:
        print(f"    SSE landscape still MONOTONE through p_max={max(P31_TARGETS)}.")
        print("    TRAJECTORY C: Dataset underdetermined at this scale. Phase 32 needed.")
        print(f"    Best fixed-c fit: {winner} (SSE ratio B/A = {sse_ratio_B_A:.2f}×)")

    return {
        "extension": extension_results,
        "n_primes_full": all_n_primes,
        "ratios_full": all_ratios,
        "monotone_decreasing": bool(monotone),
        "sse_landscape": landscape,
        "landscape_has_minimum": has_minimum,
        "landscape_minimum": min_entry,
        "run_A_c1":  {**run_c1,  "c_fixed": TARGET_C1, "label": "Sedenion c1"},
        "run_B_pi":  {**run_pi,  "c_fixed": C_CIRCLE,  "label": "Circle Method 1/2pi"},
        "run_C_140": {**run_140, "c_fixed": 0.140,     "label": "sqrt-law intercept"},
        "winner_fixed_c": winner,
        "sse_ratio_B_over_A": sse_ratio_B_A,
    }

# ---------------------------------------------------------------------------
# Track B — D6 direction partition check
# ---------------------------------------------------------------------------

def run_track_B():
    """
    Map prime bilateral direction assignments within the D6 cone.
    The 45 bilateral P∪Q directions = D6 minus 15 both-negative roots (AIEX-053).
    Check whether {5,7,11} and {2,3,13} fall in geometrically distinct sub-regions.

    Approximation: use log(p) mod (2π) as a proxy for the bilateral
    direction angle in the 8D projection. Full Gram matrix analysis
    requires Lean 4 / Phase 19 data.
    """
    print("\n" + "="*65)
    print("Track B: D6 Direction Partition — {5,7,11} vs {2,3,13}")
    print("="*65)

    test_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    anchor_set  = {5, 7, 11}
    decay_set   = {2, 3, 13}

    results = {}
    print(f"\n  {'Prime':>6}  {'log(p)':>10}  {'angle_8D (deg)':>16}  {'D6_sector':>12}  {'Set':>8}")
    print("  " + "-"*58)

    for p in test_primes:
        log_p   = np.log(p)
        # Bilateral direction: project onto 8D via log(p) periodicity
        # In Phase 19, bilateral directions correspond to pairs (εᵢeᵢ + εⱼeⱼ)
        # The angle in the D6 cone ≈ arctan(log(p) mod π / π) * (180/π)
        angle_proxy = (log_p % np.pi) / np.pi * 180.0
        # D6 sector: divide the 45 directions into 3 bands
        if angle_proxy < 60:
            sector = "low"
        elif angle_proxy < 120:
            sector = "mid"
        else:
            sector = "high"

        prime_set = "anchor" if p in anchor_set else ("decay" if p in decay_set else "extended")
        results[p] = {"log_p": log_p, "angle_proxy_deg": angle_proxy,
                      "d6_sector": sector, "set": prime_set}
        print(f"  {p:>6}  {log_p:>10.6f}  {angle_proxy:>16.4f}  {sector:>12}  {prime_set:>8}")

    # Check segregation
    anchor_sectors = {results[p]["d6_sector"] for p in anchor_set}
    decay_sectors  = {results[p]["d6_sector"] for p in decay_set}
    overlap        = anchor_sectors & decay_sectors

    print(f"\n  Anchor {{5,7,11}} sectors: {anchor_sectors}")
    print(f"  Decay  {{2,3,13}} sectors:  {decay_sectors}")
    print(f"  Sector overlap:           {overlap if overlap else 'None'}")

    segregated = len(overlap) == 0
    print(f"\n  D6 SEGREGATION: {'CONFIRMED (no sector overlap)' if segregated else 'NOT confirmed (sectors overlap)'}")
    print("  NOTE: This is a proxy analysis. Full Gram matrix classification")
    print("  from Phase 19 bilateral 8D data required for definitive result.")

    return {
        "prime_directions": {str(k): v for k, v in results.items()},
        "anchor_sectors": list(anchor_sectors),
        "decay_sectors": list(decay_sectors),
        "sector_overlap": list(overlap),
        "proxy_segregation_confirmed": segregated,
        "note": "Proxy via log(p) mod pi. Phase 19 Gram matrix required for definitive classification."
    }

# ---------------------------------------------------------------------------
# Track C — c1^2 + c3^2 = 1 analytic check
# ---------------------------------------------------------------------------

def run_track_C():
    """
    Verify c1^2 + c3^2 = 1 and assess whether theta_W has an analytic
    expression independent of numerical fit.
    """
    print("\n" + "="*65)
    print("Track C: c1² + c3² = 1 Analytic Check")
    print("="*65)

    # Numerical verification
    norm_sq   = TARGET_C1**2 + TARGET_C3**2
    theta_W   = np.arccos(TARGET_C3)          # Weil angle in radians
    theta_deg = np.degrees(theta_W)
    c1_from_angle = np.sin(theta_W)
    c3_from_angle = np.cos(theta_W)

    print(f"\n  c1              = {TARGET_C1:.16f}")
    print(f"  c3              = {TARGET_C3:.16f}")
    print(f"  c1² + c3²       = {norm_sq:.16f}  (target: 1.0)")
    print(f"  |norm_sq - 1|   = {abs(norm_sq - 1.0):.2e}")
    print(f"  θ_W             = {theta_deg:.10f} degrees")
    print(f"  sin(θ_W)        = {c1_from_angle:.16f}  (= c1? {abs(c1_from_angle - TARGET_C1) < 1e-14})")
    print(f"  cos(θ_W)        = {c3_from_angle:.16f}  (= c3? {abs(c3_from_angle - TARGET_C3) < 1e-14})")

    # Check: is theta_W a rational multiple of pi?
    ratio_to_pi   = theta_W / np.pi
    ratio_to_pi_2 = theta_W / (np.pi / 2)
    print(f"\n  θ_W / π         = {ratio_to_pi:.10f}  (rational? "
          f"{'possibly' if abs(ratio_to_pi - round(ratio_to_pi*100)/100) < 0.001 else 'no'})")
    print(f"  θ_W / (π/2)     = {ratio_to_pi_2:.10f}")

    # Check: relation to known constants
    candidates = {
        "log(2)/10":     np.log(2) / 10,
        "1/(4π)":        1.0 / (4 * np.pi),
        "arctan(1/8)":   np.arctan(1.0/8),
        "π/46":          np.pi / 46,
        "log(3)/12":     np.log(3) / 12,
        "1/zetazero_1":  1.0 / 14.134725,  # 1/γ₁
    }
    print("\n  Proximity to known constants (|θ_W - candidate| < 0.001 rad):")
    any_match = False
    for name, val in candidates.items():
        diff = abs(theta_W - val)
        if diff < 0.01:
            print(f"    CLOSE: {name} = {val:.8f}  (diff={diff:.2e})")
            any_match = True
    if not any_match:
        print("    None within 0.01 rad. θ_W does not match common analytic constants.")

    # Status
    is_unit = abs(norm_sq - 1.0) < 1e-14
    print(f"\n  STATUS: c1² + c3² = 1 is {'NUMERICALLY EXACT' if is_unit else 'NOT exact'} "
          f"to double precision.")
    print("  THEOREM CANDIDATE: Identity holds by definition if (c1, c3) = (sin θ_W, cos θ_W).")
    print("  OPEN QUESTION: Is θ_W analytically defined by the Weil explicit formula,")
    print("  or is it only known numerically from the 5D bilateral projection?")

    return {
        "c1": TARGET_C1, "c3": TARGET_C3,
        "c1_sq_plus_c3_sq": norm_sq,
        "deviation_from_unity": abs(norm_sq - 1.0),
        "numerically_exact": is_unit,
        "theta_W_radians": float(theta_W),
        "theta_W_degrees": float(theta_deg),
        "theta_W_over_pi": float(ratio_to_pi),
        "known_constant_match": any_match,
        "theorem_status": "holds by trig identity if theta_W is the true Weil angle",
        "open_question": "Does theta_W have an analytic expression in the Weil explicit formula?"
    }

# ---------------------------------------------------------------------------
# Track D — Bilateral zero pair count extension
# ---------------------------------------------------------------------------

def bilateral_zero_pairs(n_zeros, primes=None, threshold=1e-2):
    """
    Count bilateral zero pairs at n_zeros.
    A 'bilateral pair' is a pair of zeros (γᵢ, γⱼ) where the
    bilateral trace T(γᵢ) and T(γⱼ) satisfy |T(γᵢ) + T(γⱼ)| < threshold
    (approximate bilateral cancellation).

    Phase 29 baseline: 6,290 pairs at 500 zeros.
    """
    if primes is None:
        # Use Canonical Six prime set: {5, 7, 11} anchor + {2, 3, 13}
        primes = [2, 3, 5, 7, 11, 13]

    zeros_sub = ZEROS[:min(n_zeros, N_ZEROS)]
    if len(zeros_sub) < n_zeros:
        return None, f"Only {len(zeros_sub)} zeros available (requested {n_zeros})"

    traces = bilateral_trace(primes, zeros_sub)
    count  = 0
    for i in range(len(traces)):
        for j in range(i+1, len(traces)):
            if abs(traces[i] + traces[j]) < threshold:
                count += 1
    return count, None

def run_track_D():
    """
    Extend bilateral zero pair count from Phase 29 baseline (6,290 at N=500).
    Test at N=500 (baseline verify), N=750, N=1000.
    Fit growth model: pairs ~ N^alpha.
    """
    print("\n" + "="*65)
    print("Track D: Bilateral Zero Pair Count Extension")
    print("="*65)

    baseline = {"n_zeros": 500, "pairs": 6290}  # Phase 29 confirmed
    test_sizes = [500, 750, 1000]

    pair_counts = []
    results = {}
    print(f"\n  {'N_zeros':>8}  {'Pairs':>10}  {'Pairs/N²':>12}  {'Status':>12}")
    print("  " + "-"*48)

    for n_z in test_sizes:
        if n_z > N_ZEROS:
            print(f"  {n_z:>8}  {'N/A':>10}  {'N/A':>12}  {'need mpmath':>12}")
            results[f"N{n_z}"] = {"n_zeros": n_z, "pairs": None,
                                   "note": "Requires mpmath with sufficient zeros loaded"}
            continue
        t0    = time.time()
        pairs, err = bilateral_zero_pairs(n_z)
        elapsed = time.time() - t0
        if err:
            print(f"  {n_z:>8}  ERROR: {err}")
            continue
        density = pairs / (n_z * (n_z - 1) / 2)
        pair_counts.append((n_z, pairs))
        results[f"N{n_z}"] = {"n_zeros": n_z, "pairs": pairs,
                               "density": density, "elapsed_s": elapsed}
        baseline_match = "(baseline ✓)" if n_z == 500 and abs(pairs - 6290) / 6290 < 0.05 else ""
        print(f"  {n_z:>8}  {pairs:>10}  {density:>12.6f}  {baseline_match:>12}  [{elapsed:.1f}s]")

    # Fit growth model pairs ~ N^alpha
    if len(pair_counts) >= 2:
        ns     = np.array([x[0] for x in pair_counts], dtype=float)
        counts = np.array([x[1] for x in pair_counts], dtype=float)
        try:
            log_n = np.log(ns)
            log_c = np.log(counts)
            coeffs = np.polyfit(log_n, log_c, 1)
            alpha  = coeffs[0]
            print(f"\n  Growth model fit: pairs ~ N^{alpha:.4f}")
            print(f"  Phase 29 finding: superlinear growth (alpha > 1.0)")
            print(f"  Phase 31 result:  alpha = {alpha:.4f} "
                  f"({'superlinear ✓' if alpha > 1.0 else 'linear or sublinear — check'})")
            results["growth_alpha"] = float(alpha)
        except Exception as e:
            print(f"  Growth fit failed: {e}")

    return results

# ---------------------------------------------------------------------------
# Artifact save
# ---------------------------------------------------------------------------

def save_artifacts(track_a, track_b, track_c, track_d):
    """Save all Phase 31 artifacts for GitHub and CAILculator ingestion."""

    def json_safe(obj):
        """Recursively convert numpy types to native Python for JSON serialization."""
        if isinstance(obj, dict):
            return {k: json_safe(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [json_safe(v) for v in obj]
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        return obj

    # Full results JSON
    output = {
        "metadata": {
            "phase": 31,
            "date": "2026-03-27",
            "script": "rh_phase31.py",
            "target_c1": TARGET_C1,
            "target_c3": TARGET_C3,
            "weil_angle_degrees": float(WEIL_ANGLE),
            "zeros_used": N_ZEROS,
            "p31_targets": P31_TARGETS,
        },
        "track_A_weil_extension":   track_a,
        "track_B_d6_partition":     track_b,
        "track_C_analytic_check":   track_c,
        "track_D_zero_pair_count":  track_d,
    }
    with open("phase31_results.json", "w") as f:
        json.dump(json_safe(output), f, indent=2)
    print("\n[OK] Saved phase31_results.json")

    # Weil sequence JSON (GitHub artifact)
    weil_artifact = {
        "phase": 31,
        "n_primes": track_a["n_primes_full"],
        "ratios":   track_a["ratios_full"],
        "p30_baseline_n":      list(P30_N_PRIMES.astype(int)),
        "p30_baseline_ratios": list(P30_RATIOS),
        "p31_extension": track_a["extension"],
    }
    with open("phase31_weil_sequence.json", "w") as f:
        json.dump(json_safe(weil_artifact), f, indent=2)
    print("[OK] Saved phase31_weil_sequence.json")

    # SSE landscape CSV (GitHub artifact)
    landscape = track_a.get("sse_landscape", [])
    if landscape:
        with open("phase31_sse_landscape.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["c", "sse", "r2", "b", "a"])
            writer.writeheader()
            writer.writerows(landscape)
        print("[OK] Saved phase31_sse_landscape.csv")

    # Human-readable summary
    with open("phase31_summary.txt", "w") as f:
        f.write("Phase 31 Summary — RH Investigation\n")
        f.write("Chavez AI Labs LLC\n")
        f.write("="*60 + "\n\n")
        f.write(f"Zeros used: {N_ZEROS}\n")
        f.write(f"p_max targets: {P31_TARGETS}\n\n")

        f.write("Track A — Weil Ratio Extension:\n")
        for p_max, data in track_a["extension"].items():
            f.write(f"  {p_max}: ratio={data['ratio']:.6f}  "
                    f"N_primes={data['n_primes']}\n")
        f.write(f"  Monotone decreasing: {track_a['monotone_decreasing']}\n")
        f.write(f"  SSE minimum detected: {track_a['landscape_has_minimum']}\n")
        if track_a['landscape_minimum']:
            m = track_a['landscape_minimum']
            f.write(f"  Minimum at c={m['c']:.5f}  SSE={m['sse']:.8f}\n")
        f.write(f"  Best fixed-c: {track_a['winner_fixed_c']} "
                f"(SSE ratio B/A = {track_a['sse_ratio_B_over_A']:.3f}x)\n")
        f.write(f"  Run A (c1):   b={track_a['run_A_c1']['b']:.4f}  "
                f"SSE={track_a['run_A_c1']['sse']:.8f}\n")
        f.write(f"  Run B (1/2π): b={track_a['run_B_pi']['b']:.4f}  "
                f"SSE={track_a['run_B_pi']['sse']:.8f}\n")
        f.write(f"  Run C (0.140):b={track_a['run_C_140']['b']:.4f}  "
                f"SSE={track_a['run_C_140']['sse']:.8f}\n\n")

        f.write("Track B — D6 Partition:\n")
        f.write(f"  Proxy segregation: {track_b['proxy_segregation_confirmed']}\n")
        f.write(f"  {track_b['note']}\n\n")

        f.write("Track C — c1² + c3² = 1:\n")
        f.write(f"  Numerically exact: {track_c['numerically_exact']}\n")
        f.write(f"  Deviation: {track_c['deviation_from_unity']:.2e}\n")
        f.write(f"  θ_W = {track_c['theta_W_degrees']:.8f} degrees\n")
        f.write(f"  Known constant match: {track_c['known_constant_match']}\n\n")

        f.write("ZDTP Hinge Recurrence (p=13,17,19,23): via Claude Desktop\n")
        f.write("  See phase31_zdtp_hinge.json after MCP runs.\n")

    print("[OK] Saved phase31_summary.txt")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 65)
    print("RH Investigation — Phase 31")
    print("Chavez AI Labs LLC | Applied Pathological Mathematics")
    print("Sedenion Horizon Verification & High-Prime Extension")
    print("=" * 65)
    print(f"Constants: c1={TARGET_C1}  c3={TARGET_C3}")
    print(f"Weil angle: {WEIL_ANGLE:.6f}°  |  c1²+c3²={TARGET_C1**2+TARGET_C3**2:.16f}")

    track_a = run_track_A()
    track_b = run_track_B()
    track_c = run_track_C()
    track_d = run_track_D()

    save_artifacts(track_a, track_b, track_c, track_d)

    print("\n" + "="*65)
    print("Phase 31 complete.")
    print("Next: Claude Desktop ZDTP runs for p=13,17,19,23 hinge check.")
    print("="*65)

if __name__ == "__main__":
    main()
