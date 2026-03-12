"""
RH Phase 10B Data Preparation
Computes Riemann zeros 1,001 through 10,000 using mpmath.
Appends to existing rh_zeros.json to produce rh_zeros_10k.json.

Runtime: ~35-45 minutes at mp.dps=15
Run unattended: python rh_zeros_10k.py
"""

import mpmath
import json
import time
import os

mpmath.mp.dps = 15

script_dir = os.path.dirname(os.path.abspath(__file__))

zeros_path = os.path.join(script_dir, 'rh_zeros.json')
output_path = os.path.join(script_dir, 'rh_zeros_10k.json')
gaps_output_path = os.path.join(script_dir, 'rh_gaps_10k.json')

print("RH Phase 10B — Zero Computation")
print("=" * 40)

with open(zeros_path, 'r') as f:
    zeros_existing = json.load(f)

print(f"Loaded {len(zeros_existing)} existing zeros")
print(f"Range: {zeros_existing[0]:.6f} to {zeros_existing[-1]:.6f}")
print(f"Computing zeros 1001-10000...")
print()

zeros_new = []
start_time = time.time()

for n in range(1001, 10001):
    z = float(mpmath.im(mpmath.zetazero(n)))
    zeros_new.append(z)

    if n % 100 == 0:
        elapsed = time.time() - start_time
        rate = (n - 1000) / elapsed
        remaining = (9000 - (n - 1000)) / rate
        print(f"  Zero {n:5d}: {z:12.6f} | "
              f"{elapsed:6.1f}s elapsed | "
              f"~{remaining/60:.1f} min remaining | "
              f"{rate:.1f} zeros/sec")

elapsed_total = time.time() - start_time
print()
print(f"Computation complete in {elapsed_total/60:.1f} minutes")

zeros_10k = zeros_existing + zeros_new

with open(output_path, 'w') as f:
    json.dump(zeros_10k, f)

print(f"Saved {len(zeros_10k)} zeros to rh_zeros_10k.json")
print(f"Range: {zeros_10k[0]:.6f} to {zeros_10k[-1]:.6f}")

gaps_10k = [zeros_10k[i+1] - zeros_10k[i] for i in range(len(zeros_10k)-1)]

with open(gaps_output_path, 'w') as f:
    json.dump(gaps_10k, f)

print(f"Saved {len(gaps_10k)} gaps to rh_gaps_10k.json")
print()
print("Done. Files ready for Phase 10B.")
print(f"  {output_path}")
print(f"  {gaps_output_path}")
