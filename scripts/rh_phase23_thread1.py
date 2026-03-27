"""
Phase 23 Thread 1: Algebraic Closure of the 6-Root Set Under Sedenion Multiplication
Chavez AI Labs LLC -- March 24, 2026

The 6 prime roots {v1, v4, q3, q2, v5, q4} are NOT closed under sedenion multiplication
-- q2 x q4 = 2*(e6-e9) exits the set (Phase 21B). What is the minimal closed set?

Computations:
1. Product table -- all 36 pairwise sedenion products of the 6 prime roots
2. Closure generation -- iteratively add normalized products until stable
3. New vector characterization -- norm, 5D membership, bilateral partners, prime correspondence
4. Root system identification -- closed under negation? Weyl reflections? Recognizable system?
5. Prime correspondence -- do new directions match primes p=17,19,23 or Phase 20C cross-block roots?

Output: phase23_thread1_results.json + RH_Phase23_Thread1_Results.md
"""

import numpy as np
import json
import importlib.util

# ── Load sedenion multiplication from phase18d ────────────────────────────────
spec = importlib.util.spec_from_file_location('phase18d', 'rh_phase18d_prep.py')
phase18d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase18d)
sed_product = phase18d.sed_product

# ── Root definitions (16D, 0-indexed) ─────────────────────────────────────────
def make16(pairs):
    v = np.zeros(16)
    for idx, s in pairs:
        v[idx] = float(s)
    return v

ROOTS_16D = {
    'v1': make16([(2, 1), (7, -1)]),    # e2-e7  Block A p=7
    'v4': make16([(2, 1), (7,  1)]),    # e2+e7  Block A p=11
    'q3': make16([(6, 1), (9,  1)]),    # e6+e9  Block A p=13  (bilateral hub)
    'q2': make16([(5, 1), (10, 1)]),    # e5+e10 Block B p=3   (Heegner)
    'v5': make16([(3, 1), (6,  1)]),    # e3+e6  Block B p=5
    'q4': make16([(3, 1), (12,-1)]),    # e3-e12 Block C p=2
}
PRIME  = {'v1': 7, 'v4': 11, 'q3': 13, 'q2': 3, 'v5': 5, 'q4': 2}
BLOCK  = {'v1': 'A', 'v4': 'A', 'q3': 'A', 'q2': 'B', 'v5': 'B', 'q4': 'C'}

# 5D fixed subspace projection P5 (from Phase 22):
# Basis: [e2, e7, e3, e6, (e4+e5)/sqrt2]   (indices 2,7,3,6 and (4+5)/sqrt2)
# A 16D vector is in the 5D subspace if it has no components outside positions {2,3,4,5,6,7,9,10,12}
# More precisely: the 5D embedding uses directions Block A {e2,e7}, Block B {e3,e6}, Block C {(e4+e5)/sqrt2}
# We check via projecting onto the 6D span {e2,e7,e3,e6,e4,e5} and then checking the extra direction
SUBSPACE_6D_INDICES = {2, 3, 4, 5, 6, 7}  # the 6D span of the embedding

def norm_sq(v):
    return float(np.dot(v, v))

def in_6D_subspace(v, tol=1e-8):
    """Check if a 16D vector lives entirely in the 6D span {e2,e3,e4,e5,e6,e7}."""
    for i in range(16):
        if i not in SUBSPACE_6D_INDICES and abs(v[i]) > tol:
            return False
    return True

def in_5D_subspace(v, tol=1e-8):
    """Check if a 16D vector lives in the 5D fixed subspace.
    The 5D subspace is spanned by: (e2-e7)/sqrt2, (e2+e7)/sqrt2, (e3+e6)/sqrt2,
    (e3-e6... wait, Block B has e3+e6 and e5+e10 (??)

    Actually the 5D subspace in 6D coordinates is the 5D FIXED subspace of s_alpha4.
    For the embedding, the 5D is spanned by the 5 independent root directions
    after removing the antisymmetric direction u_antisym = (e4-e5)/sqrt2.

    The 6D span is {e2,e7,e3,e6,e4,e5}. Within that, the antisymmetric direction is
    (e4-e5)/sqrt2. The 5D fixed subspace is orthogonal to (e4-e5)/sqrt2 within 6D.
    A vector in 6D is in the 5D iff its component along (e4-e5)/sqrt2 is zero,
    i.e., v[4] == v[5].
    """
    if not in_6D_subspace(v, tol):
        return False
    # Check v[4] == v[5] (no antisymmetric component)
    return abs(v[4] - v[5]) < tol

def scalar_part(v):
    return float(v[0])

def vector_part(v):
    w = v.copy()
    w[0] = 0.0
    return w

def nonzero_indices(v, tol=1e-10):
    return [(i, round(float(v[i]), 6)) for i in range(len(v)) if abs(v[i]) > tol]

def vec_to_str(v, tol=1e-9):
    nz = nonzero_indices(v, tol)
    if not nz:
        return "0"
    parts = []
    for i, c in nz:
        if c == 1:
            parts.append(f"e{i}")
        elif c == -1:
            parts.append(f"-e{i}")
        else:
            parts.append(f"{c:+.4g}*e{i}")
    return " + ".join(parts).replace("+ -", "- ")

def are_parallel(u, v, tol=1e-8):
    """Check if u and v are parallel (one is a scalar multiple of the other)."""
    n1, n2 = norm_sq(u), norm_sq(v)
    if n1 < tol or n2 < tol:
        return False
    dot = abs(float(np.dot(u, v)))
    cos2 = (dot * dot) / (n1 * n2)
    return abs(cos2 - 1.0) < tol

def find_in_set(v, vec_list, tol=1e-8):
    """Return index in vec_list if v is parallel (same direction or opposite) to any element."""
    ns = norm_sq(v)
    if ns < tol:
        return None
    for i, u in enumerate(vec_list):
        nu = norm_sq(u)
        if nu < tol:
            continue
        dot = float(np.dot(v, u))
        cos2 = (dot * dot) / (ns * nu)
        if abs(cos2 - 1.0) < tol:
            return i
    return None

def normalize(v):
    n = np.sqrt(norm_sq(v))
    return v / n

# ──────────────────────────────────────────────────────────────────────────────
print("=" * 68)
print("PHASE 23 THREAD 1: Algebraic Closure of the 6-Root Set")
print("=" * 68)

root_names = list(ROOTS_16D.keys())
root_vecs  = list(ROOTS_16D.values())

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 1: Full 6×6 Product Table
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("COMPUTATION 1: Full 6x6 Product Table")
print("=" * 68)

product_table = {}
NEW_VECTORS_FROM_PRODUCTS = []  # (name, 16D vector) new directions found

for na in root_names:
    product_table[na] = {}
    for nb in root_names:
        va = ROOTS_16D[na]
        vb = ROOTS_16D[nb]
        prod = sed_product(va, vb)
        sc   = scalar_part(prod)
        vp   = vector_part(prod)
        ns   = norm_sq(prod)

        in6d = in_6D_subspace(prod)
        in5d = in_5D_subspace(prod)

        # Check if vector part (normalized) matches any original root
        if norm_sq(vp) > 1e-8:
            norm_vp = normalize(vp)
            idx_in_set = find_in_set(norm_vp, [normalize(r) for r in root_vecs])
        else:
            idx_in_set = None

        product_table[na][nb] = {
            'scalar_part': round(sc, 8),
            'vector_part_indices': nonzero_indices(vp),
            'norm_sq': round(ns, 8),
            'in_6D_subspace': in6d,
            'in_5D_subspace': in5d,
            'vector_part_str': vec_to_str(vp),
            'in_original_set': idx_in_set is not None,
            'original_set_member': root_names[idx_in_set] if idx_in_set is not None else None,
        }

        # Track new unit-norm directions in the vector part
        if norm_sq(vp) > 1e-8:
            unit_vp = vp / np.sqrt(norm_sq(vp))
            if find_in_set(unit_vp, root_vecs) is None:
                # Not in original set — potentially new
                if find_in_set(unit_vp, [r for _, r in NEW_VECTORS_FROM_PRODUCTS]) is None:
                    NEW_VECTORS_FROM_PRODUCTS.append((f"{na}x{nb}", unit_vp * np.sqrt(2)))  # store as norm^2=2 version

print("\nProduct table (scalar | vector | norm² | in5D | in original set):")
print(f"{'':6} | " + " | ".join(f"{nb:8}" for nb in root_names))
print("-" * 80)
for na in root_names:
    row_parts = []
    for nb in root_names:
        e = product_table[na][nb]
        if e['norm_sq'] < 1e-8:
            row_parts.append("   ZERO  ")
        elif e['in_original_set']:
            row_parts.append(f" in-set  ")
        elif e['in_6D_subspace']:
            row_parts.append(f" in6D   ")
        else:
            row_parts.append(f" EXITS  ")
    print(f"{na:6} | " + " | ".join(row_parts))

print("\nDetailed exits from 6D subspace:")
exit_count = 0
for na in root_names:
    for nb in root_names:
        e = product_table[na][nb]
        if e['norm_sq'] > 1e-8 and not e['in_6D_subspace']:
            print(f"  {na} x {nb}: sc={e['scalar_part']}, vec={e['vector_part_str']}, norm²={e['norm_sq']:.4f}, in5D={e['in_5D_subspace']}")
            exit_count += 1

if exit_count == 0:
    print("  None.")

print("\nAll zero products (bilateral candidates):")
zero_count = 0
for na in root_names:
    for nb in root_names:
        e = product_table[na][nb]
        if e['norm_sq'] < 1e-8:
            print(f"  {na} x {nb} = 0")
            zero_count += 1
print(f"  Total: {zero_count}")

print("\nProducts staying in 6D with non-zero scalar:")
for na in root_names:
    for nb in root_names:
        e = product_table[na][nb]
        if e['norm_sq'] > 1e-8 and e['in_6D_subspace'] and abs(e['scalar_part']) > 1e-8:
            print(f"  {na} x {nb}: sc={e['scalar_part']}, vec={e['vector_part_str']}, norm²={e['norm_sq']:.4f}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 2: Closure Generation
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("COMPUTATION 2: Iterative Closure Generation")
print("=" * 68)

# Start with the 6 prime roots (as norm^2=2 vectors)
closed_set = [(name, vec.copy()) for name, vec in ROOTS_16D.items()]
generation = {name: 0 for name in root_names}  # which generation each vector was added

MAX_ITERS = 20
added_per_iter = []

print(f"\nStarting set: {[n for n, _ in closed_set]}")

for iteration in range(MAX_ITERS):
    new_this_iter = []
    n_current = len(closed_set)

    for i in range(n_current):
        for j in range(n_current):
            na, va = closed_set[i]
            nb, vb = closed_set[j]
            prod = sed_product(va, vb)
            vp = vector_part(prod)
            ns_vp = norm_sq(vp)

            if ns_vp < 1e-8:
                continue  # zero product or scalar only

            # Normalize to unit vector, then scale to norm^2 = 2 (E8 first shell)
            unit = vp / np.sqrt(ns_vp)
            new_candidate = unit * np.sqrt(2.0)

            # Check if this direction is already in closed_set
            existing = [v for _, v in closed_set + new_this_iter]
            if find_in_set(new_candidate, existing) is None:
                new_name = f"gen{iteration+1}_{na}x{nb}"
                new_this_iter.append((new_name, new_candidate))
                generation[new_name] = iteration + 1

    if not new_this_iter:
        print(f"\nClosure reached at iteration {iteration+1} (no new vectors).")
        break

    print(f"Iteration {iteration+1}: {len(new_this_iter)} new vectors added")
    for name, vec in new_this_iter:
        print(f"  {name}: {vec_to_str(vec)}, norm²={norm_sq(vec):.4f}")

    closed_set.extend(new_this_iter)
    added_per_iter.append(len(new_this_iter))

    if iteration == MAX_ITERS - 1:
        print(f"\nWARNING: Did not converge in {MAX_ITERS} iterations!")

print(f"\nFinal closed set size: {len(closed_set)} vectors")
print(f"Original set: 6 vectors (primes p=2,3,5,7,11,13)")
print(f"New vectors generated: {len(closed_set) - 6}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 3: New Vector Characterization
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("COMPUTATION 3: Characterization of New Vectors")
print("=" * 68)

# Load bilateral family for partner checking
with open('p18d_enumeration.json', 'r') as f:
    enum_data = json.load(f)
bilateral_pairs_data = enum_data['pairs']

def bilateral_partners_in_family(v, pairs_data, tol=1e-8):
    """Find which bilateral family members annihilate v bilaterally."""
    partners = []
    for pair in pairs_data:
        P = np.array(pair['P_16D'])
        Q = np.array(pair['Q_16D'])
        for candidate_name, candidate in [('P', P), ('Q', Q)]:
            pv = sed_product(candidate, v)
            vp2 = sed_product(v, candidate)
            if norm_sq(pv) < tol and norm_sq(vp2) < tol:
                partners.append((pair['id'], candidate_name))
    return partners

# Also load bilateral family vectors as 16D arrays
bilateral_all_vecs = []
for pair in bilateral_pairs_data:
    P = np.array(pair['P_16D'])
    Q = np.array(pair['Q_16D'])
    bilateral_all_vecs.append(P)
    bilateral_all_vecs.append(Q)

def in_bilateral_family(v, tol=1e-8):
    """Check if v (normalized) is parallel to any member of the bilateral family."""
    return find_in_set(v, bilateral_all_vecs) is not None

# E8 first shell check: norm^2 = 2
def on_E8_first_shell(v, tol=1e-8):
    return abs(norm_sq(v) - 2.0) < tol

new_vectors_info = []
for name, vec in closed_set:
    if name not in ROOTS_16D:
        ns = norm_sq(vec)
        in5d = in_5D_subspace(vec)
        in6d = in_6D_subspace(vec)
        in_bil = in_bilateral_family(vec)
        on_e8 = on_E8_first_shell(vec)
        nz = nonzero_indices(vec)

        print(f"\n{name}:")
        print(f"  Expression: {vec_to_str(vec)}")
        print(f"  norm² = {ns:.4f}")
        print(f"  In 6D subspace: {in6d}")
        print(f"  In 5D subspace: {in5d}")
        print(f"  On E8 first shell (norm²=2): {on_e8}")
        print(f"  In bilateral family: {in_bil}")
        print(f"  Nonzero indices: {nz}")

        new_vectors_info.append({
            'name': name,
            'expression': vec_to_str(vec),
            'nonzero_indices': nz,
            'norm_sq': round(ns, 6),
            'in_6D_subspace': in6d,
            'in_5D_subspace': in5d,
            'on_E8_first_shell': on_e8,
            'in_bilateral_family': in_bil,
            'generation': generation.get(name, -1),
        })

if not new_vectors_info:
    print("No new vectors generated — set is already closed!")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 4: Root System Identification
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("COMPUTATION 4: Root System Identification")
print("=" * 68)

all_vecs = [vec for _, vec in closed_set]
all_names = [name for name, _ in closed_set]
n_vecs = len(all_vecs)

print(f"\nTotal vectors in closed set: {n_vecs}")
print(f"Checking root system properties...\n")

# Check 1: Closed under negation?
negation_closed = True
negation_missing = []
for name, vec in closed_set:
    neg = -vec
    if find_in_set(neg, all_vecs) is None:
        negation_closed = False
        negation_missing.append(name)
print(f"Closed under negation: {negation_closed}")
if negation_missing:
    print(f"  Missing negatives: {negation_missing}")

# Check 2: Gram matrix
print(f"\nGram matrix (inner products):")
gram = np.zeros((n_vecs, n_vecs))
for i in range(n_vecs):
    for j in range(n_vecs):
        gram[i, j] = float(np.dot(all_vecs[i], all_vecs[j]))

# Count inner product values
ip_counts = {}
for i in range(n_vecs):
    for j in range(n_vecs):
        v = round(gram[i, j], 4)
        ip_counts[v] = ip_counts.get(v, 0) + 1

print(f"Inner product distribution: {dict(sorted(ip_counts.items()))}")

# Check 3: Rank (dimension of span)
if n_vecs > 0:
    F = np.array(all_vecs)  # shape: (n_vecs, 16)
    rank = np.linalg.matrix_rank(F, tol=1e-8)
    print(f"Rank of closed set (span dimension): {rank}")

# Check 4: Weyl reflections — are new vectors images of old under Weyl reflections?
print("\nWeyl reflection check (s_alpha: v -> v - 2<v,alpha>/<alpha,alpha> * alpha):")
weyl_closed = True
weyl_missing = []
for i, (ni, vi) in enumerate(closed_set):
    for j, (nj, vj) in enumerate(closed_set):
        # Weyl reflection of vi in hyperplane perpendicular to vj
        ip = float(np.dot(vi, vj))
        ns_j = norm_sq(vj)
        if ns_j < 1e-8:
            continue
        reflected = vi - (2 * ip / ns_j) * vj
        # Check if reflected is in the set (or zero)
        ns_r = norm_sq(reflected)
        if ns_r > 1e-8:
            if find_in_set(reflected / np.sqrt(ns_r), [v / np.sqrt(norm_sq(v)) for v in all_vecs if norm_sq(v) > 1e-8]) is None:
                weyl_closed = False
                weyl_missing.append((ni, nj, vec_to_str(reflected)))

print(f"Closed under Weyl reflections: {weyl_closed}")
if weyl_missing[:5]:
    print(f"  Examples not in set: {weyl_missing[:5]}")
if len(weyl_missing) > 5:
    print(f"  ... and {len(weyl_missing)-5} more")

# Compare sizes with known root systems
print(f"\nComparison with known root systems (rank {rank}):")
known = {
    'A1': 2, 'A2': 6, 'A3': 12, 'A4': 20,
    'B2/C2': 8, 'B3': 18, 'B4': 32,
    'D3': 12, 'D4': 24, 'D5': 40, 'D6': 60,
    '(A1)^2': 4, '(A1)^3': 6, '(A1)^4': 8, '(A1)^5': 10, '(A1)^6': 12,
    'A2+A1': 8, 'G2': 12, 'F4': 48,
    'E6': 72, 'E7': 126, 'E8': 240,
}
print(f"  Current set size: {n_vecs}")
for rname, rsize in sorted(known.items(), key=lambda x: x[1]):
    if abs(rsize - n_vecs) <= 2:
        print(f"  *** MATCH or near-match: {rname} has {rsize} roots ***")
    elif rsize == n_vecs:
        print(f"  EXACT MATCH: {rname}")

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTATION 5: Prime Correspondence
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("COMPUTATION 5: Prime Correspondence of New Vectors")
print("=" * 68)

# Phase 20C cross-block directions for p=17,19,23
# These are "D6 minus both-negative" directions not in the original 6 prime roots
# We check if new vectors match those used in the 9-prime formula
# The 9-prime formula uses cross-block roots; from Phase 20B/20C notes:
# p=17 -> v2=u_antisym (structurally impossible), p=17,19,23 use cross-block D6 roots
# The D6 roots (Phase 19 T1) are all e_i + eps_j*e_j with i<j in {1..6} and not both negative

# Candidate prime assignments: check if new vectors match any (A1)^6 (A1)^n root directions
# or if they have a natural "log(p)/sqrt(p) * r_p" interpretation

print("\nNew vectors and their potential prime correspondences:")
for info in new_vectors_info:
    name = info['name']
    vec = next(v for n, v in closed_set if n == name)
    nz = nonzero_indices(vec)
    print(f"\n{name}: {info['expression']}")
    print(f"  Nonzero indices: {nz}")
    print(f"  In 6D subspace: {info['in_6D_subspace']}")
    print(f"  In bilateral family: {info['in_bilateral_family']}")

    # Check against all D6 root directions (not just original 6)
    # A D6 direction in {e1..e6} (0-indexed {1..6}) is eps_i * e_i + eps_j * e_j
    # with (eps_i, eps_j) != (-1,-1)
    # Original 6 use {e2,e7,e3,e6,e4,e5} — note e7 and e5,e10 are outside {1..6}!
    # Actually the original roots use 16D positions: v1 uses positions {2,7}
    # The D6 structure from Phase 19 lives in 8D positions {1..6}
    # Let me just check if the vector corresponds to any prime by index pattern

    # Simple check: does this vector use only two indices? If so, potentially a root.
    if len(nz) == 2:
        i1, c1 = nz[0]
        i2, c2 = nz[1]
        print(f"  Two-index vector: e{i1}{'+'if c1>0 else ''}{c1}*e{i1} ... using indices ({i1},{i2})")

# Also check: is the new vector the same as a bilateral family member (Phase 18D)?
print("\nChecking if new vectors match Phase 18D bilateral family members:")
for info in new_vectors_info:
    name = info['name']
    vec = next(v for n, v in closed_set if n == name)
    if info['in_bilateral_family']:
        print(f"  {name}: YES — in bilateral family")
        idx = find_in_set(vec, bilateral_all_vecs)
        if idx is not None:
            pair_idx = idx // 2
            pq = 'P' if idx % 2 == 0 else 'Q'
            pair_id = bilateral_pairs_data[pair_idx]['id']
            print(f"    -> bilateral pair id={pair_id}, vector={pq}")
    else:
        print(f"  {name}: NOT in bilateral family")

# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 68)
print("OVERALL SUMMARY")
print("=" * 68)
print(f"\nOriginal set: 6 vectors ({', '.join(root_names)})")
print(f"Closure size: {len(closed_set)} vectors")
print(f"New vectors:  {len(new_vectors_info)}")
print(f"\nClosed under negation: {negation_closed}")
print(f"Closed under Weyl reflections: {weyl_closed}")
print(f"Rank (span dimension): {rank}")

if not negation_closed:
    print(f"\nNOTE: Set is NOT closed under negation.")
    print(f"For a root system, must include all ±alpha pairs.")
    print(f"Adding negatives would give {n_vecs + len(negation_missing)} vectors.")

print(f"\nProduct table summary:")
zero_prods = sum(1 for na in root_names for nb in root_names
                  if product_table[na][nb]['norm_sq'] < 1e-8)
in_set_prods = sum(1 for na in root_names for nb in root_names
                   if product_table[na][nb]['norm_sq'] > 1e-8 and
                   product_table[na][nb]['in_original_set'])
in_6d_prods = sum(1 for na in root_names for nb in root_names
                  if product_table[na][nb]['norm_sq'] > 1e-8 and
                  product_table[na][nb]['in_6D_subspace'])
exits_prods = 36 - zero_prods - in_6d_prods
print(f"  Zero products: {zero_prods}/36")
print(f"  Products in original set: {in_set_prods}/36")
print(f"  Products in 6D subspace: {in_6d_prods}/36")
print(f"  Products exiting 6D subspace: {exits_prods}/36")

# ═══════════════════════════════════════════════════════════════════════════════
# SAVE RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
def safe(x):
    if isinstance(x, (np.bool_,)):          return bool(x)
    if isinstance(x, (np.integer,)):        return int(x)
    if isinstance(x, (np.floating, float)):
        if np.isnan(x) or np.isinf(x):     return None
        return float(x)
    if isinstance(x, np.ndarray):          return x.tolist()
    return x

def deep_safe(obj):
    if isinstance(obj, dict):
        return {k: deep_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [deep_safe(v) for v in obj]
    return safe(obj)

# Build closed set list for JSON
closed_set_json = []
for name, vec in closed_set:
    closed_set_json.append({
        'name': name,
        'expression': vec_to_str(vec),
        'vector_16D': vec.tolist(),
        'norm_sq': round(norm_sq(vec), 6),
        'in_6D_subspace': in_6D_subspace(vec),
        'in_5D_subspace': in_5D_subspace(vec),
        'generation': generation.get(name, 0),
        'original': name in ROOTS_16D,
    })

results = {
    'experiment': 'Phase 23 Thread 1 — Algebraic Closure of 6-Root Set',
    'date': '2026-03-24',
    'computation_1_product_table': {
        'root_names': root_names,
        'products': deep_safe(product_table),
        'summary': {
            'zero_products': zero_prods,
            'products_in_original_set': in_set_prods,
            'products_in_6D_subspace': in_6d_prods,
            'products_exiting_6D': exits_prods,
        }
    },
    'computation_2_closure': {
        'original_size': 6,
        'closed_size': len(closed_set),
        'n_new_vectors': len(new_vectors_info),
        'closed_set': closed_set_json,
        'iterations_to_converge': len(added_per_iter) + 1,
    },
    'computation_3_new_vectors': deep_safe(new_vectors_info),
    'computation_4_root_system': {
        'closed_under_negation': bool(negation_closed),
        'negation_missing': negation_missing,
        'closed_under_weyl_reflections': bool(weyl_closed),
        'weyl_missing_count': len(weyl_missing),
        'rank': int(rank),
        'inner_product_distribution': {str(k): v for k, v in ip_counts.items()},
        'gram_matrix': gram.tolist(),
    },
    'computation_5_prime_correspondence': {
        'new_vector_details': deep_safe(new_vectors_info),
    },
    'headline_results': {
        'original_set_size': 6,
        'closed_set_size': len(closed_set),
        'closed_under_negation': bool(negation_closed),
        'closed_under_weyl': bool(weyl_closed),
        'rank': int(rank),
        'zero_products_in_36': zero_prods,
        'exits_from_6D': exits_prods,
    }
}

with open('phase23_thread1_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to phase23_thread1_results.json")
print("Next: Write RH_Phase23_Thread1_Results.md")
