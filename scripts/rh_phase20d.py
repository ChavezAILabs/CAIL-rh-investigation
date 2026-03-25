"""
Phase 20D: Near-Miss Pair Analysis -- Diophantine Structure
Chavez AI Labs LLC -- March 24, 2026

Target pairs:
  6-prime: rho_54 (t ~ 153.025) & rho_98 (t ~ 232.337), |cos theta| = 0.9928
  9-prime: rho_42 & rho_95, |cos theta| = 0.9964 (secondary)

Core question:
  cos(t_i * log p) / cos(t_j * log p) = constant lambda for ALL primes p?
  -- 5 constraints in 2 unknowns, generically overdetermined
  -- Near-proportionality means ratios are NEARLY constant

Analysis:
  1. Ratio table + spread (max - min ratio across primes)
  2. (t_i - t_j) / log p -- near-rational? (Diophantine near-miss)
  3. Block failure mode -- which block drives near-proportionality?
  4. Comparison to generic pair (|cos theta| ~ 0.5)
  5. Actual f5D vectors side by side
"""

import json
import numpy as np
from fractions import Fraction

# ── Load zeros from rh_zeros.json (1000 zeros, 0-indexed) ────────────────────
# rho_n = 1/2 + i*t_n; rh_zeros.json[n-1] = t_n
with open('rh_zeros.json', 'r') as f:
    zeros_list = json.load(f)   # list of floats, 0-indexed

def t(n):
    """Return imaginary part of n-th Riemann zero (1-indexed)."""
    return zeros_list[n - 1]

# Headline pair (6-prime near-miss from Phase 20C)
t54 = t(54)
t98 = t(98)

# Secondary pair (9-prime near-miss from Phase 20C)
t42 = t(42)
t95 = t(95)

# Build dict for later use
zeros_by_n = {n+1: zeros_list[n] for n in range(len(zeros_list))}

print(f"Zeros loaded from phase20c_results.json")
print(f"t_54 = {t54:.15f}")
print(f"t_98 = {t98:.15f}")
print(f"t_42 = {t42:.15f}")
print(f"t_95 = {t95:.15f}")

# ── Embedding setup (identical to Phase 20B/20C) ─────────────────────────────
sqrt2 = np.sqrt(2.0)
TWO_PI = 2.0 * np.pi

# 6D basis: [e2, e7, e3, e6, e4, e5]
# Prime-to-root assignment
R = {
    2:  np.array([0.,  0.,  0.,  0.,  1.,  1.]) / sqrt2,  # q4
    3:  np.array([0.,  0., -1.,  1.,  0.,  0.]) / sqrt2,  # q2
    5:  np.array([0.,  0.,  1.,  1.,  0.,  0.]) / sqrt2,  # v5
    7:  np.array([1., -1.,  0.,  0.,  0.,  0.]) / sqrt2,  # v1
    11: np.array([1.,  1.,  0.,  0.,  0.,  0.]) / sqrt2,  # v4
    13: np.array([-1., 1.,  0.,  0.,  0.,  0.]) / sqrt2,  # q3
}

PRIMES_6 = [2, 3, 5, 7, 11, 13]
BLOCK = {
    'A': [7, 11, 13],   # {e2, e7}
    'B': [3, 5],        # {e3, e6} -- Heegner channel
    'C': [2],           # {(e4+e5)/sqrt2}
}

def f5D(t, primes=PRIMES_6):
    out = np.zeros(6)
    for p in primes:
        out += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * R[p]
    return out

def abs_cos_theta(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-12 or n2 < 1e-12:
        return float('nan')
    return abs(np.dot(v1, v2) / (n1 * n2))


# ── Analysis function ─────────────────────────────────────────────────────────
def analyze_pair(t_i, t_j, n_i, n_j, primes=PRIMES_6):
    delta_t = t_i - t_j
    logps = [np.log(p) for p in primes]

    # 1. Ratio table: cos(t_i * log p) / cos(t_j * log p)
    cos_i_vals = {p: np.cos(t_i * np.log(p)) for p in primes}
    cos_j_vals = {p: np.cos(t_j * np.log(p)) for p in primes}

    ratios = {}
    for p in primes:
        cj = cos_j_vals[p]
        if abs(cj) > 1e-10:
            ratios[p] = cos_i_vals[p] / cj
        else:
            ratios[p] = float('nan')

    valid_ratios = [r for r in ratios.values() if not np.isnan(r)]
    ratio_mean = np.mean(valid_ratios) if valid_ratios else float('nan')
    ratio_spread = max(valid_ratios) - min(valid_ratios) if len(valid_ratios) > 1 else float('nan')

    # 2. (t_i - t_j) / log p and fractional parts
    dt_over_logp = {p: delta_t / np.log(p) for p in primes}
    frac_parts = {p: dt_over_logp[p] - round(dt_over_logp[p]) for p in primes}

    # 3. Block analysis: spread within each block
    block_spreads = {}
    block_ratios = {}
    for block_name, block_primes in BLOCK.items():
        bp = [p for p in block_primes if p in primes]
        if not bp:
            continue
        br = [ratios[p] for p in bp if not np.isnan(ratios[p])]
        block_ratios[block_name] = br
        block_spreads[block_name] = max(br) - min(br) if len(br) > 1 else 0.0

    # 4. Actual f5D vectors
    v_i = f5D(t_i, primes)
    v_j = f5D(t_j, primes)
    ct = abs_cos_theta(v_i, v_j)

    # 5. Best rational approximations of |delta_t| / log p
    def best_rationals(x, max_denom=200):
        best = []
        for d in range(1, max_denom + 1):
            n = round(x * d)
            err = abs(x * d - n)
            best.append((d, n, err))
        best.sort(key=lambda x: x[2])
        return best[:5]

    rat_approx = {}
    for p in primes:
        val = abs(delta_t) / np.log(p)
        rat_approx[p] = best_rationals(val)

    return {
        'n_i': n_i, 'n_j': n_j,
        't_i': t_i, 't_j': t_j,
        'delta_t': delta_t,
        'abs_cos_theta': ct,
        'ratios': ratios,
        'ratio_mean': ratio_mean,
        'ratio_spread': ratio_spread,
        'dt_over_logp': dt_over_logp,
        'frac_parts': frac_parts,
        'block_spreads': block_spreads,
        'block_ratios': block_ratios,
        'v_i': v_i.tolist(),
        'v_j': v_j.tolist(),
        'rat_approx': rat_approx,
    }


def print_pair_analysis(result, label):
    r = result
    n_i, n_j = r['n_i'], r['n_j']
    t_i, t_j = r['t_i'], r['t_j']
    delta_t = r['delta_t']
    primes = PRIMES_6  # will use whatever primes are in ratios

    print(f"\n{'='*65}")
    print(f"  {label}: rho_{n_i} & rho_{n_j}")
    print(f"  t_{n_i} = {t_i:.12f}")
    print(f"  t_{n_j} = {t_j:.12f}")
    print(f"  Delta_t = {delta_t:.12f}")
    print(f"  |cos theta| = {r['abs_cos_theta']:.10f}")
    print(f"{'='*65}")

    # Ratio table
    print(f"\n--- 1. Ratio table: cos(t_{n_i}*log p) / cos(t_{n_j}*log p) ---")
    print(f"{'Prime':>6}  {'Block':>6}  {'cos_i':>12}  {'cos_j':>12}  {'ratio':>12}")
    print("-" * 55)
    prime_to_block = {}
    for bname, bprimes in BLOCK.items():
        for p in bprimes:
            prime_to_block[p] = bname
    for p, ratio in r['ratios'].items():
        ci = np.cos(t_i * np.log(p))
        cj = np.cos(t_j * np.log(p))
        bname = prime_to_block.get(p, '?')
        print(f"{p:>6}  {bname:>6}  {ci:>12.8f}  {cj:>12.8f}  {ratio:>12.8f}")
    print(f"\n  Lambda (mean ratio)   = {r['ratio_mean']:>12.8f}")
    print(f"  Spread (max-min)      = {r['ratio_spread']:>12.8f}  <<< KEY: how close to 0?")

    # Block analysis
    print(f"\n--- 3. Block failure mode ---")
    for bname, spread in r['block_spreads'].items():
        brats = r['block_ratios'][bname]
        mean_br = np.mean(brats) if brats else float('nan')
        tag = " <<< TIGHTEST" if spread == min(r['block_spreads'].values()) else ""
        print(f"  Block {bname}: spread={spread:.8f}  mean_ratio={mean_br:.8f}{tag}")

    # Diophantine structure
    print(f"\n--- 2. Diophantine structure: |Delta_t| / log p ---")
    print(f"  |Delta_t| = {abs(delta_t):.12f}")
    print(f"{'Prime':>6}  {'|Dt|/log p':>14}  {'frac(Dt/logp)':>15}  {'best_approx':>12}  {'error':>10}")
    print("-" * 62)
    for p in r['dt_over_logp']:
        val = abs(r['dt_over_logp'][p])
        frac = r['frac_parts'][p]
        rat = r['rat_approx'][p][0]  # (denom, numer, error)
        # numer/denom approximates |Dt|/logp
        print(f"{p:>6}  {val:>14.8f}  {frac:>+15.8f}  "
              f"{rat[1]:>5}/{rat[0]:<5}  {rat[2]:>10.2e}")

    # Vectors side by side
    print(f"\n--- 5. f5D vectors side by side ---")
    v_i = np.array(r['v_i'])
    v_j = np.array(r['v_j'])
    comp_names = ['e2', 'e7', 'e3', 'e6', 'e4', 'e5']
    print(f"{'Comp':>5}  {'f5D(t_i)':>14}  {'f5D(t_j)':>14}  {'ratio':>12}")
    print("-" * 50)
    for k, cname in enumerate(comp_names):
        ci = v_i[k]
        cj = v_j[k]
        ratio = ci / cj if abs(cj) > 1e-10 else float('nan')
        print(f"{cname:>5}  {ci:>14.8f}  {cj:>14.8f}  {ratio:>12.8f}")
    print(f"  ||v_i|| = {np.linalg.norm(v_i):.8f}  ||v_j|| = {np.linalg.norm(v_j):.8f}")


# ── Run analyses ──────────────────────────────────────────────────────────────
print("\n" + "="*65)
print("PHASE 20D: Near-Miss Pair Analysis")
print("Chavez AI Labs LLC -- March 24, 2026")
print("="*65)

# Headline pair: rho_54 & rho_98 (6-prime)
r_main = analyze_pair(t54, t98, 54, 98)
print_pair_analysis(r_main, "HEADLINE 6-prime near-miss")

# Secondary pair: rho_42 & rho_95 (6-prime formula)
r_sec = analyze_pair(t42, t95, 42, 95)
print_pair_analysis(r_sec, "SECONDARY 9-prime alert pair (6-prime formula)")

# Generic reference pair: find one with |cos theta| ~ 0.5
# Use rho_1 & rho_4 from phase20b (known to be moderate)
t1 = zeros_by_n[1]
t4 = zeros_by_n[4]
t5 = zeros_by_n[5]
t10 = zeros_by_n[10]

# Check a few to find |cos theta| ~ 0.5
candidates = [(1,4), (1,5), (4,10), (5,10), (2,7), (3,10)]
best_ref = None
best_ref_ct = 1.0
for (a,b) in candidates:
    va = f5D(zeros_by_n[a])
    vb = f5D(zeros_by_n[b])
    ct = abs_cos_theta(va, vb)
    if abs(ct - 0.5) < abs(best_ref_ct - 0.5):
        best_ref = (a, b)
        best_ref_ct = ct
print(f"\nSelected reference pair: rho_{best_ref[0]} & rho_{best_ref[1]}, |cos theta| = {best_ref_ct:.4f}")

r_ref = analyze_pair(zeros_by_n[best_ref[0]], zeros_by_n[best_ref[1]], best_ref[0], best_ref[1])
print_pair_analysis(r_ref, f"REFERENCE generic pair (|cos theta| ~ 0.5)")

# ── Comparison summary ────────────────────────────────────────────────────────
print("\n" + "="*65)
print("COMPARISON SUMMARY")
print("="*65)
print(f"\n{'Pair':>25}  {'|cos theta|':>12}  {'Ratio spread':>14}  {'Tightest block':>15}")
print("-" * 72)

def tightest_block(r):
    if not r['block_spreads']:
        return 'N/A'
    return min(r['block_spreads'], key=r['block_spreads'].get)

pairs = [
    (f"rho_{r_main['n_i']} & rho_{r_main['n_j']} (6p)", r_main),
    (f"rho_{r_sec['n_i']}  & rho_{r_sec['n_j']}  (6p)", r_sec),
    (f"rho_{r_ref['n_i']}  & rho_{r_ref['n_j']}   (ref)", r_ref),
]
for plabel, rr in pairs:
    print(f"{plabel:>25}  {rr['abs_cos_theta']:>12.8f}  "
          f"{rr['ratio_spread']:>14.8f}  {tightest_block(rr):>15}")

print(f"\nKey insight: near-miss pair ratio spread ({r_main['ratio_spread']:.6f}) vs "
      f"reference ({r_ref['ratio_spread']:.6f})")
print(f"  Compression factor: {r_ref['ratio_spread'] / r_main['ratio_spread']:.1f}x tighter in near-miss")

# ── Save results ──────────────────────────────────────────────────────────────
def make_serializable(obj):
    if isinstance(obj, dict):
        return {str(k): make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    elif isinstance(obj, float):
        return obj if not (np.isnan(obj) or np.isinf(obj)) else None
    elif isinstance(obj, np.floating):
        v = float(obj)
        return v if not (np.isnan(v) or np.isinf(v)) else None
    elif isinstance(obj, np.integer):
        return int(obj)
    else:
        return obj

output = {
    'experiment': 'Phase20D_NearMiss_Diophantine',
    'date': '2026-03-24',
    'headline_pair_rho54_rho98': make_serializable(r_main),
    'secondary_pair_rho42_rho95': make_serializable(r_sec),
    'reference_pair': make_serializable(r_ref),
}

with open('phase20d_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to phase20d_results.json")
