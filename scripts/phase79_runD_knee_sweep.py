#!/usr/bin/env python3
"""
phase79_runD_knee_sweep.py -- CAIL-RH Investigation, Phase 79 Run D
Chavez AI Labs LLC -- Applied Pathological Mathematics

Run D: Commensurability Knee Sweep.

Tests the C-001 candidate mechanism for the detector decay found in Phase 78:
a p_max-truncated detector's finest oscillation has period 2*pi/log(p_max),
while the mean zero spacing at height t is 2*pi/log(t/2*pi). Setting the two
periods equal predicts that a detector truncated at p_max loses discrimination
at height gamma ~= 2*pi*p_max -- a one-parameter prediction with no free
constants.

This script measures, for seven prime truncations (p_max = 7,11,13,17,19,23,29)
plus two control arms, local ROC AUC (primary) and amplitude-normalized T1
(secondary) in sliding windows of zeros, fits a two-segment (broken-stick)
regression of AUC against height for each arm, bootstraps a CI on the
breakpoint, and tests whether the seven fitted breakpoints scale linearly
with p_max with slope 2*pi.

Reused verbatim (per the handoff's explicit instruction not to reimplement):
roc_auc, local_maxima, peak_matching, t1_value_at_zeros, all copied from
phase78_q18_candidate1_per_gateway.py. The gateway-realized identity check for
arms C/E reuses the PATTERNS/U/c_channel/encoding_batch closed-form from
phase78_q18_runC_high_zeros.py -- this is the Gateway Linear Law, validated
22/22 against live CAILculator in Phase 76, not a fresh live MCP call (same
convention the Phase 78 scripts already use for "gateway-realized" figures).

Methodological caveat (record this in any writeup): the two-segment vs.
single-segment F-test's p-value does not correct for the breakpoint location
being chosen by grid search (the Davies 1987 problem) -- it is an approximate,
liberal indicator, not a corrected significance test. The bootstrap CI on the
breakpoint (2,000 resamples over windows) is the primary evidence for a knee;
report it, not the p-value alone. This is a different procedure from the
permutation-null Monte-Carlo p-values elsewhere in the corpus (see C-007/C-008)
and must not be conflated with them -- no Monte-Carlo null is used anywhere in
this script; AUC and the bootstrap CI are computed directly from the data.

See rh-phase79-runD-claude-code-handoff.md for the full spec.

Outputs:
  ../results/phase79_runD_results.json      -- per-arm, per-window measurements
  ../results/phase79_runD_slope_fit.json    -- the fitted breakpoints + slope fit
"""
import bisect
import json
import math

import numpy as np
from scipy import stats as sstats

SEED = 20260612
TWO_PI = 2.0 * math.pi

# ---------------------------------------------------------------------------
# Reused verbatim from phase78_q18_candidate1_per_gateway.py
# ---------------------------------------------------------------------------

def t1_value_at_zeros(T, Y, zeros, n_trials=5000, seed=SEED):
    rng = np.random.default_rng(seed)
    obs = float(np.mean(np.interp(zeros, T, Y)))
    null = np.array([
        np.mean(np.interp(rng.uniform(T[0], T[-1], len(zeros)), T, Y))
        for _ in range(n_trials)])
    z = float((obs - null.mean()) / null.std())
    p_two = float(min(1.0, 2 * min(np.mean(null <= obs), np.mean(null >= obs))))
    return {"n_zeros": len(zeros), "observed": obs, "null_mean": float(null.mean()),
            "null_std": float(null.std()), "z": z, "p_two_sided": p_two}


def roc_auc(T, Y, zeros, delta):
    zarr = np.asarray(zeros)
    dist = np.min(np.abs(T[:, None] - zarr[None, :]), axis=1)
    pos = Y[dist < delta]
    neg = Y[dist >= delta]
    ranks = np.argsort(np.argsort(np.concatenate([pos, neg]))) + 1
    r_pos = ranks[:len(pos)].sum()
    auc = (r_pos - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))
    return {"delta": delta, "n_pos": int(len(pos)), "n_neg": int(len(neg)), "auc": float(auc)}


def local_maxima(T, Y):
    idx = np.where((Y[1:-1] > Y[:-2]) & (Y[1:-1] > Y[2:]))[0] + 1
    return T[idx], Y[idx]


def peak_matching(T, Y, zeros, eps):
    pt, pv = local_maxima(T, Y)
    order = np.argsort(-pv)
    zarr = np.asarray(zeros)
    best = {"f1": 0.0}
    for k in range(1, len(order) + 1):
        sel = np.sort(pt[order[:k]])
        used = np.zeros(len(zarr), bool)
        tp = 0
        for p in sel:
            d = np.abs(zarr - p)
            d[used] = np.inf
            j = int(np.argmin(d))
            if d[j] < eps:
                used[j] = True
                tp += 1
        prec = tp / k
        rec = tp / len(zarr)
        f1 = 2 * prec * rec / (prec + rec) if prec + rec > 0 else 0.0
        if f1 > best["f1"]:
            best = {"f1": f1, "precision": prec, "recall": rec, "n_predictions": k}
    return {"eps": eps, "n_maxima": int(len(pt)), "best": best}


# ---------------------------------------------------------------------------
# Explicit-formula detector family (Run D's primary detector form)
# ---------------------------------------------------------------------------

def w_freq(q):
    """w_q = log(q)/sqrt(q). Computed from the formula every time (C-006)."""
    return math.log(q) / math.sqrt(q)


def explicit_detector(T, freqs):
    D = np.zeros_like(T)
    for q in freqs:
        D = D - 2.0 * w_freq(q) * np.cos(T * math.log(q))
    return D


ARMS = {
    "A": {"p_max": 7,  "freqs": (2, 3, 5, 7)},
    "B": {"p_max": 11, "freqs": (2, 3, 5, 7, 11)},
    "C": {"p_max": 13, "freqs": (2, 3, 5, 7, 11, 13)},
    "D": {"p_max": 17, "freqs": (2, 3, 5, 7, 11, 13, 17)},
    "E": {"p_max": 19, "freqs": (2, 3, 5, 7, 11, 13, 17, 19)},
    "F": {"p_max": 23, "freqs": (2, 3, 5, 7, 11, 13, 17, 19, 23)},
    "G": {"p_max": 29, "freqs": (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)},
}

CONTROLS = {
    "term_count": {
        "p_max": 13, "freqs": (2, 5, 7, 11, 13),
        "note": "arm C minus p=3; same max frequency (log 13), one fewer term. "
                "Prediction: knee should NOT move from arm C's.",
    },
    "nonprime": {
        "p_max": 15, "freqs": (2, 3, 5, 7, 11, 15),
        "note": "arm C with p=13 replaced by non-prime q=15; max frequency "
                "moves from log 13 to log 15. Prediction: knee moves to 2*pi*15.",
    },
}


# ---------------------------------------------------------------------------
# Gateway-realized identity check (arms C and E only; C-009 naming)
# ---------------------------------------------------------------------------

def gateway_identity_check(T):
    LN = {p: math.log(p) for p in (2, 3, 5, 7, 11, 13, 17, 19)}
    W = {p: math.log(p) / math.sqrt(p) for p in (2, 3, 5, 7, 11, 13, 17, 19)}

    def vec(*pairs, n=16):
        v = np.zeros(n)
        for i, val in pairs:
            v[i] = val
        return v

    PATTERNS = {
        2: (vec((3, 1), (12, 1)), vec((5, 1), (10, 1))),
        3: (vec((4, 1), (11, 1)), vec((6, 1), (9, 1))),
        6: (vec((2, 1), (13, -1)), vec((6, 1), (9, 1))),
    }
    U = {g: P + Q for g, (P, Q) in PATTERNS.items()}

    def encoding_batch(sigma, T, with_higher_primes):
        X = np.zeros((len(T), 16))
        X[:, 0] = sigma
        X[:, 1] = T
        X[:, 3] = W[2] * np.cos(T * LN[2])
        X[:, 5] = W[3] * np.cos(T * LN[3])
        X[:, 10] = W[11] * np.cos(T * LN[11])
        X[:, 12] = W[13] * np.cos(T * LN[13])
        X[:, 6] = W[5] * np.cos(T * LN[5])
        X[:, 9] = W[7] * np.cos(T * LN[7])
        if with_higher_primes:
            X[:, 4] = W[17] * np.cos(T * LN[17])
            X[:, 11] = W[19] * np.cos(T * LN[19])
        return X

    def c_channel(X, g):
        return -2.0 * X @ U[g]

    X6 = encoding_batch(0.5, T, False)
    X8 = encoding_batch(0.5, T, True)
    base6_gateway = c_channel(X6, 2) + c_channel(X6, 6)
    ext8_gateway = c_channel(X8, 2) + c_channel(X8, 3)
    base6_explicit = explicit_detector(T, (2, 3, 5, 7, 11, 13))
    ext8_explicit = explicit_detector(T, (2, 3, 5, 7, 11, 13, 17, 19))
    f6_identity = float(np.max(np.abs(base6_gateway - base6_explicit)))
    f8_identity = float(np.max(np.abs(ext8_gateway - ext8_explicit)))
    return {"f6_identity_residual": f6_identity, "f8_identity_residual": f8_identity}


# ---------------------------------------------------------------------------
# Windowed local measurement
# ---------------------------------------------------------------------------

def local_t1_normalized(Tloc, Yloc, window_zeros, eps):
    rms = float(np.sqrt(np.mean(Yloc ** 2))) if len(Yloc) else float("nan")
    peaks = []
    for z in window_zeros:
        m = np.abs(Tloc - z) < eps
        if np.any(m):
            peaks.append(float(np.max(np.abs(Yloc[m]))))
    mean_peak = float(np.mean(peaks)) if peaks else float("nan")
    t1n = mean_peak / rms if (rms and rms > 0 and np.isfinite(mean_peak)) else float("nan")
    return {"t1_mean_peak": mean_peak, "t1_rms": rms, "t1_normalized": t1n,
            "t1_n_zeros_matched": len(peaks)}


def sliding_windows(zin, width, step):
    windows = []
    i = 0
    while i + width <= len(zin):
        windows.append(zin[i:i + width])
        i += step
    return windows


def measure_arm(T, Y, zin, width, step, margin_mult=3.0, deltas=(0.25, 0.5), eps=0.5):
    rows = []
    for wz in sliding_windows(zin, width, step):
        w0, w1 = wz[0], wz[-1]
        mean_gap = (w1 - w0) / (len(wz) - 1)
        buf = margin_mult * mean_gap
        lo, hi = w0 - buf, w1 + buf
        i0 = np.searchsorted(T, lo, side="left")
        i1 = np.searchsorted(T, hi, side="right")
        Tloc, Yloc = T[i0:i1], Y[i0:i1]
        if len(Tloc) == 0:
            continue
        lo_idx = bisect.bisect_left(zin, lo)
        hi_idx = bisect.bisect_right(zin, hi)
        zloc = zin[lo_idx:hi_idx]
        if len(zloc) == 0:
            continue
        row = {"gamma_center": float(np.mean(wz)), "gamma_lo": float(w0), "gamma_hi": float(w1),
               "n_zeros_window": len(wz), "n_zeros_local": len(zloc),
               "local_range": [float(lo), float(hi)]}
        for d in deltas:
            r = roc_auc(Tloc, Yloc, zloc, d)
            row[f"auc_delta{d}"] = r["auc"]
        row.update(local_t1_normalized(Tloc, Yloc, wz, eps=eps))
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# Segmented (two-segment / broken-stick) regression, fully vectorized over
# candidate breakpoints via closed-form 3x3 normal-equation solve (Cramer's
# rule), so a 2,000-resample bootstrap is cheap.
# ---------------------------------------------------------------------------

def fit_single_segment(g, y):
    n = len(g)
    X = np.column_stack([np.ones(n), g])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    rss = float(np.sum((y - X @ coef) ** 2))
    return rss, coef.tolist()


def fit_two_segment_vec(g, y, candidates):
    S00 = float(len(g))
    S01 = float(g.sum())
    S11 = float((g * g).sum())
    S0y = float(y.sum())
    S1y = float((g * y).sum())
    Syy = float((y * y).sum())

    H = np.clip(g[:, None] - candidates[None, :], 0.0, None)   # (n, ncand)
    S0h = H.sum(axis=0)
    S1h = g @ H
    Shh = np.einsum("ij,ij->j", H, H)
    Shy = y @ H

    a11, a12, a13 = S00, S01, S0h
    a21, a22, a23 = S01, S11, S1h
    a31, a32, a33 = S0h, S1h, Shh
    b1, b2, b3 = S0y, S1y, Shy

    det = a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)
    valid = np.abs(det) > 1e-9
    det_safe = np.where(valid, det, 1.0)

    detA = b1 * (a22 * a33 - a23 * a32) - a12 * (b2 * a33 - a23 * b3) + a13 * (b2 * a32 - a22 * b3)
    detB = a11 * (b2 * a33 - a23 * b3) - b1 * (a21 * a33 - a23 * a31) + a13 * (a21 * b3 - b2 * a31)
    detC = a11 * (a22 * b3 - b2 * a32) - a12 * (a21 * b3 - b2 * a31) + b1 * (a21 * a32 - a22 * a31)

    a_coef = detA / det_safe
    b_coef = detB / det_safe
    c_coef = detC / det_safe

    rss = Syy - (a_coef * S0y + b_coef * S1y + c_coef * Shy)
    rss = np.where(valid & (rss >= -1e-9), np.clip(rss, 0.0, None), np.inf)

    k = int(np.argmin(rss))
    return {"rss": float(rss[k]), "breakpoint": float(candidates[k]),
            "coef": [float(a_coef[k]), float(b_coef[k]), float(c_coef[k])]}


def segmented_test(gamma_arr, y_arr, min_pts=4, n_grid=60):
    order = np.argsort(gamma_arr)
    g, y = gamma_arr[order], y_arr[order]
    n = len(g)
    if n < 2 * min_pts + 2:
        rss0, coef0 = fit_single_segment(g, y)
        return {"status": "insufficient_points", "n_windows": n,
                "linear": {"rss": rss0, "coef": coef0}}
    lo_bp, hi_bp = float(g[min_pts]), float(g[-min_pts - 1])
    if hi_bp <= lo_bp:
        rss0, coef0 = fit_single_segment(g, y)
        return {"status": "insufficient_points", "n_windows": n,
                "linear": {"rss": rss0, "coef": coef0}}
    candidates = np.linspace(lo_bp, hi_bp, n_grid)
    two = fit_two_segment_vec(g, y, candidates)
    rss0, coef0 = fit_single_segment(g, y)
    dof0, dof1 = n - 2, n - 4
    if dof1 <= 0:
        return {"status": "insufficient_points", "n_windows": n,
                "linear": {"rss": rss0, "coef": coef0}}
    if not np.isfinite(two["rss"]) or two["rss"] <= 0:
        f_stat, p_value = float("inf"), 0.0
    else:
        f_stat = ((rss0 - two["rss"]) / (dof0 - dof1)) / (two["rss"] / dof1)
        p_value = float(sstats.f.sf(f_stat, dof0 - dof1, dof1)) if f_stat > 0 else 1.0
    tol = 0.02 * (hi_bp - lo_bp)
    boundary_hit = bool(two["breakpoint"] <= lo_bp + tol or two["breakpoint"] >= hi_bp - tol)
    knee_detected = bool((p_value < 0.05) and not boundary_hit)
    return {
        "status": "fit", "n_windows": n, "search_range": [lo_bp, hi_bp], "n_grid": n_grid,
        "linear": {"rss": rss0, "coef": coef0, "dof": dof0},
        "two_segment": {**two, "dof": dof1},
        "f_stat": float(f_stat), "p_value": p_value,
        "boundary_hit": boundary_hit, "knee_detected": knee_detected,
        "note": "p_value is an uncorrected (Davies-problem) indicator; the "
                "bootstrap CI is the primary evidence, not this p-value.",
    }


def bootstrap_breakpoint(gamma_arr, y_arr, n_boot=2000, min_pts=4, n_grid=60, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(gamma_arr)
    bps, s1s, s2s = [], [], []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        g_b, y_b = gamma_arr[idx], y_arr[idx]
        order = np.argsort(g_b)
        g_b, y_b = g_b[order], y_b[order]
        if n < 2 * min_pts + 2:
            continue
        lo_bp, hi_bp = float(g_b[min_pts]), float(g_b[-min_pts - 1])
        if hi_bp <= lo_bp:
            continue
        candidates = np.linspace(lo_bp, hi_bp, n_grid)
        two = fit_two_segment_vec(g_b, y_b, candidates)
        if not np.isfinite(two["rss"]):
            continue
        bps.append(two["breakpoint"])
        s1s.append(two["coef"][1])
        s2s.append(two["coef"][1] + two["coef"][2])
    bps_arr = np.array(bps)
    out = {"n_boot": n_boot, "n_success": int(len(bps_arr)), "seed": seed}
    if len(bps_arr) >= 20:
        out.update({
            "breakpoint_median": float(np.median(bps_arr)),
            "breakpoint_ci95": [float(np.percentile(bps_arr, 2.5)), float(np.percentile(bps_arr, 97.5))],
            "slope_pre_ci95": [float(np.percentile(s1s, 2.5)), float(np.percentile(s1s, 97.5))],
            "slope_post_ci95": [float(np.percentile(s2s, 2.5)), float(np.percentile(s2s, 97.5))],
            "bootstrap_breakpoints": bps_arr.tolist(),
        })
    else:
        out["status"] = "bootstrap_failed_insufficient_successes"
    return out


# ---------------------------------------------------------------------------
# Per-arm driver
# ---------------------------------------------------------------------------

def run_arm(T, zin, freqs, p_max, width, step, n_boot=2000, n_grid=60):
    Y = explicit_detector(T, freqs)
    windows = measure_arm(T, Y, zin, width=width, step=step)
    gamma_arr = np.array([r["gamma_center"] for r in windows])
    auc_arr = np.array([r["auc_delta0.5"] for r in windows])
    t1_arr = np.array([r["t1_normalized"] for r in windows])
    seg = segmented_test(gamma_arr, auc_arr)
    boot = bootstrap_breakpoint(gamma_arr, auc_arr, n_boot=n_boot, n_grid=n_grid)
    # Secondary channel (amplitude-normalized T1), reported alongside AUC but
    # not used to drive the primary breakpoint/slope-vs-p_max conclusion.
    finite = np.isfinite(t1_arr)
    seg_t1 = segmented_test(gamma_arr[finite], t1_arr[finite]) if finite.sum() >= 10 else \
        {"status": "insufficient_points"}
    boot_t1 = (bootstrap_breakpoint(gamma_arr[finite], t1_arr[finite], n_boot=n_boot, n_grid=n_grid)
               if finite.sum() >= 10 else {"status": "insufficient_points"})
    return {
        "p_max": p_max, "freqs": list(freqs), "predicted_knee": TWO_PI * p_max,
        "n_windows": len(windows), "windows": windows,
        "segmented_fit": seg, "bootstrap": boot,
        "segmented_fit_t1_secondary": seg_t1, "bootstrap_t1_secondary": boot_t1,
    }


# ---------------------------------------------------------------------------
# Model-free reach measure: first sustained crossing of a FIXED AUC threshold
# (same absolute threshold for every arm), vs. the segmented-regression
# breakpoint above (which is a fitted, model-dependent quantity). Requested
# as a referee-facing cross-check that doesn't depend on the two-segment
# model at all: sort windows by height, find the first run of `min_run`
# consecutive windows all below `threshold`, report that run's first gamma.
# Right-censoring (an arm's AUC never sustains a drop below threshold within
# the observed range) is a valid, reportable outcome, not a fit failure.
# ---------------------------------------------------------------------------

def threshold_crossing(gamma_arr, y_arr, threshold, min_run=3):
    order = np.argsort(gamma_arr)
    g, y = gamma_arr[order], y_arr[order]
    below = y < threshold
    for i in range(len(g) - min_run + 1):
        if below[i:i + min_run].all():
            return float(g[i])
    return None


def bootstrap_threshold_crossing(gamma_arr, y_arr, threshold, n_boot=2000, min_run=3, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(gamma_arr)
    crossings = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        c = threshold_crossing(gamma_arr[idx], y_arr[idx], threshold, min_run)
        if c is not None:
            crossings.append(c)
    arr = np.array(crossings)
    out = {"n_boot": n_boot, "n_success": int(len(arr)), "threshold": threshold, "min_run": min_run}
    if len(arr) >= 20:
        out["median"] = float(np.median(arr))
        out["ci95"] = [float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))]
        out["bootstrap_crossings"] = arr.tolist()
    return out


def arm_usable_for_slope(arm_result):
    seg = arm_result["segmented_fit"]
    boot = arm_result["bootstrap"]
    if seg.get("status") != "fit":
        return False
    if seg.get("boundary_hit"):
        return False
    if boot.get("n_success", 0) < 20:
        return False
    return True


def nested_slope_fit(arm_points, n_draws=2000, seed=SEED):
    rng = np.random.default_rng(seed)
    pmax_arr = np.array([p["p_max"] for p in arm_points], dtype=float)
    bp_point = np.array([p["breakpoint_point"] for p in arm_points], dtype=float)
    slope0, intercept0 = np.polyfit(pmax_arr, bp_point, 1)
    resid = bp_point - (slope0 * pmax_arr + intercept0)
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((bp_point - bp_point.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    boot_arrays = [np.array(p["bootstrap_breakpoints"]) for p in arm_points]
    slopes, intercepts = [], []
    for _ in range(n_draws):
        bp_draw = np.array([rng.choice(b) for b in boot_arrays])
        s, i = np.polyfit(pmax_arr, bp_draw, 1)
        slopes.append(s)
        intercepts.append(i)
    slopes = np.array(slopes)
    intercepts = np.array(intercepts)
    slope_ci = [float(np.percentile(slopes, 2.5)), float(np.percentile(slopes, 97.5))]
    intercept_ci = [float(np.percentile(intercepts, 2.5)), float(np.percentile(intercepts, 97.5))]
    return {
        "arms": [p["arm"] for p in arm_points],
        "p_max": pmax_arr.tolist(), "breakpoint_point": bp_point.tolist(),
        "slope": float(slope0), "intercept": float(intercept0), "r2": float(r2),
        "slope_ci95": slope_ci, "intercept_ci95": intercept_ci,
        "predicted_slope_2pi": TWO_PI,
        "slope_ci_contains_2pi": bool(slope_ci[0] <= TWO_PI <= slope_ci[1]),
        "intercept_ci_contains_zero": bool(intercept_ci[0] <= 0.0 <= intercept_ci[1]),
        "n_draws": n_draws, "seed": seed,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    zeros_all = json.load(open("../data/riemann/rh_zeros.json"))
    T_LO, T_HI, DT = 10.0, 600.0, 0.005
    T = np.arange(T_LO, T_HI + DT / 2, DT)
    zin = [z for z in zeros_all if T_LO + 1 < z < T_HI - 1]
    print(f"grid: {len(T)} pts in [{T_LO},{T_HI}]; zeros in range: {len(zin)} "
          f"(gamma_1={zin[0]:.3f} .. gamma_{len(zin)}={zin[-1]:.3f})")

    results = {
        "phase": "79", "run": "D",
        "grid": {"t_lo": T_LO, "t_hi": T_HI, "dt": DT, "n": int(len(T))},
        "zeros_source": "../data/riemann/rh_zeros.json",
        "zeros_in_range": len(zin), "gamma_last": zin[-1],
    }

    # ---- 0. Pilot: window width choice, on arm C only ------------------------
    # The handoff's suggested default (width=40, step=10) turned out to be far
    # too coarse: zero density in the predicted-knee region (gamma 44-182) is
    # low enough that EVERY arm's predicted knee falls inside the first ~1-2
    # windows out of 31 (e.g. arm C has only 21 zeros below its own predicted
    # knee of 81.7 -- barely half of one 40-zero window). At width>=30 the
    # segmented fit degenerates: breakpoint search hits the interior-candidate
    # boundary and the bootstrap CI spans nearly the whole domain. A wider
    # pilot grid (10-40 zeros/window) is run here to find where the fit
    # actually stabilizes before committing to a width for all nine series.
    print("\n=== 0. PILOT: window width on arm C ===")
    pilot = {}
    Y_C = explicit_detector(T, ARMS["C"]["freqs"])
    for width, step in ((10, 5), (15, 5), (20, 5), (25, 5), (30, 10), (40, 10)):
        windows = measure_arm(T, Y_C, zin, width=width, step=step)
        gamma_arr = np.array([r["gamma_center"] for r in windows])
        auc_arr = np.array([r["auc_delta0.5"] for r in windows])
        seg = segmented_test(gamma_arr, auc_arr)
        boot = bootstrap_breakpoint(gamma_arr, auc_arr, n_boot=300, n_grid=60)
        ci_width = (boot["breakpoint_ci95"][1] - boot["breakpoint_ci95"][0]
                    if "breakpoint_ci95" in boot else float("inf"))
        pilot[str(width)] = {
            "n_windows": len(windows), "step": step, "p_value": seg.get("p_value"),
            "knee_detected": seg.get("knee_detected"), "boundary_hit": seg.get("boundary_hit"),
            "breakpoint_point": seg.get("two_segment", {}).get("breakpoint"),
            "breakpoint_ci95_pilot300": boot.get("breakpoint_ci95"),
            "ci95_width_pilot300": ci_width,
        }
        print(f"  width={width:2d} step={step}: n_windows={len(windows):3d} "
              f"bp={seg.get('two_segment', {}).get('breakpoint', float('nan')):7.2f} "
              f"p={seg.get('p_value', float('nan')):.4f} "
              f"knee_detected={seg.get('knee_detected')} "
              f"boundary_hit={seg.get('boundary_hit')} ci95_width(300boot)={ci_width:.2f}")
    CHOSEN_WIDTH, CHOSEN_STEP = 20, 5
    print(f"  chosen width={CHOSEN_WIDTH}, step={CHOSEN_STEP} -- deviates from the "
          f"handoff-suggested 40/10 default; chosen because width>=30 hits the "
          f"boundary_hit degeneracy above (documented in pilot table) while "
          f"width=20 gives the clearest interior, non-boundary knee (lowest "
          f"p-value among non-degenerate widths) on arm C.")
    results["window_design"] = {
        "pilot": pilot, "chosen_width": CHOSEN_WIDTH, "chosen_step": CHOSEN_STEP,
        "local_margin_mult": 3.0, "auc_delta_primary": 0.5, "t1_eps": 0.5,
        "n_grid_breakpoint_search": 60, "n_boot_full": 2000,
    }

    # ---- 1. Seven arms ---------------------------------------------------
    print("\n=== 1. SEVEN-ARM SWEEP (full width/step, n_boot=2000) ===")
    results["arms"] = {}
    for name, spec in ARMS.items():
        print(f"  arm {name}: p_max={spec['p_max']}, primes={spec['freqs']}")
        r = run_arm(T, zin, spec["freqs"], spec["p_max"], CHOSEN_WIDTH, CHOSEN_STEP)
        results["arms"][name] = r
        seg, boot = r["segmented_fit"], r["bootstrap"]
        bp = seg.get("two_segment", {}).get("breakpoint")
        ci = boot.get("breakpoint_ci95")
        print(f"    predicted knee = {r['predicted_knee']:7.2f}   "
              f"fitted bp = {bp if bp is None else round(bp, 2)}   "
              f"boot CI95 = {ci}   knee_detected={seg.get('knee_detected')}   "
              f"boundary_hit={seg.get('boundary_hit')}")

    # ---- 2. Control arms ---------------------------------------------------
    print("\n=== 2. CONTROL ARMS ===")
    results["controls"] = {}
    for name, spec in CONTROLS.items():
        print(f"  control {name}: freqs={spec['freqs']}  ({spec['note']})")
        r = run_arm(T, zin, spec["freqs"], spec["p_max"], CHOSEN_WIDTH, CHOSEN_STEP)
        r["note"] = spec["note"]
        results["controls"][name] = r
        seg, boot = r["segmented_fit"], r["bootstrap"]
        bp = seg.get("two_segment", {}).get("breakpoint")
        ci = boot.get("breakpoint_ci95")
        print(f"    predicted knee = {r['predicted_knee']:7.2f}   "
              f"fitted bp = {bp if bp is None else round(bp, 2)}   boot CI95 = {ci}")

    # ---- 3. Gateway identity check (arms C, E only; C-009 naming) ---------
    print("\n=== 3. GATEWAY IDENTITY CHECK (arms C, E) ===")
    identity = gateway_identity_check(T)
    results["identity_checks"] = identity
    print(f"  f6_identity_residual = {identity['f6_identity_residual']:.3e}")
    print(f"  f8_identity_residual = {identity['f8_identity_residual']:.3e}")

    with open("../results/phase79_runD_results.json", "w") as fh:
        json.dump(results, fh, indent=2, default=float)
    print("\nwrote ../results/phase79_runD_results.json")

    # ---- 4. Slope fit across the seven arms --------------------------------
    print("\n=== 4. SLOPE FIT: breakpoint vs. p_max ===")
    arm_points = []
    excluded = []
    for name in ARMS:
        r = results["arms"][name]
        if arm_usable_for_slope(r):
            arm_points.append({
                "arm": name, "p_max": r["p_max"],
                "breakpoint_point": r["segmented_fit"]["two_segment"]["breakpoint"],
                "bootstrap_breakpoints": r["bootstrap"]["bootstrap_breakpoints"],
            })
        else:
            excluded.append(name)
            print(f"  arm {name}: EXCLUDED from slope fit (measurement-limited: "
                  f"status={r['segmented_fit'].get('status')}, "
                  f"boundary_hit={r['segmented_fit'].get('boundary_hit')}, "
                  f"boot_n_success={r['bootstrap'].get('n_success')})")

    slope_fit = {"arms_used": [p["arm"] for p in arm_points], "arms_excluded": excluded}
    if len(arm_points) >= 3:
        fit = nested_slope_fit(arm_points, n_draws=2000, seed=SEED)
        slope_fit.update(fit)
        print(f"  slope = {fit['slope']:.4f}  CI95={fit['slope_ci95']}  "
              f"(predicted 2*pi = {TWO_PI:.4f})")
        print(f"  intercept = {fit['intercept']:.4f}  CI95={fit['intercept_ci95']}")
        print(f"  R^2 = {fit['r2']:.4f}")
        print(f"  slope CI contains 2*pi: {fit['slope_ci_contains_2pi']}")
        print(f"  intercept CI contains 0: {fit['intercept_ci_contains_zero']}")
    else:
        slope_fit["status"] = "insufficient_usable_arms"
        print("  INSUFFICIENT usable arms for a slope fit.")

    # controls: report knee comparison vs arm C
    arm_c_bp = results["arms"]["C"]["segmented_fit"].get("two_segment", {}).get("breakpoint")
    controls_report = {}
    for name in CONTROLS:
        r = results["controls"][name]
        controls_report[name] = {
            "predicted_knee": r["predicted_knee"],
            "fitted_breakpoint": r["segmented_fit"].get("two_segment", {}).get("breakpoint"),
            "boot_ci95": r["bootstrap"].get("breakpoint_ci95"),
            "arm_C_breakpoint_for_comparison": arm_c_bp,
        }
    slope_fit["controls"] = controls_report
    print("\n  Controls vs. arm C breakpoint (%s):" % arm_c_bp)
    for name, c in controls_report.items():
        print(f"    {name}: predicted={c['predicted_knee']:.2f} fitted={c['fitted_breakpoint']} "
              f"CI95={c['boot_ci95']}")

    # ---- 5. Model-free reach: first sustained crossing of a fixed AUC ------
    # threshold, vs. p_max. Does not depend on the segmented-regression model
    # rejected in step 4 -- a direct, referee-facing cross-check. Run as a
    # SWEEP over threshold, not a single choice: the first pass at a single
    # threshold (0.85) showed a real, high-R^2 positive slope, but a second
    # threshold (0.90) gave a materially different slope -- so the honest
    # report is the full sensitivity curve, not one number.
    print("\n=== 5. MODEL-FREE REACH: threshold-crossing sensitivity sweep ===")
    MIN_RUN = 3
    THRESHOLDS = [0.78, 0.80, 0.82, 0.84, 0.85, 0.86, 0.88, 0.90, 0.92, 0.94]
    reach = {"min_run": MIN_RUN, "thresholds": THRESHOLDS, "n_boot": 2000, "by_threshold": {}}
    print(f"  {'thresh':>7s} {'n_censored':>10s} {'slope':>8s} {'ci_lo':>8s} {'ci_hi':>8s} "
          f"{'R2':>6s} {'contains_2pi':>12s}")
    for thresh in THRESHOLDS:
        by_arm = {}
        pts = []
        for name in ARMS:
            r = results["arms"][name]
            gamma_arr = np.array([w["gamma_center"] for w in r["windows"]])
            auc_arr = np.array([w["auc_delta0.5"] for w in r["windows"]])
            point = threshold_crossing(gamma_arr, auc_arr, thresh, MIN_RUN)
            boot = bootstrap_threshold_crossing(gamma_arr, auc_arr, thresh, n_boot=2000, min_run=MIN_RUN)
            by_arm[name] = {"p_max": r["p_max"], "crossing_point": point, "bootstrap": boot}
            if point is not None and boot.get("n_success", 0) >= 20:
                pts.append({"arm": name, "p_max": r["p_max"], "breakpoint_point": point,
                            "bootstrap_breakpoints": boot["bootstrap_crossings"]})
        censored = [name for name in ARMS if name not in [p["arm"] for p in pts]]
        entry = {"by_arm": by_arm, "arms_used": [p["arm"] for p in pts], "arms_censored": censored}
        if len(pts) >= 4:
            fit = nested_slope_fit(pts, n_draws=2000, seed=SEED)
            entry["slope_fit"] = fit
            print(f"  {thresh:7.2f} {len(censored):10d} {fit['slope']:8.2f} "
                  f"{fit['slope_ci95'][0]:8.2f} {fit['slope_ci95'][1]:8.2f} {fit['r2']:6.3f} "
                  f"{str(fit['slope_ci_contains_2pi']):>12s}")
        else:
            entry["slope_fit"] = {"status": "insufficient_usable_arms", "n_usable": len(pts)}
            print(f"  {thresh:7.2f} {len(censored):10d}   too few usable arms ({len(pts)})")
        reach["by_threshold"][str(thresh)] = entry

    slope_fit["reach_threshold_crossing"] = reach

    with open("../results/phase79_runD_slope_fit.json", "w") as fh:
        json.dump(slope_fit, fh, indent=2, default=float)
    print("\nwrote ../results/phase79_runD_slope_fit.json")
