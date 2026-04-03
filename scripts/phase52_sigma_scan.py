import numpy as np
import json
import time

def cd_conj(v):
    c = list(v)
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    c1 = [x - y for x, y in zip(cd_mul(a1, b1), cd_mul(cd_conj(b2), a2))]
    c2 = [x + y for x, y in zip(cd_mul(b2, a1), cd_mul(a2, cd_conj(b1)))]
    return c1 + c2

def norm_sq(v): return sum(x * x for x in v)

def make16(pairs):
    v = [0.0] * 16
    for i, val in pairs: v[i] = float(val)
    return v

sqrt2 = np.sqrt(2.0)

ROOT_16D_BASE = {
    2:  make16([(3,  1.0), (12, -1.0)]),
    3:  make16([(5,  1.0), (10,  1.0)]),
    5:  make16([(3,  1.0), (6,   1.0)]),
    7:  make16([(2,  1.0), (7,  -1.0)]),
    11: make16([(2,  1.0), (7,   1.0)]),
    13: make16([(6,  1.0), (9,   1.0)]),
}
PRIMES_6 = [2, 3, 5, 7, 11, 13]

GATEWAYS_16D = {
    'S1':  make16([(3,  1.0)]),   # e3  -- Master
    'S2':  make16([(5,  1.0)]),   # e5  -- Multi-modal
    'S3A': make16([(10, 1.0)]),   # e10 -- Discontinuous
    'S3B': make16([(6,  1.0)]),   # e6  -- Diagonal A
    'S4':  make16([(9,  1.0)]),   # e9  -- Diagonal B
    'S5':  make16([(12, 1.0)]),   # e12 -- Orthogonal
}
GATEWAY_ORDER = ['S1', 'S2', 'S3A', 'S3B', 'S4', 'S5']

def F_16d(t, sigma=0.5):
    r = make16([(0, 1.0)])
    for p in PRIMES_6:
        theta = t * np.log(p)
        rp = ROOT_16D_BASE[p]
        rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16
        f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

def zdtp_convergence(F_16):
    mags = [float(np.sqrt(norm_sq(cd_mul(F_16, GATEWAYS_16D[g])))) for g in GATEWAY_ORDER]
    mu        = float(np.mean(mags))
    sigma_mag = float(np.std(mags))
    if mu == 0: return 0.0, mags, mu, sigma_mag
    return 1.0 - sigma_mag / mu, mags, mu, sigma_mag

# Load zeros
print("Loading Riemann zeros...")
with open('rh_zeros_10k.json', 'r') as f:
    zeros = json.load(f)

idx = 10000
gamma = zeros[idx - 1]
print(f"Targeting Zero n={idx}, gamma={gamma:.4f}")

sigmas = np.linspace(0.0, 1.0, 101)
results = []

print("Running sigma-scan...")
for s in sigmas:
    Fv = F_16d(gamma, sigma=s)
    conv, mags, mu, sig_mag = zdtp_convergence(Fv)
    results.append({
        "sigma": float(s),
        "convergence": float(conv),
        "mean_mag": float(mu),
        "std_mag": float(sig_mag)
    })

payload = {
    "experiment": "Phase 52 Track B - Global sigma-scan",
    "n": idx,
    "gamma": float(gamma),
    "scan_results": results
}

with open("phase52_sigma_scan_n10k.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"Results saved to phase52_sigma_scan_n10k.json")

# Find peak
best_sigma = max(results, key=lambda x: x['convergence'])
print(f"Peak convergence: {best_sigma['convergence']:.6f} at sigma={best_sigma['sigma']:.3f}")
