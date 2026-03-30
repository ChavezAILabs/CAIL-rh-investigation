"""
rh_phase43b.py
==============
Phase 43b: Spinor Rank Analysis
Constructs the Spinor Gram Matrix G for the first 50 Riemann zeros
and performs rank and orthogonality analysis.

Chavez AI Labs LLC — March 28, 2026
"""

import numpy as np
import json

# Mapping to Bivector Indices (e3, e5, e10, e6, e9, e12)
B_INDICES = [3, 5, 10, 6, 9, 12]

def load_data():
    # Load signatures
    with open('phase43b_zdtp_signatures.json', 'r') as f:
        sig_data = json.load(f)
    
    gammas = np.array([item['gamma'] for item in sig_data])
    signatures = np.array([item['signature'] for item in sig_data])
    return gammas, signatures

def compute_psi_at_zero(n_idx, gammas, signatures):
    """
    Computes psi(gamma_n) = 0.5*e0 + sum_k (sum_m w_m * cos(gamma_n * gamma_m) * S_{m,k}) * Bk
    """
    N = len(gammas)
    K = signatures.shape[1]
    weights = 1.0 / np.sqrt(gammas)
    t = gammas[n_idx]
    
    psi = np.zeros(16)
    psi[0] = 0.5
    
    for k in range(K):
        val = 0.0
        for m in range(N):
            val += weights[m] * np.cos(t * gammas[m]) * signatures[m, k]
        
        idx = B_INDICES[k]
        psi[idx] = val
        
    return psi

def main():
    gammas, signatures = load_data()
    N = len(gammas)
    
    print(f"Constructing {N} spinors...")
    spinors = []
    for n in range(N):
        spinors.append(compute_psi_at_zero(n, gammas, signatures))
    
    spinors = np.array(spinors) # Shape (50, 16)
    
    # Construct Gram Matrix G
    print("Computing 50x50 Gram Matrix G...")
    G = np.dot(spinors, spinors.T)
    
    # Eigendecomposition
    evals = np.linalg.eigvalsh(G)
    evals = sorted(evals, reverse=True)
    
    # Effective Rank (tol = 1e-12)
    tol = 1e-12
    rank = np.sum(np.array(evals) > tol)
    
    print(f"\nRANK ANALYSIS:")
    print(f"  Effective Rank (tol={tol}): {rank}")
    print(f"  Phase 42 Ceiling (12): {'EXCEEDED' if rank > 12 else 'NOT EXCEEDED'}")
    
    # Orthogonality Check
    print("\nORTHOGONALITY CHECK:")
    # Geometric Phase between scalar (0.5) and bivector sum (rest of components)
    # The multivector is v = [0.5, 0, 0, v3, 0, v5, v6, 0, 0, v9, v10, 0, v12, 0, 0, 0]
    # scalar = [0.5, 0, ...]
    # bivector = [0, 0, ..., v3, ...]
    # They are orthogonal in R^16.
    
    phases = []
    for n in range(N):
        scalar_part = spinors[n, 0]
        bivector_part = spinors[n, 1:]
        bv_norm = np.linalg.norm(bivector_part)
        # dot(scalar, bivector) should be 0.
        dot_val = scalar_part * 0.0 # scalar component of bivector is 0.
        # angle = arctan(bv_norm / scalar_part)
        phase_deg = np.degrees(np.arctan2(bv_norm, scalar_part))
        phases.append(phase_deg)
    
    mean_phase = np.mean(phases)
    print(f"  Mean Geometric Phase (Scalar vs Bivector): {mean_phase:.4f} degrees")
    print(f"  Standard Deviation: {np.std(phases):.4f}")
    
    # Save results
    results = {
        "phase": "43b",
        "n_zeros": N,
        "rank": int(rank),
        "phase_42_ceiling": 12,
        "ceiling_exceeded": bool(rank > 12),
        "eigenvalues": [float(e) for e in evals],
        "geometric_phases": [float(p) for p in phases],
        "mean_phase": float(mean_phase),
        "std_dev_phase": float(np.std(phases))
    }
    
    with open('phase43b_rank_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to phase43b_rank_results.json")

if __name__ == "__main__":
    main()
