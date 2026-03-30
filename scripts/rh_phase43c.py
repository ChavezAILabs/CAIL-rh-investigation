"""
rh_phase43c.py
==============
Phase 43c: The "Wobble" Test
Compares Spinor Rank and Geometric Phase Stability across:
sigma = 0.4, 0.5 (Critical Line), and 0.6

Chavez AI Labs LLC — March 28, 2026
"""

import numpy as np
import json

B_INDICES = [3, 5, 10, 6, 9, 12]

def compute_rank_and_phase(gammas, signatures, sigma_val):
    N = len(gammas)
    K = signatures.shape[1]
    weights = 1.0 / np.sqrt(gammas)
    
    spinors = []
    for n in range(N):
        t = gammas[n]
        psi = np.zeros(16)
        psi[0] = 0.5 # Scalar remains fixed at 0.5 per instructions
        
        for k in range(K):
            val = 0.0
            for m in range(N):
                val += weights[m] * np.cos(t * gammas[m]) * signatures[m, k]
            psi[B_INDICES[k]] = val
        spinors.append(psi)
    
    spinors = np.array(spinors)
    
    # Rank Analysis
    G = np.dot(spinors, spinors.T)
    evals = sorted(np.linalg.eigvalsh(G), reverse=True)
    rank = np.sum(np.array(evals) > 1e-12)
    
    # Geometric Phase Analysis
    phases = []
    for n in range(N):
        bv_norm = np.linalg.norm(spinors[n, 1:])
        phase_deg = np.degrees(np.arctan2(bv_norm, 0.5))
        phases.append(phase_deg)
        
    return {
        "sigma": sigma_val,
        "rank": int(rank),
        "mean_phase": float(np.mean(phases)),
        "std_dev_phase": float(np.std(phases)),
        "max_eval": float(evals[0]),
        "min_pos_eval": float(evals[rank-1]) if rank > 0 else 0.0
    }

def main():
    # Load Wobble Data (0.4 and 0.6)
    with open('phase43c_zdtp_signatures_wobble.json', 'r') as f:
        wobble_data = json.load(f)
    
    # Load Baseline Data (0.5)
    with open('phase43b_zdtp_signatures.json', 'r') as f:
        baseline_data = json.load(f)
        
    results = []
    
    # Test 0.5 (Baseline)
    g_05 = np.array([item['gamma'] for item in baseline_data])
    s_05 = np.array([item['signature'] for item in baseline_data])
    print("Analyzing sigma = 0.5 (Baseline)...")
    results.append(compute_rank_and_phase(g_05, s_05, 0.5))
    
    # Test 0.4 and 0.6
    for sig_str in ["sigma_0.4", "sigma_0.6"]:
        sig_val = float(sig_str.split('_')[1])
        data = wobble_data[sig_str]
        g = np.array([item['gamma'] for item in data])
        s = np.array([item['signature'] for item in data])
        print(f"Analyzing {sig_str}...")
        results.append(compute_rank_and_phase(g, s, sig_val))
        
    # Print Summary Table
    print("\n" + "="*65)
    print(f"{'Sigma':<10} | {'Rank':<6} | {'Mean Phase':<12} | {'Phase StdDev':<12}")
    print("-"*65)
    for r in results:
        print(f"{r['sigma']:<10.1f} | {r['rank']:<6} | {r['mean_phase']:<12.4f} | {r['std_dev_phase']:<12.4f}")
    print("="*65)
    
    # Check Prediction
    baseline = results[0]
    shattered = any(r['std_dev_phase'] > baseline['std_dev_phase'] * 2 for r in results[1:])
    rank_shift = any(r['rank'] != baseline['rank'] for r in results[1:])
    
    print("\nPREDICTION VERIFICATION:")
    print(f"  Rank Shift Detected: {rank_shift}")
    print(f"  Phase Stability Shattered (StdDev boost): {shattered}")
    
    if rank_shift or shattered:
        print("\nCONCLUSION: The 'Wobble' confirms the Critical Line requirement.")
    else:
        print("\nCONCLUSION: The Sedenionic Spinor is unexpectedly robust off-line.")

    with open('phase43c_wobble_results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
