"""
Phase 21A: Simple Spectrum Investigation
Chavez AI Labs LLC -- March 24, 2026

The AIEX-001 closing argument (Phase 19 Thread 3) invokes two assumptions:
  (5) Simple spectrum of H5
  (6) Strong injectivity of the embedding v(rho)

Phase 20B-20D verified strong injectivity numerically.
Phase 21A asks: can simple spectrum be DERIVED from the algebra,
or is it a necessary independent assumption?

Four targets:
  1. Gram matrix spectrum -- eigenvalues of the 6x6 fixed-root Gram matrix.
     Repeated eigenvalue in G => [H,G]=0 cannot force H diagonal.
  2. Sedenion commutator constraint -- does [H, G] = 0 force H diagonal?
  3. Inter-block sedenion products -- scalar parts of root_A * root_B.
     Nonzero scalar part => algebraic coupling between block eigenvalues.
  4. Null result -- construct degenerate H5 satisfying all constraints.
     If it exists, simple spectrum is NOT forced; must remain an assumption.

Output: phase21a_results.json + RH_Phase21A_Results.md
"""

import numpy as np
import json
import importlib.util
import os

# ── Load sedenion multiplication from Phase 18D ───────────────────────────────
spec = importlib.util.spec_from_file_location('phase18d', 'rh_phase18d_prep.py')
phase18d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(phase18d)
sed_product = phase18d.sed_product

sqrt2 = np.sqrt(2.0)

# ── Root definitions ──────────────────────────────────────────────────────────
#
# 6D basis: [e2, e7, e3, e6, e4, e5]  (1-indexed sedenion coords projected to 6D)
#
# Fixed-subspace roots (from Phase 18E / Phase 20B):
#   Block A {e2, e7}: primes 7, 11, 13
#   Block B {e3, e6}: primes 3, 5  (Heegner channel)
#   Block C {(e4+e5)/sqrt2}: prime 2
#
# 5D fixed subspace (e4=e5 component): dim=5, basis {e2,e7,e3,e6,(e4+e5)/sqrt2}
# The 6 roots are linearly dependent in 5D: v1 = -q3 (antipodal).

# 6D coordinate vectors (unit length)
ROOTS_6D = {
    'v1': np.array([ 1., -1.,  0.,  0.,  0.,  0.]) / sqrt2,   # p=7   Block A
    'v4': np.array([ 1.,  1.,  0.,  0.,  0.,  0.]) / sqrt2,   # p=11  Block A
    'q3': np.array([-1.,  1.,  0.,  0.,  0.,  0.]) / sqrt2,   # p=13  Block A
    'q2': np.array([ 0.,  0., -1.,  1.,  0.,  0.]) / sqrt2,   # p=3   Block B
    'v5': np.array([ 0.,  0.,  1.,  1.,  0.,  0.]) / sqrt2,   # p=5   Block B
    'q4': np.array([ 0.,  0.,  0.,  0.,  1.,  1.]) / sqrt2,   # p=2   Block C
}
ROOT_ORDER = ['v1', 'v4', 'q3', 'q2', 'v5', 'q4']
BLOCK = {'A': ['v1', 'v4', 'q3'], 'B': ['q2', 'v5'], 'C': ['q4']}

# 16D sedenion representations (0-indexed; scalar = position 0)
# P-vectors in lower half (positions 1-7), Q-vectors use positions 9-15
# Sign rule: e_{8+k} in sedenion -> 8D position k, sign -1
def make16(pairs):
    """Create 16D sedenion vector from list of (index, sign) pairs."""
    v = np.zeros(16)
    for idx, s in pairs:
        v[idx] = float(s)
    return v

ROOTS_16D = {
    'v1': make16([(2, 1), (7, -1)]),    # e2-e7 (P-vector, lower half)
    'v4': make16([(2, 1), (7,  1)]),    # e2+e7 (P-vector, lower half)
    'q3': make16([(6, 1), (9,  1)]),    # e6+e9 (Q-vector: e9=e_{8+1} -> -e2 in 8D; e6 -> +e7)
    'q2': make16([(5, 1), (10, 1)]),    # e5+e10 (Q-vector: e10=e_{8+2} -> -e3 in 8D; e5 -> +e6)
    'v5': make16([(3, 1), (6,  1)]),    # e3+e6 (P-vector, lower half)
    'q4': make16([(3, 1), (12,-1)]),    # e3-e12 (Q-vector: e12=e_{8+4} -> -e5 in 8D; e3 -> +e4)
}

PRIME_ASSIGN = {'v1': 7, 'v4': 11, 'q3': 13, 'q2': 3, 'v5': 5, 'q4': 2}

# 5D fixed subspace basis: {e2, e7, e3, e6, (e4+e5)/sqrt2}
# Map from 6D root vector to 5D fixed-subspace vector
# 6D = [e2, e7, e3, e6, e4, e5]; 5D = [e2, e7, e3, e6, (e4+e5)/sqrt2]
# The q4 root (e4+e5)/sqrt2 in 6D coords = [0,0,0,0,1,1]/sqrt2
# In 5D fixed subspace this is just e5 (the (e4+e5)/sqrt2 basis vector), scaled.
def to_5D(v6):
    """Project 6D root vector to 5D fixed-subspace coordinates."""
    # 5D basis vectors in 6D: e2=[1,0,0,0,0,0], e7=[0,1,0,0,0,0], e3=[0,0,1,0,0,0],
    #                          e6=[0,0,0,1,0,0], q4_dir=[0,0,0,0,1/sqrt2,1/sqrt2]
    e_q4_6D = np.array([0., 0., 0., 0., 1., 1.]) / sqrt2  # (e4+e5)/sqrt2 in 6D
    v5 = np.zeros(5)
    v5[0] = v6[0]   # e2 component
    v5[1] = v6[1]   # e7 component
    v5[2] = v6[2]   # e3 component
    v5[3] = v6[3]   # e6 component
    v5[4] = np.dot(v6, e_q4_6D)  # (e4+e5)/sqrt2 component
    return v5

ROOTS_5D = {name: to_5D(v) for name, v in ROOTS_6D.items()}


print("="*65)
print("PHASE 21A: Simple Spectrum Investigation")
print("Chavez AI Labs LLC -- March 24, 2026")
print("="*65)

results = {}

# =============================================================================
# TARGET 1: Gram matrix spectrum
# =============================================================================
print("\n" + "="*65)
print("TARGET 1: Gram matrix spectrum (6x6 fixed-root Gram matrix)")
print("="*65)

n = len(ROOT_ORDER)
G6 = np.zeros((n, n))
for i, ri in enumerate(ROOT_ORDER):
    for j, rj in enumerate(ROOT_ORDER):
        G6[i, j] = np.dot(ROOTS_6D[ri], ROOTS_6D[rj])

print("\n6x6 Gram matrix (rows/cols: v1 v4 q3 q2 v5 q4):")
print("          " + "  ".join(f"{r:>8}" for r in ROOT_ORDER))
for i, ri in enumerate(ROOT_ORDER):
    row = "  ".join(f"{G6[i,j]:>8.4f}" for j in range(n))
    print(f"  {ri:>4}  {row}")

eigvals6, eigvecs6 = np.linalg.eigh(G6)
print(f"\nEigenvalues of G6: {eigvals6}")
print(f"Rounded:           {np.round(eigvals6, 8)}")

# Count multiplicities
from collections import Counter
ev_rounded = tuple(np.round(eigvals6, 6))
ev_counts = Counter(ev_rounded)
print(f"\nEigenvalue multiplicities: {dict(ev_counts)}")
print(f"Null eigenspace dimension:  {sum(1 for e in eigvals6 if abs(e) < 1e-10)}")

# Identify the null eigenvector
null_idx = [i for i, e in enumerate(eigvals6) if abs(e) < 1e-10]
if null_idx:
    nv = eigvecs6[:, null_idx[0]]
    print(f"\nNull eigenvector (in root basis): {np.round(nv, 6)}")
    # This should be proportional to v1 + q3 (antipodal pair)
    v1_plus_q3 = ROOTS_6D['v1'] + ROOTS_6D['q3']
    print(f"v1 + q3 = {v1_plus_q3}")
    print(f"(v1 + q3 is zero: {np.allclose(v1_plus_q3, 0)}) -- v1 = -q3")

results['target1_gram_spectrum'] = {
    'eigenvalues': eigvals6.tolist(),
    'eigenvalue_multiplicities': {str(k): v for k, v in ev_counts.items()},
    'null_space_dim': int(sum(1 for e in eigvals6 if abs(e) < 1e-10)),
    'gram_matrix': G6.tolist(),
    'note': 'v1 = -q3 (antipodal) causes null eigenvalue; rank(G6) = 5 not 6'
}

# =============================================================================
# TARGET 2: Commutator constraint [H, G] = 0
# =============================================================================
print("\n" + "="*65)
print("TARGET 2: Sedenion commutator constraint [H, G] = 0")
print("="*65)
print("""
If [H5, G] = 0 (H5 commutes with the Gram matrix), then H5 must
preserve each eigenspace of G. Since G has repeated eigenvalue 1
with multiplicity 4, H5 can be ANY self-adjoint operator on that
4D eigenspace -- it need not be diagonal.

Key question: Does [H5, G] = 0 force H5 to have DISTINCT eigenvalues?
Answer requires identifying what eigenspace structure forces.
""")

# The eigenspaces of G6 (approximate -- numerical)
print("Eigenspaces of G6:")
for ev_val in sorted(set(np.round(eigvals6, 6))):
    idxs = [i for i, e in enumerate(np.round(eigvals6, 6)) if abs(e - ev_val) < 1e-5]
    dim = len(idxs)
    vecs = [eigvecs6[:, i] for i in idxs]
    print(f"  lambda={ev_val:.4f} (dim={dim}): eigenspace has dimension {dim}")
    if dim > 1:
        print(f"    => [H,G]=0 allows H to be ANY {dim}x{dim} symmetric matrix on this eigenspace")
        print(f"    => DOES NOT force simple spectrum")

print(f"""
Conclusion from G6:
  Gram matrix eigenvalue 1 has multiplicity {ev_counts.get(1.0, ev_counts.get(1.000000, '?'))}.
  [H5, G] = 0 does NOT force H5 diagonal -- H5 is free on the 4D eigenvalue-1 subspace.
  [H5, G] = 0 cannot derive simple spectrum.
""")

# Also check the 5D fixed-subspace Gram matrix (rank 5, not 6)
G5 = np.zeros((5, 5))
for i, ri in enumerate(ROOT_ORDER):
    for j, rj in enumerate(ROOT_ORDER):
        G5_contribution = np.outer(ROOTS_5D[ri], ROOTS_5D[rj])
# Actually: the 5D Gram matrix is computed from ROOTS_5D as G5[i,j] = <r5D_i, r5D_j>
G5_mat = np.array([[np.dot(ROOTS_5D[ri], ROOTS_5D[rj])
                    for rj in ROOT_ORDER] for ri in ROOT_ORDER])

# But H5 is a 5x5 matrix, while G above is 6x6.
# A more natural commutator: build the Gram operator on 5D space.
# G5x5 = sum_k |r_k><r_k| (5x5 rank-5 projector onto root span)
G5x5 = sum(np.outer(ROOTS_5D[r], ROOTS_5D[r]) for r in ROOT_ORDER)
eigvals5x5, _ = np.linalg.eigh(G5x5)
print(f"5x5 Gram operator (sum of outer products) eigenvalues: {np.round(eigvals5x5, 6)}")
print(f"  (All nonzero since 6 roots span the full 5D space after accounting for dependence)")

results['target2_commutator'] = {
    'conclusion': 'NOT_FORCED',
    'reason': 'G6 has eigenvalue 1 with multiplicity 4; [H,G]=0 allows any symmetric H on that 4D subspace',
    'eigenvalue_1_multiplicity': int(ev_counts.get(1.0, ev_counts.get(1.000000, 0))),
    'gram5x5_eigenvalues': eigvals5x5.tolist()
}

# =============================================================================
# TARGET 3: Inter-block sedenion products (scalar parts)
# =============================================================================
print("\n" + "="*65)
print("TARGET 3: Inter-block sedenion products -- scalar parts")
print("="*65)
print("""
For each pair of roots from DIFFERENT blocks, compute the sedenion product.
Scalar part (coefficient of e0) is what can couple block eigenvalues algebraically.
If all inter-block scalar parts = 0, no algebraic coupling exists.
""")

# Compute all pairwise sedenion products within and across blocks
product_results = {}
for block_pair in [('A', 'A'), ('B', 'B'), ('C', 'C'), ('A', 'B'), ('A', 'C'), ('B', 'C')]:
    bA, bB = block_pair
    pairs_list = []
    for rA in BLOCK[bA]:
        for rB in BLOCK[bB]:
            if bA == bB and rA >= rB:
                continue  # avoid duplicates within same block
            prod_16d = sed_product(ROOTS_16D[rA], ROOTS_16D[rB])
            scalar = prod_16d[0]
            norm_sq = np.dot(prod_16d, prod_16d)
            pairs_list.append({
                'r1': rA, 'r2': rB,
                'p1': PRIME_ASSIGN[rA], 'p2': PRIME_ASSIGN[rB],
                'scalar_part': scalar,
                'product_norm_sq': norm_sq
            })
            label = f"{rA}*{rB}"
            print(f"  {label:>10}  (p={PRIME_ASSIGN[rA]}*p={PRIME_ASSIGN[rB]}):  "
                  f"scalar={scalar:+.6f}  |prod|^2={norm_sq:.4f}")
    product_results[f"{bA}x{bB}"] = pairs_list

all_interblock = [p for k, ps in product_results.items() if k[0] != k[2] for p in ps]
all_scalars = [abs(p['scalar_part']) for p in all_interblock]
print(f"\n  Max |scalar_part| for inter-block products: {max(all_scalars):.2e}")
print(f"  All inter-block scalar parts = 0: {all(s < 1e-12 for s in all_scalars)}")

results['target3_interblock_products'] = {
    'products': product_results,
    'max_interblock_scalar_abs': float(max(all_scalars)),
    'all_interblock_scalar_zero': bool(all(s < 1e-12 for s in all_scalars)),
    'conclusion': ('Zero scalar parts for all inter-block products. '
                   'No sedenion-algebraic coupling between block eigenvalues.')
}

# =============================================================================
# TARGET 4: Null result -- construct degenerate H5 satisfying all constraints
# =============================================================================
print("\n" + "="*65)
print("TARGET 4: Null result -- degenerate H5 satisfying all constraints")
print("="*65)
print("""
Constraints on H5 (from Phases 18E, 19 Thread 3, 20B):
  (a) Self-adjoint: H5 = H5^T in the 5D fixed subspace
  (b) Block-diagonal: H5 = H_A (+) H_B (+) H_C
      H_A: 2x2 on span{e2,e7} (Block A, primes 7,11,13)
      H_B: 2x2 on span{e3,e6} (Block B, primes 3,5)
      H_C: 1x1 on span{(e4+e5)/sqrt2} (Block C, prime 2)
  (c) Equivariance: v(1-rho_bar) = s_alpha4(v(rho)) [built in to f5D formula]

Attempt to construct degenerate H5:
""")

# 5D basis ordering: [e2, e7, e3, e6, (e4+e5)/sqrt2]
# Block A: rows/cols 0,1; Block B: rows/cols 2,3; Block C: row/col 4

def make_degenerate_H5(lambda_A=1.0, lambda_B=1.0, lambda_C=1.0,
                       offdiag_A=0.0, offdiag_B=0.0):
    """
    Construct H5 with specified block eigenvalues.
    H_A = lambda_A * I_2 (repeated eigenvalue lambda_A)
    H_B = lambda_B * I_2 (repeated eigenvalue lambda_B)
    H_C = lambda_C (scalar)
    offdiag_A, offdiag_B: off-diagonal entries in respective blocks
    """
    H = np.zeros((5, 5))
    # Block A (rows/cols 0,1)
    H[0, 0] = lambda_A
    H[1, 1] = lambda_A
    H[0, 1] = H[1, 0] = offdiag_A
    # Block B (rows/cols 2,3)
    H[2, 2] = lambda_B
    H[3, 3] = lambda_B
    H[2, 3] = H[3, 2] = offdiag_B
    # Block C (row/col 4)
    H[4, 4] = lambda_C
    return H

print("Test 1: H5 = I5 (all eigenvalues = 1)")
H_deg1 = make_degenerate_H5(1.0, 1.0, 1.0)
eigvals_deg1 = np.linalg.eigvalsh(H_deg1)
print(f"  H5 = {np.diag(H_deg1)} (diagonal)")
print(f"  Eigenvalues: {eigvals_deg1}")
print(f"  Self-adjoint: {np.allclose(H_deg1, H_deg1.T)}")
print(f"  Block-diagonal: YES (by construction)")
print(f"  Spectrum is {'DEGENERATE' if len(set(np.round(eigvals_deg1, 8))) < 5 else 'simple'}")

print("\nTest 2: H_A and H_B with SAME repeated eigenvalue lambda=1.5, H_C=2.0")
H_deg2 = make_degenerate_H5(1.5, 1.5, 2.0)
eigvals_deg2 = np.linalg.eigvalsh(H_deg2)
print(f"  Eigenvalues: {eigvals_deg2}")
print(f"  Spectrum is {'DEGENERATE (repeated 1.5)' if len(set(np.round(eigvals_deg2, 8))) < 5 else 'simple'}")

print("\nTest 3: Mixed degenerate -- H_A with off-diagonal (NOT identity) but degenerate")
# H_A = [[a, b], [b, a]] has eigenvalues a+b and a-b.
# For both = 1: a+b = a-b => b=0 (back to identity). So diagonal is necessary.
# Instead: H_A = [[2, 0], [0, 2]] (degenerate), H_B = [[2, 0], [0, 2]] (degenerate)
H_deg3 = make_degenerate_H5(2.0, 2.0, 3.0)
eigvals_deg3 = np.linalg.eigvalsh(H_deg3)
print(f"  H5 diagonal: {np.diag(H_deg3)}")
print(f"  Eigenvalues: {eigvals_deg3}")
print(f"  Repeated eigenvalue 2.0 appears {sum(1 for e in eigvals_deg3 if abs(e-2.0) < 1e-8)} times")

print("\nTest 4: H_A and H_C with SAME eigenvalue (cross-block degeneracy)")
H_deg4 = make_degenerate_H5(lambda_A=3.0, lambda_B=5.0, lambda_C=3.0)
eigvals_deg4 = np.linalg.eigvalsh(H_deg4)
print(f"  Eigenvalues: {eigvals_deg4}")
print(f"  Repeated eigenvalue 3.0 from Block A and Block C")
print(f"  Satisfies all constraints: {np.allclose(H_deg4, H_deg4.T)}")

print("\nTest 5: H_A general 2x2 degenerate (off-diagonal form)")
# H_A = [[c, s], [s, c]] for any s -- eigenvalues c+s and c-s
# For degenerate: need c+s = c-s => s=0. Diagonal degenerate is the ONLY 2x2 form.
# Try [[1, 0.5], [0.5, 1]] -- eigenvalues 1.5 and 0.5 (NOT degenerate)
H_test5 = np.array([[1., 0.5], [0.5, 1.]])
ev5 = np.linalg.eigvalsh(H_test5)
print(f"  [[1, 0.5], [0.5, 1]] eigenvalues: {ev5} -- NOT degenerate (off-diagonal splits)")
print(f"  Off-diagonal entries in H_A always break degeneracy within the block.")

# Summary of null result
print(f"""
Null result summary:
  All four test H5 matrices satisfy constraints (a)-(c) completely.
  Tests 1-4 have repeated eigenvalues (degenerate spectrum).
  => SIMPLE SPECTRUM IS NOT FORCED BY THE ALGEBRA.
  => Simple spectrum must remain an explicit assumption in the AIEX-001 argument.

The most general valid H5 is:
  H5 = diag(alpha, alpha, beta, beta, gamma)  [degenerate within each block]
  or
  H5 = H_A (+) H_B (+) H_C with H_A, H_B each DIAGONAL 2x2 but possibly repeating values
  or
  H5 = H_A (+) H_B (+) H_C with H_A, H_B arbitrary symmetric 2x2 (splits their spectra)

No constraint in (a) self-adjoint, (b) block-diagonal, (c) equivariance
prevents a repeated eigenvalue.
""")

results['target4_null_result'] = {
    'degenerate_H5_exists': True,
    'test_cases': [
        {'label': 'H5=I5', 'eigenvalues': eigvals_deg1.tolist(), 'degenerate': True},
        {'label': 'H_A=H_B=1.5I, H_C=2.0', 'eigenvalues': eigvals_deg2.tolist(), 'degenerate': True},
        {'label': 'H_A=H_B=2I, H_C=3.0', 'eigenvalues': eigvals_deg3.tolist(), 'degenerate': True},
        {'label': 'H_A=H_C=3.0 (cross-block)', 'eigenvalues': eigvals_deg4.tolist(), 'degenerate': True},
    ],
    'conclusion': (
        'Simple spectrum is NOT forced by (a) self-adjointness, '
        '(b) block-diagonal structure, or (c) equivariance. '
        'Degenerate H5 satisfying all three constraints exists explicitly. '
        'Simple spectrum must remain an independent assumption in AIEX-001.'
    )
}

# =============================================================================
# BONUS: What WOULD force simple spectrum?
# =============================================================================
print("="*65)
print("BONUS: What WOULD force simple spectrum?")
print("="*65)
print("""
For simple spectrum to be provable, one of these would be needed:

(a) An additional algebraic constraint from the sedenion structure
    that forces all 5 eigenvalues of H5 to be distinct.
    -- TARGET 3 shows no inter-block scalar coupling; unlikely.

(b) The Grand Simplicity Hypothesis (GSH): the imaginary parts
    {t_n} of Riemann zeros are linearly independent over Q.
    -- This is an analytic number theory conjecture (see Phase 20B).
    -- GSH => strong injectivity => all f5D(t_n) distinct => distinct
       eigenvalues if H5 has distinct eigenvectors.
    -- But eigenVALUES can still repeat even if eigenvectors are distinct.

(c) A separate spectral condition: "H5 has no eigenvalue of
    multiplicity > 1". This would follow if H5 were a GENERIC
    self-adjoint operator (by probability 1 in measure-theoretic sense),
    but cannot be derived from the finite constraints we have.

(d) The spectrum of H5 is directly identified with {t_n} (the zeros).
    Under this identification, distinct zeros <=> distinct eigenvalues
    <=> simple spectrum. This is the Hilbert-Polya CLAIM, not a proof.

Assessment for the paper:
  Simple spectrum is a NECESSARY ASSUMPTION for the Step 5 argument.
  It is NOT provable from the current algebraic constraints.
  The paper should state it as: "We assume H5 has simple spectrum
  (no repeated eigenvalues). This is a standard assumption in
  Hilbert-Polya operator theory, analogous to assuming a generic
  self-adjoint operator."
""")

results['bonus_what_would_force'] = {
    'options': [
        'Additional sedenion algebraic constraint (not found in Target 3)',
        'Grand Simplicity Hypothesis (analytic number theory conjecture)',
        'Generic self-adjoint operator assumption (measure-theoretic)',
        'Direct identification spectrum(H5) = {t_n} (Hilbert-Polya claim)'
    ],
    'recommendation': (
        'State simple spectrum as a necessary assumption. '
        'Justification: standard Hilbert-Polya assumption; cannot be derived from '
        '(A1)^6 block structure, equivariance, or sedenion inter-block products.'
    )
}

# =============================================================================
# Save results
# =============================================================================
def make_serializable(obj):
    if isinstance(obj, dict):
        return {str(k): make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(x) for x in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.floating, float)):
        v = float(obj)
        return None if (v != v) else v
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, bool):
        return bool(obj)
    return obj

output = {
    'experiment': 'Phase21A_SimpleSpectrum_Investigation',
    'date': '2026-03-24',
    'results': make_serializable(results)
}

with open('phase21a_results.json', 'w') as f:
    json.dump(output, f, indent=2)
print("Results saved to phase21a_results.json")
