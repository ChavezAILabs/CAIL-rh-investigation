"""
RH Phase 13B -- 20-Band Berry-Keating Pearson r Correlation
============================================================
Question: Does the exact BK prime orbit formula R_c(t) correlate significantly
with actual vs GUE spacing ratio deviations when using 20 bands (vs 10 in Phase 12C)?

Theory: With 20 bands, the Pearson r significance threshold drops from 0.632
to ~0.444 (n=20, p<0.05, two-tailed). Phase 12C peaked at r=0.5793 with 10 bands --
potentially significant at 20-band resolution.

Method:
  1. Split 10,000 zeros into 20 equal-count bands (500 zeros each)
  2. Compute spacing ratios and mean spacing ratio per band
  3. Generate GUE synthetic (5 seeds) mean-matched per band; compute GUE mean_sr
  4. band_delta_k = actual_mean_sr_k - GUE_mean_sr_k  (20-vector)
  5. Compute R_c(t_mid_k) for cumulative prime sets (exact BK formula)
  6. Pearson r between R_c and band_delta at each step
  7. Report r, compare to threshold; identify first crossing if any

Exact BK formula:
  R_c(t) = sum_p [ (1/sqrt(p)) * cos(log(p)*t) + (1/p) * cos(2*log(p)*t) ]

Significance threshold: |r| > 0.444 (p<0.05, two-tailed, n=20 bands)
Phase 12C threshold was 0.632 (n=10). With n=20 it drops substantially.

Data:
  rh_zeros_10k.json -- 10,000 zero heights
  rh_gaps_10k.json  -- 9,999 gaps
"""

import json, math, random, os
from itertools import accumulate

script_dir = os.path.dirname(os.path.abspath(__file__))

# -- Load data ----------------------------------------------------------------
with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)   # 10,000 heights

with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)   # 9,999 gaps

N_ZEROS = len(zeros)
N_BANDS = 20
BAND_SIZE = N_ZEROS // N_BANDS   # 500 zeros per band
print(f"Zeros: {N_ZEROS}  Bands: {N_BANDS}  Band size: {BAND_SIZE}")

# -- Band structure -----------------------------------------------------------
bands = []
for k in range(N_BANDS):
    start = k * BAND_SIZE
    end   = start + BAND_SIZE
    band_zeros = zeros[start:end]
    # gaps within this band (BAND_SIZE-1 gaps)
    band_gaps  = gaps_all[start:end-1]
    t_mid      = (band_zeros[0] + band_zeros[-1]) / 2.0
    mean_gap   = sum(band_gaps) / len(band_gaps)
    bands.append({
        'k':        k,
        'start':    start,
        'end':      end,
        't_lo':     band_zeros[0],
        't_hi':     band_zeros[-1],
        't_mid':    t_mid,
        'gaps':     band_gaps,
        'zeros':    band_zeros,
        'mean_gap': mean_gap,
    })

print(f"\nBand structure:")
print(f"  Band 0:  t = {bands[0]['t_lo']:.2f} to {bands[0]['t_hi']:.2f}  "
      f"(t_mid={bands[0]['t_mid']:.2f}, mean_gap={bands[0]['mean_gap']:.4f})")
print(f"  Band 9:  t = {bands[9]['t_lo']:.2f} to {bands[9]['t_hi']:.2f}  "
      f"(t_mid={bands[9]['t_mid']:.2f}, mean_gap={bands[9]['mean_gap']:.4f})")
print(f"  Band 19: t = {bands[19]['t_lo']:.2f} to {bands[19]['t_hi']:.2f}  "
      f"(t_mid={bands[19]['t_mid']:.2f}, mean_gap={bands[19]['mean_gap']:.4f})")

# -- Spacing ratios -----------------------------------------------------------
def spacing_ratios(gaps):
    return [min(gaps[i], gaps[i+1]) / max(gaps[i], gaps[i+1])
            for i in range(len(gaps)-1)]

def mean_sr(gaps):
    sr = spacing_ratios(gaps)
    return sum(sr) / len(sr) if sr else 0.0

# -- GUE synthetic sampler (Wigner/Rayleigh) ----------------------------------
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return samples

# -- Compute actual mean spacing ratio per band -------------------------------
actual_msr = []
for b in bands:
    actual_msr.append(mean_sr(b['gaps']))

print(f"\nActual mean spacing ratio range: {min(actual_msr):.4f} to {max(actual_msr):.4f}")

# -- Compute GUE ensemble mean spacing ratio per band (5 seeds) ---------------
GUE_SEEDS = [1, 2, 3, 4, 5]
gue_msr_by_seed = []
for seed in GUE_SEEDS:
    seed_msr = []
    for b in bands:
        gue_gaps = sample_wigner(len(b['gaps']), b['mean_gap'], seed * 100 + b['k'])
        seed_msr.append(mean_sr(gue_gaps))
    gue_msr_by_seed.append(seed_msr)

gue_msr_ensemble = [
    sum(gue_msr_by_seed[s][k] for s in range(len(GUE_SEEDS))) / len(GUE_SEEDS)
    for k in range(N_BANDS)
]

print(f"GUE ensemble mean spacing ratio range: {min(gue_msr_ensemble):.4f} to {max(gue_msr_ensemble):.4f}")

# -- Band deltas: actual - GUE_ensemble ---------------------------------------
band_deltas = [actual_msr[k] - gue_msr_ensemble[k] for k in range(N_BANDS)]
t_mids      = [b['t_mid'] for b in bands]

print(f"\nBand deltas (actual - GUE):")
print(f"  Range: {min(band_deltas):.4f} to {max(band_deltas):.4f}")
print(f"  Mean:  {sum(band_deltas)/N_BANDS:.4f}")

# -- Pearson r ----------------------------------------------------------------
def pearson_r(x, y):
    n  = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    num  = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx   = math.sqrt(sum((x[i] - mx)**2 for i in range(n)))
    dy   = math.sqrt(sum((y[i] - my)**2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)

# -- Exact BK R_c formula -----------------------------------------------------
def rc_value(t, primes):
    """R_c(t) = sum_p [(1/sqrt(p))*cos(log(p)*t) + (1/p)*cos(2*log(p)*t)]"""
    return sum(
        (1.0 / math.sqrt(p)) * math.cos(math.log(p) * t)
        + (1.0 / p) * math.cos(2.0 * math.log(p) * t)
        for p in primes
    )

def rc_vector(t_mids, primes):
    return [rc_value(t, primes) for t in t_mids]

# -- Step through prime sets --------------------------------------------------
PRIME_STEPS = [2, 3, 5, 7, 11, 13, 17, 19, 23]
THRESHOLD_20 = 0.4438   # Pearson r critical value: n=20, p<0.05, two-tailed
THRESHOLD_10 = 0.6319   # Phase 12C threshold for comparison

print(f"\nSignificance thresholds:")
print(f"  n=10 bands (Phase 12C): |r| > {THRESHOLD_10:.4f}")
print(f"  n=20 bands (Phase 13B): |r| > {THRESHOLD_20:.4f}")

print(f"\n{'='*70}")
print(f"PHASE 13B -- BK PEARSON r AT 20-BAND RESOLUTION")
print(f"{'='*70}")
print(f"\n{'Step':>6}  {'Primes':>30}  {'r':>8}  {'|r|>0.444?':>12}  {'Phase12C r':>12}")
print(f"{'-'*70}")

steps_results = []
prime_set = []
phase12c_r = {
    # From Phase 12C 10-band results for reference
    2:  0.4799, 3:  0.2261, 5:  0.3211, 7:  0.4037,
    11: 0.4844, 13: 0.4461, 17: 0.5195, 19: 0.5686,
    23: 0.5793
}

signal_primes = []
for i, p in enumerate(PRIME_STEPS):
    prime_set = PRIME_STEPS[:i+1]
    rc_vec    = rc_vector(t_mids, prime_set)
    r         = pearson_r(rc_vec, band_deltas)
    significant = abs(r) > THRESHOLD_20
    if significant and p not in signal_primes:
        signal_primes.append(p)
    p12c = phase12c_r.get(p, None)
    p12c_str = f"{p12c:.4f}" if p12c else "  --  "
    prime_str = str(prime_set)
    print(f"{i+1:>6}  {prime_str:>30}  {r:>8.4f}  "
          f"{'YES ***' if significant else 'no':>12}  {p12c_str:>12}")
    steps_results.append({
        'step': i+1,
        'primes': prime_set[:],
        'last_prime': p,
        'rc_vector': rc_vec,
        'r': r,
        'significant_20band': significant,
        'phase12c_r': p12c,
    })

print(f"\nPrimes achieving significance (|r|>{THRESHOLD_20:.4f}) at 20-band resolution:")
print(f"  {signal_primes if signal_primes else 'None'}")

# -- Extended prime search beyond p=23 ----------------------------------------
def next_primes(after_list, count):
    primes = list(after_list)
    candidate = primes[-1] + 2
    added = []
    while len(added) < count:
        is_prime = all(candidate % p != 0 for p in range(2, int(candidate**0.5)+1))
        if is_prime:
            added.append(candidate)
            primes.append(candidate)
        candidate += 2
    return added

print(f"\n--- Extension: p=29..53 ---")
print(f"{'Step':>6}  {'Last prime':>12}  {'r':>8}  {'|r|>0.444?':>12}")
print(f"{'-'*45}")
extension_primes = [29, 31, 37, 41, 43, 47, 53]
current_prime_set = PRIME_STEPS[:]
for p in extension_primes:
    current_prime_set.append(p)
    rc_vec = rc_vector(t_mids, current_prime_set)
    r      = pearson_r(rc_vec, band_deltas)
    significant = abs(r) > THRESHOLD_20
    if significant and p not in signal_primes:
        signal_primes.append(p)
    print(f"{len(current_prime_set):>6}  {p:>12}  {r:>8.4f}  {'YES ***' if significant else 'no':>12}")
    steps_results.append({
        'step': len(current_prime_set),
        'primes': current_prime_set[:],
        'last_prime': p,
        'rc_vector': rc_vector(t_mids, current_prime_set),
        'r': r,
        'significant_20band': significant,
        'phase12c_r': None,
    })

# -- Band detail table --------------------------------------------------------
print(f"\n--- Band detail table ---")
print(f"{'Band':>5}  {'t_mid':>8}  {'Act_msr':>9}  {'GUE_msr':>9}  {'Delta':>8}  "
      f"{'R_c(base)':>10}")
rc_base = rc_vector(t_mids, PRIME_STEPS)
for k in range(N_BANDS):
    print(f"{k:>5}  {t_mids[k]:>8.1f}  {actual_msr[k]:>9.5f}  "
          f"{gue_msr_ensemble[k]:>9.5f}  {band_deltas[k]:>8.5f}  "
          f"{rc_base[k]:>10.5f}")

# -- Save results -------------------------------------------------------------
results = {
    'phase': '13B',
    'question': 'Does 20-band resolution achieve BK significance vs 10-band Phase 12C?',
    'n_zeros': N_ZEROS,
    'n_bands': N_BANDS,
    'band_size': BAND_SIZE,
    'threshold_20band': THRESHOLD_20,
    'threshold_10band': THRESHOLD_10,
    'gue_seeds': GUE_SEEDS,
    't_mids': t_mids,
    'actual_msr': actual_msr,
    'gue_msr_ensemble': gue_msr_ensemble,
    'band_deltas': band_deltas,
    'prime_steps': [
        {
            'primes': s['primes'],
            'last_prime': s['last_prime'],
            'r': s['r'],
            'significant_20band': s['significant_20band'],
            'phase12c_r': s['phase12c_r'],
        }
        for s in steps_results
    ],
    'signal_primes': signal_primes,
    'phase12c_peak_r': 0.5793,
    'phase12c_peak_prime': 23,
}

out = os.path.join(script_dir, 'p13b_results.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to p13b_results.json")
