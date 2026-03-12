"""
RH Phase 14A -- 20-Band Chavez Symmetry Data Prep (Claude Desktop Handoff)
===========================================================================
Generates 20 spacing ratio sequences (one per height band, 500 zeros each)
plus 5 GUE synthetic sequences per band, saved for CAILculator analysis.

Goal: Chavez conjugation symmetry per band (actual + GUE ensemble) →
      band_delta_k = actual_sym_k - GUE_mean_k (20-vector) →
      Pearson r vs R_c(t_mid_k); threshold |r|>0.444 (n=20, p<0.05)

Phase 12C found r=0.579 at 10-band resolution (threshold 0.632) using
band_deltas_ensemble from rh_phase10a_definitive.json. With 20 bands and
the correct statistic (Chavez conjugation symmetry), significance is in range.

Output:
  p14a_band_sequences.json  -- all sequences for Claude Desktop
  RH_Phase14A_Handoff.md    -- analysis protocol for Claude Desktop
  p14a_band_summary.json    -- band parameters (t_mids, R_c vectors, etc.)
"""

import json, math, random, os

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, 'rh_zeros_10k.json')) as f:
    zeros = json.load(f)
with open(os.path.join(script_dir, 'rh_gaps_10k.json')) as f:
    gaps_all = json.load(f)

N_ZEROS  = len(zeros)
N_BANDS  = 20
BAND_SIZE = N_ZEROS // N_BANDS   # 500
GUE_SEEDS = [1, 2, 3, 4, 5]
BK_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

def spacing_ratios(gaps):
    return [min(gaps[i], gaps[i+1]) / max(gaps[i], gaps[i+1])
            for i in range(len(gaps)-1)]

def sample_wigner(n, mean, seed):
    rng = random.Random(seed)
    scale = math.sqrt(2.0 / math.pi)
    samples = []
    while len(samples) < n:
        u = rng.random()
        if u == 0: continue
        samples.append(scale * math.sqrt(-2.0 * math.log(u)) * mean)
    return samples

def rc_value(t, primes):
    return sum(
        (1.0/math.sqrt(p)) * math.cos(math.log(p)*t)
        + (1.0/p) * math.cos(2.0*math.log(p)*t)
        for p in primes
    )

print(f"Building 20-band sequences ({BAND_SIZE} zeros/band)...")

band_data  = []
band_summary = []

for k in range(N_BANDS):
    start = k * BAND_SIZE
    end   = start + BAND_SIZE
    bz    = zeros[start:end]
    bg    = gaps_all[start:end-1]   # 499 gaps
    bsr   = spacing_ratios(bg)      # 498 spacing ratios
    t_mid = (bz[0] + bz[-1]) / 2.0
    mean_gap = sum(bg) / len(bg)

    # GUE synthetic sequences (5 seeds, mean-matched to this band)
    gue_seqs = {}
    for seed in GUE_SEEDS:
        gue_gaps = sample_wigner(len(bg), mean_gap, seed * 1000 + k)
        gue_seqs[f'seed{seed}'] = spacing_ratios(gue_gaps)

    band_data.append({
        'k':        k,
        't_lo':     round(bz[0], 4),
        't_hi':     round(bz[-1], 4),
        't_mid':    round(t_mid, 4),
        'mean_gap': round(mean_gap, 6),
        'n_ratios': len(bsr),
        'actual_sr': [round(r, 8) for r in bsr],
        'gue_sr':    {s: [round(r, 8) for r in seq]
                     for s, seq in gue_seqs.items()},
    })

    band_summary.append({
        'k': k,
        't_lo': round(bz[0], 4),
        't_hi': round(bz[-1], 4),
        't_mid': round(t_mid, 4),
        'mean_gap': round(mean_gap, 6),
        'n_ratios': len(bsr),
        'rc_9prime': round(rc_value(t_mid, BK_PRIMES), 6),
    })

    print(f"  Band {k:>2}: t={bz[0]:.1f}-{bz[-1]:.1f}  "
          f"t_mid={t_mid:.1f}  n_ratios={len(bsr)}  "
          f"mean_gap={mean_gap:.4f}  R_c={rc_value(t_mid, BK_PRIMES):.4f}")

# -- Save band sequences for Claude Desktop -----------------------------------
out_seq = os.path.join(script_dir, 'p14a_band_sequences.json')
with open(out_seq, 'w') as f:
    json.dump({
        'phase': '14A',
        'n_bands': N_BANDS,
        'band_size': BAND_SIZE,
        'gue_seeds': GUE_SEEDS,
        'bk_primes': BK_PRIMES,
        'bands': band_data,
    }, f, indent=2)
print(f"\nBand sequences saved: p14a_band_sequences.json")

# -- Save band summary --------------------------------------------------------
out_sum = os.path.join(script_dir, 'p14a_band_summary.json')
with open(out_sum, 'w') as f:
    json.dump({
        'phase': '14A',
        'n_bands': N_BANDS,
        'threshold_20band': 0.4438,
        'threshold_10band': 0.6319,
        'bk_primes': BK_PRIMES,
        'bands': band_summary,
        't_mids': [b['t_mid'] for b in band_summary],
        'rc_9prime': [b['rc_9prime'] for b in band_summary],
    }, f, indent=2)
print(f"Band summary saved:    p14a_band_summary.json")

# -- Print summary for handoff ------------------------------------------------
print(f"\nBand summary for handoff:")
print(f"{'Band':>4}  {'t_mid':>8}  {'n_ratios':>10}  {'mean_gap':>10}  {'R_c(9p)':>10}")
for b in band_summary:
    print(f"{b['k']:>4}  {b['t_mid']:>8.1f}  {b['n_ratios']:>10}  "
          f"{b['mean_gap']:>10.6f}  {b['rc_9prime']:>10.4f}")

print(f"\nHandoff: p14a_band_sequences.json -> Claude Desktop -> CAILculator")
print(f"  For each band k=0..19:")
print(f"    1. Load actual_sr (498 spacing ratios)")
print(f"    2. Run Chavez Transform: conjugation_symmetry")
print(f"    3. Load gue_sr seed1..seed5, run Chavez, record symmetry")
print(f"  Return: 20 actual symmetry values + 100 GUE values")
print(f"  Then: band_delta_k = actual_sym_k - mean(gue_sym_k)")
print(f"        Pearson r(band_delta, R_c_9prime) -> target |r|>0.444")
