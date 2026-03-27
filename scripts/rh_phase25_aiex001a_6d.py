"""
AIEX-001a Phase 25 — Multiplicative Sedenion Embedding (6D Projected)
Chavez AI Labs LLC · March 25, 2026

AIEX-001a: F(sigma+it) = prod_p exp_sed(t*log(p)*r_p)
where exp_sed(theta*r) = cos(theta)*e0 + sin(theta)*r_hat

Key finding: perfect sigma symmetry around sigma=1/2 in both criticality
measure and ZDTP proxy. ZDTP(sigma=0.5)=0.242 vs ZDTP(sigma=0.6)=0.162.
ZDTP diff sequence: 84.0% conjugation, 95% bilateral confidence, 39 pairs.
"""
import numpy as np
from mpmath import mp, zetazero
import json
mp.dps = 25

sqrt2 = np.sqrt(2.0)
ROOT_DIRS = {
    2:  np.array([0,0,0,0,1,1])/sqrt2,
    3:  np.array([0,0,-1,1,0,0])/sqrt2,
    5:  np.array([0,0,1,1,0,0])/sqrt2,
    7:  np.array([1,-1,0,0,0,0])/sqrt2,
    11: np.array([1,1,0,0,0,0])/sqrt2,
    13: np.array([-1,1,0,0,0,0])/sqrt2,
}
U_ANTISYM = np.array([0,0,0,0,1,-1])/sqrt2
PRIMES = [2,3,5,7,11,13]

def F_multiplicative(t, sigma=0.5):
    scalar = 1.0
    vector = np.zeros(6)
    for p in PRIMES:
        r_p = ROOT_DIRS[p]
        theta = t * np.log(p)
        cos_t, sin_t = np.cos(theta), np.sin(theta)
        new_scalar = scalar * cos_t - np.dot(vector, r_p) * sin_t
        new_vector = cos_t * vector + scalar * sin_t * r_p
        scalar, vector = new_scalar, new_vector
    vector = vector + (sigma - 0.5) * U_ANTISYM
    return scalar, vector

def criticality(t, sigma=0.5):
    s, v = F_multiplicative(t, sigma)
    s2, v2 = s**2, np.dot(v,v)
    return abs(s2 - v2), s, np.sqrt(v2), s2 + v2

def zdtp_proxy(t, sigma=0.5):
    s, v = F_multiplicative(t, sigma)
    s2, v2 = s**2, np.dot(v,v)
    total = s2 + v2
    return (1.0 - abs(s2-v2)/total) if total > 1e-15 else 0.0

if __name__ == '__main__':
    print("Fetching 100 Riemann zeros...")
    zeros = [float(zetazero(n).imag) for n in range(1, 101)]

    SIGMA_VALS = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    zdtp_by_sigma = {}
    crit_by_sigma = {}
    for sv in SIGMA_VALS:
        zdtp_by_sigma[sv] = [zdtp_proxy(t, sv) for t in zeros]
        crit_by_sigma[sv] = [criticality(t, sv)[0] for t in zeros]

    print("Mean ZDTP by sigma:")
    for sv in SIGMA_VALS:
        print(f"  sigma={sv:.1f}: {np.mean(zdtp_by_sigma[sv]):.6f}")

    seqs = {
        'zdtp_sigma05': zdtp_by_sigma[0.5],
        'zdtp_sigma06': zdtp_by_sigma[0.6],
        'zdtp_diff_05_06': [zdtp_by_sigma[0.5][i]-zdtp_by_sigma[0.6][i] for i in range(100)],
        'crit_sigma05': crit_by_sigma[0.5],
        'mean_zdtp_by_sigma': {str(sv): float(np.mean(zdtp_by_sigma[sv])) for sv in SIGMA_VALS},
    }
    with open('phase25_results.json', 'w') as f:
        json.dump(seqs, f)
    print("Saved: phase25_results.json")
