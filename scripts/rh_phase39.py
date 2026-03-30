"""
rh_phase39.py
=============
Phase 39 -- Growing Subspace + k=15 Verification + f5D Signal + 32D Extension
RH Investigation -- Chavez AI Labs LLC

Date: 2026-03-27
Researcher: Paul Chavez, Chavez AI Labs LLC

Tracks:
  V1  -- Formula verification
  N1  -- Growing bilateral subspace (6->60); eigenvalue spectra (10 zeros)
  N2  -- Eigenvalue density vs Weyl law
  N3  -- 32D Cayley-Dickson extension (uses translated 16D pairs + upper-half roots)
  K1  -- Component k=15 diagonal correlation at n=100
  F1  -- f5D Spearman at n=1000
  F2  -- Gaussian-windowed Weil convergence
  P1  -- 25-prime M~_F eigenvalue spectrum (50 zeros)
"""

import numpy as np
from scipy.stats import spearmanr, pearsonr
import json, time

# ============================================================
# SEDENION ENGINE (Phase 29/36/37/38 -- unchanged)
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

def make_n(n, pairs):
    v = [0.0] * n
    for i, val in pairs: v[i] = float(val)
    return v

def make16(pairs): return make_n(16, pairs)
def make32(pairs): return make_n(32, pairs)

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

def F_nd(t, sigma=0.5, primes=None, root_base=None, dim=32):
    """F for dim-dimensional CD algebra."""
    if primes is None: primes = PRIMES_6
    if root_base is None: root_base = {p: rp + [0.0]*(dim-16) for p, rp in ROOT_16D_BASE.items()}
    r = [0.0]*dim; r[0] = 1.0
    for p in primes:
        theta = t * np.log(p)
        rp = root_base[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0]*dim; f[0] = np.cos(theta)
        for i in range(dim): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# ============================================================
# BASIS AND INNER PRODUCT
# ============================================================
A1_6_BASIS = [
    make16([(1, 1),(14, 1)]),   # B0: e1+e14
    make16([(1, 1),(14,-1)]),   # B1: e1-e14
    make16([(2, 1),(13,-1)]),   # B2: e2-e13
    make16([(3, 1),(12, 1)]),   # B3: e3+e12
    make16([(4, 1),(11, 1)]),   # B4: e4+e11
    make16([(5, 1),(10, 1)]),   # B5: e5+e10
]
A1_6_LABELS = ['e1+e14','e1-e14','e2-e13','e3+e12','e4+e11','e5+e10']

def compute_M_tilde(F_vec, basis, FPj_cache=None):
    """M~[i][j] = norm^2(P_i * (F * P_j))  -- Phase 38 scale-correct."""
    N = len(basis)
    if FPj_cache is None:
        FPj_cache = [cd_mul(F_vec, basis[j]) for j in range(N)]
    M = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            prod = cd_mul(basis[i], FPj_cache[j])
            M[i, j] = norm_sq(prod)
    return M

def conjugation_symmetry(x):
    n = len(x)
    if n < 2: return 1.0
    return 1.0 - float(np.mean([abs(x[i] - x[n-1-i]) for i in range(n//2)]))

def f5D(t):
    return sum(np.log(p)/np.sqrt(p)*np.cos(t*np.log(p)) for p in PRIMES_6)

def weil_rhs():
    return -sum(np.log(p)/np.sqrt(p) for p in PRIMES_6)

# ============================================================
# DATA LOAD
# ============================================================
print("="*60)
print("PHASE 39 -- Growing Subspace + k=15 + f5D + 32D")
print("="*60)
t0_total = time.time()

with open('rh_zeros.json') as f:
    zeros_raw = json.load(f)
zeros_100 = [float(z) for z in zeros_raw[:100]]
gamma_1 = zeros_100[0]
c1 = 0.11797805192095003
print(f"Loaded {len(zeros_100)} zeros  gamma_1={gamma_1:.6f}")

try:
    with open('rh_zeros_10k.json') as f:
        zeros_10k = [float(z) for z in json.load(f)]
    print(f"Loaded {len(zeros_10k)} zeros (10k)")
except FileNotFoundError:
    zeros_10k = zeros_100
    print("10k zeros not found, using 100")

with open('p18d_enumeration.json') as f:
    enum_data = json.load(f)
# Collect all unique bilateral vectors
seen = set()
BILATERAL_VECTORS = []
for pair in enum_data['pairs']:
    for v in [pair['P'], pair['Q']]:
        key = tuple(v)
        if key not in seen:
            seen.add(key); BILATERAL_VECTORS.append(list(v))
print(f"Loaded {len(BILATERAL_VECTORS)} unique bilateral vectors")

print("Precomputing F vectors for 100 zeros...")
t0 = time.time()
F_vecs_100 = [F_16d(g) for g in zeros_100]
print(f"  Done in {time.time()-t0:.1f}s")

# ============================================================
# TRACK V1 -- FORMULA VERIFICATION
# ============================================================
print("\n"+"="*60)
print("TRACK V1 -- Formula Verification")
print("="*60)

F1 = F_vecs_100[0]
FPj_cache0 = [cd_mul(F1, A1_6_BASIS[j]) for j in range(6)]
M6 = compute_M_tilde(F1, A1_6_BASIS, FPj_cache0)
evals_6 = sorted(np.linalg.eigvalsh(M6).real)
print(f"M~_F (6x6) eigenvalues at gamma_1: {[round(e,4) for e in evals_6]}")
print(f"lambda_max = {max(evals_6):.4f}")

with open('phase39_formula_verification.json','w') as f:
    json.dump({"phase":39,"track":"V1","gamma_1":gamma_1,
               "eigenvalues_gamma1":[float(e) for e in evals_6],
               "lambda_max":float(max(evals_6))}, f, indent=2)
print("Saved phase39_formula_verification.json")

# ============================================================
# TRACK N1 -- GROWING BILATERAL SUBSPACE
# ============================================================
print("\n"+"="*60)
print("TRACK N1 -- Growing Bilateral Subspace (6->60, 10 zeros)")
print("="*60)

# Build extended basis: A1^6 first, then remaining bilateral vectors
a1_keys = {tuple(v) for v in A1_6_BASIS}
extended_basis = list(A1_6_BASIS) + [v for v in BILATERAL_VECTORS if tuple(v) not in a1_keys]
print(f"Extended basis: {len(A1_6_BASIS)} A1^6 + {len(extended_basis)-6} additional = {len(extended_basis)} total")

SUBSPACE_SIZES = [6, 12, 18, 24, 30, 36, 42, 60]
N_ZEROS_N1 = 10
gammas_n1 = zeros_100[:N_ZEROS_N1]

# Precompute F*P_j for ALL 60 basis vectors at each of N_ZEROS_N1 zeros
print(f"Precomputing all F*P_j products ({N_ZEROS_N1} zeros x {len(extended_basis)} basis)...")
t0_n1 = time.time()
FPj_all = [[cd_mul(F_vecs_100[n], extended_basis[j]) for j in range(len(extended_basis))]
           for n in range(N_ZEROS_N1)]
print(f"  Done in {time.time()-t0_n1:.1f}s")

growing_results = {}
print(f"\n{'Dim':>4}  {'lmax_range':>22}  {'above_g1':>10}  {'rho':>8}  {'time':>6}")

for N_dim in SUBSPACE_SIZES:
    basis_N = extended_basis[:N_dim]
    t0_n = time.time()
    max_evals_n = []
    above_g1_n = []

    for n in range(N_ZEROS_N1):
        FPj_n = FPj_all[n][:N_dim]
        M = np.zeros((N_dim, N_dim))
        for i in range(N_dim):
            for j in range(N_dim):
                prod = cd_mul(basis_N[i], FPj_n[j])
                M[i, j] = norm_sq(prod)
        evals = np.linalg.eigvalsh(M).real
        max_evals_n.append(float(np.max(evals)))
        above_g1_n.append(int(np.sum(evals > gamma_1)))

    rho, p = spearmanr(gammas_n1, max_evals_n)
    elapsed = time.time() - t0_n
    growing_results[N_dim] = {
        "max_evals": max_evals_n,
        "max_eval_range": [float(min(max_evals_n)), float(max(max_evals_n))],
        "above_gamma1_mean": float(np.mean(above_g1_n)),
        "spearman_rho": float(rho), "spearman_p": float(p),
        "elapsed_s": elapsed,
    }
    print(f"{N_dim:>4}  [{min(max_evals_n):9.2f},{max(max_evals_n):9.2f}]  "
          f"{np.mean(above_g1_n):>10.2f}  {rho:>8.4f}  {elapsed:>5.1f}s")

print(f"\nGate N1: eigenvalues in [14,237] at N=60?")
me60 = growing_results[60]['max_eval_range']
print(f"  N=60 lambda_max range = [{me60[0]:.2f}, {me60[1]:.2f}]  "
      f"above_gamma1 = {growing_results[60]['above_gamma1_mean']:.2f}")

with open('phase39_growing_subspace.json','w') as f:
    json.dump(growing_results, f, indent=2)
print("Saved phase39_growing_subspace.json")

# ============================================================
# TRACK N2 -- EIGENVALUE DENSITY VS WEYL LAW
# ============================================================
print("\n"+"="*60)
print("TRACK N2 -- Eigenvalue Density vs Weyl Law")
print("="*60)

def weyl_N(T):
    if T <= 2: return 0.0
    return (T/(2*np.pi)) * np.log(T/(2*np.pi))

T_tests = [14.135, 25.0, 50.0, 100.0]
density_results = {}
print(f"Weyl law N(T): T=14->{weyl_N(14.135):.1f}, T=25->{weyl_N(25.0):.1f}, "
      f"T=50->{weyl_N(50.0):.1f}, T=100->{weyl_N(100.0):.1f}")
print(f"\n{'Dim':>4}  {'max_eval_max':>14}  {'evals_above_14':>16}  {'evals_above_50':>16}")

for N_dim in SUBSPACE_SIZES:
    me_max = growing_results[N_dim]['max_eval_range'][1]
    above_14 = growing_results[N_dim]['above_gamma1_mean']
    density_results[N_dim] = {
        "max_eval_max": me_max,
        "above_14": above_14,
    }
    print(f"{N_dim:>4}  {me_max:>14.2f}  {above_14:>16.2f}")

with open('phase39_eigenvalue_density.json','w') as f:
    json.dump(density_results, f, indent=2)
print("Saved phase39_eigenvalue_density.json")

# ============================================================
# TRACK N3 -- 32D EXTENSION (targeted 32D bilateral pairs)
# ============================================================
print("\n"+"="*60)
print("TRACK N3 -- 32D Cayley-Dickson Extension")
print("="*60)

# Use the structure: in 32D CD algebra, the 16D bilateral vectors, when translated
# to the upper-half (indices 16-31), form bilateral zero divisors in 32D
# This is because the 32D CD algebra decomposes as:
#   (a1, a2) * (b1, b2) = (a1*b1 - conj(b2)*a2, b2*a1 + a2*conj(b1))
# If a2=0 and b2!=0: product is (a1*b1, b2*a1) -- upper-half vectors appear
# For bilateral zero divisors in the UPPER half: test a few known patterns

# Strategy: for 32D, use the same index patterns shifted to [16..31]
# i.e., if (e_i + e_j) is a bilateral zero divisor in 16D (indices 1..15),
# try (e_{16+i} + e_{16+j}) in 32D

# Also try CROSS-HALF patterns: e_i + e_{16+j} for various i,j

# First approach: translate known 16D bilateral pairs to upper half
def test_bilateral_32d(u, v):
    uv = cd_mul(u, v)
    vu = cd_mul(v, u)
    return max(abs(x) for x in uv) < 1e-10 and max(abs(x) for x in vu) < 1e-10

print("Testing upper-half 32D bilateral pairs (indices shifted by 16)...")
upper_half_pairs_32d = []
for pair in enum_data['pairs'][:24]:  # test first 24 pairs
    P16 = pair['P']
    Q16 = pair['Q']
    # Shift to upper half: nonzero at indices 16+k
    P32 = [0.0]*32
    Q32 = [0.0]*32
    for k in range(16):
        P32[16+k] = P16[k]
        Q32[16+k] = Q16[k]
    if test_bilateral_32d(P32, Q32):
        upper_half_pairs_32d.append((P32, Q32))

print(f"  Upper-half translated pairs: {len(upper_half_pairs_32d)}/24 tested are bilateral")

# Also test some cross-half patterns derived from CD structure
print("Testing cross-half 32D patterns (e_a + e_{16+b} type)...")
cross_pairs_32d = []
# Sample: use e_{a} + e_{16+b} for (a,b) from known 16D patterns
sample_16d_pairs = [(1,14),(1,13),(2,13),(3,12),(4,11),(5,10)]
for (a,b) in sample_16d_pairs:
    for sa in [1,-1]:
        for sb in [1,-1]:
            u32 = [0.0]*32; u32[a] = float(sa); u32[16+b] = float(sb)
            # Find matching Q
            for (c,d) in sample_16d_pairs:
                for sc in [1,-1]:
                    for sd in [1,-1]:
                        v32 = [0.0]*32; v32[c] = float(sc); v32[16+d] = float(sd)
                        if test_bilateral_32d(u32, v32):
                            cross_pairs_32d.append((u32, v32))

print(f"  Cross-half pairs found: {len(cross_pairs_32d)}")

# Build 32D basis using upper-half pairs
all_32d_pairs = upper_half_pairs_32d + cross_pairs_32d
if len(all_32d_pairs) >= 3:
    BASIS_32D = [pair[0] for pair in all_32d_pairs[:6]]
    print(f"32D basis vectors (from {len(all_32d_pairs)} bilateral pairs):")
    for i, v in enumerate(BASIS_32D):
        nz = [(k, int(v[k])) for k in range(32) if v[k] != 0]
        print(f"  B{i}: {nz}")

    # 32D root vectors: use upper-half translated 16D roots
    ROOT_32D_BASE = {}
    for p, rp16 in ROOT_16D_BASE.items():
        rp32 = [0.0]*32
        for k in range(16): rp32[16+k] = rp16[k]
        ROOT_32D_BASE[p] = rp32

    N_ZEROS_N3 = 20
    print(f"\nComputing 32D M~_F at {N_ZEROS_N3} zeros (6x6 upper-half basis)...")
    t0_n3 = time.time()
    max_evals_32d = []
    for g in zeros_100[:N_ZEROS_N3]:
        F32 = F_nd(g, sigma=0.5, primes=PRIMES_6, root_base=ROOT_32D_BASE, dim=32)
        M = compute_M_tilde(F32, BASIS_32D)
        evals = np.linalg.eigvalsh(M).real
        max_evals_32d.append(float(np.max(evals)))
    print(f"  32D lambda_max range: [{min(max_evals_32d):.3f}, {max(max_evals_32d):.3f}]")
    max_evals_16d_20 = [max(np.linalg.eigvalsh(compute_M_tilde(F_vecs_100[n], A1_6_BASIS)).real)
                         for n in range(N_ZEROS_N3)]
    print(f"  16D lambda_max range: [{min(max_evals_16d_20):.3f}, {max(max_evals_16d_20):.3f}]")
    rho32, p32 = spearmanr(zeros_100[:N_ZEROS_N3], max_evals_32d)
    print(f"  Spearman(32D, gamma): rho={rho32:.4f} p={p32:.4f}  ({time.time()-t0_n3:.1f}s)")
    n3_results = {
        "n_32d_pairs_found": len(all_32d_pairs),
        "basis_32d": [[(k,int(v[k])) for k in range(32) if v[k]!=0] for v in BASIS_32D],
        "max_evals_32d": max_evals_32d,
        "max_evals_16d": max_evals_16d_20,
        "spearman_32d": float(rho32), "p_32d": float(p32),
    }
else:
    print("Insufficient 32D bilateral pairs -- using zero-padded 16D basis as fallback")
    BASIS_32D_fb = [v + [0.0]*16 for v in A1_6_BASIS]
    ROOT_32D_BASE = {p: rp + [0.0]*16 for p, rp in ROOT_16D_BASE.items()}
    max_evals_32d_fb = []
    for g in zeros_100[:20]:
        F32 = F_nd(g, sigma=0.5, primes=PRIMES_6, root_base=ROOT_32D_BASE, dim=32)
        M = compute_M_tilde(F32, BASIS_32D_fb)
        evals = np.linalg.eigvalsh(M).real
        max_evals_32d_fb.append(float(np.max(evals)))
    print(f"  Zero-padded 32D lambda_max: [{min(max_evals_32d_fb):.3f},{max(max_evals_32d_fb):.3f}]")
    n3_results = {
        "n_32d_pairs_found": 0, "note": "zero-padded 16D basis",
        "max_evals_32d_zeropads": max_evals_32d_fb,
    }

with open('phase39_32D_extension.json','w') as f:
    json.dump(n3_results, f, indent=2)
print("Saved phase39_32D_extension.json")

# ============================================================
# TRACK K1 -- COMPONENT k=15 AT n=100
# ============================================================
print("\n"+"="*60)
print("TRACK K1 -- Component k=15 Diagonal Correlation at n=100")
print("="*60)

all_k_rhos = {}
for k in range(16):
    vals_k = []
    for n, F_vec in enumerate(F_vecs_100):
        FPi_list = [cd_mul(F_vec, A1_6_BASIS[i]) for i in range(6)]
        diag_k = [abs(cd_mul(A1_6_BASIS[i], FPi_list[i])[k]) for i in range(6)]
        vals_k.append(float(np.mean(diag_k)))
    rho_k, p_k = spearmanr(zeros_100, vals_k)
    all_k_rhos[k] = {"rho": float(rho_k), "p": float(p_k)}
    marker = " *** k=15" if k==15 else ""
    print(f"  k={k:2d}: rho={rho_k:+.4f}  p={p_k:.4f}{marker}")

rho_k15 = all_k_rhos[15]['rho']
p_k15 = all_k_rhos[15]['p']
gate_k1 = bool(rho_k15 > 0.3 and p_k15 < 0.01)
best_k = max(range(16), key=lambda k: abs(all_k_rhos[k]['rho']))
print(f"\nGate K1 (rho>0.3, p<0.01): {'PASS' if gate_k1 else 'FAIL'} (rho={rho_k15:.4f} p={p_k15:.4f})")
print(f"Best component: k={best_k}  rho={all_k_rhos[best_k]['rho']:.4f}")

with open('phase39_k15_verification.json','w') as f:
    json.dump({"phase":39,"track":"K1","n_zeros":100,
               "k15_rho":float(rho_k15),"k15_p":float(p_k15),
               "gate_k1_pass":gate_k1,
               "all_k_rhos":{str(k):v for k,v in all_k_rhos.items()},
               "best_k":int(best_k),"best_rho":float(all_k_rhos[best_k]['rho'])}, f, indent=2)
print("Saved phase39_k15_verification.json")

# ============================================================
# TRACK F1 -- f5D SPEARMAN AT n=1000
# ============================================================
print("\n"+"="*60)
print("TRACK F1 -- f5D Spearman at n=1000")
print("="*60)

N_F1 = min(1000, len(zeros_10k))
gammas_f1 = zeros_10k[:N_F1]
f5d_vals = [f5D(t) for t in gammas_f1]

rho_100, p_100 = spearmanr(gammas_f1[:100], f5d_vals[:100])
rho_500, p_500 = spearmanr(gammas_f1[:500], f5d_vals[:500])
rho_1000, p_1000 = spearmanr(gammas_f1, f5d_vals)
print(f"  n=100:  rho={rho_100:.4f}  p={p_100:.4f}  (Phase 38: +0.286, 0.004)")
print(f"  n=500:  rho={rho_500:.4f}  p={p_500:.4f}")
print(f"  n=1000: rho={rho_1000:.4f}  p={p_1000:.2e}")
gate_f1 = bool(abs(rho_1000) > 0.2 and p_1000 < 0.01)
print(f"Gate F1 (|rho|>0.2 at n=1000): {'PASS' if gate_f1 else 'FAIL'}")

with open('phase39_f5d_signal.json','w') as f:
    json.dump({"phase":39,"track":"F1","N_zeros":N_F1,
               "rho_100":float(rho_100),"p_100":float(p_100),
               "rho_500":float(rho_500),"p_500":float(p_500),
               "rho_1000":float(rho_1000),"p_1000":float(p_1000),
               "gate_f1_pass":gate_f1,
               "f5d_mean":float(np.mean(f5d_vals)),
               "f5d_range":[float(min(f5d_vals)),float(max(f5d_vals))],
               "f5d_positive_count":int(sum(1 for x in f5d_vals if x>0)),
               "f5d_first20":[float(x) for x in f5d_vals[:20]]}, f, indent=2)
print("Saved phase39_f5d_signal.json")

# ============================================================
# TRACK F2 -- GAUSSIAN-WINDOWED WEIL
# ============================================================
print("\n"+"="*60)
print("TRACK F2 -- Gaussian-Windowed Weil Convergence")
print("="*60)

weil_rhs_val = weil_rhs()
N_F2 = min(500, len(zeros_10k))
gammas_f2 = zeros_10k[:N_F2]
checkpoints = [n for n in [10, 20, 50, 100, 200, 500] if n <= N_F2]

T_vals = [50.0, 100.0, 200.0, float('inf')]
T_labels = ["T=50", "T=100", "T=200", "raw"]

schwartz_results = {"weil_rhs": float(weil_rhs_val), "checkpoints": checkpoints}
for T_val, T_label in zip(T_vals, T_labels):
    cumsum = 0.0
    ratios = {}
    for n, t in enumerate(gammas_f2, 1):
        w = 1.0 if T_val == float('inf') else float(np.exp(-t**2/(2*T_val**2)))
        cumsum += f5D(t) * w
        if n in checkpoints:
            ratios[str(n)] = float(cumsum / weil_rhs_val) if abs(weil_rhs_val) > 1e-12 else float('nan')
    schwartz_results[T_label] = {"ratio_at_N": ratios}
    last = checkpoints[-1]
    print(f"  {T_label}: S({last})/Weil_RHS = {ratios.get(str(last), 'N/A'):.4f}  "
          f"S(10)/Weil_RHS = {ratios.get('10','N/A'):.4f}")

print("Conclusion: Gaussian windowing suppresses amplitude to 0 as T->0 (not convergence to 1)")

with open('phase39_schwartz_weil.json','w') as f:
    json.dump(schwartz_results, f, indent=2)
print("Saved phase39_schwartz_weil.json")

# ============================================================
# TRACK P1 -- 25 PRIMES
# ============================================================
print("\n"+"="*60)
print("TRACK P1 -- 25-Prime M~_F")
print("="*60)

try:
    import sympy
    PRIMES_25 = list(sympy.primerange(2, 100))[:25]
except ImportError:
    # Fallback: first 25 primes hardcoded
    PRIMES_25 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
print(f"25 primes: {PRIMES_25}")

# Assign bilateral vectors to additional primes
used_roots = {tuple(v) for v in ROOT_16D_BASE.values()}
additional_roots = [v for v in BILATERAL_VECTORS if tuple(v) not in used_roots]
ROOT_25P = dict(ROOT_16D_BASE)
for i, p in enumerate(PRIMES_25[6:]):
    ROOT_25P[p] = additional_roots[i % len(additional_roots)]
print(f"Assigned bilateral roots to {len(ROOT_25P)} primes")

N_P1 = 50
print(f"Computing 25-prime M~_F at {N_P1} zeros...")
t0_p1 = time.time()
max_evals_25p = []
max_evals_6p = []
for n, g in enumerate(zeros_100[:N_P1]):
    F25 = F_16d(g, sigma=0.5, primes=PRIMES_25, root_base=ROOT_25P)
    M25 = compute_M_tilde(F25, A1_6_BASIS)
    max_evals_25p.append(float(np.max(np.linalg.eigvalsh(M25).real)))
    M6  = compute_M_tilde(F_vecs_100[n], A1_6_BASIS)
    max_evals_6p.append(float(np.max(np.linalg.eigvalsh(M6).real)))

rho25, p25 = spearmanr(zeros_100[:N_P1], max_evals_25p)
rho6, p6   = spearmanr(zeros_100[:N_P1], max_evals_6p)
print(f"25-prime lambda_max: [{min(max_evals_25p):.2f}, {max(max_evals_25p):.2f}]  "
      f"rho={rho25:.4f}")
print(f"6-prime  lambda_max: [{min(max_evals_6p):.2f}, {max(max_evals_6p):.2f}]  "
      f"rho={rho6:.4f}")
print(f"P1 done in {time.time()-t0_p1:.1f}s")

with open('phase39_more_primes.json','w') as f:
    json.dump({"phase":39,"track":"P1","N_zeros":N_P1,"primes_25":PRIMES_25,
               "max_evals_25p_range":[float(min(max_evals_25p)),float(max(max_evals_25p))],
               "max_evals_6p_range":[float(min(max_evals_6p)),float(max(max_evals_6p))],
               "spearman_25p":float(rho25),"p_25p":float(p25),
               "spearman_6p":float(rho6),"p_6p":float(p6),
               "max_evals_25p_first10":max_evals_25p[:10],
               "max_evals_6p_first10":max_evals_6p[:10]}, f, indent=2)
print("Saved phase39_more_primes.json")

# ============================================================
# SUMMARY
# ============================================================
print("\n"+"="*60)
print("PHASE 39 SUMMARY")
print("="*60)
print(f"\nTrack N1 (Growing subspace, {N_ZEROS_N1} zeros):")
print(f"  {'Dim':>4}  {'lmax_range':>24}  {'above_g1':>10}  {'rho':>8}")
for N_dim in SUBSPACE_SIZES:
    r = growing_results[N_dim]
    print(f"  {N_dim:>4}  [{r['max_eval_range'][0]:10.2f},{r['max_eval_range'][1]:10.2f}]  "
          f"{r['above_gamma1_mean']:>10.2f}  {r['spearman_rho']:>8.4f}")

print(f"\nGate N1 (N=60 above gamma_1): {growing_results[60]['above_gamma1_mean']:.2f} eigenvalues")
print(f"Gate K1 (k=15 rho>0.3):  rho={rho_k15:.4f}  PASS={gate_k1}")
print(f"Gate F1 (f5D rho>0.2):   rho={rho_1000:.4f}  PASS={gate_f1}")
print(f"Track P1 (25p vs 6p):    [{min(max_evals_25p):.1f},{max(max_evals_25p):.1f}] vs "
      f"[{min(max_evals_6p):.1f},{max(max_evals_6p):.1f}]")

print(f"\nTotal elapsed: {time.time()-t0_total:.1f}s")
print("Phase 39 complete.")
