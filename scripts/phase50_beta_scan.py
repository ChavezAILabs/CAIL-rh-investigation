import numpy as np
import json
from scipy.special import gammainc, gammaincinv

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

def sample_beta_spacings(beta, n, mean_spacing=2.3):
    # P_beta(s) = a * s^beta * exp(-b * s^2)
    # Mean spacing <sRequest> = Gamma((beta+2)/2) / (b^0.5 * Gamma((beta+1)/2))
    # Let <sRequest> = mean_spacing
    # b = [Gamma((beta+2)/2) / (mean_spacing * Gamma((beta+1)/2))]^2
    from scipy.special import gamma
    b = (gamma((beta + 2) / 2.0) / (mean_spacing * gamma((beta + 1) / 2.0)))**2
    
    # CDF(s) = P( (beta+1)/2, b*s^2 ) where P is regularized lower incomplete gamma
    u = np.random.rand(n)
    s_sq = gammaincinv((beta + 1) / 2.0, u) / b
    return np.sqrt(s_sq)

np.random.seed(50)
n_points = 100
mean_spacing = 2.3
gamma_start = 14.134725141734695
betas = [0.5, 1.0, 1.5, 2.0]

all_payloads = {}

for beta in betas:
    spacings = sample_beta_spacings(beta, n_points - 1, mean_spacing)
    gammas = [gamma_start]
    for s in spacings:
        gammas.append(gammas[-1] + s)
    
    vectors = []
    for i, g in enumerate(gammas):
        Fv = F_16d(g, sigma=0.5)
        vectors.append({
            "n": i + 1,
            "gamma": float(g),
            "F_vector": [float(x) for x in Fv]
        })
    
    label = f"Beta_{beta}"
    all_payloads[label] = {
        "beta": beta,
        "n_vectors": len(vectors),
        "vectors": vectors
    }

with open("phase50_beta_scan_vectors.json", "w") as f:
    json.dump(all_payloads, f, indent=2)

print("Generated phase50_beta_scan_vectors.json for betas [0.5, 1.0, 1.5, 2.0]")
