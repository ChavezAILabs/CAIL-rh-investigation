"""
RH Phase 13D -- Per-Band DFT SNR vs Berry-Keating R_c(t)
=========================================================
Question: Does the within-band DFT power at log-prime frequencies correlate
with the BK prime orbit correction R_c(t_mid) per height band?

Motivation:
  Phase 13A: Global DFT shows SNR 7-245x at log-prime frequencies (8/9 primes).
             Signal is ordering-dependent (shuffling destroys it).
  Phase 13B/C: Band-level Pearson r fails when using ordering-blind statistics
               (mean spacing ratio, P2 variance ratio).
  Insight: The DFT within a band PRESERVES ordering, unlike mean/variance.
           Per-band DFT SNR is the right ordering-sensitive, band-level statistic.

Hypothesis: If BK is the source of the Phase 13A signal, the within-band DFT
SNR at log-prime frequencies should oscillate with R_c(t_mid). Bands where
R_c constructively reinforces the prime-orbit phase at frequency log(p) should
show higher per-band DFT power than bands in destructive phase.

Method:
  1. Split 9,998 spacing ratios into N_bands height bands
  2. Within each band k: compute DFT power at omega=log(p) for actual and GUE (3 seeds)
     P(omega, band_k) = |(1/N_b) * sum_j (r_j - mu_k) * exp(-i*omega*t_j)|^2
     Heights t_j are ABSOLUTE (not renormalized) -- BK phase is absolute
  3. Per-band SNR_k(p) = P_actual(omega, band_k) / P_GUE_mean(omega, band_k)
  4. Pearson r between SNR_k and R_c(t_mid_k) for each prime p
  5. Test primes with strongest Phase 13A signal: p=5,7,11,13,17,19,23
  6. Run at both 10-band and 20-band resolution

Significance thresholds:
  n=10 bands: |r| > 0.632
  n=20 bands: |r| > 0.444

Key distinction from 13B/C:
  13B used mean(r_k within band) -- ordering-blind, loses phase information
  13C used var(P2_k within band) -- height-confounded, loses BK oscillation
  13D uses DFT(r_k, omega=log p) -- ordering-sensitive, frequency-targeted
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

N_ZEROS = len(zeros)

# -- Spacing ratios -----------------------------------------------------------
def spacing_ratios(gaps):
    return [min(gaps[i], gaps[i+1]) / max(gaps[i], gaps[i+1])
            for i in range(len(gaps)-1)]

# -- DFT power at single frequency, using absolute heights --------------------
def dft_power(ratios, heights, omega):
    """P(omega) = |(1/N)*sum_k (r_k - mu)*exp(-i*omega*t_k)|^2"""
    if len(ratios) < 2:
        return 0.0
    mu = sum(ratios) / len(ratios)
    re = sum((r - mu) * math.cos(omega * t) for r, t in zip(ratios, heights))
    im = sum((r - mu) * math.sin(omega * t) for r, t in zip(ratios, heights))
    n  = len(ratios)
    return (re/n)**2 + (im/n)**2

# -- GUE sampler (Rayleigh / Wigner surmise) ----------------------------------
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
        (1.0/math.sqrt(p)) * math.cos(math.log(p)*t)
        + (1.0/p) * math.cos(2.0*math.log(p)*t)
        for p in primes
    )

# -- Pearson r ----------------------------------------------------------------
def pearson_r(x, y):
    n  = len(x)
    if n < 3: return 0.0
    mx = sum(x)/n
    my = sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx  = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy  = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    if dx == 0 or dy == 0: return 0.0
    return num / (dx*dy)

# -- Test configuration -------------------------------------------------------
# Primes with strongest Phase 13A signal (SNR > 50x)
SIGNAL_PRIMES = [5, 7, 11, 13, 17, 19, 23]
PRIME_OMEGAS  = {p: math.log(p) for p in SIGNAL_PRIMES}

# BK prime set for R_c
BK_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

GUE_SEEDS    = [1, 2, 3]
THRESHOLDS   = {10: 0.6319, 20: 0.4438}

print("="*72)
print("PHASE 13D -- PER-BAND DFT SNR vs BK R_c(t)")
print("="*72)
print(f"Signal primes tested: {SIGNAL_PRIMES}")
print(f"BK primes for R_c:    {BK_PRIMES}")
print(f"GUE seeds: {GUE_SEEDS}")

all_results = {}

for n_bands in [10, 20]:
    band_size = N_ZEROS // n_bands
    thresh    = THRESHOLDS[n_bands]

    print(f"\n{'='*65}")
    print(f"  {n_bands}-BAND ANALYSIS  (threshold |r| > {thresh:.4f}, "
          f"band_size={band_size} zeros)")
    print(f"{'='*65}")

    # Build bands
    bands = []
    for k in range(n_bands):
        start    = k * band_size
        end      = start + band_size
        bz       = zeros[start:end]
        bg       = gaps_all[start:end-1]
        bsr      = spacing_ratios(bg)
        # Heights for spacing ratios: z[n+1] for each ratio pair
        # ratio[i] uses gaps[i] and gaps[i+1], associated with zero index start+i+1
        bh       = [zeros[start + i + 1] for i in range(len(bsr))]
        mean_gap = sum(bg) / len(bg)
        bands.append({
            'k': k, 'start': start, 'end': end,
            't_lo': bz[0], 't_hi': bz[-1],
            't_mid': (bz[0]+bz[-1])/2.0,
            'gaps': bg, 'ratios': bsr, 'heights': bh,
            'mean_gap': mean_gap,
            'n_ratios': len(bsr),
        })

    t_mids  = [b['t_mid'] for b in bands]
    rc9_vec = [rc_value(t, BK_PRIMES) for t in t_mids]

    # -- Per-band DFT power: actual vs GUE ------------------------------------
    print(f"\nComputing per-band DFT power...")

    # Actual
    act_dft = {p: [] for p in SIGNAL_PRIMES}
    for b in bands:
        for p in SIGNAL_PRIMES:
            act_dft[p].append(dft_power(b['ratios'], b['heights'], PRIME_OMEGAS[p]))

    # GUE (3 seeds, averaged)
    gue_dft_seeds = {p: {s: [] for s in GUE_SEEDS} for p in SIGNAL_PRIMES}
    for seed in GUE_SEEDS:
        for b in bands:
            gue_gaps = sample_wigner(len(b['gaps']), b['mean_gap'], seed*1000 + b['k'])
            gue_sr   = spacing_ratios(gue_gaps)
            for p in SIGNAL_PRIMES:
                gue_dft_seeds[p][seed].append(
                    dft_power(gue_sr, b['heights'], PRIME_OMEGAS[p]))

    gue_dft = {p: [
        sum(gue_dft_seeds[p][s][k] for s in GUE_SEEDS) / len(GUE_SEEDS)
        for k in range(n_bands)
    ] for p in SIGNAL_PRIMES}

    # Per-band SNR
    snr_band = {p: [] for p in SIGNAL_PRIMES}
    for p in SIGNAL_PRIMES:
        for k in range(n_bands):
            gue_pw = gue_dft[p][k]
            snr_band[p].append(act_dft[p][k] / gue_pw if gue_pw > 0 else 0.0)

    # -- Pearson r: SNR vs R_c ------------------------------------------------
    print(f"\n  r(SNR_band, R_c) per prime (9-prime R_c):")
    print(f"  {'Prime':>7}  {'log(p)':>7}  {'r':>8}  {'|r|>thr?':>10}  "
          f"{'mean SNR':>10}  {'min SNR':>9}  {'max SNR':>9}")
    print(f"  {'-'*65}")

    prime_r_results = {}
    signal_found = []
    for p in SIGNAL_PRIMES:
        r   = pearson_r(rc9_vec, snr_band[p])
        sig = abs(r) > thresh
        mn  = sum(snr_band[p]) / n_bands
        lo  = min(snr_band[p])
        hi  = max(snr_band[p])
        if sig: signal_found.append(p)
        print(f"  {p:>7}  {math.log(p):>7.4f}  {r:>8.4f}  "
              f"{'YES ***' if sig else 'no':>10}  {mn:>10.3f}  {lo:>9.3f}  {hi:>9.3f}")
        prime_r_results[p] = {'r': r, 'significant': sig,
                              'mean_snr': mn, 'min_snr': lo, 'max_snr': hi,
                              'snr_per_band': snr_band[p]}

    print(f"\n  Signal primes: {signal_found if signal_found else 'None'}")

    # -- Also test each individual prime's R_c contribution -------------------
    print(f"\n  r(SNR_p, R_c_p) -- using R_c from p only (single-prime R_c):")
    print(f"  {'Prime':>7}  {'r(SNR_p, Rc_p)':>16}  {'r(SNR_p, Rc9)':>15}")
    print(f"  {'-'*42}")
    for p in SIGNAL_PRIMES:
        rc_p_vec = [rc_value(t, [p]) for t in t_mids]
        r_self   = pearson_r(rc_p_vec, snr_band[p])
        r_full   = prime_r_results[p]['r']
        print(f"  {p:>7}  {r_self:>16.4f}  {r_full:>15.4f}")

    # -- Band detail table for strongest prime (p=13) -------------------------
    best_p = max(SIGNAL_PRIMES, key=lambda p: abs(prime_r_results[p]['r']))
    print(f"\n  Band detail for p={best_p} (highest |r|={abs(prime_r_results[best_p]['r']):.4f}):")
    print(f"  {'Band':>5}  {'t_mid':>8}  {'act_dft':>12}  {'gue_dft':>12}  "
          f"{'SNR':>8}  {'R_c(9p)':>10}")
    for k in range(n_bands):
        print(f"  {k:>5}  {t_mids[k]:>8.1f}  {act_dft[best_p][k]:>12.4e}  "
              f"{gue_dft[best_p][k]:>12.4e}  {snr_band[best_p][k]:>8.3f}  "
              f"{rc9_vec[k]:>10.4f}")

    all_results[f'{n_bands}band'] = {
        't_mids': t_mids,
        'rc9_vector': rc9_vec,
        'prime_results': {
            str(p): {
                'r_vs_rc9': prime_r_results[p]['r'],
                'significant': prime_r_results[p]['significant'],
                'mean_snr': prime_r_results[p]['mean_snr'],
                'snr_per_band': prime_r_results[p]['snr_per_band'],
                'act_dft_per_band': act_dft[p],
                'gue_dft_per_band': gue_dft[p],
            }
            for p in SIGNAL_PRIMES
        },
        'signal_primes': signal_found,
        'threshold': thresh,
    }

# -- Global comparison: total SNR vs band SNR --------------------------------
print(f"\n{'='*72}")
print("COMPARISON: GLOBAL (Phase 13A) vs PER-BAND SNR")
print("="*72)
print(f"{'Prime':>7}  {'Global SNR (13A)':>18}  {'Per-band mean SNR (10b)':>24}  "
      f"{'Per-band mean SNR (20b)':>24}")
phase13a_snr = {5: 76.1, 7: 139.7, 11: 231.2, 13: 245.4, 17: 205.9, 19: 211.5, 23: 185.1}
for p in SIGNAL_PRIMES:
    g_snr  = phase13a_snr.get(p, '--')
    b10    = all_results['10band']['prime_results'][str(p)]['mean_snr']
    b20    = all_results['20band']['prime_results'][str(p)]['mean_snr']
    print(f"{p:>7}  {g_snr:>18}  {b10:>24.3f}  {b20:>24.3f}")

# -- Save results -------------------------------------------------------------
out = os.path.join(script_dir, 'p13d_results.json')
with open(out, 'w') as f:
    json.dump({
        'phase': '13D',
        'question': 'Does per-band DFT SNR at log-prime frequencies correlate with R_c?',
        'signal_primes_tested': SIGNAL_PRIMES,
        'bk_primes': BK_PRIMES,
        'gue_seeds': GUE_SEEDS,
        'thresholds': THRESHOLDS,
        'phase13a_global_snr': phase13a_snr,
        'results': all_results,
    }, f, indent=2)

print(f"\nResults saved to p13d_results.json")
