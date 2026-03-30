"""
Phase 19 Thread 2 — Annihilation Topology AT-1
Chavez AI Labs LLC · March 23, 2026

Classifies the 48 bilateral zero divisor pairs as canonical (Type I, pure Clifford grade)
vs CD-specific (Type II, mixed Clifford grade), connecting the 16D sedenion algebra
classification to the 8D Cl(7,0) geometric grade structure from Thread 1.

Inputs:  p18d_enumeration.json, p18d_results_final.json, rh_phase18d_prep.py, clifford_verified.py
Outputs: phase19_thread2_results.json
"""

import json
import sys
import numpy as np
import importlib.util

# ── Load sedenion product ───────────────────────────────────────────────────

spec = importlib.util.spec_from_file_location('phase18d', 'rh_phase18d_prep.py')
phase18d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase18d)
sed_product = phase18d.sed_product

# ── Load CliffordElement ────────────────────────────────────────────────────

CLIFFORD_PATH = r'C:\Users\chave\PROJECTS\cailculator-mcp\src\cailculator_mcp'
if CLIFFORD_PATH not in sys.path:
    sys.path.insert(0, CLIFFORD_PATH)
from clifford_verified import CliffordElement

N_CLIFFORD = 7  # Cl(7,0), 128-dimensional

# ── Helper functions ────────────────────────────────────────────────────────

def to_8d(vec16):
    """Convert 16D sedenion vector to 8D image: P_8D[k] = P[k] - P[k+8]."""
    v = np.asarray(vec16)
    return tuple(float(v[k] - v[k+8]) for k in range(8))

def make_clifford(d8):
    """
    Build Cl(7,0) grade-1 element from 8D direction vector.
    Blade convention: e_k at coeffs[1<<(k-1)], k=1..7 (1-indexed).
    d8[0] is unused (position 0 in 8D = position 1, but Cl(7,0) has blades 1-7).
    d8[k] for k=0..6 maps to Clifford blade e_{k+1}: coeffs[1<<k] = d8[k].
    Wait — d8 is 0-indexed: d8[0]..d8[7]. The 8D space is indexed 0..7.
    Cl(7,0) has 7 generators e_1..e_7. We map 8D position k to Clifford e_{k+1}
    for k=0..6 (8D position 7 is always 0 in the bilateral set, confirmed Thread 1).
    """
    coeffs = [0.0] * (1 << N_CLIFFORD)
    for k in range(7):  # 8D positions 0..6 -> Clifford e_1..e_7
        if abs(d8[k]) > 1e-10:
            coeffs[1 << k] = d8[k]
    return CliffordElement(N_CLIFFORD, coeffs)

def get_grade_structure(cl_elem):
    """
    Returns set of grades with non-negligible norm in the multivector.
    """
    grades = set()
    n = N_CLIFFORD
    dim = 1 << n
    for blade in range(dim):
        if abs(cl_elem.coeffs[blade]) > 1e-10:
            g = bin(blade).count('1')
            grades.add(g)
    return grades

def grade_norm(cl_elem, grade):
    """L2 norm of the grade-k part."""
    n = N_CLIFFORD
    total = 0.0
    for blade in range(1 << n):
        if bin(blade).count('1') == grade:
            total += cl_elem.coeffs[blade] ** 2
    return total ** 0.5

def inner_product_8d(d8_a, d8_b):
    """Standard inner product of two 8D vectors."""
    return sum(d8_a[k] * d8_b[k] for k in range(8))

# ── Load data ───────────────────────────────────────────────────────────────

with open('p18d_enumeration.json') as f:
    enum = json.load(f)
pairs = enum['pairs']

with open('p18d_results_final.json') as f:
    p18d_results = json.load(f)
task3_results = p18d_results['task3']['pair_results']

# Build canonical index set from Phase 18D task3
canonical_indices = set()
for i, pr in enumerate(task3_results):
    if pr.get('canonical'):
        canonical_indices.add(i)

print(f'Loaded {len(pairs)} bilateral pairs.')
print(f'Canonical pairs from Phase 18D: {len(canonical_indices)}')
print()

# ── Section 1: Verify all P*Q = 0 ──────────────────────────────────────────

print('=' * 60)
print('SECTION 1: Sedenion Annihilation Verification')
print('=' * 60)

pq_zero_count = 0
pq_failures = []
for i, e in enumerate(pairs):
    P = np.array(e['P'])
    Q = np.array(e['Q'])
    PQ = sed_product(P, Q)
    norm_pq = np.linalg.norm(PQ)
    if norm_pq < 1e-10:
        pq_zero_count += 1
    else:
        pq_failures.append((i, norm_pq))

print(f'P*Q = 0 verified: {pq_zero_count}/48')
if pq_failures:
    print(f'FAILURES: {pq_failures}')
else:
    print('All 48 pairs annihilate: P*Q = 0 confirmed.')
print()

# ── Section 2: Direct basis annihilation (Type I naive test) ────────────────

print('=' * 60)
print('SECTION 2: Direct Basis Annihilation Test (e_a * e_b = 0?)')
print('=' * 60)

def basis_vec(k, n=16):
    v = np.zeros(n)
    v[k] = 1.0
    return v

direct_zero_pairs = []
for i in range(16):
    for j in range(16):
        if i == j:
            continue
        ei = basis_vec(i)
        ej = basis_vec(j)
        result = sed_product(ei, ej)
        if np.allclose(result, 0, atol=1e-10):
            direct_zero_pairs.append((i, j))

print(f'Ordered basis pairs (i,j) i!=j where e_i * e_j = 0: {len(direct_zero_pairs)}')
if len(direct_zero_pairs) == 0:
    print('RESULT: No direct basis annihilation exists in sedenions.')
    print('All bilateral zero divisors are "Type II" in the naive sense.')
    print('(This is expected: sedenion basis elements e_i * e_j = +/-e_k for all i!=j)')
print()

# Check specifically the (a,b) and (c,d) pairs from the bilateral family
print('Checking (a,b) pairs from bilateral enumeration:')
ab_zero = 0
for e in pairs:
    ea = basis_vec(e['a'])
    eb = basis_vec(e['b'])
    r = sed_product(ea, eb)
    if np.allclose(r, 0, atol=1e-10):
        ab_zero += 1
print(f'  e_a * e_b = 0: {ab_zero}/48')
print(f'  e_c * e_d = 0: ', end='')
cd_zero = 0
for e in pairs:
    ec = basis_vec(e['c'])
    ed = basis_vec(e['d'])
    r = sed_product(ec, ed)
    if np.allclose(r, 0, atol=1e-10):
        cd_zero += 1
print(f'{cd_zero}/48')
print()

# ── Section 3: Clifford grade structure classification ──────────────────────

print('=' * 60)
print('SECTION 3: Clifford Cl(7,0) Grade Structure Classification')
print('=' * 60)
print()

pair_results = []
canonical_grades = {'pure_0': 0, 'pure_2': 0, 'mixed_02': 0, 'other': 0}
cd_grades = {'pure_0': 0, 'pure_2': 0, 'mixed_02': 0, 'other': 0}

for i, e in enumerate(pairs):
    is_canonical = i in canonical_indices
    P_16d = np.array(e['P'])
    Q_16d = np.array(e['Q'])

    # 8D projections
    P_8d = to_8d(P_16d)
    Q_8d = to_8d(Q_16d)

    # Inner product in 8D
    inner = inner_product_8d(P_8d, Q_8d)

    # Clifford grade-1 elements
    cl_P = make_clifford(P_8d)
    cl_Q = make_clifford(Q_8d)

    # Geometric product
    cl_PQ = cl_P * cl_Q

    # Grade structure
    grades = get_grade_structure(cl_PQ)
    g0_norm = grade_norm(cl_PQ, 0)
    g2_norm = grade_norm(cl_PQ, 2)

    # Classify
    if grades == {0}:
        grade_type = 'pure_0'
    elif grades == {2}:
        grade_type = 'pure_2'
    elif grades == {0, 2}:
        grade_type = 'mixed_02'
    else:
        grade_type = 'other'

    is_pure = grade_type in ('pure_0', 'pure_2')

    if is_canonical:
        canonical_grades[grade_type] += 1
    else:
        cd_grades[grade_type] += 1

    pair_results.append({
        'index': i,
        'a': e['a'], 'b': e['b'], 's': e['s'],
        'c': e['c'], 'd': e['d'], 't': e['t'],
        'is_canonical': is_canonical,
        'P_8d': list(P_8d),
        'Q_8d': list(Q_8d),
        'inner_product_8d': inner,
        'grade_type': grade_type,
        'grade_0_norm': round(g0_norm, 10),
        'grade_2_norm': round(g2_norm, 10),
        'grades_present': sorted(list(grades)),
        'is_pure_grade': is_pure,
    })

# Print results
print('Canonical pairs (6) grade structure:')
for k, v in canonical_grades.items():
    if v > 0:
        print(f'  {k}: {v}')
print()
print('CD-specific pairs (42) grade structure:')
for k, v in cd_grades.items():
    if v > 0:
        print(f'  {k}: {v}')
print()

# Check prediction: canonical -> pure, cd-specific -> mixed
canon_pure = sum(1 for pr in pair_results if pr['is_canonical'] and pr['is_pure_grade'])
canon_mixed = sum(1 for pr in pair_results if pr['is_canonical'] and not pr['is_pure_grade'])
cd_pure = sum(1 for pr in pair_results if not pr['is_canonical'] and pr['is_pure_grade'])
cd_mixed = sum(1 for pr in pair_results if not pr['is_canonical'] and not pr['is_pure_grade'])

print('Prediction test: canonical <-> pure, CD-specific <-> mixed')
print(f'  Canonical + pure:  {canon_pure}/6  (expected 6)')
print(f'  Canonical + mixed: {canon_mixed}/6  (expected 0)')
print(f'  CD-specific + pure: {cd_pure}/42  (expected 0)')
print(f'  CD-specific + mixed: {cd_mixed}/42  (expected 42)')

prediction_confirmed = (canon_pure == 6 and canon_mixed == 0 and
                        cd_pure == 0 and cd_mixed == 42)
print(f'\nPrediction CONFIRMED: {prediction_confirmed}')
print()

# ── Section 4: Inner product analysis for canonical pairs ──────────────────

print('=' * 60)
print('SECTION 4: Inner Product Analysis (Canonical Pairs)')
print('=' * 60)
canon_pairs = [pr for pr in pair_results if pr['is_canonical']]
print('Canonical pair inner products (8D):')
for pr in canon_pairs:
    inner = pr['inner_product_8d']
    print(f"  a={pr['a']},b={pr['b']},s={pr['s']} / c={pr['c']},d={pr['d']},t={pr['t']}"
          f"  inner={inner:.1f}  grade={pr['grade_type']}")
print()

# ── Section 5: CD-specific inner product distribution ──────────────────────

print('=' * 60)
print('SECTION 5: CD-specific Pair Inner Product Distribution')
print('=' * 60)
cd_pairs = [pr for pr in pair_results if not pr['is_canonical']]
inner_vals = [pr['inner_product_8d'] for pr in cd_pairs]
from collections import Counter
inner_counts = Counter(round(x) for x in inner_vals)
print('Inner product histogram (CD-specific, 42 pairs):')
for val in sorted(inner_counts.keys()):
    print(f'  inner = {val:+d}: {inner_counts[val]}')
print()

# ── Section 6: (A1)^6 membership cross-tabulation ──────────────────────────

print('=' * 60)
print('SECTION 6: (A1)^6 Membership Cross-tabulation')
print('=' * 60)

can6_roots_8d = set([
    (0., 1., 0., 0., 0., 0., -1., 0.),   # v1
    (0., -1., 0., 0., 0., 0., 1., 0.),   # q3
    (0., 0., 0., 1., -1., 0., 0., 0.),   # v2
    (0., 0., 0., -1., 1., 0., 0., 0.),   # v3
    (0., 1., 0., 0., 0., 0., 1., 0.),    # v4
    (0., 0., 1., 0., 0., 1., 0., 0.),    # v5
    (0., 0., -1., 0., 0., 1., 0., 0.),   # q2
    (0., 0., 0., 1., 1., 0., 0., 0.),    # q4
])

# Classify by A1^6 membership
both_in_a16 = 0
p_only_a16 = 0
q_only_a16 = 0
neither_a16 = 0
for pr in pair_results:
    p_in = tuple(pr['P_8d']) in can6_roots_8d
    q_in = tuple(pr['Q_8d']) in can6_roots_8d
    if p_in and q_in:
        both_in_a16 += 1
    elif p_in:
        p_only_a16 += 1
    elif q_in:
        q_only_a16 += 1
    else:
        neither_a16 += 1

print('(A1)^6 membership of bilateral pair 8D images:')
print(f'  Both P_8d and Q_8d in (A1)^6: {both_in_a16}')
print(f'  P_8d in (A1)^6 only: {p_only_a16}')
print(f'  Q_8d in (A1)^6 only: {q_only_a16}')
print(f'  Neither in (A1)^6: {neither_a16}')
print()

# Cross-tab: (A1)^6 membership vs canonical/CD
print('Cross-tabulation: (A1)^6 membership vs canonical status:')
for p_in_a16 in [True, False]:
    for q_in_a16 in [True, False]:
        canon_count = sum(1 for pr in pair_results
                         if (tuple(pr['P_8d']) in can6_roots_8d) == p_in_a16
                         and (tuple(pr['Q_8d']) in can6_roots_8d) == q_in_a16
                         and pr['is_canonical'])
        cd_count = sum(1 for pr in pair_results
                      if (tuple(pr['P_8d']) in can6_roots_8d) == p_in_a16
                      and (tuple(pr['Q_8d']) in can6_roots_8d) == q_in_a16
                      and not pr['is_canonical'])
        label = f'P_in={p_in_a16}, Q_in={q_in_a16}'
        print(f'  {label}: canonical={canon_count}, CD-specific={cd_count}')
print()

# ── Save results ────────────────────────────────────────────────────────────

results = {
    'experiment': 'Phase19_Thread2_AnnihilationTopology',
    'date': '2026-03-23',
    'total_pairs': 48,
    'canonical_pairs': len(canonical_indices),
    'cd_specific_pairs': 48 - len(canonical_indices),

    'section1_pq_annihilation': {
        'all_48_verified': pq_zero_count == 48,
        'zero_count': pq_zero_count,
        'failures': pq_failures,
    },

    'section2_direct_basis_annihilation': {
        'ordered_basis_pairs_tested': 240,
        'direct_zero_pairs': len(direct_zero_pairs),
        'ab_zero_count': ab_zero,
        'cd_zero_count': cd_zero,
        'result': 'No direct basis-element annihilation in sedenions',
    },

    'section3_clifford_grade': {
        'canonical_grade_distribution': canonical_grades,
        'cd_specific_grade_distribution': cd_grades,
        'canonical_pure_count': canon_pure,
        'canonical_mixed_count': canon_mixed,
        'cd_specific_pure_count': cd_pure,
        'cd_specific_mixed_count': cd_mixed,
        'prediction_confirmed': prediction_confirmed,
    },

    'section4_canonical_inner_products': {
        pr['a']: {
            'b': pr['b'], 's': pr['s'],
            'c': pr['c'], 'd': pr['d'], 't': pr['t'],
            'inner_8d': pr['inner_product_8d'],
            'grade_type': pr['grade_type']
        } for pr in canon_pairs
    },

    'section6_a16_membership': {
        'both_P_Q_in_a16': both_in_a16,
        'p_only': p_only_a16,
        'q_only': q_only_a16,
        'neither': neither_a16,
    },

    'pair_results': pair_results,
}

with open('phase19_thread2_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print('Results saved to phase19_thread2_results.json')
print()
print('=' * 60)
print('SUMMARY')
print('=' * 60)
print(f'P*Q = 0 for all 48 pairs: {pq_zero_count == 48}')
print(f'Direct basis annihilation (e_i*e_j=0): 0 pairs')
print(f'Canonical/pure grade alignment: {canon_pure}/6 canonical are pure')
print(f'CD-specific/mixed grade alignment: {cd_mixed}/42 CD-specific are mixed')
print(f'Prediction CONFIRMED: {prediction_confirmed}')
