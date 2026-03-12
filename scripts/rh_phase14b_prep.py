"""
RH Phase 14B -- Antipodal Pair DFT Spectral Analysis
=====================================================
Applies the Phase 13A DFT methodology to the P2 projection sequence (the
antipodal embed_pair direction) and investigates the spectral isometry
between the antipodal pair P2/P3.

The Canonical Six antipodal pair:
  v2 = (0,0,0, 1,-1,0,0,0)  [Color Group 2]
  v3 = (0,0,0,-1, 1,0,0,0)  [Color Group 3] = -v2
  Connected by Weyl reflection alpha_4 (Lean 4 proven)

P2 projection of embed_pair(g1,g2):
  P2(g1,g2) = dot(embed_pair, v2)
             = g1*g2/(g1+g2) - (g1+g2)/2
             = -(g1^2 + g2^2) / (2*(g1+g2))   [always <= 0]

P3 projection = -P2 (the antipodal direction) [always >= 0]

Three sub-experiments:
  14B-i:  DFT at log-prime frequencies on P2 sequence -- compare to Phase 13A
  14B-ii: Verify antipodal spectral isometry: DFT_power(P3) = DFT_power(P2)
          analytically guaranteed since P3-mu3 = -(P2-mu2), so |DFT|^2 identical
  14B-iii: Per-band P2 skewness (20 bands) vs R_c -- phase-sensitive BK test

Data: rh_zeros_10k.json (10,000 zeros), rh_gaps_10k.json (9,999 gaps)
Phase 13A spacing ratio results for comparison:
  p=3: SNR=7.6, p=5: SNR=76, p=7: SNR=140, p=11: SNR=231, p=13: SNR=245
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

N_ZEROS = len(zeros)

# -- Projections --------------------------------------------------------------
def p2_proj(g1, g2):
    """P2 = -(g1^2+g2^2)/(2*(g1+g2)), always <= 0"""
    s = g1 + g2
    return -(g1**2 + g2**2) / (2.0 * s)

def p3_proj(g1, g2):
    """P3 = -P2, always >= 0"""
    return -p2_proj(g1, g2)

def p2_sequence(gaps):
    return [p2_proj(gaps[i], gaps[i+1]) for i in range(len(gaps)-1)]

def p3_sequence(gaps):
    return [-v for v in p2_sequence(gaps)]

# -- DFT power ----------------------------------------------------------------
def dft_power(seq, heights, omega):
    mu = sum(seq) / len(seq)
    re = sum((x - mu) * math.cos(omega * t) for x, t in zip(seq, heights))
    im = sum((x - mu) * math.sin(omega * t) for x, t in zip(seq, heights))
    n  = len(seq)
    return (re/n)**2 + (im/n)**2

# -- Samplers -----------------------------------------------------------------
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return samples

def sample_poisson(n, mean, seed):
    rng = random.Random(seed)
    return [-mean * math.log(rng.random() or 1e-300) for _ in range(n)]

def shuffle_seq(seq, seed):
    rng = random.Random(seed)
    s = seq[:]
    rng.shuffle(s)
    return s

# -- Pearson r ----------------------------------------------------------------
def pearson_r(x, y):
    n  = len(x)
    mx, my = sum(x)/n, sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx  = math.sqrt(sum((x[i]-mx)**2 for i in range(n)))
    dy  = math.sqrt(sum((y[i]-my)**2 for i in range(n)))
    return num/(dx*dy) if dx*dy else 0.0

def skewness(seq):
    n  = len(seq)
    mu = sum(seq)/n
    s  = math.sqrt(sum((x-mu)**2 for x in seq)/(n-1))
    if s == 0: return 0.0
    return sum(((x-mu)/s)**3 for x in seq) / n

# -- BK R_c -------------------------------------------------------------------
def rc_value(t, primes):
    return sum(
        (1.0/math.sqrt(p))*math.cos(math.log(p)*t)
        + (1.0/p)*math.cos(2.0*math.log(p)*t)
        for p in primes
    )

# -- Build global P2 sequence -------------------------------------------------
mean_gap = sum(gaps_all) / len(gaps_all)
p2_seq   = p2_sequence(gaps_all)    # 9,998 values
p3_seq   = p3_sequence(gaps_all)    # 9,998 values
heights  = [zeros[i+1] for i in range(len(p2_seq))]  # absolute heights

N        = len(p2_seq)
mean_p2  = sum(p2_seq) / N
mean_p3  = sum(p3_seq) / N

print(f"P2 sequence: n={N}")
print(f"  P2 range: {min(p2_seq):.4f} to {max(p2_seq):.4f}")
print(f"  P2 mean:  {mean_p2:.6f}")
print(f"  P3 range: {min(p3_seq):.4f} to {max(p3_seq):.4f}")
print(f"  P3 mean:  {mean_p3:.6f}  (should equal -P2 mean: {-mean_p2:.6f})")

PRIMES      = [2, 3, 5, 7, 11, 13, 17, 19, 23]
prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals    = sorted(prime_omegas.values())
ctrl_omegas = [(log_vals[i]+log_vals[i+1])/2 for i in range(len(log_vals)-1)]
BK_PRIMES   = [2, 3, 5, 7, 11, 13, 17, 19, 23]
SEEDS       = [1, 2, 3]

# ============================================================================
# 14B-i: DFT on P2 sequence at log-prime frequencies
# ============================================================================
print(f"\n{'='*70}")
print(f"14B-i: DFT at log-prime frequencies -- P2 sequence")
print(f"{'='*70}")

all_omegas = list(prime_omegas.values()) + ctrl_omegas

# Actual P2
prof_p2_actual = {om: dft_power(p2_seq, heights, om) for om in all_omegas}

# GUE controls (p2 of GUE gaps)
prof_p2_gue_list = []
for seed in SEEDS:
    gue_gaps = sample_wigner(len(gaps_all), mean_gap, seed)
    gue_p2   = p2_sequence(gue_gaps)
    prof_p2_gue_list.append({om: dft_power(gue_p2, heights, om) for om in all_omegas})
prof_p2_gue = {om: sum(d[om] for d in prof_p2_gue_list)/len(SEEDS) for om in all_omegas}

# Poisson controls
prof_p2_poi_list = []
for seed in SEEDS:
    poi_gaps = sample_poisson(len(gaps_all), mean_gap, seed)
    poi_p2   = p2_sequence(poi_gaps)
    prof_p2_poi_list.append({om: dft_power(poi_p2, heights, om) for om in all_omegas})
prof_p2_poi = {om: sum(d[om] for d in prof_p2_poi_list)/len(SEEDS) for om in all_omegas}

# Shuffled controls
prof_p2_shuf_list = []
for seed in SEEDS:
    shuf_p2 = shuffle_seq(p2_seq, seed)
    prof_p2_shuf_list.append({om: dft_power(shuf_p2, heights, om) for om in all_omegas})
prof_p2_shuf = {om: sum(d[om] for d in prof_p2_shuf_list)/len(SEEDS) for om in all_omegas}

# Noise floors
noise_p2_actual = sum(prof_p2_actual[om] for om in ctrl_omegas) / len(ctrl_omegas)
noise_p2_gue    = sum(prof_p2_gue[om]    for om in ctrl_omegas) / len(ctrl_omegas)
noise_p2_poi    = sum(prof_p2_poi[om]    for om in ctrl_omegas) / len(ctrl_omegas)
noise_p2_shuf   = sum(prof_p2_shuf[om]   for om in ctrl_omegas) / len(ctrl_omegas)

# Phase 13A spacing ratio SNR for comparison
sr_snr_13a = {2:0.84, 3:7.6, 5:76.1, 7:139.7, 11:231.2, 13:245.4,
              17:205.9, 19:211.5, 23:185.1}

print(f"\n{'Prime':>6}  {'log(p)':>7}  {'Act SNR':>9}  {'GUE SNR':>9}  "
      f"{'Poi SNR':>9}  {'Shuf SNR':>9}  {'SR SNR(13A)':>12}  Signal?")
print(f"{'-'*80}")

signal_primes_p2 = []
p2_snr_results   = {}
for p in PRIMES:
    om       = prime_omegas[p]
    snr_act  = prof_p2_actual[om] / noise_p2_actual if noise_p2_actual  > 0 else 0
    snr_gue  = prof_p2_gue[om]    / noise_p2_gue    if noise_p2_gue     > 0 else 0
    snr_poi  = prof_p2_poi[om]    / noise_p2_poi    if noise_p2_poi     > 0 else 0
    snr_shuf = prof_p2_shuf[om]   / noise_p2_shuf   if noise_p2_shuf    > 0 else 0
    signal   = snr_act > 2.0 and snr_act > 1.5 * max(snr_gue, snr_poi, snr_shuf)
    if signal: signal_primes_p2.append(p)
    sr_snr   = sr_snr_13a.get(p, '--')
    print(f"{p:>6}  {om:>7.4f}  {snr_act:>9.3f}  {snr_gue:>9.3f}  "
          f"{snr_poi:>9.3f}  {snr_shuf:>9.3f}  {str(sr_snr):>12}  "
          f"{'YES' if signal else ''}")
    p2_snr_results[p] = {'snr_act': snr_act, 'snr_gue': snr_gue,
                         'snr_poi': snr_poi, 'snr_shuf': snr_shuf,
                         'signal': signal}

print(f"\nNoise floors: actual={noise_p2_actual:.3e}  GUE={noise_p2_gue:.3e}  "
      f"Poi={noise_p2_poi:.3e}  Shuf={noise_p2_shuf:.3e}")
print(f"P2 signal primes: {signal_primes_p2 if signal_primes_p2 else 'None'}")

# ============================================================================
# 14B-ii: Antipodal spectral isometry verification
# ============================================================================
print(f"\n{'='*70}")
print(f"14B-ii: Antipodal spectral isometry -- P2 vs P3 DFT power")
print(f"{'='*70}")
print(f"Theorem: P3 = -P2, so (P3-mu3) = -(P2-mu2), thus |DFT(P3)|^2 = |DFT(P2)|^2")
print(f"\nNumerical verification at each log-prime omega:")
print(f"{'Prime':>6}  {'omega':>7}  {'P2 power':>14}  {'P3 power':>14}  "
      f"{'Ratio P3/P2':>12}  {'Equal?':>8}")
print(f"{'-'*65}")
max_deviation = 0.0
for p in PRIMES:
    om      = prime_omegas[p]
    pw_p2   = prof_p2_actual[om]
    pw_p3   = dft_power(p3_seq, heights, om)
    ratio   = pw_p3 / pw_p2 if pw_p2 > 0 else float('inf')
    dev     = abs(ratio - 1.0)
    max_deviation = max(max_deviation, dev)
    equal   = dev < 1e-10
    print(f"{p:>6}  {om:>7.4f}  {pw_p2:>14.6e}  {pw_p3:>14.6e}  "
          f"{ratio:>12.10f}  {'YES' if equal else 'NO (dev='+str(dev)[:8]+')'}")

print(f"\nMax deviation from exact equality: {max_deviation:.2e}")
print(f"Isometry confirmed: {'YES' if max_deviation < 1e-8 else 'NO'}")

# ============================================================================
# 14B-iii: Per-band P2 skewness vs R_c
# ============================================================================
print(f"\n{'='*70}")
print(f"14B-iii: Per-band P2 skewness (20 bands) vs R_c(t_mid)")
print(f"{'='*70}")

N_BANDS   = 20
BAND_SIZE = N_ZEROS // N_BANDS
thresh_20 = 0.4438

band_t_mids   = []
band_p2_skew  = []
band_gue_skew = []

for k in range(N_BANDS):
    start   = k * BAND_SIZE
    end     = start + BAND_SIZE
    bz      = zeros[start:end]
    bg      = gaps_all[start:end-1]
    bp2     = p2_sequence(bg)
    t_mid   = (bz[0]+bz[-1])/2.0
    mean_g  = sum(bg)/len(bg)
    band_t_mids.append(t_mid)
    band_p2_skew.append(skewness(bp2))
    # GUE skewness (3-seed ensemble)
    gue_skews = []
    for seed in SEEDS:
        gg = sample_wigner(len(bg), mean_g, seed*100+k)
        gue_skews.append(skewness(p2_sequence(gg)))
    band_gue_skew.append(sum(gue_skews)/len(gue_skews))

rc9_vec    = [rc_value(t, BK_PRIMES) for t in band_t_mids]
delta_skew = [band_p2_skew[k] - band_gue_skew[k] for k in range(N_BANDS)]
r_skew_rc  = pearson_r(rc9_vec, band_p2_skew)
r_delta_rc = pearson_r(rc9_vec, delta_skew)

print(f"\n{'Band':>4}  {'t_mid':>8}  {'P2 skew':>10}  {'GUE skew':>10}  "
      f"{'Delta':>8}  {'R_c(9p)':>10}")
print(f"{'-'*58}")
for k in range(N_BANDS):
    print(f"{k:>4}  {band_t_mids[k]:>8.1f}  {band_p2_skew[k]:>10.4f}  "
          f"{band_gue_skew[k]:>10.4f}  {delta_skew[k]:>8.4f}  {rc9_vec[k]:>10.4f}")

print(f"\nr(P2_skew, R_c):       {r_skew_rc:.4f}  "
      f"{'YES ***' if abs(r_skew_rc) > thresh_20 else 'no'} (threshold {thresh_20})")
print(f"r(skew_delta, R_c):    {r_delta_rc:.4f}  "
      f"{'YES ***' if abs(r_delta_rc) > thresh_20 else 'no'}")

# ============================================================================
# Save results
# ============================================================================
results = {
    'phase': '14B',
    'n_p2': N,
    'mean_gap': mean_gap,
    'primes_tested': PRIMES,
    '14Bi_p2_dft': {
        'signal_primes': signal_primes_p2,
        'noise_floor_actual': noise_p2_actual,
        'noise_floor_gue': noise_p2_gue,
        'snr': {str(p): p2_snr_results[p] for p in PRIMES},
        'phase13a_sr_snr': sr_snr_13a,
    },
    '14Bii_isometry': {
        'theorem': 'P3=-P2 => |DFT(P3)|^2 = |DFT(P2)|^2',
        'max_deviation': max_deviation,
        'isometry_confirmed': max_deviation < 1e-8,
    },
    '14Biii_skewness': {
        't_mids': band_t_mids,
        'p2_skew_per_band': band_p2_skew,
        'gue_skew_per_band': band_gue_skew,
        'delta_skew': delta_skew,
        'rc9_vector': rc9_vec,
        'r_p2skew_vs_rc': r_skew_rc,
        'r_delta_vs_rc': r_delta_rc,
        'threshold_20band': thresh_20,
        'significant': abs(r_skew_rc) > thresh_20 or abs(r_delta_rc) > thresh_20,
    },
}

out = os.path.join(script_dir, 'p14b_results.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to p14b_results.json")
