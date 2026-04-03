import json
import numpy as np

with open("CAIL-rh-investigation/data/riemann/rh_zeros_10k.json", "r") as f:
    zeros = json.load(f)

def get_spacing(n_start, count=10):
    subset = zeros[n_start:n_start+count]
    log_subset = np.log(subset)
    diffs = np.diff(log_subset)
    return np.mean(diffs)

n_1k = 1000
n_5k = 5000
n_10k = 10000

s1 = get_spacing(n_1k)
s5 = get_spacing(n_5k)
s10 = get_spacing(n_10k - 11) # Last 10 gaps

print(f"n=1000 spacing:  {s1:.8f}")
print(f"n=5000 spacing:  {s5:.8f}")
print(f"n=10000 spacing: {s10:.8f}")

# Frequency estimate C = 1 / (spacing * n_peaks_per_period)
# If Phase 56 saw 3 peaks in 101 zeros, that's ~33 zeros per peak.
# Let's say period P_log = spacing * 33
print(f"n=1000 estimated period:  {s1 * 33:.8f}")
print(f"n=5000 estimated period:  {s5 * 33:.8f}")
print(f"n=10000 estimated period: {s10 * 33:.8f}")
