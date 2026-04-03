
import numpy as np
import json

def get_gamma(n):
    gammas = json.load(open('rh_zeros_10k.json'))
    return gammas[n-1]

C = 1.55
def get_phase(gamma):
    return (C * np.log(gamma)) % (2 * np.pi)

points = [1000, 4950, 5000]
for n in points:
    g = get_gamma(n)
    log_g = np.log(g)
    phase = get_phase(g)
    print(f"n={n:5d}: gamma={g:8.2f}, log_gamma={log_g:8.4f}, phase={phase:8.4f}")
