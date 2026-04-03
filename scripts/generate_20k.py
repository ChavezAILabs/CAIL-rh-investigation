import numpy as np
import json
import mpmath

# Constants for F_16d
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

def F_16d(t, sigma=0.5):
    r = make16([(0, 1.0)])
    for p in PRIMES_6:
        theta = float(t * np.log(p))
        rp = ROOT_16D_BASE[p]
        rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16
        f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

print("Calculating Riemann zero n=20,000...")
gamma_20k = mpmath.zetazero(20000).imag
print(f"gamma_20k = {gamma_20k}")

print("Generating F-vector...")
Fv = F_16d(gamma_20k)
energy = norm_sq(Fv)

result = {
    "n": 20000,
    "gamma": float(gamma_20k),
    "F_vector": [float(x) for x in Fv],
    "energy": float(energy)
}

with open("phase58_n20k_vector.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Generated n=20,000 vector with energy {energy:.6f}")
