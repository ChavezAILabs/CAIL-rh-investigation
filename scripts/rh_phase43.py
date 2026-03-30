"""
rh_phase43.py
=============
Phase 43: Sedenionic Spinor Field Reconstruction
Implementation of the sedenionic spinor psi(t) using ZDTP signatures
modulated by Riemann zeros.

Definition:
  psi(t) = 0.5 * e0 + sum_{k=1}^6 (sum_n w_n * cos(t * gamma_n) * S_{n,k}) * Bk

Where:
  gamma_n: Riemann zeros
  S_{n,k}: ZDTP gateway magnitudes
  Bk: Canonical Six bivectors {e3, e5, e6, e9, e10, e12}

Chavez AI Labs LLC — March 28, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import json

# Riemann Zeros (first 10)
GAMMAS = np.array([
    14.13472514, 21.02203964, 25.01085758, 30.42487613, 32.93506159,
    37.58617816, 40.91871901, 43.32707328, 48.00515088, 49.77383248
])

# ZDTP Signatures (Magnitudes for gateways S1, S2, S3A, S3B, S4, S5)
# S3B and S4 are symmetric pairs.
SIGNATURES = np.array([
    [1.936, 3.819, 2.266, 4.155, 4.155, 2.370], # n=1
    [5.022, 1.915, 5.593, 2.550, 2.550, 4.445], # n=2
    [2.772, 3.961, 3.467, 4.442, 4.442, 3.712], # n=3
    [3.731, 4.343, 3.790, 4.350, 4.350, 4.066], # n=4
    [4.589, 4.700, 3.274, 3.651, 3.651, 4.375], # n=5
    [2.533, 4.718, 2.844, 4.842, 4.842, 3.118], # n=6
    [3.106, 3.559, 3.422, 3.054, 3.054, 3.639], # n=7
    [2.528, 3.029, 2.811, 3.520, 3.520, 2.679], # n=8
    [3.505, 3.491, 4.057, 4.501, 4.501, 3.078], # n=9
    [2.686, 2.672, 2.811, 2.708, 2.708, 3.047], # n=10
])

# Mapping to Bivector Indices (e3, e5, e10, e6, e9, e12)
# Chosen to match symmetric pairs S3B/S4 -> e6/e9
B_INDICES = [3, 5, 10, 6, 9, 12]

def compute_psi(t, gammas, signatures, weights=None):
    if weights is None:
        weights = 1.0 / np.sqrt(gammas)
    
    N = len(gammas)
    K = signatures.shape[1]
    
    # Scalar component
    psi = np.zeros(16)
    psi[0] = 0.5
    
    # Imaginary components
    for k in range(K):
        # Modulation sum
        val = 0.0
        for n in range(N):
            val += weights[n] * np.cos(t * gammas[n]) * signatures[n, k]
        
        # Assign to bivector basis
        idx = B_INDICES[k]
        psi[idx] = val
        
    return psi

def psi_norm_sq(psi):
    return np.sum(psi**2)

# Range of t
t_vals = np.linspace(10, 60, 1000)
density = []

for t in t_vals:
    p = compute_psi(t, GAMMAS, SIGNATURES)
    density.append(psi_norm_sq(p))

density = np.array(density)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t_vals, density, label='Spinor Density $|\psi(t)|^2$', color='blue')
for g in GAMMAS:
    plt.axvline(x=g, color='red', linestyle='--', alpha=0.5, label='Riemann Zero' if g == GAMMAS[0] else "")

plt.title('Phase 43: Sedenionic Spinor Density $|\psi(t)|^2$')
plt.xlabel('t')
plt.ylabel('Density')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('phase43_spinor_density.png')
print("Plot saved to phase43_spinor_density.png")

# Peak analysis
peaks = []
# Simple local maxima
for i in range(1, len(density)-1):
    if density[i] > density[i-1] and density[i] > density[i+1]:
        peaks.append((t_vals[i], density[i]))

print("\nDetected peaks in density:")
for pt, val in sorted(peaks, key=lambda x: -x[1])[:10]:
    # Find closest zero
    dist = np.min(np.abs(GAMMAS - pt))
    print(f"  t={pt:.4f}, val={val:.4f}, dist_to_zero={dist:.4f}")

# Save results
results = {
    "phase": 43,
    "description": "Sedenionic Spinor Field Reconstruction",
    "n_zeros": len(GAMMAS),
    "t_range": [float(t_vals[0]), float(t_vals[-1])],
    "peaks": [{"t": float(p[0]), "val": float(p[1])} for p in peaks]
}
with open('phase43_results.json', 'w') as f:
    json.dump(results, f, indent=2)
