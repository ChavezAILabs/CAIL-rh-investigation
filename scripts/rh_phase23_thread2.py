"""
Phase 23 Thread 2: lambda_min(G5) Trajectory to N=500 + GUE Norm Comparison
Chavez AI Labs LLC — March 2026

Script:  rh_phase23_thread2.py
Output:  phase23_thread2_results.json + RH_Phase23_Thread2_Results.md

Questions:
  1. Does lambda_min(G5) continue growing monotonically to N=500?
  2. Which growth model best fits: linear, sqrt(N), or log(N)?
  3. Do zeros track / exceed / fall below random controls?
  4. Does a GUE-distributed spacing sequence score ~73% (zeros) or ~93% (random uniform)
     on diagonal norm Chavez? Determines whether the Phase 22 inversion is a GUE signature.

Phase 22 baseline (N=100):
  lambda_min(G5) = 10.459, cond = 4.40 (random mean: 10.778, cond 5.20)
  Diagonal norm Chavez: zeros 73.8%, random 92.9%
"""

import json
import numpy as np
from scipy import stats as scipy_stats

rng = np.random.default_rng(seed=42)
sqrt2 = np.sqrt(2.0)

# ══════════════════════════════════════════════════════════════════════════════
# EMBEDDING (Phase 20B exact)
# ══════════════════════════════════════════════════════════════════════════════

ROOT_DIRS = {
    2:  np.array([0, 0, 0, 0, 1, 1]) / sqrt2,
    3:  np.array([0, 0,-1, 1, 0, 0]) / sqrt2,
    5:  np.array([0, 0, 1, 1, 0, 0]) / sqrt2,
    7:  np.array([1,-1, 0, 0, 0, 0]) / sqrt2,
    11: np.array([1, 1, 0, 0, 0, 0]) / sqrt2,
    13: np.array([-1,1, 0, 0, 0, 0]) / sqrt2,
}
LOG_SQRT = {p: np.log(p) / np.sqrt(p) for p in ROOT_DIRS}
BLOCK_IDX = {'A': slice(0, 2), 'B': slice(2, 4), 'C': slice(4, 6)}

def f5D(t):
    out = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        out += LOG_SQRT[p] * np.cos(t * np.log(p)) * r
    return out

def build_F(t_vals):
    F = np.zeros((len(t_vals), 6))
    for i, t in enumerate(t_vals):
        F[i] = f5D(t)
    return F

# G5 via P5 projection: 6D -> 5D (combines e4/e5 into (e4+e5)/sqrt2)
P5 = np.zeros((5, 6))
P5[0,0] = 1.0; P5[1,1] = 1.0; P5[2,2] = 1.0; P5[3,3] = 1.0
P5[4,4] = 1.0 / sqrt2; P5[4,5] = 1.0 / sqrt2

def gram_G5(F):
    F5 = F @ P5.T
    return F5.T @ F5

# ── JSON helper ────────────────────────────────────────────────────────────────

def safe(x):
    if isinstance(x, (np.bool_,)):        return bool(x)
    if isinstance(x, (np.integer,)):      return int(x)
    if isinstance(x, (np.floating, float)):
        if np.isnan(x) or np.isinf(x):   return None
        return float(x)
    return x

# ── Local Chavez (for sequences of any length here — scientific answer needed) ─

def conjugation_symmetry(seq):
    x = np.asarray(seq, dtype=float)
    if len(x) < 2: return 1.0
    xmin, xmax = x.min(), x.max()
    if xmax - xmin < 1e-15: return 1.0
    x = (x - xmin) / (xmax - xmin)
    n = len(x)
    return float(1.0 - np.mean([abs(x[i] - x[n-1-i]) for i in range(n // 2)]))

# ── GUE Wigner surmise (beta=2) sampler ──────────────────────────────────────

def sample_gue_spacings(n, rng_):
    """Sample n normalized spacings from GUE Wigner surmise (beta=2).
    P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi). Mode at s = sqrt(pi)/2 ~ 0.886.
    """
    s_mode = np.sqrt(np.pi) / 2.0
    p_max  = (32.0 / np.pi**2) * s_mode**2 * np.exp(-4.0 * s_mode**2 / np.pi)
    samples = []
    while len(samples) < n:
        batch_s = rng_.uniform(0.0, 5.0, 20000)
        batch_u = rng_.uniform(0.0, p_max, 20000)
        batch_p = (32.0 / np.pi**2) * batch_s**2 * np.exp(-4.0 * batch_s**2 / np.pi)
        accepted = batch_s[batch_u < batch_p].tolist()
        samples.extend(accepted)
    return np.array(samples[:n])

def gue_t_values(n, t_start, t_end, rng_):
    """Generate n t-values with GUE spacing distribution over [t_start, t_end]."""
    spacings = sample_gue_spacings(n - 1, rng_)
    total    = t_end - t_start
    scaled   = spacings / spacings.sum() * total
    t        = np.empty(n)
    t[0]     = t_start
    t[1:]    = t_start + np.cumsum(scaled)
    return t

# ══════════════════════════════════════════════════════════════════════════════
# LOAD ZEROS (from cached rh_zeros.json — 1000 zeros at mpmath dps=25)
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("PHASE 23 THREAD 2: lambda_min(G5) Trajectory + GUE Norm Comparison")
print("=" * 65)
print()

with open('rh_zeros.json') as f:
    all_zeros = json.load(f)

N_MAX = 500
zeros_t = np.array(all_zeros[:N_MAX])
t_min, t_max = zeros_t[0], zeros_t[N_MAX - 1]
print(f"Loaded {N_MAX} zeros from rh_zeros.json")
print(f"  t_1   = {t_min:.6f}")
print(f"  t_500 = {t_max:.6f}")
print()

N_SEEDS   = 10
rand_t_sets = [rng.uniform(t_min, t_max, N_MAX) for _ in range(N_SEEDS)]

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: Extended lambda_min(G5) Trajectory
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("COMPUTATION 1: Extended lambda_min(G5) Trajectory")
print("=" * 65)
print()
print(f"{'N':>6}  {'zeros lmin(G5)':>16}  {'zeros cond':>12}  "
      f"{'rand lmin(mean)':>17}  {'rand cond(mean)':>16}")
print("-" * 77)

N_values   = [100, 150, 200, 250, 300, 400, 500]
traj       = []

for N in N_values:
    F_n  = build_F(zeros_t[:N])
    G5_n = gram_G5(F_n)
    ev_n = np.sort(np.linalg.eigvalsh(G5_n))
    lmin = float(ev_n[0]); lmax = float(ev_n[-1])
    cond = lmax / lmin if lmin > 1e-15 else float('inf')

    rand_lmins = []; rand_conds = []
    for t_rand in rand_t_sets:
        F_r  = build_F(t_rand[:N])
        G5_r = gram_G5(F_r)
        ev_r = np.sort(np.linalg.eigvalsh(G5_r))
        lm_r = float(ev_r[0]); lx_r = float(ev_r[-1])
        rand_lmins.append(lm_r)
        rand_conds.append(lx_r / lm_r if lm_r > 1e-15 else float('inf'))

    rml  = float(np.mean(rand_lmins))
    rmc  = float(np.mean([c for c in rand_conds if c != float('inf')]))

    traj.append({
        'N': N,
        'zeros': {
            'lambda_min': safe(lmin), 'lambda_max': safe(lmax),
            'condition_number': safe(cond),
            'all_eigenvalues': [safe(e) for e in ev_n.tolist()],
        },
        'random': {
            'lambda_min_mean': safe(rml),
            'lambda_min_std':  safe(float(np.std(rand_lmins))),
            'condition_number_mean': safe(rmc),
            'lambda_min_all': [safe(v) for v in rand_lmins],
        },
    })

    cs = f'{cond:.2f}' if cond != float('inf') else 'inf'
    rs = f'{rmc:.2f}' if rmc != float('inf') else 'inf'
    print(f"{N:>6}  {lmin:>16.4f}  {cs:>12}  {rml:>17.4f}  {rs:>16}")

print()

lmins_z = [r['zeros']['lambda_min']        for r in traj]
lmins_r = [r['random']['lambda_min_mean']  for r in traj]
Ns_arr  = np.array(N_values, dtype=float)

print(f"Zeros trend:  {' -> '.join(f'{x:.3f}' for x in lmins_z)}")
print(f"Random trend: {' -> '.join(f'{x:.3f}' for x in lmins_r)}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: Growth Rate Fitting
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("COMPUTATION 2: Growth Rate Fitting")
print("=" * 65)
print()
print("Fitting lambda_min(N) to three models.")
print("Marchenko-Pastur prediction for random: lambda_min ~ sqrt(N).")
print()

lmins_arr = np.array(lmins_z)

models = {
    'linear':  (Ns_arr,          'a * N'),
    'sqrt_N':  (np.sqrt(Ns_arr), 'a * sqrt(N)'),
    'log_N':   (np.log(Ns_arr),  'a * log(N) + b'),
}

fit_results = {}
for name, (x, formula) in models.items():
    slope, intercept, r, p_val, se = scipy_stats.linregress(x, lmins_arr)
    r2 = r ** 2
    fit_results[name] = {
        'formula': formula, 'slope': safe(slope),
        'intercept': safe(intercept), 'r_squared': safe(r2),
    }
    print(f"  {formula:20s}  slope={slope:8.4f}  intercept={intercept:8.4f}  R²={r2:.6f}")

best_model = max(fit_results, key=lambda k: fit_results[k]['r_squared'])
print()
print(f"Best fit: {best_model}  (R²={fit_results[best_model]['r_squared']:.6f})")

# Also fit random for comparison
lmins_r_arr = np.array(lmins_r)
rand_fits = {}
for name, (x, formula) in models.items():
    slope_r, intercept_r, r_r, _, _ = scipy_stats.linregress(x, lmins_r_arr)
    rand_fits[name] = {'slope': safe(slope_r), 'intercept': safe(intercept_r),
                       'r_squared': safe(r_r**2)}

best_rand = max(rand_fits, key=lambda k: rand_fits[k]['r_squared'])
print(f"Random best fit: {best_rand}  (R²={rand_fits[best_rand]['r_squared']:.6f})")
print()

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: Block Trajectories
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("COMPUTATION 3: Block Trajectories")
print("=" * 65)
print()
print("Tracking smaller eigenvalue of G_A (2x2, Block A) and G_B (2x2, Block B).")
print()
print(f"{'N':>6}  {'G_A lmin(zeros)':>17}  {'G_A lmin(rand)':>16}  "
      f"{'G_B lmin(zeros)':>17}  {'G_B lmin(rand)':>16}")
print("-" * 80)

block_traj = []

for N in N_values:
    row = {'N': N, 'A': {}, 'B': {}}
    for blk in ('A', 'B'):
        sl   = BLOCK_IDX[blk]
        F_n  = build_F(zeros_t[:N])[:, sl]
        G_n  = F_n.T @ F_n  # 2×2
        ev_n = np.sort(np.linalg.eigvalsh(G_n))
        lmin_z = float(ev_n[0])

        rand_lmins_b = []
        for t_rand in rand_t_sets:
            F_r  = build_F(t_rand[:N])[:, sl]
            G_r  = F_r.T @ F_r
            ev_r = np.sort(np.linalg.eigvalsh(G_r))
            rand_lmins_b.append(float(ev_r[0]))

        row[blk] = {
            'lambda_min_zeros': safe(lmin_z),
            'lambda_min_rand_mean': safe(float(np.mean(rand_lmins_b))),
            'lambda_min_rand_std':  safe(float(np.std(rand_lmins_b))),
        }

    block_traj.append(row)
    print(f"{N:>6}  {row['A']['lambda_min_zeros']:>17.4f}  "
          f"{row['A']['lambda_min_rand_mean']:>16.4f}  "
          f"{row['B']['lambda_min_zeros']:>17.4f}  "
          f"{row['B']['lambda_min_rand_mean']:>16.4f}")

print()

# Growth rate for each block
for blk in ('A', 'B'):
    lmins_blk = np.array([r[blk]['lambda_min_zeros'] for r in block_traj])
    _, _, r_lin, _, _ = scipy_stats.linregress(Ns_arr, lmins_blk)
    _, _, r_sq,  _, _ = scipy_stats.linregress(np.sqrt(Ns_arr), lmins_blk)
    _, _, r_log, _, _ = scipy_stats.linregress(np.log(Ns_arr),  lmins_blk)
    best_blk = max([('linear', r_lin**2), ('sqrt', r_sq**2), ('log', r_log**2)],
                   key=lambda x: x[1])
    print(f"Block {blk} best fit: {best_blk[0]}  R²={best_blk[1]:.4f}")

print()

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: GUE Norm Comparison
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("COMPUTATION 4: GUE Norm Comparison")
print("=" * 65)
print()
print("The Phase 22 open question: does GUE-distributed spacing produce the same")
print("diagonal norm Chavez score as Riemann zeros (73.8%) or as uniform random (92.9%)?")
print()
print("GUE Wigner surmise (beta=2): P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)")
print()

N_GUE    = 100
N_GUE_SEEDS = 10
t_start  = zeros_t[0]
t_end    = zeros_t[N_GUE - 1]  # match Phase 22 range exactly

# Phase 22 reference values
zeros_diag_sym_phase22  = 0.738  # from Phase 22 CAILculator
random_diag_sym_phase22 = 0.929  # from Phase 22 CAILculator

# Compute zeros diagonal norms (N=100) locally for direct comparison
F_zeros_100 = build_F(zeros_t[:N_GUE])
diag_zeros  = np.array([F_zeros_100[i] @ F_zeros_100[i] for i in range(N_GUE)])
sym_zeros   = conjugation_symmetry(np.sort(diag_zeros))

# GUE controls
gue_diag_syms = []
gue_sequences = []

for seed in range(N_GUE_SEEDS):
    t_gue   = gue_t_values(N_GUE, t_start, t_end, rng)
    F_gue   = build_F(t_gue)
    d_gue   = np.array([F_gue[i] @ F_gue[i] for i in range(N_GUE)])
    sym_gue = conjugation_symmetry(np.sort(d_gue))
    gue_diag_syms.append(safe(sym_gue))
    gue_sequences.append([safe(v) for v in np.sort(d_gue).tolist()])

gue_mean = float(np.mean(gue_diag_syms))
gue_std  = float(np.std(gue_diag_syms))

# Uniform random controls (replicate Phase 22 for direct comparison)
rand_diag_syms = []
for t_rand in rand_t_sets[:N_GUE_SEEDS]:
    F_rand = build_F(t_rand[:N_GUE])
    d_rand = np.array([F_rand[i] @ F_rand[i] for i in range(N_GUE)])
    rand_diag_syms.append(conjugation_symmetry(np.sort(d_rand)))
rand_mean = float(np.mean(rand_diag_syms))

print(f"Diagonal norm Chavez (sorted ||f5D(tn)||^2, n=100):")
print(f"  Riemann zeros:      {sym_zeros:.4f}   [Phase 22 CAILculator: {zeros_diag_sym_phase22:.3f}]")
print(f"  GUE-distributed:    {gue_mean:.4f} ± {gue_std:.4f}   (10 seeds)")
print(f"  Uniform random:     {rand_mean:.4f}   [Phase 22 CAILculator: {random_diag_sym_phase22:.3f}]")
print()

gue_verdict = (
    "GUE SIGNATURE CONFIRMED — GUE control scores like zeros, not like uniform random"
    if abs(gue_mean - sym_zeros) < abs(gue_mean - rand_mean)
    else "GUE control scores closer to random — inversion is NOT a pure GUE signature"
)
print(f"Verdict: {gue_verdict}")
print()

# Also compute at N=500 for extended comparison
F_zeros_500 = build_F(zeros_t[:N_MAX])
diag_z500   = np.array([F_zeros_500[i] @ F_zeros_500[i] for i in range(N_MAX)])
sym_z500    = conjugation_symmetry(np.sort(diag_z500))

gue_diag_syms_500 = []
t_end_500 = zeros_t[N_MAX - 1]
for _ in range(N_GUE_SEEDS):
    t_gue500 = gue_t_values(N_MAX, t_start, t_end_500, rng)
    F_g500   = build_F(t_gue500)
    d_g500   = np.array([F_g500[i] @ F_g500[i] for i in range(N_MAX)])
    gue_diag_syms_500.append(conjugation_symmetry(np.sort(d_g500)))
gue_mean_500 = float(np.mean(gue_diag_syms_500))
gue_std_500  = float(np.std(gue_diag_syms_500))

rand_diag_syms_500 = []
for t_rand in rand_t_sets:
    F_r500 = build_F(t_rand[:N_MAX])
    d_r500 = np.array([F_r500[i] @ F_r500[i] for i in range(N_MAX)])
    rand_diag_syms_500.append(conjugation_symmetry(np.sort(d_r500)))
rand_mean_500 = float(np.mean(rand_diag_syms_500))

print(f"Extended at N=500:")
print(f"  Zeros:           {sym_z500:.4f}")
print(f"  GUE-distributed: {gue_mean_500:.4f} ± {gue_std_500:.4f}")
print(f"  Uniform random:  {rand_mean_500:.4f}")
print()

# ══════════════════════════════════════════════════════════════════════════════
# OVERALL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 65)
print("OVERALL SUMMARY")
print("=" * 65)
print()

final_lmin_z = lmins_z[-1]   # at N=500
final_lmin_r = lmins_r[-1]
ratio_500    = safe(final_lmin_z / final_lmin_r) if final_lmin_r else None

print(f"lambda_min(G5) at N=500:")
print(f"  Zeros:  {final_lmin_z:.4f}")
print(f"  Random: {final_lmin_r:.4f}  ratio={f'{ratio_500:.4f}' if ratio_500 else 'N/A'}")
print()
print(f"Growth model (zeros): {best_model}  R²={fit_results[best_model]['r_squared']:.4f}")
print(f"Growth model (random): {best_rand}  R²={rand_fits[best_rand]['r_squared']:.4f}")
print()
print(f"GUE norm comparison (n=100):")
print(f"  Zeros={sym_zeros:.4f}  GUE={gue_mean:.4f}  Random={rand_mean:.4f}")
print(f"  GUE closer to: {'zeros' if abs(gue_mean-sym_zeros)<abs(gue_mean-rand_mean) else 'random'}")
print()
print(f"GUE norm comparison (n=500):")
print(f"  Zeros={sym_z500:.4f}  GUE={gue_mean_500:.4f}  Random={rand_mean_500:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# SAVE JSON
# ══════════════════════════════════════════════════════════════════════════════

results = {
    'experiment': 'Phase23_Thread2_Trajectory_GUE',
    'date': '2026-03-24',
    'n_zeros_loaded': N_MAX,
    'zeros_t_range': [safe(t_min), safe(t_max)],
    'n_random_seeds': N_SEEDS,
    'phase22_baseline': {
        'lambda_min_N100': 10.459,
        'condition_number_N100': 4.40,
        'diagonal_norm_chavez_zeros': 0.738,
        'diagonal_norm_chavez_random': 0.929,
    },
    'computation_1_trajectory': {
        'N_values': N_values,
        'trajectory': traj,
        'zeros_lambda_min_trend': [safe(x) for x in lmins_z],
        'random_lambda_min_trend': [safe(x) for x in lmins_r],
        'ratio_zeros_over_random_at_N500': safe(ratio_500),
    },
    'computation_2_growth_fitting': {
        'zeros': fit_results,
        'zeros_best_model': best_model,
        'random': rand_fits,
        'random_best_model': best_rand,
    },
    'computation_3_block_trajectories': {
        'N_values': N_values,
        'trajectory': block_traj,
    },
    'computation_4_gue_norm_comparison': {
        'n_zeros_compared': N_GUE,
        't_range': [safe(t_start), safe(t_end)],
        'n_gue_seeds': N_GUE_SEEDS,
        'zeros_diagonal_norm_chavez': safe(sym_zeros),
        'gue_diagonal_norm_chavez_mean': safe(gue_mean),
        'gue_diagonal_norm_chavez_std':  safe(gue_std),
        'gue_diagonal_norm_chavez_all':  gue_diag_syms,
        'uniform_random_diagonal_norm_chavez_mean': safe(rand_mean),
        'gue_verdict': gue_verdict,
        'n500': {
            'zeros': safe(sym_z500),
            'gue_mean': safe(gue_mean_500),
            'gue_std':  safe(gue_std_500),
            'random_mean': safe(rand_mean_500),
        },
    },
    'headline_results': {
        'lambda_min_N500_zeros':  safe(final_lmin_z),
        'lambda_min_N500_random': safe(final_lmin_r),
        'ratio_N500': safe(ratio_500),
        'best_growth_model': best_model,
        'best_growth_r2': safe(fit_results[best_model]['r_squared']),
        'gue_norm_chavez_mean': safe(gue_mean),
        'zeros_norm_chavez': safe(sym_zeros),
        'random_norm_chavez': safe(rand_mean),
        'gue_verdict': gue_verdict,
    },
    'cailculator_sequences': {
        'zeros_diag_norms_sorted_100': [safe(v) for v in np.sort(diag_zeros).tolist()],
        'zeros_diag_norms_sorted_500': [safe(v) for v in np.sort(diag_z500).tolist()],
        'gue_diag_norms_sorted_100_all_seeds': gue_sequences,
        'gue_diag_norms_sorted_100_seed0': gue_sequences[0] if gue_sequences else [],
        'random_diag_norms_sorted_100_seed0': [
            safe(v) for v in sorted(
                [F_zeros_100[i] @ F_zeros_100[i] for i in range(N_GUE)]
            )
        ],
    },
}

with open('phase23_thread2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to phase23_thread2_results.json")
print("Next: Write RH_Phase23_Thread2_Results.md")
