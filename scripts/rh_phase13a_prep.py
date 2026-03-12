"""
RH Phase 13A -- Log-Prime Spectral Analysis of Zero Spacing Ratios
===================================================================
Question: Do prime-log frequencies appear in the power spectrum of the
empirical zero spacing ratio sequence?

Theory: The Berry-Keating explicit formula guarantees oscillations at
angular frequencies omega = log(p) in the zero density. We test whether
these are detectable in the spacing ratio sequence r_n = min(g_n, g_{n+1})
/ max(g_n, g_{n+1}), which is scale-free and ordering-dependent.

Method: Compute DFT power at specific angular frequencies, including
exact log-prime values and interleaved control (non-prime) frequencies.
Compare actual zeros vs GUE, Poisson, and shuffled controls.

Key output:
  Signal-to-noise ratio (SNR) = P(log p) / mean_P(controls) per prime p
  If actual SNR >> controls SNR at log-prime frequencies: prime signal detected.

Data:
  rh_zeros_10k.json -- 10,000 zero heights (t values)
  rh_gaps_10k.json  -- 9,999 gaps

Spacing ratios: r_n = min(g_n, g_{n+1}) / max(g_n, g_{n+1})
  n = 0..9997 -> 9,998 ratios
  Height associated with r_n: zeros[n+1] (zero between the two gaps)
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── Load data ─────────────────────────────────────────────────────────────────
with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)   # 10,000 heights

with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)  # 9,999 gaps

# ── Compute spacing ratios ────────────────────────────────────────────────────
def spacing_ratios(gap_seq):
    return [min(gap_seq[i], gap_seq[i+1]) / max(gap_seq[i], gap_seq[i+1])
            for i in range(len(gap_seq)-1)]

ratios_actual = spacing_ratios(gaps_all)   # 9,998 values
heights       = [zeros[i+1] for i in range(len(ratios_actual))]  # z_1..z_{9998}
N             = len(ratios_actual)
mean_gap      = sum(gaps_all) / len(gaps_all)

print(f"Spacing ratios: n={N}")
print(f"Height range:   {heights[0]:.2f} to {heights[-1]:.2f}")
print(f"Mean gap:       {mean_gap:.4f}")
mean_ratio = sum(ratios_actual) / N
print(f"Mean ratio:     {mean_ratio:.4f}")

# ── DFT power at a single angular frequency ───────────────────────────────────
def dft_power(ratios, heights, omega):
    """
    P(omega) = |A(omega)|^2  where
    A(omega) = (1/N) * sum_k  (r_k - mean_r) * exp(-i*omega*t_k)
             = (1/N) * [sum cos(omega*t_k)*(r_k-mu)] - i*(1/N)*[sum sin(omega*t_k)*(r_k-mu)]
    Scale-free: only relative powers matter for comparison.
    """
    mu = sum(ratios) / len(ratios)
    re = sum((r - mu) * math.cos(omega * t) for r, t in zip(ratios, heights))
    im = sum((r - mu) * math.sin(omega * t) for r, t in zip(ratios, heights))
    n  = len(ratios)
    return (re/n)**2 + (im/n)**2

# ── Frequency grid ────────────────────────────────────────────────────────────
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
prime_omegas   = {p: math.log(p) for p in PRIMES}

# Control frequencies: midpoints between consecutive log-prime values
log_vals = sorted(prime_omegas.values())
control_omegas = [(log_vals[i] + log_vals[i+1]) / 2
                  for i in range(len(log_vals)-1)]   # 8 controls

# Full scan: omega = 0.1 to 4.0 in steps of 0.05  (for spectrum plot)
scan_omegas = [round(0.1 + k*0.05, 4) for k in range(79)]   # 79 points

print(f"\nPrime-log frequencies tested: {[round(v,3) for v in log_vals]}")
print(f"Control frequencies:          {[round(v,3) for v in control_omegas]}")

# ── Samplers ──────────────────────────────────────────────────────────────────
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

def shuffle_sequence(seq, seed):
    rng = random.Random(seed)
    s = seq[:]
    rng.shuffle(s)
    return s

# ── Compute power profiles ────────────────────────────────────────────────────
SEEDS = [1, 2, 3]

def power_profile(ratios, heights, omegas):
    """Return dict of {omega: power} for given frequency list."""
    return {om: dft_power(ratios, heights, om) for om in omegas}

def avg_dict(list_of_dicts):
    keys = list_of_dicts[0].keys()
    return {k: sum(d[k] for d in list_of_dicts) / len(list_of_dicts) for k in keys}

all_omegas = list(prime_omegas.values()) + control_omegas

print("\nComputing actual zero power profile...")
prof_actual = power_profile(ratios_actual, heights, all_omegas)

print("Computing GUE controls (3 seeds)...")
prof_gue_list = []
for seed in SEEDS:
    gaps_syn = sample_wigner(len(gaps_all), mean_gap, seed)
    ratios_syn = spacing_ratios(gaps_syn)
    prof_gue_list.append(power_profile(ratios_syn, heights, all_omegas))
prof_gue = avg_dict(prof_gue_list)

print("Computing Poisson controls (3 seeds)...")
prof_poi_list = []
for seed in SEEDS:
    gaps_syn = sample_poisson(len(gaps_all), mean_gap, seed)
    ratios_syn = spacing_ratios(gaps_syn)
    prof_poi_list.append(power_profile(ratios_syn, heights, all_omegas))
prof_poi = avg_dict(prof_poi_list)

print("Computing shuffled controls (3 seeds)...")
prof_shuf_list = []
for seed in SEEDS:
    ratios_shuf = shuffle_sequence(ratios_actual, seed)
    prof_shuf_list.append(power_profile(ratios_shuf, heights, all_omegas))
prof_shuf = avg_dict(prof_shuf_list)

# ── Full spectrum scan (actual only, for context) ─────────────────────────────
print("Computing full spectrum scan (actual, GUE, Poisson, shuffled)...")
scan_actual = power_profile(ratios_actual, heights, scan_omegas)
scan_gue    = avg_dict([power_profile(
    spacing_ratios(sample_wigner(len(gaps_all), mean_gap, s)), heights, scan_omegas)
    for s in SEEDS])
scan_poi    = avg_dict([power_profile(
    spacing_ratios(sample_poisson(len(gaps_all), mean_gap, s)), heights, scan_omegas)
    for s in SEEDS])
scan_shuf   = avg_dict([power_profile(
    shuffle_sequence(ratios_actual, s), heights, scan_omegas)
    for s in SEEDS])

# ── SNR computation ───────────────────────────────────────────────────────────
def snr(prof_prime, prof_control, prime_omegas_list, control_omegas_list):
    """SNR = P(log p) / mean_P(control freqs) for each prime."""
    noise_floor = sum(prof_control[om] for om in control_omegas_list) / len(control_omegas_list)
    if noise_floor == 0:
        return {om: 0 for om in prime_omegas_list}
    return {om: prof_prime[om] / noise_floor for om in prime_omegas_list}

# ── Print results ─────────────────────────────────────────────────────────────
print("\n" + "="*75)
print("PHASE 13A -- LOG-PRIME SPECTRAL ANALYSIS")
print("="*75)

print("\n--- Power at log-prime frequencies ---")
print(f"{'Prime':>6}  {'log(p)':>7}  {'Actual':>12}  {'GUE':>12}  "
      f"{'Poisson':>12}  {'Shuffled':>12}")
print("-"*70)
for p in PRIMES:
    om = prime_omegas[p]
    print(f"{p:>6}  {om:>7.4f}  {prof_actual[om]:>12.6e}  {prof_gue[om]:>12.6e}  "
          f"{prof_poi[om]:>12.6e}  {prof_shuf[om]:>12.6e}")

noise_actual = sum(prof_actual[om] for om in control_omegas) / len(control_omegas)
noise_gue    = sum(prof_gue[om]    for om in control_omegas) / len(control_omegas)
noise_poi    = sum(prof_poi[om]    for om in control_omegas) / len(control_omegas)
noise_shuf   = sum(prof_shuf[om]   for om in control_omegas) / len(control_omegas)

print(f"\nMean noise floor (control freqs):")
print(f"  Actual={noise_actual:.6e}  GUE={noise_gue:.6e}  "
      f"Poisson={noise_poi:.6e}  Shuffled={noise_shuf:.6e}")

print("\n--- SNR = P(log p) / noise_floor ---")
print(f"{'Prime':>6}  {'log(p)':>7}  {'Act SNR':>9}  {'GUE SNR':>9}  "
      f"{'Poi SNR':>9}  {'Shuf SNR':>9}  Signal?")
print("-"*70)
signal_primes = []
for p in PRIMES:
    om = prime_omegas[p]
    snr_act  = prof_actual[om] / noise_actual  if noise_actual  > 0 else 0
    snr_gue  = prof_gue[om]    / noise_gue     if noise_gue     > 0 else 0
    snr_poi  = prof_poi[om]    / noise_poi     if noise_poi     > 0 else 0
    snr_shuf = prof_shuf[om]   / noise_shuf    if noise_shuf    > 0 else 0
    # Signal: actual SNR substantially exceeds all controls
    signal = snr_act > 2.0 and snr_act > 1.5 * max(snr_gue, snr_poi, snr_shuf)
    if signal:
        signal_primes.append(p)
    flag = "YES" if signal else ""
    print(f"{p:>6}  {om:>7.4f}  {snr_act:>9.3f}  {snr_gue:>9.3f}  "
          f"{snr_poi:>9.3f}  {snr_shuf:>9.3f}  {flag}")

print(f"\nPrimes with detected signal: {signal_primes if signal_primes else 'None'}")

# ── Scan: find top peaks and check if they align with log-primes ──────────────
print("\n--- Top 10 peaks in actual spectrum scan (omega=0.1 to 4.0) ---")
sorted_scan = sorted(scan_actual.items(), key=lambda x: -x[1])
log_prime_set = {round(math.log(p), 3) for p in PRIMES}
print(f"{'Rank':>5}  {'omega':>7}  {'Power':>12}  {'log-prime?':>12}  "
      f"{'Nearest prime':>14}")
for rank, (om, pw) in enumerate(sorted_scan[:10], 1):
    nearest_p = min(PRIMES, key=lambda p: abs(math.log(p) - om))
    dist = abs(math.log(nearest_p) - om)
    is_prime_freq = dist < 0.08
    print(f"{rank:>5}  {om:>7.4f}  {pw:>12.6e}  "
          f"{'YES' if is_prime_freq else 'no':>12}  "
          f"p={nearest_p} (dist={dist:.3f})")

# ── Save results ──────────────────────────────────────────────────────────────
results = {
    "phase": "13A",
    "question": "Do log-prime frequencies appear in zero spacing ratio power spectrum?",
    "n_ratios": N,
    "height_range": [heights[0], heights[-1]],
    "mean_gap": mean_gap,
    "mean_ratio": mean_ratio,
    "primes_tested": PRIMES,
    "prime_omegas": {str(p): math.log(p) for p in PRIMES},
    "signal_primes_detected": signal_primes,
    "noise_floors": {
        "actual": noise_actual, "gue": noise_gue,
        "poisson": noise_poi, "shuffled": noise_shuf
    },
    "prime_power": {
        "actual":   {str(p): prof_actual[prime_omegas[p]] for p in PRIMES},
        "gue":      {str(p): prof_gue[prime_omegas[p]]    for p in PRIMES},
        "poisson":  {str(p): prof_poi[prime_omegas[p]]    for p in PRIMES},
        "shuffled": {str(p): prof_shuf[prime_omegas[p]]   for p in PRIMES},
    },
    "snr": {
        "actual":   {str(p): prof_actual[prime_omegas[p]]  / noise_actual  for p in PRIMES},
        "gue":      {str(p): prof_gue[prime_omegas[p]]     / noise_gue     for p in PRIMES},
        "poisson":  {str(p): prof_poi[prime_omegas[p]]     / noise_poi     for p in PRIMES},
        "shuffled": {str(p): prof_shuf[prime_omegas[p]]    / noise_shuf    for p in PRIMES},
    },
    "spectrum_scan": {
        "omegas":   scan_omegas,
        "actual":   [scan_actual[om] for om in scan_omegas],
        "gue":      [scan_gue[om]    for om in scan_omegas],
        "poisson":  [scan_poi[om]    for om in scan_omegas],
        "shuffled": [scan_shuf[om]   for om in scan_omegas],
    },
    "top_10_actual_peaks": sorted_scan[:10],
}

out = os.path.join(script_dir, 'p13a_results.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to p13a_results.json")
