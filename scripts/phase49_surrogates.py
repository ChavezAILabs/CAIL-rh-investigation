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
    # sigma terms are added to indices 4 and 5 as per rh_phase48.py
    sqrt2 = np.sqrt(2.0)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# Generate Surrogates
np.random.seed(49) # For reproducibility
n_points = 100
mean_spacing = 2.3
gamma_start = 14.134725141734695

# GUE (Wigner)
u_gue = np.random.rand(n_points - 1)
spacings_gue = mean_spacing * np.sqrt(-4.0 / np.pi * np.log(1.0 - u_gue))
gammas_gue = [gamma_start]
for s in spacings_gue:
    gammas_gue.append(gammas_gue[-1] + s)

# Poisson
u_poi = np.random.rand(n_points - 1)
spacings_poi = -mean_spacing * np.log(1.0 - u_poi)
gammas_poi = [gamma_start]
for s in spacings_poi:
    gammas_poi.append(gammas_poi[-1] + s)

# Construct F-vectors
def generate_payload(label, gammas):
    vectors = []
    for i, g in enumerate(gammas):
        Fv = F_16d(g, sigma=0.5)
        vectors.append({
            "n": i + 1,
            "gamma": float(g),
            "sigma": 0.5,
            "F_vector": [float(x) for x in Fv],
            "norm_sq": float(norm_sq(Fv))
        })
    return {
        "band": label,
        "sigma": 0.5,
        "n_vectors": len(vectors),
        "vectors": vectors
    }

with open("phase49_fvectors_gue.json", "w") as f:
    json.dump(generate_payload("GUE_Surrogate", gammas_gue), f, indent=2)

with open("phase49_fvectors_poisson.json", "w") as f:
    json.dump(generate_payload("Poisson_Surrogate", gammas_poi), f, indent=2)

print("Generated phase49_fvectors_gue.json and phase49_fvectors_poisson.json")
