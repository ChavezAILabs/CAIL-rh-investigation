"""
Phase 30 — Claude Code computation script
GUE Overlap Integral (Thread 1) + Weil Ratio Convergence (Thread 2)
Produces phase30_results.json for Claude Desktop/CAILculator analysis.

Claude Code's job: pure math, pure Python, no MCP.
Claude Desktop's job: CAILculator on the output sequences.

Run from: C:\dev\projects\Experiments_January_2026\Primes_2026
"""
import numpy as np
from scipy.stats import linregress
import json, time, os

# ============================================================
# PRIMES & SCALAR FUNCTIONS
# ============================================================
def sieve_primes(limit):
    """Sieve of Eratosthenes"""
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit + 1, i):
                is_p[j] = False
    return [i for i in range(2, limit + 1) if is_p[i]]

def f5D_scalar(t, primes):
    """Prime weight function: f5D(t) = sum_p (log p / sqrt(p)) * cos(t * log p)"""
    return float(sum(np.log(p) / np.sqrt(p) * np.cos(t * np.log(p)) for p in primes))

def Tr_BK(t, primes):
    """Trace of Berry-Keating Hamiltonian — identical to f5D_scalar"""
    return float(sum((np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) for p in primes))

def Weil_RHS(primes):
    """Weil explicit formula RHS: -sum_p log(p)/sqrt(p)"""
    return -float(sum(np.log(p) / np.sqrt(p) for p in primes))

def R2(r):
    """Montgomery-Dyson GUE two-point pair correlation"""
    if abs(r) < 1e-10:
        return 0.0
    return 1.0 - (np.sin(np.pi * r) / (np.pi * r))**2

def R2_vec(r_mat):
    """Vectorized R2 for numpy arrays"""
    with np.errstate(invalid='ignore', divide='ignore'):
        sinc = np.where(np.abs(r_mat) < 1e-10,
                        0.0,
                        (np.sin(np.pi * r_mat) / (np.pi * r_mat))**2)
    return 1.0 - sinc

# Machine-exact target constants from Phase 24
TARGET_c1 = 0.11797805192095003   # sin(Weil angle)
TARGET_c3 = 0.9930162029216528    # cos(Weil angle)

# Prime sets
PRIMES_6  = sieve_primes(13)   # [2,3,5,7,11,13]
PRIMES_9  = sieve_primes(23)   # 9 primes
PRIMES_16 = sieve_primes(53)   # 16 primes
PRIMES_25 = sieve_primes(97)   # 25 primes

print("=" * 62)
print("PHASE 30 - GUE Overlap Integral + Weil Ratio Convergence")
print("=" * 62)
print(f"  Primes 6:  {PRIMES_6}")
print(f"  Primes 9:  {PRIMES_9}")
print(f"  Primes 16: {PRIMES_16}")
print(f"  Primes 25: {PRIMES_25[:5]} ... {PRIMES_25[-3:]}")

# ============================================================
# DATA LOAD
# ============================================================
CACHE = 'rh_zeros.json'
if os.path.exists(CACHE):
    with open(CACHE) as fh:
        zeros_all = json.load(fh)
    zeros = zeros_all[:500]
    print(f"\nLoaded {len(zeros)} zeros from cache: t_1={zeros[0]:.4f} .. t_500={zeros[499]:.4f}")
else:
    from mpmath import mp, zetazero
    mp.dps = 25
    print("\nFetching 500 zeros from mpmath (this takes ~10 min)...")
    t0 = time.time()
    zeros = [float(zetazero(n).imag) for n in range(1, 501)]
    print(f"Done in {time.time()-t0:.1f}s")

# ============================================================
# THREAD 1: GUE Overlap Integral
# ============================================================
print("\n" + "=" * 62)
print("THREAD 1: GUE Overlap Integral — testing c1 derivation")
print("=" * 62)
print(f"  Target c1 = {TARGET_c1:.16f}")
print()

# --- 1A: Grid-based double integral ---
print("  [1A] Grid-based continuous double integral")
print(f"  {'T':>6}  {'N':>5}  {'c1_hat':>14}  {'ratio/c1':>10}  {'time(s)':>7}")

def gue_overlap_grid(T, N, primes):
    """
    Numerically evaluate:
      c1_hat = [∫∫ f5D(t)·f5D(t')·R2_norm(t,t') dt dt']
               / [∫∫ f5D(t)·f5D(t') dt dt']

    where R2_norm uses local zero density for normalization:
      density(t) = log(t / 2π) / (2π)
      r_norm(t, t') = |t - t'| * density(mean(t, t'))

    Grid: midpoint rule on [0, T] × [0, T].
    """
    dt = T / N
    # Midpoint grid avoids t=0 (where log is undefined for density)
    t_grid = np.linspace(dt / 2, T - dt / 2, N)

    # f5D on grid
    f = np.array([f5D_scalar(t, primes) for t in t_grid])

    # Outer product of f values
    f_outer = np.outer(f, f)  # N × N

    # Pairwise differences and local density normalization
    diff_mat = t_grid[:, None] - t_grid[None, :]   # N × N
    t_mean_mat = 0.5 * (t_grid[:, None] + t_grid[None, :])
    # Clip to avoid log(negative) for small t values
    t_mean_mat = np.clip(t_mean_mat, 2 * np.pi + 0.1, None)
    density_mat = np.log(t_mean_mat / (2 * np.pi)) / (2 * np.pi)
    r_mat = np.abs(diff_mat) * density_mat   # normalized separation

    # R2 matrix
    R_mat = R2_vec(r_mat)

    # Double integrals via midpoint quadrature
    numer = float(np.sum(f_outer * R_mat)) * dt**2
    denom = float(np.sum(f_outer)) * dt**2

    if abs(denom) < 1e-15:
        return None, numer, denom, None
    c1_hat = numer / denom
    return float(c1_hat), float(numer), float(denom), denom / dt**2  # last: sum(f_outer)

grid_results = {}
# (T, N) pairs — N chosen so dt < 0.2 (resolves p=13 oscillations, period ~2.4)
for T, N in [(50, 500), (100, 700), (200, 1200), (500, 2500)]:
    t0 = time.time()
    c1_hat, numer, denom, f_sq_sum = gue_overlap_grid(T, N, PRIMES_6)
    elapsed = time.time() - t0
    ratio = c1_hat / TARGET_c1 if c1_hat is not None else None
    print(f"  {T:>6}  {N:>5}  {c1_hat:>14.8f}  {ratio:>10.6f}  {elapsed:>7.2f}")
    grid_results[f"T{T}"] = {
        "T": T, "N": N,
        "c1_hat": c1_hat,
        "numer": numer,
        "denom": denom,
        "ratio_to_c1": ratio,
        "elapsed_s": float(elapsed),
    }

# --- 1B: Zero-based discrete version ---
print()
print("  [1B] Zero-based discrete double sum (zeros as integration measure)")
print(f"  {'N_zeros':>8}  {'c1_hat':>14}  {'ratio/c1':>10}  {'time(s)':>7}")

def gue_overlap_zeros(zeros_list, primes):
    """
    Discrete analog using actual Riemann zeros as integration nodes.

    The N zeros t_1 < ... < t_N are treated as sample points for the
    continuous measure. Each pair (i,j) contributes:
      f5D(t_i) · f5D(t_j) · w_i · w_j · R2(r_ij)

    where:
      w_i   = 1 / density(t_i)  (volume element; density = log(t/2π)/(2π))
      r_ij  = |t_i - t_j| * mean_density(i,j)   (normalized separation)

    The denominator uses R2=1 everywhere (unit correlation).

    Note: At integer normalized separations, R2 = 1 - (sin(kπ)/kπ)² = 1 exactly
    for k ∈ Z, k≠0 (since sin(kπ)=0). So the GUE suppression is ONLY at r≈0,
    i.e., only the diagonal (i=j, R2=0) vs off-diagonal (R2→1) distinction matters.
    """
    t = np.array(zeros_list, dtype=float)
    N = len(t)

    # Local density (zero of zeta at height t has density ≈ log(t/2π)/(2π))
    density = np.log(np.clip(t, 2*np.pi + 0.1, None) / (2 * np.pi)) / (2 * np.pi)
    w = 1.0 / density   # volume element weights

    # f5D values
    f = np.array([f5D_scalar(ti, primes) for ti in t])
    fw = f * w           # weight-absorbed f

    # Weighted outer product
    f_outer = np.outer(fw, fw)   # N × N

    # Normalized pairwise separations
    diff_mat = t[:, None] - t[None, :]
    density_mean = 0.5 * (density[:, None] + density[None, :])
    r_mat = np.abs(diff_mat) * density_mean

    # R2 matrix (diagonal = 0 by R2(0) = 0; integers = 1 exactly)
    R_mat = R2_vec(r_mat)

    numer = float(np.sum(f_outer * R_mat))
    denom = float(np.sum(f_outer))   # no R2 weighting

    if abs(denom) < 1e-15:
        return None, numer, denom
    c1_hat = numer / denom
    return float(c1_hat), float(numer), float(denom)

zero_results = {}
for N_zeros in [50, 100, 200, 500]:
    t0 = time.time()
    c1_hat, numer, denom = gue_overlap_zeros(zeros[:N_zeros], PRIMES_6)
    elapsed = time.time() - t0
    ratio = c1_hat / TARGET_c1 if c1_hat is not None else None
    print(f"  {N_zeros:>8}  {c1_hat:>14.8f}  {ratio:>10.6f}  {elapsed:>7.2f}")
    zero_results[f"N{N_zeros}"] = {
        "N_zeros": N_zeros,
        "c1_hat": c1_hat,
        "numer": numer,
        "denom": denom,
        "ratio_to_c1": ratio,
        "elapsed_s": float(elapsed),
    }

# --- 1C: Alternative — R2 self-overlap of f5D power spectrum ---
print()
print("  [1C] Alternative formulas tested against c1")

# Test 1: What is R2 evaluated AT c1?
r2_at_c1 = R2(TARGET_c1)
# Test 2: What r gives R2(r) = c1?  (solve numerically)
from scipy.optimize import brentq
try:
    r_solve = brentq(lambda r: R2(r) - TARGET_c1, 0.01, 0.9)
except ValueError:
    r_solve = None

# Test 3: Diagonal fraction for zero-based estimate
# c1_hat ≈ 1 - diag_sum/total_sum
# For zeros: diag contributes 0 to numer (R2(0)=0), positive to denom
# So c1_hat = off_diag_numer / total_denom
# off_diag_numer ≈ total_denom - diag_denom (since R2≈1 for off-diag integers)
f_vals = np.array([f5D_scalar(t, PRIMES_6) for t in zeros[:100]])
density_vals = np.log(np.array(zeros[:100]) / (2*np.pi)) / (2*np.pi)
w_vals = 1.0 / density_vals
fw_vals = f_vals * w_vals
diag_sum = float(np.sum(fw_vals**2))
total_sum = float(np.sum(np.outer(fw_vals, fw_vals)))
diag_fraction = diag_sum / total_sum
c1_pred_diagonal = 1.0 - diag_fraction

print(f"  R2(c1) = R2({TARGET_c1:.5f}) = {r2_at_c1:.8f}")
print(f"  r such that R2(r) = c1: r = {r_solve:.8f}" if r_solve else "  No r in (0,1) solves R2(r) = c1")
print(f"  Diagonal fraction of zero-based sum (N=100): {diag_fraction:.8f}")
print(f"  Predicted c1 from diagonal suppression: {c1_pred_diagonal:.8f}")
print(f"  Target c1 = {TARGET_c1:.8f}")
print(f"  Weil angle = {np.degrees(np.arcsin(TARGET_c1)):.4f} degrees")

alt_results = {
    "R2_at_c1": float(r2_at_c1),
    "r_solving_R2_eq_c1": float(r_solve) if r_solve else None,
    "diagonal_fraction_N100": float(diag_fraction),
    "c1_pred_diagonal_suppression": float(c1_pred_diagonal),
    "weil_angle_degrees": float(np.degrees(np.arcsin(TARGET_c1))),
    "c1_squared_plus_c3_squared": float(TARGET_c1**2 + TARGET_c3**2),
}

# Convergence summary for Thread 1
c1_grid_vals   = [v["c1_hat"] for v in grid_results.values() if v["c1_hat"] is not None]
c1_zero_vals   = [v["c1_hat"] for v in zero_results.values() if v["c1_hat"] is not None]
print()
print(f"  Grid c1_hat range:  [{min(c1_grid_vals):.6f}, {max(c1_grid_vals):.6f}]")
print(f"  Zero c1_hat range:  [{min(c1_zero_vals):.6f}, {max(c1_zero_vals):.6f}]")
print(f"  Target c1:           {TARGET_c1:.6f}")
converging_to_c1 = all(abs(v - TARGET_c1) < 0.01 for v in c1_zero_vals[-2:])
print(f"  Converging to c1?   {converging_to_c1}")

# ============================================================
# THREAD 2: Weil Ratio Convergence with Extended Prime Sets
# ============================================================
print()
print("=" * 62)
print("THREAD 2: Weil Ratio Convergence — large prime sets")
print("=" * 62)
print(f"  {'Label':>6}  {'N_p':>4}  {'p_max':>5}  {'Weil_RHS':>12}  {'mean_Tr':>10}  "
      f"{'ratio':>10}  {'d(1/4)':>10}")

PRIME_SETS_T2 = {
    "p13":  sieve_primes(13),
    "p23":  sieve_primes(23),
    "p29":  sieve_primes(29),
    "p37":  sieve_primes(37),
    "p53":  sieve_primes(53),
    "p71":  sieve_primes(71),
    "p97":  sieve_primes(97),
    "p127": sieve_primes(127),
    "p151": sieve_primes(151),
}

thread2 = {}
ratio_sequence = []
weil_rhs_sequence = []
n_primes_list = []
p_max_list = []

for label, pset in PRIME_SETS_T2.items():
    rhs = Weil_RHS(pset)
    tr_z = [Tr_BK(t, pset) for t in zeros[:100]]
    mean_z = float(np.mean(tr_z))
    ratio = mean_z / rhs if abs(rhs) > 1e-10 else 0.0
    diff_q = ratio - 0.25
    print(f"  {label:>6}  {len(pset):>4}  {max(pset):>5}  {rhs:12.4f}  {mean_z:10.4f}  "
          f"{ratio:10.6f}  {diff_q:+10.6f}")
    ratio_sequence.append(float(ratio))
    weil_rhs_sequence.append(float(rhs))
    n_primes_list.append(len(pset))
    p_max_list.append(max(pset))
    thread2[label] = {
        "primes": pset,
        "n_primes": len(pset),
        "p_max": int(max(pset)),
        "weil_rhs": float(rhs),
        "mean_tr_zeros_100": float(mean_z),
        "ratio": float(ratio),
        "diff_from_quarter": float(diff_q),
        "tr_zeros_100": tr_z,
    }

# Analytic candidates and limit fits
print()
print("  Analytic limit fits:")
log_p_max = [np.log(p) for p in p_max_list]
inv_log_p = [1.0 / np.log(p) for p in p_max_list]
inv_n     = [1.0 / n for n in n_primes_list]

sl_a, ic_a, r_a, _, _ = linregress(inv_log_p, ratio_sequence)
sl_b, ic_b, r_b, _, _ = linregress(inv_n,     ratio_sequence)
sl_c, ic_c, r_c, _, _ = linregress(log_p_max, ratio_sequence)

print(f"  ratio vs 1/log(p_max):  limit = {ic_a:.6f}  (R²={r_a**2:.4f})")
print(f"  ratio vs 1/n_primes:    limit = {ic_b:.6f}  (R²={r_b**2:.4f})")
print(f"  ratio vs log(p_max):    limit direction, slope = {sl_c:.6f}  (R²={r_c**2:.4f})")

# Named constant comparison
print()
print("  Named constant comparison:")
named = [
    ("1/4",          0.25),
    ("1/e",          1.0 / np.e),
    ("1/(2pi)",      1.0 / (2 * np.pi)),
    ("log2/pi",      np.log(2) / np.pi),
    ("1/pi",         1.0 / np.pi),
    ("gamma_Euler",  0.5772156649),
    ("sqrt2-1",      np.sqrt(2) - 1),
    ("(sqrt5-1)/2",  (np.sqrt(5) - 1) / 2),
]
for name, val in named:
    diffs = [r - val for r in ratio_sequence]
    trend = "decreasing toward" if diffs[-1] < diffs[0] else "away from"
    print(f"    {name:>12} = {val:.6f}:  current gap [{min(diffs):+.6f}, {max(diffs):+.6f}]  ({trend})")

# Is ratio monotone?
monotone_dec = all(ratio_sequence[i] >= ratio_sequence[i+1] for i in range(len(ratio_sequence)-1))
monotone_inc = all(ratio_sequence[i] <= ratio_sequence[i+1] for i in range(len(ratio_sequence)-1))
print()
print(f"  Ratio sequence: {[round(r, 6) for r in ratio_sequence]}")
print(f"  Monotone decreasing: {monotone_dec}")
print(f"  Monotone increasing: {monotone_inc}")
print(f"  Best limit estimate (1/log fit): {ic_a:.8f}")
print(f"  Best limit estimate (1/n fit):   {ic_b:.8f}")

analytic_fits = {
    "vs_inv_log_pmax": {
        "slope": float(sl_a), "intercept": float(ic_a), "R2": float(r_a**2),
        "limit_estimate": float(ic_a),
    },
    "vs_inv_n_primes": {
        "slope": float(sl_b), "intercept": float(ic_b), "R2": float(r_b**2),
        "limit_estimate": float(ic_b),
    },
    "vs_log_pmax": {
        "slope": float(sl_c), "intercept": float(ic_c), "R2": float(r_c**2),
    },
}

# ============================================================
# SAVE OUTPUT
# ============================================================
results = {
    "metadata": {
        "phase": 30,
        "date": "2026-03-26",
        "script": "rh_phase30.py",
        "target_c1": TARGET_c1,
        "target_c3": TARGET_c3,
        "weil_angle_degrees": float(np.degrees(np.arcsin(TARGET_c1))),
        "zeros_used": len(zeros),
    },
    "thread1_gue_overlap": {
        "description": "Tests whether c1 arises as GUE two-point overlap integral of f5D",
        "formula": "c1_hat = int int f5D(t)*f5D(t')*R2_norm(t,t') dt dt' / int int f5D(t)*f5D(t') dt dt'",
        "grid_based_1A": grid_results,
        "zero_based_1B": zero_results,
        "alternative_1C": alt_results,
        "convergence_target": TARGET_c1,
        "converging_to_c1": bool(converging_to_c1),
        "grid_c1_range": [float(min(c1_grid_vals)), float(max(c1_grid_vals))],
        "zero_c1_range": [float(min(c1_zero_vals)), float(max(c1_zero_vals))],
    },
    "thread2_weil_ratio": {
        "description": "Weil ratio mean_Tr_BK / Weil_RHS vs prime set size — does it converge to 1/4?",
        "prime_sets": thread2,
        "ratio_sequence": ratio_sequence,
        "weil_rhs_sequence": weil_rhs_sequence,
        "n_primes_list": n_primes_list,
        "p_max_list": p_max_list,
        "analytic_fits": analytic_fits,
        "monotone_decreasing": bool(monotone_dec),
        "monotone_increasing": bool(monotone_inc),
    },
}

outfile = "phase30_results.json"
with open(outfile, "w") as fh:
    json.dump(results, fh, indent=2)

print()
print("=" * 62)
print(f"Saved: {outfile}")
print("=" * 62)
print()
print("HANDOFF TO CLAUDE DESKTOP:")
print("  Load phase30_results.json")
print("  Run CAILculator on:")
print("  - thread1_gue_overlap.zero_based_1B.*.c1_hat  (sequence, analyze_dataset)")
print("  - thread1_gue_overlap.grid_based_1A.*.c1_hat  (sequence, analyze_dataset)")
print("  - thread2_weil_ratio.ratio_sequence            (analyze_dataset)")
print("  - thread2_weil_ratio.weil_rhs_sequence         (analyze_dataset)")
print("  - thread2_weil_ratio.prime_sets.*.tr_zeros_100 (chavez_transform per set)")
