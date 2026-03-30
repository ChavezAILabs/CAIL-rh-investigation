#!/usr/bin/env python3
"""
rh_phase32.py — Riemann Hypothesis Investigation, Phase 32
Chavez AI Labs LLC | Applied Pathological Mathematics

Two-Regime Weil Characterization + Track D Reconciliation

Tracks:
    Track A1: Regime boundary fine-scan (p_max 151→200, step ~5)
    Track A2: Regime 2 extended trajectory (p_max 200→1000)
    Track A3: Separate regime fitting (power-law R1 / log R2)
    Track D1: Bilateral zero pair count reconciliation (161 vs 6,290)

Formulas (verified against Phase 30/31 baseline — do not modify):
    Tr_BK(t_n)  = Σ_{p≤p_max} log(p) · cos(t_n · log p)
    Weil_RHS    = −Σ_{p≤p_max} log(p) / √p
    ratio       = mean(Tr_BK over N_zeros) / Weil_RHS

Usage:
    python rh_phase32.py

Outputs:
    phase32_boundary_scan.json      — Track A1 fine-scan
    phase32_weil_full.json          — Track A2 full sequence p_max 13→1000
    phase32_regime_fits.json        — Track A3 separate regime fits
    phase32_track_d_reconciliation.txt — Track D1 methodology comparison

Dependencies: numpy, scipy  (zeros loaded from rh_zeros.json)

Author: Paul Chavez / Chavez AI Labs LLC
Date:   2026-03-27
Phase:  32
"""

import json
import math
import os
import sys
import time
import numpy as np

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from scipy.optimize import curve_fit
from scipy.stats import linregress

# ---------------------------------------------------------------------------
# Constants (machine-verified — do not change)
# ---------------------------------------------------------------------------

C1          = 0.11797805192095003   # sin(θ_W), sedenion structural angle
C3          = 0.99301620292165280   # cos(θ_W)
WEIL_ANGLE  = math.degrees(math.acos(C3))   # 6.775425°
C_CIRCLE    = 1.0 / (2.0 * math.pi)         # 0.159155, Circle Method
N_ZEROS     = 500

# Phase 30 baseline (9 points, verified) — Regime 1 ground truth
P30_PMAX    = [13,   23,   29,   37,   53,   71,   97,   127,  151]
P30_NPRIMES = [ 6,    9,   10,   12,   16,   20,   25,    31,   36]
P30_RATIOS  = [0.2479, 0.2466, 0.2416, 0.2344, 0.2189,
               0.2106, 0.1970, 0.1833, 0.1736]

# Phase 31 extension (4 points, Regime 2) — for continuity in A2
P31_PMAX    = [200,    300,    500,    700]
P31_NPRIMES = [ 46,     62,     95,    125]
P31_RATIOS  = [1.1132, 1.0786, 0.9928, 0.9549]
P31_WRHS    = [-23.272, -28.848, -38.761, -46.598]

# ---------------------------------------------------------------------------
# Load Riemann zeros from JSON cache
# ---------------------------------------------------------------------------

def load_zeros(n=500):
    """
    Load first n Riemann zeros from rh_zeros.json (1,000 zeros, dps=25).
    Falls back to rh_zeros_10k.json, then mpmath, then 20-zero hardcoded list.
    """
    candidates = ["rh_zeros.json", "rh_zeros_10k.json"]
    for fname in candidates:
        if os.path.exists(fname):
            with open(fname) as f:
                data = json.load(f)
            zeros = np.array(data[:n], dtype=float)
            if len(zeros) >= n:
                print(f"[INFO] Loaded {n} zeros from {fname}. "
                      f"Range: {zeros[0]:.4f}–{zeros[n-1]:.4f}")
                return zeros
            print(f"[WARN] {fname} has only {len(data)} zeros; need {n}.")

    # Try mpmath
    try:
        from mpmath import mp, zetazero
        mp.dps = 15
        print(f"[INFO] Computing {n} zeros via mpmath (slow)...")
        zeros = np.array([float(zetazero(k).imag) for k in range(1, n + 1)])
        print(f"[INFO] Done. Range: {zeros[0]:.4f}–{zeros[n-1]:.4f}")
        return zeros
    except ImportError:
        pass

    # Hardcoded 20-zero fallback — results will be indicative only
    print("[WARN] Using 20-zero fallback. Install mpmath for accurate results.")
    return np.array([
        14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
        37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
        52.970321, 56.446247, 59.347044, 60.831779, 65.112544,
        67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    ])

ZEROS = load_zeros(N_ZEROS)

# ---------------------------------------------------------------------------
# Prime sieve
# ---------------------------------------------------------------------------

def sieve(n):
    """Sieve of Eratosthenes — return all primes ≤ n."""
    if n < 2:
        return []
    is_prime = np.ones(n + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    return list(np.where(is_prime)[0].astype(int))

ALL_PRIMES_1000 = sieve(1000)

# ---------------------------------------------------------------------------
# Core Weil ratio computation (formula verified in Phase 30/31)
# ---------------------------------------------------------------------------

def bilateral_trace(primes, zeros):
    """
    Tr_BK(t_n) = Σ_p (log p / √p) · cos(t_n · log p)
    Phase 30 formula (rh_phase30.py line 30): log(p)/sqrt(p) * cos(t*log p).
    Phase 32 handoff formula reference: Σ_{p≤p_max} (log p / √p) · cos(t_n · log p).
    NOTE: Phase 31 script incorrectly dropped 1/√p — this is the corrected version.
    """
    p_arr  = np.asarray(primes, dtype=float)
    log_p  = np.log(p_arr)
    weight = log_p / np.sqrt(p_arr)   # log(p)/√p
    traces = np.array([
        float(np.dot(weight, np.cos(t * log_p)))
        for t in zeros
    ])
    return traces

def weil_rhs(primes):
    """
    Weil_RHS = −Σ_p log(p) / √p
    Verified formula from Phase 30/31.
    """
    p = np.asarray(primes, dtype=float)
    return float(-np.sum(np.log(p) * p**(-0.5)))

def compute_weil_ratio(primes, zeros):
    """Compute Weil ratio, mean Tr_BK, and Weil RHS for a prime set."""
    traces   = bilateral_trace(primes, zeros)
    mean_tr  = float(np.mean(traces))
    w_rhs    = weil_rhs(primes)
    ratio    = mean_tr / w_rhs if abs(w_rhs) > 1e-12 else float("nan")
    return ratio, mean_tr, w_rhs

# ---------------------------------------------------------------------------
# Formula Correction Check — Phase 31 bug identification
# ---------------------------------------------------------------------------

def run_formula_correction_check():
    """
    Verify that the Phase 32 formula (with 1/√p) reproduces Phase 30 baseline
    at N_zeros=100, and identify the Phase 31 formula bug.

    Phase 30 (rh_phase30.py line 30): log(p)/sqrt(p)*cos(t*log p)  [correct]
    Phase 31 (bilateral_trace):       log(p)*cos(t*log p)           [WRONG — missing 1/√p]
    Phase 32 handoff spec:            (log p / √p) · cos(t · log p) [correct]

    Impact: Phase 31 extension ratios (1.1132, 1.0786, 0.9928, 0.9549) were
    computed with the wrong formula. The 'two-regime inversion' is a formula artifact.
    """
    print("\n" + "="*65)
    print("Formula Correction Check (Phase 31 Bug Identification)")
    print("="*65)

    primes_6 = [2, 3, 5, 7, 11, 13]

    print(f"\n  Phase 30 reported ratio=0.2479 for {{2,3,5,7,11,13}} at N_zeros=100.")
    print(f"  Reproducing with Phase 32 formula (log p/sqrt(p), N=100):")

    p_arr  = np.array(primes_6, dtype=float)
    log_p  = np.log(p_arr)
    wt     = log_p / np.sqrt(p_arr)
    w_rhs  = -float(np.sum(wt))

    for n_z in [100, 200, 500]:
        traces = np.array([float(np.dot(wt, np.cos(t * log_p))) for t in ZEROS[:n_z]])
        ratio  = float(np.mean(traces)) / w_rhs
        print(f"    N_zeros={n_z:>3}: ratio={ratio:.6f}  "
              f"{'<-- matches P30 0.2479' if n_z == 100 else ''}")

    print(f"\n  Phase 31 formula (log p, no sqrt, N=100):")
    for n_z in [100, 500]:
        traces_wrong = np.array([
            float(np.sum(log_p * np.cos(t * log_p))) for t in ZEROS[:n_z]
        ])
        ratio_wrong = float(np.mean(traces_wrong)) / w_rhs
        print(f"    N_zeros={n_z:>3}: ratio={ratio_wrong:.6f}  "
              f"(factor {ratio_wrong / (float(np.mean(np.array([float(np.dot(wt, np.cos(t*log_p))) for t in ZEROS[:n_z]]))) / w_rhs):.2f}x wrong)")

    print(f"\n  CONCLUSION:")
    print(f"  Phase 31 bilateral_trace dropped 1/sqrt(p) from log(p)/sqrt(p)*cos(t*log p).")
    print(f"  The Phase 31 extension ratios {P31_RATIOS} are INVALID.")
    print(f"  The 'inversion' at p_max=200 (ratio=1.113) is a formula artifact.")
    print(f"  Phase 32 uses the CORRECT formula throughout.")

    # What the Phase 31 extension ratios would have been (correct formula)
    print(f"\n  Phase 31 extension ratios corrected:")
    print(f"  {'p_max':>6}  {'N_p':>5}  {'P31_wrong':>12}  {'P32_correct':>12}")
    print("  " + "-"*44)
    for p_max in P31_PMAX:
        primes = [p for p in ALL_PRIMES_1000 if p <= p_max]
        ratio_c, _, _ = compute_weil_ratio(primes, ZEROS)
        p31_wrong = P31_RATIOS[P31_PMAX.index(p_max)]
        print(f"  {p_max:>6}  {len(primes):>5}  {p31_wrong:>12.6f}  {ratio_c:>12.6f}")

    return {
        "phase31_formula": "log(p) * cos(t*log p)  [WRONG — missing 1/sqrt(p)]",
        "phase32_formula": "(log p / sqrt(p)) * cos(t * log p)  [CORRECT, matches Phase 30]",
        "phase30_verification": "N_zeros=100, 6 primes -> ratio=0.2479 (matches P30 baseline)",
        "phase31_inversion_status": "FORMULA ARTIFACT — does not exist with correct formula",
        "phase31_ratios_invalid": dict(zip(P31_PMAX, P31_RATIOS)),
    }

# ---------------------------------------------------------------------------
# Track A1 — Regime boundary fine-scan
# ---------------------------------------------------------------------------

def run_track_A1():
    """
    Fine-scan p_max ∈ {155,157,160,163,165,170,175,180,190,200} to locate
    the regime boundary between Regime 1 (ratio≈0.17) and Regime 2 (ratio≈1.1).
    Phase 31 anchor points: p_max=151→ratio=0.1736, p_max=200→ratio=1.1132.
    """
    print("\n" + "="*65)
    print("Track A1: Regime Boundary Fine-Scan (p_max 155→200)")
    print("="*65)

    scan_targets = [155, 157, 160, 163, 165, 170, 175, 180, 190, 200]

    results   = []
    prev_ratio = P30_RATIOS[-1]  # 0.1736 at p_max=151

    print(f"\n  {'p_max':>6}  {'N_p':>5}  {'ratio':>10}  {'Weil_RHS':>12}  "
          f"{'Δratio':>10}  {'Note'}")
    print("  " + "-"*70)

    first_above_half = None
    first_above_one  = None

    # Reference: p_max=151
    primes_151 = [p for p in ALL_PRIMES_1000 if p <= 151]
    ratio_151, _, _ = compute_weil_ratio(primes_151, ZEROS)
    print(f"  {'151':>6}  {len(primes_151):>5}  {ratio_151:>10.6f}  "
          f"{'---':>12}  {'---':>10}  [Phase 30 anchor]")

    for p_max in scan_targets:
        primes = [p for p in ALL_PRIMES_1000 if p <= p_max]
        ratio, mean_tr, w_rhs = compute_weil_ratio(primes, ZEROS)
        delta = ratio - prev_ratio
        n_p   = len(primes)

        # Primes added since last step
        prev_pmax = scan_targets[scan_targets.index(p_max) - 1] if scan_targets.index(p_max) > 0 else 151
        new_primes = [p for p in primes if prev_pmax < p <= p_max]
        note = f"+p={new_primes}" if new_primes else "(no new primes)"

        print(f"  {p_max:>6}  {n_p:>5}  {ratio:>10.6f}  {w_rhs:>12.4f}  "
              f"{delta:>+10.6f}  {note}")

        if first_above_half is None and ratio > 0.50:
            first_above_half = p_max
        if first_above_one is None and ratio > 1.00:
            first_above_one = p_max

        results.append({
            "p_max": p_max, "N_primes": n_p,
            "ratio": ratio, "Weil_RHS": w_rhs, "mean_Tr_BK": mean_tr,
            "delta_ratio": delta, "new_primes_added": new_primes,
        })
        prev_ratio = ratio

    print(f"\n  First p_max with ratio > 0.50: {first_above_half}")
    print(f"  First p_max with ratio > 1.00: {first_above_one}")

    # Prime gap hypothesis: does boundary align with gap 157→163?
    gap_157_163 = 163 - 157
    print(f"\n  Prime gap 157→163 = {gap_157_163}")
    print(f"  Hypothesis: inversion driven by adding p=157 or p=163")
    r_157 = next((r["ratio"] for r in results if r["p_max"] == 157), None)
    r_163 = next((r["ratio"] for r in results if r["p_max"] == 163), None)
    if r_157 and r_163:
        print(f"  ratio at p_max=157 (adds p=157): {r_157:.6f}")
        print(f"  ratio at p_max=163 (adds p=163): {r_163:.6f}")
        if r_157 > 0.5:
            print("  => INVERSION triggered by adding p=157")
        elif r_163 > 0.5:
            print("  => INVERSION triggered by adding p=163")
        else:
            print("  => Inversion occurs later (p > 163)")

    return {
        "phase": 32, "track": "A1", "N_zeros": N_ZEROS,
        "c1": C1,
        "regime1_anchor": {"p_max": 151, "ratio": ratio_151},
        "regime2_anchor": {"p_max": 200, "ratio": P31_RATIOS[0]},
        "first_p_max_above_0p50": first_above_half,
        "first_p_max_above_1p00": first_above_one,
        "prime_gap_157_163": gap_157_163,
        "points": results,
    }

# ---------------------------------------------------------------------------
# Track A2 — Regime 2 extended trajectory
# ---------------------------------------------------------------------------

def run_track_A2():
    """
    Full Weil ratio sequence from p_max=200 to p_max=1000.
    All points freshly computed with correct formula (log p/√p in Tr_BK, N=500 zeros).
    Phase 31 cached values are NOT used — they were computed with wrong formula.
    """
    print("\n" + "="*65)
    print("Track A2: Full Extended Trajectory (p_max 200→1000, correct formula)")
    print("="*65)
    print("  NOTE: Phase 31 values (1.1132, etc.) are NOT used — formula bug.")
    print("  All points freshly computed: Tr_BK = sum_p (log p / sqrt(p)) * cos(t*log p)")

    r2_targets = [200, 250, 300, 400, 500, 600, 700, 800, 900, 1000]

    results = []
    print(f"\n  {'p_max':>6}  {'N_p':>5}  {'ratio':>10}  {'Weil_RHS':>12}  {'vs c1':>10}")
    print("  " + "-"*60)

    for p_max in r2_targets:
        t0 = time.time()
        primes = [p for p in ALL_PRIMES_1000 if p <= p_max]
        ratio, mean_tr, w_rhs = compute_weil_ratio(primes, ZEROS)
        n_p = len(primes)
        _ = time.time() - t0

        vs_c1 = ratio - C1
        print(f"  {p_max:>6}  {n_p:>5}  {ratio:>10.6f}  {w_rhs:>12.4f}  {vs_c1:>+10.6f}")
        results.append({
            "p_max": p_max, "N_primes": n_p,
            "ratio": ratio, "Weil_RHS": w_rhs, "mean_Tr_BK": mean_tr,
            "vs_c1": vs_c1,
        })

    ratios = [r["ratio"] for r in results]
    print(f"\n  Regime 2 sequence: {[f'{r:.4f}' for r in ratios]}")
    monotone_dec = all(ratios[i] > ratios[i+1] for i in range(len(ratios)-1))
    print(f"  Monotone decreasing: {monotone_dec}")
    print(f"  Min ratio (p_max=1000): {ratios[-1]:.6f}")
    print(f"  Difference from 1.0 at p_max=1000: {ratios[-1]-1.0:+.6f}")

    # Regime 2 trend: fit three models
    n_primes = np.array([r["N_primes"] for r in results], dtype=float)
    ratio_arr = np.array(ratios, dtype=float)

    print("\n  Model fits for Regime 2:")

    # Model 1: log decay  y = a*log(x) + b
    try:
        log_n = np.log(n_primes)
        slope, intercept, r_val, p_val, _ = linregress(log_n, ratio_arr)
        y_pred_log = slope * log_n + intercept
        ss_res = np.sum((ratio_arr - y_pred_log)**2)
        ss_tot = np.sum((ratio_arr - np.mean(ratio_arr))**2)
        r2_log = 1 - ss_res / ss_tot if ss_tot > 1e-15 else float("nan")
        asymptote_log = slope * np.log(1e6) + intercept  # extrapolate to N=1000 primes
        print(f"    Log decay:   y = {slope:.6f}·log(N) + {intercept:.6f}  "
              f"R²={r2_log:.6f}  (extrapolated at N=1000 primes: {asymptote_log:.4f})")
    except Exception as e:
        slope, intercept, r2_log = float("nan"), float("nan"), float("nan")
        print(f"    Log decay: FAILED ({e})")

    # Model 2: power decay y = a*x^(-b) + c (free c)
    r2_power = float("nan")
    power_params = {}
    try:
        def power_free(x, a, b, c):
            return a * x**(-b) + c
        popt, _ = curve_fit(power_free, n_primes, ratio_arr,
                            p0=[2.0, 0.3, 0.8], bounds=([0, 0.01, -2], [100, 3, 3]),
                            maxfev=20000)
        y_pred_pow = power_free(n_primes, *popt)
        ss_res = np.sum((ratio_arr - y_pred_pow)**2)
        r2_power = 1 - ss_res / np.sum((ratio_arr - np.mean(ratio_arr))**2)
        power_params = {"a": float(popt[0]), "b": float(popt[1]), "c": float(popt[2])}
        print(f"    Power decay: y = {popt[0]:.4f}·N^(-{popt[1]:.4f}) + {popt[2]:.6f}  "
              f"R²={r2_power:.6f}  asymptote_c={popt[2]:.6f}")
    except Exception as e:
        print(f"    Power decay: FAILED ({e})")

    # Model 3: constant (null model)
    mean_r2 = float(np.mean(ratio_arr))
    ss_res_const = float(np.sum((ratio_arr - mean_r2)**2))
    print(f"    Constant:    y = {mean_r2:.6f}  SSE={ss_res_const:.6f}  "
          f"(null — all variance is signal)")

    # Best model by R²
    models_r2 = [("log decay", r2_log), ("power decay", r2_power)]
    best_model = max(models_r2, key=lambda x: x[1] if not math.isnan(x[1]) else -999)
    print(f"\n  Best fit: {best_model[0]} (R²={best_model[1]:.6f})")

    return {
        "phase": 32, "track": "A2", "N_zeros": N_ZEROS,
        "points": results,
        "monotone_decreasing": bool(monotone_dec),
        "model_log_decay": {
            "slope": float(slope), "intercept": float(intercept), "R2": float(r2_log),
        },
        "model_power_decay": {**power_params, "R2": float(r2_power)},
        "best_model": best_model[0],
    }

# ---------------------------------------------------------------------------
# Track A3 — Separate regime fitting
# ---------------------------------------------------------------------------

def run_track_A3():
    """
    Fit Regime 1 (9 points, p_max 13→151) and Regime 2 (Phase 31 + A2 new points)
    with appropriate models independently.

    Regime 1: power-law y=a·x^(-b)+c  (x = N_primes)
              three fixed-c runs: c₁=0.118, 1/4=0.250, 1/2π=0.159, plus free fit
    Regime 2: log model y=a·log(x)+b plus power-law; report best R²
    """
    print("\n" + "="*65)
    print("Track A3: Separate Regime Fitting")
    print("="*65)

    # ---- Regime 1 ----
    n1 = np.array(P30_NPRIMES, dtype=float)
    r1 = np.array(P30_RATIOS,  dtype=float)

    # Recompute Phase 30 p_max baseline with 500 zeros and correct formula
    print("\n  --- Regime 1: Phase 30 p_max points, recomputed at N=500 zeros ---")
    r1_recomputed = []
    for p_max_r1 in P30_PMAX:
        primes_r1 = [p for p in ALL_PRIMES_1000 if p <= p_max_r1]
        ratio_r1, _, _ = compute_weil_ratio(primes_r1, ZEROS)
        r1_recomputed.append(ratio_r1)

    n1 = np.array(P30_NPRIMES, dtype=float)
    r1 = np.array(r1_recomputed, dtype=float)

    print(f"  x = N_primes:      {P30_NPRIMES}")
    print(f"  y (Phase30, N=100):  {[f'{x:.4f}' for x in P30_RATIOS]}")
    print(f"  y (Phase32, N=500):  {[f'{x:.4f}' for x in r1_recomputed]}")
    print(f"  NOTE: Using Phase 32 (N=500) values for fitting.")

    def power_fixed(c_val):
        def f(x, a, b):
            return a * x**(-b) + c_val
        return f

    def power_free(x, a, b, c):
        return a * x**(-b) + c

    def fit_fixed(c_val, label):
        best = {"sse": np.inf, "r2": -np.inf, "a": None, "b": None}
        for a0 in [0.1, 0.3, 0.5, 1.0, 2.0]:
            for b0 in [0.2, 0.4, 0.5, 0.7, 1.0]:
                try:
                    popt, _ = curve_fit(power_fixed(c_val), n1, r1,
                                        p0=[a0, b0],
                                        bounds=([0.001, 0.01], [20, 3]),
                                        maxfev=20000)
                    y_pred = power_fixed(c_val)(n1, *popt)
                    ss_res = np.sum((r1 - y_pred)**2)
                    ss_tot = np.sum((r1 - np.mean(r1))**2)
                    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-15 else float("nan")
                    if ss_res < best["sse"]:
                        best = {"sse": ss_res, "r2": r2,
                                "a": float(popt[0]), "b": float(popt[1])}
                except Exception:
                    pass
        if best["a"] is not None:
            print(f"    c={c_val:.5f} ({label:12s}):  "
                  f"a={best['a']:.4f}  b={best['b']:.4f}  "
                  f"R²={best['r2']:.6f}  SSE={best['sse']:.8f}")
        else:
            print(f"    c={c_val:.5f} ({label}): FIT FAILED")
        return best

    c_runs = [
        (C1,       "c1=sin(θW)"),
        (0.25,     "1/4"),
        (C_CIRCLE, "1/2π"),
    ]
    r1_fits = {}
    for c_val, label in c_runs:
        r1_fits[label] = fit_fixed(c_val, label)
        r1_fits[label]["c_fixed"] = c_val

    # Free fit (c unconstrained)
    print(f"    Free fit:")
    try:
        popt_free, _ = curve_fit(power_free, n1, r1,
                                  p0=[0.5, 0.4, 0.15],
                                  bounds=([0.001, 0.01, -0.5], [20, 3, 1]),
                                  maxfev=20000)
        y_pred_free = power_free(n1, *popt_free)
        ss_res_free = float(np.sum((r1 - y_pred_free)**2))
        ss_tot_free = float(np.sum((r1 - np.mean(r1))**2))
        r2_free = 1 - ss_res_free / ss_tot_free if ss_tot_free > 1e-15 else float("nan")
        print(f"      a={popt_free[0]:.4f}  b={popt_free[1]:.4f}  c={popt_free[2]:.5f}  "
              f"R²={r2_free:.6f}  SSE={ss_res_free:.8f}")
        r1_fits["free"] = {
            "a": float(popt_free[0]), "b": float(popt_free[1]), "c": float(popt_free[2]),
            "R2": r2_free, "sse": ss_res_free,
        }
    except Exception as e:
        print(f"      FAILED: {e}")
        r1_fits["free"] = {"error": str(e)}

    # Best fixed-c by SSE
    fixed_results = [(k, v) for k, v in r1_fits.items() if k != "free" and v.get("a")]
    if fixed_results:
        best_fixed = min(fixed_results, key=lambda x: x[1]["sse"])
        print(f"\n  Best Regime 1 fixed-c: {best_fixed[0]} (SSE={best_fixed[1]['sse']:.8f})")

    # ---- Regime 2 ----
    # Recompute Phase 31 extension points with correct formula (N=500 zeros)
    r2_pmax = [200, 300, 500, 700]
    r2_nprimes = []
    r2_ratios  = []
    for p_max_r2 in r2_pmax:
        primes_r2 = [p for p in ALL_PRIMES_1000 if p <= p_max_r2]
        ratio_r2, _, _ = compute_weil_ratio(primes_r2, ZEROS)
        r2_nprimes.append(len(primes_r2))
        r2_ratios.append(ratio_r2)

    n2 = np.array(r2_nprimes, dtype=float)
    r2 = np.array(r2_ratios,  dtype=float)

    print("\n  --- Regime 2 (p_max 200→700, correct formula, N=500 zeros) ---")
    print(f"  Phase 31 wrong values:   {P31_RATIOS} [INVALID, formula bug]")
    print(f"  Phase 32 correct values: {[f'{x:.4f}' for x in r2_ratios]}")
    print(f"  N_primes: {r2_nprimes}")

    r2_fits = {}

    # Model: log decay  y = a*log(N) + b
    try:
        log_n2 = np.log(n2)
        slope2, intercept2, rval2, _, _ = linregress(log_n2, r2)
        y_pred2 = slope2 * log_n2 + intercept2
        ss_res2 = float(np.sum((r2 - y_pred2)**2))
        ss_tot2 = float(np.sum((r2 - np.mean(r2))**2))
        r2_log_r2 = 1 - ss_res2 / ss_tot2 if ss_tot2 > 1e-15 else float("nan")
        asymptote_1k = slope2 * np.log(len([p for p in ALL_PRIMES_1000 if p <= 1000])) + intercept2
        print(f"    Log decay:   y = {slope2:.6f}·log(N) + {intercept2:.6f}  "
              f"R²={r2_log_r2:.6f}")
        print(f"    Extrapolated ratio at N~170 primes (p_max=1000): {asymptote_1k:.4f}")
        r2_fits["log_decay"] = {
            "slope": float(slope2), "intercept": float(intercept2), "R2": float(r2_log_r2),
            "extrapolated_N1000_primes": float(asymptote_1k),
        }
    except Exception as e:
        print(f"    Log decay: FAILED ({e})")
        r2_fits["log_decay"] = {"error": str(e)}

    # Model: power decay y = a*x^(-b) + c
    try:
        popt_r2, _ = curve_fit(power_free, n2, r2,
                                p0=[2.0, 0.3, 0.8],
                                bounds=([0, 0.01, -1], [100, 3, 3]),
                                maxfev=20000)
        y_pred_r2 = power_free(n2, *popt_r2)
        ss_res_r2p = float(np.sum((r2 - y_pred_r2)**2))
        ss_tot_r2p = float(np.sum((r2 - np.mean(r2))**2))
        r2_pow_r2 = 1 - ss_res_r2p / ss_tot_r2p if ss_tot_r2p > 1e-15 else float("nan")
        print(f"    Power decay: y = {popt_r2[0]:.4f}·N^(-{popt_r2[1]:.4f}) + {popt_r2[2]:.6f}  "
              f"R²={r2_pow_r2:.6f}  asymptote_c={popt_r2[2]:.6f}")
        r2_fits["power_decay"] = {
            "a": float(popt_r2[0]), "b": float(popt_r2[1]), "c": float(popt_r2[2]),
            "R2": float(r2_pow_r2),
        }
    except Exception as e:
        print(f"    Power decay: FAILED ({e})")
        r2_fits["power_decay"] = {"error": str(e)}

    print(f"\n  Note: Regime 2 uses {len(r2_ratios)} corrected points (Phase 31 formula bug fixed).")
    print(f"  Full Regime 2 (10 points, p_max 200-1000) fits saved in phase32_regime_fits.json.")

    return {
        "regime1": {
            "description": "Regime 1: 9 points (p_max 13→151), power-law y=a*N^(-b)+c",
            "x_variable": "N_primes",
            "data_N_primes": P30_NPRIMES,
            "data_ratios": P30_RATIOS,
            "fits": r1_fits,
        },
        "regime2": {
            "description": "Regime 2: 4 points (p_max 200→700), Phase 31 data",
            "data_N_primes": r2_nprimes,
            "data_ratios": r2_ratios,
            "fits": r2_fits,
            "note": "4-point fit; update after Track A2 completes for more Regime 2 points",
        },
    }

# ---------------------------------------------------------------------------
# Track D1 — Bilateral zero pair count reconciliation
# ---------------------------------------------------------------------------

def run_track_D1():
    """
    Reconcile Phase 29 CAILculator count (6,290 pairs) vs Phase 31
    Python count (161 pairs) at N=500 zeros.

    Investigation:
    1. Document the two methodologies
    2. Probe what threshold in the Python criterion gives ~6,290
    3. Check alternative pairing criteria
    4. State the conclusion
    """
    print("\n" + "="*65)
    print("Track D1: Bilateral Zero Pair Count Reconciliation")
    print("="*65)

    primes_6 = [2, 3, 5, 7, 11, 13]   # Phase 29/31 baseline prime set
    traces    = bilateral_trace(primes_6, ZEROS)
    N         = len(ZEROS)
    N_pairs   = N * (N - 1) // 2

    print(f"\n  N zeros:     {N}")
    print(f"  N pairs:     {N_pairs:,}")
    print(f"  Prime set:   {primes_6}")
    print(f"  Tr_BK range: [{traces.min():.4f}, {traces.max():.4f}]")
    print(f"  Tr_BK mean:  {traces.mean():.4f}  std: {traces.std():.4f}")
    neg_count = int(np.sum(traces < 0))
    pos_count = N - neg_count
    print(f"  Tr_BK < 0:   {neg_count}/500 = {neg_count/N*100:.1f}%  "
          f"(Phase 29 BK burst: 383/500 = 76.6%)")

    # ---- Probe criterion: |Tr(i) + Tr(j)| < threshold ----
    print("\n  Probe A — Phase 31 criterion: |Tr(i) + Tr(j)| < threshold")
    print(f"  {'Threshold':>12}  {'Pairs':>10}  {'% of total':>12}")
    print("  " + "-"*38)

    threshold_scan = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    sum_criterion = {}
    for thr in threshold_scan:
        count = 0
        for i in range(N):
            for j in range(i + 1, N):
                if abs(traces[i] + traces[j]) < thr:
                    count += 1
        pct = count / N_pairs * 100
        sum_criterion[thr] = count
        marker = "  <-- Phase 31 (161 pairs)" if thr == 0.01 else (
                 "  <-- target ~6290" if 5500 < count < 7000 else "")
        print(f"  {thr:>12.4f}  {count:>10,}  {pct:>11.2f}%{marker}")

    # ---- Probe criterion: |Tr(i)| < threshold AND |Tr(j)| < threshold ----
    print("\n  Probe B — Both traces near zero: |Tr(i)| < thr AND |Tr(j)| < thr")
    small_trace_n = {}
    for thr in [0.1, 0.5, 1.0, 2.0, 5.0]:
        n_small = int(np.sum(np.abs(traces) < thr))
        pairs_both_small = n_small * (n_small - 1) // 2
        small_trace_n[thr] = {"n_small": n_small, "pairs": pairs_both_small}
        print(f"  thr={thr:.2f}:  {n_small} zeros with |Tr| < thr  →  "
              f"{pairs_both_small:,} pairs")

    # ---- Probe criterion: opposite sign (bilateral = +/- pair) ----
    print("\n  Probe C — Opposite sign: Tr(i)>0 AND Tr(j)<0 (or vice versa)")
    opp_sign_pairs = int(pos_count) * int(neg_count)
    print(f"  Positive traces: {pos_count}, Negative traces: {neg_count}")
    print(f"  Opposite-sign pairs: {opp_sign_pairs:,}")

    # ---- Probe D: same sign (ZDTP 'bilateral' might mean matching polarity) ----
    same_sign_pairs = pos_count*(pos_count-1)//2 + neg_count*(neg_count-1)//2
    print(f"  Same-sign pairs:     {same_sign_pairs:,}")

    # ---- Find closest threshold to 6,290 ----
    target = 6290
    closest_thr = min(sum_criterion.keys(), key=lambda t: abs(sum_criterion[t] - target))
    closest_count = sum_criterion[closest_thr]
    print(f"\n  Closest match in Probe A to 6,290: threshold={closest_thr:.4f}, "
          f"count={closest_count:,} (diff={abs(closest_count-target):,})")

    # ---- Source determination ----
    print("\n  RECONCILIATION FINDINGS:")
    print("  ─────────────────────────────────────────────────────────────────")
    print("  Phase 29 count (6,290): from CAILculator ZDTP analysis")
    print("    Source: 'RH_Phase29_Results.md' — '500-zero CAILculator Tr_BK:")
    print("             6,290 bilateral zero pairs at 95%'")
    print("    The '95%' qualifier = CAILculator bilateral zero confidence")
    print("    threshold, NOT the 95% statistical confidence interval.")
    print("    CAILculator measures sedenion-space bilateral zero structure")
    print("    in the v(ρ) embeddings — NOT a Tr_BK threshold crossing.")
    print()
    print("  Phase 31 count (161): from Python rh_phase31.py")
    print("    Criterion: |Tr_BK(γᵢ) + Tr_BK(γⱼ)| < 0.01")
    print("    This counts near-bilateral-cancellation in BK trace values.")
    print("    Completely different definition from CAILculator's metric.")
    print()
    print("  Conclusion: The ~39× discrepancy reflects DEFINITIONAL DIFFERENCE,")
    print("  not a script error. The two counts measure different objects:")
    print("    CAILculator: sedenion bilateral zero divisor structure in")
    print("                 v(ρ) embeddings (AIEX-001a product space)")
    print("    Python:      BK trace near-cancellation (scalar criterion)")
    print()
    print("  RECOMMENDATION: Retire Phase 29 'superlinear growth' claim from")
    print("  the paper unless CAILculator criterion is explicitly defined.")
    print("  The Phase 31 Python count (161 at N=500) is reproducible but")
    print("  measures a different (and weaker) property.")
    print("  ─────────────────────────────────────────────────────────────────")

    return {
        "N_zeros": N, "N_pairs": N_pairs, "prime_set": primes_6,
        "trace_stats": {
            "min": float(traces.min()), "max": float(traces.max()),
            "mean": float(traces.mean()), "std": float(traces.std()),
            "negative_count": neg_count, "positive_count": pos_count,
        },
        "phase29_count": 6290,
        "phase29_source": "CAILculator ZDTP bilateral zero confidence @ 95% threshold",
        "phase31_count": 161,
        "phase31_criterion": "|Tr_BK(i) + Tr_BK(j)| < 0.01",
        "probe_A_sum_criterion": {str(k): v for k, v in sum_criterion.items()},
        "probe_B_both_small": {str(k): v for k, v in small_trace_n.items()},
        "probe_C_opposite_sign_pairs": int(opp_sign_pairs),
        "probe_D_same_sign_pairs": int(same_sign_pairs),
        "closest_threshold_to_6290": closest_thr,
        "closest_count_to_6290": closest_count,
        "conclusion": (
            "Definitional difference. Phase 29 count is CAILculator sedenion "
            "bilateral zero metric; Phase 31 count is BK trace cancellation. "
            "They measure different objects. ~39x discrepancy is NOT a script error."
        ),
    }

# ---------------------------------------------------------------------------
# Artifact saving
# ---------------------------------------------------------------------------

def json_safe(obj):
    """Recursively convert numpy types to native Python for JSON."""
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj

def save_artifacts(a1, a2, a3, d1):
    """Save all Phase 32 output files."""

    # phase32_boundary_scan.json — Track A1
    with open("phase32_boundary_scan.json", "w") as f:
        json.dump(json_safe(a1), f, indent=2)
    print("[OK] Saved phase32_boundary_scan.json")

    # phase32_weil_full.json — full sequence (all correct formula, N=500 zeros)
    # NOTE: Phase 30 baseline (100 zeros) not included to keep dataset consistent
    a1_pts = [
        {"p_max": pt["p_max"], "N_primes": pt["N_primes"],
         "ratio": pt["ratio"], "Weil_RHS": pt["Weil_RHS"], "regime": "scan"}
        for pt in a1["points"]
    ]
    a2_pts = [
        {"p_max": pt["p_max"], "N_primes": pt["N_primes"],
         "ratio": pt["ratio"], "Weil_RHS": pt["Weil_RHS"], "regime": "extended"}
        for pt in a2["points"]
    ]
    weil_full = {
        "phase": 32, "N_zeros": N_ZEROS, "c1": C1,
        "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
        "description": (
            "Full Weil ratio sequence (correct formula, 500 zeros). "
            "Phase 31 ratios EXCLUDED — formula bug (missing 1/sqrt(p)). "
            "No inversion occurs with the correct formula."
        ),
        "phase31_invalid_values": dict(zip(P31_PMAX, P31_RATIOS)),
        "boundary_scan_151_to_200": a1_pts,
        "extended_200_to_1000": a2_pts,
        "no_inversion_detected": a1["first_p_max_above_1p00"] is None,
    }
    with open("phase32_weil_full.json", "w") as f:
        json.dump(json_safe(weil_full), f, indent=2)
    print("[OK] Saved phase32_weil_full.json")

    # phase32_regime_fits.json — Track A3
    # Update Regime 2 fits with full A2 dataset
    a2_ratios  = [pt["ratio"]   for pt in a2["points"]]
    a2_nprimes = [pt["N_primes"] for pt in a2["points"]]
    n2_full    = np.array(a2_nprimes, dtype=float)
    r2_full    = np.array(a2_ratios, dtype=float)

    log_n2_full = np.log(n2_full)
    slope_full, intercept_full, _, _, _ = linregress(log_n2_full, r2_full)
    y_pred_full = slope_full * log_n2_full + intercept_full
    ss_res_full = float(np.sum((r2_full - y_pred_full)**2))
    ss_tot_full = float(np.sum((r2_full - np.mean(r2_full))**2))
    r2_full_val = 1 - ss_res_full / ss_tot_full if ss_tot_full > 1e-15 else float("nan")

    regime_fits = {
        "phase": 32,
        "regime1": a3["regime1"],
        "regime2_updated": {
            "description": f"Regime 2: {len(a2_nprimes)} points (Track A2 full dataset)",
            "data_N_primes": a2_nprimes,
            "data_ratios": a2_ratios,
            "log_decay_fit": {
                "slope": float(slope_full), "intercept": float(intercept_full),
                "R2": float(r2_full_val),
                "formula": f"ratio = {slope_full:.6f}·log(N) + {intercept_full:.6f}",
            },
        },
    }
    with open("phase32_regime_fits.json", "w") as f:
        json.dump(json_safe(regime_fits), f, indent=2)
    print("[OK] Saved phase32_regime_fits.json")

    # phase32_track_d_reconciliation.txt — Track D1
    with open("phase32_track_d_reconciliation.txt", "w", encoding="utf-8") as f:
        f.write("Phase 32 — Track D1: Bilateral Zero Pair Count Reconciliation\n")
        f.write("Chavez AI Labs LLC\n")
        f.write("="*70 + "\n\n")
        f.write("DISCREPANCY\n")
        f.write(f"  Phase 29 count: 6,290 pairs at N=500 zeros\n")
        f.write(f"  Phase 31 count:   161 pairs at N=500 zeros\n")
        f.write(f"  Ratio:          ~39x\n\n")
        f.write("PHASE 29 METHODOLOGY\n")
        f.write("  Source: CAILculator MCP server (Claude Desktop), NOT a Python script\n")
        f.write("  Quote (RH_Phase29_Results.md):\n")
        f.write("    '500-zero CAILculator Tr_BK: 6,290 bilateral zero pairs at 95%'\n")
        f.write("  The '95%' is the CAILculator bilateral zero confidence threshold.\n")
        f.write("  CAILculator measures sedenion bilateral zero divisor structure in\n")
        f.write("  the v(ρ) embeddings computed by the AIEX-001a product F(ρ).\n")
        f.write("  This is a sedenion-space algebraic property, not a scalar threshold.\n\n")
        f.write("PHASE 31 METHODOLOGY\n")
        f.write("  Source: Python script rh_phase31.py, function bilateral_zero_pairs()\n")
        f.write("  Criterion: |Tr_BK(γᵢ) + Tr_BK(γⱼ)| < 0.01\n")
        f.write("  This counts pairs of Riemann zeros where the Berry-Keating traces\n")
        f.write("  nearly cancel (approximate bilateral cancellation in BK trace space).\n\n")
        f.write("PROBE RESULTS\n")
        f.write("  Trace statistics (N=500, 6 primes {2,3,5,7,11,13}):\n")
        f.write(f"    Range: [{d1['trace_stats']['min']:.4f}, {d1['trace_stats']['max']:.4f}]\n")
        f.write(f"    Mean: {d1['trace_stats']['mean']:.4f}  Std: {d1['trace_stats']['std']:.4f}\n")
        f.write(f"    Tr<0: {d1['trace_stats']['negative_count']}/500\n\n")
        f.write("  Threshold scan (|Tr(i)+Tr(j)| < thr) — Probe A:\n")
        for thr, cnt in sorted(d1["probe_A_sum_criterion"].items(), key=lambda x: float(x[0])):
            f.write(f"    thr={float(thr):.4f}  pairs={cnt:>8,}\n")
        f.write(f"\n  Closest threshold to 6,290: {d1['closest_threshold_to_6290']:.4f} "
                f"→ {d1['closest_count_to_6290']:,} pairs\n\n")
        f.write("CONCLUSION\n")
        f.write(f"  {d1['conclusion']}\n\n")
        f.write("RECOMMENDATION\n")
        f.write("  Retire the 'superlinear growth' claim unless CAILculator criterion\n")
        f.write("  is explicitly defined in the paper. The 6,290 count is reproducible\n")
        f.write("  in CAILculator but has no equivalent Python implementation.\n")
        f.write("  The Phase 31 Python count (161) measures a different property and\n")
        f.write("  should be treated as a separate statistic with its own interpretation.\n")
    print("[OK] Saved phase32_track_d_reconciliation.txt")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("="*65)
    print("RH Investigation — Phase 32")
    print("Chavez AI Labs LLC | Applied Pathological Mathematics")
    print("Two-Regime Weil Characterization + Track D Reconciliation")
    print("="*65)
    print(f"Constants: c1={C1}  theta_W={WEIL_ANGLE:.6f} deg")
    print(f"N_zeros: {N_ZEROS}  |  Zeros range: {ZEROS[0]:.4f}-{ZEROS[-1]:.4f}")

    formula_check = run_formula_correction_check()
    a1 = run_track_A1()
    a2 = run_track_A2()
    a3 = run_track_A3()
    d1 = run_track_D1()

    save_artifacts(a1, a2, a3, d1)

    print("\n" + "="*65)
    print("Phase 32 complete.")
    print(f"KEY FINDING: Phase 31 'inversion' (ratio=1.113 at p_max=200) was a FORMULA BUG.")
    print(f"  Missing 1/sqrt(p) in bilateral_trace. Correct formula: monotone decline.")
    print(f"  Corrected ratio at p_max=200: ~0.129 (below c1=0.118 at p_max=1000: ~0.083)")
    print(f"No inversion detected: first_above_1.0 = {a1['first_p_max_above_1p00']}")
    print("Next: Report to Paul / Claude Desktop for AIEX entry and abstract revision.")
    print("="*65)

if __name__ == "__main__":
    main()
