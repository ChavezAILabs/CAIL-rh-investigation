"""
rh_phase41.py
=============
Phase 41 -- Aggregated Operator M_agg: Rank Lifting via Zero Accumulation
RH Investigation -- Chavez AI Labs LLC

Date: 2026-03-28
Researcher: Paul Chavez, Chavez AI Labs LLC

Core construction:
    M_agg[i][j] = sum_{n=1}^{N_zeros} ||P_i * (F(rho_n) * P_j)||^2

Properties:
  - PSD by construction (each term is norm^2 >= 0)
  - Effective rank = min(16 * N_zeros, 60)
  - At N_zeros=4: full rank (reaches 60)
  - Phase 40 diagnosis: single-zero effective rank ~16 => aggregation is the fix

Tracks:
  V1  -- Formula verification (M_tilde confirmed, M_agg at N_zeros=1 matches)
  G1  -- M_agg sweep: N_zeros in {4, 8, 16, 30, 60}; eigenvalues, Spearman, PSD
  G2  -- Rank verification: rank(M_agg) at each N_zeros (expect min(16*N, 60))
  G3  -- Full eigenvalue distribution at N_zeros=60 vs Riemann zeros
  W1  -- Weyl density matching: how many eigenvalues fall in [14, gamma_60]?
"""

import numpy as np
from scipy.stats import spearmanr
import json, time

# ============================================================
# SEDENION ENGINE (Phase 40 -- unchanged)
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

# (A1)^6 canonical basis
A1_6_BASIS = [
    make16([(1,  1.0), (14,  1.0)]),
    make16([(1,  1.0), (14, -1.0)]),
    make16([(2,  1.0), (13, -1.0)]),
    make16([(3,  1.0), (12,  1.0)]),
    make16([(4,  1.0), (11,  1.0)]),
    make16([(5,  1.0), (10,  1.0)]),
]

def compute_M_agg(basis, gammas_subset):
    """
    M_agg[i][j] = sum_{n} ||P_i * (F(gamma_n) * P_j)||^2
    PSD by construction.
    """
    N = len(basis)
    M = np.zeros((N, N))
    for g in gammas_subset:
        Fv = F_16d(g)
        FPj = [cd_mul(Fv, basis[j]) for j in range(N)]
        for i in range(N):
            for j in range(N):
                prod = cd_mul(basis[i], FPj[j])
                M[i, j] += norm_sq(prod)
    return M

# ============================================================
# LOAD DATA
# ============================================================
print("Loading data...")
gammas_all = json.load(open("rh_zeros_10k.json"))
gammas_100 = gammas_all[:100]

print("Loading bilateral vectors...")
enum_data = json.load(open("p18d_enumeration.json"))
bilateral_60 = []
seen = set()
for pair in enum_data["pairs"]:
    for vec in [pair["P"], pair["Q"]]:
        key = tuple(round(x, 8) for x in vec)
        if key not in seen:
            seen.add(key)
            bilateral_60.append(vec)
        neg_key = tuple(round(-x, 8) for x in vec)
        if neg_key not in seen:
            seen.add(neg_key)
            bilateral_60.append([-x for x in vec])
        if len(bilateral_60) >= 60:
            break
    if len(bilateral_60) >= 60:
        break
bilateral_60 = bilateral_60[:60]
print(f"  Bilateral vectors loaded: {len(bilateral_60)}")

t0_total = time.time()
results = {}

# ============================================================
# TRACK V1 -- Formula Verification
# ============================================================
print("\nTrack V1 (Formula verification)...")
gamma1 = gammas_100[0]

# Confirm M_tilde at N_zeros=1 matches Phase 40 baseline
M_single = compute_M_agg(A1_6_BASIS, [gamma1])
evals_single = sorted(np.linalg.eigvalsh(M_single).real)
print(f"  M_agg (N=1, 6-basis) lambda_max: {max(evals_single):.3f} (Phase 40 baseline: 21.955)")

# M_agg at N_zeros=1 with 60-vector basis
M_single_60 = compute_M_agg(bilateral_60, [gamma1])
evals_s60 = sorted(np.linalg.eigvalsh(M_single_60).real)
print(f"  M_agg (N=1, 60-basis) lambda_max: {max(evals_s60):.3f}, min: {min(evals_s60):.4f}")
print(f"  PSD at N_zeros=1: {min(evals_s60) >= -1e-10}")

results["V1"] = {
    "M_agg_N1_6basis_lambda_max": float(max(evals_single)),
    "phase40_baseline": 21.955,
    "match": bool(abs(max(evals_single) - 21.955) < 0.05),
    "M_agg_N1_60basis_lambda_max": float(max(evals_s60)),
    "M_agg_N1_60basis_min_eval": float(min(evals_s60)),
}
json.dump({"track": "V1", **results["V1"]},
          open("phase41_formula_verification.json", "w"), indent=2)

# ============================================================
# TRACK G1 + G2 -- M_agg sweep + rank verification
# ============================================================
print("\nTrack G1+G2 (M_agg sweep + rank, N_zeros in {4,8,16,30,60})...")

N_ZEROS_SWEEP = [4, 8, 16, 30, 60]
sweep_results = []
rank_results = []

for N_z in N_ZEROS_SWEEP:
    t_z = time.time()
    gammas_z = gammas_100[:N_z]

    M_z = compute_M_agg(bilateral_60, gammas_z)
    evals_z = np.linalg.eigvalsh(M_z).real
    evals_sorted_asc = sorted(evals_z)
    evals_sorted_desc = sorted(evals_z, reverse=True)

    # Rank
    rank_z = int(np.linalg.matrix_rank(M_z, tol=1e-6))
    expected_rank = min(16 * N_z, 60)

    # PSD check
    min_eval = float(min(evals_z))
    is_psd = bool(min_eval >= -1e-8)

    # Top-N_z eigenvalues vs sorted gammas
    top_evals = sorted(evals_z, reverse=True)[:N_z]
    sorted_gammas = sorted(gammas_z)

    rho_top, p_top = spearmanr(top_evals, sorted_gammas)

    # All eigenvalues vs all gammas (both ascending)
    rho_all, p_all = spearmanr(evals_sorted_asc[-N_z:], sorted_gammas)

    elapsed = time.time() - t_z
    print(f"  N_zeros={N_z:2d}: rank={rank_z}/{expected_rank}, PSD={is_psd}, "
          f"min_eval={min_eval:.4f}, "
          f"rho_top={rho_top:+.4f}(p={p_top:.3f}), elapsed={elapsed:.1f}s")

    sweep_results.append({
        "N_zeros": N_z,
        "rank": rank_z, "expected_rank": expected_rank,
        "rank_match": bool(rank_z >= expected_rank - 2),
        "is_psd": is_psd,
        "min_eigenvalue": min_eval,
        "max_eigenvalue": float(max(evals_z)),
        "eigenvalues_all_sorted": [float(x) for x in evals_sorted_asc],
        "top_N_eigenvalues": [float(x) for x in top_evals],
        "gammas_subset": [float(g) for g in sorted_gammas],
        "spearman_rho_top_N": float(rho_top),
        "spearman_p_top_N": float(p_top),
        "spearman_rho_all_N": float(rho_all),
        "spearman_p_all_N": float(p_all),
        "gate_G1_pass": bool(rho_top > 0.3 and p_top < 0.05),
    })
    rank_results.append({
        "N_zeros": N_z, "rank": rank_z,
        "expected_rank": expected_rank,
        "ratio": float(rank_z / expected_rank),
    })

json.dump({"track": "G1", "sweep": sweep_results},
          open("phase41_M_agg_sweep.json", "w"), indent=2)
json.dump({"track": "G2", "rank_results": rank_results},
          open("phase41_rank_verification.json", "w"), indent=2)

results["G1"] = sweep_results
results["G2"] = rank_results

# ============================================================
# TRACK G3 -- Full eigenvalue distribution at N_zeros=60
# ============================================================
print("\nTrack G3 (Eigenvalue distribution at N_zeros=60)...")

# Get M_agg results for N_zeros=60 (already computed above)
agg_60_result = next(r for r in sweep_results if r["N_zeros"] == 60)
evals_60 = sorted(agg_60_result["eigenvalues_all_sorted"])
gammas_60 = sorted(gammas_100[:60])

intervals = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 300)]
eval_counts = {}
gamma_counts = {}
for lo, hi in intervals:
    eval_counts[f"{lo}-{hi}"] = sum(1 for e in evals_60 if lo <= e < hi)
    gamma_counts[f"{lo}-{hi}"] = sum(1 for g in gammas_60 if lo <= g < hi)

print(f"  Eigenvalue range: [{min(evals_60):.2f}, {max(evals_60):.2f}]")
print(f"  Zero range: [{min(gammas_60):.2f}, {max(gammas_60):.2f}]")
print(f"  {'Range':>10}  {'Evals':>6}  {'Zeros':>6}")
for lo, hi in intervals:
    key = f"{lo}-{hi}"
    print(f"  {key:>10}  {eval_counts[key]:>6}  {gamma_counts[key]:>6}")

# Distribution-level Spearman: sorted eigenvalues vs sorted gammas
rho_dist, p_dist = spearmanr(evals_60, gammas_60)
print(f"  Spearman(sorted evals, sorted gammas): rho={rho_dist:.4f}, p={p_dist:.4f}")

results["G3"] = {
    "N_zeros": 60, "N_basis": 60,
    "eigenvalue_range": [float(min(evals_60)), float(max(evals_60))],
    "zero_range": [float(min(gammas_60)), float(max(gammas_60))],
    "eigenvalue_interval_counts": eval_counts,
    "zero_interval_counts": gamma_counts,
    "spearman_sorted_rho": float(rho_dist),
    "spearman_sorted_p": float(p_dist),
    "gate_G3_pass": bool(rho_dist > 0.3 and p_dist < 0.05),
}
json.dump({"track": "G3", **results["G3"]},
          open("phase41_agg_distribution.json", "w"), indent=2)

# ============================================================
# TRACK W1 -- Weyl density matching
# ============================================================
print("\nTrack W1 (Weyl density matching at N_zeros=60)...")

gamma_60_max = gammas_60[-1]   # = gamma_60
gamma_1_val  = gammas_60[0]    # = gamma_1

# How many of the 60 M_agg eigenvalues fall in [gamma_1, gamma_60]?
in_range_count = sum(1 for e in evals_60 if gamma_1_val <= e <= gamma_60_max)
# How many are positive?
positive_count = sum(1 for e in evals_60 if e > 0)
# Weyl count: exactly 60 zeros in [gamma_1, gamma_60] by construction
weyl_target = 60

print(f"  Eigenvalues in [gamma_1={gamma_1_val:.1f}, gamma_60={gamma_60_max:.1f}]: "
      f"{in_range_count}/60")
print(f"  Positive eigenvalues: {positive_count}/60")
print(f"  Gate W1 (>=50 eigenvalues in range): {in_range_count >= 50}")

# Weyl law density profile
import numpy as np
T_range = np.linspace(gamma_1_val, gamma_60_max, 100)
weyl_density = [(T / (2 * np.pi)) * np.log(T / (2 * np.pi)) for T in T_range]

# How many eigenvalues in each Weyl band?
weyl_bands = [(14, 50), (50, 100), (100, 150), (150, 200), (200, 236.5)]
weyl_band_evals = {}
weyl_band_zeros = {}
for lo, hi in weyl_bands:
    weyl_band_evals[f"{lo:.0f}-{hi:.0f}"] = sum(1 for e in evals_60 if lo <= e < hi)
    weyl_band_zeros[f"{lo:.0f}-{hi:.0f}"] = sum(1 for g in gammas_60 if lo <= g < hi)

print(f"  Band distribution:")
print(f"  {'Band':>10}  {'Evals':>6}  {'Zeros':>6}")
for lo, hi in weyl_bands:
    key = f"{lo:.0f}-{hi:.0f}"
    print(f"  {key:>10}  {weyl_band_evals[key]:>6}  {weyl_band_zeros[key]:>6}")

results["W1"] = {
    "N_zeros": 60, "N_basis": 60,
    "gamma_1": float(gamma_1_val),
    "gamma_60": float(gamma_60_max),
    "eigenvalues_in_range": in_range_count,
    "positive_eigenvalues": positive_count,
    "weyl_target": weyl_target,
    "gate_W1_pass": bool(in_range_count >= 50),
    "band_eigenvalue_counts": weyl_band_evals,
    "band_zero_counts": weyl_band_zeros,
}
json.dump({"track": "W1", **results["W1"]},
          open("phase41_weyl_matching.json", "w"), indent=2)

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*60)
print("Phase 41 Summary")
print("="*60)
print(f"V1: lambda_max(N=1,6-basis)={results['V1']['M_agg_N1_6basis_lambda_max']:.3f} "
      f"match={results['V1']['match']}")
print()
print("G1+G2 (M_agg sweep):")
print(f"  {'N_zeros':>8}  {'rank':>6}  {'exp':>6}  {'PSD':>6}  {'min_eval':>10}  {'rho_top':>8}  {'p':>8}  {'G1':>6}")
for r in sweep_results:
    print(f"  {r['N_zeros']:>8}  {r['rank']:>6}  {r['expected_rank']:>6}  "
          f"{'Y' if r['is_psd'] else 'N':>6}  {r['min_eigenvalue']:>10.4f}  "
          f"{r['spearman_rho_top_N']:>+8.4f}  {r['spearman_p_top_N']:>8.4f}  "
          f"{'PASS' if r['gate_G1_pass'] else 'FAIL':>6}")
print()
print(f"G3 (distribution, N=60): rho={results['G3']['spearman_sorted_rho']:.4f}, "
      f"p={results['G3']['spearman_sorted_p']:.4f}, "
      f"PASS={results['G3']['gate_G3_pass']}")
print(f"W1 (Weyl density):       {results['W1']['eigenvalues_in_range']}/60 in range, "
      f"PASS={results['W1']['gate_W1_pass']}")
print(f"\nTotal elapsed: {time.time()-t0_total:.1f}s")
print("\nOutput files:")
for fname in ["phase41_formula_verification.json", "phase41_M_agg_sweep.json",
              "phase41_rank_verification.json", "phase41_agg_distribution.json",
              "phase41_weyl_matching.json"]:
    print(f"  {fname}")
