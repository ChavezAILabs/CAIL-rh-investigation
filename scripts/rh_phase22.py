"""
Phase 22: Weil-Gram Bridge — Chavez Transform on Zero Image Gram Matrix
Chavez AI Labs LLC — March 2026

Script: rh_phase22.py
Output: phase22_results.json  (+ RH_Phase22_Results.md written separately)

Central Hypothesis:
  The 5×5 Gram matrix G5 of zero images is positive definite and bounded away
  from singularity as N grows. Its eigenvalue sequence has GUE-level conjugation
  symmetry under the Chavez Transform. This connects strong injectivity to the
  same statistical structure (Montgomery-Dyson) that governs the zeros themselves.

Embedding (Phase 20B — exact):
  f5D(t) = sum_p (log p / sqrt(p)) * cos(t * log p) * r_p
  Prime -> direction: p=2:q4, p=3:q2, p=5:v5, p=7:v1, p=11:v4, p=13:q3
  6D basis: [e2, e7, e3, e6, e4, e5]

Rank structure:
  - v1 = -q3 (antipodal): the 6 roots span only 5D, not 6D.
  - Block C = {e4,e5}: q4=(e4+e5)/sqrt2 is a single 1D direction (rank 1).
  - G6 = F.T@F (6x6) has one structural zero eigenvalue.
  - G5 = F5.T@F5 (5x5) with P5 projection is the correct PD object.
  - P5 basis: [e2, e7, e3, e6, (e4+e5)/sqrt2]

CAILculator MCP routing (sequences length >= 50):
  Sequences prepared for MCP handoff (NOT computed locally):
    - 100 diagonal values ||f5D(tn)||^2  (Computation 3a)
    - 100 sorted row norms of F5         (Computation 3b)
    - Row-wise sorted mean profile       (Computation 5)
    - ZDTP on 4950 off-diagonal inner products (Computation 5)
    - Per-block 100-D diagonal sequences (Computation 2)
  Short sequences computed locally:
    - 5 eigenvalues of G5               (Computation 3)
    - Block G5 eigenvalues (2 per block) (Computation 2)
    - Trajectory lambda_min(G5) vs N    (Computation 4)

Five Computations:
  1. G5 (5x5) Gram matrix — eigenvalues, condition number, PD check
  2. Block-wise Gram matrices — A {p=7,11,13}, B {p=3,5}, C {p=2}
  3. Chavez on eigenvalue + diagonal sequences (short: local; long: MCP)
  4. lambda_min(G5) trajectory — N = 10, 20, 30, 50, 75, 100
  5. Row-wise Gram structure — data prepared for CAILculator ZDTP
"""

import numpy as np
import json
import mpmath

mpmath.mp.dps = 25
rng = np.random.default_rng(seed=42)

# ══════════════════════════════════════════════════════════════════════════════
# EMBEDDING — Phase 20B exact
# ══════════════════════════════════════════════════════════════════════════════

sqrt2 = np.sqrt(2.0)

# 6D basis: [e2, e7, e3, e6, e4, e5]
# Block A {e2,e7} — indices 0,1 — primes 7, 11, 13
# Block B {e3,e6} — indices 2,3 — primes 3, 5  (Heegner channel)
# Block C {e4,e5} — indices 4,5 — prime 2

PRIME_ROOT = {
    2:  np.array([ 0.,  0.,  0.,  0.,  1.,  1.]) / sqrt2,  # q4 = (e4+e5)/sqrt2
    3:  np.array([ 0.,  0., -1.,  1.,  0.,  0.]) / sqrt2,  # q2 = (-e3+e6)/sqrt2
    5:  np.array([ 0.,  0.,  1.,  1.,  0.,  0.]) / sqrt2,  # v5 = (e3+e6)/sqrt2
    7:  np.array([ 1., -1.,  0.,  0.,  0.,  0.]) / sqrt2,  # v1 = (e2-e7)/sqrt2
    11: np.array([ 1.,  1.,  0.,  0.,  0.,  0.]) / sqrt2,  # v4 = (e2+e7)/sqrt2
    13: np.array([-1.,  1.,  0.,  0.,  0.,  0.]) / sqrt2,  # q3 = (-e2+e7)/sqrt2
}

BLOCK_IDX    = {'A': slice(0, 2), 'B': slice(2, 4), 'C': slice(4, 6)}
BLOCK_PRIMES = {'A': [7, 11, 13], 'B': [3, 5], 'C': [2]}
LOG_SQRT     = {p: np.log(p) / np.sqrt(p) for p in PRIME_ROOT}

def f5D(t):
    """Phase 20B embedding: sum_p (log p / sqrt p) * cos(t * log p) * r_p"""
    out = np.zeros(6)
    for p, r in PRIME_ROOT.items():
        out += LOG_SQRT[p] * np.cos(t * np.log(p)) * r
    return out

def build_F(t_vals):
    """Build N×6 embedding matrix F where F[n] = f5D(t_vals[n])."""
    N = len(t_vals)
    F = np.zeros((N, 6))
    for i, t in enumerate(t_vals):
        F[i] = f5D(t)
    return F

# ── G5: 5D projection — removes the v1/q3 redundancy ─────────────────────────
# Maps 6D basis [e2, e7, e3, e6, e4, e5] -> 5D basis [e2, e7, e3, e6, (e4+e5)/sqrt2]
# v1=-q3 means {e2,e7} already captures the full Block A span.
# Block C: q4=(e4+e5)/sqrt2 is a single 1D direction — rank 1 in {e4,e5}.

P5 = np.zeros((5, 6))
P5[0, 0] = 1.0            # e2 -> coord 0
P5[1, 1] = 1.0            # e7 -> coord 1
P5[2, 2] = 1.0            # e3 -> coord 2
P5[3, 3] = 1.0            # e6 -> coord 3
P5[4, 4] = 1.0 / sqrt2    # (e4+e5)/sqrt2 : e4 component
P5[4, 5] = 1.0 / sqrt2    # (e4+e5)/sqrt2 : e5 component

def gram_G5(F):
    """G5 = (F@P5.T).T @ (F@P5.T) = 5x5 Gram matrix in 5D subspace."""
    F5 = F @ P5.T    # N×5
    return F5.T @ F5  # 5×5

def gram_G6(F):
    """G6 = F.T @ F (6x6). Has one structural zero eigenvalue from v1=-q3."""
    return F.T @ F

def gram_NxN(F):
    """G_NxN = F @ F.T (N×N inner product matrix)."""
    return F @ F.T

# ── JSON serialization helper ──────────────────────────────────────────────────

def safe(x):
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        if np.isnan(x) or np.isinf(x):
            return None
        return float(x)
    return x

# ── Conjugation symmetry (local, for short sequences only) ────────────────────

def conjugation_symmetry(seq):
    """CAILculator formula. Input normalized to [0,1]. For sequences < 50."""
    x = np.asarray(seq, dtype=float)
    if len(x) < 2:
        return 1.0
    xmin, xmax = x.min(), x.max()
    if xmax - xmin < 1e-15:
        return 1.0
    x = (x - xmin) / (xmax - xmin)
    n = len(x)
    diffs = [abs(x[i] - x[n - 1 - i]) for i in range(n // 2)]
    return float(1.0 - np.mean(diffs))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 0: Fetch N=100 Riemann zeros
# ══════════════════════════════════════════════════════════════════════════════

N_MAX   = 100
N_SEEDS = 10

print("=" * 65)
print("PHASE 22: Weil-Gram Bridge")
print("=" * 65)
print(f"\nFetching {N_MAX} Riemann zeros (mpmath dps=25)...")

zeros_t = []
for n in range(1, N_MAX + 1):
    z = mpmath.zetazero(n)
    zeros_t.append(float(z.imag))
    if n % 20 == 0:
        print(f"  ... fetched {n}/{N_MAX}: t_{n} = {zeros_t[-1]:.4f}")

zeros_t = np.array(zeros_t)
t_min, t_max = zeros_t[0], zeros_t[-1]
print(f"\n  t_1   = {t_min:.6f}")
print(f"  t_100 = {t_max:.6f}")

rand_t_sets = [rng.uniform(t_min, t_max, N_MAX) for _ in range(N_SEEDS)]

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: G5 and G6 Gram Matrix Construction (N=100)
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("COMPUTATION 1: Gram Matrix Construction (N=100)")
print("=" * 65)
print()
print("Rank structure:")
print("  v1 = -q3 (antipodal) => 6 roots span only 5D.")
print("  Block C (q4) is a single 1D direction in {e4,e5}.")
print("  G6 = F.T@F (6x6) has one structural zero eigenvalue.")
print("  G5 = (F@P5.T).T@(F@P5.T) (5x5) is the primary PD object.")
print()

F_zeros  = build_F(zeros_t)
F5_zeros = F_zeros @ P5.T    # N×5

# G5 — primary positive definiteness check
G5_zeros   = gram_G5(F_zeros)
evals_G5   = np.sort(np.linalg.eigvalsh(G5_zeros))
is_pd_G5   = bool(np.all(evals_G5 > 0))
cond_G5    = safe(float(evals_G5[-1] / evals_G5[0])) if evals_G5[0] > 1e-15 else None

# G6 — reference
G6_zeros   = gram_G6(F_zeros)
evals_G6   = np.sort(np.linalg.eigvalsh(G6_zeros))

# G_NxN (100×100)
G_full     = gram_NxN(F_zeros)
evals_full = np.sort(np.linalg.eigvalsh(G_full))
n_pos_full = int(np.sum(evals_full > 1e-10))
diag_vals  = np.diag(G_full)    # ||f5D(tn)||^2

print(f"G5 (5×5 — primary PD object):")
print(f"  Eigenvalues: {', '.join(f'{e:.6f}' for e in evals_G5)}")
print(f"  Positive definite: {is_pd_G5}")
print(f"  Condition number:  {f'{cond_G5:.2f}' if cond_G5 else 'inf'}")
print(f"  Trace: {float(np.trace(G5_zeros)):.4f}")
print()

print(f"G6 (6×6 — reference, has structural zero from v1=-q3):")
print(f"  Eigenvalues: {', '.join(f'{e:.6f}' for e in evals_G6)}")
print(f"  Rank: {int(np.sum(evals_G6 > 1e-10))}  (expected 5 of 6)")
print()

print(f"G_100x100 eigenvalue summary:")
print(f"  Positive (> 1e-10): {n_pos_full}  (embedding rank = 5)")
print(f"  5 largest: {', '.join(f'{e:.4f}' for e in evals_full[-5:])}")
print()

print(f"Diagonal ||f5D(tn)||^2:  "
      f"min={diag_vals.min():.6f}  max={diag_vals.max():.6f}  "
      f"mean={diag_vals.mean():.6f}  std={diag_vals.std():.6f}")
print()

# Random control G5
rand_G5_results = []
for seed_idx, t_rand in enumerate(rand_t_sets):
    F_rand    = build_F(t_rand)
    G5_rand   = gram_G5(F_rand)
    ev_rand   = np.sort(np.linalg.eigvalsh(G5_rand))
    is_pd_r   = bool(np.all(ev_rand > 0))
    cond_r    = safe(float(ev_rand[-1] / ev_rand[0])) if ev_rand[0] > 1e-15 else None
    rand_G5_results.append({
        'seed': seed_idx,
        'eigenvalues': [safe(e) for e in ev_rand.tolist()],
        'is_positive_definite': is_pd_r,
        'condition_number': cond_r,
        'min_eigenvalue': safe(float(ev_rand[0])),
    })

rand_min_evals = [r['min_eigenvalue'] for r in rand_G5_results if r['min_eigenvalue'] is not None]
rand_conds     = [r['condition_number'] for r in rand_G5_results if r['condition_number'] is not None]

print(f"Random control G5 ({N_SEEDS} seeds):")
print(f"  Min eigenvalue — mean={np.mean(rand_min_evals):.4f}  "
      f"std={np.std(rand_min_evals):.4f}  "
      f"range=[{min(rand_min_evals):.4f}, {max(rand_min_evals):.4f}]")
print(f"  Condition number — mean={np.mean(rand_conds):.2f}  std={np.std(rand_conds):.2f}")
print(f"  All positive definite: {all(r['is_positive_definite'] for r in rand_G5_results)}")
print()

print(f"SUMMARY — Computation 1:")
print(f"  Zeros G5 min eigenvalue:   {evals_G5[0]:.6f}")
print(f"  Random G5 min eigenvalue:  {np.mean(rand_min_evals):.6f} (mean)")
print(f"  Zeros condition number:    {f'{cond_G5:.2f}' if cond_G5 else 'inf'}")
print(f"  Random condition number:   {np.mean(rand_conds):.2f} (mean)")
print(f"  G5 positive definite:      {is_pd_G5}")

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: Block-wise Gram Matrices
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("COMPUTATION 2: Block-wise Gram Matrices")
print("=" * 65)
print()
print("Block A {e2,e7}  primes p=7,11,13 — 2D span (v1,v4,q3 all in {e2,e7})")
print("Block B {e3,e6}  primes p=3,5     — 2D span (Heegner channel)")
print("Block C {e4,e5}  prime  p=2       — effective 1D (q4 is single direction)")
print("G_full = G_A + G_B + G_C (additive decomposition)")
print()
print("100-D diagonal sequences per block prepared for CAILculator MCP.")
print()

block_results        = {}
block_diag_sequences = {}
G_reconstructed      = np.zeros((N_MAX, N_MAX))

for blk in ('A', 'B', 'C'):
    sl     = BLOCK_IDX[blk]
    F_blk  = F_zeros[:, sl]     # N×2
    G_blk  = F_blk @ F_blk.T   # N×N block Gram
    G6_blk = F_blk.T @ F_blk   # 2×2
    G_reconstructed += G_blk

    ev_blk      = np.sort(np.linalg.eigvalsh(G6_blk))
    n_nonzero   = int(np.sum(ev_blk > 1e-10))
    is_pd_blk   = bool(np.all(ev_blk > 0))
    cond_blk    = safe(float(ev_blk[-1] / ev_blk[0])) if ev_blk[0] > 1e-15 else None

    diag_blk    = np.diag(G_blk)
    block_diag_sequences[blk] = diag_blk.tolist()

    # Local Chavez on block 2×2 eigenvalues only (n=2 < 50)
    sym_ev_blk = conjugation_symmetry(ev_blk)

    block_results[blk] = {
        'primes': BLOCK_PRIMES[blk],
        'embedding_dim': sl.stop - sl.start,
        'effective_rank': n_nonzero,
        'G6_block_eigenvalues': [safe(e) for e in ev_blk.tolist()],
        'G6_block_is_positive_definite': is_pd_blk,
        'G6_block_condition_number': cond_blk,
        'G6_block_conjugation_symmetry_local': safe(sym_ev_blk),
        'diag_min': safe(float(diag_blk.min())),
        'diag_max': safe(float(diag_blk.max())),
        'diag_mean': safe(float(diag_blk.mean())),
        'note_chavez_mcp': f'100-D diagonal sequence in block_diag_sequences.{blk} for CAILculator.',
    }

    print(f"Block {blk} (primes {BLOCK_PRIMES[blk]}):")
    print(f"  G_block eigenvalues: {', '.join(f'{e:.6f}' for e in ev_blk)}")
    print(f"  Effective rank: {n_nonzero} / {sl.stop - sl.start}")
    if blk == 'C':
        print(f"  *** rank 1 — q4=(e4+e5)/sqrt2 is a single direction ***")
    print(f"  Diagonal range: [{diag_blk.min():.4f}, {diag_blk.max():.4f}]  "
          f"local Chavez (n=2 eigenvalues): {sym_ev_blk:.4f}")
    print()

recon_err = float(np.max(np.abs(G_full - G_reconstructed)))
print(f"Reconstruction check ||G - (G_A+G_B+G_C)||_inf = {recon_err:.2e}  "
      f"{'OK' if recon_err < 1e-12 else 'WARNING'}")

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: Chavez on Eigenvalue Sequences
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("COMPUTATION 3: Chavez on Eigenvalue Sequences")
print("=" * 65)
print()
print("n < 50 — computed locally; n >= 50 — prepared for CAILculator MCP.")
print()

# ── (a) 5 eigenvalues of G5 — LOCAL (n=5) ────────────────────────────────────

sym_G5_evals_zeros = conjugation_symmetry(evals_G5)

rand_G5_eval_syms = []
for t_rand in rand_t_sets:
    F_rand  = build_F(t_rand)
    G5_rand = gram_G5(F_rand)
    ev      = np.sort(np.linalg.eigvalsh(G5_rand))
    rand_G5_eval_syms.append(conjugation_symmetry(ev))

print(f"(a) G5 eigenvalues (n=5, local):")
print(f"  Zeros eigenvalues:  {', '.join(f'{e:.4f}' for e in evals_G5)}")
print(f"  Zeros Chavez sym:   {sym_G5_evals_zeros:.6f}")
print(f"  Random Chavez sym:  mean={np.mean(rand_G5_eval_syms):.6f}  "
      f"std={np.std(rand_G5_eval_syms):.6f}")
print(f"  Delta:              {sym_G5_evals_zeros - np.mean(rand_G5_eval_syms):+.6f}")
print()

# ── (b) 100 diagonal values ||f5D(tn)||^2 — MCP HANDOFF ──────────────────────

diag_sorted = np.sort(diag_vals)

rand_diag_sorted_all = []
for t_rand in rand_t_sets:
    F_rand = build_F(t_rand)
    d      = np.array([F_rand[i] @ F_rand[i] for i in range(N_MAX)])
    rand_diag_sorted_all.append(np.sort(d).tolist())

print(f"(b) 100 sorted diagonal values ||f5D(tn)||^2 — CAILculator MCP:")
print(f"  Range: [{diag_vals.min():.6f}, {diag_vals.max():.6f}]")
print(f"  Sequence saved as cailculator_sequences.diag_norms_sorted_100")
print()

# ── (c) Row norms of F5 (100 values) — MCP HANDOFF ───────────────────────────

row_norms_F5        = np.sqrt(np.sum(F5_zeros ** 2, axis=1))
row_norms_F5_sorted = np.sort(row_norms_F5)

# Singular values of F5 (5 values — local, n=5)
_, sv_F5, _ = np.linalg.svd(F5_zeros, full_matrices=False)

print(f"(c) Singular values of F5 (n=5, local):")
print(f"  sv(F5): {', '.join(f'{v:.4f}' for v in sv_F5)}")
print(f"  Condition: {sv_F5[0]/sv_F5[-1]:.2f}  "
      f"(= sqrt(cond G5) = sqrt({cond_G5:.2f}) = {np.sqrt(cond_G5):.2f})")
print()
print(f"(c2) 100 sorted row norms of F5 — CAILculator MCP:")
print(f"  Range: [{row_norms_F5_sorted.min():.6f}, {row_norms_F5_sorted.max():.6f}]")
print(f"  Sequence saved as cailculator_sequences.row_norms_F5_sorted_100")
print()

# ── (d) Off-diagonal inner products (4950 values) — MCP HANDOFF ──────────────

upper_tri_vals   = G_full[np.triu_indices(N_MAX, k=1)]
upper_tri_sorted = np.sort(upper_tri_vals)

print(f"(d) Off-diagonal inner products G[i,j], i<j (n=4950) — CAILculator MCP:")
print(f"  Range: [{upper_tri_sorted.min():.6f}, {upper_tri_sorted.max():.6f}]")
print(f"  Mean: {upper_tri_sorted.mean():.6f}  Std: {upper_tri_sorted.std():.6f}")
print(f"  Sequence saved as cailculator_sequences.upper_tri_inner_products_4950")
print()

print(f"SUMMARY — Computation 3:")
print(f"  G5 evals (n=5):  zeros={sym_G5_evals_zeros:.4f}  "
      f"random={np.mean(rand_G5_eval_syms):.4f}  "
      f"delta={sym_G5_evals_zeros - np.mean(rand_G5_eval_syms):+.4f}")
print(f"  Long sequences (n >= 50): prepared for CAILculator MCP.")

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: lambda_min(G5) Trajectory
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("COMPUTATION 4: lambda_min(G5) Trajectory")
print("=" * 65)
print()
print("Tracking lambda_min(G5) as N grows.")
print("Stable, bounded-away-from-zero floor => strong injectivity signal.")
print()
print(f"{'N':>6}  {'zeros lambda_min(G5)':>22}  {'zeros cond(G5)':>16}  "
      f"{'rand mean(lmin)':>17}  {'rand mean(cond)':>16}")
print("-" * 86)

N_trajectory      = [10, 20, 30, 50, 75, 100]
trajectory_results = []

for N in N_trajectory:
    F_n    = build_F(zeros_t[:N])
    G5_n   = gram_G5(F_n)
    ev_n   = np.sort(np.linalg.eigvalsh(G5_n))
    lmin_n = float(ev_n[0])
    lmax_n = float(ev_n[-1])
    cond_n = lmax_n / lmin_n if lmin_n > 1e-15 else float('inf')

    rand_lmins  = []
    rand_conds_n = []
    for t_rand in rand_t_sets:
        F_rand_n = build_F(t_rand[:N])
        G5_rn    = gram_G5(F_rand_n)
        ev_rn    = np.sort(np.linalg.eigvalsh(G5_rn))
        lmin_r   = float(ev_rn[0])
        lmax_r   = float(ev_rn[-1])
        rand_lmins.append(lmin_r)
        rand_conds_n.append(lmax_r / lmin_r if lmin_r > 1e-15 else float('inf'))

    rand_lmin_mean = float(np.mean(rand_lmins))
    finite_conds   = [c for c in rand_conds_n if c != float('inf')]
    rand_cond_mean = float(np.mean(finite_conds)) if finite_conds else float('inf')

    trajectory_results.append({
        'N': N,
        'zeros': {
            'lambda_min_G5': safe(lmin_n),
            'lambda_max_G5': safe(lmax_n),
            'condition_number_G5': safe(cond_n),
            'G5_eigenvalues': [safe(e) for e in ev_n.tolist()],
        },
        'random_control': {
            'lambda_min_mean': safe(rand_lmin_mean),
            'lambda_min_std': safe(float(np.std(rand_lmins))),
            'condition_number_mean': safe(rand_cond_mean),
        },
    })

    cond_str      = f'{cond_n:.2f}' if cond_n != float('inf') else 'inf'
    rand_cond_str = f'{rand_cond_mean:.2f}' if rand_cond_mean != float('inf') else 'inf'
    print(f"{N:>6}  {lmin_n:>22.6f}  {cond_str:>16}  "
          f"{rand_lmin_mean:>17.6f}  {rand_cond_str:>16}")

print()

lmins_zeros = [r['zeros']['lambda_min_G5']           for r in trajectory_results]
lmins_rand  = [r['random_control']['lambda_min_mean'] for r in trajectory_results]
final_zero  = lmins_zeros[-1]
final_rand  = lmins_rand[-1]
ratio       = safe(final_zero / final_rand) if final_rand and final_rand > 0 else None

print(f"Zeros lambda_min(G5) trend:  {' -> '.join(f'{x:.4f}' for x in lmins_zeros)}")
print(f"Random lambda_min(G5) trend: {' -> '.join(f'{x:.4f}' for x in lmins_rand)}")
print()
print(f"At N=100:")
print(f"  Zeros lambda_min(G5):  {final_zero:.6f}")
print(f"  Random lambda_min(G5): {final_rand:.6f}")
if ratio:
    print(f"  Ratio zeros/random:    {ratio:.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 5: Row-wise Gram Structure (Data for CAILculator ZDTP)
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("COMPUTATION 5: Row-wise Gram Structure")
print("=" * 65)
print()
print("Each row G[i,:] = [<f5D(ti), f5D(tj)> : j=0..99] is a 100D vector.")
print("ZDTP + Chavez Transform: CAILculator MCP.")
print("Local statistics for context.")
print()

# Local row stats (no 100-D Chavez locally)
row_means_zeros  = np.array([G_full[i, :].mean() for i in range(N_MAX)])
row_stds_zeros   = np.array([G_full[i, :].std()  for i in range(N_MAX)])

# Mean sorted-row profile (useful 100-D summary for MCP)
row_sorted_zeros      = np.sort(G_full, axis=1)
row_sorted_means      = row_sorted_zeros.mean(axis=0)   # 100D
row_sorted_stds       = row_sorted_zeros.std(axis=0)    # 100D

# Random control (seed 0)
F_rand_rep            = build_F(rand_t_sets[0])
G_rand_rep            = gram_NxN(F_rand_rep)
row_sorted_rand       = np.sort(G_rand_rep, axis=1)
row_sorted_means_rand = row_sorted_rand.mean(axis=0)

print(f"Row statistics (100 rows of G_100x100):")
print(f"  Row mean:   min={row_means_zeros.min():.4f}  "
      f"max={row_means_zeros.max():.4f}  mean={row_means_zeros.mean():.4f}")
print(f"  Row std:    min={row_stds_zeros.min():.4f}   "
      f"max={row_stds_zeros.max():.4f}  mean={row_stds_zeros.mean():.4f}")
print()
print(f"Mean sorted-row profile (zeros vs random seed 0):")
print(f"  rank=0:   zeros={row_sorted_means[0]:.4f}   random={row_sorted_means_rand[0]:.4f}")
print(f"  rank=50:  zeros={row_sorted_means[50]:.4f}  random={row_sorted_means_rand[50]:.4f}")
print(f"  rank=99:  zeros={row_sorted_means[99]:.4f}  random={row_sorted_means_rand[99]:.4f}")
print()
print("NOTE: Full ZDTP on individual rows via CAILculator MCP.")
print("      Sequences saved in cailculator_sequences:")
print("        row_sorted_means_100         (mean sorted profile)")
print("        upper_tri_inner_products_4950 (all off-diagonal G[i,j])")

# ══════════════════════════════════════════════════════════════════════════════
# CAILculator HANDOFF SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("CAILculator MCP HANDOFF")
print("=" * 65)
print()
print("Sequences in phase22_results.json -> cailculator_sequences:")
print()
print("  1. diag_norms_sorted_100         (n=100)")
print("     Sorted ||f5D(tn)||^2 values — Chavez + ZDTP + GUE/Poisson baselines")
print()
print("  2. row_norms_F5_sorted_100       (n=100)")
print("     Sorted row norms of 5D embedding matrix F5")
print("     Chavez + ZDTP + GUE/Poisson baselines")
print()
print("  3. row_sorted_means_100          (n=100)")
print("     Mean of each sorted Gram row — Chavez zeros vs random")
print()
print("  4. upper_tri_inner_products_4950 (n=4950)")
print("     All off-diagonal inner products G[i,j], i<j — ZDTP analysis")
print()
print("  5. block_diag_A_sorted_100, block_diag_B_sorted_100, block_diag_C_sorted_100")
print("     100-D diagonal sequences per block — Chavez per block")
print()
print("  6. random_diag_norms_sorted_100_seed0")
print("     Random control for comparison with diag_norms_sorted_100")

# ══════════════════════════════════════════════════════════════════════════════
# OVERALL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 65)
print("OVERALL SUMMARY")
print("=" * 65)
print()

print(f"Result A — G5 (5×5) Positive Definiteness:")
print(f"  PD: {is_pd_G5}  |  lambda_min = {evals_G5[0]:.6f}  |  "
      f"cond = {f'{cond_G5:.2f}' if cond_G5 else 'inf'}")
print()
print(f"Result B — G5 eigenvalue Chavez (n=5, local):")
print(f"  Zeros: {sym_G5_evals_zeros:.4f}  "
      f"Random mean: {np.mean(rand_G5_eval_syms):.4f}  "
      f"Delta: {sym_G5_evals_zeros - np.mean(rand_G5_eval_syms):+.4f}")
print()
print(f"Result C — Block Analysis:")
for blk in 'ABC':
    r     = block_results[blk]['effective_rank']
    dim   = block_results[blk]['embedding_dim']
    cond_b = block_results[blk]['G6_block_condition_number']
    print(f"  Block {blk}: rank={r}/{dim}  "
          f"cond={f'{cond_b:.2f}' if cond_b else 'inf'}")
print()
print(f"Result D — Trajectory lambda_min(G5):")
traj_N_str    = ', '.join(str(r['N']) for r in trajectory_results)
traj_zer_str  = ', '.join(f"{r['zeros']['lambda_min_G5']:.4f}" for r in trajectory_results)
traj_rand_str = ', '.join(f"{r['random_control']['lambda_min_mean']:.4f}" for r in trajectory_results)
print(f"  N:      {traj_N_str}")
print(f"  Zeros:  {traj_zer_str}")
print(f"  Random: {traj_rand_str}")
print(f"  At N=100: zeros={final_zero:.6f}  random={final_rand:.6f}  "
      f"ratio={f'{ratio:.4f}' if ratio else 'N/A'}")
print()
print("CAILculator: 7 sequences prepared in cailculator_sequences.*")

# ══════════════════════════════════════════════════════════════════════════════
# SAVE JSON
# ══════════════════════════════════════════════════════════════════════════════

results = {
    'experiment': 'Phase22_Weil_Gram_Bridge',
    'date': '2026-03-24',
    'n_zeros': N_MAX,
    'n_random_seeds': N_SEEDS,
    'zeros_t_range': [safe(t_min), safe(t_max)],
    'embedding': {
        'formula': 'f5D(t) = sum_p (log p / sqrt p) * cos(t * log p) * r_p',
        'primes': [2, 3, 5, 7, 11, 13],
        'prime_to_root': {
            '2': 'q4=(e4+e5)/sqrt2', '3': 'q2=(-e3+e6)/sqrt2',
            '5': 'v5=(e3+e6)/sqrt2', '7': 'v1=(e2-e7)/sqrt2',
            '11': 'v4=(e2+e7)/sqrt2', '13': 'q3=(-e2+e7)/sqrt2',
        },
        'basis_6d': '[e2, e7, e3, e6, e4, e5]',
        'blocks': {
            'A': {'indices': [0, 1], 'primes': [7, 11, 13]},
            'B': {'indices': [2, 3], 'primes': [3, 5], 'note': 'Heegner channel'},
            'C': {'indices': [4, 5], 'primes': [2],  'note': 'rank 1, q4 direction'},
        },
    },
    'rank_note': (
        'v1 = -q3 (antipodal): 6 roots span only 5D. Block C effective rank 1. '
        'G5 (5x5 via P5 projection) is the primary PD object. '
        'G6 (6x6) kept for reference — has one structural zero eigenvalue.'
    ),
    'computation_1': {
        'G5': {
            'eigenvalues': [safe(e) for e in evals_G5.tolist()],
            'is_positive_definite': safe(is_pd_G5),
            'condition_number': safe(cond_G5),
            'trace': safe(float(np.trace(G5_zeros))),
            'min_eigenvalue': safe(float(evals_G5[0])),
            'max_eigenvalue': safe(float(evals_G5[-1])),
        },
        'G6_reference': {
            'eigenvalues': [safe(e) for e in evals_G6.tolist()],
            'rank': int(np.sum(evals_G6 > 1e-10)),
        },
        'G_100x100': {
            'n_positive_eigenvalues': n_pos_full,
            'largest_5_eigenvalues': [safe(e) for e in evals_full[-5:].tolist()],
        },
        'diagonal': {
            'min': safe(float(diag_vals.min())),
            'max': safe(float(diag_vals.max())),
            'mean': safe(float(diag_vals.mean())),
            'std': safe(float(diag_vals.std())),
            'values': [safe(v) for v in diag_vals.tolist()],
        },
        'random_control_G5': {
            'n_seeds': N_SEEDS,
            'min_eigenvalue_mean': safe(float(np.mean(rand_min_evals))),
            'min_eigenvalue_std': safe(float(np.std(rand_min_evals))),
            'condition_number_mean': safe(float(np.mean(rand_conds))),
            'seeds': rand_G5_results,
        },
    },
    'computation_2': {
        'reconstruction_error': safe(recon_err),
        'blocks': block_results,
        'block_diag_sequences': block_diag_sequences,
    },
    'computation_3': {
        'G5_eigenvalues_local': {
            'zeros_eigenvalues': [safe(e) for e in evals_G5.tolist()],
            'zeros_conjugation_symmetry': safe(sym_G5_evals_zeros),
            'random_mean': safe(float(np.mean(rand_G5_eval_syms))),
            'random_std': safe(float(np.std(rand_G5_eval_syms))),
            'delta': safe(float(sym_G5_evals_zeros - np.mean(rand_G5_eval_syms))),
            'note': 'n=5, computed locally (< 50)',
        },
        'note_long_sequences': (
            'Chavez Transform for sequences n >= 50 deferred to CAILculator MCP. '
            'See cailculator_sequences below.'
        ),
    },
    'computation_4': {
        'trajectory': trajectory_results,
        'N_values': N_trajectory,
        'zeros_lambda_min_at_N100': safe(final_zero),
        'random_lambda_min_mean_at_N100': safe(final_rand),
        'ratio_zeros_over_random': safe(ratio),
        'zeros_trend': [safe(x) for x in lmins_zeros],
        'random_trend': [safe(x) for x in lmins_rand],
    },
    'computation_5': {
        'row_means': [safe(v) for v in row_means_zeros.tolist()],
        'row_stds':  [safe(v) for v in row_stds_zeros.tolist()],
        'row_sorted_means': [safe(v) for v in row_sorted_means.tolist()],
        'row_sorted_stds':  [safe(v) for v in row_sorted_stds.tolist()],
        'row_sorted_means_random_seed0': [safe(v) for v in row_sorted_means_rand.tolist()],
        'note': 'Full ZDTP + Chavez via CAILculator MCP. See cailculator_sequences.',
    },
    'cailculator_sequences': {
        'diag_norms_sorted_100': [safe(v) for v in diag_sorted.tolist()],
        'row_norms_F5_sorted_100': [safe(v) for v in row_norms_F5_sorted.tolist()],
        'row_sorted_means_100': [safe(v) for v in row_sorted_means.tolist()],
        'upper_tri_inner_products_4950': [safe(v) for v in upper_tri_sorted.tolist()],
        'block_diag_A_sorted_100': [safe(v) for v in sorted(block_diag_sequences['A'])],
        'block_diag_B_sorted_100': [safe(v) for v in sorted(block_diag_sequences['B'])],
        'block_diag_C_sorted_100': [safe(v) for v in sorted(block_diag_sequences['C'])],
        'random_diag_norms_sorted_100_seed0': [safe(v) for v in sorted(rand_diag_sorted_all[0])],
    },
    'headline_results': {
        'result_A_G5_positive_definite': safe(is_pd_G5),
        'result_A_smallest_eigenvalue': safe(float(evals_G5[0])),
        'result_A_condition_number': safe(cond_G5),
        'result_B_G5_evals_Chavez_zeros': safe(sym_G5_evals_zeros),
        'result_B_G5_evals_Chavez_random_mean': safe(float(np.mean(rand_G5_eval_syms))),
        'result_B_G5_evals_Chavez_delta': safe(float(sym_G5_evals_zeros - np.mean(rand_G5_eval_syms))),
        'result_C_block_ranks': {b: block_results[b]['effective_rank'] for b in 'ABC'},
        'result_D_trajectory_zeros': [safe(x) for x in lmins_zeros],
        'result_D_trajectory_random': [safe(x) for x in lmins_rand],
        'result_D_ratio_at_N100': safe(ratio),
        'note_chavez_long_sequences': 'Run CAILculator MCP on cailculator_sequences.*',
    },
}

with open('phase22_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to phase22_results.json")
print("Next: Run CAILculator MCP on cailculator_sequences.* in Claude Desktop.")
