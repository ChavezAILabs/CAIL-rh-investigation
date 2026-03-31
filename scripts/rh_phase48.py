"""
rh_phase48.py  --  GENERATOR HALF
===================================
Phase 48 -- gamma_n-Scaling of ZDTP Convergence
The Asymptotic Structure of Sedenion Transmission

Division of labor:
  Claude Code (this script): generate F-vectors for all scan bands, save to JSON
  Claude Desktop + CAILculator: run real ZDTP cascade on each batch, return results
  Claude Code (rh_phase48_analysis.py): fit, analyze, summarize after Desktop returns

Output files (for Claude Desktop):
  phase48_fvectors_band1.json   -- n=1..100,   step=1, sigma=0.5  (100 vectors)
  phase48_fvectors_band2.json   -- n=101..500,  step=1, sigma=0.5  (400 vectors)
  phase48_fvectors_band3.json   -- n=501..2000, step=3, sigma=0.5  (~500 vectors)
  phase48_fvectors_band4.json   -- n=2001..5000,step=5, sigma=0.5  (~600 vectors)
  phase48_fvectors_sigma04.json -- n=1..100,   step=1, sigma=0.4  (100 vectors, Track E)

Instructions for Claude Desktop (embedded in each file's metadata):
  For each vector, run CAILculator ZDTP with dimensions=[16, 32, 64], all 6 gateways.
  Return: n, gamma, convergence_score, gateway_magnitudes [S1, S2, S3A, S3B, S4, S5],
          mean_magnitude, std_magnitude.

Date: 2026-03-30
"""

import numpy as np
import json, time

# ============================================================
# SEDENION ENGINE (unchanged from Phase 42)
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
        rp = ROOT_16D_BASE[p]
        rn = np.sqrt(norm_sq(rp))
        f = [0.0] * 16
        f[0] = np.cos(theta)
        for i in range(16): f[i] += np.sin(theta) * rp[i] / rn
        r = cd_mul(r, f)
    r[4] += (sigma - 0.5) / sqrt2
    r[5] -= (sigma - 0.5) / sqrt2
    return r

# ============================================================
# LOAD DATA
# ============================================================
print("Loading Riemann zeros...")
gammas_all = json.load(open("rh_zeros_10k.json"))
print(f"  Loaded {len(gammas_all)} zeros")
print(f"  gamma range: [{gammas_all[0]:.3f}, {gammas_all[4999]:.3f}] (first 5000)")

t0 = time.time()

# ============================================================
# BATCH DEFINITIONS
# ============================================================
# (label, filename, idx_start, idx_end, step, sigma)
BATCHES = [
    ('Band1',    'phase48_fvectors_band1.json',   0,    100,  1, 0.5),
    ('Band2',    'phase48_fvectors_band2.json',   100,  500,  1, 0.5),
    ('Band3',    'phase48_fvectors_band3.json',   500,  2000, 3, 0.5),
    ('Band4',    'phase48_fvectors_band4.json',   2000, 5000, 5, 0.5),
    ('Sigma04',  'phase48_fvectors_sigma04.json', 0,    100,  1, 0.4),
]

DESKTOP_INSTRUCTIONS = (
    "For each entry in 'vectors': run CAILculator ZDTP with dimensions=[16, 32, 64], "
    "all 6 Canonical Six gateways (S1=e3, S2=e5, S3A=e10, S3B=e6, S4=e9, S5=e12). "
    "Record: n, gamma, convergence_score, gateway_magnitudes "
    "[S1, S2, S3A, S3B, S4, S5] (64D), mean_magnitude, std_magnitude. "
    "Save results to phase48_zdtp_{band}.json with same structure."
)

# ============================================================
# GENERATE BATCHES
# ============================================================
batch_summary = []

for label, filename, idx_start, idx_end, step, sigma in BATCHES:
    indices = list(range(idx_start, idx_end, step))
    vectors = []

    for idx in indices:
        gamma = gammas_all[idx]
        Fv = F_16d(gamma, sigma=sigma)
        vectors.append({
            "n":        idx + 1,
            "gamma":    float(gamma),
            "sigma":    sigma,
            "F_vector": [float(x) for x in Fv],
            "norm_sq":  float(norm_sq(Fv)),
        })

    payload = {
        "band":         label,
        "sigma":        sigma,
        "n_vectors":    len(vectors),
        "n_range":      [vectors[0]["n"], vectors[-1]["n"]],
        "gamma_range":  [vectors[0]["gamma"], vectors[-1]["gamma"]],
        "primes":       PRIMES_6,
        "operator":     "AIEX-001a: F(sigma+it) = prod_p exp_sed(t*log(p)*r_p/||r_p||)",
        "instructions": DESKTOP_INSTRUCTIONS.replace("{band}", label.lower()),
        "vectors":      vectors,
    }

    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)

    gamma_lo = vectors[0]["gamma"]
    gamma_hi = vectors[-1]["gamma"]
    print(f"  {label:8s}: {len(vectors):4d} vectors  "
          f"n={vectors[0]['n']}..{vectors[-1]['n']}  "
          f"gamma=[{gamma_lo:.1f}, {gamma_hi:.1f}]  "
          f"sigma={sigma}  -> {filename}")

    batch_summary.append({
        "band":       label,
        "filename":   filename,
        "n_vectors":  len(vectors),
        "n_range":    [vectors[0]["n"], vectors[-1]["n"]],
        "gamma_range": [gamma_lo, gamma_hi],
        "sigma":      sigma,
    })

# ============================================================
# MANIFEST
# ============================================================
manifest = {
    "phase": 48,
    "date": "2026-03-30",
    "description": "F-vector batches for Claude Desktop ZDTP cascade",
    "total_vectors": sum(b["n_vectors"] for b in batch_summary),
    "batches": batch_summary,
    "expected_output_files": [
        f"phase48_zdtp_{b['band'].lower()}.json" for b in batch_summary
    ],
    "analysis_script": "rh_phase48_analysis.py",
    "desktop_instructions": DESKTOP_INSTRUCTIONS,
}
with open("phase48_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"\n  Total vectors generated: {manifest['total_vectors']}")
print(f"  Elapsed: {time.time()-t0:.1f}s")
print("\nOutput files:")
for b in batch_summary:
    print(f"  {b['filename']}  ({b['n_vectors']} vectors)")
print("  phase48_manifest.json")
print("\nReady for Claude Desktop ZDTP cascade.")
print("Hand off batch files in order: Band1 -> Band2 -> Band3 -> Band4 -> Sigma04")
print("Then run rh_phase48_analysis.py once all phase48_zdtp_*.json files are returned.")
