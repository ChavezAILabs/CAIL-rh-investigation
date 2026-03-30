"""
rh_phase34.py — Phase 34: c1 Asymptote Test + 2D Surface Fit
Chavez AI Labs LLC | Applied Pathological Mathematics
Paul Chavez | 2026-03-27

Tracks:
  V1  — Formula verification (always first)
  E0  — dps=15 vs dps=25 sanity check
  E1  — 6-prime ratio at N_zeros up to 10000 (c1 asymptote test)
  E2  — 36-prime and 62-prime asymptote comparison
  S1  — Characterize a(N_p) and b(N_p) over 6 prime sets
  S2  — Surface reconstruction and residuals
  B1  — b(N_p) Weyl equidistribution hypothesis test
  P1  — Exact c1 Euler product probe
  P2  — 6-prime Weil truncation fraction
"""

import sys
import json
import math
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

C1   = 0.11797805192095003   # sin(theta_W)
C3   = 0.99301620292165280   # cos(theta_W)
THETA_W_DEG = math.degrees(math.asin(C1))

print("=" * 65)
print("RH Investigation - Phase 34")
print("Chavez AI Labs LLC | Applied Pathological Mathematics")
print("c1 Asymptote Test + 2D Surface Fit")
print("=" * 65)
print(f"c1={C1}  theta_W={THETA_W_DEG:.6f} deg")

# ─────────────────────────────────────────────────────────────────────────────
# Load zeros
# ─────────────────────────────────────────────────────────────────────────────

def load_zeros(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):
        return np.array(data, dtype=float)
    for key in ("zeros", "imaginary_parts", "values"):
        if key in data:
            return np.array(data[key], dtype=float)
    raise ValueError(f"Cannot parse zeros from {path}")

ZEROS_25 = load_zeros("rh_zeros.json")       # 1000 zeros, dps=25
ZEROS_10K = load_zeros("rh_zeros_10k.json")  # 10000 zeros, dps=15
N_25  = len(ZEROS_25)
N_10K = len(ZEROS_10K)
print(f"Zeros (dps=25): {N_25}  range {ZEROS_25[0]:.4f}-{ZEROS_25[-1]:.4f}")
print(f"Zeros (dps=15): {N_10K}  range {ZEROS_10K[0]:.4f}-{ZEROS_10K[-1]:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# Prime helpers
# ─────────────────────────────────────────────────────────────────────────────

def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i in range(2, n+1) if sieve[i]]

def first_n_primes(n):
    # Generate enough primes; use sieve up to n*log(n*log(n))+10 (upper bound)
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n))) * 1.5) + 20
    ps = primes_up_to(limit)
    while len(ps) < n:
        limit *= 2
        ps = primes_up_to(limit)
    return ps[:n]

# Define the 6 canonical prime sets from Phase 33/34 spec
PRIME_SETS = {
    "6p_pmax13":   np.array(primes_up_to(13),  dtype=float),
    "15p_pmax47":  np.array(primes_up_to(47),  dtype=float),
    "36p_pmax151": np.array(primes_up_to(151), dtype=float),
    "62p_pmax300": np.array(primes_up_to(300), dtype=float),
    "95p_pmax499": np.array(primes_up_to(499), dtype=float),
    "168p_pmax1000": np.array(primes_up_to(1000), dtype=float),
}
print(f"\nPrime set sizes: {[(k, len(v)) for k, v in PRIME_SETS.items()]}")

# ─────────────────────────────────────────────────────────────────────────────
# Core BK computation (vectorized)
# ─────────────────────────────────────────────────────────────────────────────

def weil_rhs(primes):
    p = np.asarray(primes, dtype=float)
    return float(-np.sum(np.log(p) / np.sqrt(p)))

def compute_ratio(primes, zeros_arr):
    """Compute Weil ratio for given prime set and zero array."""
    p    = np.asarray(primes, dtype=float)
    log_p = np.log(p)
    wt   = log_p / np.sqrt(p)
    # cos matrix: (N_zeros, N_primes)
    cos_mat = np.cos(np.outer(zeros_arr, log_p))
    traces  = cos_mat @ wt
    rhs     = float(-np.sum(wt))
    return float(np.mean(traces) / rhs)

def compute_ratio_at_N(primes, zeros_full, n_zeros):
    return compute_ratio(primes, zeros_full[:n_zeros])

# Choose zeros source based on n_zeros
def get_zeros(n_zeros):
    if n_zeros <= N_25:
        return ZEROS_25[:n_zeros]
    elif n_zeros <= N_10K:
        return ZEROS_10K[:n_zeros]
    else:
        raise ValueError(f"n_zeros={n_zeros} exceeds available {N_10K}")

# ─────────────────────────────────────────────────────────────────────────────
# Model fitting helpers
# ─────────────────────────────────────────────────────────────────────────────

def fit_power_law(Ns, ratios):
    """y = a * N^(-b)"""
    log_N = np.log(Ns)
    log_y = np.log(ratios)
    b, log_a = np.polyfit(log_N, log_y, 1)
    b = -b
    a = math.exp(log_a)
    pred = a * Ns**(-b)
    ss_res = np.sum((ratios - pred)**2)
    ss_tot = np.sum((ratios - np.mean(ratios))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
    return float(a), float(b), float(r2)

def fit_inv_sqrt_offset(Ns, ratios):
    """y = A/sqrt(N) + c_inf"""
    def model(N, A, c_inf):
        return A / np.sqrt(N) + c_inf
    try:
        popt, _ = curve_fit(model, Ns, ratios, p0=[1.0, 0.1], maxfev=5000)
        A, c_inf = popt
        pred = model(Ns, A, c_inf)
        ss_res = np.sum((ratios - pred)**2)
        ss_tot = np.sum((ratios - np.mean(ratios))**2)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
        return float(A), float(c_inf), float(r2)
    except Exception:
        return None, None, None

def fit_power_offset(Ns, ratios):
    """y = A * N^(-b) + c_inf"""
    def model(N, A, b, c_inf):
        return A * N**(-b) + c_inf
    try:
        popt, _ = curve_fit(model, Ns, ratios, p0=[1.0, 0.2, 0.05], maxfev=10000,
                            bounds=([0, 0.001, -0.5], [10, 2, 0.5]))
        A, b, c_inf = popt
        pred = model(Ns, A, b, c_inf)
        ss_res = np.sum((ratios - pred)**2)
        ss_tot = np.sum((ratios - np.mean(ratios))**2)
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
        return float(A), float(b), float(c_inf), float(r2)
    except Exception:
        return None, None, None, None

def fit_log_decay(Ns, ratios):
    """y = a * log(N) + b"""
    log_N = np.log(Ns)
    coeffs = np.polyfit(log_N, ratios, 1)
    pred = np.polyval(coeffs, log_N)
    ss_res = np.sum((ratios - pred)**2)
    ss_tot = np.sum((ratios - np.mean(ratios))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
    return float(coeffs[0]), float(coeffs[1]), float(r2)

# ─────────────────────────────────────────────────────────────────────────────
# Track V1 — Formula Verification
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track V1: Formula Verification Suite")
print("=" * 65)

V1_CHECKS = [
    ("Weil_RHS: 6 primes",           lambda: weil_rhs(PRIME_SETS["6p_pmax13"]),            -4.014042, 1e-5),
    ("ratio: N=100, 6 primes",        lambda: compute_ratio_at_N(PRIME_SETS["6p_pmax13"],    ZEROS_25, 100),  0.247931, 1e-5),
    ("ratio: N=500, 6 primes",        lambda: compute_ratio_at_N(PRIME_SETS["6p_pmax13"],    ZEROS_25, 500),  0.173349, 1e-5),
    ("ratio: N=500, 36 primes",       lambda: compute_ratio_at_N(PRIME_SETS["36p_pmax151"],  ZEROS_25, 500),  0.136356, 1e-5),
    ("ratio: N=500, 62 primes (~c1)", lambda: compute_ratio_at_N(PRIME_SETS["62p_pmax300"],  ZEROS_25, 500),  0.118099, 2e-4),
]

v1_results = []
all_pass = True
print(f"\n  {'Check':<45} {'Computed':>10} {'Expected':>10} Status")
print("  " + "-" * 75)
for name, fn, expected, tol in V1_CHECKS:
    computed = fn()
    ok = abs(computed - expected) < tol
    status = "PASS" if ok else "FAIL"
    if not ok:
        all_pass = False
    print(f"  {name:<45} {computed:>10.6f} {expected:>10.6f}   {status}")
    v1_results.append({"check": name, "computed": computed, "expected": expected, "pass": ok})

print(f"\n  Overall: {'ALL PASS' if all_pass else 'FAILURES DETECTED'}")

if not all_pass:
    print("\n  *** ABORTING: formula verification failed ***")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Track E0 — dps=15 vs dps=25 sanity check
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track E0: dps=15 vs dps=25 Sanity Check")
print("=" * 65)

e0_results = []
for n in [100, 500, 1000]:
    r25  = compute_ratio(PRIME_SETS["6p_pmax13"], ZEROS_25[:n])
    r15  = compute_ratio(PRIME_SETS["6p_pmax13"], ZEROS_10K[:n])
    diff = abs(r25 - r15)
    ok   = diff < 0.0001
    print(f"  N={n:5d}: dps=25 ratio={r25:.8f}  dps=15 ratio={r15:.8f}  diff={diff:.2e}  {'OK' if ok else 'WARN'}")
    e0_results.append({"N_zeros": n, "ratio_dps25": r25, "ratio_dps15": r15, "diff": diff, "ok": ok})

print("  -> dps=15 zeros_10k will be used for N_zeros > 1000.")

# ─────────────────────────────────────────────────────────────────────────────
# Track E1 — 6-prime c1 Asymptote Test
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track E1: 6-Prime c1 Asymptote Test (N_zeros up to 10000)")
print("=" * 65)

E1_N_ZEROS = [1000, 2000, 3000, 5000, 7500, 10000]
p6 = PRIME_SETS["6p_pmax13"]

e1_points = []
print(f"\n  {'N_zeros':>8} {'ratio':>10} {'vs_c1':>10}")
print("  " + "-" * 35)
for n in E1_N_ZEROS:
    z = get_zeros(n)
    r = compute_ratio(p6, z)
    vs = r - C1
    print(f"  {n:>8d} {r:>10.6f} {vs:>+10.6f}")
    e1_points.append({"N_zeros": n, "ratio": r, "vs_c1": vs})

Ns_e1  = np.array([p["N_zeros"] for p in e1_points], dtype=float)
Rs_e1  = np.array([p["ratio"]   for p in e1_points], dtype=float)

# Fit models
a_pl, b_pl, r2_pl = fit_power_law(Ns_e1, Rs_e1)
A_is, cinf_is, r2_is = fit_inv_sqrt_offset(Ns_e1, Rs_e1)
A_po, b_po, cinf_po, r2_po = fit_power_offset(Ns_e1, Rs_e1)
a_ld, b_ld, r2_ld = fit_log_decay(Ns_e1, Rs_e1)

print(f"\n  Power law  (a*N^(-b)):         a={a_pl:.6f}  b={b_pl:.6f}  R²={r2_pl:.6f}  c_inf=0 (decays to 0)")
print(f"  1/sqrt(N)+c_inf:               A={A_is:.6f}  c_inf={cinf_is:.6f}  R²={r2_is:.6f}")
if A_po is not None:
    print(f"  Power+offset (A*N^(-b)+c_inf): A={A_po:.6f}  b={b_po:.6f}  c_inf={cinf_po:.6f}  R²={r2_po:.6f}")
print(f"  Log-decay  (a*log(N)+b):       a={a_ld:.6f}  b={b_ld:.6f}  R²={r2_ld:.6f}")

# Prediction at N=10000 from each model
print(f"\n  Predictions at N=10000:")
print(f"    Power law:     {a_pl * 10000**(-b_pl):.6f}")
print(f"    1/sqrt(N)+c∞: {A_is/math.sqrt(10000)+cinf_is:.6f}  (c∞={cinf_is:.6f}, vs c1={cinf_is-C1:+.6f})")
if A_po is not None:
    print(f"    Power+offset:  {A_po*10000**(-b_po)+cinf_po:.6f}  (c∞={cinf_po:.6f}, vs c1={cinf_po-C1:+.6f})")

# Decision gate
gate_met = A_is is not None and abs(cinf_is - C1) < 0.0005
gate_met_po = A_po is not None and abs(cinf_po - C1) < 0.0005
print(f"\n  Decision gate (|c∞-c1|<0.0005):")
print(f"    1/sqrt model: c∞={cinf_is:.8f}  |c∞-c1|={abs(cinf_is-C1):.6f}  {'STRONG CANDIDATE' if gate_met else 'not met'}")
if A_po is not None:
    print(f"    Power+offset: c∞={cinf_po:.8f}  |c∞-c1|={abs(cinf_po-C1):.6f}  {'STRONG CANDIDATE' if gate_met_po else 'not met'}")

e1_result = {
    "prime_set": "6p_pmax13",
    "N_primes": 6,
    "points": e1_points,
    "fits": {
        "power_law":   {"a": a_pl, "b": b_pl, "R2": r2_pl, "c_inf": 0.0, "model": "a*N^(-b)"},
        "inv_sqrt":    {"A": A_is, "c_inf": cinf_is, "R2": r2_is, "model": "A/sqrt(N)+c_inf"},
        "power_offset":{"A": A_po, "b": b_po, "c_inf": cinf_po, "R2": r2_po, "model": "A*N^(-b)+c_inf"},
        "log_decay":   {"a": a_ld, "b": b_ld, "R2": r2_ld, "model": "a*log(N)+b"},
    },
    "decision_gate_met_inv_sqrt": gate_met,
    "decision_gate_met_power_offset": gate_met_po,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track E2 — 36-prime and 62-prime Asymptote Comparison
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track E2: 36-prime and 62-prime Asymptote Comparison")
print("=" * 65)

E2_N_ZEROS = [1000, 2000, 5000, 10000]
E2_SETS = [("36p_pmax151", "36 primes"), ("62p_pmax300", "62 primes")]

e2_results = []
for set_key, label in E2_SETS:
    ps = PRIME_SETS[set_key]
    points = []
    print(f"\n  --- {label} ---")
    print(f"  {'N_zeros':>8} {'ratio':>10} {'vs_c1':>10}")
    print("  " + "-" * 32)
    for n in E2_N_ZEROS:
        z = get_zeros(n)
        r = compute_ratio(ps, z)
        vs = r - C1
        print(f"  {n:>8d} {r:>10.6f} {vs:>+10.6f}")
        points.append({"N_zeros": n, "ratio": r, "vs_c1": vs})

    Ns_e2 = np.array([p["N_zeros"] for p in points], dtype=float)
    Rs_e2 = np.array([p["ratio"]   for p in points], dtype=float)

    a2_pl, b2_pl, r2_pl2 = fit_power_law(Ns_e2, Rs_e2)
    A2_is, c2_inf, r2_is2 = fit_inv_sqrt_offset(Ns_e2, Rs_e2)
    A2_po, b2_po, c2_inf_po, r2_po2 = fit_power_offset(Ns_e2, Rs_e2)

    print(f"\n  Power law:     a={a2_pl:.6f}  b={b2_pl:.6f}  R²={r2_pl2:.6f}")
    print(f"  1/sqrt+c∞:    c∞={c2_inf:.6f}  vs c1={c2_inf-C1:+.6f}  R²={r2_is2:.6f}")
    if A2_po is not None:
        print(f"  Power+offset: c∞={c2_inf_po:.6f}  vs c1={c2_inf_po-C1:+.6f}  R²={r2_po2:.6f}")

    e2_results.append({
        "prime_set": set_key,
        "N_primes": len(ps),
        "points": points,
        "fits": {
            "power_law":   {"a": a2_pl, "b": b2_pl, "R2": r2_pl2},
            "inv_sqrt":    {"A": A2_is, "c_inf": c2_inf, "R2": r2_is2},
            "power_offset":{"A": A2_po, "b": b2_po, "c_inf": c2_inf_po, "R2": r2_po2},
        }
    })

# ─────────────────────────────────────────────────────────────────────────────
# Track S1 — Characterize a(N_p) and b(N_p)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track S1: 2D Surface — Characterize a(N_p) and b(N_p)")
print("=" * 65)

S1_N_ZEROS = [100, 200, 500, 1000]

# Power-law parameters from Phase 33 (inputs)
P33_FITS = {
    "6p_pmax13":   {"a": 0.6478, "b": 0.2112},
    "36p_pmax151": {"a": None,   "b": 0.1468},
    "62p_pmax300": {"a": 0.2465, "b": 0.1197},
}

s1_table = []
print(f"\n  {'Prime set':<18} {'N_p':>5} {'p_max':>6}  {'N=100':>8} {'N=200':>8} {'N=500':>8} {'N=1000':>8}  {'a_fit':>8} {'b_fit':>8} {'R2':>7}")
print("  " + "-" * 90)

for set_key, ps in PRIME_SETS.items():
    Np    = len(ps)
    pmax  = int(ps[-1])
    ratios_at_N = []
    for n in S1_N_ZEROS:
        z = get_zeros(n)
        r = compute_ratio(ps, z)
        ratios_at_N.append(r)

    Ns_s1 = np.array(S1_N_ZEROS, dtype=float)
    Rs_s1 = np.array(ratios_at_N, dtype=float)

    if set_key in P33_FITS and P33_FITS[set_key]["a"] is not None:
        # Use Phase 33 a if available, just re-confirm
        a_fit, b_fit, r2_fit = fit_power_law(Ns_s1, Rs_s1)
    else:
        a_fit, b_fit, r2_fit = fit_power_law(Ns_s1, Rs_s1)

    print(f"  {set_key:<18} {Np:>5} {pmax:>6}  {ratios_at_N[0]:>8.4f} {ratios_at_N[1]:>8.4f} {ratios_at_N[2]:>8.4f} {ratios_at_N[3]:>8.4f}  {a_fit:>8.4f} {b_fit:>8.4f} {r2_fit:>7.5f}")

    s1_table.append({
        "prime_set": set_key,
        "N_primes": Np,
        "p_max": pmax,
        "ratios": {str(n): r for n, r in zip(S1_N_ZEROS, ratios_at_N)},
        "a": a_fit,
        "b": b_fit,
        "R2": r2_fit,
    })

# Fit a(N_p) and b(N_p) vs N_p
Nps   = np.array([row["N_primes"] for row in s1_table], dtype=float)
a_vals = np.array([row["a"]       for row in s1_table], dtype=float)
b_vals = np.array([row["b"]       for row in s1_table], dtype=float)

def try_models_1d(Xs, Ys, label):
    results = {}
    # Power law
    a_, b_, r2_ = fit_power_law(Xs, Ys)
    results["power_law"] = {"a": a_, "b": b_, "R2": r2_, "model": f"{a_:.4f}*N^(-{b_:.4f})"}

    # Log decay
    a_l, b_l, r2_l = fit_log_decay(Xs, Ys)
    results["log_decay"] = {"a": a_l, "b": b_l, "R2": r2_l, "model": f"{a_l:.4f}*log(N)+{b_l:.4f}"}

    # 1/sqrt(N)
    def inv_sqrt(N, A, c):
        return A / np.sqrt(N) + c
    try:
        popt, _ = curve_fit(inv_sqrt, Xs, Ys, p0=[1.0, 0.05], maxfev=5000)
        pred = inv_sqrt(Xs, *popt)
        ss_res = np.sum((Ys - pred)**2)
        ss_tot = np.sum((Ys - np.mean(Ys))**2)
        r2_ = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
        results["inv_sqrt"] = {"A": float(popt[0]), "c": float(popt[1]), "R2": float(r2_),
                               "model": f"{popt[0]:.4f}/sqrt(N)+{popt[1]:.4f}"}
    except Exception:
        pass

    # 1/log(N)
    log_Xs = np.log(Xs)
    def inv_log(N, A, c):
        return A / np.log(N) + c
    try:
        popt2, _ = curve_fit(inv_log, Xs, Ys, p0=[1.0, 0.05], maxfev=5000)
        pred2 = inv_log(Xs, *popt2)
        ss_res = np.sum((Ys - pred2)**2)
        ss_tot = np.sum((Ys - np.mean(Ys))**2)
        r2_2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
        results["inv_log"] = {"A": float(popt2[0]), "c": float(popt2[1]), "R2": float(r2_2),
                              "model": f"{popt2[0]:.4f}/log(N)+{popt2[1]:.4f}"}
    except Exception:
        pass

    best = max(results.items(), key=lambda x: x[1]["R2"])
    print(f"\n  {label}:")
    for mname, mres in sorted(results.items(), key=lambda x: -x[1]["R2"]):
        print(f"    {mname:<14} R²={mres['R2']:.6f}  {mres['model']}")
    print(f"    Best: {best[0]} (R²={best[1]['R2']:.6f})")
    return results

print("\n  --- Fitting a(N_p) vs N_p ---")
a_models = try_models_1d(Nps, a_vals, "a(N_p)")

print("\n  --- Fitting b(N_p) vs N_p ---")
b_models = try_models_1d(Nps, b_vals, "b(N_p)")

# Check: b ∝ 1/log(N_p)?
print("\n  --- b vs 1/log(N_p) check ---")
inv_log_Np = 1.0 / np.log(Nps)
print(f"  N_p values: {Nps.astype(int).tolist()}")
print(f"  b values:   {[f'{v:.6f}' for v in b_vals]}")
print(f"  1/log(N_p): {[f'{v:.6f}' for v in inv_log_Np]}")
print(f"  b/1/log(N_p) ratios: {[f'{b/il:.4f}' for b, il in zip(b_vals, inv_log_Np)]}")

s1_result = {
    "table": s1_table,
    "a_models": a_models,
    "b_models": b_models,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track S2 — Surface Reconstruction and Residuals
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track S2: Surface Reconstruction and Residuals")
print("=" * 65)

# Use best-fit models to predict ratio
# Best model for a(N_p) and b(N_p) will be determined from S1 results
# Use power law fits as they typically win

# Power-law fits for a and b
a_fit_a, b_fit_a, r2_a = fit_power_law(Nps, a_vals)  # a(N_p) = A * N_p^(-alpha)
a_fit_b, b_fit_b, r2_b = fit_power_law(Nps, b_vals)  # b(N_p) = B * N_p^(-beta)

print(f"\n  a(N_p) power fit: {a_fit_a:.6f} * N_p^(-{b_fit_a:.6f})  R²={r2_a:.6f}")
print(f"  b(N_p) power fit: {a_fit_b:.6f} * N_p^(-{b_fit_b:.6f})  R²={r2_b:.6f}")

# Predicted surface: ratio(N_p, N_z) = a(N_p) * N_z^(-b(N_p))
print("\n  Surface reconstruction (predicted vs actual, Phase 33 grid):")
print(f"\n  {'N_p':>5} {'p_max':>6}  {'N=100':>25} {'N=200':>25} {'N=500':>25} {'N=1000':>25}")
print(f"  {'':>12}  {'pred/actual/resid':>25} {'pred/actual/resid':>25} {'pred/actual/resid':>25} {'pred/actual/resid':>25}")
print("  " + "-" * 115)

s2_residuals = []
all_resids = []
for row in s1_table:
    Np   = row["N_primes"]
    pmax = row["p_max"]
    a_pred = a_fit_a * Np**(-b_fit_a)
    b_pred = a_fit_b * Np**(-b_fit_b)

    row_resids = []
    cols = []
    for n in S1_N_ZEROS:
        actual  = row["ratios"][str(n)]
        pred    = a_pred * n**(-b_pred)
        resid   = pred - actual
        cols.append(f"{pred:.4f}/{actual:.4f}/{resid:+.4f}")
        row_resids.append({"N_zeros": n, "predicted": pred, "actual": actual, "residual": resid})
        all_resids.append(abs(resid))

    print(f"  {Np:>5} {pmax:>6}  {cols[0]:>25} {cols[1]:>25} {cols[2]:>25} {cols[3]:>25}")
    s2_residuals.append({"N_primes": Np, "p_max": pmax, "a_pred": a_pred, "b_pred": b_pred, "points": row_resids})

print(f"\n  Max |residual|: {max(all_resids):.6f}")
print(f"  Mean |residual|: {np.mean(all_resids):.6f}")
print(f"  Median |residual|: {np.median(all_resids):.6f}")

s2_result = {
    "a_N_p_fit": {"a": a_fit_a, "b": b_fit_a, "R2": r2_a, "model": "a*N_p^(-b)"},
    "b_N_p_fit": {"a": a_fit_b, "b": b_fit_b, "R2": r2_b, "model": "a*N_p^(-b)"},
    "max_residual": float(max(all_resids)),
    "mean_residual": float(np.mean(all_resids)),
    "grid": s2_residuals,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track B1 — b(N_p) Weyl Equidistribution Probe
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track B1: b(N_p) Weyl Equidistribution Probe")
print("=" * 65)

def star_discrepancy(xs):
    """Compute D*_N (star discrepancy) for sequence in [0,1]."""
    xs_sorted = np.sort(xs)
    N = len(xs_sorted)
    i_arr = np.arange(1, N+1, dtype=float)
    sup1 = np.max(np.abs(i_arr / N - xs_sorted))
    sup2 = np.max(np.abs((i_arr - 1) / N - xs_sorted))
    return float(max(sup1, sup2))

def l2_discrepancy(xs):
    """L2 discrepancy of sequence in [0,1]."""
    xs_sorted = np.sort(xs)
    N = len(xs_sorted)
    # Formula: D²_N = 1/3 - (2/N)*sum(x_i*(1-x_i)) + (1/N²)*sum(min(x_i,x_j))
    term1 = 1.0/3.0
    term2 = (2.0/N) * np.sum(xs_sorted * (1.0 - xs_sorted))
    # Efficient sum of min(xi, xj)
    i_arr = np.arange(1, N+1, dtype=float)
    term3 = (1.0/N**2) * np.sum((2*i_arr - 1) * xs_sorted)
    return float(math.sqrt(max(term1 - term2 + term3, 0)))

print(f"\n  Discrepancy of {{log p mod 2pi}} for each prime set:")
print(f"\n  {'Prime set':<18} {'N_p':>5} {'D*_N':>10} {'L2_disc':>10} {'|Weil_RHS|':>12} {'log(pmax)':>10} {'b':>8}")
print("  " + "-" * 80)

b1_data = []
for row, (set_key, ps) in zip(s1_table, PRIME_SETS.items()):
    xs = (np.log(ps) % (2 * math.pi)) / (2 * math.pi)  # map to [0,1]
    d_star = star_discrepancy(xs)
    l2_disc = l2_discrepancy(xs)
    wrhs = abs(weil_rhs(ps))
    log_pmax = math.log(ps[-1])
    b = row["b"]
    print(f"  {set_key:<18} {len(ps):>5} {d_star:>10.6f} {l2_disc:>10.6f} {wrhs:>12.6f} {log_pmax:>10.4f} {b:>8.6f}")
    b1_data.append({
        "prime_set": set_key,
        "N_p": len(ps),
        "d_star": d_star,
        "l2_disc": l2_disc,
        "weil_rhs_abs": wrhs,
        "log_pmax": log_pmax,
        "pi_pmax": len(ps),
        "b": b,
    })

# Correlate b with predictors
Bs = np.array([d["b"] for d in b1_data])
predictors = {
    "D*_N":           np.array([d["d_star"]      for d in b1_data]),
    "L2_disc":        np.array([d["l2_disc"]      for d in b1_data]),
    "1/D*_N":         1.0 / np.array([d["d_star"]  for d in b1_data]),
    "|Weil_RHS|":     np.array([d["weil_rhs_abs"] for d in b1_data]),
    "log(pmax)":      np.array([d["log_pmax"]     for d in b1_data]),
    "1/log(pi(pmax))": 1.0 / np.log(np.array([d["N_p"] for d in b1_data], dtype=float)),
    "log(N_p)":       np.log(np.array([d["N_p"]  for d in b1_data], dtype=float)),
    "1/sqrt(N_p)":    1.0 / np.sqrt(np.array([d["N_p"] for d in b1_data], dtype=float)),
}

print("\n  Correlation of b with predictors:")
print(f"  {'Predictor':<22} {'r':>8} {'R²':>8} {'Flag'}")
print("  " + "-" * 55)
b1_corrs = {}
for pname, pvals in predictors.items():
    r, pval = pearsonr(Bs, pvals)
    r2 = r**2
    flag = " *** R²>0.95" if r2 > 0.95 else (" ** R²>0.90" if r2 > 0.90 else "")
    print(f"  {pname:<22} {r:>8.4f} {r2:>8.4f}{flag}")
    b1_corrs[pname] = {"r": float(r), "R2": float(r2)}

b1_result = {"data": b1_data, "correlations": b1_corrs}

# ─────────────────────────────────────────────────────────────────────────────
# Track P1 — Exact c1 Euler Product Probe
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track P1: c1 Euler Product Probe")
print("=" * 65)

p6_arr = PRIME_SETS["6p_pmax13"]
log_p6 = np.log(p6_arr)

W   = float(np.sum(log_p6 / np.sqrt(p6_arr)))   # = |Weil_RHS| = 4.014042
A   = float(np.sum(log_p6 / p6_arr))
B   = float(np.sum(log_p6 / p6_arr**2))
C   = float(np.sum(log_p6**2 / np.sqrt(p6_arr)))
D   = float(np.sum(log_p6 / p6_arr**1.5))
E_s = float(np.sum(1.0 / np.sqrt(p6_arr)))
F   = float(np.sum(1.0 / p6_arr))
G   = float(np.sum(log_p6**2 / p6_arr))

# Truncated Mertens product Π(1-1/p)^{-1}
mertens = float(np.prod(1.0 / (1.0 - 1.0/p6_arr)))

# log(p)/sqrt(p) sum squared
W2  = W**2

print(f"\n  6-prime Euler product sums:")
print(f"    W  = sum log(p)/sqrt(p)  = {W:.8f}  (= |Weil_RHS|)")
print(f"    A  = sum log(p)/p        = {A:.8f}")
print(f"    B  = sum log(p)/p^2      = {B:.8f}")
print(f"    C  = sum (log p)^2/sqrt(p) = {C:.8f}")
print(f"    D  = sum log(p)/p^(3/2)  = {D:.8f}")
print(f"    E  = sum 1/sqrt(p)       = {E_s:.8f}")
print(f"    F  = sum 1/p             = {F:.8f}")
print(f"    G  = sum (log p)^2/p     = {G:.8f}")
print(f"    Mertens (6p)             = {mertens:.8f}")
print(f"\n  Target: c1 = {C1:.10f}")

# Build candidate expressions
candidates = {}

# Ratios
for name, val in [("W", W), ("A", A), ("B", B), ("C", C), ("D", D), ("E", E_s), ("F", F), ("G", G)]:
    for name2, val2 in [("W", W), ("A", A), ("B", B), ("C", C), ("D", D), ("E", E_s), ("F", F), ("G", G)]:
        if name != name2 and abs(val2) > 1e-10:
            candidates[f"{name}/{name2}"] = val / val2

# Inverse
for name, val in [("W", W), ("A", A), ("B", B), ("C", C), ("D", D), ("E", E_s)]:
    candidates[f"1/{name}"] = 1.0/val if abs(val) > 1e-10 else None
    candidates[f"1/{name}^2"] = 1.0/val**2 if abs(val) > 1e-10 else None

# Trig combinations
candidates["sin(arctan(A/W))"] = math.sin(math.atan(A/W))
candidates["sin(arctan(B/W))"] = math.sin(math.atan(B/W))
candidates["sin(arctan(D/W))"] = math.sin(math.atan(D/W))
candidates["sin(arctan(B/A))"] = math.sin(math.atan(B/A))
candidates["sin(arctan(F/A))"] = math.sin(math.atan(F/A))
candidates["sin(arctan(E/W))"] = math.sin(math.atan(E_s/W))
candidates["sin(arctan(W/C))"] = math.sin(math.atan(W/C))
candidates["cos(arctan(W/A))"] - None if False else None
candidates["sin(1/W)"] = math.sin(1.0/W)
candidates["sin(A)"]  = math.sin(A)
candidates["sin(B)"]  = math.sin(B)
candidates["sin(pi*A/W)"] = math.sin(math.pi * A / W)
candidates["sin(pi*B/W)"] = math.sin(math.pi * B / W)
candidates["sin(pi*F)"]   = math.sin(math.pi * F)
candidates["sin(pi*D/W)"] = math.sin(math.pi * D / W)
candidates["sin(pi*B/A)"] = math.sin(math.pi * B / A)
candidates["B/W^(3/2)"]   = B / W**1.5
candidates["D/W"]         = D / W
candidates["B/A^2"]       = B / A**2 if abs(A) > 1e-10 else None
candidates["A^2/W^2"]     = A**2/W**2
candidates["A/W^2"]       = A/W**2
candidates["B/W^2"]       = B/W**2
candidates["Mertens^(-1)/W"] = 1.0/(mertens * W) if abs(mertens) > 1e-10 else None
candidates["A/(W*Mertens)"]  = A/(W * mertens)
candidates["1/(W*sqrt(pi))"] = 1.0/(W * math.sqrt(math.pi))
candidates["pi/(W^2)"]    = math.pi / W**2
candidates["1/(pi*W)"]    = 1.0/(math.pi * W)
candidates["W/(4*C)"]     = W / (4*C)
candidates["W^2/(4*C*W)"] = W**2/(4*C*W) if abs(C) > 1e-10 else None
candidates["A/(2*W)"]     = A / (2*W)

# Remove None
candidates = {k: v for k, v in candidates.items() if v is not None}

# Find closest to c1
threshold = 0.005
close_matches = []
for expr, val in candidates.items():
    diff = abs(val - C1)
    if diff < threshold:
        close_matches.append((diff, expr, val))

close_matches.sort()

print(f"\n  Candidates within 0.005 of c1={C1:.8f}:")
p1_matches = []
if close_matches:
    print(f"  {'Expression':<30} {'Value':>12} {'|val-c1|':>12}")
    print("  " + "-" * 58)
    for diff, expr, val in close_matches[:20]:
        print(f"  {expr:<30} {val:>12.8f} {diff:>12.8f}")
        p1_matches.append({"expression": expr, "value": val, "diff_from_c1": diff})
else:
    print("  No candidates within 0.005 of c1.")

p1_result = {
    "sums": {"W": W, "A": A, "B": B, "C": C, "D": D, "E": E_s, "F": F, "G": G, "mertens": mertens},
    "c1": C1,
    "close_matches": p1_matches,
    "threshold": threshold,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track P2 — Weil Truncation Fraction
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("Track P2: Weil Truncation Fraction (6/12/24/48 primes)")
print("=" * 65)

N_ZEROS_P2 = 500
zeros_p2 = ZEROS_25[:N_ZEROS_P2]

# Find prime set boundaries for 12, 24, 48 primes
def nth_prime(n):
    ps = first_n_primes(n)
    return ps

p_sets_p2 = {
    6:  np.array(first_n_primes(6),  dtype=float),
    12: np.array(first_n_primes(12), dtype=float),
    24: np.array(first_n_primes(24), dtype=float),
    48: np.array(first_n_primes(48), dtype=float),
}

print(f"\n  Prime sets for P2:")
for n, ps in p_sets_p2.items():
    print(f"    {n:2d} primes: p_max={int(ps[-1])}, Weil_RHS={weil_rhs(ps):.6f}")

# Compute traces for full (48-prime) set
traces_48 = np.array([float(np.dot(
    np.log(p_sets_p2[48]) / np.sqrt(p_sets_p2[48]),
    np.cos(t * np.log(p_sets_p2[48]))
)) for t in zeros_p2])
mean_48 = float(np.mean(traces_48))
rhs_48  = weil_rhs(p_sets_p2[48])
ratio_48 = mean_48 / rhs_48

print(f"\n  Ratios at N_zeros={N_ZEROS_P2}:")
print(f"  {'N_primes':>10} {'p_max':>6} {'Weil_RHS':>12} {'ratio':>10} {'ratio/ratio_48':>16} {'vs c1²':>10}")
print("  " + "-" * 72)

p2_results = []
for n in [6, 12, 24, 48]:
    ps = p_sets_p2[n]
    r  = compute_ratio(ps, zeros_p2)
    frac_of_48 = r / ratio_48
    c1sq       = C1**2
    vs_c1sq    = r - c1sq
    vs_c1      = r - C1
    print(f"  {n:>10} {int(ps[-1]):>6} {weil_rhs(ps):>12.6f} {r:>10.6f} {frac_of_48:>16.6f} {vs_c1sq:>10.6f}")
    p2_results.append({
        "N_primes": n,
        "p_max": int(ps[-1]),
        "ratio": r,
        "fraction_of_48prime": frac_of_48,
        "vs_c1": r - C1,
        "vs_c1_squared": vs_c1sq,
    })

# Check: does ratio(6p)/ratio(48p) converge to c1 or c1^2?
ratio_6p  = p2_results[0]["ratio"]
frac_6_of_48 = ratio_6p / ratio_48
print(f"\n  ratio(6p)/ratio(48p) = {frac_6_of_48:.6f}")
print(f"  c1                   = {C1:.6f}")
print(f"  c1^2                 = {C1**2:.6f}")
print(f"  |frac - c1|  = {abs(frac_6_of_48 - C1):.6f}")
print(f"  |frac - c1^2| = {abs(frac_6_of_48 - C1**2):.6f}")

# Check if ratio(6p) ≈ c1 * ratio(48p)?
pred_6_from_c1 = C1 * ratio_48
print(f"\n  c1 * ratio(48p) = {pred_6_from_c1:.6f}  vs actual ratio(6p) = {ratio_6p:.6f}")
print(f"  Difference: {abs(ratio_6p - pred_6_from_c1):.6f}")

p2_result = {
    "N_zeros": N_ZEROS_P2,
    "ratio_48p": ratio_48,
    "results": p2_results,
    "fraction_6p_of_48p": float(frac_6_of_48),
    "c1": C1,
    "c1_squared": C1**2,
}

# ─────────────────────────────────────────────────────────────────────────────
# Save JSON output files
# ─────────────────────────────────────────────────────────────────────────────

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] Saved {path}")

# V1
save_json({
    "phase": 34, "track": "V1",
    "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
    "c1": C1,
    "e0_dps_comparison": e0_results,
    "v1_checks": v1_results,
    "all_pass": all_pass,
}, "phase34_formula_verification.json")

# E1
save_json({
    "phase": 34, "track": "E1",
    "formula": "Tr_BK = sum_p (log p / sqrt(p)) * cos(t * log p)",
    "c1": C1,
    "prime_set": [2,3,5,7,11,13],
    "N_primes": 6,
    "zeros_source": "rh_zeros_10k.json (dps=15 for N>1000)",
    "points": e1_result["points"],
    "fits": e1_result["fits"],
    "decision_gate_inv_sqrt": e1_result["decision_gate_met_inv_sqrt"],
    "decision_gate_power_offset": e1_result["decision_gate_met_power_offset"],
}, "phase34_c1_asymptote_test.json")

# E2
save_json({
    "phase": 34, "track": "E2",
    "c1": C1,
    "sets": e2_results,
}, "phase34_asymptote_comparison.json")

# S1/S2
save_json({
    "phase": 34, "track": "S1",
    "c1": C1,
    "N_zeros_used": S1_N_ZEROS,
    "surface_table": s1_table,
    "a_models": s1_result["a_models"],
    "b_models": s1_result["b_models"],
}, "phase34_surface_parameters.json")

save_json({
    "phase": 34, "track": "S2",
    "c1": C1,
    "a_N_p_fit": s2_result["a_N_p_fit"],
    "b_N_p_fit": s2_result["b_N_p_fit"],
    "max_residual": s2_result["max_residual"],
    "mean_residual": s2_result["mean_residual"],
    "grid": s2_result["grid"],
}, "phase34_surface_residuals.json")

# B1
save_json({
    "phase": 34, "track": "B1",
    "data": b1_result["data"],
    "correlations": b1_result["correlations"],
}, "phase34_b_predictor_analysis.json")

# P1
save_json({
    "phase": 34, "track": "P1",
    "c1": C1,
    "prime_set": [2,3,5,7,11,13],
    "sums": p1_result["sums"],
    "threshold": threshold,
    "close_matches": p1_result["close_matches"],
}, "phase34_c1_euler_probe.json")

# P2
save_json({
    "phase": 34, "track": "P2",
    "c1": C1,
    "c1_squared": C1**2,
    "N_zeros": N_ZEROS_P2,
    **p2_result,
}, "phase34_weil_truncation.json")

print("\n" + "=" * 65)
print("Phase 34 complete.")
print(f"  c1 asymptote (inv_sqrt model): c∞ = {cinf_is:.8f}")
print(f"  vs c1 = {cinf_is - C1:+.8f}")
print(f"  Decision gate met (inv_sqrt): {gate_met}")
print(f"  Decision gate met (power+offset): {gate_met_po}")
print("=" * 65)
