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
    return r

# Load zeros
with open('CAIL-rh-investigation/data/riemann/rh_zeros_10k.json', 'r') as f:
    zeros = json.load(f)

indices = [1000, 2500, 5000, 7500, 10000]
vectors = []

for idx in indices:
    g = zeros[idx - 1]
    Fv = F_16d(g, sigma=0.5)
    vectors.append({
        "n": idx,
        "gamma": float(g),
        "F_vector": [float(x) for x in Fv]
    })

payload = {
    "band": "Asymptotic_Scan",
    "sigma": 0.5,
    "n_vectors": len(vectors),
    "vectors": vectors
}

with open("phase51_asymptotic_vectors.json", "w") as f:
    json.dump(payload, f, indent=2)

print(f"Generated phase51_asymptotic_vectors.json for n in {indices}")
