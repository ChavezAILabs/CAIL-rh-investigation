"""
RH Phase 13C -- Act/GUE Variance Ratio vs Berry-Keating R_c Per Band
=====================================================================
Question: Does the Act/GUE P2-projection variance ratio per height band
correlate with the BK prime orbit correction R_c(t)?

Motivation:
  Phase 12A: Act/GUE variance ratio is height-dependent (oscillates 0.665-0.756).
  Phase 12C: BK R_c correlates with band-level spacing ratio structure (r=0.579, 10 bands).
  Phase 13B: Mean spacing ratio per band is too flat to detect BK oscillation.
  Phase 13A: Log-prime spectral signal confirmed at individual-ratio level.

Hypothesis: The Act/GUE variance RATIO per band tracks R_c(t_mid). Where R_c is
large (constructive BK interference), actual zeros are further from GUE in variance.
Where R_c is near zero, variance ratio approaches 1.

Method:
  1. 20 bands x 500 zeros (same as 13B)
  2. embed_pair(g1,g2) -> P2 projection per band
  3. P2 variance: actual vs GUE (5 seeds)
  4. Act/GUE variance ratio per band
  5. Pearson r against R_c(t_mid) for cumulative prime sets
  6. Also test 10-band resolution (for direct comparison to Phase 12C)

P2 projection (from embed_pair):
  embed_pair(g1,g2) = [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)^2/s]
  where s = g1 + g2
  P2 component: -(g1^2 + g2^2) / (2*(g1+g2))
  -- this is the actual P2 value used in all prior phases

Significance thresholds:
  n=20 bands: |r| > 0.444
  n=10 bands: |r| > 0.632
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

N_ZEROS  = len(zeros)

# -- P2 projection ------------------------------------------------------------
def p2_proj(g1, g2):
    s = g1 + g2
    if s == 0: return 0.0
    return -(g1**2 + g2**2) / (2.0 * s)

def p2_sequence(gaps):
    return [p2_proj(gaps[i], gaps[i+1]) for i in range(len(gaps)-1)]

def variance(seq):
    n = len(seq)
    if n < 2: return 0.0
    mu = sum(seq) / n
    return sum((x - mu)**2 for x in seq) / (n - 1)

# -- GUE sampler --------------------------------------------------------------
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return samples

# -- BK R_c -------------------------------------------------------------------
def rc_value(t, primes):
    return sum(
        (1.0 / math.sqrt(p)) * math.cos(math.log(p) * t)
        + (1.0 / p) * math.cos(2.0 * math.log(p) * t)
        for p in primes
    )

# -- Pearson r ----------------------------------------------------------------
def pearson_r(x, y):
    n  = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx  = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy  = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    if dx == 0 or dy == 0: return 0.0
    return num / (dx * dy)

# -- Build bands (configurable n_bands) ---------------------------------------
def build_bands(n_bands):
    band_size = N_ZEROS // n_bands
    bands = []
    for k in range(n_bands):
        start = k * band_size
        end   = start + band_size
        bz    = zeros[start:end]
        bg    = gaps_all[start:end-1]
        bands.append({
            'k':        k,
            't_mid':    (bz[0] + bz[-1]) / 2.0,
            'gaps':     bg,
            'mean_gap': sum(bg) / len(bg),
        })
    return bands

GUE_SEEDS = [1, 2, 3, 4, 5]
PRIME_STEPS = [2, 3, 5, 7, 11, 13, 17, 19, 23]
THRESHOLD = {10: 0.6319, 20: 0.4438}

print("="*70)
print("PHASE 13C -- ACT/GUE P2 VARIANCE RATIO vs BK R_c PER BAND")
print("="*70)

all_band_results = {}

for n_bands in [10, 20]:
    bands = build_bands(n_bands)
    t_mids = [b['t_mid'] for b in bands]
    thresh = THRESHOLD[n_bands]

    print(f"\n{'='*60}")
    print(f"  {n_bands}-BAND ANALYSIS  (threshold |r| > {thresh:.4f})")
    print(f"{'='*60}")

    # Actual P2 variance per band
    act_var = []
    for b in bands:
        p2 = p2_sequence(b['gaps'])
        act_var.append(variance(p2))

    # GUE P2 variance per band (5-seed ensemble)
    gue_var_by_seed = []
    for seed in GUE_SEEDS:
        sv = []
        for b in bands:
            gue_gaps = sample_wigner(len(b['gaps']), b['mean_gap'], seed*100 + b['k'])
            sv.append(variance(p2_sequence(gue_gaps)))
        gue_var_by_seed.append(sv)

    gue_var = [
        sum(gue_var_by_seed[s][k] for s in range(len(GUE_SEEDS))) / len(GUE_SEEDS)
        for k in range(n_bands)
    ]

    # Act/GUE ratio per band
    ratio_per_band = [act_var[k] / gue_var[k] if gue_var[k] > 0 else 0
                      for k in range(n_bands)]

    print(f"\nAct/GUE P2 variance ratio per band:")
    print(f"  Range: {min(ratio_per_band):.4f} to {max(ratio_per_band):.4f}")
    print(f"  Mean:  {sum(ratio_per_band)/n_bands:.4f}")

    # Pearson r vs R_c for each prime step
    print(f"\n{'Step':>5}  {'Primes':>28}  {'r':>8}  {'Significant?':>14}")
    print(f"{'-'*60}")

    step_results = []
    signal_primes = []
    for i, p in enumerate(PRIME_STEPS):
        prime_set = PRIME_STEPS[:i+1]
        rc_vec = [rc_value(t, prime_set) for t in t_mids]
        r = pearson_r(rc_vec, ratio_per_band)
        sig = abs(r) > thresh
        if sig: signal_primes.append(p)
        ps = str(prime_set)
        print(f"{i+1:>5}  {ps:>28}  {r:>8.4f}  {'YES ***' if sig else 'no':>14}")
        step_results.append({'primes': prime_set, 'last_prime': p, 'r': r, 'significant': sig})

    # Also try: correlation of R_c with ABSOLUTE variance (not ratio)
    print(f"\n  -- Also: r(R_c, actual P2 variance) and r(R_c, GUE P2 variance) --")
    for i, p in enumerate(PRIME_STEPS):
        prime_set = PRIME_STEPS[:i+1]
        rc_vec = [rc_value(t, prime_set) for t in t_mids]
        r_act = pearson_r(rc_vec, act_var)
        r_gue = pearson_r(rc_vec, gue_var)
        r_ratio = pearson_r(rc_vec, ratio_per_band)
        if i in [0, 4, 8]:   # print select rows
            print(f"  p={p:>2}: r(Rc,act_var)={r_act:>7.4f}  r(Rc,gue_var)={r_gue:>7.4f}  "
                  f"r(Rc,ratio)={r_ratio:>7.4f}")

    print(f"\nSignal primes: {signal_primes if signal_primes else 'None'}")

    # Band detail
    print(f"\n  Band detail (9-prime R_c):")
    rc9 = [rc_value(t, PRIME_STEPS) for t in t_mids]
    print(f"  {'Band':>4}  {'t_mid':>8}  {'act_var':>10}  {'gue_var':>10}  "
          f"{'ratio':>8}  {'R_c(9p)':>10}")
    for k in range(n_bands):
        print(f"  {k:>4}  {t_mids[k]:>8.1f}  {act_var[k]:>10.6f}  {gue_var[k]:>10.6f}  "
              f"{ratio_per_band[k]:>8.4f}  {rc9[k]:>10.4f}")

    all_band_results[f'{n_bands}band'] = {
        't_mids': t_mids,
        'act_var': act_var,
        'gue_var': gue_var,
        'ratio_per_band': ratio_per_band,
        'steps': step_results,
        'signal_primes': signal_primes,
    }

# -- Save results -------------------------------------------------------------
out = os.path.join(script_dir, 'p13c_results.json')
with open(out, 'w') as f:
    json.dump({
        'phase': '13C',
        'question': 'Does Act/GUE P2 variance ratio per band correlate with BK R_c?',
        'gue_seeds': GUE_SEEDS,
        'prime_steps': PRIME_STEPS,
        'thresholds': THRESHOLD,
        'results': all_band_results,
    }, f, indent=2)

print(f"\nResults saved to p13c_results.json")
