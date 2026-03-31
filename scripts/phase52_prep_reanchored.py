import numpy as np
import json

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

ROOT_16D_BASE = {
    2:  make16([(3,  1.0), (12, -1.0)]),
    3:  make16([(5,  1.0), (10,  1.0)]),
    5:  make16([(3,  1.0), (6,   1.0)]),
    7:  make16([(2,  1.0), (7,  -1.0)]),
    11: make16([(2,  1.0), (7,   1.0)]),
    13: make16([(6,  1.0), (9,   1.0)]),
}
PRIMES_6 = [2, 3, 5, 7, 11, 13]

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
    sqrt2 = np.sqrt(2.0)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# Load true zeros
with open('rh_zeros_10k.json', 'r') as f:
    zeros = json.load(f)

payload = []

# Anchor Checks (sigma=0.5)
for n in [1000, 5000]:
    g = zeros[n-1]
    Fv = F_16d(g, sigma=0.5)
    payload.append({
        "type": "anchor",
        "n": n,
        "gamma": float(g),
        "sigma": 0.5,
        "F_16d": [float(x) for x in Fv]
    })

# dense sigma-scan for n=10,000
n_10k = 10000
g_10k = zeros[n_10k-1]
sigmas = np.linspace(0.0, 1.0, 21)

for s in sigmas:
    Fv = F_16d(g_10k, sigma=s)
    payload.append({
        "type": "sigma_scan",
        "n": n_10k,
        "gamma": float(g_10k),
        "sigma": float(s),
        "F_16d": [float(x) for x in Fv]
    })

with open("phase52_reanchored_vectors.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"Generated {len(payload)} vectors to phase52_reanchored_vectors.json")
print(f"Verified gamma_10000: {g_10k}")
