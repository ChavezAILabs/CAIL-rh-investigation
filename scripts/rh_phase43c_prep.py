"""
rh_phase43c_prep.py
===================
Generates F vectors for sigma=0.4 and sigma=0.6 for the first 50 zeros.
These will be sent to the generalist for ZDTP signature generation.
"""

import numpy as np
import json

def cd_conj(v):
    c = list(v); c[0] = v[0]
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0]*b[0]]
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

def F_16d(t, sigma=0.5):
    r = make16([(0, 1.0)])
    for p in PRIMES_6:
        theta = t * np.log(p)
        rp = ROOT_16D_BASE[p]; rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16; f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

gammas = json.load(open("rh_zeros_10k.json"))[:50]

wobble_vectors = []
for sigma in [0.4, 0.6]:
    for n, g in enumerate(gammas):
        Fv = F_16d(g, sigma=sigma)
        wobble_vectors.append({
            "n": n + 1,
            "sigma": sigma,
            "gamma": float(g),
            "F_vector": [float(x) for x in Fv]
        })

with open("phase43c_F_vectors_wobble.json", "w") as f:
    json.dump(wobble_vectors, f, indent=2)

print(f"Saved {len(wobble_vectors)} wobble vectors to phase43c_F_vectors_wobble.json")
