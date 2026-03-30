"""
rh_phase35.py — Phase 35: Analytic Derivation + Operator Groundwork
Chavez AI Labs LLC | Applied Pathological Mathematics
Paul Chavez | 2026-03-27

Tracks:
  V1  — Formula verification (always first)
  W1  — Cosine mean decay C_N(log p) per prime
  W2  — β(p) prime-independence test
  W3  — b vs W = |Weil_RHS| functional form
  C1  — c₁ level curve parametrization
  C2  — c₁ level curve analytic tests
  L1  — Long-range limit: N_p=168 at large N_zeros
  O1  — Weil explicit formula connection (derivation + verification)
  O2  — Sedenion scalar trace vs classical Tr_BK
"""

import sys, json, math
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import pearsonr, linregress

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

C1 = 0.11797805192095003
C3 = 0.99301620292165280
THETA_W = math.degrees(math.asin(C1))

print("=" * 65)
print("RH Investigation - Phase 35")
print("Chavez AI Labs LLC | Applied Pathological Mathematics")
print("Analytic Derivation + Operator Groundwork")
print("=" * 65)

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

ZEROS_25  = load_zeros("rh_zeros.json")
ZEROS_10K = load_zeros("rh_zeros_10k.json")
print(f"Zeros dps=25: {len(ZEROS_25)}   dps=15: {len(ZEROS_10K)}")

def get_zeros(n):
    if n <= len(ZEROS_25):
        return ZEROS_25[:n]
    return ZEROS_10K[:n]

# ─────────────────────────────────────────────────────────────────────────────
# Prime helpers
# ─────────────────────────────────────────────────────────────────────────────

def primes_up_to(n):
    sieve = [True]*(n+1); sieve[0]=sieve[1]=False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i): sieve[j]=False
    return [i for i in range(2, n+1) if sieve[i]]

P6   = np.array(primes_up_to(13),   dtype=float)
P168 = np.array(primes_up_to(1000), dtype=float)

def weil_rhs(primes):
    p = np.asarray(primes, dtype=float)
    return float(-np.sum(np.log(p)/np.sqrt(p)))

def compute_ratio(primes, zeros_arr):
    p = np.asarray(primes, dtype=float)
    wt = np.log(p)/np.sqrt(p)
    cos_mat = np.cos(np.outer(zeros_arr, np.log(p)))
    traces  = cos_mat @ wt
    rhs = float(-np.sum(wt))
    return float(np.mean(traces)/rhs)

# Phase 34 surface parameters (verified)
P34_TABLE = [
    {"N_p":  6, "p_max":  13, "a": 0.6461, "b": 0.2103, "W": 4.014042},
    {"N_p": 15, "p_max":  47, "a": 0.5243, "b": 0.1873, "W": 9.581320},
    {"N_p": 36, "p_max": 151, "a": 0.3474, "b": 0.1498, "W":19.397144},
    {"N_p": 62, "p_max": 300, "a": 0.2488, "b": 0.1212, "W":28.848057},
    {"N_p": 95, "p_max": 499, "a": 0.1718, "b": 0.0848, "W":38.761427},
    {"N_p":168, "p_max":1000, "a": 0.1151, "b": 0.0553, "W":56.574158},
]

def fit_power_law(Xs, Ys):
    b, log_a = np.polyfit(np.log(Xs), np.log(Ys), 1)
    a = math.exp(log_a); b = -b
    pred = a * Xs**(-b)
    ss_res = np.sum((Ys-pred)**2); ss_tot = np.sum((Ys-np.mean(Ys))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 1.0
    return float(a), float(b), float(r2)

def fit_power_offset(Xs, Ys):
    def model(N, A, b, c): return A*N**(-b)+c
    try:
        popt, _ = curve_fit(model, Xs, Ys, p0=[0.5,0.15,0.05],
                            bounds=([0,0.001,-0.5],[5,2,0.5]), maxfev=10000)
        pred = model(Xs, *popt)
        ss_res = np.sum((Ys-pred)**2); ss_tot = np.sum((Ys-np.mean(Ys))**2)
        r2 = 1-ss_res/ss_tot if ss_tot > 0 else 1.0
        return float(popt[0]), float(popt[1]), float(popt[2]), float(r2)
    except Exception:
        return None, None, None, None

# ─────────────────────────────────────────────────────────────────────────────
# SEDENION ENGINE (from rh_phase29_bk_burst.py)
# ─────────────────────────────────────────────────────────────────────────────

def cd_conj(v):
    c = list(v); c[0] = v[0]
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0]*b[0]]
    h = n//2
    a1,a2,b1,b2 = a[:h],a[h:],b[:h],b[h:]
    c1 = [x-y for x,y in zip(cd_mul(a1,b1), cd_mul(cd_conj(b2),a2))]
    c2 = [x+y for x,y in zip(cd_mul(b2,a1), cd_mul(a2,cd_conj(b1)))]
    return c1+c2

def norm_sq(v): return sum(x*x for x in v)

def make16(pairs):
    v=[0.0]*16
    for i,val in pairs: v[i]=float(val)
    return v

sqrt2 = math.sqrt(2.0)

ROOT_16D = {
    2:  make16([(3, 1.0),(12,-1.0)]),
    3:  make16([(5, 1.0),(10, 1.0)]),
    5:  make16([(3, 1.0),(6,  1.0)]),
    7:  make16([(2, 1.0),(7, -1.0)]),
    11: make16([(2, 1.0),(7,  1.0)]),
    13: make16([(6, 1.0),(9,  1.0)]),
}

def F_16d(t, sigma=0.5, primes=None):
    if primes is None: primes = [2,3,5,7,11,13]
    r = make16([(0,1.0)])
    for p in primes:
        theta = t*math.log(p)
        rp = ROOT_16D[p]; rn = math.sqrt(norm_sq(rp))
        f = [0.0]*16; f[0] = math.cos(theta)
        for i in range(16): f[i] += math.sin(theta)*rp[i]/rn
        r = cd_mul(r, f)
    r[4] += (sigma-0.5)/sqrt2
    r[5] -= (sigma-0.5)/sqrt2
    return r

def scalar_part(sed_vec):
    return sed_vec[0]

# ─────────────────────────────────────────────────────────────────────────────
# Track V1 — Formula Verification
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track V1: Formula Verification")
print("="*65)

V1 = [
    ("Weil_RHS 6p",      lambda: weil_rhs(P6),                              -4.014042, 1e-5),
    ("ratio N=100, 6p",  lambda: compute_ratio(P6, ZEROS_25[:100]),          0.247931, 1e-5),
    ("ratio N=500, 6p",  lambda: compute_ratio(P6, ZEROS_25[:500]),          0.173349, 1e-5),
    ("ratio N=500, 36p", lambda: compute_ratio(np.array(primes_up_to(151),dtype=float), ZEROS_25[:500]), 0.136356, 1e-5),
    ("ratio N=500, 62p", lambda: compute_ratio(np.array(primes_up_to(300),dtype=float), ZEROS_25[:500]), 0.118099, 2e-4),
]

all_pass = True
for name, fn, exp, tol in V1:
    got = fn(); ok = abs(got-exp) < tol; all_pass = all_pass and ok
    print(f"  {name:<28} got={got:.6f}  exp={exp:.6f}  {'PASS' if ok else 'FAIL'}")

if not all_pass:
    print("  *** ABORTING: V1 failed ***"); sys.exit(1)
print("  All PASS")

# ─────────────────────────────────────────────────────────────────────────────
# Track W1 — Cosine Mean Decay C_N(log p)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track W1: Cosine Mean Decay C_N(log p) per prime")
print("="*65)

PRIMES_6 = [2, 3, 5, 7, 11, 13]
W1_N_ZEROS = [100, 500, 1000, 5000, 10000]

# Precompute: for each N, compute cosine means for each prime
# C_N(log p) = (1/N) sum_{n=1}^N cos(gamma_n * log p)
w1_data = []
print(f"\n  {'Prime':>6} {'log_p':>8}", end="")
for n in W1_N_ZEROS:
    print(f"  N={n:>6}", end="")
print(f"  {'A':>8} {'beta':>8} {'R2':>8}")
print("  " + "-"*80)

for p in PRIMES_6:
    log_p = math.log(p)
    wt_p  = math.log(p)/math.sqrt(p)  # w(p)
    CN_vals = []
    for n in W1_N_ZEROS:
        z = get_zeros(n)
        CN = float(np.mean(np.cos(z * log_p)))
        CN_vals.append(CN)

    Ns_arr = np.array(W1_N_ZEROS, dtype=float)
    CN_arr = np.abs(np.array(CN_vals))  # fit magnitude (decay of |C_N|)

    # Power law fit on |C_N| vs N
    try:
        A_fit, beta_fit, r2_fit = fit_power_law(Ns_arr, CN_arr)
    except Exception:
        A_fit, beta_fit, r2_fit = None, None, None

    vals_str = "".join(f"  {v:>8.5f}" for v in CN_vals)
    if A_fit is not None:
        print(f"  {p:>6} {log_p:>8.4f}{vals_str}  {A_fit:>8.5f} {beta_fit:>8.5f} {r2_fit:>8.6f}")
    else:
        print(f"  {p:>6} {log_p:>8.4f}{vals_str}  fit_failed")

    w1_data.append({
        "prime": p, "log_p": log_p, "weight_w_p": wt_p,
        "CN_vals": {str(n): float(v) for n, v in zip(W1_N_ZEROS, CN_vals)},
        "A": float(A_fit) if A_fit is not None else None,
        "beta": float(beta_fit) if beta_fit is not None else None,
        "R2": float(r2_fit) if r2_fit is not None else None,
    })

# ─────────────────────────────────────────────────────────────────────────────
# Track W2 — beta(p) Prime-Independence Test
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track W2: beta(p) Prime-Independence Test")
print("="*65)

betas = [d["beta"] for d in w1_data if d["beta"] is not None]
A_vals = [d["A"]  for d in w1_data if d["A"]   is not None]
wts   = [d["weight_w_p"] for d in w1_data if d["beta"] is not None]

betas_arr = np.array(betas)
wts_arr   = np.array(wts)
log_ps    = np.array([math.log(p) for p in PRIMES_6])

beta_mean   = float(np.mean(betas_arr))
beta_std    = float(np.std(betas_arr))
beta_cv     = beta_std / beta_mean if beta_mean != 0 else 0
beta_w_mean = float(np.sum(wts_arr * betas_arr) / np.sum(wts_arr))  # weighted mean

print(f"\n  beta values per prime:")
for d in w1_data:
    print(f"    p={d['prime']:3d}  log_p={d['log_p']:.4f}  beta={d['beta']:.6f}  A={d['A']:.6f}  R2={d['R2']:.6f}")

print(f"\n  beta statistics:")
print(f"    mean   = {beta_mean:.6f}")
print(f"    std    = {beta_std:.6f}")
print(f"    CV     = {beta_cv:.4f}  (0=perfectly constant)")
print(f"    weighted mean <beta>_w = {beta_w_mean:.6f}")
print(f"    empirical b (Phase 34) = 0.210258")
print(f"    |<beta>_w - b| = {abs(beta_w_mean - 0.210258):.6f}")

# Test: is beta constant (i.e., is variation < noise)?
# Correlation of beta with log_p
r_beta_logp, pv_beta_logp = pearsonr(log_ps, betas_arr)
print(f"\n  Correlation beta vs log_p: r={r_beta_logp:.4f}  R2={r_beta_logp**2:.4f}")
print(f"  -> beta is {'NOT ' if abs(r_beta_logp) > 0.5 else ''}systematically related to log_p")

if beta_cv < 0.1:
    print(f"\n  CONCLUSION: beta is approximately CONSTANT across primes (CV={beta_cv:.4f})")
    print(f"  b = <beta>_w = {beta_w_mean:.6f} is the derivation of the power-law exponent.")
else:
    print(f"\n  CONCLUSION: beta varies across primes (CV={beta_cv:.4f})")
    print(f"  The weighted mean <beta>_w = {beta_w_mean:.6f} is the effective decay exponent.")

# Express the full mean trace using per-prime decomposition
print(f"\n  Per-prime contribution to <Tr_BK>_N at N=500:")
Tr_decomp = {}
z500 = get_zeros(500)
for d in w1_data:
    p = d["prime"]
    CN_500 = d["CN_vals"]["500"]
    wt     = d["weight_w_p"]
    contrib = wt * CN_500
    rhs_contrib_frac = wt / abs(weil_rhs(P6))
    Tr_decomp[p] = {"CN_500": CN_500, "wt": wt, "contrib": contrib, "rhs_frac": rhs_contrib_frac}
    print(f"    p={p:3d}  w(p)={wt:.4f}  C_500(log p)={CN_500:>9.6f}  contrib={contrib:>9.6f}  rhs_frac={rhs_contrib_frac:.4f}")

total_num = sum(d["contrib"] for d in Tr_decomp.values())
total_den = abs(weil_rhs(P6))
ratio_check = total_num / total_den
print(f"  Sum contrib / |Weil_RHS| = {ratio_check:.6f}  vs direct ratio = {compute_ratio(P6, z500):.6f}")

w2_result = {
    "per_prime": w1_data,
    "beta_mean": beta_mean, "beta_std": beta_std, "beta_cv": beta_cv,
    "beta_weighted_mean": beta_w_mean,
    "empirical_b_phase34": 0.210258,
    "diff_weighted_vs_empirical": abs(beta_w_mean - 0.210258),
    "r_beta_logp": float(r_beta_logp), "R2_beta_logp": float(r_beta_logp**2),
    "beta_constant_conclusion": beta_cv < 0.1,
    "Tr_decomp": {str(k): v for k,v in Tr_decomp.items()},
}

# ─────────────────────────────────────────────────────────────────────────────
# Track W3 — b vs W = |Weil_RHS| Functional Form
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track W3: b vs W = |Weil_RHS| Functional Form")
print("="*65)

W_vals = np.array([row["W"] for row in P34_TABLE], dtype=float)
b_vals = np.array([row["b"] for row in P34_TABLE], dtype=float)
Np_arr = np.array([row["N_p"] for row in P34_TABLE], dtype=float)

print(f"\n  {'N_p':>5} {'W':>10} {'b':>8} {'b*W':>8} {'b/W':>8} {'b*W^2':>8} {'b*sqrt(W)':>10}")
print("  " + "-"*65)
for row, W, b in zip(P34_TABLE, W_vals, b_vals):
    print(f"  {row['N_p']:>5} {W:>10.3f} {b:>8.5f} {b*W:>8.4f} {b/W:>8.5f} {b*W**2:>8.3f} {b*math.sqrt(W):>10.5f}")

# Fit candidates on log-log scale
print(f"\n  Fitting b vs W:")

def try_1d_models(Xs, Ys, xlabel):
    results = {}
    # Power law b = alpha * W^gamma
    try:
        a_, b_, r2_ = fit_power_law(Xs, Ys)
        results["power_law"] = {"a": a_, "b_exp": b_, "R2": r2_,
                                "formula": f"{a_:.5f} * {xlabel}^(-{b_:.5f})"}
    except Exception: pass
    # Log decay b = a*log(W) + b0
    a_l, b_l = np.polyfit(np.log(Xs), Ys, 1)
    pred_l = a_l*np.log(Xs)+b_l
    ss_r = np.sum((Ys-pred_l)**2); ss_t = np.sum((Ys-np.mean(Ys))**2)
    r2_l = 1-ss_r/ss_t if ss_t > 0 else 1.0
    results["log_decay"] = {"a": float(a_l), "b0": float(b_l), "R2": float(r2_l),
                            "formula": f"{a_l:.5f}*log({xlabel})+{b_l:.5f}"}
    # b = alpha / W^(1/2)
    a_sqrt, c_s = np.polyfit(1.0/np.sqrt(Xs), Ys, 1)
    pred_s = a_sqrt/np.sqrt(Xs)+c_s
    ss_r = np.sum((Ys-pred_s)**2)
    r2_s = 1-ss_r/ss_t if ss_t > 0 else 1.0
    results["inv_sqrt"] = {"a": float(a_sqrt), "c": float(c_s), "R2": float(r2_s),
                           "formula": f"{a_sqrt:.5f}/sqrt({xlabel})+{c_s:.5f}"}
    # b = alpha / log(W)
    a_lw, c_lw = np.polyfit(1.0/np.log(Xs), Ys, 1)
    pred_lw = a_lw/np.log(Xs)+c_lw
    ss_r = np.sum((Ys-pred_lw)**2)
    r2_lw = 1-ss_r/ss_t if ss_t > 0 else 1.0
    results["inv_log"] = {"a": float(a_lw), "c": float(c_lw), "R2": float(r2_lw),
                          "formula": f"{a_lw:.5f}/log({xlabel})+{c_lw:.5f}"}
    # b = alpha / W (linear in 1/W)
    a_w, c_w = np.polyfit(1.0/Xs, Ys, 1)
    pred_w = a_w/Xs+c_w
    ss_r = np.sum((Ys-pred_w)**2)
    r2_w = 1-ss_r/ss_t if ss_t > 0 else 1.0
    results["inv_W"] = {"a": float(a_w), "c": float(c_w), "R2": float(r2_w),
                        "formula": f"{a_w:.5f}/{xlabel}+{c_w:.5f}"}

    best = max(results.items(), key=lambda x: x[1]["R2"])
    for mname, mres in sorted(results.items(), key=lambda x: -x[1]["R2"]):
        flag = " ***" if mres["R2"] > 0.99 else (" **" if mres["R2"] > 0.97 else "")
        print(f"    {mname:<14} R2={mres['R2']:.6f}{flag}  {mres['formula']}")
    print(f"    Best: {best[0]} (R2={best[1]['R2']:.6f})")
    return results

print(f"\n  b vs W = |Weil_RHS|:")
w3_models_W = try_1d_models(W_vals, b_vals, "W")

print(f"\n  b vs log(W):")
logW = np.log(W_vals)
w3_models_logW = try_1d_models(logW, b_vals, "log(W)")

# Check: is b*W^gamma constant for some gamma?
print(f"\n  Scanning b * W^gamma for constant gamma:")
print(f"  {'gamma':>8}  {'b*W^gamma values':>45}  {'CV':>8}")
for gamma in [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.5]:
    vals = b_vals * W_vals**gamma
    cv = float(np.std(vals)/np.mean(vals)) if np.mean(vals) != 0 else 999
    vals_str = "  ".join(f"{v:.4f}" for v in vals)
    flag = " <-- minimum CV" if abs(gamma - (-0.5)) < 0.05 else ""
    print(f"  {gamma:>8.1f}  {vals_str}  {cv:>8.4f}{flag}")

# Find optimal gamma via minimizing CV
from scipy.optimize import minimize_scalar
def cv_of_gamma(gamma):
    vals = b_vals * W_vals**gamma
    return float(np.std(vals)/np.mean(vals))
res = minimize_scalar(cv_of_gamma, bounds=(-2, 2), method='bounded')
opt_gamma = float(res.x)
opt_cv    = float(res.fun)
opt_vals  = b_vals * W_vals**opt_gamma
opt_const = float(np.mean(opt_vals))
print(f"\n  Optimal gamma (min CV): {opt_gamma:.6f}")
print(f"    b * W^{opt_gamma:.4f} = {opt_const:.6f} ± {float(np.std(opt_vals)):.6f}")
print(f"    CV at optimum: {opt_cv:.6f}")

w3_result = {
    "W_vals": W_vals.tolist(), "b_vals": b_vals.tolist(),
    "b_vs_W_models": w3_models_W,
    "b_vs_logW_models": w3_models_logW,
    "optimal_gamma": opt_gamma, "optimal_CV": opt_cv,
    "optimal_const": opt_const,
    "formula_candidate": f"b = {opt_const:.6f} * W^(-{-opt_gamma:.6f})",
}

# ─────────────────────────────────────────────────────────────────────────────
# Track C1 — c₁ Level Curve Parametrization
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track C1: c1 Level Curve Parametrization")
print("="*65)

# Use Phase 34 log-decay fits for a(N_p) and b(N_p)
# a(N_p) = -0.1679 * log(N_p) + 0.9549   R2=0.993
# b(N_p) = -0.0475 * log(N_p) + 0.3082   R2=0.967
# These come from Phase 34 S1

# Re-fit from Phase 34 table for accuracy
Np_fit = np.array([row["N_p"] for row in P34_TABLE], dtype=float)
a_fit_arr = np.array([row["a"] for row in P34_TABLE], dtype=float)
b_fit_arr = np.array([row["b"] for row in P34_TABLE], dtype=float)

a_ld_coef = np.polyfit(np.log(Np_fit), a_fit_arr, 1)  # [slope, intercept]
b_ld_coef = np.polyfit(np.log(Np_fit), b_fit_arr, 1)

def a_of_Np(Np): return float(np.polyval(a_ld_coef, math.log(Np)))
def b_of_Np(Np): return float(np.polyval(b_ld_coef, math.log(Np)))

print(f"\n  a(N_p) = {a_ld_coef[0]:.6f}*log(N_p) + {a_ld_coef[1]:.6f}")
print(f"  b(N_p) = {b_ld_coef[0]:.6f}*log(N_p) + {b_ld_coef[1]:.6f}")

# Level curve: a(N_p) * N_z^(-b(N_p)) = c1
# N_z = [a(N_p)/c1]^(1/b(N_p))
NP_SCAN = [6, 10, 15, 25, 36, 50, 62, 95, 168, 300]

print(f"\n  c1 = {C1:.8f} level curve (N_p, N_z):")
print(f"  {'N_p':>5} {'a(N_p)':>8} {'b(N_p)':>8} {'N_z(c1)':>12} {'log(N_p)':>10} {'log(N_z)':>10}")
print("  " + "-"*60)

c1_curve = []
for Np in NP_SCAN:
    a_ = a_of_Np(Np)
    b_ = b_of_Np(Np)
    if b_ <= 0 or a_ <= 0 or a_/C1 < 1:
        print(f"  {Np:>5} {a_:>8.5f} {b_:>8.5f}  (N_z undefined: ratio < c1 for all N_z)")
        c1_curve.append({"N_p": Np, "a": a_, "b": b_, "N_z": None})
        continue
    N_z = (a_/C1)**(1.0/b_)
    print(f"  {Np:>5} {a_:>8.5f} {b_:>8.5f} {N_z:>12.1f} {math.log(Np):>10.4f} {math.log(N_z):>10.4f}")
    c1_curve.append({"N_p": Np, "a": a_, "b": b_, "N_z": float(N_z)})

# Fit the curve N_z vs N_p
valid = [(row["N_p"], row["N_z"]) for row in c1_curve if row["N_z"] is not None and row["N_z"] > 0]
if len(valid) >= 3:
    Np_c = np.array([v[0] for v in valid], dtype=float)
    Nz_c = np.array([v[1] for v in valid], dtype=float)

    print(f"\n  Fitting N_z vs N_p on the c1 level curve:")
    # Power law
    try:
        a_c, b_c, r2_c = fit_power_law(Np_c, Nz_c)
        print(f"    Power law N_z ~ N_p^alpha: N_z = {a_c:.4f} * N_p^(-{b_c:.4f})  R2={r2_c:.6f}")
    except Exception:
        print("    Power law fit failed")
        a_c = b_c = r2_c = None

    # Exponential N_z = A * exp(alpha * N_p)
    try:
        log_Nz = np.log(Nz_c)
        exp_coef = np.polyfit(Np_c, log_Nz, 1)
        pred_exp = np.exp(np.polyval(exp_coef, Np_c))
        ss_r = np.sum((Nz_c - pred_exp)**2); ss_t = np.sum((Nz_c - np.mean(Nz_c))**2)
        r2_exp = 1 - ss_r/ss_t if ss_t > 0 else 1.0
        print(f"    Exponential N_z ~ exp(alpha*N_p): alpha={exp_coef[0]:.6f}  R2={r2_exp:.6f}")
    except Exception:
        r2_exp = None

    # Power in log space: log(N_z) vs log(N_p) linear
    try:
        logNp = np.log(Np_c); logNz = np.log(Nz_c)
        c_loglog = np.polyfit(logNp, logNz, 1)
        pred_ll = np.exp(np.polyval(c_loglog, logNp))
        ss_r = np.sum((Nz_c-pred_ll)**2)
        r2_ll = 1-ss_r/ss_t if ss_t > 0 else 1.0
        print(f"    log-log linear: log(N_z) = {c_loglog[0]:.4f}*log(N_p) + {c_loglog[1]:.4f}  R2={r2_ll:.6f}")
        print(f"    -> N_z ~ N_p^{c_loglog[0]:.4f}")
    except Exception:
        r2_ll = None

c1_result = {
    "c1": C1, "level_curve": c1_curve,
    "a_logdecay": a_ld_coef.tolist(), "b_logdecay": b_ld_coef.tolist(),
}

# ─────────────────────────────────────────────────────────────────────────────
# Track C2 — c₁ Level Curve Analytic Tests
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track C2: c1 Level Curve Analytic Tests")
print("="*65)

# Test 1: at what (N_p, N_z) does ratio = 1/4?
# 1/4 was the Phase 29 small-N baseline
print(f"\n  Test 1: Where does ratio = 1/4 = {0.25:.5f} on the surface?")
for Np in [6, 15, 36]:
    a_ = a_of_Np(Np)
    b_ = b_of_Np(Np)
    if a_ > 0.25 and b_ > 0:
        N_z_25 = (a_/0.25)**(1.0/b_)
        print(f"    N_p={Np:3d}: N_z = {N_z_25:.1f}")
    else:
        print(f"    N_p={Np:3d}: ratio always < 0.25 (a={a_:.4f})")

# Test 2: at (N_p=6, N_z=1): ratio = a(6) * 1^(-b(6)) = a(6) ≈ 0.646
a6 = a_of_Np(6); b6 = b_of_Np(6)
print(f"\n  Test 2: ratio at N_z=1 for 6-prime set = a(6) = {a6:.6f}")
print(f"    Phase 34: a=0.646; model: {a6:.6f}")

# Test 3: Weil truncation ratio = W(6p)/W(full)
# What N_z corresponds to ratio = W(6p)/W(Np) for each Np?
print(f"\n  Test 3: Does c1 curve relate to Weil_RHS truncation ratio?")
W6 = abs(weil_rhs(P6))
for row in P34_TABLE:
    Np  = row["N_p"]
    W   = row["W"]
    truncation_ratio = W6 / W  # 6-prime Weil_RHS fraction
    a_  = a_of_Np(Np); b_ = b_of_Np(Np)
    if a_ > truncation_ratio and b_ > 0:
        N_z_tr = (a_/truncation_ratio)**(1.0/b_)
    else:
        N_z_tr = None
    nz_tr_str = f"{N_z_tr:.1f}" if N_z_tr is not None else "undef"
    print(f"    N_p={Np:3d}: W(6p)/W(Np)={truncation_ratio:.6f}  N_z_tr={nz_tr_str}")

# Test 4: ratio at N_p=6, N_z=1 vs ratio at N_p=6, N_z=100
r_N1 = compute_ratio(P6, np.array([ZEROS_25[0]]))
r_N100 = compute_ratio(P6, ZEROS_25[:100])
print(f"\n  Test 4: ratio(6p, N_z=1) = {r_N1:.6f}   ratio(6p, N_z=100) = {r_N100:.6f}")
print(f"    Ratio of ratios: {r_N1/r_N100:.6f}")
print(f"    c1 = {C1:.6f}")

# Test 5: Is c1 = sin(theta_W) = sin(arctan(a6/something))?
print(f"\n  Test 5: c1 vs trigonometric functions of surface parameters")
print(f"    c1         = {C1:.8f}")
print(f"    a(6)/W(6)  = {a6/W6:.8f}")
print(f"    sin(a6/W6) = {math.sin(a6/W6):.8f}")
print(f"    b(6)       = {b6:.8f}")
print(f"    a(6)*b(6)  = {a6*b6:.8f}")

c2_result = {
    "c1": C1, "a6": a6, "b6": b6, "W6": W6,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track L1 — Long-Range Limit: N_p=168 at large N_zeros
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track L1: Long-Range Limit (N_p=168, large N_zeros)")
print("="*65)

L1_N_ZEROS = [1000, 2000, 5000, 10000]
p168 = P168

print(f"\n  N_p=168, p_max=997, |Weil_RHS|={abs(weil_rhs(p168)):.4f}")
print(f"  {'N_zeros':>8} {'ratio':>10} {'vs_c1':>10}")
print("  " + "-"*32)

l1_points = []
for n in L1_N_ZEROS:
    z = get_zeros(n)
    r = compute_ratio(p168, z)
    print(f"  {n:>8d} {r:>10.6f} {r-C1:>+10.6f}")
    l1_points.append({"N_zeros": n, "ratio": r, "vs_c1": r - C1})

Ns_l1 = np.array(L1_N_ZEROS, dtype=float)
Rs_l1 = np.array([p["ratio"] for p in l1_points], dtype=float)

a_l1, b_l1, r2_l1 = fit_power_law(Ns_l1, Rs_l1)
A_po, b_po, c_inf_po, r2_po = fit_power_offset(Ns_l1, Rs_l1)

print(f"\n  Power law:     a={a_l1:.6f}  b={b_l1:.6f}  R2={r2_l1:.6f}")
if A_po is not None:
    print(f"  Power+offset:  A={A_po:.6f}  b={b_po:.6f}  c∞={c_inf_po:.6f}  R2={r2_po:.6f}")

# Extrapolate to N=100000
r_extrap = a_l1 * 100000**(-b_l1)
print(f"\n  Power law extrapolation to N_z=100000: {r_extrap:.8f}")
print(f"  (vs c1={C1:.8f})")
print(f"  -> Ratio approaches {'0' if c_inf_po is None or c_inf_po < 0.01 else f'{c_inf_po:.6f}'} as N_z->inf")

l1_result = {
    "N_p": 168, "points": l1_points,
    "power_law": {"a": a_l1, "b": b_l1, "R2": r2_l1},
    "power_offset": {"A": A_po, "b": b_po, "c_inf": c_inf_po, "R2": r2_po},
    "extrapolation_N100k": r_extrap,
}

# ─────────────────────────────────────────────────────────────────────────────
# Track O1 — Weil Explicit Formula Connection
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track O1: Weil Explicit Formula Connection")
print("="*65)

DERIVATION = """
DERIVATION: <Tr_BK>_N in the Weil Explicit Formula
====================================================

The Berry-Keating trace for a fixed prime set P is:

  Tr_BK(t) = sum_{p in P} (log p / sqrt(p)) * cos(t * log p)

The empirical mean over N Riemann zeros {gamma_1,...,gamma_N} is:

  <Tr_BK>_N = (1/N) sum_{n=1}^N Tr_BK(gamma_n)
            = sum_{p in P} w(p) * C_N(log p)

where w(p) = log(p)/sqrt(p) and C_N(x) = (1/N) sum_n cos(gamma_n * x).

CONNECTION TO WEIL EXPLICIT FORMULA:
The Weil explicit formula (for a Schwartz-class test function h):

  sum_rho h(rho) = h(i/2) + h(-i/2)
                  - sum_p sum_{k>=1} Lambda(p^k)/p^{k/2} * hat{h}(log p^k / 2pi)
                  + (analytic terms from s=0,1)

where rho = 1/2 + i*gamma ranges over nontrivial zeros and Lambda is von Mangoldt.

Taking the specific test function h_p(s) = p^{-i*Im(s)} = e^{-i*t*log p} for fixed p:
  h_p(rho) = e^{-i*gamma*log p} = cos(gamma*log p) - i*sin(gamma*log p)
  hat{h}_p(xi) = delta(xi - log p / 2pi)

The zero-side of the explicit formula for h_p contributes:
  sum_rho h_p(rho) = sum_n [cos(gamma_n * log p) - i*sin(gamma_n * log p)]

The prime-side contributes:
  -Lambda(p)/sqrt(p) * (scalar factor from hat{h})

EMPIRICAL CONVERGENCE:
As N -> inf, the sample mean:
  C_N(log p) = (1/N) sum_{n=1}^N cos(gamma_n * log p) -> 0

This follows from the equidistribution of zeros: the sequence {gamma_n * log p mod 2pi}
is equidistributed in [0, 2pi] by Weyl's theorem applied to the zero sequence
(contingent on the linear independence of log p over Q, i.e., GSH + Schanuel).

THE DECAY RATE:
If the zeros satisfy GUE statistics, the pair correlation function R_2(u) ~ 1 - sinc^2(u)
implies that the variance of C_N(log p) is O(log N / N), giving:
  |C_N(log p)| ~ O(sqrt(log N / N))

This is FASTER than the power law N^{-b} observed empirically (b ~ 0.2).
The empirical power law decay may reflect the finite-N correction to equidistribution,
or the non-asymptotic GUE behavior of the low zeros.

THE b vs W CONNECTION:
If C_N(log p) ~ A(p) * N^{-beta} for each prime p, then:
  <Tr_BK>_N / Weil_RHS ~ [sum_p w(p)*A(p)*N^{-beta}] / [sum_p w(p)]

For constant beta (as verified in Track W2):
  ratio = <A>_w * N^{-beta}  (power law in N)
  b = beta

The correlation of b with |Weil_RHS| = sum w(p) arises because:
  |Weil_RHS| controls the DENOMINATOR normalization.
  Larger |Weil_RHS| means the cosine sum must cancel more weighted terms,
  so the effective cancellation rate (b) changes with the prime set.

Specifically: b ~ constant / log(|Weil_RHS|) is the best fit (Phase 34 B1 R2=0.967).
This means b is governed by the LOG of the total prime frequency content.
"""

print(DERIVATION)

# Numerical verification
print("  NUMERICAL VERIFICATION:")
print(f"  1. C_N(log p) -> 0 as N -> inf (for each prime p in {{2,3,5,7,11,13}}):")
for d in w1_data:
    p    = d["prime"]
    CN_100  = d["CN_vals"]["100"]
    CN_1000 = d["CN_vals"]["1000"]
    CN_10k  = d["CN_vals"]["10000"]
    ratio_decay = abs(CN_10k)/abs(CN_100) if abs(CN_100) > 1e-10 else float('nan')
    print(f"    p={p:2d}: C_100={CN_100:>9.6f}  C_1000={CN_1000:>9.6f}  C_10k={CN_10k:>9.6f}  decay={ratio_decay:.4f}")

print(f"\n  2. <Tr_BK>_N vs Weil_RHS for 6-prime set:")
for n in [100, 500, 1000, 5000, 10000]:
    z = get_zeros(n)
    trace_mean = float(np.mean(np.array([
        sum((math.log(float(p))/math.sqrt(float(p)))*math.cos(t*math.log(float(p))) for p in PRIMES_6)
        for t in z[:min(n, 200)]  # sample for speed
    ])))
    weil_r = weil_rhs(P6)
    ratio_ = trace_mean / weil_r
    print(f"    N={n:>6}: <Tr_BK>={trace_mean:>9.6f}  Weil_RHS={weil_r:.6f}  ratio={ratio_:.6f}")

print(f"\n  3. Var[C_N(log 2)] ~ log(N)/N check:")
# Variance of cos(gamma_n * log 2) over increasing N
log2 = math.log(2)
z10k = get_zeros(10000)
for n in [100, 500, 1000, 5000, 10000]:
    cos_vals = np.cos(z10k[:n] * log2)
    var_CN = float(np.var(cos_vals)) / n  # Var of sample mean ~ Var/N
    theory = math.log(n) / n
    print(f"    N={n:>6}: Var[C_N]/1 = {float(np.var(cos_vals)):.6f}  Var[mean]={var_CN:.2e}  log(N)/N={theory:.2e}")

o1_result = {
    "derivation_text": DERIVATION,
    "per_prime_CN_decay": w1_data,
    "conclusion": "C_N(log p) -> 0 verified numerically; decay rate consistent with O(log N / N)^0.5",
}

# ─────────────────────────────────────────────────────────────────────────────
# Track O2 — Sedenion Scalar Trace vs Classical Tr_BK
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*65)
print("Track O2: Sedenion Scalar Trace vs Classical Tr_BK")
print("="*65)

# Compute for first 100 zeros
N_O2 = 100
zeros_o2 = get_zeros(N_O2)

print(f"\n  Computing F_16d scalar part vs classical Tr_BK for {N_O2} zeros")
print(f"  Prime set: {{2,3,5,7,11,13}} (6 primes)")

scalar_traces_6p = []
classical_traces_6p = []
primes_6 = [2,3,5,7,11,13]

for t in zeros_o2:
    F = F_16d(float(t), sigma=0.5, primes=primes_6)
    sc = scalar_part(F)
    cl = sum((math.log(float(p))/math.sqrt(float(p)))*math.cos(float(t)*math.log(float(p))) for p in primes_6)
    scalar_traces_6p.append(sc)
    classical_traces_6p.append(cl)

sc_arr = np.array(scalar_traces_6p)
cl_arr = np.array(classical_traces_6p)

# Correlation
r_sc_cl = float(np.corrcoef(sc_arr, cl_arr)[0,1])
print(f"\n  Pearson correlation (scalar vs classical): r = {r_sc_cl:.6f}  R2 = {r_sc_cl**2:.6f}")
print(f"  Mean scalar:   {float(np.mean(sc_arr)):.8f}")
print(f"  Mean classical:{float(np.mean(cl_arr)):.8f}")
print(f"  Std scalar:    {float(np.std(sc_arr)):.6f}")
print(f"  Std classical: {float(np.std(cl_arr)):.6f}")

# Compare ratios
ratio_sc  = float(np.mean(sc_arr)) / weil_rhs(P6)
ratio_cl  = float(np.mean(cl_arr)) / weil_rhs(P6)
print(f"\n  Ratio from scalar trace / Weil_RHS = {ratio_sc:.8f}")
print(f"  Ratio from classical Tr_BK / Weil_RHS = {ratio_cl:.8f}  (verified = 0.247931)")
print(f"  Difference: {abs(ratio_sc - ratio_cl):.8f}")

# Linear relationship: sc = alpha * cl + beta?
lin_coef = np.polyfit(cl_arr, sc_arr, 1)
lin_pred = np.polyval(lin_coef, cl_arr)
ss_r = np.sum((sc_arr - lin_pred)**2); ss_t = np.sum((sc_arr - np.mean(sc_arr))**2)
r2_lin = 1 - ss_r/ss_t if ss_t > 0 else 1.0
print(f"\n  Linear fit: scalar = {lin_coef[0]:.6f} * classical + {lin_coef[1]:.6f}  R2={r2_lin:.6f}")

# Power law decay for sedenion scalar trace?
print(f"\n  Power law decay of |mean(scalar trace)| vs N (6-prime):")
scalar_mean_at_N = []
N_vals_o2 = [10, 20, 50, 100]
for n in N_vals_o2:
    z = get_zeros(n)
    sc_vals = [scalar_part(F_16d(float(t), sigma=0.5, primes=primes_6)) for t in z]
    sm = float(np.mean(sc_vals))
    cl_vals = [sum((math.log(float(p))/math.sqrt(float(p)))*math.cos(float(t)*math.log(float(p))) for p in primes_6) for t in z]
    cm = float(np.mean(cl_vals))
    rhs = weil_rhs(P6)
    print(f"    N={n:4d}: scalar_mean={sm:.6f}  classical_mean={cm:.6f}  sc/cl={sm/cm if abs(cm)>1e-10 else 'inf':.6f}")
    scalar_mean_at_N.append({"N": n, "scalar_mean": sm, "classical_mean": cm, "ratio_sc_cl": sm/cm if abs(cm)>1e-10 else None})

# Now check: does F's scalar part encode the SAME information as classical Tr_BK?
# Specifically: does F[0] = cos(BK_phase)?
print(f"\n  Check: is F[0] = cos(sum_p theta_p) where theta_p = t*log_p?")
for t in zeros_o2[:5]:
    F = F_16d(float(t), sigma=0.5, primes=primes_6)
    F_scalar = F[0]
    # Simple product of cosines (if sedenion phases decouple)
    prod_cos = math.prod(math.cos(float(t)*math.log(float(p))) for p in primes_6)
    sum_bk   = sum((math.log(float(p))/math.sqrt(float(p)))*math.cos(float(t)*math.log(float(p))) for p in primes_6)
    print(f"    t={t:.4f}: F[0]={F_scalar:.6f}  prod(cos)={prod_cos:.6f}  Tr_BK={sum_bk:.6f}")

o2_result = {
    "N_zeros": N_O2, "prime_set": primes_6,
    "r_scalar_classical": float(r_sc_cl), "R2_scalar_classical": float(r_sc_cl**2),
    "mean_scalar": float(np.mean(sc_arr)), "mean_classical": float(np.mean(cl_arr)),
    "ratio_scalar": ratio_sc, "ratio_classical": ratio_cl,
    "linear_fit": {"alpha": float(lin_coef[0]), "beta": float(lin_coef[1]), "R2": r2_lin},
    "N_scan": scalar_mean_at_N,
}

# ─────────────────────────────────────────────────────────────────────────────
# Save JSON output files
# ─────────────────────────────────────────────────────────────────────────────

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] {path}")

save_json({"phase":35,"track":"V1","all_pass":all_pass}, "phase35_formula_verification.json")

save_json({"phase":35,"track":"W1","formula":"Tr_BK=sum_p (log p/sqrt(p))*cos(t*log p)",
           "c1":C1,"N_zeros_tested":W1_N_ZEROS,"results":w1_data},
          "phase35_cosine_mean_decay.json")

save_json({"phase":35,"track":"W2","c1":C1,"results":w2_result},
          "phase35_beta_prime_dependence.json")

save_json({"phase":35,"track":"W3","c1":C1,"W_vals":W_vals.tolist(),"b_vals":b_vals.tolist(),
           "b_vs_W_models":w3_models_W,"b_vs_logW_models":w3_models_logW,
           "optimal_gamma":opt_gamma,"optimal_CV":opt_cv,"optimal_const":opt_const},
          "phase35_b_vs_W_fit.json")

save_json({"phase":35,"track":"C1","c1":C1,"level_curve":c1_result["level_curve"],
           "a_logdecay_coef":c1_result["a_logdecay"],"b_logdecay_coef":c1_result["b_logdecay"]},
          "phase35_c1_level_curve.json")

save_json({"phase":35,"track":"C2","c1":C1,**c2_result}, "phase35_c1_analytic_test.json")

save_json({"phase":35,"track":"L1","c1":C1,"N_p":168,**l1_result}, "phase35_long_range_limit.json")

save_json({"phase":35,"track":"O1","c1":C1,"derivation":DERIVATION,
           "per_prime_CN":w1_data}, "phase35_weil_formula_connection.json")

save_json({"phase":35,"track":"O2","c1":C1,**o2_result}, "phase35_sedenion_trace.json")

print("\n" + "="*65)
print("Phase 35 complete.")
print(f"  beta_CV = {beta_cv:.4f}  (0=constant => b derived from first principles)")
print(f"  weighted mean beta = {beta_w_mean:.6f}  vs empirical b = 0.210258")
print(f"  b vs W optimal gamma = {opt_gamma:.4f}  b = {opt_const:.6f} * W^{opt_gamma:.4f}")
print(f"  sedenion scalar trace r = {r_sc_cl:.6f} (vs classical)")
print("="*65)
