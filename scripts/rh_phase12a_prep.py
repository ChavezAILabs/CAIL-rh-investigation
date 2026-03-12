"""
RH Phase 12A — Act/GUE Variance Asymptote Study
=================================================
Question: Does the Act/GUE P2 variance ratio plateau at ~0.75 (Phase 11A),
or does it continue drifting toward 1.0 as sample size grows?

Known data points:
  n=97  (Phase 10C) : Act/GUE mean ~ 0.651
  n=498 (Phase 11A) : Act/GUE mean ~ 0.756
  n=998 (Phase 11A) : Act/GUE mean ~ 0.756

This script extends to n=2000, 5000, 9998 using rh_gaps_10k.json.

IMPORTANT: Mean gap decreases as n grows (zeros get denser at higher heights).
GUE synthetic sequences are mean-matched to actual gaps at each scale.

Output:
  - p12a_results.json: variance ratios at all scales
  - p12a_actual_n{N}_P2.json: P2 projections for CAILculator (conjugation symmetry)
  - p12a_gue_s{S}_n{N}_P2.json: GUE P2 projections for CAILculator
"""

import json
import math
import os
import random

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── Load 10k gaps ─────────────────────────────────────────────────────────────
with open(os.path.join(script_dir, 'rh_gaps_10k.json'), 'r') as f:
    all_gaps_10k = json.load(f)

print(f"Loaded rh_gaps_10k.json: {len(all_gaps_10k)} gaps")

# ── Also load prior scale data for complete picture ───────────────────────────
with open(os.path.join(script_dir, 'rh_gaps.json'), 'r') as f:
    all_gaps_1k = json.load(f)

# ── P2 embed_pair projection ──────────────────────────────────────────────────
P2 = [0, 0, 0, 1, -1, 0, 0, 0]

def embed_pair(g1, g2):
    s = g1 + g2
    return [g1, g2, g1-g2, g1*g2/s, (g1+g2)/2.0, g1/s, g2/s, (g1-g2)**2/s]

def dot(v, w):
    return sum(a*b for a, b in zip(v, w))

def project_p2(gaps):
    return [dot(embed_pair(gaps[i], gaps[i+1]), P2) for i in range(len(gaps)-1)]

def variance(xs):
    n = len(xs)
    mu = sum(xs) / n
    return sum((x-mu)**2 for x in xs) / n

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

# ── Prior scale data (Phase 10C and 11A) ─────────────────────────────────────
# Hardcoded from Phase 10C / 11A results for the trend table
prior_data = [
    {"n_pairs": 97,  "act_gue_P1": 0.626, "act_gue_P2": 0.662,
     "act_gue_P4": 0.628, "act_gue_P5": 0.688, "mean": 0.651, "source": "Phase 10C"},
    {"n_pairs": 498, "act_gue_P1": 0.742, "act_gue_P2": 0.789,
     "act_gue_P4": 0.738, "act_gue_P5": 0.768, "mean": 0.759, "source": "Phase 11A"},
    {"n_pairs": 998, "act_gue_P1": 0.734, "act_gue_P2": 0.762,
     "act_gue_P4": 0.743, "act_gue_P5": 0.786, "mean": 0.756, "source": "Phase 11A"},
]

# ── Run new scales ────────────────────────────────────────────────────────────
SCALES      = [2000, 5000, 9998]
GUE_SEEDS   = [1, 2, 3, 4, 5]
new_results = []

print("\n" + "="*65)
print("PHASE 12A — Act/GUE P2 VARIANCE RATIO AT EXTENDED SCALE")
print("="*65)

for n_pairs in SCALES:
    # Use first (n_pairs+1) gaps → n_pairs consecutive pairs
    # Pull from 1k file if n_pairs < 999, else from 10k file
    if n_pairs <= 998:
        gaps = all_gaps_1k[:n_pairs+1]
    else:
        gaps = all_gaps_10k[:n_pairs+1]

    mean_gap = sum(gaps) / len(gaps)
    print(f"\nn_pairs={n_pairs}: using {len(gaps)} gaps, mean_gap={mean_gap:.4f}")

    # Project actual
    proj_actual = project_p2(gaps)
    var_actual  = variance(proj_actual)

    # Save actual P2 projection for CAILculator
    out_path = os.path.join(script_dir, f'p12a_actual_n{n_pairs}_P2.json')
    with open(out_path, 'w') as f:
        json.dump(proj_actual, f)
    print(f"  Saved p12a_actual_n{n_pairs}_P2.json ({len(proj_actual)} values)")

    # Generate GUE ensemble
    gue_vars = []
    for seed in GUE_SEEDS:
        gaps_gue  = sample_wigner(len(gaps), mean_gap, seed)
        proj_gue  = project_p2(gaps_gue)
        var_gue   = variance(proj_gue)
        gue_vars.append(var_gue)

        # Save GUE P2 projection for CAILculator
        out_path = os.path.join(script_dir, f'p12a_gue_s{seed}_n{n_pairs}_P2.json')
        with open(out_path, 'w') as f:
            json.dump(proj_gue, f)

    gue_var_mean = sum(gue_vars) / len(gue_vars)
    ratio        = var_actual / gue_var_mean

    print(f"  Var(actual)={var_actual:.6f}  Var(GUE mean)={gue_var_mean:.6f}  "
          f"Act/GUE={ratio:.4f}")

    new_results.append({
        "n_pairs":      n_pairs,
        "mean_gap":     mean_gap,
        "var_actual":   var_actual,
        "var_gue_mean": gue_var_mean,
        "var_gue_seeds": gue_vars,
        "act_gue_ratio": ratio,
        "source":       "Phase 12A",
    })

# ── Print full trend table ────────────────────────────────────────────────────
print("\n" + "-"*55)
print(f"{'n_pairs':>8}  {'mean_gap':>9}  {'Act/GUE':>8}  Source")
print("-"*55)
for row in prior_data:
    mg_str = "~2.24" if row['n_pairs'] <= 998 else "varies"
    print(f"{row['n_pairs']:>8}  {'~2.24':>9}  {row['mean']:>8.4f}  {row['source']}")
for row in new_results:
    print(f"{row['n_pairs']:>8}  {row['mean_gap']:>9.4f}  "
          f"{row['act_gue_ratio']:>8.4f}  Phase 12A")

# ── Asymptote assessment ──────────────────────────────────────────────────────
print("\nAsymptote assessment:")
ratios_new = [r['act_gue_ratio'] for r in new_results]
if ratios_new[-1] - ratios_new[0] < 0.02:
    print("  PLATEAU: ratio stable across n=2000-9998 (+/-0.02) -> asymptote identified")
elif ratios_new[-1] > ratios_new[0]:
    print("  CONTINUING DRIFT: ratio still increasing at n=9998")
else:
    print("  REVERSAL: ratio decreased from n=2000 to n=9998")

# ── Save results ──────────────────────────────────────────────────────────────
summary = {
    "phase": "12A",
    "question": "Does Act/GUE P2 variance ratio plateau at ~0.75 or continue drifting?",
    "note_p2_only": "P2 direction only (prior phases showed all P-vectors track together)",
    "prior_data": prior_data,
    "new_data":   new_results,
    "gue_seeds":  GUE_SEEDS,
    "files": {
        "actual":  [f"p12a_actual_n{n}_P2.json" for n in SCALES],
        "gue":     [f"p12a_gue_s{s}_n{n}_P2.json" for s in GUE_SEEDS for n in SCALES],
    }
}
out_path = os.path.join(script_dir, 'p12a_results.json')
with open(out_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nResults saved to p12a_results.json")
print(f"P2 projection files ready for CAILculator conjugation_symmetry calls.")
