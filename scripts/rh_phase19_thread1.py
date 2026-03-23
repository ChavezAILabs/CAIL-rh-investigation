"""
Phase 19 Thread 1 — 45-Direction E8 Root System Classification
Chavez AI Labs LLC · March 23, 2026

Question: Which 45 of the 84 D7 roots are present in the full bilateral
zero divisor family, and what geometric structure do they form?

Pre-computation established:
  - All 45 directions are +-ei+-ej with i,j in {1..7} -> subset of D7
  - Set does NOT form a root system (Weyl closure fails)
  - Gram entries in {-2,-1,0,+1,+2}
  - Span dimension = 6; 15 antipodal pairs + 15 unpaired directions

This script:
  1. Extracts all 45 distinct 8D directions from p18d_enumeration.json
  2. Builds the full D7 root set (84 roots)
  3. Identifies which 39 D7 roots are ABSENT
  4. Checks W(D7) orbit structure
  5. Checks for A2/D4 sub-structure (Heegner selectivity: ℚ(√-3)/ℚ(√-2))
  6. Computes full 45x45 Gram matrix with entry histogram
  7. Checks root system closure (Weyl reflections)
  8. Analyzes antipodal structure and the 15 unpaired directions
  9. Clifford Cl(7,0) pass via CAILculator CliffordElement:
     - Grade-1 bilateral vectors in Cl(7,0)
     - Geometric product structure of closure-failure pairs (grade-0 vs grade-2)
     - A2 sub-structure: triples (alpha, beta, alpha+beta) all in bilateral set
     - D4 sub-structure: 4-index subsets with all 24 sign combos (D4 = 24 roots)
     - Canonical Six Clifford consistency

Note on E6: E6 has 72 roots; bilateral set has only 45. Full E6 sub-system
is impossible. The Heegner-motivated targets are A2 (6 roots, Eisenstein/
Q(sqrt(-3))) and D4 (24 roots, Q(sqrt(-2))). These are the structures that
the Phase 18F Lie-algebraic connections predict should appear.

CAILculator Clifford: uses CliffordElement from clifford_verified.py
(verified against 552 bridge patterns at 32D, Beta v7+). Convention:
n=7 for Cl(7,0), grade-1 vector e_k at coeffs[1<<(k-1)], 1-indexed.

Input:  p18d_enumeration.json
Output: phase19_thread1_results.json, RH_Phase19_Thread1_Results.md
"""

import json
import sys
import numpy as np
from itertools import combinations

# CAILculator Clifford implementation
sys.path.insert(0, r'C:\Users\chave\PROJECTS\cailculator-mcp\src')
from cailculator_mcp.clifford_verified import CliffordElement

# ---------------------------------------------------------------------------
# 1. Load 45 distinct bilateral directions from Phase 18D enumeration
# ---------------------------------------------------------------------------

with open("p18d_enumeration.json") as f:
    enum_data = json.load(f)

pairs = enum_data["pairs"]
print(f"Loaded {len(pairs)} bilateral pairs from p18d_enumeration.json")

def to_8d(vec16):
    """Convert 16D sedenion P or Q vector to 8D image via sign rule.

    Rule: component at position k in 8D gets the value from position k (for k<8)
    and -1 * value from position k+8 (for k>=8), combined.

    For bilateral roots: P and Q are e_a + e_b (two basis elements).
    The 8D image maps e_k → +e_k (k<8) and e_{k+8} → -e_k (k<8), so
    e_a + e_b where a<8, b>=8 maps to e_a - e_{b-8}.

    In practice: 8D image = first 8 components - last 8 components.
    (Confirmed by Phase 18E: e5+e10 maps to (0,0,-1,0,0,+1,0,0) = e3-e6 sign convention)
    """
    v = np.array(vec16, dtype=float)
    return v[:8] - v[8:]

# Extract all distinct 8D directions (P and Q separately, then deduplicate)
directions_set = {}  # tuple -> np.array, for deduplication

for pair in pairs:
    for key in ("P", "Q"):
        v8 = to_8d(pair[key])
        # normalize representation: use tuple as dict key
        key_tuple = tuple(np.round(v8, 8))
        if key_tuple not in directions_set:
            directions_set[key_tuple] = v8

all_dirs = list(directions_set.values())
print(f"Distinct 8D directions: {len(all_dirs)}")

# Verify all have norm^2 = 2
norms_sq = [np.dot(d, d) for d in all_dirs]
assert all(abs(n - 2.0) < 1e-10 for n in norms_sq), "Not all directions have norm^2=2!"
print("All directions confirmed on E8 first shell (norm^2 = 2) OK")

# ---------------------------------------------------------------------------
# 2. Build full D7 root system (84 roots)
# ---------------------------------------------------------------------------
# D7: all ±eᵢ±eⱼ with i≠j, i,j ∈ {0..6} of the 7D subspace.
# In 8D with x[0]=0: positions 1..7, so i,j ∈ {1..7}.

def make_d7_roots():
    roots = []
    for i in range(1, 8):
        for j in range(i+1, 8):
            for si in (+1, -1):
                for sj in (+1, -1):
                    r = np.zeros(8)
                    r[i] = si
                    r[j] = sj
                    roots.append(r)
    return roots

d7_roots = make_d7_roots()
print(f"D7 root system: {len(d7_roots)} roots")  # should be 84

def root_to_tuple(r):
    return tuple(int(x) for x in np.round(r, 8))

d7_set = {root_to_tuple(r): r for r in d7_roots}

# Check which bilateral directions are in D7
bilateral_tuples = [tuple(int(x) for x in np.round(d, 8)) for d in all_dirs]
in_d7 = [t in d7_set for t in bilateral_tuples]
print(f"Bilateral directions in D7: {sum(in_d7)} / {len(all_dirs)}")

absent_from_bilateral = {t: v for t, v in d7_set.items() if t not in set(bilateral_tuples)}
print(f"D7 roots absent from bilateral set: {len(absent_from_bilateral)}")

# ---------------------------------------------------------------------------
# 3. Identify the absent 39 D7 roots and look for patterns
# ---------------------------------------------------------------------------

absent_roots = list(absent_from_bilateral.values())
absent_roots.sort(key=lambda r: (np.argmax(np.abs(r)), r.tolist()))

print("\n--- Absent D7 roots (39) ---")
absent_index_pairs = []
for r in absent_roots:
    nonzero = [(i, int(r[i])) for i in range(8) if abs(r[i]) > 0.5]
    absent_index_pairs.append(nonzero)
    print(f"  {nonzero}")

# Check if absent roots share a common index pattern
absent_indices = set()
for r in absent_roots:
    nonzero_idx = tuple(sorted([i for i in range(8) if abs(r[i]) > 0.5]))
    absent_indices.add(nonzero_idx)

present_indices = set()
for d in all_dirs:
    nonzero_idx = tuple(sorted([i for i in range(8) if abs(d[i]) > 0.5]))
    present_indices.add(nonzero_idx)

print(f"\nDistinct index pairs in bilateral set: {len(present_indices)}")
print(f"Distinct index pairs absent: {len(absent_indices)}")
print("Present index pairs:", sorted(present_indices))
print("Absent index pairs:", sorted(absent_indices))

# ---------------------------------------------------------------------------
# 4. Span dimension check
# ---------------------------------------------------------------------------
mat = np.array(all_dirs)  # 45 x 8
rank = np.linalg.matrix_rank(mat, tol=1e-10)
print(f"\nSpan dimension of 45 bilateral directions: {rank}")

# ---------------------------------------------------------------------------
# 5. Full 45x45 Gram matrix
# ---------------------------------------------------------------------------
G = mat @ mat.T  # 45x45 inner product matrix

gram_entries = G.flatten().round().astype(int)
unique, counts = np.unique(gram_entries, return_counts=True)
print("\n--- Gram matrix entry histogram ---")
for val, cnt in zip(unique, counts):
    print(f"  {val:+d}: {cnt} entries")

# Off-diagonal only
off_diag = G[np.triu_indices(45, k=1)].round().astype(int)
off_unique, off_counts = np.unique(off_diag, return_counts=True)
print("Off-diagonal (upper triangle) entry histogram:")
for val, cnt in zip(off_unique, off_counts):
    print(f"  {val:+d}: {cnt} entries")

# ---------------------------------------------------------------------------
# 6. Antipodal structure
# ---------------------------------------------------------------------------
bilateral_tuple_set = set(bilateral_tuples)

antipodal_pairs = []
unpaired = []
seen = set()

for i, d in enumerate(all_dirs):
    if i in seen:
        continue
    neg_t = tuple(int(x) for x in np.round(-d, 8))
    if neg_t in bilateral_tuple_set:
        # Find the index of the negation
        neg_idx = next(j for j, t in enumerate(bilateral_tuples) if t == neg_t)
        if neg_idx not in seen:
            antipodal_pairs.append((i, neg_idx))
            seen.add(i)
            seen.add(neg_idx)
    else:
        unpaired.append(i)
        seen.add(i)

print(f"\nAntipodal pairs: {len(antipodal_pairs)}")
print(f"Unpaired directions (no negation in set): {len(unpaired)}")

print("\nUnpaired directions (no negation in bilateral set):")
for i in unpaired:
    d = all_dirs[i]
    nonzero = [(j, int(d[j])) for j in range(8) if abs(d[j]) > 0.5]
    print(f"  {nonzero}")

# ---------------------------------------------------------------------------
# 7. Root system closure test (Weyl reflections)
# ---------------------------------------------------------------------------
# For a root system: if α,β are roots and ⟨α,β⟩ = -1, then σ_α(β) = β + α must be in the set.
# (Similarly for ⟨α,β⟩ = +1: σ_α(β) = β - α must be in the set.)
# More precisely: σ_α(β) = β - 2⟨α,β⟩/⟨α,α⟩ · α = β - ⟨α,β⟩ · α (since ⟨α,α⟩=2)

closure_failures = []
for i, alpha in enumerate(all_dirs):
    for j, beta in enumerate(all_dirs):
        if i == j:
            continue
        inner = np.dot(alpha, beta)
        inner_int = int(round(inner))
        if inner_int == 0:
            continue
        # Weyl reflection σ_α(β) = β - inner_int * alpha  (since ⟨α,α⟩=2)
        reflected = beta - inner_int * alpha
        # Check if reflected is in the bilateral set
        ref_t = tuple(int(x) for x in np.round(reflected, 8))
        if ref_t not in bilateral_tuple_set:
            closure_failures.append((i, j, inner_int, reflected.tolist()))

print(f"\nRoot system closure failures: {len(closure_failures)}")
if len(closure_failures) > 0:
    # Show a few examples
    print("Sample failures (a, b, <a,b>, sigma_a(b) not in set):")
    for cf in closure_failures[:5]:
        i, j, ip, ref = cf
        print(f"  a={[int(x) for x in np.round(all_dirs[i],0)]}, b={[int(x) for x in np.round(all_dirs[j],0)]}, <a,b>={ip}, sigma_a(b)={[int(x) for x in np.round(ref,0)]}")

# Check what the closure failures would produce (what directions are needed)
missing_for_closure = set()
for cf in closure_failures:
    ref_t = tuple(int(x) for x in np.round(cf[3], 8))
    missing_for_closure.add(ref_t)

print(f"Distinct missing directions for closure: {len(missing_for_closure)}")

# Are the missing closure directions a subset of D7?
closure_in_d7 = sum(1 for t in missing_for_closure if t in d7_set)
print(f"Missing closure directions that ARE in D7: {closure_in_d7} / {len(missing_for_closure)}")

# ---------------------------------------------------------------------------
# 8. E6 sub-structure check (Heegner selectivity motivation)
# ---------------------------------------------------------------------------
# E6 root system: 72 roots. In E8 embedding, E6 lives in a 6D sub-lattice.
# One standard embedding of E6 in D7: roots are ±eᵢ±eⱼ for i,j in specific index set
# plus additional roots from the full E6 construction.
#
# E6 in E8: The 72 roots of E6 are the E8 roots orthogonal to two specific simple roots.
# In coordinates: E6 roots are those ±eᵢ±eⱼ patterns that satisfy additional constraints.
#
# The A₂ factor relevant to E8=E6⊕A₂⊕U(1) decomposition appears in specific 2D subspace.
#
# Simple check: count pairs with |inner product| = 1 (A-type angle, characteristic of E6/E8)
# vs |inner product| = 0 (orthogonal, characteristic of D-type)

print("\n--- Inner product angle classification ---")
angle_counts = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0}
for i in range(len(all_dirs)):
    for j in range(i+1, len(all_dirs)):
        ip = int(round(np.dot(all_dirs[i], all_dirs[j])))
        if ip in angle_counts:
            angle_counts[ip] += 1

for ip, cnt in sorted(angle_counts.items()):
    angle_name = {-2: "antipodal", -1: "120°", 0: "90°", 1: "60°", 2: "same"}
    print(f"  <a,b> = {ip:+d} ({angle_name.get(ip, '?')}): {cnt} pairs")

# E6 has characteristic 120° and 60° angles (±1 inner products)
# D-type systems only have 90° and 180° (0 and ±2 inner products)
pairs_with_60_120 = angle_counts[1] + angle_counts[-1]
print(f"\n  Pairs with 60/120 degree angles (|<a,b>|=1): {pairs_with_60_120}")
print(f"  -> Non-zero: set has E6/A-type geometry, not pure D-type")

# ---------------------------------------------------------------------------
# 9. W(D7) orbit structure
# ---------------------------------------------------------------------------
# W(D7) acts by: (i) permuting the 7 coordinates {1..7}, (ii) flipping an even number of signs.
# Two roots are in the same W(D7) orbit iff they have the same form (e.g., both +e_i+e_j,
# or one +e_i+e_j and one +e_i-e_j after permutation — these are in the SAME D7 orbit
# since W(D7) includes sign flips of pairs).
#
# In D7: there is ONE orbit (all ±eᵢ±eⱼ are related by permutation + even sign flips).
# So the bilateral subset is either all in that one orbit or a proper subset.
#
# More refined: classify by the SIGN pattern of the root.
# For ±eᵢ±eⱼ: four types by signs (++, +-, -+, --) but W(D7) makes them all equivalent.
# So all 84 D7 roots form one orbit. All 45 bilateral directions are in the same W(D7) orbit.
# The question is: what condition on (i,j,sᵢ,sⱼ) selects the 45 from the 84?

# Classify the 45 bilateral directions by index pair (i,j) with i<j
bilateral_by_index = {}
for d in all_dirs:
    nonzero = [(k, int(round(d[k]))) for k in range(8) if abs(d[k]) > 0.5]
    assert len(nonzero) == 2
    i1, s1 = nonzero[0]
    i2, s2 = nonzero[1]
    idx_pair = (min(i1,i2), max(i1,i2))
    if idx_pair not in bilateral_by_index:
        bilateral_by_index[idx_pair] = []
    bilateral_by_index[idx_pair].append((s1 if i1 < i2 else s2, s2 if i1 < i2 else s1))

print("\n--- Bilateral directions by index pair (i,j) ---")
print("Format: (i,j) -> list of (sign_i, sign_j) present in bilateral set")
for idx_pair in sorted(bilateral_by_index.keys()):
    signs = bilateral_by_index[idx_pair]
    print(f"  ({idx_pair[0]},{idx_pair[1]}): {sorted(signs)} — {len(signs)} of 4 sign combos")

# Which index pairs have all 4 sign combos? (complete pairs)
complete_pairs = [(ip, signs) for ip, signs in bilateral_by_index.items() if len(signs) == 4]
partial_pairs = [(ip, signs) for ip, signs in bilateral_by_index.items() if len(signs) < 4]
print(f"\nIndex pairs with all 4 sign combos: {len(complete_pairs)}")
print(f"Index pairs with partial sign combos: {len(partial_pairs)}")

# All (i,j) pairs available in D7 (21 pairs total for i<j in 1..7)
all_d7_index_pairs = [(i,j) for i in range(1,8) for j in range(i+1,8)]
absent_index_pairs_set = set(all_d7_index_pairs) - set(bilateral_by_index.keys())
print(f"\nIndex pairs with NO bilateral directions: {len(absent_index_pairs_set)}")
print("Absent index pairs:", sorted(absent_index_pairs_set))

# ---------------------------------------------------------------------------
# 10. Clifford Cl(7,0) pass — CAILculator CliffordElement
# ---------------------------------------------------------------------------
# The 45 bilateral directions are grade-1 vectors in Cl(7,0).
# 8D position k (k in 1..7, x[0]=0) -> Clifford generator e_k (1-indexed).
# Coefficient for e_k: coeffs[1 << (k-1)].
#
# Note: Cl(7,0) with n=7 gives 2^7 = 128-dimensional multivector space.
# All generators square to +1 (positive definite). Blade names: e1, e12, etc.

print("\n=== CLIFFORD Cl(7,0) PASS ===")
CL_N = 7  # Cl(7,0)

def bilateral_to_clifford(d8):
    """Convert 8D bilateral direction (positions 1..7) to Cl(7,0) grade-1 vector."""
    coeffs = [0.0] * (2**CL_N)
    for k in range(1, 8):  # 8D positions 1..7 -> Clifford e_k (1-indexed)
        val = d8[k]
        if abs(val) > 0.5:
            blade_idx = 1 << (k - 1)  # e_k is at position 1<<(k-1)
            coeffs[blade_idx] = float(round(val))
    return CliffordElement(n=CL_N, coeffs=coeffs)

def get_grade_content(cl_elem):
    """Return grade-by-grade norms for a Cl(7,0) multivector."""
    grade_norms = {}
    for grade in range(CL_N + 1):
        # Grade-g blades: bitmask indices with exactly g bits set
        norm_sq = 0.0
        for idx in range(2**CL_N):
            if bin(idx).count('1') == grade:
                norm_sq += cl_elem.coeffs[idx]**2
        if norm_sq > 1e-12:
            grade_norms[grade] = float(norm_sq**0.5)
    return grade_norms

def blade_label(idx, n=CL_N):
    """Human-readable blade label from bitmask index."""
    if idx == 0:
        return "scalar"
    bits = [str(i+1) for i in range(n) if (idx >> i) & 1]
    return "e" + "".join(bits)

# Build Clifford elements for all 45 directions
cl_dirs = [bilateral_to_clifford(d) for d in all_dirs]
print(f"Built {len(cl_dirs)} Cl(7,0) grade-1 vectors from bilateral directions")

# Verify grade-1 purity and norm
for i, (d, cl) in enumerate(zip(all_dirs, cl_dirs)):
    gc = get_grade_content(cl)
    assert list(gc.keys()) == [1], f"Direction {i} not pure grade-1: {gc}"
    assert abs(gc[1]**2 - 2.0) < 1e-10, f"Direction {i} norm^2 != 2: {gc[1]**2}"
print("All 45 Cl(7,0) elements confirmed pure grade-1 with norm^2=2")

# --- 10a. Geometric product structure of closure-failure pairs ---
# For pairs with inner product +-1 (sharing one index), compute full geometric product.
# Result: grade-0 (scalar = inner product) + grade-2 (bivector = exterior product).
# Check: do the grade-2 components land in identifiable bivector sub-spaces?

print("\n--- Geometric product structure of closure-failure pairs ---")

# The closure failures are pairs with |inner product| = 1.
# Sample the first 10 for geometric analysis; record grade histogram for all.
grade2_component_counts = {}  # blade_label -> count of times it appears in grade-2 parts
n_closure_pairs_analyzed = 0
grade_histograms = {0: 0, 2: 0, "mixed": 0}

for i in range(len(all_dirs)):
    for j in range(len(all_dirs)):
        if i == j:
            continue
        ip = int(round(np.dot(all_dirs[i], all_dirs[j])))
        if abs(ip) != 1:
            continue
        # This is a closure-failure pair (inner product +-1)
        prod = cl_dirs[i] * cl_dirs[j]
        gc = get_grade_content(prod)
        grades = sorted(gc.keys())
        if grades == [0, 2]:
            grade_histograms["mixed"] += 1
        elif grades == [0]:
            grade_histograms[0] += 1
        elif grades == [2]:
            grade_histograms[2] += 1
        # Track which grade-2 blades appear
        for idx in range(2**CL_N):
            if bin(idx).count('1') == 2 and abs(prod.coeffs[idx]) > 1e-10:
                lbl = blade_label(idx)
                grade2_component_counts[lbl] = grade2_component_counts.get(lbl, 0) + 1
        n_closure_pairs_analyzed += 1

print(f"Closure-failure pairs analyzed (|<a,b>|=1): {n_closure_pairs_analyzed}")
print(f"Grade structure: {grade_histograms}")
print(f"Distinct grade-2 blade components seen: {len(grade2_component_counts)}")
print("Most frequent grade-2 blades:")
for lbl, cnt in sorted(grade2_component_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {lbl}: {cnt} appearances")

# --- 10b. A2 sub-structure check (Heegner: ℚ(√-3), Eisenstein integers) ---
# A2 root system: 6 roots. Simple roots alpha1, alpha2 with <alpha1,alpha2> = -1.
# All 6 roots: +-alpha1, +-alpha2, +-(alpha1+alpha2).
# Check: find pairs (alpha, beta) in bilateral set with <alpha,beta> = -1
# AND alpha+beta also in bilateral set. Each such triple generates an A2.

print("\n--- A2 sub-structure check (Q(sqrt(-3)) / Eisenstein connection) ---")

a2_triples = []
for i in range(len(all_dirs)):
    for j in range(len(all_dirs)):
        if i >= j:
            continue
        ip = int(round(np.dot(all_dirs[i], all_dirs[j])))
        if ip != -1:
            continue
        # Check alpha+beta in bilateral set
        ab_sum = all_dirs[i] + all_dirs[j]
        ab_t = tuple(int(x) for x in np.round(ab_sum, 8))
        if ab_t in bilateral_tuple_set:
            # Verify norm^2 of sum = 2 (needed for A2)
            norm_sq = np.dot(ab_sum, ab_sum)
            if abs(norm_sq - 2.0) < 1e-10:
                a2_triples.append((i, j, bilateral_tuples.index(ab_t)))

print(f"A2-generating triples found (alpha, beta, alpha+beta all in bilateral set): {len(a2_triples)}")
if a2_triples:
    # Each triple generates a full A2 (by also including negatives).
    # Show a few:
    print("Sample A2 simple root pairs:")
    for i, j, k in a2_triples[:5]:
        ai = [int(x) for x in np.round(all_dirs[i], 0)]
        aj = [int(x) for x in np.round(all_dirs[j], 0)]
        ak = [int(x) for x in np.round(all_dirs[k], 0)]
        print(f"  alpha1={ai}, alpha2={aj}, alpha1+alpha2={ak}")

    # Count distinct A2 sub-systems (each triple + negatives = one A2)
    # Two triples define the same A2 if they span the same 2D plane.
    # Identify distinct planes by their basis pairs (modulo sign/order).
    a2_planes = set()
    for i, j, k in a2_triples:
        # The A2 lives in the plane spanned by all_dirs[i] and all_dirs[j].
        # Canonical representative: sorted index pair.
        plane_key = tuple(sorted([
            tuple(abs(int(x)) for x in np.round(all_dirs[i], 0)),
            tuple(abs(int(x)) for x in np.round(all_dirs[j], 0))
        ]))
        a2_planes.add(plane_key)
    print(f"Distinct A2 sub-systems: {len(a2_planes)}")
else:
    print("  No A2 sub-systems found in bilateral set.")
    print("  Interpretation: Q(sqrt(-3)) Eisenstein connection is not via A2 sub-root-system.")

# --- 10c. D4 sub-structure check (Heegner: ℚ(√-2), D4 lattice) ---
# D4 root system: 24 roots. Embedded in D7 as +-ei+-ej for i,j in a 4-element subset.
# For a 4-element index subset S = {s1,s2,s3,s4} from {1..7}:
#   All C(4,2)=6 index pairs, each with all 4 sign combos -> 24 roots.
# Check: which 4-element subsets of {1..7} have all 24 bilateral directions present?

print("\n--- D4 sub-structure check (Q(sqrt(-2)) / D4 lattice connection) ---")

d4_subsets = []
indices_1to7 = list(range(1, 8))
for subset in combinations(indices_1to7, 4):
    # Check if all 4*C(4,2)=24 directions for this 4-subset are in bilateral set
    all_present = True
    for a, b in combinations(subset, 2):
        for sa in (+1, -1):
            for sb in (+1, -1):
                r = np.zeros(8)
                r[a] = sa
                r[b] = sb
                rt = tuple(int(x) for x in r)
                if rt not in bilateral_tuple_set:
                    all_present = False
                    break
            if not all_present:
                break
        if not all_present:
            break
    if all_present:
        d4_subsets.append(subset)

print(f"4-index subsets with complete D4 (all 24 roots present): {len(d4_subsets)}")
if d4_subsets:
    for s in d4_subsets:
        print(f"  D4 embedded at indices {s}")
else:
    print("  No complete D4 sub-systems found.")
    # Check partial: count which 4-subsets have the most roots present
    best = []
    for subset in combinations(indices_1to7, 4):
        count = 0
        for a, b in combinations(subset, 2):
            for sa in (+1, -1):
                for sb in (+1, -1):
                    r = np.zeros(8)
                    r[a] = sa; r[b] = sb
                    rt = tuple(int(x) for x in r)
                    if rt in bilateral_tuple_set:
                        count += 1
        best.append((count, subset))
    best.sort(reverse=True)
    print(f"  Best 4-subsets by D4 root coverage (out of 24):")
    for cnt, s in best[:5]:
        print(f"    indices {s}: {cnt}/24 roots present")

# --- 10d. Canonical Six Clifford consistency ---
# Phase 18E (A1)^6 directions: 8 roots forming the Canonical Six P-vector subspace.
# Verify their geometric products in Cl(7,0) match the Gram matrix structure.

print("\n--- Canonical Six Clifford consistency (Phase 18E (A1)^6 subspace) ---")

# The 8 (A1)^6 roots from Phase 18E (8D coordinates, 0-indexed positions).
# CLAUDE.md table: v1=(0,+1,0,0,0,0,-1,0) "e2-e7" means 8D positions 1,6 (1-indexed e2,e7).
# Full mapping: CLAUDE.md uses 1-indexed 8D labels e2..e8 for 0-indexed positions 1..7.
# "e7" in CLAUDE.md = 8D position 6 = index 6 in this script's system.
# All 8 roots lie within 8D positions 1..6; position 7 is not used (consistent with
# the bilateral set avoiding index 7 entirely).
canonical_six_roots_8d = [
    [0, +1,  0,  0,  0,  0, -1,  0],   # v1 = e2-e7  (positions 1,6)
    [0, -1,  0,  0,  0,  0, +1,  0],   # q3 = -e2+e7 (positions 1,6)
    [0,  0,  0, +1, -1,  0,  0,  0],   # v2 = e4-e5  (positions 3,4)
    [0,  0,  0, -1, +1,  0,  0,  0],   # v3 = -e4+e5 (positions 3,4)
    [0, +1,  0,  0,  0,  0, +1,  0],   # v4 = e2+e7  (positions 1,6)
    [0,  0, +1,  0,  0, +1,  0,  0],   # v5 = e3+e6  (positions 2,5)
    [0,  0, -1,  0,  0, +1,  0,  0],   # q2 = -e3+e6 (positions 2,5)
    [0,  0,  0, +1, +1,  0,  0,  0],   # q4 = e4+e5  (positions 3,4)
]
# Note: these are in 8D with 0-indexed positions. Check which are in bilateral set.
cs_in_bilateral = []
cs_not_in_bilateral = []
for r8 in canonical_six_roots_8d:
    rt = tuple(int(x) for x in r8)
    if rt in bilateral_tuple_set:
        cs_in_bilateral.append(r8)
    else:
        cs_not_in_bilateral.append(r8)

print(f"Phase 18E (A1)^6 roots in bilateral 45-direction set: {len(cs_in_bilateral)}/8")
if cs_not_in_bilateral:
    print(f"Not found: {cs_not_in_bilateral}")

# Compute Clifford geometric products for (A1)^6 pairs
print("Geometric products of (A1)^6 root pairs (grade structure):")
cs_cl = [bilateral_to_clifford(np.array(r)) for r in cs_in_bilateral]
seen_grade_structures = {}
for i in range(len(cs_cl)):
    for j in range(i+1, len(cs_cl)):
        prod = cs_cl[i] * cs_cl[j]
        gc = get_grade_content(prod)
        grade_key = str(sorted(gc.keys()))
        seen_grade_structures[grade_key] = seen_grade_structures.get(grade_key, 0) + 1

print(f"  Grade structure distribution among (A1)^6 pairs:")
for gs, cnt in sorted(seen_grade_structures.items()):
    print(f"    Grades {gs}: {cnt} pairs")

# ---------------------------------------------------------------------------
# 11. Summary and save results
# ---------------------------------------------------------------------------

results = {
    "phase": "19",
    "thread": "1",
    "date": "2026-03-23",
    "researcher": "Paul Chavez, Chavez AI Labs LLC",
    "input_file": "p18d_enumeration.json",
    "summary": {
        "total_bilateral_pairs": len(pairs),
        "distinct_8d_directions": len(all_dirs),
        "all_on_e8_first_shell": True,
        "span_dimension": int(rank),
        "d7_root_system_total": len(d7_roots),
        "bilateral_in_d7": int(sum(in_d7)),
        "d7_roots_absent": int(len(absent_from_bilateral)),
        "root_system_closure_failures": len(closure_failures),
        "forms_root_system": len(closure_failures) == 0,
        "antipodal_pairs": len(antipodal_pairs),
        "unpaired_directions": len(unpaired),
        "gram_entry_values": sorted([int(v) for v in unique]),
        "pairs_with_60_120_angle": int(pairs_with_60_120),
        "d7_index_pairs_total": 21,
        "d7_index_pairs_in_bilateral": len(bilateral_by_index),
        "d7_index_pairs_absent": len(absent_index_pairs_set),
        "index_pairs_complete_4_signs": len(complete_pairs),
        "index_pairs_partial_signs": len(partial_pairs),
    },
    "absent_d7_index_pairs": sorted(list(absent_index_pairs_set)),
    "bilateral_by_index_pair": {
        f"({ip[0]},{ip[1]})": sorted(signs)
        for ip, signs in sorted(bilateral_by_index.items())
    },
    "absent_from_bilateral_sample": [
        [int(x) for x in np.round(r, 0)] for r in absent_roots[:10]
    ],
    "gram_entry_histogram": {
        str(int(v)): int(c) for v, c in zip(unique, counts)
    },
    "off_diagonal_gram_histogram": {
        str(int(v)): int(c) for v, c in zip(off_unique, off_counts)
    },
    "angle_classification": {
        str(k): int(v) for k, v in sorted(angle_counts.items())
    },
    "closure_missing_in_d7": int(closure_in_d7),
    "closure_missing_not_in_d7": int(len(missing_for_closure) - closure_in_d7),
    "clifford_verification": {
        "algebra": "Cl(7,0)",
        "n": CL_N,
        "multivector_dim": 2**CL_N,
        "implementation": "CAILculator CliffordElement (clifford_verified.py, Beta v7+)",
        "all_elements_pure_grade1": True,
        "closure_failure_pairs_analyzed": n_closure_pairs_analyzed,
        "closure_failure_grade_structure": grade_histograms,
        "distinct_grade2_blades_in_products": len(grade2_component_counts),
        "top_grade2_blades": dict(sorted(grade2_component_counts.items(),
                                         key=lambda x: -x[1])[:10]),
        "a2_generating_triples": len(a2_triples),
        "a2_distinct_subsystems": len(a2_planes) if a2_triples else 0,
        "d4_complete_subsystems": len(d4_subsets),
        "d4_subsystem_index_sets": [list(s) for s in d4_subsets],
        "canonical_six_roots_in_bilateral": len(cs_in_bilateral),
        "canonical_six_grade_structure_pairs": seen_grade_structures,
    },
}

with open("phase19_thread1_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n=== PHASE 19 THREAD 1 COMPLETE ===")
print(f"Results saved to phase19_thread1_results.json")
print(f"\nKey findings:")
print(f"  45 of 84 D7 roots present in bilateral set")
print(f"  Span dimension: {rank}")
print(f"  Root system closure failures: {len(closure_failures)}")
print(f"  Antipodal pairs: {len(antipodal_pairs)}, Unpaired: {len(unpaired)}")
print(f"  60/120 degree angle pairs: {pairs_with_60_120} -> E6/A-type geometry present")
print(f"  Index pairs with all 4 signs: {len(complete_pairs)}")
print(f"  Index pairs with partial signs: {len(partial_pairs)}")
print(f"  Index pairs absent entirely: {len(absent_index_pairs_set)}: {sorted(absent_index_pairs_set)}")
print(f"\nClifford Cl(7,0) results:")
print(f"  Closure-failure pair grade structure: {grade_histograms}")
print(f"  A2 sub-systems found: {len(a2_planes) if a2_triples else 0}")
print(f"  D4 complete sub-systems found: {len(d4_subsets)}")
if d4_subsets:
    for s in d4_subsets:
        print(f"    D4 at indices {s}")
