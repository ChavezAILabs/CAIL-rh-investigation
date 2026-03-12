"""
RH Phase 12C — Berry-Keating Prime Orbit Extension
====================================================
Question: Where does the BK prime orbit correlation peak?
Phase 11B reached r=0.7338 at p=23. Extend to p=29, 31, 37, 41, 43, 47, 53.
Find the peak and characterize the interference pattern.

BK prime orbit sum model:
  R_c(t) = sum over primes p: (1/sqrt(p)) * cos(log(p)*t)
          + sum over prime squares p^2: (1/p) * cos(log(p^2)*t)

Base model (Phase 10A, primes 2,3,5,7,11 + squares):
  r = 0.6135 (vs stored 0.5428 — normalization difference, see Phase 11B note)

Phase 11B extensions (p=13,17,19,23):
  +p=13,17: r=0.6793 (first crossing)
  +p=13,17,19,23: r=0.7338

Data: t_mids and band_deltas_ensemble from rh_phase10a_definitive.json
Correlation: Pearson r between R_c(t_mids) and band_deltas_ensemble (n=10)
Significance threshold: |r| > 0.632 (p<0.05, n=10)
"""

import json
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# ── Load Phase 10A data ───────────────────────────────────────────────────────
with open(os.path.join(script_dir, 'rh_phase10a_definitive.json'), 'r') as f:
    data10a = json.load(f)

t_mids   = data10a['t_mids']             # 10 band midpoints
deltas   = data10a['band_deltas_ensemble']  # actual - GUE_ensemble_mean per band

print(f"Band midpoints: {t_mids}")
print(f"Band deltas:    {[round(d, 4) for d in deltas]}")

# ── Pearson r ─────────────────────────────────────────────────────────────────
def pearson_r(xs, ys):
    n = len(xs)
    mx = sum(xs)/n;  my = sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
    sx  = math.sqrt(sum((x-mx)**2 for x in xs))
    sy  = math.sqrt(sum((y-my)**2 for y in ys))
    return num / (sx * sy) if sx * sy > 0 else 0.0

# ── Build R_c incrementally ───────────────────────────────────────────────────
def rc_value(t, primes):
    """Compute R_c(t) for given set of primes (each contributes p-term + p^2 term)."""
    total = 0.0
    for p in primes:
        total += (1.0 / math.sqrt(p)) * math.cos(math.log(p) * t)
        total += (1.0 / p)            * math.cos(math.log(p*p) * t)
    return total

def rc_vector(t_list, primes):
    return [rc_value(t, primes) for t in t_list]

# ── Primes to test (Phase 11B already did 2-23) ───────────────────────────────
# Start from base (2,3,5,7,11) then re-derive phase 11B, then extend
PRIMES_BASE  = [2, 3, 5, 7, 11]
PRIMES_11B   = [13, 17, 19, 23]          # Phase 11B additions
PRIMES_12C   = [29, 31, 37, 41, 43, 47, 53, 59, 61, 67]  # Phase 12C additions

SIGNIFICANCE = 0.632   # p<0.05, n=10

# ── Compute r at each cumulative prime set ─────────────────────────────────────
results = []
active_primes = []

print("\n" + "="*65)
print("PHASE 12C — BK PRIME ORBIT EXTENSION")
print(f"Significance threshold: |r| > {SIGNIFICANCE}  (p<0.05, n=10)")
print("="*65)
print(f"\n{'Primes added':>12}  {'All primes':>30}  {'r':>7}  {'Sig?':>6}")
print("-"*65)

for prime in PRIMES_BASE + PRIMES_11B + PRIMES_12C:
    active_primes.append(prime)
    rc_vec = rc_vector(t_mids, active_primes)
    r = pearson_r(rc_vec, deltas)
    sig = "YES" if abs(r) >= SIGNIFICANCE else "no"
    label = "BASE" if prime in PRIMES_BASE else ("11B" if prime in PRIMES_11B else "12C")
    prime_str = str(sorted(active_primes))
    if len(prime_str) > 30:
        prime_str = f"[{','.join(str(p) for p in active_primes[-4:])}] +prev"
    print(f"{f'+p={prime} ({label})':>14}  {str(sorted(active_primes)):>30}  {r:>7.4f}  {sig:>6}")
    results.append({
        "prime_added": prime,
        "all_primes":  sorted(active_primes[:]),
        "n_primes":    len(active_primes),
        "r":           r,
        "significant": abs(r) >= SIGNIFICANCE,
    })

# ── Find peak ─────────────────────────────────────────────────────────────────
peak = max(results, key=lambda x: x['r'])
print(f"\nPeak r = {peak['r']:.4f} at +p={peak['prime_added']} "
      f"(n_primes={peak['n_primes']})")
print(f"Peak primes: {peak['all_primes']}")

# ── Phase 11B cross-check ──────────────────────────────────────────────────────
# Verify Phase 11B first-crossing result
print("\nPhase 11B cross-check (expect first sig crossing at +p=17):")
for row in results:
    if row['prime_added'] in [11, 13, 17, 19, 23]:
        print(f"  +p={row['prime_added']}: r={row['r']:.4f}  sig={row['significant']}")

# ── Interference pattern ───────────────────────────────────────────────────────
print("\nInterference pattern (r change when each prime added):")
prev_r = 0.0
for row in results:
    change = row['r'] - prev_r
    direction = "constructive" if change > 0 else "destructive"
    print(f"  +p={row['prime_added']:>3}: dr={change:+.4f} ({direction})")
    prev_r = row['r']

# ── Save ───────────────────────────────────────────────────────────────────────
summary = {
    "phase": "12C",
    "question": "Where does BK prime orbit correlation peak?",
    "t_mids":  t_mids,
    "deltas":  deltas,
    "significance_threshold": SIGNIFICANCE,
    "results": results,
    "peak": peak,
    "phase_11b_first_crossing": next(
        (r for r in results if r['significant'] and r['prime_added'] >= 13), None
    ),
    "n_significant": sum(1 for r in results if r['significant']),
}
out_path = os.path.join(script_dir, 'p12c_results.json')
with open(out_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nResults saved to p12c_results.json")
