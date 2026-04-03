
import numpy as np
import json

# ============================================================
# SEDENION ENGINE
# ============================================================

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

# Standard ZDTP Gateways
GATEWAY_ORDER = ['S1', 'S2', 'S3A', 'S3B', 'S4', 'S5']
GATEWAYS_16D = {
    'S1':  make16([(3,  1.0)]),
    'S2':  make16([(5,  1.0)]),
    'S3A': make16([(10, 1.0)]),
    'S3B': make16([(6,  1.0)]),
    'S4':  make16([(9,  1.0)]),
    'S5':  make16([(12, 1.0)]),
}

def compute_local_zdtp(F_16):
    mags = [np.sqrt(norm_sq(cd_mul(F_16, GATEWAYS_16D[g]))) for g in GATEWAY_ORDER]
    mu = np.mean(mags)
    sigma = np.std(mags)
    return 1.0 - sigma / mu, mu

def detect_bilateral_pairs(v, threshold=0.01):
    pairs = 0
    n = len(v)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(v[i] + v[j]) < threshold or abs(v[i] - v[j]) < threshold:
                pairs += 1
    return pairs

print("Loading vectors...")
with open('phase56_density_scan_vectors.json', 'r') as f:
    vectors = json.load(f)

results = []
for v in vectors:
    conv, mu = compute_local_zdtp(v['F_vector'])
    pairs = detect_bilateral_pairs(v['F_vector'])
    results.append({
        "n": v['n'],
        "gamma": v['gamma'],
        "convergence": float(conv),
        "mean_magnitude": float(mu),
        "energy": v['energy'],
        "bilateral_pairs": pairs
    })

with open("phase56_density_scan_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Processed {len(results)} vectors locally.")
