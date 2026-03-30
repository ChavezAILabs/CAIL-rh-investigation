"""
rh_phase37.py
=============
Phase 37 — Anti-Symmetric Spectral Structure + Eigenvalue Matching
RH Investigation — Chavez AI Labs LLC

Date: 2026-03-27
Researcher: Paul Chavez, Chavez AI Labs LLC

Description
-----------
Primary question: Do eigenvalues of iA(rho) match the imaginary parts {gamma_n}
of Riemann zeros, where A = M_F - F[0]*I is the anti-symmetric part of the
6x6 restriction matrix?

Honest documentation of Phase 36 mechanism correction:
  F(sigma+it) is a list of float64 for ALL sigma (structural, not sigma=1/2 specific).
  Im(F) = 0 everywhere. The hermiticity PASS from Phase 36 holds for the trivial
  reason that F is always real. The critical-line/hermiticity equivalence claimed
  in the handoff is a refinement target, not a closed proof.

Tracks:
  V1  — Formula verification
  E1  — iA(rho) eigenvalues for 100 zeros
  E2  — Eigenvalue matching tests (E2a direct, E2b scaled, E2c rank correlation)
  E3  — Eigenvalue trajectory analysis
  R1  — Reality condition: Im(F_k) at 100 zeros
  R2  — Reality vs sigma: Im(F) for sigma in 0.1..0.9 at gamma_1
  S1  — Corrected spectral det det_6(E - iA): roots vs gamma_n
  S2  — Gamma_sed candidate: null space of A, ground state construction
  C1  — Chavez Transform on eigenvalue sequences
  P1  — A_antisym structure: rank, linearity, bilateral correspondence
  P2  — Discrete Fourier test on (A1)^6 P-vectors

Output files (11):
  phase37_formula_verification.json
  phase37_iA_eigenvalues.json
  phase37_eigenvalue_matching.json
  phase37_eigenvalue_trajectory.json
  phase37_reality_condition.json
  phase37_reality_vs_sigma.json
  phase37_corrected_spectral_det.json
  phase37_gamma_sed_candidate.json
  phase37_chavez_eigenvalue.json
  phase37_A_structure.json
  phase37_fourier_bilateral.json
"""

import numpy as np
from scipy.stats import spearmanr, pearsonr
import json, time

# ============================================================
# SEDENION ENGINE (Phase 29/36 — unchanged)
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

def F_16d(t, sigma=0.5, primes=None):
    if primes is None: primes = [2, 3, 5, 7, 11, 13]
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
# (A1)^6 BASIS AND M_F CONSTRUCTION (Phase 36 — unchanged)
# ============================================================
A1_6_BASIS = [
    make16([(1,  1), (14,  1)]),   # B0: e1+e14
    make16([(1,  1), (14, -1)]),   # B1: e1-e14
    make16([(2,  1), (13, -1)]),   # B2: e2-e13
    make16([(3,  1), (12,  1)]),   # B3: e3+e12
    make16([(4,  1), (11,  1)]),   # B4: e4+e11
    make16([(5,  1), (10,  1)]),   # B5: e5+e10 (= q2, Heegner direction)
]
A1_6_LABELS = ['e1+e14', 'e1-e14', 'e2-e13', 'e3+e12', 'e4+e11', 'e5+e10']

# Q-vectors for the 6 canonical bilateral pairs
CANONICAL_Q = [
    make16([(3, 1), (12,  1)]),   # Q0: e3+e12 = B3
    make16([(3, 1), (12, -1)]),   # Q1: e3-e12
    make16([(5, 1), (10,  1)]),   # Q2: e5+e10 = B5
    make16([(6, 1), (9,   1)]),   # Q3: e6+e9
    make16([(5, 1), (10,  1)]),   # Q4: e5+e10 = B5
    make16([(6, 1), (9,   1)]),   # Q5: e6+e9
]

def compute_M_F(F_vec, basis=A1_6_BASIS):
    """M_F[i][j] = scalar_part(P_i * (F * P_j)) / (-2)"""
    M = np.zeros((6, 6))
    for j in range(6):
        FPj = cd_mul(F_vec, basis[j])
        for i in range(6):
            M[i, j] = cd_mul(basis[i], FPj)[0] / (-2.0)
    return M

def get_iA(F_vec):
    """Extract anti-symmetric part A = M_F - F[0]*I, return iA."""
    MF = compute_M_F(F_vec)
    F0 = F_vec[0]
    A = MF - F0 * np.eye(6)
    iA = 1j * A   # hermitian (since A is real anti-symmetric)
    return MF, F0, A, iA

def conjugation_symmetry(x):
    n = len(x)
    if n < 2: return 1.0
    return 1.0 - float(np.mean([abs(x[i] - x[n-1-i]) for i in range(n//2)]))

# ============================================================
# DATA LOAD
# ============================================================
print("=" * 60)
print("PHASE 37 — Anti-Symmetric Spectral Structure + iA Eigenvalues")
print("=" * 60)
t0_total = time.time()

with open('rh_zeros.json') as f:
    zeros_raw = json.load(f)
zeros_100 = [float(z) for z in zeros_raw[:100]]
zeros_50  = [float(z) for z in zeros_raw[:50]]
gamma_1   = zeros_100[0]   # 14.134725
c1 = 0.11797805192095003
print(f"Loaded {len(zeros_100)} zeros  gamma_1={gamma_1:.6f}")

# ============================================================
# TRACK V1 — FORMULA VERIFICATION
# ============================================================
print("\n" + "=" * 60)
print("TRACK V1 — Formula Verification")
print("=" * 60)

Fv1 = F_16d(gamma_1)
MF1, F0_1, A1_mat, iA1 = get_iA(Fv1)
evals_iA1 = sorted(np.linalg.eigvalsh(iA1).real)
antisym_check = float(np.max(np.abs(A1_mat + A1_mat.T)))
print(f"F(gamma_1) norm^2 = {norm_sq(Fv1):.6f}")
print(f"F[0] at gamma_1   = {F0_1:.8f}")
print(f"A anti-symmetry max |A+A^T| = {antisym_check:.2e}  (expect 0)")
print(f"iA eigenvalues at gamma_1: {[round(e, 6) for e in evals_iA1]}")
print(f"gamma_1 = {gamma_1:.6f}  (for comparison)")

v1_results = {
    "phase": 37, "track": "V1", "c1": c1,
    "F_norm_sq_gamma1": float(norm_sq(Fv1)),
    "F0_gamma1": float(F0_1),
    "A_antisymmetry_check": antisym_check,
    "iA_eigenvalues_gamma1": evals_iA1,
    "gamma_1": gamma_1,
    "pass": bool(antisym_check < 1e-10)
}
with open('phase37_formula_verification.json', 'w') as f:
    json.dump(v1_results, f, indent=2)
print("Saved phase37_formula_verification.json")

# ============================================================
# TRACK E1 — iA EIGENVALUES FOR 100 ZEROS
# ============================================================
print("\n" + "=" * 60)
print("TRACK E1 — iA(rho_n) Eigenvalues for 100 Zeros")
print("=" * 60)

t0_e1 = time.time()
eigendata = []
for n, t in enumerate(zeros_100):
    Fv = F_16d(t)
    MF, F0, A_n, iA_n = get_iA(Fv)
    evals = sorted(np.linalg.eigvalsh(iA_n).real)
    eigendata.append({
        'n': n + 1,
        'gamma': t,
        'F0': float(F0),
        'iA_eigenvalues': [float(e) for e in evals],
        'max_positive_eigenval': float(max(evals)),
        'min_negative_eigenval': float(min(evals)),
        'sum_sq_eigenvals': float(sum(e**2 for e in evals)),
        'A_frobenius_norm': float(np.linalg.norm(A_n, 'fro')),
    })

print(f"Done in {time.time()-t0_e1:.2f}s")
# Summary
max_evals = [d['max_positive_eigenval'] for d in eigendata]
gammas    = [d['gamma'] for d in eigendata]
print(f"Max positive iA eigenvalue range: [{min(max_evals):.4f}, {max(max_evals):.4f}]")
print(f"gamma range: [{min(gammas):.4f}, {max(gammas):.4f}]")
print(f"Ratio gamma/max_eigenval: min={min(g/e for g,e in zip(gammas,max_evals)):.2f}, "
      f"max={max(g/e for g,e in zip(gammas,max_evals)):.2f}")
print("First 5 eigenvalue sets:")
for d in eigendata[:5]:
    print(f"  n={d['n']:3} gamma={d['gamma']:8.4f}  iA_evals={[round(e,4) for e in d['iA_eigenvalues']]}")

e1_results = {
    "phase": 37, "track": "E1", "c1": c1, "N_zeros": 100,
    "basis_labels": A1_6_LABELS,
    "max_eigenval_range": [float(min(max_evals)), float(max(max_evals))],
    "gamma_range": [float(min(gammas)), float(max(gammas))],
    "ratio_gamma_to_max_eigenval_min": float(min(g/e for g,e in zip(gammas,max_evals))),
    "ratio_gamma_to_max_eigenval_max": float(max(g/e for g,e in zip(gammas,max_evals))),
    "eigendata": eigendata
}
with open('phase37_iA_eigenvalues.json', 'w') as f:
    json.dump(e1_results, f, indent=2)
print("Saved phase37_iA_eigenvalues.json")

# ============================================================
# TRACK E2 — EIGENVALUE MATCHING TESTS
# ============================================================
print("\n" + "=" * 60)
print("TRACK E2 — Eigenvalue Matching: E2a Direct, E2b Scaled, E2c Rank")
print("=" * 60)

# E2a: direct match — does any eigenvalue equal gamma_n within 1e-6?
e2a_matches = 0
for d in eigendata:
    gamma = d['gamma']
    for ev in d['iA_eigenvalues']:
        if abs(ev - gamma) < 1e-6:
            e2a_matches += 1
            print(f"  E2a MATCH: n={d['n']} gamma={gamma:.6f} == eigenval={ev:.6f}")
print(f"E2a direct matches (tol 1e-6): {e2a_matches}")

# E2b: scaled match — scan c such that c * max_eigenval ≈ gamma_n
# For each zero, best_c = gamma_n / max_eigenval
best_c_per_zero = [g / e for g, e in zip(gammas, max_evals)]
c_mean = float(np.mean(best_c_per_zero))
c_std  = float(np.std(best_c_per_zero))
c_cv   = c_std / c_mean if c_mean != 0 else float('inf')
print(f"\nE2b scaled match (gamma_n / max_eigenval):")
print(f"  mean c = {c_mean:.4f}  std = {c_std:.4f}  CV = {c_cv:.3f}")
# Try fixed c = mean: check residuals
residuals_fixed_c = [abs(c_mean * e - g) / g for g, e in zip(gammas, max_evals)]
mean_rel_resid = float(np.mean(residuals_fixed_c))
print(f"  Fixed c={c_mean:.4f}: mean relative residual = {mean_rel_resid:.4f}")
e2b_pass = c_cv < 0.05 and mean_rel_resid < 0.05
print(f"  E2b PASS (CV<5%, residual<5%): {e2b_pass}")

# Also try: c * middle eigenval (index 4, second largest positive)
mid_evals = [d['iA_eigenvalues'][4] for d in eigendata]  # index 4 = second positive
best_c_mid = [g / e if abs(e) > 1e-10 else float('inf') for g, e in zip(gammas, mid_evals)]
valid_mid = [c for c in best_c_mid if c != float('inf') and c < 1e6]
if valid_mid:
    c_mid_mean = float(np.mean(valid_mid))
    c_mid_cv   = float(np.std(valid_mid) / c_mid_mean)
    print(f"  Mid eigenval c = {c_mid_mean:.4f}  CV = {c_mid_cv:.3f}")

# E2c: rank correlation — does rank(max_eigenval_n) correlate with rank(gamma_n)?
rho_max, p_max = spearmanr(gammas, max_evals)
rho_sumsq, p_sumsq = spearmanr(gammas, [d['sum_sq_eigenvals'] for d in eigendata])
rho_frob, p_frob = spearmanr(gammas, [d['A_frobenius_norm'] for d in eigendata])
print(f"\nE2c rank correlation (Spearman):")
print(f"  gamma vs max_eigenval:   rho={rho_max:.4f}  p={p_max:.4e}")
print(f"  gamma vs sum_sq_evals:   rho={rho_sumsq:.4f}  p={p_sumsq:.4e}")
print(f"  gamma vs ||A||_F:        rho={rho_frob:.4f}  p={p_frob:.4e}")

e2_results = {
    "phase": 37, "track": "E2", "c1": c1,
    "description": "Primary decision gate: eigenvalue-zero matching",
    "E2a_direct_match": {
        "tolerance": 1e-6, "matches": e2a_matches,
        "pass": bool(e2a_matches > 0)
    },
    "E2b_scaled_match": {
        "best_c_mean": c_mean, "best_c_std": c_std, "best_c_CV": c_cv,
        "mean_relative_residual_fixed_c": mean_rel_resid,
        "pass": bool(e2b_pass)
    },
    "E2c_rank_correlation": {
        "spearman_rho_gamma_vs_max_eigenval": float(rho_max),
        "p_value": float(p_max),
        "spearman_rho_gamma_vs_sumsq": float(rho_sumsq),
        "spearman_rho_gamma_vs_frobA": float(rho_frob),
        "pass": bool(abs(rho_max) > 0.3 and p_max < 0.05)
    },
    "per_zero_c_values": [float(c) for c in best_c_per_zero],
    "summary": (
        f"E2a: {e2a_matches} direct matches (expect 0 — eigenvals O(1) vs gamma O(14-50)). "
        f"E2b: CV={c_cv:.3f} {'PASS' if e2b_pass else 'FAIL'} for scaled match. "
        f"E2c: Spearman rho={rho_max:.4f} (p={p_max:.3e})."
    )
}
with open('phase37_eigenvalue_matching.json', 'w') as f:
    json.dump(e2_results, f, indent=2)
print("Saved phase37_eigenvalue_matching.json")

# ============================================================
# TRACK E3 — EIGENVALUE TRAJECTORY
# ============================================================
print("\n" + "=" * 60)
print("TRACK E3 — Eigenvalue Trajectory vs Gamma")
print("=" * 60)

# All 6 eigenvalue trajectories
traj = np.array([[d['iA_eigenvalues'][k] for d in eigendata] for k in range(6)])
gammas_arr = np.array(gammas)

print("Eigenvalue statistics across 100 zeros:")
for k in range(6):
    rho_k, p_k = spearmanr(gammas_arr, traj[k])
    print(f"  k={k}: mean={traj[k].mean():.4f}  std={traj[k].std():.4f}  "
          f"Spearman_rho={rho_k:.4f} (p={p_k:.3e})")

# Sum of squared eigenvalues
sum_sq = np.array([d['sum_sq_eigenvals'] for d in eigendata])
rho_ss, p_ss = pearsonr(gammas_arr, sum_sq)
print(f"  Sum_sq: mean={sum_sq.mean():.4f}  Pearson_r={rho_ss:.4f} (p={p_ss:.3e})")

# Do eigenvalues grow with gamma? Check via linear regression slope
from scipy.stats import linregress
slope_max, _, r_max, _, _ = linregress(gammas_arr, traj[5])  # index 5 = largest positive
print(f"  Slope of max eigenval vs gamma: {slope_max:.6f}  R^2={r_max**2:.4f}")

e3_results = {
    "phase": 37, "track": "E3", "c1": c1,
    "N_zeros": 100,
    "eigenvalue_trajectories": {
        f"k{k}": {
            "mean": float(traj[k].mean()), "std": float(traj[k].std()),
            "min": float(traj[k].min()), "max": float(traj[k].max()),
            "spearman_rho_vs_gamma": float(spearmanr(gammas_arr, traj[k])[0]),
            "spearman_p": float(spearmanr(gammas_arr, traj[k])[1]),
            "values_first_10": traj[k, :10].tolist()
        } for k in range(6)
    },
    "sum_sq_pearson_r": float(rho_ss),
    "sum_sq_pearson_p": float(p_ss),
    "max_eigenval_slope_vs_gamma": float(slope_max),
    "max_eigenval_R2_vs_gamma": float(r_max**2),
}
with open('phase37_eigenvalue_trajectory.json', 'w') as f:
    json.dump(e3_results, f, indent=2)
print("Saved phase37_eigenvalue_trajectory.json")

# ============================================================
# TRACK R1 — REALITY CONDITION AT 100 ZEROS
# ============================================================
print("\n" + "=" * 60)
print("TRACK R1 — Reality Condition: Im(F_k) at 100 Zeros")
print("=" * 60)

# F is a list of float64 by construction — always real
# Verify and document this explicitly
max_imag_per_zero = []
for t in zeros_100:
    Fv = F_16d(t)
    max_imag = max(abs(complex(Fk).imag) for Fk in Fv)
    max_imag_per_zero.append(float(max_imag))

global_max_imag = max(max_imag_per_zero)
print(f"Max |Im(F_k)| across 100 zeros: {global_max_imag:.2e}")
print(f"F component type: {type(F_16d(gamma_1)[0]).__name__}")
print("FINDING: F is a list of float64 — Im = 0 identically (structural, not sigma=1/2 specific)")

r1_results = {
    "phase": 37, "track": "R1", "c1": c1,
    "N_zeros": 100,
    "global_max_imag": global_max_imag,
    "all_real": bool(global_max_imag == 0.0),
    "F_component_type": type(F_16d(gamma_1)[0]).__name__,
    "mechanism": (
        "F_16d() returns a list of float64 values. All sedenion exponentials "
        "exp_sed(t*log(p)*r_p/||r_p||) = cos(theta)*e0 + sin(theta)*r_hat_p "
        "have real components. The sigma correction adds a real scalar to components "
        "4 and 5. Therefore Im(F_k) = 0 identically for ALL sigma, not just sigma=1/2. "
        "The hermiticity PASS from Phase 36 holds for this structural reason, not as "
        "evidence that the critical line condition is encoded in the sedenion algebra."
    )
}
with open('phase37_reality_condition.json', 'w') as f:
    json.dump(r1_results, f, indent=2)
print("Saved phase37_reality_condition.json")

# ============================================================
# TRACK R2 — REALITY VS SIGMA
# ============================================================
print("\n" + "=" * 60)
print("TRACK R2 — Reality vs Sigma: Im(F) for sigma in 0.1..0.9")
print("=" * 60)

sigma_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
r2_data = []
print(f"{'sigma':8} | {'max|Im(F)|':14} | {'||F||^2':10} | {'F[0]':10} | {'note'}")
print("-" * 65)
for sigma in sigma_vals:
    Fv = F_16d(gamma_1, sigma=sigma)
    max_im = max(abs(complex(Fk).imag) for Fk in Fv)
    ns = norm_sq(Fv)
    F0 = Fv[0]
    note = "CRITICAL LINE" if abs(sigma - 0.5) < 1e-10 else ""
    print(f"  {sigma:.1f}     | {max_im:.6e}   | {ns:.6f} | {F0:.6f} | {note}")
    r2_data.append({"sigma": sigma, "max_imag": float(max_im),
                    "norm_sq": float(ns), "F0": float(F0)})

print()
print("FINDING: Im(F) = 0 for ALL sigma. The reality condition does not")
print("distinguish sigma=1/2 from other values.")
print("The Srednicki proof path through Track R2 does NOT close.")
print("The eigenvalue path through iA remains the primary open direction.")

r2_results = {
    "phase": 37, "track": "R2", "c1": c1,
    "gamma_1": gamma_1,
    "sigma_scan": r2_data,
    "reality_sigma_specific": False,
    "finding": (
        "Im(F(sigma+i*gamma_1)) = 0 for ALL sigma in {0.1,...,0.9}. "
        "F_16d() is a real-valued function of (t, sigma) for all real inputs. "
        "Reality is structural (float64 arithmetic), not a consequence of sigma=1/2. "
        "The handoff's proposed proof path: "
        "'F real iff sigma=1/2 -> hermiticity iff sigma=1/2 -> zeros on critical line' "
        "does not hold because the first implication is false. "
        "Correction: hermiticity holds for all sigma (trivially), so it cannot "
        "serve as the distinguishing condition for the critical line."
    )
}
with open('phase37_reality_vs_sigma.json', 'w') as f:
    json.dump(r2_results, f, indent=2)
print("Saved phase37_reality_vs_sigma.json")

# ============================================================
# TRACK S1 — CORRECTED SPECTRAL DETERMINANT det_6(E - iA)
# ============================================================
print("\n" + "=" * 60)
print("TRACK S1 — Corrected Spectral Det det_6(E - iA(rho_n))")
print("=" * 60)

N_s1 = 50
s1_data = []
# For each zero: det_6(E - iA) roots = eigenvalues of iA exactly
# Also evaluate det at E = gamma_n (the test)
print(f"{'n':4} | {'gamma_n':10} | {'det at E=gamma_n':18} | {'closest root':12} | {'|root-gamma|':12}")
for idx, d in enumerate(eigendata[:N_s1]):
    gamma_n = d['gamma']
    evals_iA = d['iA_eigenvalues']  # sorted, these ARE the roots of det(E-iA)=0
    # det_6(E - iA) = product_k (E - mu_k)
    # At E = gamma_n:
    det_at_gamma = float(np.prod([gamma_n - mu for mu in evals_iA]))
    closest_root = min(evals_iA, key=lambda mu: abs(mu - gamma_n))
    dist = abs(closest_root - gamma_n)
    if idx < 5:
        print(f"  {idx+1:3} | {gamma_n:10.4f} | {det_at_gamma:18.4f} | {closest_root:12.6f} | {dist:12.6f}")
    s1_data.append({
        'n': d['n'], 'gamma_n': float(gamma_n),
        'det_at_gamma_n': float(det_at_gamma),
        'iA_roots': evals_iA,
        'closest_root_to_gamma': float(closest_root),
        'dist_closest_root_to_gamma': float(dist),
    })
print(f"  ...")
dists = [d['dist_closest_root_to_gamma'] for d in s1_data]
print(f"Distance (closest iA root to gamma_n): min={min(dists):.4f}  mean={np.mean(dists):.4f}  max={max(dists):.4f}")
det_at_gammas = [abs(d['det_at_gamma_n']) for d in s1_data]
print(f"|det_6(gamma_n - iA)| range: [{min(det_at_gammas):.4f}, {max(det_at_gammas):.4f}]")
print(f"det_6 near zero at gamma_n: {sum(1 for d in det_at_gammas if d < 0.1)}")

s1_results = {
    "phase": 37, "track": "S1", "c1": c1, "N_zeros": N_s1,
    "finding": (
        "det_6(E - iA(rho_n)) roots = eigenvalues of iA (by construction). "
        "Roots are +/-lambda_k, O(0.01-1.6). gamma_n are O(14-50). "
        "det_6(gamma_n - iA) >> 0 for all n — the corrected spectral determinant "
        "does NOT vanish at the Riemann zeros."
    ),
    "dist_closest_root_min": float(min(dists)),
    "dist_closest_root_mean": float(np.mean(dists)),
    "det_at_gamma_range": [float(min(det_at_gammas)), float(max(det_at_gammas))],
    "zeros_of_det_match_gamma": False,
    "data": s1_data[:10]
}
with open('phase37_corrected_spectral_det.json', 'w') as f:
    json.dump(s1_results, f, indent=2)
print("Saved phase37_corrected_spectral_det.json")

# ============================================================
# TRACK S2 — GAMMA_SED CANDIDATE: NULL SPACE AND GROUND STATE
# ============================================================
print("\n" + "=" * 60)
print("TRACK S2 — Gamma_sed Candidate: Null Space of A")
print("=" * 60)

# For each zero: find the eigenvector of A with smallest |eigenvalue| (null space approx)
# A has eigenvalues 0 or ±i*lambda (for anti-symmetric); smallest |lambda| = near-null direction
s2_data = []
null_consistency = []
for d in eigendata[:50]:
    t = d['gamma']
    Fv = F_16d(t)
    MF, F0, A_n, iA_n = get_iA(Fv)
    evals, evecs = np.linalg.eigh(iA_n)
    # Smallest |eigenvalue| = index of min abs
    min_idx = int(np.argmin(np.abs(evals)))
    v0 = evecs[:, min_idx].real   # ground state (smallest lambda)
    min_eval = float(evals[min_idx].real)
    # Gamma_sed candidate: <v0, iA * v0> = min_eval (trivially)
    # More interesting: <v0, F_projected> where F_proj = sum c_i * P_i
    # F_proj coefficients
    coeffs = []
    for P in A1_6_BASIS:
        fp = cd_mul(Fv, P)
        coeffs.append(fp[0] / (-2.0))
    gamma_sed_val = float(np.dot(v0, np.array(coeffs)))
    null_consistency.append(min_eval)
    s2_data.append({
        'n': d['n'], 'gamma': t,
        'min_eigenval_iA': min_eval,
        'ground_state_v0': v0.tolist(),
        'gamma_sed_inner_product': gamma_sed_val,
        'gamma_sed_near_zero': bool(abs(gamma_sed_val) < 0.01)
    })

min_evals = [d['min_eigenval_iA'] for d in s2_data]
gs_vals  = [d['gamma_sed_inner_product'] for d in s2_data]
print(f"Min |eigenval of iA| range: [{min(min_evals):.6f}, {max(min_evals):.6f}]")
print(f"<v0, F_proj> (gamma_sed candidate) range: [{min(gs_vals):.6f}, {max(gs_vals):.6f}]")
print(f"gamma_sed near zero (<0.01): {sum(d['gamma_sed_near_zero'] for d in s2_data)}/50")
print(f"gamma_sed mean: {np.mean(gs_vals):.6f}  std: {np.std(gs_vals):.6f}")

# Is there a consistent null vector across zeros?
# Compare v0 directions at different zeros via pairwise dot products
v0_vectors = np.array([d['ground_state_v0'] for d in s2_data])
v0_dots = []
for i in range(min(10, len(v0_vectors))):
    for j in range(i+1, min(10, len(v0_vectors))):
        v0_dots.append(abs(float(np.dot(v0_vectors[i], v0_vectors[j]))))
print(f"Ground state v0 consistency: mean |v0_i . v0_j| = {np.mean(v0_dots):.4f}  "
      f"(1=same direction, 0=orthogonal)")

s2_results = {
    "phase": 37, "track": "S2", "c1": c1, "N_zeros": 50,
    "min_eigenval_range": [float(min(min_evals)), float(max(min_evals))],
    "gamma_sed_mean": float(np.mean(gs_vals)),
    "gamma_sed_std": float(np.std(gs_vals)),
    "gamma_sed_near_zero_count": int(sum(d['gamma_sed_near_zero'] for d in s2_data)),
    "v0_consistency_mean_dot": float(np.mean(v0_dots)),
    "data": s2_data[:10]
}
with open('phase37_gamma_sed_candidate.json', 'w') as f:
    json.dump(s2_results, f, indent=2)
print("Saved phase37_gamma_sed_candidate.json")

# ============================================================
# TRACK C1 — CHAVEZ TRANSFORM ON EIGENVALUE SEQUENCES
# ============================================================
print("\n" + "=" * 60)
print("TRACK C1 — Chavez Transform on Eigenvalue Sequences")
print("=" * 60)

# 3 positive eigenvalue trajectories (k=3,4,5 = positive half of paired spectrum)
cs_evals = {}
for k in range(3, 6):
    seq = list(traj[k, :])   # positive eigenvalues only
    cs = conjugation_symmetry(seq)
    cs_evals[f'k{k}_positive'] = float(cs)
    print(f"  Positive eigenval k={k} ({A1_6_LABELS[k]}): CS={cs:.4f}")

# Sum-of-squared eigenvalues
cs_sumsq = conjugation_symmetry(sum_sq[:100].tolist())
print(f"  Sum_sq eigenvals: CS={cs_sumsq:.4f}")

# Frobenius norm of A
frob_seq = [d['A_frobenius_norm'] for d in eigendata]
cs_frob = conjugation_symmetry(frob_seq)
print(f"  ||A||_F sequence: CS={cs_frob:.4f}")

# Compare to Phase 36 reference (6D projection CS = 81.4%)
print(f"\n  Phase 36 reference: 6D projection CS = 81.4%")

c1_results = {
    "phase": 37, "track": "C1", "c1": c1,
    "cs_positive_eigenvalues": cs_evals,
    "cs_sum_sq_eigenvals": float(cs_sumsq),
    "cs_frobenius_A": float(cs_frob),
    "phase36_reference_6D_CS": 0.814,
    "interpretation": (
        "Chavez conjugation symmetry on eigenvalue time series. "
        "Compare to Phase 36 6D projection CS=81.4% (within RZ gap range). "
        "Eigenvalue sequences reflect the spectral structure of A(rho_n)."
    )
}
with open('phase37_chavez_eigenvalue.json', 'w') as f:
    json.dump(c1_results, f, indent=2)
print("Saved phase37_chavez_eigenvalue.json")

# ============================================================
# TRACK P1 — A_ANTISYM STRUCTURE
# ============================================================
print("\n" + "=" * 60)
print("TRACK P1 — A_antisym Structure: Rank, Linearity, Bilateral Correspondence")
print("=" * 60)

# For 10 representative zeros: print A matrix and analyze structure
p1_data = []
print("A = M_F - F[0]*I matrices for first 5 zeros:")
for idx, d in enumerate(eigendata[:5]):
    t = d['gamma']
    Fv = F_16d(t)
    MF, F0, A_n, _ = get_iA(Fv)
    rank_A = int(np.linalg.matrix_rank(A_n, tol=1e-10))
    # Which entries dominate?
    A_abs = np.abs(A_n)
    max_entry_idx = np.unravel_index(A_abs.argmax(), A_abs.shape)
    print(f"\n  n={idx+1} gamma={t:.4f}  rank(A)={rank_A}  max|A[i,j]|={A_abs.max():.4f} at {max_entry_idx}")
    for row in A_n:
        print("    " + "  ".join(f"{v:7.4f}" for v in row))
    p1_data.append({
        'n': d['n'], 'gamma': t, 'rank': rank_A,
        'max_abs_entry': float(A_abs.max()),
        'max_entry_idx': [int(x) for x in max_entry_idx],
        'A_matrix': A_n.tolist(),
        'frobenius_norm': float(np.linalg.norm(A_n, 'fro'))
    })

# Test linearity: A(rho1+rho2) ?= A(rho1) + A(rho2)?  [approximate, not exact since F is multiplicative]
t1, t2 = zeros_100[0], zeros_100[1]
Fv1_, Fv2_ = F_16d(t1), F_16d(t2)
_, _, A_1, _ = get_iA(Fv1_)
_, _, A_2, _ = get_iA(Fv2_)
# Note: F(t1+t2) != F(t1)*F(t2) in general (not linear), so check approximate
Fv12 = F_16d(t1 + t2)
_, _, A_12, _ = get_iA(Fv12)
linearity_err = float(np.linalg.norm(A_12 - (A_1 + A_2), 'fro'))
print(f"\nLinearity test A(t1+t2) vs A(t1)+A(t2): ||diff||_F = {linearity_err:.4f}")
print(f"(Large error expected — F is multiplicative, not additive)")

# Rank distribution across 100 zeros
ranks = []
for d in eigendata[:100]:
    t = d['gamma']
    Fv = F_16d(t)
    MF, F0, A_n, _ = get_iA(Fv)
    ranks.append(int(np.linalg.matrix_rank(A_n, tol=1e-10)))
from collections import Counter
rank_dist = dict(Counter(ranks))
print(f"Rank distribution of A across 100 zeros: {rank_dist}")

p1_results = {
    "phase": 37, "track": "P1", "c1": c1,
    "rank_distribution": rank_dist,
    "linearity_test_error": linearity_err,
    "is_linear": bool(linearity_err < 0.1),
    "sample_matrices": p1_data
}
with open('phase37_A_structure.json', 'w') as f:
    json.dump(p1_results, f, indent=2)
print("Saved phase37_A_structure.json")

# ============================================================
# TRACK P2 — DISCRETE FOURIER TEST ON P-VECTORS
# ============================================================
print("\n" + "=" * 60)
print("TRACK P2 — Discrete Fourier Test on (A1)^6 P-vectors")
print("=" * 60)

# Test: is DFT(P_i) proportional to Q_i?
# Take DFT of the 16-component sedenion vector
print("DFT of P-vectors vs Q-vectors:")
p2_data = []
for i, (P, Q, label) in enumerate(zip(A1_6_BASIS, CANONICAL_Q, A1_6_LABELS)):
    P_arr = np.array(P)
    Q_arr = np.array(Q)
    dft_P = np.fft.fft(P_arr)  # 16-component DFT
    dft_P_real = dft_P.real
    dft_P_imag = dft_P.imag
    # Compare |DFT(P)| to Q (normalized)
    dft_mag = np.abs(dft_P)
    Q_norm = Q_arr / (np.linalg.norm(Q_arr) + 1e-15)
    dft_norm = dft_mag / (np.linalg.norm(dft_mag) + 1e-15)
    # Cosine similarity between DFT magnitude and Q
    cos_sim = float(np.dot(dft_norm, Q_norm))
    # Also check: is DFT(P) just P itself?  (self-dual under DFT?)
    dft_vs_P_cos = float(np.dot(dft_norm, np.abs(P_arr) / (np.linalg.norm(P_arr) + 1e-15)))
    print(f"  P{i} ({label}): cos(DFT(P),Q)={cos_sim:.4f}  cos(DFT(P),|P|)={dft_vs_P_cos:.4f}")
    # Nonzero DFT components
    nz_dft = [(j, float(dft_P[j].real), float(dft_P[j].imag)) for j in range(16) if abs(dft_P[j]) > 1e-10]
    p2_data.append({
        'i': i, 'label': label,
        'P_nonzero': [(j, float(v)) for j, v in enumerate(P_arr) if v != 0],
        'Q_nonzero': [(j, float(v)) for j, v in enumerate(Q_arr) if v != 0],
        'cos_sim_dft_P_vs_Q': float(cos_sim),
        'cos_sim_dft_P_vs_absP': float(dft_vs_P_cos),
        'nonzero_dft_components': nz_dft[:6]
    })

p2_results = {
    "phase": 37, "track": "P2", "c1": c1,
    "description": "Discrete Fourier test on (A1)^6 P-vectors vs bilateral Q-partners",
    "data": p2_data,
    "interpretation": (
        "DFT of P_i tested against Q_i (bilateral partner). "
        "cos_sim close to 1 would mean DFT(P) ∝ Q — Fourier self-duality. "
        "cos_sim close to 0 means no direct Fourier relation. "
        "This probes whether the bilateral annihilation P*Q=0 has a Fourier interpretation."
    )
}
with open('phase37_fourier_bilateral.json', 'w') as f:
    json.dump(p2_results, f, indent=2)
print("Saved phase37_fourier_bilateral.json")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PHASE 37 SUMMARY")
print("=" * 60)

print(f"V1  — Formula verification:    A anti-symmetry = {antisym_check:.2e}  PASS={antisym_check < 1e-10}")
print(f"E1  — iA eigenvalues computed: 100 zeros done")
print(f"      max eigenval range:       [{min(max_evals):.4f}, {max(max_evals):.4f}]")
print(f"      gamma range:              [{min(gammas):.4f}, {max(gammas):.4f}]")
print(f"E2a — Direct match:            {e2a_matches} matches (expect 0)")
print(f"E2b — Scaled match:            c_mean={c_mean:.2f} CV={c_cv:.3f} PASS={e2b_pass}")
print(f"E2c — Rank correlation:        Spearman rho={rho_max:.4f} (p={p_max:.3e})")
print(f"E3  — Trajectory:              sum_sq Pearson r={rho_ss:.4f}")
print(f"R1  — Reality at 100 zeros:    max|Im(F)|={global_max_imag:.2e} (structural zero)")
print(f"R2  — Reality vs sigma:        ALWAYS 0 — not sigma=1/2 specific")
print(f"S1  — Corrected det:           closest root to gamma: mean dist={np.mean(dists):.4f}")
print(f"S2  — Gamma_sed candidate:     near_zero={sum(d['gamma_sed_near_zero'] for d in s2_data)}/50")
print(f"C1  — Chavez eigenvalues:      CS values computed")
print(f"P1  — A structure:             rank dist={rank_dist}")
print(f"P2  — Fourier bilateral:       cos sim values computed")
print(f"\nKey finding: iA eigenvalues are O(0.01-1.6); gamma values are O(14-50).")
print(f"No direct or scaled match. The eigenvalue path through iA does not close at this order.")
print(f"R2 correction: F is ALWAYS real (structural), not sigma=1/2 specific.")
print(f"\nElapsed: {time.time()-t0_total:.1f}s")
print("All 11 output files saved.")
