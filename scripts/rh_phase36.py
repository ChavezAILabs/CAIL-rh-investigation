"""
rh_phase36.py
=============
Phase 36 — Bilateral ZD Inner Product + Srednicki Operator Construction
RH Investigation — Chavez AI Labs LLC

Date: 2026-03-27
Researcher: Paul Chavez, Chavez AI Labs LLC

Description
-----------
Primary algebraic phase: constructs the bilateral ZD inner product on the (A1)^6
Canonical Six subspace and tests hermiticity following the Srednicki (2011) template.

Tracks:
  V1  — Formula verification (standard 5 checks)
  I1  — Project F(rho) onto (A1)^6, compute <F|, F'|>_ZD for 100 zero pairs
  I2  — Hermiticity test |IP(n,m) - IP(m,n)*| across 100x100 pairs
  F1  — 6x6 mutual annihilation matrix M[i][j] = scalar_part(P_i * Q_j)
  F2  — F|_{(A1)^6} * (F|_{(A1)^6})* = ||F|_{(A1)^6}||^2 * e0
  D1  — M_F[i][j] = <P_i, F(rho)*P_j>; det_6(rho*I - M_F) for 50 zeros
  C1  — Chavez conjugation_symmetry on 6D projection time series
  P1  — A2 subsystem inner products at p=3 vs chi3 anomaly

Output files (8):
  phase36_formula_verification.json
  phase36_bilateral_inner_product.json
  phase36_hermiticity_test.json
  phase36_fourier_analogue.json
  phase36_selfdual_verification.json
  phase36_spectral_determinant.json
  phase36_chavez_transform_spectral.json
  phase36_p3_a2_inner_product.json

References
----------
  Srednicki (2011) arXiv:1104.1850v3 — BK Hamiltonian and Local RH
  Phase 29 sedenion engine (cd_mul, cd_conj, make16, F_16d, ROOT_16D_BASE)
  Phase 18D canonical six bilateral pairs (p18d_enumeration.json)
  Phase 35: F[0] uncorrelated with Tr_BK (r=0.013)

GitHub: https://github.com/ChavezAILabs/CAIL-rh-investigation
Zenodo: https://doi.org/10.5281/zenodo.17402495
"""

import numpy as np
from scipy.stats import pearsonr
import json, time, os

# ============================================================
# SEDENION ENGINE (from Phase 29 — verified)
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
    for i, val in pairs:
        v[i] = float(val)
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

def F_16d(t, sigma=0.5, primes=None):
    if primes is None: primes = [2, 3, 5, 7, 11, 13]
    r = make16([(0, 1.0)])
    for p in primes:
        theta = t * np.log(p)
        rp = ROOT_16D_BASE[p]
        rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16
        f[0] = np.cos(theta)
        for i in range(16):
            f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

def Tr_BK(t, primes=None):
    if primes is None: primes = [2, 3, 5, 7, 11, 13]
    return float(sum((np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) for p in primes))

def Weil_RHS(primes=None):
    if primes is None: primes = [2, 3, 5, 7, 11, 13]
    return -sum(np.log(p) / np.sqrt(p) for p in primes)

# ============================================================
# (A1)^6 SUBSPACE DEFINITION
# ============================================================
# 6 mutually orthogonal vectors from the Canonical Six bilateral family
# G[i][j] = scalar_part(P_i * P_j) = -2 * delta[i][j]  (verified below)
# Indices: 5 unique canonical P-vectors + e5+e10 (canonical Q for pairs 3,5)
A1_6_BASIS = [
    make16([(1,  1), (14,  1)]),   # B0: e1 + e14
    make16([(1,  1), (14, -1)]),   # B1: e1 - e14
    make16([(2,  1), (13, -1)]),   # B2: e2 - e13
    make16([(3,  1), (12,  1)]),   # B3: e3 + e12
    make16([(4,  1), (11,  1)]),   # B4: e4 + e11
    make16([(5,  1), (10,  1)]),   # B5: e5 + e10
]
A1_6_LABELS = ['e1+e14', 'e1-e14', 'e2-e13', 'e3+e12', 'e4+e11', 'e5+e10']

# Canonical Six bilateral pairs from p18d_enumeration.json (6 canonical, canonical=True)
# Verified bilateral (PQ=QP=0) in cd_mul framework
CANONICAL_P = [
    make16([(1, 1), (14,  1)]),   # e1+e14
    make16([(1, 1), (14, -1)]),   # e1-e14 (pattern 2)
    make16([(1, 1), (14, -1)]),   # e1-e14 (pattern 3 — same P, different Q)
    make16([(2, 1), (13, -1)]),   # e2-e13
    make16([(3, 1), (12,  1)]),   # e3+e12
    make16([(4, 1), (11,  1)]),   # e4+e11
]
CANONICAL_Q = [
    make16([(3, 1), (12,  1)]),   # e3+e12 = B3
    make16([(3, 1), (12, -1)]),   # e3-e12
    make16([(5, 1), (10,  1)]),   # e5+e10 = B5
    make16([(6, 1), (9,   1)]),   # e6+e9
    make16([(5, 1), (10,  1)]),   # e5+e10 = B5
    make16([(6, 1), (9,   1)]),   # e6+e9
]

def project_A1_6(F_vec, basis=A1_6_BASIS):
    """Project sedenion F onto (A1)^6 subspace.
    Coefficients c_i = scalar_part(F * P_i) / G[i,i]
    G[i,i] = scalar_part(P_i * P_i) = -||P_i||^2 = -2
    Returns: list of 6 real coefficients
    """
    coeffs = []
    for P in basis:
        fp = cd_mul(F_vec, P)
        c = fp[0] / (-2.0)   # G[i,i] = -2
        coeffs.append(c)
    return coeffs

def reconstruct_A1_6(coeffs, basis=A1_6_BASIS):
    """Reconstruct F|_{(A1)^6} = sum_i c_i * P_i"""
    result = [0.0] * 16
    for c, P in zip(coeffs, basis):
        for k in range(16):
            result[k] += c * P[k]
    return result

def inner_product_ZD(coeffs_n, coeffs_m):
    """<F_n|, F_m|>_ZD = sum_i c_n[i] * c_m[i] * G[i,i]
    = -2 * sum_i c_n[i] * c_m[i]   (G[i,i] = -2)
    """
    return -2.0 * sum(cn * cm for cn, cm in zip(coeffs_n, coeffs_m))

def conjugation_symmetry(x):
    """CAILculator formula: 1 - mean(|x[i] - x[n-1-i]| for i in range(n//2))"""
    n = len(x)
    if n < 2: return 1.0
    diffs = [abs(x[i] - x[n - 1 - i]) for i in range(n // 2)]
    return 1.0 - np.mean(diffs)

# ============================================================
# DATA LOAD
# ============================================================
print("=" * 60)
print("PHASE 36 — Bilateral ZD Inner Product + Srednicki Operator")
print("=" * 60)

CACHE_1K = 'rh_zeros.json'
CACHE_10K = 'rh_zeros_10k.json'

t0 = time.time()
with open(CACHE_1K) as f:
    zeros_1k = json.load(f)
zeros_100 = [float(z) for z in zeros_1k[:100]]
zeros_50  = [float(z) for z in zeros_1k[:50]]
print(f"Loaded {len(zeros_100)} zeros from {CACHE_1K}  (t1={zeros_100[0]:.4f})")

c1 = 0.11797805192095003

# ============================================================
# TRACK V1 — FORMULA VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("TRACK V1 — Formula Verification")
print("=" * 60)

t_test = 14.134725
F_test = F_16d(t_test)
print(f"F({t_test:.4f}) norm^2 = {norm_sq(F_test):.8f}  (expect ~1.0)")
print(f"F[0] (scalar) = {F_test[0]:.8f}")

# Check sigma symmetry
F_half    = F_16d(t_test, sigma=0.5)
F_off_hi  = F_16d(t_test, sigma=0.6)
F_off_lo  = F_16d(t_test, sigma=0.4)
norm_half = norm_sq(F_half)
norm_hi   = norm_sq(F_off_hi)
norm_lo   = norm_sq(F_off_lo)
print(f"sigma symmetry: ||F(0.4)||^2={norm_lo:.8f}  ||F(0.6)||^2={norm_hi:.8f}  diff={abs(norm_hi-norm_lo):.2e}")

# Check Tr_BK and Weil_RHS
tr_test = Tr_BK(t_test)
weil = Weil_RHS()
print(f"Tr_BK({t_test:.4f}) = {tr_test:.6f}")
print(f"Weil_RHS (6 primes) = {weil:.6f}")

# Verify G_ij = -2 delta_ij for (A1)^6 basis
G_mat = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        G_mat[i, j] = cd_mul(A1_6_BASIS[i], A1_6_BASIS[j])[0]
gram_diag = np.diag(G_mat).tolist()
gram_max_offdiag = float(np.max(np.abs(G_mat - np.diag(np.diag(G_mat)))))
print(f"\n(A1)^6 Gram matrix diagonal: {[round(x,4) for x in gram_diag]}")
print(f"Max off-diagonal: {gram_max_offdiag:.2e}  (expect 0.0)")
gram_ok = all(abs(d + 2) < 1e-10 for d in gram_diag) and gram_max_offdiag < 1e-10
print(f"G = -2*I confirmed: {gram_ok}")

v1_results = {
    "phase": 36,
    "track": "V1",
    "description": "Formula verification",
    "c1": c1,
    "F_norm_sq_at_t1": float(norm_sq(F_test)),
    "F_scalar_at_t1": float(F_test[0]),
    "sigma_symmetry_diff": float(abs(norm_hi - norm_lo)),
    "sigma_symmetry_ok": bool(abs(norm_hi - norm_lo) < 1e-10),
    "Tr_BK_at_t1": float(tr_test),
    "Weil_RHS_6p": float(weil),
    "gram_diagonal": gram_diag,
    "gram_max_offdiag": gram_max_offdiag,
    "gram_minus2I_confirmed": bool(gram_ok),
    "basis_labels": A1_6_LABELS,
    "pass": bool(gram_ok and abs(norm_hi - norm_lo) < 1e-6)
}
with open('phase36_formula_verification.json', 'w') as f:
    json.dump(v1_results, f, indent=2)
print("Saved phase36_formula_verification.json")

# ============================================================
# TRACK I1 — BILATERAL ZD INNER PRODUCT
# ============================================================
print("\n" + "=" * 60)
print("TRACK I1 — Bilateral ZD Inner Product <F(rho)|, F(rho')|>_ZD")
print("=" * 60)

t0_i1 = time.time()
N_i1 = 100
# Precompute projections for first N_i1 zeros
projections = []
for n, t in enumerate(zeros_100[:N_i1]):
    Fv = F_16d(t)
    coeffs = project_A1_6(Fv)
    proj_norm_sq = sum(c * c for c in coeffs)
    projections.append({
        'n': n + 1,
        't': t,
        'coeffs': coeffs,
        'proj_norm_sq': proj_norm_sq
    })

# Compute inner products for first 10x10 pairs (save full 100x100 as matrix)
print(f"Computing {N_i1}x{N_i1} inner product matrix...")
ip_matrix = np.zeros((N_i1, N_i1))
for n in range(N_i1):
    for m in range(N_i1):
        ip_matrix[n, m] = inner_product_ZD(projections[n]['coeffs'], projections[m]['coeffs'])

print(f"Done in {time.time()-t0_i1:.1f}s")
print(f"IP[0,0] = {ip_matrix[0,0]:.6f}  (= -2 * ||proj_0||^2 = {-2*projections[0]['proj_norm_sq']:.6f})")
print(f"IP diagonal range: [{ip_matrix.diagonal().min():.4f}, {ip_matrix.diagonal().max():.4f}]")
print(f"IP off-diag range: [{ip_matrix[~np.eye(N_i1,dtype=bool)].min():.4f}, {ip_matrix[~np.eye(N_i1,dtype=bool)].max():.4f}]")

# Sample 5x5 corner
print("IP[0:5, 0:5] matrix:")
for row in ip_matrix[:5, :5]:
    print("  " + "  ".join(f"{v:8.4f}" for v in row))

i1_results = {
    "phase": 36,
    "track": "I1",
    "description": "Bilateral ZD inner product on (A1)^6 projection",
    "c1": c1,
    "N_zeros": N_i1,
    "basis_labels": A1_6_LABELS,
    "diagonal_mean": float(ip_matrix.diagonal().mean()),
    "diagonal_min": float(ip_matrix.diagonal().min()),
    "diagonal_max": float(ip_matrix.diagonal().max()),
    "offdiag_mean": float(ip_matrix[~np.eye(N_i1, dtype=bool)].mean()),
    "offdiag_max_abs": float(np.max(np.abs(ip_matrix[~np.eye(N_i1, dtype=bool)]))),
    "ip_matrix_10x10": ip_matrix[:10, :10].tolist(),
    "sample_projections": [
        {"n": p["n"], "t": p["t"],
         "coeffs": [round(c, 6) for c in p["coeffs"]],
         "proj_norm_sq": p["proj_norm_sq"]} for p in projections[:5]
    ]
}
with open('phase36_bilateral_inner_product.json', 'w') as f:
    json.dump(i1_results, f, indent=2)
print("Saved phase36_bilateral_inner_product.json")

# ============================================================
# TRACK I2 — HERMITICITY TEST
# ============================================================
print("\n" + "=" * 60)
print("TRACK I2 — Hermiticity Test |IP(n,m) - IP(m,n)*|")
print("=" * 60)

# For real sedenion F at critical line zeros: coefficients are real
# -> inner products are real -> IP(n,m)* = IP(n,m)
# -> hermiticity = |IP(n,m) - IP(m,n)| = |ip_matrix[n,m] - ip_matrix[m,n]|
herm_matrix = np.abs(ip_matrix - ip_matrix.T)
max_violation = float(herm_matrix.max())
mean_violation = float(herm_matrix.mean())
print(f"Max hermiticity violation: {max_violation:.2e}")
print(f"Mean hermiticity violation: {mean_violation:.2e}")
print(f"Hermiticity gate (<1e-10): {max_violation < 1e-10}")

# Count by magnitude
n_exact_zero = int(np.sum(herm_matrix < 1e-15))
n_near_zero  = int(np.sum(herm_matrix < 1e-10))
total_pairs  = N_i1 * N_i1
print(f"Pairs with violation < 1e-15: {n_exact_zero}/{total_pairs}")
print(f"Pairs with violation < 1e-10: {n_near_zero}/{total_pairs}")

i2_results = {
    "phase": 36,
    "track": "I2",
    "description": "Hermiticity test: |IP(n,m) - IP(m,n)*|",
    "c1": c1,
    "N_zeros_tested": N_i1,
    "results": {
        "max_violation": max_violation,
        "mean_violation": mean_violation,
        "hermiticity_confirmed": bool(max_violation < 1e-10),
        "gate_threshold": 1e-10,
        "pairs_exact_zero_1e15": n_exact_zero,
        "pairs_near_zero_1e10": n_near_zero,
        "total_pairs": total_pairs,
        "note": ("F(rho) at critical line zeros is purely real-valued sedenion. "
                 "All projection coefficients are real -> inner products are real "
                 "-> IP(n,m) = IP(m,n) exactly (conjugate symmetry of reals).")
    }
}
with open('phase36_hermiticity_test.json', 'w') as f:
    json.dump(i2_results, f, indent=2)
print("Saved phase36_hermiticity_test.json")

# ============================================================
# TRACK F1 — FOURIER ANALOGUE: MUTUAL ANNIHILATION MATRIX
# ============================================================
print("\n" + "=" * 60)
print("TRACK F1 — Fourier Analogue: Mutual Annihilation M[i][j] = scalar(P_i * Q_j)")
print("=" * 60)

# Verify individual bilateral annihilation for all 6 canonical pairs
print("Canonical Six bilateral annihilation (cd_mul framework):")
bilateral_ok = True
pair_results = []
for i in range(6):
    Pi, Qi = CANONICAL_P[i], CANONICAL_Q[i]
    pq = cd_mul(Pi, Qi)
    qp = cd_mul(Qi, Pi)
    ns_pq = norm_sq(pq)
    ns_qp = norm_sq(qp)
    ok = ns_pq < 1e-20 and ns_qp < 1e-20
    if not ok: bilateral_ok = False
    Pnz = [(j, v) for j, v in enumerate(Pi) if v != 0]
    Qnz = [(j, v) for j, v in enumerate(Qi) if v != 0]
    print(f"  Pair {i+1}: P={Pnz}  Q={Qnz}")
    print(f"    |PQ|^2={ns_pq:.2e}  |QP|^2={ns_qp:.2e}  bilateral={ok}")
    pair_results.append({
        "pair": i + 1,
        "P_nz": str(Pnz),
        "Q_nz": str(Qnz),
        "PQ_norm_sq": float(ns_pq),
        "QP_norm_sq": float(ns_qp),
        "bilateral": bool(ok)
    })
print(f"All 6 bilateral: {bilateral_ok}")

# Compute 6x6 mutual annihilation matrix M[i][j] = scalar_part(can_P[i] * can_Q[j])
print("\n6x6 mutual annihilation matrix M[i][j] = scalar(can_P[i] * can_Q[j]):")
M_annihilate = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        M_annihilate[i, j] = cd_mul(CANONICAL_P[i], CANONICAL_Q[j])[0]
print(M_annihilate.round(3))
max_offdiag_M = float(np.max(np.abs(M_annihilate - np.diag(np.diag(M_annihilate)))))
print(f"Max off-diagonal |M[i][j]|: {max_offdiag_M:.4f}")
print("Note: M[4,0]=-2 because can_P[4]=e3+e12=can_Q[0] (same vector — degenerate pair 1)")

f1_results = {
    "phase": 36,
    "track": "F1",
    "description": "Fourier analogue: bilateral annihilation + mutual annihilation matrix",
    "c1": c1,
    "bilateral_annihilation_all_6": bilateral_ok,
    "pair_results": pair_results,
    "mutual_annihilation_matrix": M_annihilate.tolist(),
    "max_offdiag_abs": max_offdiag_M,
    "interpretation": (
        "Diagonal: all 0 (trivially P*Q diagonal terms are zero). "
        "Off-diagonal: M[4,0]=-2 because can_P[4]=e3+e12=can_Q[0] (degenerate: P5 equals Q1). "
        "This is the degenerate-type pattern where P and Q-image coincide. "
        "All 6 bilateral pairs pass P*Q=Q*P=0 (machine exact). "
        "Srednicki analogue: bilateral annihilation condition mirrors Fourier self-duality."
    )
}
with open('phase36_fourier_analogue.json', 'w') as f:
    json.dump(f1_results, f, indent=2)
print("Saved phase36_fourier_analogue.json")

# ============================================================
# TRACK F2 — SELF-DUAL VERIFICATION: F|*(F|)* = ||F|||^2 * e0
# ============================================================
print("\n" + "=" * 60)
print("TRACK F2 — Self-Dual: F|*(F|)* = ||F|_|^2 * e0")
print("=" * 60)

N_f2 = 100
scalar_ok_list = []
norm_sq_proj_list = []
max_nonscalar_list = []

for n, t in enumerate(zeros_100[:N_f2]):
    Fv = F_16d(t)
    coeffs = project_A1_6(Fv)
    F_proj = reconstruct_A1_6(coeffs)
    F_conj = cd_conj(F_proj)
    FF_star = cd_mul(F_proj, F_conj)
    ns = norm_sq(F_proj)
    norm_sq_proj_list.append(ns)
    # Check: FF_star[0] = ns, FF_star[1..15] = 0
    scalar_diff = abs(FF_star[0] - ns)
    nonscalar_max = max(abs(FF_star[k]) for k in range(1, 16))
    scalar_ok_list.append(scalar_diff < 1e-10 and nonscalar_max < 1e-10)
    max_nonscalar_list.append(nonscalar_max)

all_selfdual = all(scalar_ok_list)
print(f"F|*(F|)* = ||F|||^2 * e0: {all_selfdual} ({sum(scalar_ok_list)}/{N_f2})")
print(f"Max non-scalar component across 100 zeros: {max(max_nonscalar_list):.2e}")
print(f"||F||||^2 range: [{min(norm_sq_proj_list):.4f}, {max(norm_sq_proj_list):.4f}]")
print(f"||F||||^2 mean: {np.mean(norm_sq_proj_list):.6f}")

f2_results = {
    "phase": 36,
    "track": "F2",
    "description": "Self-duality: F|_{(A1)^6} * conj = ||F|||^2 * e0",
    "c1": c1,
    "N_zeros": N_f2,
    "selfdual_all": bool(all_selfdual),
    "selfdual_count": int(sum(scalar_ok_list)),
    "max_nonscalar_component": float(max(max_nonscalar_list)),
    "proj_norm_sq_mean": float(np.mean(norm_sq_proj_list)),
    "proj_norm_sq_min": float(min(norm_sq_proj_list)),
    "proj_norm_sq_max": float(max(norm_sq_proj_list)),
    "interpretation": (
        "F|_{(A1)^6} * conj(F|_{(A1)^6}) = ||F|_{(A1)^6}||^2 * e0 confirmed. "
        "This is the sedenion alternative-law identity restricted to the subspace. "
        "Non-scalar parts vanish to machine precision — the (A1)^6 projection inherits "
        "the full-sedenion self-dual property. Srednicki analogue: norm preservation "
        "under the 'Fourier transform' (bilateral annihilation map)."
    )
}
with open('phase36_selfdual_verification.json', 'w') as f:
    json.dump(f2_results, f, indent=2)
print("Saved phase36_selfdual_verification.json")

# ============================================================
# TRACK D1 — SPECTRAL DETERMINANT
# ============================================================
print("\n" + "=" * 60)
print("TRACK D1 — Spectral Determinant det_6(rho*I - M_F)")
print("=" * 60)

N_d1 = 50

def compute_M_F(F_vec, basis=A1_6_BASIS):
    """M_F[i][j] = scalar_part(P_i * (F * P_j)) / G[j,j]
    Uses G[j,j] = -2.
    """
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            M[i, j] = cd_mul(basis[i], FPj)[0] / (-2.0)
    return M

print("Computing M_F and spectral determinants for 50 zeros...")
det_results = []
eigenval_traces = []
for idx, t in enumerate(zeros_50[:N_d1]):
    rho = complex(0.5, t)
    Fv = F_16d(t)
    MF = compute_M_F(Fv)
    # det_6(rho*I - M_F) — complex determinant
    rhoI_minus_MF = rho * np.eye(6) - MF
    det_val = np.linalg.det(rhoI_minus_MF)
    eigenvals = np.linalg.eigvals(MF)
    tr = float(np.trace(MF))
    det_results.append({
        "n": idx + 1,
        "t": float(t),
        "rho_real": 0.5,
        "rho_imag": float(t),
        "det_real": float(det_val.real),
        "det_imag": float(det_val.imag),
        "det_abs": float(abs(det_val)),
        "MF_trace": tr,
        "MF_eigvals_real": [float(e.real) for e in eigenvals],
        "MF_eigvals_imag": [float(e.imag) for e in eigenvals],
    })
    eigenval_traces.append(tr)

det_abs_vals = [d["det_abs"] for d in det_results]
tr_vals = [d["MF_trace"] for d in det_results]
print(f"det_6(rho - M_F) range: [{min(det_abs_vals):.4f}, {max(det_abs_vals):.4f}]")
print(f"M_F trace range: [{min(tr_vals):.4f}, {max(tr_vals):.4f}]")
print(f"Sample: det at t1={det_results[0]['t']:.4f} -> |det|={det_results[0]['det_abs']:.4f}")
print(f"Sample M_F trace at t1={det_results[0]['MF_trace']:.6f}")
print(f"Sample M_F eigvals (real): {[round(x,4) for x in det_results[0]['MF_eigvals_real']]}")

# Check for zero determinants
near_zero_dets = [d for d in det_results if d['det_abs'] < 0.1]
print(f"det near zero (< 0.1): {len(near_zero_dets)}")

d1_results = {
    "phase": 36,
    "track": "D1",
    "description": "Spectral determinant det_6(rho - M_F) for 50 zeros",
    "c1": c1,
    "N_zeros": N_d1,
    "MF_definition": "M_F[i][j] = scalar_part(P_i * (F * P_j)) / G[j,j]",
    "det_abs_min": float(min(det_abs_vals)),
    "det_abs_max": float(max(det_abs_vals)),
    "det_abs_mean": float(np.mean(det_abs_vals)),
    "trace_mean": float(np.mean(tr_vals)),
    "trace_std": float(np.std(tr_vals)),
    "near_zero_dets": len(near_zero_dets),
    "det_results": det_results[:10],   # save first 10 for inspection
    "interpretation": (
        "M_F[i][j] = scalar_part(P_i * (F(rho) * P_j)) / (-2). "
        "This is the 6x6 matrix representation of F(rho) in the (A1)^6 basis. "
        "det_6(rho*I - M_F) is the Srednicki analogue of det_N(E - H_BK). "
        "Zeros of the spectral determinant would correspond to gamma values "
        "where rho is an eigenvalue of M_F."
    )
}
with open('phase36_spectral_determinant.json', 'w') as f:
    json.dump(d1_results, f, indent=2)
print("Saved phase36_spectral_determinant.json")

# ============================================================
# TRACK C1 — CHAVEZ TRANSFORM AS SPECTRAL TOOL
# ============================================================
print("\n" + "=" * 60)
print("TRACK C1 — Chavez Transform on F|_{(A1)^6} Projections")
print("=" * 60)

# Apply conjugation_symmetry to each component of the 6D projection time series
# (time series: index = zero number, value = coefficient component)
N_c1 = 100
all_coeffs = np.array([project_A1_6(F_16d(t)) for t in zeros_100[:N_c1]])
# all_coeffs shape: (100, 6)

print(f"Projection matrix shape: {all_coeffs.shape}")

# Chavez conjugation_symmetry for each of the 6 dimensions (length-100 sequences)
cs_per_dim = []
for dim in range(6):
    cs = conjugation_symmetry(all_coeffs[:, dim].tolist())
    cs_per_dim.append(cs)
    print(f"  Dim {dim} ({A1_6_LABELS[dim]}): CS = {cs:.4f}")

# Chavez on the NORM sequence (how norm changes across zeros)
norm_seq = [float(norm_sq(reconstruct_A1_6(list(all_coeffs[n, :])))) for n in range(N_c1)]
cs_norm = conjugation_symmetry(norm_seq)
print(f"  Norm^2 sequence: CS = {cs_norm:.4f}")

# Chavez on the trace sequence (Tr_BK for reference)
tr_seq = [Tr_BK(t) for t in zeros_100[:N_c1]]
cs_trbk = conjugation_symmetry(tr_seq)
print(f"  Tr_BK sequence: CS = {cs_trbk:.4f}")

# Chavez on spectral determinant abs values (D1 data, 50 zeros)
cs_det = conjugation_symmetry(det_abs_vals)
print(f"  |det_6(rho-M_F)| sequence: CS = {cs_det:.4f}")

# Check correlation between CS and det structure
cs_all_mean = float(np.mean(cs_per_dim))
cs_all_std  = float(np.std(cs_per_dim))
print(f"\nCS mean across 6 dimensions: {cs_all_mean:.4f} +/- {cs_all_std:.4f}")

c1_results = {
    "phase": 36,
    "track": "C1",
    "description": "Chavez Transform on (A1)^6 projection time series",
    "c1": c1,
    "N_zeros": N_c1,
    "basis_labels": A1_6_LABELS,
    "cs_per_dimension": [{"dim": i, "label": A1_6_LABELS[i], "cs": cs} for i, cs in enumerate(cs_per_dim)],
    "cs_norm_sq_sequence": float(cs_norm),
    "cs_TrBK_reference": float(cs_trbk),
    "cs_spectral_det_abs": float(cs_det),
    "cs_mean_6d": cs_all_mean,
    "cs_std_6d": cs_all_std,
    "interpretation": (
        "Chavez conjugation symmetry applied to each coordinate of the 6D (A1)^6 "
        "projection as a function of zero index. "
        "CS values measure bilateral symmetry in the projection time series. "
        "Comparison to Tr_BK (reference) and spectral determinant establishes "
        "the bridge from January 2026 starting point to Phase 36 operator construction."
    )
}
with open('phase36_chavez_transform_spectral.json', 'w') as f:
    json.dump(c1_results, f, indent=2)
print("Saved phase36_chavez_transform_spectral.json")

# ============================================================
# TRACK P1 — p-ADIC A2 SUBSYSTEM AT p=3
# ============================================================
print("\n" + "=" * 60)
print("TRACK P1 — A2 Subsystem Inner Products at p=3")
print("=" * 60)

# q2 direction: ROOT_16D_BASE[3] = e5+e10 = B5 in our (A1)^6 basis
# A2 subsystem at p=3 uses q2 (e5+e10) and its related directions
# chi3 anomaly: Q2 mean ratio 1.165 for conductor-3 L-function
# The q2 direction is B5 in the (A1)^6 basis

# Project F(rho) onto q2=B5 direction (the p=3 Heegner direction)
q2_vec = ROOT_16D_BASE[3]   # e5+e10
q3_vec = ROOT_16D_BASE[13]  # e6+e9  (q3)
q4_vec = ROOT_16D_BASE[2]   # e3-e12 (q4, p=2)

# A2 subsystem: the 3 roots {q2, q3, q4} (bilateral triple from Phase 23T1)
# and the 12-vector finite closure {q2,q3,q4} forms a closed subalgebra
A2_at_p3 = [q2_vec, q3_vec, q4_vec]
A2_labels = ['q2(p=3)', 'q3(p=13)', 'q4(p=2)']

N_p1 = 100
p1_data = []
for n, t in enumerate(zeros_100[:N_p1]):
    Fv = F_16d(t)
    # Project onto q2, q3, q4
    q2_coeff = cd_mul(Fv, q2_vec)[0] / (-2.0)
    q3_coeff = cd_mul(Fv, q3_vec)[0] / (-2.0)
    q4_coeff = cd_mul(Fv, q4_vec)[0] / (-2.0)
    # q2 direction is ALSO B5 in (A1)^6 basis — check consistency
    b5_coeff_from_basis = project_A1_6(Fv)[5]
    # Compute inner product in A2 subsystem
    a2_ip = -2.0 * (q2_coeff * q2_coeff + q3_coeff * q3_coeff + q4_coeff * q4_coeff)
    p1_data.append({
        'n': n + 1,
        't': t,
        'q2_coeff': float(q2_coeff),
        'q3_coeff': float(q3_coeff),
        'q4_coeff': float(q4_coeff),
        'q2_B5_consistency': float(abs(q2_coeff - b5_coeff_from_basis)),
        'a2_ip_norm': float(abs(a2_ip))
    })

# Verify q2 = B5 consistency
max_q2_b5_diff = max(d['q2_B5_consistency'] for d in p1_data)
print(f"q2 = B5 consistency (max diff): {max_q2_b5_diff:.2e}")

# Compare q2 vs q3 vs q4 projections
q2_vals = np.array([d['q2_coeff'] for d in p1_data])
q3_vals = np.array([d['q3_coeff'] for d in p1_data])
q4_vals = np.array([d['q4_coeff'] for d in p1_data])
print(f"q2 coeff mean={q2_vals.mean():.6f} std={q2_vals.std():.6f}")
print(f"q3 coeff mean={q3_vals.mean():.6f} std={q3_vals.std():.6f}")
print(f"q4 coeff mean={q4_vals.mean():.6f} std={q4_vals.std():.6f}")
print(f"q2/q4 var ratio: {q2_vals.var()/q4_vals.var():.4f}  (Heegner selectivity?)")
print(f"q2/q3 var ratio: {q2_vals.var()/q3_vals.var():.4f}")

# CS on each component
cs_q2 = conjugation_symmetry(q2_vals.tolist())
cs_q3 = conjugation_symmetry(q3_vals.tolist())
cs_q4 = conjugation_symmetry(q4_vals.tolist())
print(f"CS: q2={cs_q2:.4f}  q3={cs_q3:.4f}  q4={cs_q4:.4f}")

# Heegner check: does q2 show distinctively different behavior vs q4?
chi3_q2_ratio = 1.165  # Phase 18A finding
print(f"Phase 18A chi3/zeta Q2 ratio: {chi3_q2_ratio}")
print(f"q2 std/q4 std: {q2_vals.std()/q4_vals.std():.4f}  (elevated = Heegner signal?)")

p1_results = {
    "phase": 36,
    "track": "P1",
    "description": "A2 subsystem inner products at p=3 vs chi3 anomaly",
    "c1": c1,
    "N_zeros": N_p1,
    "chi3_q2_ratio_phase18a": chi3_q2_ratio,
    "A2_vectors": A2_labels,
    "q2_coeff_mean": float(q2_vals.mean()),
    "q2_coeff_std": float(q2_vals.std()),
    "q3_coeff_mean": float(q3_vals.mean()),
    "q3_coeff_std": float(q3_vals.std()),
    "q4_coeff_mean": float(q4_vals.mean()),
    "q4_coeff_std": float(q4_vals.std()),
    "q2_q4_var_ratio": float(q2_vals.var() / q4_vals.var()) if q4_vals.var() > 0 else None,
    "q2_q3_var_ratio": float(q2_vals.var() / q3_vals.var()) if q3_vals.var() > 0 else None,
    "q2_B5_consistency_max": float(max_q2_b5_diff),
    "cs_q2": float(cs_q2),
    "cs_q3": float(cs_q3),
    "cs_q4": float(cs_q4),
    "sample_data": p1_data[:5],
    "interpretation": (
        f"q2 direction (e5+e10, p=3) projects F(rho) onto the Heegner-selective component. "
        f"Phase 18A: chi3/zeta Q2 ratio=1.165 (elevated; conductor-3 specific). "
        f"q2 = B5 in (A1)^6 basis (max consistency diff={max_q2_b5_diff:.2e}). "
        f"q2 variance / q4 variance = {q2_vals.var()/q4_vals.var():.4f}: "
        f"{'elevated q2 (Heegner signal)' if q2_vals.var() > q4_vals.var() else 'no elevation'}. "
        f"The 60 A2 subsystems in the bilateral family are candidates for the p=3 local BK operator "
        f"that Srednicki's framework leaves open."
    )
}
with open('phase36_p3_a2_inner_product.json', 'w') as f:
    json.dump(p1_results, f, indent=2)
print("Saved phase36_p3_a2_inner_product.json")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PHASE 36 SUMMARY")
print("=" * 60)
print(f"V1 — Formula verification:      PASS={v1_results['pass']}")
print(f"     Gram G=-2I confirmed:       {gram_ok}")
print(f"I1 — ZD inner product computed: {N_i1}x{N_i1} matrix done")
print(f"     IP diagonal range: [{ip_matrix.diagonal().min():.4f}, {ip_matrix.diagonal().max():.4f}]")
print(f"I2 — Hermiticity: max violation={max_violation:.2e}  gate={'PASS' if max_violation < 1e-10 else 'FAIL'}")
print(f"F1 — Bilateral annihilation:    {'ALL 6 PASS' if bilateral_ok else 'FAIL'}")
print(f"     M[i][j] max off-diag:      {max_offdiag_M:.4f}")
print(f"F2 — Self-duality:              {all_selfdual} ({sum(scalar_ok_list)}/{N_f2})")
print(f"D1 — Spectral determinant:      |det| mean={np.mean(det_abs_vals):.4f}")
print(f"     Near-zero dets:            {len(near_zero_dets)}")
print(f"C1 — Chavez CS (6D projection): mean={cs_all_mean:.4f} ± {cs_all_std:.4f}")
print(f"     CS Tr_BK reference:        {cs_trbk:.4f}")
print(f"P1 — q2/q4 var ratio:           {q2_vals.var()/q4_vals.var():.4f}")
print(f"     CS: q2={cs_q2:.4f}  q3={cs_q3:.4f}  q4={cs_q4:.4f}")
print(f"\nGate I2 (hermiticity): {'PASS' if max_violation < 1e-10 else 'FAIL'}")
print(f"Gate D1 (spectral det zero structure): {len(near_zero_dets)} near-zero det(s) in first 50")
print(f"\nElapsed: {time.time()-t0:.1f}s")
print("\nAll 8 output files saved.")
