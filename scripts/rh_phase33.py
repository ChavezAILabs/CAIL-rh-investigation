#!/usr/bin/env python3
"""
rh_phase33.py — Riemann Hypothesis Investigation, Phase 33
Chavez AI Labs LLC | Applied Pathological Mathematics

Weil Ratio Double-Dependence Characterization

Tracks:
    V1: Formula verification suite (run before any computation)
    N1: N_zeros decay law for three fixed prime sets
    N2: (N_primes, N_zeros) ratio surface + c1 level curve
    C1: Exact c1 crossing p_max as function of N_zeros

Correct formula (Phase 30, Phase 32 verified — do not modify):
    Tr_BK(t_n) = sum_p (log p / sqrt(p)) * cos(t_n * log p)
    Weil_RHS   = -sum_p log(p) / sqrt(p)
    ratio      = mean(Tr_BK over N_zeros) / Weil_RHS

Usage:
    python rh_phase33.py

Outputs:
    phase33_formula_verification.json
    phase33_nzeros_dependence.json
    phase33_ratio_surface.json
    phase33_c1_crossing.json

Dependencies: numpy, scipy (zeros loaded from rh_zeros.json)

Author: Paul Chavez / Chavez AI Labs LLC
Date:   2026-03-27
Phase:  33
"""

import json
import math
import os
import sys
import time
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# Constants (machine-verified — do not change)
# ---------------------------------------------------------------------------

C1         = 0.11797805192095003   # sin(theta_W)
C3         = 0.99301620292165280   # cos(theta_W)
THETA_W    = math.degrees(math.acos(C3))  # 6.775425 deg
C_CIRCLE   = 1.0 / (2.0 * math.pi)       # 0.159155

# Verified baselines (Phase 32)
BASELINES = [
    {"N_zeros": 100, "N_primes":  6, "p_max":   13, "ratio": 0.247931, "Weil_RHS": -4.014042},
    {"N_zeros": 500, "N_primes":  6, "p_max":   13, "ratio": 0.173349, "Weil_RHS": -4.014042},
    {"N_zeros": 500, "N_primes": 36, "p_max":  151, "ratio": 0.136356, "Weil_RHS": None},
    {"N_zeros": 500, "N_primes": 62, "p_max":  300, "ratio": 0.118099, "Weil_RHS": None},
    {"N_zeros": 500, "N_primes":168, "p_max": 1000, "ratio": 0.082508, "Weil_RHS": None},
]
TOLERANCE = 5e-5   # PASS threshold for verification

# ---------------------------------------------------------------------------
# Load Riemann zeros (up to 1000)
# ---------------------------------------------------------------------------

def load_zeros(n=1000):
    candidates = ["rh_zeros.json", "rh_zeros_10k.json"]
    for fname in candidates:
        if os.path.exists(fname):
            with open(fname) as f:
                data = json.load(f)
            avail = len(data)
            take  = min(n, avail)
            zeros = np.array(data[:take], dtype=float)
            print(f"[INFO] Loaded {take} zeros from {fname}. "
                  f"Range: {zeros[0]:.4f}-{zeros[take-1]:.4f}")
            if take < n:
                print(f"[WARN] Requested {n} zeros but only {take} available.")
            return zeros
    try:
        from mpmath import mp, zetazero
        mp.dps = 15
        print(f"[INFO] Computing {n} zeros via mpmath...")
        zeros = np.array([float(zetazero(k).imag) for k in range(1, n + 1)])
        return zeros
    except ImportError:
        pass
    print("[WARN] Using 20-zero hardcoded fallback.")
    return np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    ])

ZEROS_ALL = load_zeros(1000)
N_AVAIL   = len(ZEROS_ALL)

# ---------------------------------------------------------------------------
# Prime sieve
# ---------------------------------------------------------------------------

def sieve(n):
    if n < 2:
        return []
    is_p = np.ones(n + 1, dtype=bool)
    is_p[0:2] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            is_p[i*i::i] = False
    return list(np.where(is_p)[0].astype(int))

ALL_PRIMES = sieve(1000)

# ---------------------------------------------------------------------------
# Core computation (vectorized)
# ---------------------------------------------------------------------------

def compute_traces_full(primes):
    """
    Precompute Tr_BK(t_n) for ALL available zeros at once.
    Returns traces array of shape (N_AVAIL,).
    Tr_BK(t) = sum_p (log p / sqrt(p)) * cos(t * log p)
    """
    p_arr  = np.asarray(primes, dtype=float)
    log_p  = np.log(p_arr)
    wt     = log_p / np.sqrt(p_arr)  # shape (N_primes,)
    # cos_matrix[i, j] = cos(zeros[i] * log(p[j]))
    cos_mat = np.cos(np.outer(ZEROS_ALL, log_p))  # (N_AVAIL, N_primes)
    traces  = cos_mat @ wt  # (N_AVAIL,)
    return traces

def weil_rhs(primes):
    p_arr = np.asarray(primes, dtype=float)
    return float(-np.sum(np.log(p_arr) / np.sqrt(p_arr)))

def ratio_at(traces, n_zeros, weil_rhs_val):
    """Compute ratio using first n_zeros entries of precomputed traces."""
    n = min(n_zeros, len(traces))
    return float(np.mean(traces[:n])) / weil_rhs_val

# ---------------------------------------------------------------------------
# Track V1 — Formula Verification Suite
# ---------------------------------------------------------------------------

def run_track_V1():
    """
    Verify Tr_BK formula against all canonical Phase 32 baselines.
    PASS/FAIL for each check. Must all PASS before further computation.
    """
    print("\n" + "="*65)
    print("Track V1: Formula Verification Suite")
    print("="*65)

    results = []
    all_pass = True

    # --- Structural checks ---
    primes_6 = [p for p in ALL_PRIMES if p <= 13]
    traces_6  = compute_traces_full(primes_6)
    wrhs_6    = weil_rhs(primes_6)

    checks = [
        # (description, computed_value, expected, tolerance)
        ("Weil_RHS: 6 primes = -4.014042",
         wrhs_6, -4.014042, 1e-5),
        ("ratio: N=100, 6 primes = 0.247931",
         ratio_at(traces_6, 100, wrhs_6), 0.247931, TOLERANCE),
        ("ratio: N=500, 6 primes = 0.173349",
         ratio_at(traces_6, 500, wrhs_6), 0.173349, TOLERANCE),
    ]

    # 36-prime set
    primes_36 = [p for p in ALL_PRIMES if p <= 151]
    traces_36  = compute_traces_full(primes_36)
    wrhs_36    = weil_rhs(primes_36)
    checks.append(("ratio: N=500, 36 primes (p_max=151) = 0.136356",
                   ratio_at(traces_36, 500, wrhs_36), 0.136356, TOLERANCE))

    # 62-prime set
    primes_62 = [p for p in ALL_PRIMES if p <= 300]
    traces_62  = compute_traces_full(primes_62)
    wrhs_62    = weil_rhs(primes_62)
    checks.append(("ratio: N=500, 62 primes (p_max=300) approx c1",
                   ratio_at(traces_62, 500, wrhs_62), C1, 5e-4))

    # Tr_BK negativity check
    neg_frac = float(np.mean(traces_6[:500] < 0))
    checks.append(("Tr_BK<0 fraction: 6 primes, N=500 = 76.6% (383/500)",
                   neg_frac, 0.766, 0.02))

    print(f"\n  {'Check':<52} {'Computed':>12} {'Expected':>12} {'Status':>6}")
    print("  " + "-"*86)
    for desc, computed, expected, tol in checks:
        passed = abs(computed - expected) <= tol
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  {desc:<52} {computed:>12.6f} {expected:>12.6f} {status:>6}")
        results.append({
            "check": desc, "computed": computed, "expected": expected,
            "tolerance": tol, "passed": passed,
        })

    print(f"\n  Overall: {'ALL PASS' if all_pass else '*** FAILURES DETECTED — STOP ***'}")
    if not all_pass:
        print("  ERROR: Formula verification failed. Do not proceed with further computation.")

    return {"all_pass": all_pass, "checks": results, "formula": "Tr_BK = sum_p (log p/sqrt(p)) * cos(t*log p)"}

# ---------------------------------------------------------------------------
# Track N1 — N_zeros Dependence Analysis
# ---------------------------------------------------------------------------

def run_track_N1():
    """
    For each of three fixed prime sets, compute the Weil ratio at
    N_zeros in {50, 100, 200, 300, 500, 750, 1000}.
    Fit ratio vs N_zeros to power-law, log-decay, and 1/sqrt(N) models.
    """
    print("\n" + "="*65)
    print("Track N1: N_zeros Dependence Analysis")
    print("="*65)

    n_zeros_list = [50, 100, 200, 300, 500, 750, 1000]
    prime_sets = {
        "6_primes_pmax13":   [p for p in ALL_PRIMES if p <=  13],
        "36_primes_pmax151": [p for p in ALL_PRIMES if p <= 151],
        "62_primes_pmax300": [p for p in ALL_PRIMES if p <= 300],
    }

    all_results = {}

    for label, primes in prime_sets.items():
        print(f"\n  --- {label} (N_primes={len(primes)}) ---")
        traces = compute_traces_full(primes)
        wrhs   = weil_rhs(primes)

        n_vals     = []
        ratio_vals = []

        print(f"  {'N_zeros':>8}  {'ratio':>10}  {'vs_c1':>10}")
        print("  " + "-"*32)

        for n_z in n_zeros_list:
            if n_z > N_AVAIL:
                print(f"  {n_z:>8}  {'N/A (not enough zeros)':>24}")
                continue
            r = ratio_at(traces, n_z, wrhs)
            n_vals.append(n_z)
            ratio_vals.append(r)
            print(f"  {n_z:>8}  {r:>10.6f}  {r - C1:>+10.6f}")

        n_arr = np.array(n_vals, dtype=float)
        r_arr = np.array(ratio_vals, dtype=float)

        # Model fits
        fits = {}

        # 1: Log-decay  y = a*log(N) + b
        try:
            slope, intercept, _, _, _ = linregress(np.log(n_arr), r_arr)
            y_pred = slope * np.log(n_arr) + intercept
            ss_res = np.sum((r_arr - y_pred)**2)
            ss_tot = np.sum((r_arr - np.mean(r_arr))**2)
            r2 = 1 - ss_res / ss_tot if ss_tot > 1e-15 else float("nan")
            fits["log_decay"] = {"a": float(slope), "b": float(intercept), "R2": float(r2)}
            print(f"\n    Log-decay:   y={slope:.6f}*log(N)+{intercept:.6f}  R2={r2:.6f}")
        except Exception as e:
            fits["log_decay"] = {"error": str(e)}

        # 2: 1/sqrt(N)  y = a/sqrt(N) + b
        try:
            inv_sqrt = 1.0 / np.sqrt(n_arr)
            slope2, intercept2, _, _, _ = linregress(inv_sqrt, r_arr)
            y_pred2 = slope2 * inv_sqrt + intercept2
            ss_res2 = np.sum((r_arr - y_pred2)**2)
            r2_2 = 1 - ss_res2 / ss_tot if ss_tot > 1e-15 else float("nan")
            fits["inv_sqrt"] = {"a": float(slope2), "b": float(intercept2), "R2": float(r2_2),
                                "asymptote_b": float(intercept2)}
            print(f"    1/sqrt(N):   y={slope2:.6f}/sqrt(N)+{intercept2:.6f}  "
                  f"R2={r2_2:.6f}  asymptote={intercept2:.6f}")
        except Exception as e:
            fits["inv_sqrt"] = {"error": str(e)}

        # 3: Power-law  y = a*N^(-b)
        try:
            def power_simple(x, a, b):
                return a * x**(-b)
            popt, _ = curve_fit(power_simple, n_arr, r_arr,
                                p0=[1.0, 0.2], bounds=([0.001, 0.01], [100, 2]),
                                maxfev=10000)
            y_pred3 = power_simple(n_arr, *popt)
            ss_res3 = np.sum((r_arr - y_pred3)**2)
            r2_3 = 1 - ss_res3 / ss_tot if ss_tot > 1e-15 else float("nan")
            fits["power_simple"] = {"a": float(popt[0]), "b": float(popt[1]), "R2": float(r2_3),
                                    "asymptote": 0.0}
            print(f"    Power y=a*N^(-b): a={popt[0]:.6f}  b={popt[1]:.6f}  R2={r2_3:.6f}")
        except Exception as e:
            fits["power_simple"] = {"error": str(e)}

        # Best model
        ranked = sorted(
            [(k, v["R2"]) for k, v in fits.items() if "R2" in v and not math.isnan(v["R2"])],
            key=lambda x: -x[1]
        )
        best = ranked[0] if ranked else ("unknown", float("nan"))
        print(f"    Best model: {best[0]} (R2={best[1]:.6f})")

        all_results[label] = {
            "N_primes": len(primes),
            "Weil_RHS": wrhs,
            "N_zeros_list": n_vals,
            "ratios": ratio_vals,
            "fits": fits,
            "best_model": best[0],
        }

    # Cross-set analysis: does decay exponent depend on N_primes?
    print("\n  --- Cross-Set Decay Exponent Comparison ---")
    print(f"  {'Prime set':<25}  {'log_decay a':>14}  {'inv_sqrt a':>12}  {'best_R2':>10}")
    print("  " + "-"*65)
    for label, res in all_results.items():
        ld = res["fits"].get("log_decay", {})
        iv = res["fits"].get("inv_sqrt", {})
        bm = res["best_model"]
        best_r2 = res["fits"].get(bm, {}).get("R2", float("nan"))
        print(f"  {label:<25}  {ld.get('a', float('nan')):>14.6f}  "
              f"{iv.get('a', float('nan')):>12.6f}  {best_r2:>10.6f}")

    return {"phase": 33, "track": "N1", "c1": C1,
            "formula": "Tr_BK = sum_p (log p/sqrt(p)) * cos(t*log p)",
            "N_zeros_tested": n_zeros_list,
            "results": all_results}

# ---------------------------------------------------------------------------
# Track N2 — (N_primes, N_zeros) Ratio Surface
# ---------------------------------------------------------------------------

def run_track_N2():
    """
    Map ratio over grid: N_primes x {6,15,36,62,95,168} x N_zeros x {100,200,500,1000}.
    Identify c1 level curve: at what (N_primes, N_zeros) does ratio = c1?
    """
    print("\n" + "="*65)
    print("Track N2: (N_primes, N_zeros) Ratio Surface")
    print("="*65)

    # Prime sets: use p_max values that give the target N_primes
    # 6→13, 15→47, 36→151, 62→293 (need to check), 95→499, 168→999
    pmax_for_n = {6: 13, 15: 47, 36: 151, 62: 300, 95: 499, 168: 1000}
    n_zeros_grid = [100, 200, 500, 1000]

    # Precompute traces for each prime set
    prime_set_data = {}
    for n_p, p_max in pmax_for_n.items():
        primes = [p for p in ALL_PRIMES if p <= p_max]
        actual_n = len(primes)
        traces = compute_traces_full(primes)
        wrhs   = weil_rhs(primes)
        prime_set_data[n_p] = {"primes": primes, "actual_N_primes": actual_n,
                                "p_max_used": p_max, "traces": traces, "Weil_RHS": wrhs}

    # Build surface grid
    print(f"\n  Ratio surface (rows=N_primes, cols=N_zeros):")
    print(f"  {'N_primes':>8}  {'p_max':>6}", end="")
    for n_z in n_zeros_grid:
        print(f"  {'N='+str(n_z):>8}", end="")
    print()
    print("  " + "-"*(8 + 6 + len(n_zeros_grid)*10 + 8))

    surface = {}
    c1_level_curve = []

    for n_p in sorted(pmax_for_n.keys()):
        data   = prime_set_data[n_p]
        traces = data["traces"]
        wrhs   = data["Weil_RHS"]
        actual = data["actual_N_primes"]
        p_max  = data["p_max_used"]

        row = {"N_primes": actual, "p_max": p_max, "Weil_RHS": wrhs, "ratios": {}}
        print(f"  {actual:>8}  {p_max:>6}", end="")

        for n_z in n_zeros_grid:
            if n_z > N_AVAIL:
                print(f"  {'---':>8}", end="")
                row["ratios"][n_z] = None
                continue
            r = ratio_at(traces, n_z, wrhs)
            row["ratios"][n_z] = r
            marker = " *" if abs(r - C1) < 0.005 else "  "
            print(f"  {r:>7.4f}{marker}", end="")

            # Record c1 proximity
            if abs(r - C1) < 0.005:
                c1_level_curve.append({
                    "N_primes": actual, "p_max": p_max, "N_zeros": n_z, "ratio": r,
                    "vs_c1": r - C1,
                })

        print()
        surface[str(actual)] = row

    print(f"\n  * = within 0.005 of c1={C1:.5f}")
    print(f"\n  c1 level curve points:")
    if c1_level_curve:
        print(f"  {'N_primes':>8}  {'p_max':>6}  {'N_zeros':>8}  {'ratio':>10}  {'vs c1':>10}")
        for pt in c1_level_curve:
            print(f"  {pt['N_primes']:>8}  {pt['p_max']:>6}  {pt['N_zeros']:>8}  "
                  f"{pt['ratio']:>10.6f}  {pt['vs_c1']:>+10.6f}")
    else:
        print("  No exact c1 crossings in this grid (coarse resolution).")

    # Diagonal analysis: is c1 a level curve or just a coincidence?
    print(f"\n  Surface diagonal (N_primes grows as N_zeros grows):")
    diagonal_pairs = [(6, 100), (15, 200), (36, 500), (62, 1000)]
    for n_p, n_z in diagonal_pairs:
        if n_p in [k for k in prime_set_data] and n_z <= N_AVAIL:
            data = prime_set_data[n_p]
            r = ratio_at(data["traces"], n_z, data["Weil_RHS"])
            print(f"    (N_p={n_p}, N_z={n_z}): ratio={r:.6f}  vs c1={r-C1:+.6f}")

    return {"phase": 33, "track": "N2", "c1": C1,
            "formula": "Tr_BK = sum_p (log p/sqrt(p)) * cos(t*log p)",
            "N_zeros_grid": n_zeros_grid,
            "surface": surface,
            "c1_level_curve_points": c1_level_curve}

# ---------------------------------------------------------------------------
# Track C1 — c1 Crossing Point Analysis
# ---------------------------------------------------------------------------

def run_track_C1():
    """
    Fine-scan p_max from 200 to 400 in steps of 5 at N_zeros in {100, 500, 1000}.
    Find the exact crossing p_max where ratio = c1, interpolated between brackets.
    Test whether the crossing p_max is N_zeros-dependent.
    """
    print("\n" + "="*65)
    print("Track C1: c1 Crossing Analysis")
    print("="*65)

    scan_pmax = list(range(200, 405, 5))
    n_zeros_tests = [nz for nz in [100, 500, 1000] if nz <= N_AVAIL]

    # Precompute all primes up to 400 incrementally
    # Build cumulative traces: for each p_max, add the new prime's contribution
    primes_up_to_400 = [p for p in ALL_PRIMES if p <= 400]
    max_pmax = 400

    results_by_nz = {}

    for n_z in n_zeros_tests:
        zeros_sub = ZEROS_ALL[:n_z]
        print(f"\n  --- N_zeros={n_z} ---")

        # Compute ratio at each p_max in scan using incremental approach
        ratios_scan = []
        cumulative_weight = np.zeros(n_z)  # Tr_BK accumulator
        all_primes_400 = [p for p in ALL_PRIMES if p <= max_pmax]
        cumulative_weil = 0.0

        last_p_idx = 0
        last_p_below_200 = [p for p in ALL_PRIMES if p <= 199]

        # Initialize with all primes up to 199 (just before scan start)
        p_arr_init = np.array(last_p_below_200, dtype=float)
        log_p_init = np.log(p_arr_init)
        wt_init    = log_p_init / np.sqrt(p_arr_init)
        cumulative_weight = np.cos(np.outer(zeros_sub, log_p_init)) @ wt_init
        cumulative_weil   = -float(np.sum(wt_init))

        # Primes in range 200..400
        scan_primes_pool = [p for p in ALL_PRIMES if 200 <= p <= max_pmax]
        pool_idx = 0

        prev_pmax = 199
        prev_ratio = ratio_at(cumulative_weight, n_z, cumulative_weil)

        crossing_pmax   = None
        crossing_ratio  = None

        print(f"  {'p_max':>6}  {'N_p':>5}  {'ratio':>10}  {'vs c1':>10}", end="")
        if n_z == 500:
            print(f"  {'new primes':>20}", end="")
        print()
        print("  " + "-"*(6+5+10+10+10 + (22 if n_z == 500 else 0)))

        # Initial row (p_max=199, no new primes)
        n_p_init = len(last_p_below_200)
        print(f"  {'199':>6}  {n_p_init:>5}  {prev_ratio:>10.6f}  {prev_ratio-C1:>+10.6f}  [start]")

        for p_max in scan_pmax:
            # Add primes from (prev_pmax+1)..p_max
            new_primes = []
            while pool_idx < len(scan_primes_pool) and scan_primes_pool[pool_idx] <= p_max:
                new_primes.append(scan_primes_pool[pool_idx])
                pool_idx += 1

            if new_primes:
                np_new  = np.array(new_primes, dtype=float)
                log_new = np.log(np_new)
                wt_new  = log_new / np.sqrt(np_new)
                cumulative_weight += np.cos(np.outer(zeros_sub, log_new)) @ wt_new
                cumulative_weil   -= float(np.sum(wt_new))

            n_p_total = len(last_p_below_200) + pool_idx
            ratio = float(np.mean(cumulative_weight)) / cumulative_weil

            vs_c1 = ratio - C1

            # Print every other row (or all for 100-zero case)
            if n_z != 500 or p_max % 10 == 0 or abs(vs_c1) < 0.003:
                new_str = (f"+p={new_primes}" if new_primes else "(no new)")
                print(f"  {p_max:>6}  {n_p_total:>5}  {ratio:>10.6f}  {vs_c1:>+10.6f}", end="")
                if n_z == 500:
                    print(f"  {new_str:>20}", end="")
                print()

            # Detect crossing c1
            if crossing_pmax is None:
                if prev_ratio >= C1 and ratio < C1:
                    # Linear interpolation
                    frac = (prev_ratio - C1) / (prev_ratio - ratio)
                    interp_pmax = prev_pmax + frac * (p_max - prev_pmax)
                    crossing_pmax  = float(interp_pmax)
                    crossing_ratio = float(C1)
                    print(f"  *** c1 CROSSING at p_max={interp_pmax:.2f} "
                          f"(between {prev_pmax} and {p_max}) ***")
                elif prev_ratio < C1 and crossing_pmax is None:
                    # Already below c1 at start of scan
                    print(f"  NOTE: Already below c1 at start of scan (N_zeros={n_z})")

            prev_pmax  = p_max
            prev_ratio = ratio
            ratios_scan.append({"p_max": p_max, "N_primes": n_p_total,
                                 "ratio": ratio, "vs_c1": vs_c1})

        results_by_nz[n_z] = {
            "N_zeros": n_z,
            "scan": ratios_scan,
            "crossing_p_max_interpolated": crossing_pmax,
        }

    # Summary: crossing p_max vs N_zeros
    print(f"\n  --- Crossing p_max Summary ---")
    print(f"  {'N_zeros':>8}  {'Crossing p_max':>16}  {'N_zeros-dependent?':>20}")
    print("  " + "-"*48)
    crossings = []
    for n_z, res in results_by_nz.items():
        cp = res["crossing_p_max_interpolated"]
        crossings.append(cp)
        cp_str = f"{cp:.1f}" if cp is not None else "not in scan range"
        print(f"  {n_z:>8}  {cp_str:>16}")

    valid_crossings = [c for c in crossings if c is not None]
    if len(valid_crossings) >= 2:
        span = max(valid_crossings) - min(valid_crossings)
        print(f"\n  Crossing p_max span across N_zeros values: {span:.1f}")
        if span < 20:
            print("  => Crossing p_max is approximately N_zeros-INDEPENDENT (span < 20)")
        else:
            print("  => Crossing p_max is N_zeros-DEPENDENT (span >= 20)")

    return {"phase": 33, "track": "C1", "c1": C1,
            "scan_pmax_range": [200, 400, 5],
            "N_zeros_tested": n_zeros_tests,
            "results_by_N_zeros": results_by_nz,
            "crossing_summary": {
                str(n_z): results_by_nz[n_z]["crossing_p_max_interpolated"]
                for n_z in n_zeros_tests
            }}

# ---------------------------------------------------------------------------
# JSON serialization helper
# ---------------------------------------------------------------------------

def json_safe(obj):
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.bool_):
        return bool(obj)
    return obj

# ---------------------------------------------------------------------------
# Save artifacts
# ---------------------------------------------------------------------------

def save_artifacts(v1, n1, n2, c1_res):
    with open("phase33_formula_verification.json", "w") as f:
        json.dump(json_safe(v1), f, indent=2)
    print("[OK] Saved phase33_formula_verification.json")

    with open("phase33_nzeros_dependence.json", "w") as f:
        json.dump(json_safe(n1), f, indent=2)
    print("[OK] Saved phase33_nzeros_dependence.json")

    with open("phase33_ratio_surface.json", "w") as f:
        json.dump(json_safe(n2), f, indent=2)
    print("[OK] Saved phase33_ratio_surface.json")

    with open("phase33_c1_crossing.json", "w", encoding="utf-8") as f:
        json.dump(json_safe(c1_res), f, indent=2)
    print("[OK] Saved phase33_c1_crossing.json")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("RH Investigation - Phase 33")
    print("Chavez AI Labs LLC | Applied Pathological Mathematics")
    print("Weil Ratio Double-Dependence Characterization")
    print("="*65)
    print(f"c1={C1}  theta_W={THETA_W:.6f} deg")
    print(f"Zeros available: {N_AVAIL}")

    v1 = run_track_V1()

    if not v1["all_pass"]:
        print("\nABORTING: Formula verification failed.")
        return

    n1     = run_track_N1()
    n2     = run_track_N2()
    c1_res = run_track_C1()

    save_artifacts(v1, n1, n2, c1_res)

    print("\n" + "="*65)
    print("Phase 33 complete.")
    # Summarize key findings
    crossings = c1_res.get("crossing_summary", {})
    for n_z, cp in crossings.items():
        cp_str = f"{cp:.1f}" if cp is not None else "not detected"
        print(f"  c1 crossing at N_zeros={n_z}: p_max={cp_str}")
    print("="*65)

if __name__ == "__main__":
    main()
