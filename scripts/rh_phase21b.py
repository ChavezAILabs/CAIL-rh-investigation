"""
Phase 21B: q3 Anomaly Investigation
Chavez AI Labs LLC -- March 24, 2026

Phase 21A revealed three surprises in the fixed-subspace root set:
  1. q3 x q2 = 0  (Block A x Block B, p=13 x p=3)  -- zero product
  2. q3 x q4 = 0  (Block A x Block C, p=13 x p=2)  -- zero product
  3. q2 x q4: |prod|^2 = 8  (Block B x Block C, p=3 x p=2) -- anomalous norm

This phase investigates:
  Section 1: Is (q3, q2) a bilateral zero divisor pair?
             Does q3 x q2 = 0 AND q2 x q3 = 0?
             Is it in the Phase 18D bilateral family or a new pairing?
  Section 2: Is (q3, q4) a bilateral zero divisor pair?
             Same questions.
  Section 3: Full zero divisor map of q3 across ALL bilateral family members.
             How many bilateral family vectors annihilate q3?
  Section 4: q2 x q4 = ? -- full 16D decomposition.
             norm^2=8 explanation. Is this a known sedenion product?
  Section 5: v5 bridge analysis.
             Why does v5 share indices with both Block A (q3) and Block C (q4)?
  Section 6: Multi-partner theorem candidate.
             Does q3 have MULTIPLE bilateral zero divisor partners simultaneously?

Output: phase21b_results.json + RH_Phase21B_Results.md
"""

import numpy as np
import json
import importlib.util

# ── Load sedenion multiplication ──────────────────────────────────────────────
spec = importlib.util.spec_from_file_location('phase18d', 'rh_phase18d_prep.py')
phase18d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase18d)
sed_product = phase18d.sed_product

# ── Load bilateral family ─────────────────────────────────────────────────────
with open('p18d_enumeration.json', 'r') as f:
    enum_data = json.load(f)
bilateral_pairs = enum_data['pairs']
print(f"Loaded {len(bilateral_pairs)} bilateral pairs from p18d_enumeration.json")

# ── Root definitions (16D, 0-indexed) ────────────────────────────────────────
def make16(pairs):
    v = np.zeros(16)
    for idx, s in pairs:
        v[idx] = float(s)
    return v

ROOTS_16D = {
    'v1': make16([(2, 1), (7, -1)]),    # e2-e7  Block A p=7
    'v4': make16([(2, 1), (7,  1)]),    # e2+e7  Block A p=11
    'q3': make16([(6, 1), (9,  1)]),    # e6+e9  Block A p=13
    'q2': make16([(5, 1), (10, 1)]),    # e5+e10 Block B p=3
    'v5': make16([(3, 1), (6,  1)]),    # e3+e6  Block B p=5
    'q4': make16([(3, 1), (12,-1)]),    # e3-e12 Block C p=2
}
PRIME = {'v1': 7, 'v4': 11, 'q3': 13, 'q2': 3, 'v5': 5, 'q4': 2}
BLOCK = {'v1': 'A', 'v4': 'A', 'q3': 'A', 'q2': 'B', 'v5': 'B', 'q4': 'C'}

results = {}

def nonzero_indices(v, tol=1e-10):
    return [(i, round(v[i])) for i in range(len(v)) if abs(v[i]) > tol]

def norm_sq(v):
    return round(float(np.dot(v, v)), 10)

def is_bilateral_pair(P, Q, tol=1e-10):
    """Check if P*Q=0 AND Q*P=0."""
    pq = sed_product(P, Q)
    qp = sed_product(Q, P)
    return np.allclose(pq, 0, atol=tol), np.allclose(qp, 0, atol=tol)

def find_in_bilateral_family(P, Q, pairs, tol=1e-10):
    """Check if (P,Q) or (Q,P) appears (up to sign) in the bilateral family."""
    for pair in pairs:
        fP = np.array(pair['P'])
        fQ = np.array(pair['Q'])
        # Check (P,Q) match
        if (np.allclose(fP, P, atol=tol) and np.allclose(fQ, Q, atol=tol)):
            return True, 'forward', pair
        if (np.allclose(fP, -P, atol=tol) and np.allclose(fQ, -Q, atol=tol)):
            return True, 'forward_neg', pair
        # Check (Q,P) match (bilateral means P and Q can be swapped in the pair)
        if (np.allclose(fP, Q, atol=tol) and np.allclose(fQ, P, atol=tol)):
            return True, 'swapped', pair
        if (np.allclose(fP, -Q, atol=tol) and np.allclose(fQ, -P, atol=tol)):
            return True, 'swapped_neg', pair
    return False, None, None

print("\n" + "="*65)
print("PHASE 21B: q3 Anomaly Investigation")
print("Chavez AI Labs LLC -- March 24, 2026")
print("="*65)

# =============================================================================
# SECTION 1: Is (q3, q2) a bilateral zero divisor pair?
# =============================================================================
print("\n" + "="*65)
print("SECTION 1: Is (q3, q2) a bilateral zero divisor pair?")
print("="*65)

q3 = ROOTS_16D['q3']   # e6+e9  (positions 6,9)
q2 = ROOTS_16D['q2']   # e5+e10 (positions 5,10)

q3_times_q2 = sed_product(q3, q2)
q2_times_q3 = sed_product(q2, q3)

print(f"\nq3 = e6+e9 (0-indexed positions 6,9): {nonzero_indices(q3)}")
print(f"q2 = e5+e10 (0-indexed positions 5,10): {nonzero_indices(q2)}")

print(f"\nq3 * q2 = {nonzero_indices(q3_times_q2)}  |prod|^2 = {norm_sq(q3_times_q2)}")
print(f"q2 * q3 = {nonzero_indices(q2_times_q3)}  |prod|^2 = {norm_sq(q2_times_q3)}")

pq_zero = np.allclose(q3_times_q2, 0, atol=1e-10)
qp_zero = np.allclose(q2_times_q3, 0, atol=1e-10)
bilateral_q3q2 = pq_zero and qp_zero
print(f"\nq3*q2=0: {pq_zero}   q2*q3=0: {qp_zero}")
print(f"=> (q3,q2) is a bilateral zero divisor pair: {bilateral_q3q2}")

in_family, direction, match = find_in_bilateral_family(q3, q2, bilateral_pairs)
print(f"=> In Phase 18D bilateral family: {in_family} (direction: {direction})")
if match:
    print(f"   Matching pair: a={match['a']}, b={match['b']}, s={match['s']}, c={match['c']}, d={match['d']}, t={match['t']}")

results['section1_q3q2'] = {
    'q3_x_q2_zero': bool(pq_zero),
    'q2_x_q3_zero': bool(qp_zero),
    'is_bilateral_pair': bool(bilateral_q3q2),
    'in_bilateral_family': bool(in_family),
    'family_direction': direction,
    'q3_x_q2': q3_times_q2.tolist(),
    'q2_x_q3': q2_times_q3.tolist()
}

# =============================================================================
# SECTION 2: Is (q3, q4) a bilateral zero divisor pair?
# =============================================================================
print("\n" + "="*65)
print("SECTION 2: Is (q3, q4) a bilateral zero divisor pair?")
print("="*65)

q4 = ROOTS_16D['q4']   # e3-e12 (positions 3,12)

q3_times_q4 = sed_product(q3, q4)
q4_times_q3 = sed_product(q4, q3)

print(f"\nq3 = e6+e9 (positions 6,9): {nonzero_indices(q3)}")
print(f"q4 = e3-e12 (positions 3,12): {nonzero_indices(q4)}")

print(f"\nq3 * q4 = {nonzero_indices(q3_times_q4)}  |prod|^2 = {norm_sq(q3_times_q4)}")
print(f"q4 * q3 = {nonzero_indices(q4_times_q3)}  |prod|^2 = {norm_sq(q4_times_q3)}")

pq_zero_2 = np.allclose(q3_times_q4, 0, atol=1e-10)
qp_zero_2 = np.allclose(q4_times_q3, 0, atol=1e-10)
bilateral_q3q4 = pq_zero_2 and qp_zero_2
print(f"\nq3*q4=0: {pq_zero_2}   q4*q3=0: {qp_zero_2}")
print(f"=> (q3,q4) is a bilateral zero divisor pair: {bilateral_q3q4}")

in_family2, direction2, match2 = find_in_bilateral_family(q3, q4, bilateral_pairs)
print(f"=> In Phase 18D bilateral family: {in_family2} (direction: {direction2})")
if match2:
    print(f"   Matching pair: a={match2['a']}, b={match2['b']}, s={match2['s']}, c={match2['c']}, d={match2['d']}, t={match2['t']}")

results['section2_q3q4'] = {
    'q3_x_q4_zero': bool(pq_zero_2),
    'q4_x_q3_zero': bool(qp_zero_2),
    'is_bilateral_pair': bool(bilateral_q3q4),
    'in_bilateral_family': bool(in_family2),
    'family_direction': direction2,
    'q3_x_q4': q3_times_q4.tolist(),
    'q4_x_q3': q4_times_q3.tolist()
}

# =============================================================================
# SECTION 3: Full zero divisor map of q3
# =============================================================================
print("\n" + "="*65)
print("SECTION 3: Full zero divisor map of q3")
print("="*65)
print("For every vector in the bilateral family, compute q3*v and v*q3.")

zero_partners = []
near_zero_partners = []

# Check all 48 P-vectors and 48 Q-vectors
for pair in bilateral_pairs:
    for side, v_raw in [('P', pair['P']), ('Q', pair['Q'])]:
        v = np.array(v_raw)
        fwd = sed_product(q3, v)
        rev = sed_product(v, q3)
        ns_fwd = norm_sq(fwd)
        ns_rev = norm_sq(rev)
        nz_fwd = np.allclose(fwd, 0, atol=1e-10)
        nz_rev = np.allclose(rev, 0, atol=1e-10)
        if nz_fwd or nz_rev:
            v_idx = nonzero_indices(v)
            entry = {
                'side': side,
                'vector': v_idx,
                'q3*v=0': bool(nz_fwd),
                'v*q3=0': bool(nz_rev),
                'bilateral': bool(nz_fwd and nz_rev)
            }
            zero_partners.append(entry)

# Deduplicate by vector content
seen_vecs = set()
unique_partners = []
for e in zero_partners:
    key = tuple(sorted(e['vector']))
    if key not in seen_vecs:
        seen_vecs.add(key)
        unique_partners.append(e)

print(f"\nBilateral family vectors that annihilate q3 (unique):")
print(f"{'Side':>6}  {'Vector':>25}  {'q3*v=0':>8}  {'v*q3=0':>8}  {'bilateral':>10}")
print("-" * 65)
bilateral_count = 0
for e in unique_partners:
    print(f"  {e['side']:>4}  {str(e['vector']):>30}  {str(e['q3*v=0']):>8}  {str(e['v*q3=0']):>8}  {str(e['bilateral']):>10}")
    if e['bilateral']:
        bilateral_count += 1

print(f"\nTotal unique vectors with at least one zero: {len(unique_partners)}")
print(f"Bilateral zero divisor partners of q3: {bilateral_count}")

# Also check the other 5 prime roots explicitly
print(f"\nExplicit check: q3 vs all 5 other prime roots")
for name, v in ROOTS_16D.items():
    if name == 'q3':
        continue
    fwd = sed_product(q3, v)
    rev = sed_product(v, q3)
    ns_fwd = norm_sq(fwd)
    ns_rev = norm_sq(rev)
    print(f"  q3 * {name} (p={PRIME[name]}): |prod|^2={ns_fwd:.0f}  "
          f"q3*v=0:{np.allclose(fwd,0,atol=1e-10)}  "
          f"v*q3=0:{np.allclose(rev,0,atol=1e-10)}")

results['section3_q3_zero_map'] = {
    'unique_zero_partners': unique_partners,
    'bilateral_partner_count': bilateral_count
}

# =============================================================================
# SECTION 4: q2 x q4 full decomposition (norm^2 = 8 explanation)
# =============================================================================
print("\n" + "="*65)
print("SECTION 4: q2 x q4 -- full 16D decomposition (norm^2 = 8)")
print("="*65)

q2_x_q4 = sed_product(q2, q4)
q4_x_q2 = sed_product(q4, q2)
print(f"\nq2 = e5+e10 (positions 5,10): {nonzero_indices(q2)}")
print(f"q4 = e3-e12 (positions 3,12): {nonzero_indices(q4)}")
print(f"\nq2 * q4 = {nonzero_indices(q2_x_q4)}")
print(f"  norm^2 = {norm_sq(q2_x_q4)}")
print(f"\nq4 * q2 = {nonzero_indices(q4_x_q2)}")
print(f"  norm^2 = {norm_sq(q4_x_q2)}")

# What is this vector? Try to decompose as sum of bilateral family roots
print(f"\nDecompose q2*q4 as combination of bilateral family roots:")
# The product lives in the upper half (positions 8-15) or lower half?
lower = q2_x_q4[:8]
upper = q2_x_q4[8:]
print(f"  Lower half (positions 0-7): {nonzero_indices(lower)}")
print(f"  Upper half (positions 8-15): {nonzero_indices(upper)}")
print(f"  |lower|^2 = {norm_sq(lower):.0f}  |upper|^2 = {norm_sq(upper):.0f}")

# Check if q2*q4 is itself in the bilateral family
in_fam_prod, dir_prod, match_prod = find_in_bilateral_family(q2_x_q4, np.zeros(16), bilateral_pairs)
print(f"\nIs q2*q4 itself a bilateral family P-vector? {in_fam_prod}")

# Is q2*q4 = alpha * (some_root + some_root)?
# Find what E8 root (if any) it is
print(f"\nChecking if q2*q4 is a scalar multiple of any bilateral family vector:")
best_match = None
best_cos = 0
for pair in bilateral_pairs:
    for side, v_raw in [('P', pair['P']), ('Q', pair['Q'])]:
        v = np.array(v_raw)
        nv = np.linalg.norm(v)
        np_ = np.linalg.norm(q2_x_q4)
        if nv > 1e-10 and np_ > 1e-10:
            cos_t = abs(np.dot(v, q2_x_q4)) / (nv * np_)
            if cos_t > best_cos:
                best_cos = cos_t
                best_match = (side, nonzero_indices(v), cos_t)

if best_match:
    print(f"  Best alignment: {best_match[0]} = {best_match[1]}, cos={best_match[2]:.6f}")
else:
    print("  No close alignment found")

# Is it a sum of two E8 roots?
print(f"\nAttempting decomposition as sum/difference of pairs of bilateral roots:")
all_roots = []
for pair in bilateral_pairs:
    for side, v_raw in [('P', pair['P']), ('Q', pair['Q'])]:
        v = np.array(v_raw)
        key = tuple(nonzero_indices(v))
        if key not in [tuple(nonzero_indices(r)) for r in all_roots]:
            all_roots.append(v)

found_decomp = []
for i, ri in enumerate(all_roots):
    for j, rj in enumerate(all_roots):
        for signs in [(1,1), (1,-1), (-1,1)]:
            combo = signs[0]*ri + signs[1]*rj
            if np.allclose(combo, q2_x_q4, atol=1e-10):
                found_decomp.append((signs, nonzero_indices(ri), nonzero_indices(rj)))

if found_decomp:
    print(f"  FOUND decompositions:")
    for (s, ri_idx, rj_idx) in found_decomp[:5]:
        print(f"    {s[0]}*{ri_idx} + {s[1]}*{rj_idx}")
else:
    print(f"  Not decomposable as sum/difference of two bilateral roots")

results['section4_q2xq4'] = {
    'q2_x_q4': q2_x_q4.tolist(),
    'q4_x_q2': q4_x_q2.tolist(),
    'norm_sq_q2xq4': norm_sq(q2_x_q4),
    'norm_sq_q4xq2': norm_sq(q4_x_q2),
    'lower_half_nonzero': nonzero_indices(lower),
    'upper_half_nonzero': nonzero_indices(upper),
    'decompositions': [(list(s), ri, rj) for s, ri, rj in found_decomp[:5]]
}

# =============================================================================
# SECTION 5: v5 bridge analysis
# =============================================================================
print("\n" + "="*65)
print("SECTION 5: v5 bridge analysis")
print("Why does v5 (p=5) couple to both Block A (q3) and Block C (q4)?")
print("="*65)

v5 = ROOTS_16D['v5']   # e3+e6 (positions 3,6)
print(f"\nv5 = e3+e6 (positions 3,6): {nonzero_indices(v5)}")
print(f"\nShared sedenion indices:")
print(f"  v5 & q3 (e6+e9): share position 6 (e7 in 1-indexed)")
print(f"  v5 & q4 (e3-e12): share position 3 (e4 in 1-indexed)")
print(f"  v5 & q2 (e5+e10): no shared positions")
print(f"  v5 & v1 (e2-e7): no shared positions")
print(f"  v5 & v4 (e2+e7): no shared positions")

print(f"\nAll sedenion products involving v5:")
for name, v in ROOTS_16D.items():
    if name == 'v5':
        continue
    fwd = sed_product(v5, v)
    rev = sed_product(v, v5)
    s_fwd = round(fwd[0], 6)  # scalar part
    s_rev = round(rev[0], 6)
    ns_fwd = norm_sq(fwd)
    ns_rev = norm_sq(rev)
    print(f"  v5*{name} (p={PRIME[name]}): scalar={s_fwd:+.3f}  |prod|^2={ns_fwd:.0f}  "
          f"  rev_scalar={s_rev:+.3f}  |rev|^2={ns_rev:.0f}")

# Shared index rule: scalar part = -<v5, v> (sedenion inner product)
print(f"\nShared index explanation for scalar parts:")
for name, v in ROOTS_16D.items():
    if name == 'v5':
        continue
    inner = np.dot(v5, v)
    print(f"  <v5, {name}> = {inner:.0f}  => scalar(v5*{name}) = {-inner:.0f}")

results['section5_v5_bridge'] = {
    'v5_indices': nonzero_indices(v5),
    'shared_with_q3': [6],  # position 6 (e7 in 1-indexed)
    'shared_with_q4': [3],  # position 3 (e4 in 1-indexed)
    'products': {}
}
for name, v in ROOTS_16D.items():
    if name == 'v5':
        continue
    fwd = sed_product(v5, v)
    rev = sed_product(v, v5)
    results['section5_v5_bridge']['products'][name] = {
        'scalar': float(fwd[0]),
        'norm_sq': norm_sq(fwd),
        'inner_product_v5_v': float(np.dot(v5, v))
    }

# =============================================================================
# SECTION 6: Multi-partner theorem
# =============================================================================
print("\n" + "="*65)
print("SECTION 6: Multi-partner bilateral zero divisor analysis")
print("="*65)

# Check ALL 6 root pairs for bilateral zero divisor property
print("\nBilateral zero divisor test for all root pairs:")
print(f"{'Pair':>12}  {'Block pair':>10}  {'P*Q=0':>8}  {'Q*P=0':>8}  {'bilateral':>10}  {'in family':>10}")
print("-" * 70)

pair_results = {}
for name_a, va in ROOTS_16D.items():
    for name_b, vb in ROOTS_16D.items():
        if name_a >= name_b:
            continue
        fwd = sed_product(va, vb)
        rev = sed_product(vb, va)
        pq_z = np.allclose(fwd, 0, atol=1e-10)
        qp_z = np.allclose(rev, 0, atol=1e-10)
        bilateral = pq_z and qp_z
        in_fam, _, _ = find_in_bilateral_family(va, vb, bilateral_pairs)
        bp = f"{BLOCK[name_a]}x{BLOCK[name_b]}"
        print(f"  {name_a}*{name_b:>4}  {bp:>10}  {str(pq_z):>8}  {str(qp_z):>8}  {str(bilateral):>10}  {str(in_fam):>10}")
        pair_results[f"{name_a}_{name_b}"] = {
            'block_pair': bp,
            'PxQ_zero': bool(pq_z),
            'QxP_zero': bool(qp_z),
            'bilateral': bool(bilateral),
            'in_18d_family': bool(in_fam)
        }

# Count bilateral partners per root
print(f"\nBilateral zero divisor partners per root (within the 6-root set):")
for name_a in ROOTS_16D:
    partners = [name_b for name_b, vb in ROOTS_16D.items()
                if name_b != name_a
                and pair_results.get(f"{min(name_a,name_b)}_{max(name_a,name_b)}", {}).get('bilateral', False)]
    print(f"  {name_a} (p={PRIME[name_a]}, Block {BLOCK[name_a]}): {len(partners)} partners: {partners}")

results['section6_multipartner'] = pair_results

# =============================================================================
# Summary
# =============================================================================
print("\n" + "="*65)
print("SUMMARY")
print("="*65)

bilateral_q3q2_final = results['section1_q3q2']['is_bilateral_pair']
bilateral_q3q4_final = results['section2_q3q4']['is_bilateral_pair']
in_family_q3q2 = results['section1_q3q2']['in_bilateral_family']
in_family_q3q4 = results['section2_q3q4']['in_bilateral_family']

print(f"""
  (q3, q2) bilateral pair: {bilateral_q3q2_final}   in 18D family: {in_family_q3q2}
  (q3, q4) bilateral pair: {bilateral_q3q4_final}   in 18D family: {in_family_q3q4}
  q2*q4 norm^2: {norm_sq(q2_x_q4):.0f}  (normal E8 product: 0, 2, or 4)

  q3 bilateral partners within 6-root set:
""")
for name_a in ROOTS_16D:
    partners = [name_b for name_b in ROOTS_16D if name_b != name_a
                and pair_results.get(f"{min(name_a,name_b)}_{max(name_a,name_b)}", {}).get('bilateral', False)]
    if partners:
        print(f"    {name_a} (p={PRIME[name_a]}): {partners}")

# ── Save ──────────────────────────────────────────────────────────────────────
def serialize(obj):
    if isinstance(obj, dict):
        return {str(k): serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        return None if v != v else v
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, bool):
        return bool(obj)
    return obj

output = {
    'experiment': 'Phase21B_q3_Anomaly',
    'date': '2026-03-24',
    'results': serialize(results)
}
with open('phase21b_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print("Results saved to phase21b_results.json")
