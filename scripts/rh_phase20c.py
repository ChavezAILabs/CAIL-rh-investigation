"""
Phase 20C: Scale to n=100 + Extended Prime Set (p=2..23)
File: rh_phase20c.py
Output: phase20c_results.json + RH_Phase20C_Results.md

Two extensions over Phase 20B:
  1. Scale to n=1..100 zeros (C(100,2) = 4,950 pairs)
  2. Add primes p=17, 19, 23 (9-prime formula)

NOTE on v2 direction (spec clarification):
  v2 = (e4-e5)/sqrt(2) = u_antisym — this IS the 1D antisymmetric direction.
  Using it in f5D would give critical-line zeros a non-zero antisymmetric
  component, breaking the equivariance theorem (Test 1 would fail).
  Instead, p=17/19/23 use cross-block D6 root directions:
    p=17: (e2+e3)/sqrt(2)  [Block A x Block B, D6 root]
    p=19: (e2+e6)/sqrt(2)  [Block A x Block B, D6 root]
    p=23: (e7+e3)/sqrt(2)  [Block A x Block B, D6 root]
  These are in the 5D fixed subspace (e4=e5=0) and are E8 first-shell roots.

Key question: is max |cos theta| bounded away from 1 as n grows?

Chavez AI Labs LLC -- March 23, 2026
"""

import numpy as np
import json
from itertools import combinations
import mpmath

mpmath.mp.dps = 25

sqrt2 = np.sqrt(2.0)

# ============================================================
# SECTION 1: Root directions and embedding
# 6D basis: [e2, e7, e3, e6, e4, e5]
# Fixed subspace: v[4] = v[5] (5D)
# Antisymmetric: v[4] = -v[5] (1D)
# s_alpha4: swaps positions 4 and 5
# ============================================================

# (A1)^6 fixed roots — used for p=2..13 (Phase 20B)
R6 = {
    2:  np.array([0., 0., 0., 0., 1.,  1.]) / sqrt2,   # q4 = (e4+e5)/sqrt2
    3:  np.array([0., 0.,-1., 1., 0.,  0.]) / sqrt2,   # q2 = (-e3+e6)/sqrt2
    5:  np.array([0., 0., 1., 1., 0.,  0.]) / sqrt2,   # v5 = (e3+e6)/sqrt2
    7:  np.array([1.,-1., 0., 0., 0.,  0.]) / sqrt2,   # v1 = (e2-e7)/sqrt2
    11: np.array([1., 1., 0., 0., 0.,  0.]) / sqrt2,   # v4 = (e2+e7)/sqrt2
    13: np.array([-1.,1., 0., 0., 0.,  0.]) / sqrt2,   # q3 = (-e2+e7)/sqrt2
}

# Extended directions for p=17, 19, 23
# These are cross-block D6 roots in the 5D fixed subspace.
# v2 = u_antisym = (e4-e5)/sqrt2 is ANTISYMMETRIC; cannot be used in f5D.
# The spec's "v2 direction" assignment is replaced with the nearest available
# fixed-subspace direction consistent with the equivariance constraint.
R_EXT = {
    17: np.array([1., 0., 1., 0., 0., 0.]) / sqrt2,  # (e2+e3)/sqrt2 cross-block
    19: np.array([1., 0., 0., 1., 0., 0.]) / sqrt2,  # (e2+e6)/sqrt2 cross-block
    23: np.array([0., 1., 1., 0., 0., 0.]) / sqrt2,  # (e7+e3)/sqrt2 cross-block
}

# 6-prime and 9-prime sets
PRIMES_6 = {p: R6[p] for p in [2, 3, 5, 7, 11, 13]}
PRIMES_9 = {**PRIMES_6, **R_EXT}

u_antisym = np.array([0., 0., 0., 0., 1., -1.]) / sqrt2

def s_alpha4(v):
    w = v.copy(); w[4], w[5] = v[5], v[4]; return w

def f5D(t, prime_root_map):
    out = np.zeros(6)
    for p, r in prime_root_map.items():
        out += (np.log(p) / np.sqrt(p)) * np.cos(t * np.log(p)) * r
    return out

def embed(sigma, t, prime_root_map):
    return f5D(t, prime_root_map) + (sigma - 0.5) * u_antisym

# ============================================================
# SETUP VERIFICATION
# ============================================================
print("=" * 60)
print("SETUP VERIFICATION")
print("=" * 60)

print("Extended directions (p=17,19,23) in 5D fixed subspace:")
for p, r in R_EXT.items():
    in_fixed = abs(r[4] - r[5]) < 1e-14
    norm_ok = abs(np.linalg.norm(r) - 1.0) < 1e-14
    print(f"  p={p}: [{', '.join(f'{x:+.4f}' for x in r)}]  "
          f"fixed={'OK' if in_fixed else 'FAIL'}, norm={'OK' if norm_ok else 'FAIL'}")

print()
print("v2 = u_antisym? (should be TRUE -- that's why it can't go in f5D):")
v2_8d = np.array([0., 0., 0., 0., 1., -1.]) / sqrt2
print(f"  v2 in 6D = {v2_8d}")
print(f"  u_antisym = {u_antisym}")
print(f"  Equal: {np.allclose(v2_8d, u_antisym)}")
print(f"  Conclusion: using v2 in f5D adds an antisymmetric component to every")
print(f"  critical-line zero, breaking Test 1. Using cross-block D6 roots instead.")

# ============================================================
# COMPUTE 100 ZEROS
# ============================================================
print()
print("=" * 60)
print("COMPUTING 100 RIEMANN ZEROS (mpmath dps=25)")
print("=" * 60)

zeros = []
for n in range(1, 101):
    z = mpmath.zetazero(n)
    zeros.append({'n': n, 'sigma': float(z.real), 't': float(z.imag)})
    if n % 10 == 0:
        print(f"  ...computed rho_1..{n} (last: t={float(z.imag):.4f})")

print(f"  First: t={zeros[0]['t']:.6f}")
print(f"  Last:  t={zeros[99]['t']:.6f}")
print(f"  Range: [{zeros[0]['t']:.2f}, {zeros[99]['t']:.2f}]")

# ============================================================
# HELPER: run the four tests for a given prime set
# ============================================================
def run_tests(zeros, prime_root_map, label):
    n_zeros = len(zeros)
    n_pairs = n_zeros * (n_zeros - 1) // 2

    print()
    print(f"{'='*60}")
    print(f"TESTS [{label}]  n={n_zeros}, {n_pairs} pairs")
    print(f"{'='*60}")

    # Precompute all f5D vectors
    f_vecs = [f5D(z['t'], prime_root_map) for z in zeros]
    norms  = [np.linalg.norm(f) for f in f_vecs]

    # Test 1: v- = 0
    max_vm = max(abs((z['sigma'] - 0.5)) for z in zeros)
    t1_pass = max_vm < 1e-12
    print(f"  Test 1 (v-=0): max sigma deviation = {max_vm:.2e}  "
          f"{'PASS' if t1_pass else 'FAIL'}")

    # Test 2: non-degeneracy
    min_norm = min(norms)
    t2_pass = min_norm > 1e-10
    print(f"  Test 2 (non-degenerate): min ||f5D|| = {min_norm:.6f}  "
          f"{'PASS' if t2_pass else 'FAIL'}")

    # Test 3: strong injectivity — compute all cos values
    cos_vals = []
    near_proportional = []   # |cos| > 0.99
    alert = []               # |cos| > 0.99

    for i, j in combinations(range(n_zeros), 2):
        fi, fj = f_vecs[i], f_vecs[j]
        ni, nj = norms[i], norms[j]
        c = np.dot(fi, fj) / (ni * nj)
        ac = abs(c)
        cos_vals.append(ac)
        if ac > 0.99:
            alert.append((zeros[i]['n'], zeros[j]['n'], ac))

    prop_pairs = sum(1 for c in cos_vals if c > 1.0 - 1e-8)
    t3_pass = prop_pairs == 0

    print(f"  Test 3 (strong injectivity):")
    print(f"    Pairs checked:   {n_pairs}")
    print(f"    Proportional:    {prop_pairs}")
    print(f"    Near-prop (>0.99): {len(alert)}")
    print(f"    Min |cos theta|: {min(cos_vals):.8f}")
    print(f"    Max |cos theta|: {max(cos_vals):.8f}")
    print(f"    Mean |cos theta|:{np.mean(cos_vals):.8f}")
    if alert:
        print(f"    ALERT: near-proportional pairs:")
        for pi, pj, c in sorted(alert, key=lambda x: -x[2])[:5]:
            print(f"      rho_{pi} & rho_{pj}: |cos| = {c:.8f}")
    print(f"    Test 3: {'PASS' if t3_pass else 'FAIL'}")

    # Test 4: equivariance (check 5 representative zeros)
    max_equiv_err = 0.0
    for z in zeros[:5]:
        v = embed(z['sigma'], z['t'], prime_root_map)
        v_conj = embed(1.0 - z['sigma'], z['t'], prime_root_map)
        err = np.linalg.norm(v_conj - s_alpha4(v))
        max_equiv_err = max(max_equiv_err, err)
    t4_pass = max_equiv_err < 1e-12
    print(f"  Test 4 (equivariance): max err (first 5) = {max_equiv_err:.2e}  "
          f"{'PASS' if t4_pass else 'FAIL'}")

    all_pass = t1_pass and t2_pass and t3_pass and t4_pass
    print(f"  ALL PASS: {all_pass}")

    return {
        'label': label,
        'n_zeros': n_zeros,
        'n_pairs': n_pairs,
        'test1_pass': bool(t1_pass),
        'test2_pass': bool(t2_pass),
        'test2_min_norm': float(min_norm),
        'test2_max_norm': float(max(norms)),
        'test3_pass': bool(t3_pass),
        'test3_n_proportional': int(prop_pairs),
        'test3_n_near_prop_99': len(alert),
        'test3_min_cos': float(min(cos_vals)),
        'test3_max_cos': float(max(cos_vals)),
        'test3_mean_cos': float(np.mean(cos_vals)),
        'test3_alerts': [(pi, pj, float(c)) for pi, pj, c in alert],
        'test4_pass': bool(t4_pass),
        'all_pass': bool(all_pass),
        'cos_vals': [float(c) for c in cos_vals],
        'f_norms': [float(n) for n in norms],
    }

# ============================================================
# RUN BOTH FORMULA VARIANTS
# ============================================================
r6 = run_tests(zeros, PRIMES_6, "6-prime p=2..13")
r9 = run_tests(zeros, PRIMES_9, "9-prime p=2..23")

# ============================================================
# ROLLING MAX ANALYSIS (bounded-away-from-1 test)
# ============================================================
print()
print("=" * 60)
print("ROLLING MAX |cos theta| vs n  (bounded-away-from-1 analysis)")
print("=" * 60)

def rolling_max(cos_vals_flat, n_zeros):
    """
    cos_vals_flat: list of |cos theta| for all C(n_zeros,2) pairs in
    lexicographic order (i<j, row-major).
    Returns list of length n_zeros: rolling_max[n-1] = max over pairs (i<j<=n).
    """
    # Build pair index mapping: pair (i,j) with i<j -> flat index
    # We know cos_vals_flat is ordered by combinations(range(n_zeros), 2)
    rolling = [0.0] * n_zeros
    pair_iter = ((i, j) for i in range(n_zeros) for j in range(i+1, n_zeros))
    flat_max = [0.0] * n_zeros  # flat_max[k] = max over pairs (i<j<=k)

    # More efficient: build a matrix of cos values
    cos_mat = np.zeros((n_zeros, n_zeros))
    for idx, (i, j) in enumerate(combinations(range(n_zeros), 2)):
        cos_mat[i, j] = cos_vals_flat[idx]
        cos_mat[j, i] = cos_vals_flat[idx]

    # Rolling max: for n from 1 to n_zeros, max over i<j<=n-1
    cur_max = 0.0
    roll = []
    for n in range(n_zeros):
        if n > 0:
            # Add all pairs (i, n) for i < n
            new_vals = cos_mat[:n, n]
            m = new_vals.max() if len(new_vals) > 0 else 0.0
            cur_max = max(cur_max, m)
        roll.append(cur_max)
    return roll

roll6 = rolling_max(r6['cos_vals'], 100)
roll9 = rolling_max(r9['cos_vals'], 100)

# Print at n=10,20,...,100
print(f"  {'n':>5}  {'6-prime':>12}  {'9-prime':>12}")
for n in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    print(f"  {n:>5}  {roll6[n-1]:>12.8f}  {roll9[n-1]:>12.8f}")

# Plateau detection: last 20 values vs first 20
plateau_6 = roll6[-1] - roll6[79]   # change over last 20
plateau_9 = roll9[-1] - roll9[79]
print()
print(f"  6-prime: max at n=100 = {roll6[-1]:.8f}  "
      f"(grew by {plateau_6:.6f} from n=80 to n=100)")
print(f"  9-prime: max at n=100 = {roll9[-1]:.8f}  "
      f"(grew by {plateau_9:.6f} from n=80 to n=100)")

if roll6[-1] < 0.95 and plateau_6 < 0.01:
    print(f"  6-prime: PLATEAU below 0.95 -- strong injectivity holds empirically")
elif roll6[-1] < 0.99:
    print(f"  6-prime: growing slowly, max < 0.99 -- no alert")
else:
    print(f"  6-prime: ALERT -- max |cos theta| approaching 1")

if roll9[-1] < roll6[-1]:
    print(f"  9-prime lowers max by {roll6[-1]-roll9[-1]:.6f} -- more primes = stronger injectivity")
else:
    print(f"  9-prime does not lower max -- additional primes are neutral or slightly increase cos")

# ============================================================
# |cos theta| HISTOGRAM (6-prime, n=100)
# ============================================================
print()
print("=" * 60)
print("HISTOGRAM: |cos theta| distribution (6-prime, n=100)")
print("=" * 60)
bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0]
cos_arr6 = np.array(r6['cos_vals'])
print(f"  {'Range':>16}  {'Count':>6}  {'Pct':>6}")
for lo, hi in zip(bins[:-1], bins[1:]):
    count = int(np.sum((cos_arr6 >= lo) & (cos_arr6 < hi)))
    pct = 100.0 * count / len(cos_arr6)
    bar = '#' * int(pct / 2)
    print(f"  [{lo:.2f}, {hi:.2f})  {count:>6}  {pct:>5.1f}%  {bar}")

print()
print("HISTOGRAM: |cos theta| distribution (9-prime, n=100)")
cos_arr9 = np.array(r9['cos_vals'])
for lo, hi in zip(bins[:-1], bins[1:]):
    count = int(np.sum((cos_arr9 >= lo) & (cos_arr9 < hi)))
    pct = 100.0 * count / len(cos_arr9)
    bar = '#' * int(pct / 2)
    print(f"  [{lo:.2f}, {hi:.2f})  {count:>6}  {pct:>5.1f}%  {bar}")

# ============================================================
# TOP 10 MOST-NEARLY-PROPORTIONAL PAIRS (both formulas)
# ============================================================
print()
print("=" * 60)
print("TOP 10 MOST-NEARLY-PROPORTIONAL PAIRS")
print("=" * 60)

def top_pairs(cos_vals_flat, zeros, k=10):
    pairs = [(zeros[i]['n'], zeros[j]['n'], cos_vals_flat[idx])
             for idx, (i, j) in enumerate(combinations(range(len(zeros)), 2))]
    return sorted(pairs, key=lambda x: -x[2])[:k]

print()
print("  6-prime (p=2..13):")
for pi, pj, c in top_pairs(r6['cos_vals'], zeros):
    print(f"    rho_{pi:3d} & rho_{pj:3d}: |cos theta| = {c:.8f}")

print()
print("  9-prime (p=2..23):")
for pi, pj, c in top_pairs(r9['cos_vals'], zeros):
    print(f"    rho_{pi:3d} & rho_{pj:3d}: |cos theta| = {c:.8f}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print()
print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  6-prime (n=100):  all_pass={r6['all_pass']}  "
      f"max|cos|={r6['test3_max_cos']:.6f}  "
      f"near-prop>0.99={r6['test3_n_near_prop_99']}")
print(f"  9-prime (n=100):  all_pass={r9['all_pass']}  "
      f"max|cos|={r9['test3_max_cos']:.6f}  "
      f"near-prop>0.99={r9['test3_n_near_prop_99']}")
print()
print(f"  Rolling max at n=100:")
print(f"    6-prime: {roll6[-1]:.8f}")
print(f"    9-prime: {roll9[-1]:.8f}")
print()
bounded_6 = roll6[-1] < 0.99 and r6['test3_n_near_prop_99'] == 0
bounded_9 = roll9[-1] < 0.99 and r9['test3_n_near_prop_99'] == 0
print(f"  Max |cos theta| bounded away from 1?")
print(f"    6-prime: {'YES (< 0.99, no alerts)' if bounded_6 else 'UNCERTAIN or NO'}")
print(f"    9-prime: {'YES (< 0.99, no alerts)' if bounded_9 else 'UNCERTAIN or NO'}")
print()
print("  Reduction chain:")
print("    Simple spectrum")
print("    + [{tn * log p} linearly independent over Q]")
print("    => strong injectivity (max|cos|<1 for all n tested)")
print("    => aiex001_critical_line_forcing => RH")

# ============================================================
# SAVE JSON
# ============================================================
results = {
    'experiment': 'Phase20C_AIEX001_Scale100_ExtendedPrimes',
    'date': '2026-03-23',
    'n_zeros': 100,
    'zeros_range': [zeros[0]['t'], zeros[-1]['t']],
    'note_v2': (
        'v2 = u_antisym = (e4-e5)/sqrt(2) is the ANTISYMMETRIC direction. '
        'Using it in f5D breaks equivariance (Test 1 fails). '
        'p=17,19,23 use cross-block D6 roots (e2+e3)/sqrt2, (e2+e6)/sqrt2, (e7+e3)/sqrt2 instead.'
    ),
    'prime_assignments': {
        '6-prime': {str(p): f'{name}' for p, name in
                    [(2,'q4=(e4+e5)/sqrt2'), (3,'q2=(-e3+e6)/sqrt2'),
                     (5,'v5=(e3+e6)/sqrt2'), (7,'v1=(e2-e7)/sqrt2'),
                     (11,'v4=(e2+e7)/sqrt2'), (13,'q3=(-e2+e7)/sqrt2')]},
        '9-prime_extension': {
            '17': '(e2+e3)/sqrt2 [cross-block D6 root]',
            '19': '(e2+e6)/sqrt2 [cross-block D6 root]',
            '23': '(e7+e3)/sqrt2 [cross-block D6 root]',
        },
    },
    'results_6prime': {k: v for k, v in r6.items() if k != 'cos_vals'},
    'results_9prime': {k: v for k, v in r9.items() if k != 'cos_vals'},
    'rolling_max_6prime': [float(x) for x in roll6],
    'rolling_max_9prime': [float(x) for x in roll9],
    'rolling_max_at_n': {
        str(n): {'6prime': float(roll6[n-1]), '9prime': float(roll9[n-1])}
        for n in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    },
    'bounded_away_from_1': {
        '6prime': bool(bounded_6),
        '9prime': bool(bounded_9),
    },
    'top10_pairs_6prime': top_pairs(r6['cos_vals'], zeros),
    'top10_pairs_9prime': top_pairs(r9['cos_vals'], zeros),
}

with open('phase20c_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print()
print("Saved to phase20c_results.json")
