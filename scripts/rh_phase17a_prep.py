"""
RH Phase 17A — Q-Vector Projection Spectral Survey (zeta zeros)
=============================================================
Access Q-vector information by projecting embed_pair output onto the 8D
images of the Canonical Six Q-vectors.

Background (Phases 14B, 15C, 15D):
- embed_pair + P-vector projection detects log-prime DFT signal (SNR 7–245x)
- Framework-independence lives in Q-vector; all prior phases only accessed P-vectors
- Route B confirmed (Phase 16): signal is arithmetic, encodes Euler product

Q-vector 8D images (16D sedenion -> 8D via sign rule: e_{8+k} -> pos k, sign -1):

  Pattern 1: Q1 = e3+e12   -> q1 = (0, 0, 0,+1,-1, 0, 0, 0) = v2  [P2, already tested]
  Pattern 2: Q2 = e5+e10   -> q2 = (0, 0,-1, 0, 0,+1, 0, 0)        [NEW]
  Pattern 3: Q3 = e6+e9    -> q3 = (0,-1, 0, 0, 0, 0,+1, 0) = -v1  [DFT power = v1]
  Pattern 4: Q4 = e3-e12   -> q4 = (0, 0, 0,+1,+1, 0, 0, 0)        [NEW]
  Pattern 5: Q5 = e5+e10   -> q2  (same as Pattern 2)
  Pattern 6: Q6 = e6+e9    -> q3  (same as Pattern 3)

Algebraic relationships (closed form):
  q4 * embed_pair(g1,g2) = g1*g2/(g1+g2) + (g1+g2)/2 = H/2 + A  [always >= 0]
  q2 * embed_pair(g1,g2) = g2 - g1 + g1/(g1+g2)                  [asymmetric]
  Note: P2 proj = H/2 - A (always <= 0); q4 + P2 = H (harmonic mean)
  q4 and P2 are complementary: they sum to the harmonic mean of the gap pair.

Three sub-experiments:
  17A-i:  q2 DFT at log-prime freqs — compare to P-vector results
  17A-ii: q4 DFT at log-prime freqs — compare to P-vector results
  17A-iii: q3 = -v1 isometry verification (analytic theorem, should be exact)

Data: rh_zeros_10k.json, rh_gaps_10k.json (10,000 zeros)
Reference (Phase 14B): P2 detected p=3,5,7,11,13,17,19,23 (8/9 primes, SNR 4–1585)
Reference (Phase 15D): All 5 P-vectors detect 8–9/9 primes
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

mean_gap = sum(gaps_all) / len(gaps_all)
N_ZEROS  = len(zeros)
print(f"Loaded {N_ZEROS} zeros, {len(gaps_all)} gaps. Mean gap: {mean_gap:.4f}")

# -- Canonical 8D direction vectors -------------------------------------------
# Q-vectors for Phase 17 (the two genuinely new directions are q2 and q4)
Q2 = (0, 0, -1, 0, 0,  1, 0, 0)   # Q2=Q5: e5+e10 — NEW
Q3 = (0, -1,  0, 0, 0,  0, 1, 0)  # Q3=Q6: e6+e9 = -v1  [isometry test]
Q4 = (0, 0,  0, 1, 1,  0, 0, 0)   # Q4: e3-e12  — NEW

# P-vectors (for comparison column in output)
V1 = (0,  1,  0,  0,  0,  0, -1, 0)
V2 = (0,  0,  0,  1, -1,  0,  0, 0)
V3 = (0,  0,  0, -1,  1,  0,  0, 0)
V4 = (0,  1,  0,  0,  0,  0,  1, 0)
V5 = (0,  0,  1,  0,  0,  1,  0, 0)

# -- embed_pair and projection -------------------------------------------------
def embed_pair(g1, g2):
    s = g1 + g2
    return (g1, g2, g1-g2, g1*g2/s, (g1+g2)/2, g1/s, g2/s, (g1-g2)**2/s)

def proj_vec(g1, g2, v):
    ep = embed_pair(g1, g2)
    return sum(ep[i]*v[i] for i in range(8))

def build_sequence(gaps, vec):
    return [proj_vec(gaps[i], gaps[i+1], vec) for i in range(len(gaps)-1)]

# -- DFT power at single angular frequency ------------------------------------
def dft_power(seq, heights, omega):
    mu = sum(seq) / len(seq)
    n  = len(seq)
    re = sum((x - mu) * math.cos(omega * t) for x, t in zip(seq, heights)) / n
    im = sum((x - mu) * math.sin(omega * t) for x, t in zip(seq, heights)) / n
    return re**2 + im**2

# -- Samplers -----------------------------------------------------------------
def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    out = []
    while len(out) < n:
        u = rng.random()
        if u > 0:
            out.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return out

def sample_poisson(n, mean, seed):
    rng = random.Random(seed)
    return [-mean * math.log(rng.random() or 1e-300) for _ in range(n)]

def shuffle_seq(seq, seed):
    rng = random.Random(seed); s = seq[:]; rng.shuffle(s); return s

def avg_snr(seq_fn, omegas, ctrl_omegas, heights, seeds):
    """Compute mean SNR dict over multiple seeds for a given sequence factory."""
    powers = {om: 0.0 for om in omegas}
    noise  = 0.0
    for seed in seeds:
        seq = seq_fn(seed)
        for om in omegas:
            powers[om] += dft_power(seq, heights, om)
        noise += sum(dft_power(seq, heights, om) for om in ctrl_omegas) / len(ctrl_omegas)
    nf = noise / len(seeds)
    return {om: powers[om] / len(seeds) / (nf if nf > 0 else 1) for om in omegas}, nf

# -- Frequency grid -----------------------------------------------------------
PRIMES       = [2, 3, 5, 7, 11, 13, 17, 19, 23]
prime_omegas = {p: math.log(p) for p in PRIMES}
log_vals     = sorted(prime_omegas.values())
ctrl_omegas  = [(log_vals[i]+log_vals[i+1])/2 for i in range(len(log_vals)-1)]
all_omegas   = list(prime_omegas.values()) + ctrl_omegas
SEEDS        = [1, 2, 3]

# Heights for DFT (associate each gap pair with the height of the central zero)
heights_pairs = [zeros[i+1] for i in range(len(gaps_all)-1)]

# -- Phase 17A-i : q2 projection DFT -----------------------------------------
print(f"\n{'='*70}")
print("17A-i: Q2 projection DFT  |  q2 = (0,0,-1,0,0,+1,0,0)  [Q2=Q5: e5+e10]")
print(f"{'='*70}")

q2_actual = build_sequence(gaps_all, Q2)
mu_q2     = sum(q2_actual) / len(q2_actual)
print(f"  n={len(q2_actual)}, mean={mu_q2:.6f}, range=[{min(q2_actual):.4f}, {max(q2_actual):.4f}]")
print(f"  [Compare P2 mean~-0.322; q4 = H/2+A (always >= 0)]")

noise_q2_actual = sum(dft_power(q2_actual, heights_pairs, om) for om in ctrl_omegas) / len(ctrl_omegas)

def gue_q2(seed):
    g = sample_wigner(len(gaps_all), mean_gap, seed)
    return build_sequence(g, Q2)
def poi_q2(seed):
    g = sample_poisson(len(gaps_all), mean_gap, seed)
    return build_sequence(g, Q2)
def shuf_q2(seed):
    return shuffle_seq(q2_actual, seed)

snr_q2_gue,  nf_gue_q2  = avg_snr(gue_q2,  all_omegas, ctrl_omegas, heights_pairs, SEEDS)
snr_q2_poi,  nf_poi_q2  = avg_snr(poi_q2,  all_omegas, ctrl_omegas, heights_pairs, SEEDS)
snr_q2_shuf, nf_shuf_q2 = avg_snr(shuf_q2, all_omegas, ctrl_omegas, heights_pairs, SEEDS)

# P14B reference P2 SNRs for comparison
p2_ref = {2: 0.84, 3: 7.6, 5: 76.1, 7: 139.7, 11: 231.2, 13: 245.4, 17: 205.9, 19: 211.5, 23: 185.1}

print(f"\n{'Prime':>6}  {'log(p)':>7}  {'Act SNR':>9}  {'GUE SNR':>9}  "
      f"{'Poi SNR':>9}  {'Shuf SNR':>9}  {'P2 SNR(14B)':>12}  Signal?")
print("-"*80)
sig_q2 = []
snr_q2_results = {}
for p in PRIMES:
    om = prime_omegas[p]
    snr_a = dft_power(q2_actual, heights_pairs, om) / (noise_q2_actual or 1)
    snr_g = snr_q2_gue[om]
    snr_p = snr_q2_poi[om]
    snr_s = snr_q2_shuf[om]
    sig = snr_a > 2.0 and snr_a > 1.5 * max(snr_g, snr_p, snr_s)
    if sig: sig_q2.append(p)
    print(f"{p:>6}  {om:>7.4f}  {snr_a:>9.3f}  {snr_g:>9.3f}  "
          f"{snr_p:>9.3f}  {snr_s:>9.3f}  {str(p2_ref.get(p,'--')):>12}  {'YES' if sig else ''}")
    snr_q2_results[p] = dict(act=snr_a, gue=snr_g, poi=snr_p, shuf=snr_s, signal=sig)
print(f"Q2 signal primes: {sig_q2 if sig_q2 else 'None'}")

# -- Phase 17A-ii : q4 projection DFT -----------------------------------------
print(f"\n{'='*70}")
print("17A-ii: Q4 projection DFT  |  q4 = (0,0,0,+1,+1,0,0,0)  [Q4: e3-e12]")
print(f"{'='*70}")

q4_actual = build_sequence(gaps_all, Q4)
mu_q4     = sum(q4_actual) / len(q4_actual)
print(f"  n={len(q4_actual)}, mean={mu_q4:.6f}, range=[{min(q4_actual):.4f}, {max(q4_actual):.4f}]")
print(f"  q4 = H/2 + A (harmonic/2 + arithmetic mean); P2 = H/2 - A; q4 + P2 = H")

noise_q4_actual = sum(dft_power(q4_actual, heights_pairs, om) for om in ctrl_omegas) / len(ctrl_omegas)

def gue_q4(seed):
    g = sample_wigner(len(gaps_all), mean_gap, seed)
    return build_sequence(g, Q4)
def poi_q4(seed):
    g = sample_poisson(len(gaps_all), mean_gap, seed)
    return build_sequence(g, Q4)
def shuf_q4(seed):
    return shuffle_seq(q4_actual, seed)

snr_q4_gue,  _ = avg_snr(gue_q4,  all_omegas, ctrl_omegas, heights_pairs, SEEDS)
snr_q4_poi,  _ = avg_snr(poi_q4,  all_omegas, ctrl_omegas, heights_pairs, SEEDS)
snr_q4_shuf, _ = avg_snr(shuf_q4, all_omegas, ctrl_omegas, heights_pairs, SEEDS)

print(f"\n{'Prime':>6}  {'log(p)':>7}  {'Act SNR':>9}  {'GUE SNR':>9}  "
      f"{'Poi SNR':>9}  {'Shuf SNR':>9}  {'P2 SNR(14B)':>12}  Signal?")
print("-"*80)
sig_q4 = []
snr_q4_results = {}
for p in PRIMES:
    om = prime_omegas[p]
    snr_a = dft_power(q4_actual, heights_pairs, om) / (noise_q4_actual or 1)
    snr_g = snr_q4_gue[om]
    snr_p = snr_q4_poi[om]
    snr_s = snr_q4_shuf[om]
    sig = snr_a > 2.0 and snr_a > 1.5 * max(snr_g, snr_p, snr_s)
    if sig: sig_q4.append(p)
    print(f"{p:>6}  {om:>7.4f}  {snr_a:>9.3f}  {snr_g:>9.3f}  "
          f"{snr_p:>9.3f}  {snr_s:>9.3f}  {str(p2_ref.get(p,'--')):>12}  {'YES' if sig else ''}")
    snr_q4_results[p] = dict(act=snr_a, gue=snr_g, poi=snr_p, shuf=snr_s, signal=sig)
print(f"Q4 signal primes: {sig_q4 if sig_q4 else 'None'}")

# -- Phase 17A-iii : q3 = -v1 isometry verification --------------------------
print(f"\n{'='*70}")
print("17A-iii: q3 = -v1 isometry  |  Theorem: q3=-v1 -> |DFT(q3)|2=|DFT(v1)|2")
print(f"{'='*70}")

q3_actual = build_sequence(gaps_all, Q3)
v1_actual = build_sequence(gaps_all, V1)

max_dev = 0.0
print(f"\n{'Prime':>6}  {'q3 power':>14}  {'v1 power':>14}  {'ratio q3/v1':>12}  Equal?")
print("-"*55)
for p in PRIMES:
    om   = prime_omegas[p]
    pw_q3 = dft_power(q3_actual, heights_pairs, om)
    pw_v1 = dft_power(v1_actual, heights_pairs, om)
    ratio = pw_q3 / pw_v1 if pw_v1 > 0 else float('inf')
    dev   = abs(ratio - 1.0)
    max_dev = max(max_dev, dev)
    print(f"{p:>6}  {pw_q3:>14.6e}  {pw_v1:>14.6e}  {ratio:>12.10f}  {'YES' if dev < 1e-10 else 'NO'}")
print(f"\nMax deviation from exact equality: {max_dev:.2e}")
print(f"Theorem confirmed: {'YES (as expected — q3=-v1 forces equal power)' if max_dev < 1e-8 else 'NO — unexpected'}")

# -- Save results -------------------------------------------------------------
results = {
    "phase": "17A",
    "question": "Do Q-vector projections detect log-prime signal? Do new Q-directions (q2, q4) carry arithmetic information?",
    "dataset": "10k zeta zeros",
    "n_pairs": len(q2_actual),
    "mean_gap": mean_gap,
    "primes_tested": PRIMES,
    "prime_omegas": {str(p): math.log(p) for p in PRIMES},
    "q2_vector": list(Q2),
    "q4_vector": list(Q4),
    "q3_isometry_theorem": "q3 = -v1 => |DFT(q3)|^2 = |DFT(v1)|^2 for any sequence",
    "q_vector_algebra": {
        "q1": "= v2 (Q1=P2 in 16D; already tested as P2 in Phase 14B)",
        "q2": "e5+e10 (Q2=Q5); proj = g2-g1+g1/(g1+g2) [asymmetric, NEW]",
        "q3": "e6+e9 (Q3=Q6) = -v1; DFT power = v1 by isometry theorem",
        "q4": "e3-e12 (Q4); proj = g1*g2/(g1+g2)+(g1+g2)/2 = H/2+A [NEW]; q4+P2=H"
    },
    "q2_stats": {
        "mean": sum(q2_actual)/len(q2_actual),
        "signal_primes": sig_q2,
        "noise_floor_actual": noise_q2_actual,
        "snr": {str(p): snr_q2_results[p] for p in PRIMES},
    },
    "q4_stats": {
        "mean": sum(q4_actual)/len(q4_actual),
        "signal_primes": sig_q4,
        "noise_floor_actual": noise_q4_actual,
        "snr": {str(p): snr_q4_results[p] for p in PRIMES},
    },
    "q3_isometry_check": {
        "max_deviation_from_1": max_dev,
        "confirmed": max_dev < 1e-8,
    },
    "p14b_p2_reference_snr": p2_ref,
    # For CAILculator: sequences of Q2 and Q4 projections (first 500 for analysis)
    "q2_sequence_500": q2_actual[:500],
    "q4_sequence_500": q4_actual[:500],
}

out = os.path.join(script_dir, 'p17a_results.json')
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to p17a_results.json")
print(f"\nSUMMARY:")
print(f"  Q2 signal primes: {sig_q2}")
print(f"  Q4 signal primes: {sig_q4}")
print(f"  q3 isometry confirmed: {max_dev < 1e-8}")
