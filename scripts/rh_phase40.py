"""
rh_phase40.py
=============
Phase 40 -- Normalized Operator + Anti-Correlation Source + Eigenvalue Distribution
RH Investigation -- Chavez AI Labs LLC

Date: 2026-03-27
Researcher: Paul Chavez, Chavez AI Labs LLC

Pre-flight (A1) result: Spearman(||F||^2, gamma_n) = -0.084, p=0.41 -- NOT significant.
Anti-correlation rho~-0.4 is DIRECTIONAL, not amplitude-based.
Normalization tracks (A2, N1_norm) run as confirmatory, not primary.
Primary tracks pivot to D1 (full eigenvalue distribution) and S1 (correlated subspace).

Tracks:
  V1  -- Formula verification (||F||^2 at gamma_1, M_tilde baseline)
  A1  -- ||F||^2 vs gamma_n Spearman (pre-flight, already run -- document result)
  A2  -- M_norm baseline at N=6 (confirmatory: does normalization change rho?)
  D1  -- Full eigenvalue distribution at N=60, M_tilde (50 zeros)
  S1  -- Correlated subspace: top-k diagonal-correlated bilateral vectors
  N1  -- M_norm growing subspace (6,12,18,30,45,60); rho and density
  N2  -- Normalized eigenvalue density vs zero density at N=60
  W1  -- Weyl law target: required N formula
"""

import numpy as np
from scipy.stats import spearmanr
import json, time

# ============================================================
# SEDENION ENGINE (Phase 38/39 -- unchanged)
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
PRIMES_6 = [2, 3, 5, 7, 11, 13]

def F_16d(t, sigma=0.5, primes=None, root_base=None):
    if primes is None: primes = PRIMES_6
    if root_base is None: root_base = ROOT_16D_BASE
    r = make16([(0, 1.0)])
    for p in primes:
        theta = t * np.log(p)
        rp = root_base[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16; f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# (A1)^6 canonical basis (Phase 36/38/39, confirmed)
A1_6_BASIS = [
    make16([(1,  1.0), (14,  1.0)]),
    make16([(1,  1.0), (14, -1.0)]),
    make16([(2,  1.0), (13, -1.0)]),
    make16([(3,  1.0), (12,  1.0)]),
    make16([(4,  1.0), (11,  1.0)]),
    make16([(5,  1.0), (10,  1.0)]),
]

def compute_M_tilde(F_vec, basis):
    """M_tilde[i][j] = ||P_i * (F * P_j)||^2 (Phase 38 norm^2 definition)"""
    N = len(basis)
    FPj = [cd_mul(F_vec, basis[j]) for j in range(N)]
    M = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            prod = cd_mul(basis[i], FPj[j])
            M[i, j] = norm_sq(prod)
    return M

def compute_M_norm(F_vec, basis):
    """M_norm[i][j] = ||P_i * (F * P_j)||^2 / ||F||^2 (Phase 40 normalized)"""
    F_ns = norm_sq(F_vec)
    N = len(basis)
    FPj = [cd_mul(F_vec, basis[j]) for j in range(N)]
    M = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            prod = cd_mul(basis[i], FPj[j])
            M[i, j] = norm_sq(prod) / F_ns
    return M

# ============================================================
# LOAD DATA
# ============================================================
print("Loading data...")
gammas_all = json.load(open("rh_zeros_10k.json"))
gammas_100 = gammas_all[:100]
gammas_50  = gammas_all[:50]

# Load 60 bilateral vectors from Phase 18D enumeration
print("Loading bilateral vectors...")
enum_data = json.load(open("p18d_enumeration.json"))
bilateral_vectors_60 = []
seen = set()
for pair in enum_data["pairs"]:
    for vec in [pair["P"], pair["Q"]]:
        key = tuple(round(x, 8) for x in vec)
        if key not in seen:
            seen.add(key)
            bilateral_vectors_60.append(vec)
        neg_key = tuple(round(-x, 8) for x in vec)
        if neg_key not in seen:
            seen.add(neg_key)
            bilateral_vectors_60.append([-x for x in vec])
        if len(bilateral_vectors_60) >= 60:
            break
    if len(bilateral_vectors_60) >= 60:
        break

bilateral_vectors_60 = bilateral_vectors_60[:60]
print(f"  Bilateral vectors loaded: {len(bilateral_vectors_60)}")

t0_total = time.time()

results = {}

# ============================================================
# TRACK V1 -- Formula Verification
# ============================================================
print("\nTrack V1 (Formula verification)...")
gamma1 = gammas_100[0]
F1 = F_16d(gamma1)
F1_norm_sq = norm_sq(F1)
M_v1 = compute_M_tilde(F1, A1_6_BASIS)
evals_v1 = sorted(np.linalg.eigvalsh(M_v1).real)
results["V1"] = {
    "gamma_1": gamma1,
    "F_norm_sq_at_gamma1": F1_norm_sq,
    "M_tilde_eigenvalues_at_gamma1": evals_v1,
    "lambda_max_at_gamma1": max(evals_v1),
    "phase39_baseline": 21.955,
    "match": bool(abs(max(evals_v1) - 21.955) < 0.05),
}
print(f"  lambda_max at gamma_1: {max(evals_v1):.3f} (Phase 39 baseline: 21.955)")
print(f"  ||F||^2 at gamma_1: {F1_norm_sq:.6f} (Phase 36 baseline: 0.9117)")

# ============================================================
# TRACK A1 -- ||F||^2 vs gamma_n (document pre-flight result)
# ============================================================
print("\nTrack A1 (||F||^2 vs gamma_n, 100 zeros)...")
F_norms_sq = [norm_sq(F_16d(g)) for g in gammas_100]
rho_Fg, p_Fg = spearmanr(F_norms_sq, gammas_100)
print(f"  Spearman(||F||^2, gamma_n): rho={rho_Fg:.4f}, p={p_Fg:.2e}")
print(f"  ||F||^2 range: [{min(F_norms_sq):.4f}, {max(F_norms_sq):.4f}]")
gate_A1 = rho_Fg < -0.3 and p_Fg < 0.01
print(f"  Gate A1: {'PASS -- amplitude is driver' if gate_A1 else 'FAIL -- directional anti-correlation'}")

results["A1"] = {
    "n": 100,
    "spearman_rho": float(rho_Fg),
    "p_value": float(p_Fg),
    "F_norm_sq_range": [float(min(F_norms_sq)), float(max(F_norms_sq))],
    "F_norm_sq_mean": float(np.mean(F_norms_sq)),
    "F_norm_sq_std": float(np.std(F_norms_sq)),
    "gate_A1_pass": bool(gate_A1),
    "conclusion": "directional anti-correlation -- normalization is confirmatory only",
}
json.dump({"track": "A1", **results["A1"]}, open("phase40_F_norm_vs_gamma.json", "w"), indent=2)

# ============================================================
# TRACK A2 -- M_norm baseline at N=6
# ============================================================
print("\nTrack A2 (M_norm baseline, N=6, 100 zeros)...")
lambda_max_tilde = []
lambda_max_norm  = []

for g in gammas_100:
    Fv = F_16d(g)
    Mt = compute_M_tilde(Fv, A1_6_BASIS)
    Mn = compute_M_norm(Fv, A1_6_BASIS)
    lambda_max_tilde.append(max(np.linalg.eigvalsh(Mt).real))
    lambda_max_norm.append(max(np.linalg.eigvalsh(Mn).real))

rho_tilde, p_tilde = spearmanr(lambda_max_tilde, gammas_100)
rho_norm,  p_norm  = spearmanr(lambda_max_norm,  gammas_100)
print(f"  M_tilde: rho={rho_tilde:.4f}, p={p_tilde:.2e}, lmax=[{min(lambda_max_tilde):.2f},{max(lambda_max_tilde):.2f}]")
print(f"  M_norm:  rho={rho_norm:.4f},  p={p_norm:.2e},  lmax=[{min(lambda_max_norm):.2f},{max(lambda_max_norm):.2f}]")
gate_A2 = rho_norm > -0.1
print(f"  Gate A2: {'PASS -- normalization removed anti-corr' if gate_A2 else 'FAIL -- anti-correlation structural'}")

results["A2"] = {
    "n": 100,
    "M_tilde_rho": float(rho_tilde), "M_tilde_p": float(p_tilde),
    "M_tilde_lmax_range": [float(min(lambda_max_tilde)), float(max(lambda_max_tilde))],
    "M_norm_rho": float(rho_norm),   "M_norm_p": float(p_norm),
    "M_norm_lmax_range": [float(min(lambda_max_norm)), float(max(lambda_max_norm))],
    "gate_A2_pass": bool(gate_A2),
}
json.dump({"track": "A2", **results["A2"]}, open("phase40_M_norm_baseline.json", "w"), indent=2)

# ============================================================
# TRACK D1 -- Full eigenvalue distribution at N=60, M_tilde (PRIMARY)
# ============================================================
print("\nTrack D1 (Full eigenvalue distribution, N=60, 50 zeros)...")
t0 = time.time()

basis_60 = bilateral_vectors_60

# Precompute F*P_j for all 60 vectors at 50 zeros
print("  Precomputing F*P_j products (50 zeros x 60 vectors)...")
FPj_all_50 = []
for n, g in enumerate(gammas_50):
    Fv = F_16d(g)
    FPj_all_50.append([cd_mul(Fv, basis_60[j]) for j in range(60)])

all_eigenvalues = []  # all 60*50 = 3000 eigenvalues
lambda_max_all = []
above_g1 = []
GAMMA_1 = gammas_100[0]  # 14.134...

print("  Computing M_tilde at N=60 for 50 zeros...")
for n in range(50):
    M = np.zeros((60, 60))
    for i in range(60):
        for j in range(60):
            prod = cd_mul(basis_60[i], FPj_all_50[n][j])
            M[i, j] = norm_sq(prod)
    evals = sorted(np.linalg.eigvalsh(M).real)
    all_eigenvalues.extend(evals)
    lambda_max_all.append(max(evals))
    above_g1.append(sum(1 for e in evals if e > GAMMA_1))

rho_d1, p_d1 = spearmanr(lambda_max_all, gammas_50)
print(f"  Spearman(lambda_max, gamma): rho={rho_d1:.4f}, p={p_d1:.2e}")
print(f"  Mean eigenvalues above gamma_1: {np.mean(above_g1):.1f}")

# Distribution analysis
intervals = [(0,50),(50,100),(100,150),(150,200),(200,300),(300,500)]
interval_counts = {}
for lo, hi in intervals:
    cnt = sum(1 for e in all_eigenvalues if lo <= e < hi)
    interval_counts[f"{lo}-{hi}"] = cnt

# Compare to zero distribution in same intervals (50 zeros, gammas in ~14-235)
zero_interval_counts = {}
for lo, hi in intervals:
    cnt = sum(1 for g in gammas_50 if lo <= g < hi)
    zero_interval_counts[f"{lo}-{hi}"] = cnt

print("  Eigenvalue distribution vs zero distribution:")
print(f"  {'Range':>10}  {'Evals':>6}  {'Zeros':>6}  {'Ratio':>6}")
for lo, hi in intervals:
    key = f"{lo}-{hi}"
    ec = interval_counts[key]; zc = zero_interval_counts[key]
    ratio = ec/zc if zc > 0 else float('inf')
    print(f"  {key:>10}  {ec:>6}  {zc:>6}  {ratio:>6.1f}")

results["D1"] = {
    "N_dim": 60, "n_zeros": 50,
    "lambda_max_rho": float(rho_d1), "lambda_max_p": float(p_d1),
    "mean_above_gamma1": float(np.mean(above_g1)),
    "eigenvalue_interval_counts": interval_counts,
    "zero_interval_counts": zero_interval_counts,
    "all_eigenvalues_summary": {
        "min": float(min(all_eigenvalues)),
        "max": float(max(all_eigenvalues)),
        "mean": float(np.mean(all_eigenvalues)),
        "median": float(np.median(all_eigenvalues)),
        "count": len(all_eigenvalues),
    },
}
json.dump({"track": "D1", **results["D1"]}, open("phase40_full_eigenvalue_distribution.json", "w"), indent=2)
print(f"  D1 time: {time.time()-t0:.1f}s")

# ============================================================
# TRACK S1 -- Correlated subspace: top-k diagonal-correlated vectors (PRIMARY)
# ============================================================
print("\nTrack S1 (Correlated subspace, 50 zeros)...")
t0 = time.time()

# Compute diagonal M_tilde[i][i] for each of 60 bilateral vectors
diag_vals = {i: [] for i in range(60)}
for n in range(50):
    Fv = F_16d(gammas_50[n])
    for i in range(60):
        prod = cd_mul(basis_60[i], cd_mul(Fv, basis_60[i]))
        diag_vals[i].append(norm_sq(prod))

# Spearman of each diagonal with gamma_n
diag_rho = {}
for i in range(60):
    rho_i, p_i = spearmanr(diag_vals[i], gammas_50)
    diag_rho[i] = (float(rho_i), float(p_i))

# Sort by rho (most positive first)
sorted_by_rho = sorted(diag_rho.items(), key=lambda x: -x[1][0])
print(f"  Top-10 diagonal rho values:")
for idx, (rho_i, p_i) in sorted_by_rho[:10]:
    print(f"    vector[{idx:2d}]: rho={rho_i:+.4f}, p={p_i:.2e}")

# Build M_norm with top-k vectors (k=6, 12, 18) and test Spearman
S1_results = {}
for k in [6, 12, 18]:
    top_k_indices = [idx for idx, _ in sorted_by_rho[:k]]
    top_k_basis = [basis_60[i] for i in top_k_indices]
    lmax_k = []
    for n in range(50):
        Fv = F_16d(gammas_50[n])
        M_k = compute_M_tilde(Fv, top_k_basis)
        lmax_k.append(max(np.linalg.eigvalsh(M_k).real))
    rho_k, p_k = spearmanr(lmax_k, gammas_50)
    print(f"  k={k}: rho={rho_k:.4f}, p={p_k:.2e}, lmax=[{min(lmax_k):.1f},{max(lmax_k):.1f}]")
    S1_results[f"k{k}"] = {
        "indices": top_k_indices,
        "rho": float(rho_k), "p": float(p_k),
        "lambda_max_range": [float(min(lmax_k)), float(max(lmax_k))],
    }

results["S1"] = {
    "n_zeros": 50,
    "diagonal_rho_all": {str(i): {"rho": v[0], "p": v[1]} for i, v in diag_rho.items()},
    "top10_indices": [idx for idx, _ in sorted_by_rho[:10]],
    "subspace_results": S1_results,
}
json.dump({"track": "S1", **results["S1"]}, open("phase40_correlated_subspace.json", "w"), indent=2)
print(f"  S1 time: {time.time()-t0:.1f}s")

# ============================================================
# TRACK N1 -- M_norm growing subspace (confirmatory)
# ============================================================
print("\nTrack N1 (M_norm growing subspace, 6->60, 50 zeros)...")
t0 = time.time()

SUBSPACE_SIZES = [6, 12, 18, 30, 45, 60]
N1_norm_results = []

# Reuse FPj_all_50 computed in D1
for N_dim in SUBSPACE_SIZES:
    basis_N = bilateral_vectors_60[:N_dim]
    lmax_norm_N = []
    above_g1_N = []
    for n in range(50):
        Fv = F_16d(gammas_50[n])
        Fns = norm_sq(Fv)
        FPj_n = [cd_mul(Fv, basis_N[j]) for j in range(N_dim)]
        M = np.zeros((N_dim, N_dim))
        for i in range(N_dim):
            for j in range(N_dim):
                prod = cd_mul(basis_N[i], FPj_n[j])
                M[i, j] = norm_sq(prod) / Fns
        evals = np.linalg.eigvalsh(M).real
        lmax_norm_N.append(max(evals))
        above_g1_N.append(sum(1 for e in evals if e > GAMMA_1))

    rho_N, p_N = spearmanr(lmax_norm_N, gammas_50)
    mean_above = np.mean(above_g1_N)
    print(f"  N={N_dim:2d}: rho={rho_N:+.4f}, above_g1={mean_above:.1f}, lmax=[{min(lmax_norm_N):.1f},{max(lmax_norm_N):.1f}]")
    N1_norm_results.append({
        "N_dim": N_dim, "n_zeros": 50,
        "rho": float(rho_N), "p": float(p_N),
        "mean_above_gamma1": float(mean_above),
        "lambda_max_range": [float(min(lmax_norm_N)), float(max(lmax_norm_N))],
    })

results["N1_norm"] = N1_norm_results
json.dump({"track": "N1_norm", "subspace_results": N1_norm_results},
          open("phase40_M_norm_growing.json", "w"), indent=2)
print(f"  N1 time: {time.time()-t0:.1f}s")

# ============================================================
# TRACK N2 -- Normalized eigenvalue density at N=60
# ============================================================
print("\nTrack N2 (Normalized density at N=60, 50 zeros)...")
t0 = time.time()

norm_evals_all = []
norm_above_g1 = []

for n in range(50):
    Fv = F_16d(gammas_50[n])
    Fns = norm_sq(Fv)
    M = np.zeros((60, 60))
    for i in range(60):
        for j in range(60):
            prod = cd_mul(basis_60[i], FPj_all_50[n][j])
            M[i, j] = norm_sq(prod) / Fns
    evals = sorted(np.linalg.eigvalsh(M).real)
    norm_evals_all.extend(evals)
    norm_above_g1.append(sum(1 for e in evals if e > GAMMA_1))

# Density in intervals
norm_interval_counts = {}
for lo, hi in intervals:
    cnt = sum(1 for e in norm_evals_all if lo <= e < hi)
    norm_interval_counts[f"{lo}-{hi}"] = cnt

print(f"  Mean above gamma_1 (M_norm, N=60): {np.mean(norm_above_g1):.1f}")
print(f"  Normalized eigenvalue range: [{min(norm_evals_all):.4f}, {max(norm_evals_all):.4f}]")
print(f"  Interval distribution (M_norm): {norm_interval_counts}")

gate_N1_norm = np.mean(norm_above_g1) >= 0.3 * 50  # 30% of zero density
print(f"  Gate N1_norm: {'PASS' if gate_N1_norm else 'FAIL'} ({np.mean(norm_above_g1):.1f} vs threshold 15)")

results["N2"] = {
    "N_dim": 60, "n_zeros": 50,
    "mean_above_gamma1": float(np.mean(norm_above_g1)),
    "eigenvalue_range": [float(min(norm_evals_all)), float(max(norm_evals_all))],
    "interval_counts": norm_interval_counts,
    "zero_interval_counts": zero_interval_counts,
    "gate_N1_norm_pass": bool(gate_N1_norm),
}
json.dump({"track": "N2", **results["N2"]}, open("phase40_density_normalized.json", "w"), indent=2)
print(f"  N2 time: {time.time()-t0:.1f}s")

# ============================================================
# TRACK W1 -- Weyl law target formula (theoretical)
# ============================================================
print("\nTrack W1 (Weyl law target formula)...")

# From Phase 39: eigenvalues above gamma_1 ~ N/6 (M_tilde)
# Weyl law: N(T) ~ (T/2pi)*log(T/2pi)
# For T = gamma_100 = 236.5: N(236.5) ~ (236.5/6.28)*log(236.5/6.28) = 37.7*3.63 ~ 137 zeros
# To match: need ~137 eigenvalues above gamma_1
# At growth rate N/6 per eigenvalue: N_required = 137 * 6 = 822
# But max bilateral vectors in 16D = 60. So 16D cannot reach Weyl density.

T_100 = gammas_all[99]  # gamma_100
weyl_100 = (T_100 / (2 * np.pi)) * np.log(T_100 / (2 * np.pi))

# Growth rate from Phase 39: ~1.0/6 eigenvalues per unit N
growth_rate_phase39 = 1.0 / 6.0  # eigenvalues per unit N
N_required_phase39 = weyl_100 / growth_rate_phase39

# After normalization: read from N1 if rate changed
if N1_norm_results:
    # Fit growth rate from N1_norm: eigenvalues_above_g1 ~ c * N
    N_vals = [r["N_dim"] for r in N1_norm_results]
    above_vals = [r["mean_above_gamma1"] for r in N1_norm_results]
    # Simple ratio at N=60
    growth_rate_norm = above_vals[-1] / N_vals[-1]
    N_required_norm = weyl_100 / growth_rate_norm if growth_rate_norm > 0 else float('inf')
else:
    growth_rate_norm = None
    N_required_norm = None

print(f"  Weyl N(T=gamma_100={T_100:.1f}): {weyl_100:.1f} zeros")
print(f"  Phase 39 growth rate: {growth_rate_phase39:.4f} evals/unit N")
print(f"  Phase 39 required N: {N_required_phase39:.0f} (max available: 60)")
if growth_rate_norm:
    print(f"  M_norm growth rate at N=60: {growth_rate_norm:.4f} evals/unit N")
    print(f"  M_norm required N: {N_required_norm:.0f}")

results["W1"] = {
    "T_target": float(T_100),
    "weyl_N_target": float(weyl_100),
    "phase39_growth_rate": growth_rate_phase39,
    "phase39_N_required": float(N_required_phase39),
    "max_available_N_16D": 60,
    "16D_sufficient": bool(N_required_phase39 <= 60),
    "M_norm_growth_rate": float(growth_rate_norm) if growth_rate_norm else None,
    "M_norm_N_required": float(N_required_norm) if N_required_norm else None,
    "formula": "N_required = Weyl_N(T_target) / growth_rate_per_unit_N",
}
json.dump({"track": "W1", **results["W1"]}, open("phase40_weyl_density_target.json", "w"), indent=2)

# ============================================================
# TRACK V1 -- Save verification file
# ============================================================
json.dump({"track": "V1", **results["V1"]}, open("phase40_formula_verification.json", "w"), indent=2)

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("Phase 40 Summary")
print("="*60)
print(f"Gate A1 (||F||^2 driver):  rho={results['A1']['spearman_rho']:+.4f}  PASS={results['A1']['gate_A1_pass']}")
print(f"Gate A2 (norm removes rho): rho_norm={results['A2']['M_norm_rho']:+.4f}  PASS={results['A2']['gate_A2_pass']}")
print(f"D1 (N=60 eigenval dist): rho={results['D1']['lambda_max_rho']:+.4f}, above_g1={results['D1']['mean_above_gamma1']:.1f}")
print(f"Gate N1_norm (density):    {results['N2']['gate_N1_norm_pass']}  mean_above={results['N2']['mean_above_gamma1']:.1f}")
print("S1 (correlated subspace):")
for k_label, kres in results["S1"]["subspace_results"].items():
    print(f"  {k_label}: rho={kres['rho']:+.4f}, lmax=[{kres['lambda_max_range'][0]:.1f},{kres['lambda_max_range'][1]:.1f}]")

print(f"\nTotal elapsed: {time.time()-t0_total:.1f}s")
print("\nOutput files:")
for fname in ["phase40_formula_verification.json", "phase40_F_norm_vs_gamma.json",
              "phase40_M_norm_baseline.json", "phase40_full_eigenvalue_distribution.json",
              "phase40_correlated_subspace.json", "phase40_M_norm_growing.json",
              "phase40_density_normalized.json", "phase40_weyl_density_target.json"]:
    print(f"  {fname}")
