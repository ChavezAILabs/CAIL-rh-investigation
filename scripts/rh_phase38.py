"""
rh_phase38.py
=============
Phase 38 -- Richer Inner Product + Scale Investigation + Weil Formula Revisit
RH Investigation -- Chavez AI Labs LLC

Date: 2026-03-27
Researcher: Paul Chavez, Chavez AI Labs LLC

Description
-----------
Four open directions from Phase 37:
  1. Richer M~_F: replace scalar_part with full sedenion norm (AIEX-146)
  2. e3+e12 preferred direction: why CS=91.1% on k=3 eigenvalue trajectory?
  3. Scale: is F[0]/lambda_max ~ 2 structurally (lambda_max = F[0]/2 theorem)?
  4. Weil formula: S(N) = sum(f5D(t_n)) was 99.3% aligned -- revisit as spectral det

Tracks:
  V1  -- Formula verification (canonical baseline)
  M1  -- Three richer M~_F definitions; eigenvalue matching
  M2  -- Non-scalar component structure (full 16D product analysis)
  S1  -- F[0]/lambda_max ratio test across 100 zeros
  S2  -- gamma_n as function of F[0] and lambda_k combinations
  E1  -- e3+e12 preferred direction column analysis
  W1  -- Weil formula spectral revisit (Phase 23T3)
  W2  -- f5D vs gamma_n; spectral determinant det5D
  A1  -- Reality characterization: random r_p vectors

Output files (9):
  phase38_formula_verification.json
  phase38_richer_MF.json
  phase38_nonscalar_structure.json
  phase38_scale_relationship.json
  phase38_gamma_from_MF.json
  phase38_b3_analysis.json
  phase38_weil_spectral.json
  phase38_f5d_gamma.json
  phase38_reality_characterization.json
"""

import numpy as np
from scipy.stats import spearmanr, pearsonr
from scipy.optimize import curve_fit
import json, time

# ============================================================
# SEDENION ENGINE (Phase 29/36/37 -- unchanged)
# ============================================================
def cd_conj(v):
    c = list(v); c[0] = v[0]
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0]*b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

def norm_sq(v): return sum(x * x for x in v)

def make16(pairs):
    v = [0.0] * 16
    for i, val in pairs: v[i] = float(val)
    return v

sqrt2 = np.sqrt(2.0)

ROOT_16D_BASE = {
    2:  make16([(3,  1.0), (12, -1.0)]),
    3:  make16([(5,  1.0), (10,  1.0)]),
    5:  make16([(3,  1.0), (6,   1.0)]),
    7:  make16([(2,  1.0), (7,  -1.0)]),
    11: make16([(2,  1.0), (7,   1.0)]),
    13: make16([(6,  1.0), (9,   1.0)]),
}

PRIMES = [2, 3, 5, 7, 11, 13]

def F_16d(t, sigma=0.5, primes=None):
    if primes is None: primes = PRIMES
    r = make16([(0, 1.0)])
    for p in primes:
        theta = t * np.log(p)
        rp = ROOT_16D_BASE[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16; f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# ============================================================
# (A1)^6 BASIS AND M_F CONSTRUCTION (Phase 36/37 -- unchanged)
# ============================================================
A1_6_BASIS = [
    make16([(1,  1), (14,  1)]),   # B0: e1+e14
    make16([(1,  1), (14, -1)]),   # B1: e1-e14
    make16([(2,  1), (13, -1)]),   # B2: e2-e13
    make16([(3,  1), (12,  1)]),   # B3: e3+e12  <- k=3 high CS direction
    make16([(4,  1), (11,  1)]),   # B4: e4+e11
    make16([(5,  1), (10,  1)]),   # B5: e5+e10 (= q2, Heegner)
]
A1_6_LABELS = ['e1+e14', 'e1-e14', 'e2-e13', 'e3+e12', 'e4+e11', 'e5+e10']

def compute_M_F(F_vec, basis=A1_6_BASIS):
    """M_F[i][j] = scalar_part(P_i * (F * P_j)) / (-2)  [Phase 36 definition]"""
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            M[i, j] = cd_mul(basis[i], FPj)[0] / (-2.0)
    return M

def compute_full_products(F_vec, basis=A1_6_BASIS):
    """Return 6x6 array of full 16D product vectors: prod[i][j] = P_i * (F * P_j)"""
    prods = [[None]*6 for _ in range(6)]
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            prods[i][j] = cd_mul(basis[i], FPj)
    return prods

def get_iA(F_vec):
    """Extract anti-symmetric part A = M_F - F[0]*I, return iA (Phase 37)."""
    MF = compute_M_F(F_vec)
    F0 = F_vec[0]
    A = MF - F0 * np.eye(6)
    iA = 1j * A
    return MF, F0, A, iA

def conjugation_symmetry(x):
    n = len(x)
    if n < 2: return 1.0
    return 1.0 - float(np.mean([abs(x[i] - x[n-1-i]) for i in range(n//2)]))

# f5D: 5D sedenion bilateral projection sum (Phase 23T3 / Phase 28)
# prime -> root map: p=2->q4, p=3->q2, p=5->v5, p=7->v1, p=11->v4, p=13->q3
PRIME_ROOT_MAP = {
    2:  make16([(4, 1), (11, 1)]),   # q4 = e4+e11
    3:  make16([(5, 1), (10, 1)]),   # q2 = e5+e10
    5:  make16([(3, 1), (6,  1)]),   # v5 = e3+e6 (from ROOT_16D_BASE[5])  -- wait, let me use correct
    7:  make16([(2, 1), (7, -1)]),   # v1 = e2-e7  (ROOT_16D_BASE[7])
    11: make16([(2, 1), (7,  1)]),   # v4 = e2+e7  (ROOT_16D_BASE[11])
    13: make16([(6, 1), (9,  1)]),   # q3 = e6+e9  (ROOT_16D_BASE[13])
}

def f5D(t):
    """?_p (log p / sqrt(p)) * cos(t * log p) -- Berry-Keating Tr_BK / sum over 6 primes"""
    return sum(np.log(p) / np.sqrt(p) * np.cos(t * np.log(p)) for p in PRIMES)

def weil_rhs():
    """Weil RHS = -?_p log(p)/sqrt(p) (the f5D(0) term with sign)"""
    return -sum(np.log(p) / np.sqrt(p) for p in PRIMES)

# ============================================================
# DATA LOAD
# ============================================================
print("=" * 60)
print("PHASE 38 -- Richer Inner Product + Scale + Weil Spectral")
print("=" * 60)
t0_total = time.time()

with open('rh_zeros.json') as f:
    zeros_raw = json.load(f)
zeros_100 = [float(z) for z in zeros_raw[:100]]
zeros_50  = [float(z) for z in zeros_raw[:50]]
zeros_10  = [float(z) for z in zeros_raw[:10]]
gamma_1   = zeros_100[0]
c1 = 0.11797805192095003
print(f"Loaded {len(zeros_100)} zeros  gamma_1={gamma_1:.6f}")

# Precompute F vectors for 100 zeros
print("Precomputing F vectors for 100 zeros...")
t0 = time.time()
F_vecs_100 = [F_16d(g) for g in zeros_100]
print(f"  Done in {time.time()-t0:.1f}s")

# ============================================================
# TRACK V1 -- FORMULA VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("TRACK V1 -- Formula Verification")
print("=" * 60)

F1 = F_vecs_100[0]
MF1, F0_1, A1_mat, iA1 = get_iA(F1)
evals_iA1 = sorted(np.linalg.eigvalsh(iA1).real)
antisym_check = float(np.max(np.abs(A1_mat + A1_mat.T)))
print(f"F[0] at gamma_1 = {F0_1:.8f}")
print(f"max |A+A^T|     = {antisym_check:.2e}  (expect 0)")
print(f"iA eigenvalues  = {[round(e, 6) for e in evals_iA1]}")
print(f"lambda_max      = {max(abs(e) for e in evals_iA1):.6f}")
print(f"F[0]/lambda_max = {F0_1/max(abs(e) for e in evals_iA1):.6f}  (check if ~2)")

v1_results = {
    "phase": 38, "track": "V1",
    "F0_gamma1": float(F0_1),
    "A_antisymmetry_check": antisym_check,
    "iA_eigenvalues_gamma1": [float(e) for e in evals_iA1],
    "lambda_max_gamma1": float(max(abs(e) for e in evals_iA1)),
    "F0_over_lambda_max": float(F0_1 / max(abs(e) for e in evals_iA1)),
    "gamma_1": gamma_1,
}
with open('phase38_formula_verification.json', 'w') as f:
    json.dump(v1_results, f, indent=2)
print("Saved phase38_formula_verification.json")

# ============================================================
# TRACK M1 -- THREE RICHER M~_F DEFINITIONS
# ============================================================
print("\n" + "=" * 60)
print("TRACK M1 -- Three Richer M~_F Definitions")
print("=" * 60)

def compute_M_tilde_full(F_vec, basis=A1_6_BASIS):
    """Candidate 1: M~[i][j] = norm^2(P_i * (F * P_j))"""
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            prod = cd_mul(basis[i], FPj)
            M[i, j] = norm_sq(prod)
    return M

def compute_M_nonscalar(F_vec, basis=A1_6_BASIS):
    """Candidate 2: M_ns[i][j] = sum of squares of components 1..15 (skip e0)"""
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            prod = cd_mul(basis[i], FPj)
            M[i, j] = sum(prod[k]**2 for k in range(1, 16))
    return M

def compute_M_component_k(F_vec, k_comp, basis=A1_6_BASIS):
    """Candidate 3: M_k[i][j] = component k of P_i * (F * P_j)"""
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            prod = cd_mul(basis[i], FPj)
            M[i, j] = prod[k_comp]
    return M

def eigenvalue_match_tests(evals_list, gammas, label):
    """Run E2a/b/c matching tests on eigenvalue list vs gammas."""
    # E2a: direct match
    tol = 1e-6
    matches_direct = 0
    for g in gammas:
        for ev in evals_list:
            if abs(abs(ev) - g) < tol:
                matches_direct += 1
    # E2b: scaled match (best c per zero)
    c_values = []
    for g, evs in zip(gammas, evals_list if hasattr(evals_list[0], '__len__') else [[e] for e in evals_list]):
        max_ev = max(abs(e) for e in evs) if hasattr(evs, '__len__') else abs(evs)
        if max_ev > 1e-12:
            c_values.append(g / max_ev)
    if c_values:
        c_mean = float(np.mean(c_values))
        c_std  = float(np.std(c_values))
        c_cv   = c_std / c_mean if c_mean > 0 else float('inf')
    else:
        c_mean = c_std = c_cv = float('nan')
    return {"E2a_direct_matches": matches_direct, "E2b_c_mean": c_mean,
            "E2b_c_std": c_std, "E2b_cv": c_cv}

print("Computing M~_F for three candidates across 50 zeros...")
t0_m1 = time.time()

richer_results = {}
gammas_50 = zeros_50

# For each candidate, store max eigenvalue per zero
for cand_name, compute_fn in [
    ("full_norm_sq",  compute_M_tilde_full),
    ("nonscalar_norm", compute_M_nonscalar),
]:
    max_evals = []
    all_evals = []
    for g, F_vec in zip(gammas_50, F_vecs_100[:50]):
        M = compute_fn(F_vec)
        evals = np.linalg.eigvalsh(M)
        max_evals.append(float(np.max(np.abs(evals))))
        all_evals.append([float(e) for e in sorted(evals)])

    c_values = [g / me for g, me in zip(gammas_50, max_evals) if me > 1e-12]
    c_mean = float(np.mean(c_values))
    c_std  = float(np.std(c_values))
    c_cv   = c_std / c_mean if c_mean > 0 else float('inf')
    rho_spearman, p_spearman = spearmanr(gammas_50, max_evals)

    richer_results[cand_name] = {
        "max_eigenvalue_range": [float(min(max_evals)), float(max(max_evals))],
        "gamma_range": [float(min(gammas_50)), float(max(gammas_50))],
        "scale_gap_factor_min": float(min(gammas_50)/max(max_evals)) if max(max_evals)>0 else None,
        "E2b_c_mean": c_mean, "E2b_c_std": c_std, "E2b_cv": c_cv,
        "E2c_spearman_rho": float(rho_spearman), "E2c_p_value": float(p_spearman),
        "first5_max_eigenvalues": max_evals[:5],
        "first5_gammas": gammas_50[:5],
        "eigenvalues_first3": all_evals[:3],
    }
    print(f"  {cand_name}: lambda_max range [{min(max_evals):.3f}, {max(max_evals):.3f}]  "
          f"gamma range [{min(gammas_50):.1f}, {max(gammas_50):.1f}]")
    print(f"    E2b CV={c_cv:.3f}  E2c Spearman rho={rho_spearman:.4f} p={p_spearman:.4f}")

# Candidate 3: find which single component k (1..15) gives best scale
print("\n  Candidate 3 -- scanning single components k=1..15 for best scale match...")
best_k = -1; best_c_cv = float('inf'); best_rho = 0.0
comp_scan = {}
for k in range(1, 16):
    max_evals_k = []
    for g, F_vec in zip(gammas_50, F_vecs_100[:50]):
        M = compute_M_component_k(F_vec, k)
        evals = np.linalg.eigvalsh(M)
        max_evals_k.append(float(np.max(np.abs(evals))))
    c_vals_k = [g / me for g, me in zip(gammas_50, max_evals_k) if me > 1e-12]
    if not c_vals_k:
        comp_scan[k] = {"c_cv": float('inf'), "spearman_rho": 0.0, "max_eval_range": [0, 0]}
        continue
    c_cv_k = float(np.std(c_vals_k) / np.mean(c_vals_k)) if np.mean(c_vals_k) > 0 else float('inf')
    rho_k, _ = spearmanr(gammas_50, max_evals_k)
    comp_scan[k] = {
        "c_cv": float(c_cv_k),
        "spearman_rho": float(rho_k),
        "max_eval_range": [float(min(max_evals_k)), float(max(max_evals_k))],
        "c_mean": float(np.mean(c_vals_k)),
    }
    if c_cv_k < best_c_cv:
        best_c_cv = c_cv_k; best_k = k; best_rho = float(rho_k)
    print(f"    k={k:2d}: CV={c_cv_k:.3f}  rho={rho_k:.4f}  "
          f"lambda_max=[{min(max_evals_k):.2f},{max(max_evals_k):.2f}]")

richer_results["component_scan"] = comp_scan
richer_results["best_single_component"] = {
    "k": best_k, "cv": best_c_cv, "spearman_rho": best_rho
}
print(f"\n  Best single component: k={best_k}  CV={best_c_cv:.3f}  rho={best_rho:.4f}")
print(f"M1 done in {time.time()-t0_m1:.1f}s")

with open('phase38_richer_MF.json', 'w') as f:
    json.dump(richer_results, f, indent=2)
print("Saved phase38_richer_MF.json")

# ============================================================
# TRACK M2 -- NON-SCALAR COMPONENT STRUCTURE
# ============================================================
print("\n" + "=" * 60)
print("TRACK M2 -- Non-Scalar Component Structure (10 zeros)")
print("=" * 60)

# For each of 10 zeros, compute the full 16D product P_i*(F*P_j) for all (i,j)
# Analyze: which components (1..15) carry variance across the 10 zeros?
component_data = {}  # (i,j) -> list of 16D vectors across 10 zeros
all_products = []    # shape: (10, 6, 6, 16)

for n, (g, F_vec) in enumerate(zip(zeros_10, F_vecs_100[:10])):
    prods = compute_full_products(F_vec)
    all_products.append(prods)

# For each (i,j) pair, compute variance across 10 zeros for each component
component_variance = np.zeros((6, 6, 16))  # [i, j, k]
component_mean_abs = np.zeros((6, 6, 16))

for i in range(6):
    for j in range(6):
        vals = np.array([[all_products[n][i][j][k] for k in range(16)]
                         for n in range(10)])  # shape (10, 16)
        component_variance[i, j] = np.var(vals, axis=0)
        component_mean_abs[i, j] = np.mean(np.abs(vals), axis=0)

# Aggregate: which component index (0..15) has highest total variance across all (i,j)?
total_var_per_component = component_variance.sum(axis=(0, 1))  # shape (16,)
total_mean_per_component = component_mean_abs.mean(axis=(0, 1))

print("Total variance per component (summed over all (i,j) pairs):")
for k in range(16):
    print(f"  k={k:2d}: total_var={total_var_per_component[k]:.6f}  mean_abs={total_mean_per_component[k]:.6f}")

# For each component k, compute Spearman correlation with gamma
gammas_10 = zeros_10
corr_with_gamma = {}
for k in range(1, 16):
    # Correlation of diagonal elements (i=j) with gamma_n
    diag_vals = [np.mean([abs(all_products[n][i][i][k]) for i in range(6)])
                 for n in range(10)]
    if np.std(diag_vals) > 1e-12:
        rho_k, p_k = spearmanr(gammas_10, diag_vals)
    else:
        rho_k, p_k = 0.0, 1.0
    corr_with_gamma[k] = {"spearman_rho": float(rho_k), "p_value": float(p_k),
                           "mean_diag_abs": float(np.mean(diag_vals))}

# Find top 3 components by variance (skip k=0)
top_comps = sorted(range(1, 16), key=lambda k: -total_var_per_component[k])[:5]
print(f"\nTop 5 non-scalar components by total variance: {top_comps}")
for k in top_comps:
    print(f"  k={k}: var={total_var_per_component[k]:.6f}  "
          f"rho_with_gamma={corr_with_gamma[k]['spearman_rho']:.4f}")

# Sample: full product for (i=0,j=0) at gamma_1
sample_prod = all_products[0][0][0]
print(f"\nSample P0*(F*P0) at gamma_1 (full 16D):\n  {[round(x,6) for x in sample_prod]}")
print(f"Scalar part (k=0): {sample_prod[0]:.6f}  (= M_F[0,0]*(-2)={-2*compute_M_F(F_vecs_100[0])[0,0]:.6f})")

m2_results = {
    "phase": 38, "track": "M2",
    "n_zeros": 10,
    "total_variance_per_component": [float(x) for x in total_var_per_component],
    "mean_abs_per_component": [float(x) for x in total_mean_per_component],
    "top5_components_by_variance": top_comps,
    "correlation_with_gamma": {str(k): v for k, v in corr_with_gamma.items()},
    "sample_product_P0_F_P0_gamma1": [float(x) for x in sample_prod],
}
with open('phase38_nonscalar_structure.json', 'w') as f:
    json.dump(m2_results, f, indent=2)
print("Saved phase38_nonscalar_structure.json")

# ============================================================
# TRACK S1 -- F[0]/LAMBDA_MAX RATIO TEST
# ============================================================
print("\n" + "=" * 60)
print("TRACK S1 -- F[0]/lambda_max Ratio Test (100 zeros)")
print("=" * 60)

F0_vals = []
lambda_max_vals = []
ratio_vals = []  # F[0] / lambda_max

for g, F_vec in zip(zeros_100, F_vecs_100):
    MF, F0, A, iA = get_iA(F_vec)
    evals = np.linalg.eigvalsh(iA).real
    lam_max = float(np.max(np.abs(evals)))
    F0_vals.append(float(F0))
    lambda_max_vals.append(lam_max)
    if lam_max > 1e-12:
        ratio_vals.append(F0 / lam_max)
    else:
        ratio_vals.append(float('nan'))

ratio_clean = [r for r in ratio_vals if not np.isnan(r)]
r_mean = float(np.mean(ratio_clean))
r_std  = float(np.std(ratio_clean))
r_cv   = r_std / abs(r_mean) if abs(r_mean) > 1e-12 else float('inf')
rho_F0_lam, p_F0_lam = spearmanr(F0_vals, lambda_max_vals)
rho_ratio_gamma, p_ratio_gamma = spearmanr(zeros_100, ratio_clean[:100] if len(ratio_clean) >= 100 else ratio_clean)

print(f"F[0]/lambda_max: mean={r_mean:.6f}  std={r_std:.6f}  CV={r_cv:.4f}")
print(f"  (CV < 0.1 -> theorem candidate; CV >= 0.1 -> not structural)")
print(f"Spearman(F0, lambda_max): rho={rho_F0_lam:.4f}  p={p_F0_lam:.4f}")
print(f"Spearman(gamma_n, ratio): rho={rho_ratio_gamma:.4f}  p={p_ratio_gamma:.4f}")
print(f"First 5 ratios: {[round(r, 4) for r in ratio_vals[:5]]}")

s1_results = {
    "phase": 38, "track": "S1",
    "F0_over_lambda_max_mean": r_mean,
    "F0_over_lambda_max_std": r_std,
    "F0_over_lambda_max_cv": r_cv,
    "theorem_candidate": bool(r_cv < 0.1),
    "spearman_F0_lambda": float(rho_F0_lam), "p_F0_lambda": float(p_F0_lam),
    "spearman_ratio_gamma": float(rho_ratio_gamma), "p_ratio_gamma": float(p_ratio_gamma),
    "ratio_values_100": [float(r) for r in ratio_vals],
    "F0_values_100": F0_vals,
    "lambda_max_values_100": lambda_max_vals,
}
with open('phase38_scale_relationship.json', 'w') as f:
    json.dump(s1_results, f, indent=2)
print("Saved phase38_scale_relationship.json")

# ============================================================
# TRACK S2 -- GAMMA FROM M_F COMBINATIONS
# ============================================================
print("\n" + "=" * 60)
print("TRACK S2 -- gamma_n as Function of F[0] and lambda Combinations")
print("=" * 60)

gammas = np.array(zeros_100, dtype=float)
F0_arr = np.array(F0_vals)
lam_arr = np.array(lambda_max_vals)

def test_fit(name, x, y):
    """Fit y = c * x, return c, R^2, residual."""
    # linear through origin
    c = float(np.dot(x, y) / np.dot(x, x))
    y_hat = c * x
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1.0 - ss_res/ss_tot if ss_tot > 1e-12 else 0.0
    rho, p = pearsonr(x, y)
    print(f"  {name}: c={c:.4f}  R^2={r2:.4f}  Pearson r={rho:.4f} p={p:.4f}")
    return {"name": name, "c": float(c), "R_sq": float(r2),
            "pearson_r": float(rho), "p_value": float(p)}

fits = []

# Test 1: gamma_n ~ c * F[0]
fits.append(test_fit("gamma ~ c * F[0]", F0_arr, gammas))

# Test 2: gamma_n ~ c * lambda_max
fits.append(test_fit("gamma ~ c * lambda_max", lam_arr, gammas))

# Test 3: gamma_n ~ c * (F[0] + lambda_max)
fits.append(test_fit("gamma ~ c * (F[0]+lambda_max)", F0_arr + lam_arr, gammas))

# Test 4: gamma_n ~ c * F[0]^2 / lambda_max
safe_mask = lam_arr > 1e-12
x4 = F0_arr[safe_mask]**2 / lam_arr[safe_mask]
fits.append(test_fit("gamma ~ c * F[0]^2/lambda_max", x4, gammas[safe_mask]))

# Test 5: gamma_n ~ c * F[0] * lambda_max
fits.append(test_fit("gamma ~ c * F[0]*lambda_max", F0_arr * lam_arr, gammas))

# Test 6: gamma_n ~ c * 1/F[0]
fits.append(test_fit("gamma ~ c * 1/F[0]", 1.0/F0_arr, gammas))

# Test 7: gamma_n ~ c * 1/lambda_max
fits.append(test_fit("gamma ~ c / lambda_max", 1.0/lam_arr[safe_mask], gammas[safe_mask]))

# Find best fit
best_fit = max(fits, key=lambda x: x['R_sq'])
print(f"\nBest fit: {best_fit['name']}  R^2={best_fit['R_sq']:.4f}")

s2_results = {
    "phase": 38, "track": "S2",
    "fits": fits,
    "best_fit": best_fit,
}
with open('phase38_gamma_from_MF.json', 'w') as f:
    json.dump(s2_results, f, indent=2)
print("Saved phase38_gamma_from_MF.json")

# ============================================================
# TRACK E1 -- e3+e12 PREFERRED DIRECTION (B3)
# ============================================================
print("\n" + "=" * 60)
print("TRACK E1 -- B3 = e3+e12 Preferred Direction Analysis")
print("=" * 60)

# For each of 100 zeros, compute the full product P_i*(F*P_j) for j=3 (B3=e3+e12)
# Compare CS of each column j's product norm sequence
print("Computing column CS for each of 6 (A1)^6 basis directions across 100 zeros...")

col_norms = np.zeros((6, 100))   # col_norms[j][n] = norm_sq of F*P_j at zero n
col_scalar = np.zeros((6, 100))  # scalar part of F*P_j

for n, F_vec in enumerate(F_vecs_100):
    for j in range(6):
        FPj = cd_mul(F_vec, A1_6_BASIS[j])
        col_norms[j, n] = float(norm_sq(FPj))
        col_scalar[j, n] = float(FPj[0])

# CS for each column norm sequence and scalar sequence
col_cs_norm = [conjugation_symmetry(col_norms[j]) for j in range(6)]
col_cs_scalar = [conjugation_symmetry(col_scalar[j]) for j in range(6)]

print("\nCS of ||F*P_j||^2 sequence (100 zeros):")
for j, (lab, cs_n, cs_s) in enumerate(zip(A1_6_LABELS, col_cs_norm, col_cs_scalar)):
    print(f"  j={j} ({lab}): CS(norm^2)={cs_n:.4f}  CS(scalar)={cs_s:.4f}"
          + (" <- B3" if j == 3 else ""))

# Also: for B3 column specifically, compute the full M~_F[i][3] (non-scalar norms)
b3_col_data = {}
for n, F_vec in enumerate(zip(zeros_100)):
    pass  # already have col_norms

# Row-wise analysis: does row i=3 also elevate?
row_norms = np.zeros((6, 100))
for n, F_vec in enumerate(F_vecs_100):
    for i in range(6):
        # Compute P_i * (F * P_j) for all j; take sum of products with B3 row
        FP3 = cd_mul(F_vec, A1_6_BASIS[3])
        Pi_FP3 = cd_mul(A1_6_BASIS[i], FP3)
        row_norms[i, n] = float(norm_sq(Pi_FP3))

row_cs = [conjugation_symmetry(row_norms[i]) for i in range(6)]
print("\nCS of ||P_i*(F*B3)||^2 sequence (rows using B3 column):")
for i, (lab, cs) in enumerate(zip(A1_6_LABELS, row_cs)):
    print(f"  i={i} ({lab}): CS={cs:.4f}" + (" <- B3" if i == 3 else ""))

# Heegner direction B5 = q2: does it also elevate?
b5_col_norms = col_norms[5]
b5_cs = conjugation_symmetry(b5_col_norms)
print(f"\nB5 (q2=e5+e10, Heegner) column norm CS = {b5_cs:.4f}")
print(f"B3 (e3+e12) column norm CS              = {col_cs_norm[3]:.4f}")

# Spearman correlation of B3 col norm with gamma
rho_b3, p_b3 = spearmanr(zeros_100, col_norms[3])
rho_b5, p_b5 = spearmanr(zeros_100, col_norms[5])
print(f"\nSpearman(B3 col norm, gamma): rho={rho_b3:.4f} p={p_b3:.4f}")
print(f"Spearman(B5 col norm, gamma): rho={rho_b5:.4f} p={p_b5:.4f}")

e1_results = {
    "phase": 38, "track": "E1",
    "column_cs_norm_sq": [float(x) for x in col_cs_norm],
    "column_cs_scalar": [float(x) for x in col_cs_scalar],
    "row_cs_b3_column": [float(x) for x in row_cs],
    "basis_labels": A1_6_LABELS,
    "b3_index": 3,
    "b5_index": 5,
    "spearman_b3_vs_gamma": float(rho_b3), "p_b3": float(p_b3),
    "spearman_b5_vs_gamma": float(rho_b5), "p_b5": float(p_b5),
    "max_col_cs": float(max(col_cs_norm)), "max_col_index": int(np.argmax(col_cs_norm)),
}
with open('phase38_b3_analysis.json', 'w') as f:
    json.dump(e1_results, f, indent=2)
print("Saved phase38_b3_analysis.json")

# ============================================================
# TRACK W1 -- WEIL FORMULA SPECTRAL REVISIT
# ============================================================
print("\n" + "=" * 60)
print("TRACK W1 -- Weil Formula Spectral Revisit (Phase 23T3)")
print("=" * 60)

# Load 10k zeros for extended N
try:
    with open('rh_zeros_10k.json') as f:
        zeros_10k = [float(z) for z in json.load(f)]
    print(f"Loaded {len(zeros_10k)} zeros from rh_zeros_10k.json")
except FileNotFoundError:
    zeros_10k = zeros_100
    print("rh_zeros_10k.json not found, using first 100")

weil_rhs_val = weil_rhs()
print(f"Weil RHS = -sum(log p/sqrt(p)) = {weil_rhs_val:.8f}")

# Compute S(N) = sum_{n=1}^N f5D(t_n) for N in range
N_vals = [10, 20, 50, 100, 200, 500] if len(zeros_10k) >= 500 else [10, 20, 50, 100]
SN_vals = []
ratio_SN_RHS = []
cumsum = 0.0
cumulative = []
zero_list_for_w1 = zeros_10k

for n, t in enumerate(zero_list_for_w1[:max(N_vals)], 1):
    cumsum += f5D(t)
    cumulative.append(cumsum)

for N in N_vals:
    SN = cumulative[N-1]
    ratio = SN / weil_rhs_val if abs(weil_rhs_val) > 1e-12 else float('nan')
    SN_vals.append(float(SN))
    ratio_SN_RHS.append(float(ratio))
    print(f"  N={N:4d}: S(N)={SN:.6f}  ratio S(N)/Weil_RHS={ratio:.6f}")

# Per-zero f5D values
f5d_per_zero = [float(f5D(t)) for t in zeros_100]
rho_f5d_gamma, p_f5d_gamma = spearmanr(zeros_100, f5d_per_zero)
rho_f5d_pearson, p_pearson = pearsonr(zeros_100, f5d_per_zero)
print(f"\nSpearman(f5D(t_n), gamma_n): rho={rho_f5d_gamma:.4f} p={p_f5d_gamma:.4f}")
print(f"Pearson(f5D(t_n), gamma_n):  r={rho_f5d_pearson:.4f} p={p_pearson:.4f}")
print(f"f5D range: [{min(f5d_per_zero):.4f}, {max(f5d_per_zero):.4f}]")

# CS on S(N)/Weil_RHS ratio sequence
if len(ratio_SN_RHS) >= 4:
    cs_ratio_seq = conjugation_symmetry(ratio_SN_RHS)
    print(f"CS of ratio sequence: {cs_ratio_seq:.4f}")
else:
    cs_ratio_seq = float('nan')

w1_results = {
    "phase": 38, "track": "W1",
    "weil_rhs": float(weil_rhs_val),
    "N_vals": N_vals,
    "SN_vals": SN_vals,
    "ratio_SN_over_RHS": ratio_SN_RHS,
    "cs_ratio_sequence": float(cs_ratio_seq),
    "per_zero_f5d_spearman": float(rho_f5d_gamma), "p_f5d_gamma": float(p_f5d_gamma),
    "per_zero_f5d_pearson": float(rho_f5d_pearson),
    "f5d_first10": f5d_per_zero[:10],
    "gammas_first10": zeros_100[:10],
}
with open('phase38_weil_spectral.json', 'w') as f:
    json.dump(w1_results, f, indent=2)
print("Saved phase38_weil_spectral.json")

# ============================================================
# TRACK W2 -- f5D VS GAMMA + SPECTRAL DETERMINANT det5D
# ============================================================
print("\n" + "=" * 60)
print("TRACK W2 -- f5D vs gamma_n; Spectral Determinant det5D")
print("=" * 60)

# Test: f5D(t_n) ~ c * gamma_n? Or f5D(t_n) ~ c * log(gamma_n)?
f5d_arr = np.array(f5d_per_zero)
gamma_arr = np.array(zeros_100)
log_gamma_arr = np.log(gamma_arr)

def fit_c(x, y):
    c = float(np.dot(x, y) / np.dot(x, x))
    y_hat = c * x
    ss_res = np.sum((y - y_hat)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1.0 - ss_res/ss_tot if ss_tot > 1e-12 else 0.0
    return c, r2

# Only use f5D > 0 for log transform
pos_mask = f5d_arr > 0
c_linear, r2_linear = fit_c(gamma_arr, f5d_arr)
c_log, r2_log = fit_c(log_gamma_arr, f5d_arr)
print(f"f5D ~ c*gamma:     c={c_linear:.6f}  R^2={r2_linear:.4f}")
print(f"f5D ~ c*log(gamma): c={c_log:.6f}  R^2={r2_log:.4f}")

# Spectral determinant det5D(E) = prod_n (E - f5D(t_n))
# Does det5D(Weil_RHS) ? 0?  Or at least close relative to some scale?
# Evaluate at E = Weil_RHS and a few other test values
E_test_vals = [weil_rhs_val, 0.0, weil_rhs_val * 0.5, weil_rhs_val * 2.0]
E_test_labels = ["Weil_RHS", "0", "0.5*Weil_RHS", "2*Weil_RHS"]

# Use log-sum for stability: log|det| = sum log|E - f5D(t_n)|
det5D_logabs = {}
f5d_100 = np.array([f5D(t) for t in zeros_100])
for E, lab in zip(E_test_vals, E_test_labels):
    diffs = np.abs(E - f5d_100)
    # Check if any diff is near 0 (a zero of det5D)
    min_diff = float(np.min(diffs))
    log_abs_det = float(np.sum(np.log(diffs + 1e-300)))
    det5D_logabs[lab] = {
        "E": float(E), "log_abs_det5D": log_abs_det,
        "min_diff_to_f5d": min_diff
    }
    print(f"  E={lab}: log|det5D(E)|={log_abs_det:.4f}  min|E-f5D|={min_diff:.6f}")

# Find E that minimizes |det5D(E)| in the range of f5D values
# This is simply finding the f5D values themselves (they are the roots by construction)
# The question is: does f5D(t_n) show any structure as a function of n?
f5d_sorted = sorted(f5d_100)
print(f"\nf5D value range: [{f5d_sorted[0]:.4f}, {f5d_sorted[-1]:.4f}]")
print(f"f5D mean: {float(np.mean(f5d_100)):.4f}  std: {float(np.std(f5d_100)):.4f}")
print(f"f5D distribution: {sum(1 for x in f5d_100 if x < 0)} negative, {sum(1 for x in f5d_100 if x >= 0)} non-negative")

# CS of the f5D sequence (ordered by zero index n)
cs_f5d_seq = conjugation_symmetry(list(f5d_100))
print(f"CS of f5D(t_n) sequence (n=1..100): {cs_f5d_seq:.4f}")

w2_results = {
    "phase": 38, "track": "W2",
    "fit_f5d_vs_gamma_linear": {"c": c_linear, "R_sq": r2_linear},
    "fit_f5d_vs_log_gamma": {"c": c_log, "R_sq": r2_log},
    "det5D_at_test_points": det5D_logabs,
    "f5d_mean": float(np.mean(f5d_100)),
    "f5d_std": float(np.std(f5d_100)),
    "f5d_range": [float(min(f5d_100)), float(max(f5d_100))],
    "cs_f5d_sequence": float(cs_f5d_seq),
    "f5d_first20": [float(x) for x in f5d_100[:20]],
    "gammas_first20": zeros_100[:20],
    "weil_rhs": float(weil_rhs_val),
}
with open('phase38_f5d_gamma.json', 'w') as f:
    json.dump(w2_results, f, indent=2)
print("Saved phase38_f5d_gamma.json")

# ============================================================
# TRACK A1 -- REALITY CHARACTERIZATION
# ============================================================
print("\n" + "=" * 60)
print("TRACK A1 -- Reality Characterization: Random r_p Vectors")
print("=" * 60)

# Test: does F remain real when r_p vectors are RANDOM 16D unit vectors?
# If yes: Im(F)=0 is a universal sedenion algebra property
# If no: Im(F)=0 is specific to the E8 root geometry

def F_16d_custom_roots(t, sigma, roots_dict, primes=PRIMES):
    """F with custom r_p vectors (may not be E8 roots)."""
    r = make16([(0, 1.0)])
    for p in primes:
        theta = t * np.log(p)
        rp = roots_dict[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16; f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

rng = np.random.default_rng(42)
n_trials = 20
random_max_imag = []

print(f"Testing {n_trials} random 16D unit vector sets:")
for trial in range(n_trials):
    # Random unit 16D vectors for each prime
    random_roots = {}
    for p in PRIMES:
        v = rng.standard_normal(16)
        v = v / np.linalg.norm(v)
        # Make into list for sedenion engine
        random_roots[p] = list(v)
    F_rand = F_16d_custom_roots(gamma_1, 0.5, random_roots)
    max_imag = max(abs(complex(x).imag) for x in F_rand)
    random_max_imag.append(float(max_imag))

print(f"  Max |Im(F)| with random roots: {random_max_imag[:5]}")
print(f"  All-zero? {all(x == 0.0 for x in random_max_imag)}")
print(f"  Max across {n_trials} trials: {max(random_max_imag):.6e}")

# Also test: integer vs non-integer components
print("\nTesting non-integer components in r_p (but still real):")
rp_nonint = {p: [float(v) for v in rng.standard_normal(16)] for p in PRIMES}
F_nonint = F_16d_custom_roots(gamma_1, 0.5, rp_nonint)
max_imag_nonint = max(abs(complex(x).imag) for x in F_nonint)
print(f"  Max |Im(F)| with non-integer real r_p: {max_imag_nonint:.6e}")

# Test: what if r_p has imaginary components? (not physically meaningful, sanity check)
# We skip this as it would require complex sedenion engine

# Characterize the theorem:
# F_16d() uses cos(theta)*e0 + sin(theta)*r_p/||r_p||
# Both theta and r_p are real => all components of each factor are real
# Product of real-component lists => all components real
# => Im(F) = 0 is a UNIVERSAL property of the sedenion exponential with real inputs
# NOT specific to E8 root directions

print("\nConclusion: Im(F)=0 is universal for real r_p inputs.")
print("The sedenion multiplication of real-component vectors gives real-component output.")
print("This is a property of the algebra (Cayley-Dickson), not the E8 geometry.")

a1_results = {
    "phase": 38, "track": "A1",
    "n_trials": n_trials,
    "random_max_imag_all_zero": all(x == 0.0 for x in random_max_imag),
    "random_max_imag_values": random_max_imag,
    "max_imag_nonint_real_rp": float(max_imag_nonint),
    "conclusion": (
        "Im(F)=0 is UNIVERSAL: holds for any real-valued r_p vectors, not just E8 roots. "
        "The Cayley-Dickson product of real-component sedenions is always real-component. "
        "Reality of F is an algebraic property of the construction (real inputs -> real output), "
        "completely independent of the E8/A1^6 geometry."
    ),
    "implication": (
        "The Phase 36 hermiticity PASS is structurally trivial. "
        "The E8 geometry is NOT what makes F real. "
        "Any 6-prime AIEX-001a with real r_p vectors would give hermiticity PASS. "
        "This closes the reality-condition proof path definitively."
    ),
}
with open('phase38_reality_characterization.json', 'w') as f:
    json.dump(a1_results, f, indent=2)
print("Saved phase38_reality_characterization.json")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PHASE 38 SUMMARY")
print("=" * 60)
total_time = time.time() - t0_total

print(f"\nTrack M1 (Richer M~_F):")
for name in ["full_norm_sq", "nonscalar_norm"]:
    r = richer_results[name]
    print(f"  {name}: lambda_max range {r['max_eigenvalue_range']}  "
          f"CV={r['E2b_cv']:.3f}  rho={r['E2c_spearman_rho']:.4f}")
print(f"  Best single component k={richer_results['best_single_component']['k']}  "
      f"CV={richer_results['best_single_component']['cv']:.3f}  "
      f"rho={richer_results['best_single_component']['spearman_rho']:.4f}")

print(f"\nTrack M2 (Non-scalar structure):")
print(f"  Top 5 variance components: {top_comps}")

print(f"\nTrack S1 (Scale relationship):")
print(f"  F[0]/lambda_max: mean={r_mean:.4f}  CV={r_cv:.4f}  "
      f"theorem_candidate={bool(r_cv < 0.1)}")

print(f"\nTrack S2 (gamma from M_F):")
print(f"  Best fit: {best_fit['name']}  R^2={best_fit['R_sq']:.4f}")

print(f"\nTrack E1 (B3 direction):")
print(f"  Column CS: {[round(x, 4) for x in col_cs_norm]}")
print(f"  Max CS direction: {A1_6_LABELS[int(np.argmax(col_cs_norm))]}  ({max(col_cs_norm):.4f})")

print(f"\nTrack W1 (Weil spectral):")
if ratio_SN_RHS:
    print(f"  S(N)/Weil_RHS at N={N_vals[-1]}: {ratio_SN_RHS[-1]:.6f}")

print(f"\nTrack W2 (f5D gamma):")
print(f"  f5D ~ c*gamma: R^2={r2_linear:.4f}  f5D ~ c*log(gamma): R^2={r2_log:.4f}")
print(f"  CS of f5D sequence: {cs_f5d_seq:.4f}")

print(f"\nTrack A1 (Reality):")
print(f"  Im(F)=0 universal: {all(x == 0.0 for x in random_max_imag)}")
print(f"  Conclusion: algebraic property of Cayley-Dickson, NOT E8-specific")

print(f"\nTotal elapsed: {total_time:.1f}s")
print("Phase 38 complete.")
