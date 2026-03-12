"""
RH Phase 12B — Skewness Artifact Test
======================================
Question: Is the -1.42 skewness of actual Riemann zeros on the P2 embed_pair
projection (Phase 11D) a transformation artifact or a genuine spectral signal?

Key mathematical note:
  embed_pair(g1, g2) = [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
  P2 = [0, 0, 0, 1, -1, 0, 0, 0]
  P2 projection = g1*g2/(g1+g2) - (g1+g2)/2
                = -(g1^2 + g2^2) / (2*(g1+g2))

  This is ALWAYS <= 0 for positive gaps. Negative skewness is structurally
  guaranteed by the P2 direction. The question is: does actual's skewness
  (-1.42) exceed what the gap distribution's mean/variance alone predicts?

Test design:
  - Actual: first 98 gaps (97 pairs)
  - GUE (Wigner surmise): seeds 1-5, mean-matched
  - Poisson (Exponential): seeds 1-5, mean-matched
  - Gaussian control: seeds 1-5, mean+std matched, clipped positive
  - Uniform control: seeds 1-5, mean-matched, symmetric, range-matched

  For each: compute raw gap stats AND P2 projection stats (mean, std, skew, kurtosis).
  Gaussian and Uniform controls are the key new additions — if they show -1.42,
  skewness is determined by mu/sigma alone (artifact). If they show ~-0.45
  (like GUE), actual zeros have genuine extra skewness.

Output: p12b_results.json + printed summary table
"""

import json
import math
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── Load actual gaps ─────────────────────────────────────────────────────────
with open(os.path.join(script_dir, 'rh_gaps.json'), 'r') as f:
    all_gaps = json.load(f)

gaps_actual = all_gaps[:98]   # first 98 gaps → 97 consecutive pairs
N_GAPS  = len(gaps_actual)    # 98
N_PAIRS = N_GAPS - 1          # 97

mean_gap = sum(gaps_actual) / N_GAPS
var_gap  = sum((g - mean_gap)**2 for g in gaps_actual) / N_GAPS
std_gap  = math.sqrt(var_gap)

print(f"Actual gaps: n={N_GAPS}, mean={mean_gap:.6f}, std={std_gap:.6f}")
print(f"Consecutive pairs: {N_PAIRS}")

# ── P2 vector and embed_pair ──────────────────────────────────────────────────
P2 = [0, 0, 0, 1, -1, 0, 0, 0]   # v2 = (0,0,0,1,-1,0,0,0)

def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1 - g2, g1*g2/s, (g1+g2)/2.0, g1/s, g2/s, (g1-g2)**2/s]

def dot(v, w):
    return sum(a*b for a, b in zip(v, w))

def project_p2(gaps):
    """97 consecutive gap pairs → 97 P2 scalar projections."""
    return [dot(embed_pair(gaps[i], gaps[i+1]), P2) for i in range(len(gaps)-1)]

# ── Statistical moments ───────────────────────────────────────────────────────
def moments(xs):
    n = len(xs)
    mu  = sum(xs) / n
    var = sum((x - mu)**2 for x in xs) / n
    sd  = math.sqrt(var) if var > 0 else 1e-300
    skew = sum((x - mu)**3 for x in xs) / n / sd**3
    kurt = sum((x - mu)**4 for x in xs) / n / sd**4 - 3.0   # excess kurtosis
    return {"n": n, "mean": mu, "std": sd, "skewness": skew, "excess_kurtosis": kurt}

# ── Samplers ──────────────────────────────────────────────────────────────────
def sample_wigner(n, mean, seed):
    """GUE Wigner surmise (Rayleigh), scaled to target mean."""
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return samples

def sample_poisson(n, mean, seed):
    """Poisson (Exponential), scaled to target mean."""
    rng = random.Random(seed)
    return [-mean * math.log(rng.random() or 1e-300) for _ in range(n)]

def sample_gaussian(n, mean, std, seed, clip_min=0.05):
    """Gaussian N(mean, std), clipped to clip_min (ensures positive gaps)."""
    rng = random.Random(seed)
    samples = []
    while len(samples) < n:
        # Box-Muller
        u1, u2 = rng.random() or 1e-300, rng.random() or 1e-300
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        x = mean + std * z
        if x >= clip_min:
            samples.append(x)
    return samples

def sample_uniform(n, mean, half_range, seed):
    """Uniform [mean - half_range, mean + half_range], clipped to 0.05."""
    rng = random.Random(seed)
    lo = max(0.05, mean - half_range)
    hi = mean + half_range
    return [lo + (hi - lo) * rng.random() for _ in range(n)]

# ── Run all distributions ─────────────────────────────────────────────────────
results = {}

# Actual
proj_actual = project_p2(gaps_actual)
results['actual'] = {
    'raw_gaps': moments(gaps_actual),
    'p2_projection': moments(proj_actual),
    'raw_proj_values': proj_actual,
}

# Synthetics: 5 seeds each
SEEDS = [1, 2, 3, 4, 5]
half_range = std_gap * math.sqrt(3)   # Uniform variance = std_gap^2 → half_range = std*sqrt(3)

for dist_name, sampler_fn in [
    ('gue',      lambda n, seed: sample_wigner(n, mean_gap, seed)),
    ('poisson',  lambda n, seed: sample_poisson(n, mean_gap, seed)),
    ('gaussian', lambda n, seed: sample_gaussian(n, mean_gap, std_gap, seed)),
    ('uniform',  lambda n, seed: sample_uniform(n, mean_gap, half_range, seed)),
]:
    dist_results = []
    for seed in SEEDS:
        gaps_syn = sampler_fn(N_GAPS, seed)
        proj_syn = project_p2(gaps_syn)
        dist_results.append({
            'seed': seed,
            'raw_gaps': moments(gaps_syn),
            'p2_projection': moments(proj_syn),
        })
    results[dist_name] = dist_results

# ── Print summary table ───────────────────────────────────────────────────────
def avg(vals): return sum(vals) / len(vals)

print("\n" + "="*75)
print("PHASE 12B — P2 PROJECTION SKEWNESS ARTIFACT TEST")
print("="*75)
print(f"\n{'Distribution':<14} {'Raw skew':>10} {'P2 skew':>10} {'P2 kurt':>10}  Notes")
print("-"*65)

# Actual
ra = results['actual']
print(f"{'actual':<14} {ra['raw_gaps']['skewness']:>10.4f} "
      f"{ra['p2_projection']['skewness']:>10.4f} "
      f"{ra['p2_projection']['excess_kurtosis']:>10.4f}  <- Phase 11D reference")

# Synthetics (mean over seeds)
dist_labels = {
    'gue':      'GUE (5 seeds)',
    'poisson':  'Poisson (5s)',
    'gaussian': 'Gaussian (5s)',
    'uniform':  'Uniform (5s)',
}
dist_notes = {
    'gue':      'matches prior phases',
    'poisson':  'matches prior phases',
    'gaussian': '<- KEY control: sym input, mean+std matched',
    'uniform':  '<- KEY control: sym input, mean-matched',
}
for dist_name, label in dist_labels.items():
    runs = results[dist_name]
    raw_skews = [r['raw_gaps']['skewness'] for r in runs]
    p2_skews  = [r['p2_projection']['skewness'] for r in runs]
    p2_kurts  = [r['p2_projection']['excess_kurtosis'] for r in runs]
    print(f"{label:<14} {avg(raw_skews):>10.4f} {avg(p2_skews):>10.4f} "
          f"{avg(p2_kurts):>10.4f}  {dist_notes[dist_name]}")

print("\nP2 projection formula: -(g1^2 + g2^2) / (2*(g1+g2))  [always <= 0 for positive gaps]")
print("\nVerdict guide:")
print("  Gaussian P2 skew ~= actual (-1.42) -> ARTIFACT (mu/sigma determines skew)")
print("  Gaussian P2 skew ~= GUE    (-0.45) -> GENUINE  (actual zeros extra-skewed)")
print("  Intermediate      -> PARTIAL (some artifact, some genuine)")

# ── Save results ──────────────────────────────────────────────────────────────
# Strip raw_proj_values for cleaner JSON (keep moments only)
results_clean = {k: v for k, v in results.items() if k != 'actual'}
results_clean['actual'] = {
    'raw_gaps': results['actual']['raw_gaps'],
    'p2_projection': results['actual']['p2_projection'],
}

summary = {
    "phase": "12B",
    "question": "Is actual P2 skewness (-1.42) a transformation artifact?",
    "n_gaps": N_GAPS,
    "n_pairs": N_PAIRS,
    "actual_mean_gap": mean_gap,
    "actual_std_gap": std_gap,
    "p2_formula": "-(g1^2 + g2^2) / (2*(g1+g2)) — always <= 0",
    "seeds": SEEDS,
    "results": results_clean,
    "verdict_thresholds": {
        "artifact": "Gaussian P2 skew within 0.2 of actual (-1.42)",
        "genuine":  "Gaussian P2 skew within 0.2 of GUE (-0.45)",
        "partial":  "Gaussian P2 skew between -0.65 and -1.22",
    }
}

out_path = os.path.join(script_dir, 'p12b_results.json')
with open(out_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nResults saved to: p12b_results.json")
