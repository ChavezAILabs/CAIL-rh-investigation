"""
Phase 24 Thread 1 — Windowed Weil Identity
Chavez AI Labs LLC · March 25, 2026

Tests whether the 12.1% residual ratio (Weil angle locked at 6.8°, Phase 23T3)
shrinks toward zero when the Gaussian window exp(-t²/T²) is applied to f5D,
making the test function Schwartz-class.

Key question: Is the 12% residual structural or a test-function artifact?
"""

import numpy as np
import json
import math

# ── Embedding (Phase 20B canonical) ──────────────────────────────────────────

sqrt2 = np.sqrt(2.0)

ROOT_DIRS = {
    2:  np.array([0, 0, 0, 0, 1,  1]) / sqrt2,   # q4 — Block C
    3:  np.array([0, 0,-1, 1, 0,  0]) / sqrt2,   # q2 — Block B (Heegner)
    5:  np.array([0, 0, 1, 1, 0,  0]) / sqrt2,   # v5 — Block B
    7:  np.array([1,-1, 0, 0, 0,  0]) / sqrt2,   # v1 — Block A
    11: np.array([1, 1, 0, 0, 0,  0]) / sqrt2,   # v4 — Block A
    13: np.array([-1,1, 0, 0, 0,  0]) / sqrt2,   # q3 — Block A (bilateral hub)
}
PRIMES = [2, 3, 5, 7, 11, 13]

BLOCK_A = [7, 11, 13]
BLOCK_B = [3, 5]
BLOCK_C = [2]

def f5D(t):
    result = np.zeros(6)
    for p, r in ROOT_DIRS.items():
        result += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def h_T(t, T):
    """Windowed test function: Gaussian window × f5D."""
    return math.exp(-t**2 / T**2) * f5D(t)

def f5D_block(t, primes):
    """f5D restricted to given block primes."""
    result = np.zeros(6)
    for p in primes:
        r = ROOT_DIRS[p]
        result += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return result

def h_T_block(t, T, primes):
    return math.exp(-t**2 / T**2) * f5D_block(t, primes)

# ── Windowed RHS (Gaussian Fourier transform of h_T) ─────────────────────────

def RHS_T(T):
    """
    Windowed Euler product RHS direction.
    ĥ_T(ω) for h_T(t) = exp(-t²/T²) * sum_p (log p/sqrt(p)) * cos(t*log p) * r_p
    Fourier transform: ĥ_T(log p_outer) uses sum over all inner prime cosine terms.
    Dominant Gaussian term: (T*sqrt(pi)/2) * exp(-T²*(omega - omega0)²/4)
    """
    result = np.zeros(6)
    for p_outer, r in ROOT_DIRS.items():
        weight = 0.0
        omega = math.log(p_outer)
        for p_inner in PRIMES:
            omega0 = math.log(p_inner)
            # ĥ_T at frequency omega from inner prime's cosine term
            weight += (math.log(p_inner) / math.sqrt(p_inner)) * \
                      (T * math.sqrt(math.pi) / 2) * \
                      math.exp(-T**2 * (omega - omega0)**2 / 4)
        result -= r * weight
    return result

def safe(x):
    if x is None:
        return None
    if isinstance(x, (list, tuple)):
        return [safe(i) for i in x]
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        if math.isnan(x) or math.isinf(x):
            return None
        return float(x)
    return x

# ── Load zeros ────────────────────────────────────────────────────────────────

print("Loading zeros...")
with open('rh_zeros.json', 'r') as f:
    zeros_raw = json.load(f)

zeros_t = [float(z) for z in zeros_raw[:500]]
N_MAX = 500
print(f"  Using {N_MAX} zeros: t1={zeros_t[0]:.4f}, t500={zeros_t[N_MAX-1]:.4f}")

# ── Precompute f5D and h_T vectors for all zeros ─────────────────────────────

print("Precomputing f5D vectors...")
f5D_vecs = np.array([f5D(t) for t in zeros_t])  # shape (500, 6)

print("Precomputing h_T vectors for each T...")
T_VALUES = [50, 100, 200, 500]

# h_T_vecs[T] = array of shape (N_MAX, 6)
h_T_vecs = {}
for T in T_VALUES:
    h_T_vecs[T] = np.array([math.exp(-zeros_t[n]**2 / T**2) * f5D_vecs[n]
                             for n in range(N_MAX)])
    n_effective = sum(1 for t in zeros_t if t < 2*T)
    print(f"  T={T}: effective zeros (t < 2T={2*T}): {n_effective}")

# ── Unwindowed RHS direction (from Phase 23T3: RHS = -f5D(0)) ────────────────

f5D_at_0 = f5D(0.0)
rhs_unwindowed = -f5D_at_0
rhs_unwindowed_dir = rhs_unwindowed / np.linalg.norm(rhs_unwindowed)
print(f"\nUnwindowed RHS direction (= -f5D(0)):")
print(f"  norm = {np.linalg.norm(rhs_unwindowed):.6f}")
print(f"  dir  = {rhs_unwindowed_dir}")

# ── Windowed RHS for each T ──────────────────────────────────────────────────

print("\nWindowed RHS directions:")
rhs_T = {}
rhs_T_dir = {}
rhs_T_cos_with_unwindowed = {}

for T in T_VALUES:
    rhs_T[T] = RHS_T(T)
    norm_rhs = np.linalg.norm(rhs_T[T])
    rhs_T_dir[T] = rhs_T[T] / norm_rhs
    cos_sim = np.dot(rhs_T_dir[T], rhs_unwindowed_dir)
    rhs_T_cos_with_unwindowed[T] = cos_sim
    print(f"  T={T}: ||RHS_T||={norm_rhs:.4f}, cos(RHS_T, RHS_unwindowed)={cos_sim:.6f}")

# ── Section 1: Windowed partial sums S_T(N) ──────────────────────────────────

print("\n=== Section 1: Windowed partial sums ===")

N_CHECKPOINTS = [10, 50, 100, 200, 300, 500]

# Cumulative sums for each T
S_T_cumulative = {}
for T in T_VALUES:
    S_T_cumulative[T] = np.cumsum(h_T_vecs[T], axis=0)  # (500, 6)

# Also unwindowed for reference
S_unwindowed_cumulative = np.cumsum(f5D_vecs, axis=0)  # (500, 6)

partial_sum_norms = {}
for T in T_VALUES:
    partial_sum_norms[T] = {}
    for N in N_CHECKPOINTS:
        norm_val = float(np.linalg.norm(S_T_cumulative[T][N-1]))
        partial_sum_norms[T][N] = norm_val

# Unwindowed norms
unwindowed_norms = {}
for N in N_CHECKPOINTS:
    unwindowed_norms[N] = float(np.linalg.norm(S_unwindowed_cumulative[N-1]))

print("|| S_T(N) || :")
print(f"{'N':>6}", end="")
for T in T_VALUES:
    print(f"  T={T:>4}", end="")
print("  Unwindowed")
for N in N_CHECKPOINTS:
    print(f"{N:>6}", end="")
    for T in T_VALUES:
        print(f"  {partial_sum_norms[T][N]:>8.4f}", end="")
    print(f"  {unwindowed_norms[N]:>10.4f}")

# ── Section 2: Residual ratio vs (T, N) ─────────────────────────────────────

print("\n=== Section 2: Residual ratios ===")

residual_ratios = {}
projections_onto_rhs = {}

for T in T_VALUES:
    residual_ratios[T] = {}
    projections_onto_rhs[T] = {}
    for N in N_CHECKPOINTS:
        S = S_T_cumulative[T][N-1]
        norm_S = np.linalg.norm(S)
        if norm_S < 1e-14:
            residual_ratios[T][N] = None
            projections_onto_rhs[T][N] = None
            continue
        proj_scalar = float(np.dot(S, rhs_T_dir[T]))
        proj_vec = proj_scalar * rhs_T_dir[T]
        residual_vec = S - proj_vec
        res_ratio = float(np.linalg.norm(residual_vec) / norm_S)
        residual_ratios[T][N] = res_ratio
        projections_onto_rhs[T][N] = proj_scalar / norm_S  # cos(angle)

# Unwindowed residuals
residual_ratios_unwindowed = {}
for N in N_CHECKPOINTS:
    S = S_unwindowed_cumulative[N-1]
    norm_S = np.linalg.norm(S)
    proj_scalar = float(np.dot(S, rhs_unwindowed_dir))
    proj_vec = proj_scalar * rhs_unwindowed_dir
    residual_vec = S - proj_vec
    residual_ratios_unwindowed[N] = float(np.linalg.norm(residual_vec) / norm_S)

print("Residual ratio = ||S_T(N) - proj|| / ||S_T(N)||:")
print(f"{'N':>6}", end="")
for T in T_VALUES:
    print(f"  T={T:>4}", end="")
print("  Unwindowed")
for N in N_CHECKPOINTS:
    print(f"{N:>6}", end="")
    for T in T_VALUES:
        v = residual_ratios[T][N]
        print(f"  {v:>8.4f}" if v is not None else "      None", end="")
    print(f"  {residual_ratios_unwindowed[N]:>10.4f}")

# ── Section 3: T -> ∞ extrapolation at N=500 ─────────────────────────────────

print("\n=== Section 3: T -> infinity extrapolation (N=500) ===")

T_vals_arr = np.array(T_VALUES, dtype=float)
res_N500 = np.array([residual_ratios[T][500] for T in T_VALUES])

print(f"T values: {T_vals_arr}")
print(f"Residual ratios at N=500: {res_N500}")

# Fit log-log: log(residual) = b*log(T) + log(a)  ->  power law
from numpy.polynomial import polynomial as P

log_T = np.log(T_vals_arr)
log_res = np.log(res_N500)
coeffs = np.polyfit(log_T, log_res, 1)
b_fit = coeffs[0]  # exponent
a_fit = math.exp(coeffs[1])  # coefficient
print(f"\nPower-law fit: residual(T) ~= {a_fit:.6f} * T^{b_fit:.4f}")
if b_fit < -0.01:
    model_type = "DECAYING (Weil identity satisfied in limit)"
elif b_fit > 0.01:
    model_type = "GROWING (window not helping)"
else:
    model_type = "CONSTANT (12% is structural)"
print(f"Model type: {model_type}")

# Also try linear fit in log-T
# residual ~= c (constant)
c_const = float(np.mean(res_N500))
print(f"Constant fit: residual ~= {c_const:.6f}")

# ── Section 4: Per-block windowed residuals (N=500) ──────────────────────────

print("\n=== Section 4: Per-block residuals at N=500 ===")

block_norms = {}
for T in T_VALUES:
    block_norms[T] = {}
    S = S_T_cumulative[T][N_MAX-1]

    for block_name, block_primes in [('A', BLOCK_A), ('B', BLOCK_B), ('C', BLOCK_C)]:
        # Project S onto the block subspace
        # Block subspace = span of ROOT_DIRS for block_primes
        block_vecs = [ROOT_DIRS[p] for p in block_primes]
        # Orthogonalize (they are already orthogonal by construction)
        block_proj = np.zeros(6)
        for bv in block_vecs:
            block_proj += np.dot(S, bv) * bv
        block_norms[T][block_name] = float(np.linalg.norm(block_proj))

    # Also compute the residual vector components in block space
    rhs_dir = rhs_T_dir[T]
    proj_scalar = np.dot(S, rhs_dir)
    residual = S - proj_scalar * rhs_dir
    block_residual_norms = {}
    for block_name, block_primes in [('A', BLOCK_A), ('B', BLOCK_B), ('C', BLOCK_C)]:
        block_vecs = [ROOT_DIRS[p] for p in block_primes]
        block_res_proj = np.zeros(6)
        for bv in block_vecs:
            block_res_proj += np.dot(residual, bv) * bv
        block_residual_norms[block_name] = float(np.linalg.norm(block_res_proj))
    block_norms[T]['residual'] = block_residual_norms
    total_residual_norm = float(np.linalg.norm(residual))
    block_norms[T]['total_residual_norm'] = total_residual_norm

print("Block decomposition of S_T(500) norm:")
print(f"{'T':>6}  {'||S_A||':>10}  {'||S_B||':>10}  {'||S_C||':>10}  {'Res_A':>8}  {'Res_B':>8}  {'Res_C':>8}")
for T in T_VALUES:
    bn = block_norms[T]
    res = bn['residual']
    print(f"{T:>6}  {bn['A']:>10.4f}  {bn['B']:>10.4f}  {bn['C']:>10.4f}  "
          f"{res['A']:>8.4f}  {res['B']:>8.4f}  {res['C']:>8.4f}")

# ── Section 5: Convergence rate for T=100 ────────────────────────────────────

print("\n=== Section 5: Convergence rate S_T=100(N) ===")

T_conv = 100
S_T100 = S_T_cumulative[T_conv]
S_final = S_T100[N_MAX-1]
norm_final = np.linalg.norm(S_final)

convergence_rates = []
for n in range(1, N_MAX):
    diff = np.linalg.norm(S_T100[n] - S_final) / (norm_final + 1e-14)
    convergence_rates.append(float(diff))

# Print at checkpoints
print(f"||S_T100(N) - S_T100(500)|| / ||S_T100(500)||:")
for N in [10, 50, 100, 200, 300, 400, 450, 490]:
    print(f"  N={N:>4}: {convergence_rates[N-1]:.6f}")

# ── Section 6: CAILculator sequences ────────────────────────────────────────

print("\n=== Section 6: CAILculator sequences (n=100 each) ===")

# n=100: N = 5, 10, 15, ..., 500
N_seq = [5*k for k in range(1, 101)]  # 100 values

cailculator_sequences = {}

# Residual ratio sequences for each T
for T in T_VALUES:
    seq_key = f"residual_ratio_T{T}_n100"
    seq = []
    for N in N_seq:
        S = S_T_cumulative[T][N-1]
        norm_S = np.linalg.norm(S)
        if norm_S < 1e-14:
            seq.append(None)
            continue
        proj_scalar = float(np.dot(S, rhs_T_dir[T]))
        residual = S - proj_scalar * rhs_T_dir[T]
        seq.append(float(np.linalg.norm(residual) / norm_S))
    cailculator_sequences[seq_key] = seq
    print(f"  {seq_key}: {len(seq)} values, range [{min(v for v in seq if v):.4f}, {max(v for v in seq if v):.4f}]")

# Unwindowed residual ratio (recompute for direct comparison)
seq_unwindowed = []
for N in N_seq:
    S = S_unwindowed_cumulative[N-1]
    norm_S = np.linalg.norm(S)
    proj_scalar = float(np.dot(S, rhs_unwindowed_dir))
    residual = S - proj_scalar * rhs_unwindowed_dir
    seq_unwindowed.append(float(np.linalg.norm(residual) / norm_S))
cailculator_sequences["residual_ratio_unwindowed_n100"] = seq_unwindowed
print(f"  residual_ratio_unwindowed_n100: range [{min(seq_unwindowed):.4f}, {max(seq_unwindowed):.4f}]")

# Projection fraction sequences (alignment with RHS)
for T in T_VALUES:
    seq_key = f"projection_fraction_T{T}_n100"
    seq = []
    for N in N_seq:
        S = S_T_cumulative[T][N-1]
        norm_S = np.linalg.norm(S)
        if norm_S < 1e-14:
            seq.append(None)
            continue
        proj_scalar = float(np.dot(S, rhs_T_dir[T]))
        seq.append(proj_scalar / norm_S)  # cosine of angle
    cailculator_sequences[seq_key] = seq
    valid = [v for v in seq if v is not None]
    print(f"  {seq_key}: range [{min(valid):.4f}, {max(valid):.4f}]")

# Convergence rate sequence for T=100
cailculator_sequences["convergence_rate_T100_n100"] = [convergence_rates[N-1] if N < N_MAX else 0.0 for N in N_seq]

# ── Compile results ───────────────────────────────────────────────────────────

results = {
    "phase": "24",
    "thread": 1,
    "title": "Windowed Weil Identity",
    "date": "2026-03-25",
    "researcher": "Paul Chavez, Chavez AI Labs",
    "n_zeros_used": N_MAX,
    "t_range": [zeros_t[0], zeros_t[N_MAX-1]],
    "T_values": T_VALUES,
    "N_checkpoints": N_CHECKPOINTS,

    "rhs_unwindowed": {
        "vector": safe(rhs_unwindowed),
        "norm": safe(np.linalg.norm(rhs_unwindowed)),
        "direction": safe(rhs_unwindowed_dir),
        "note": "= -f5D(0), algebraically exact"
    },

    "rhs_T": {
        str(T): {
            "vector": safe(rhs_T[T]),
            "norm": safe(np.linalg.norm(rhs_T[T])),
            "direction": safe(rhs_T_dir[T]),
            "cos_with_unwindowed": safe(rhs_T_cos_with_unwindowed[T])
        }
        for T in T_VALUES
    },

    "partial_sum_norms": {
        str(T): {str(N): safe(partial_sum_norms[T][N]) for N in N_CHECKPOINTS}
        for T in T_VALUES
    },
    "partial_sum_norms_unwindowed": {str(N): safe(unwindowed_norms[N]) for N in N_CHECKPOINTS},

    "residual_ratios": {
        str(T): {str(N): safe(residual_ratios[T][N]) for N in N_CHECKPOINTS}
        for T in T_VALUES
    },
    "residual_ratios_unwindowed": {str(N): safe(residual_ratios_unwindowed[N]) for N in N_CHECKPOINTS},

    "projections_onto_rhs": {
        str(T): {str(N): safe(projections_onto_rhs[T][N]) for N in N_CHECKPOINTS}
        for T in T_VALUES
    },

    "T_extrapolation_N500": {
        "T_values": safe(T_vals_arr),
        "residuals_N500": safe(res_N500),
        "power_law_fit": {
            "exponent_b": safe(b_fit),
            "coefficient_a": safe(a_fit),
            "formula": f"{a_fit:.6f} * T^{b_fit:.4f}",
            "model_type": model_type
        },
        "constant_fit": safe(c_const)
    },

    "block_decomposition_N500": {
        str(T): {
            "block_A_norm": safe(block_norms[T]['A']),
            "block_B_norm": safe(block_norms[T]['B']),
            "block_C_norm": safe(block_norms[T]['C']),
            "residual_block_A_norm": safe(block_norms[T]['residual']['A']),
            "residual_block_B_norm": safe(block_norms[T]['residual']['B']),
            "residual_block_C_norm": safe(block_norms[T]['residual']['C']),
            "total_residual_norm": safe(block_norms[T]['total_residual_norm'])
        }
        for T in T_VALUES
    },

    "convergence_rate_T100_checkpoints": {
        str(N): safe(convergence_rates[N-1]) for N in [10, 50, 100, 200, 300, 400, 450, 490]
    },

    "cailculator_sequences": {k: safe(v) for k, v in cailculator_sequences.items()},

    "key_findings": {
        "residual_ratio_at_N500": {
            str(T): safe(residual_ratios[T][500]) for T in T_VALUES
        },
        "unwindowed_N500": safe(residual_ratios_unwindowed[500]),
        "power_law_exponent": safe(b_fit),
        "model_type": model_type,
        "rhs_direction_rotation": {
            str(T): safe(rhs_T_cos_with_unwindowed[T]) for T in T_VALUES
        }
    }
}

with open('phase24_thread1_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved to phase24_thread1_results.json")
print("\n=== PHASE 24 THREAD 1 COMPLETE ===")
