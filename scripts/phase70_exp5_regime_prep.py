import numpy as np
import math

def get_euler_factors(t, sigma):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    factors = []
    for p in primes:
        s = complex(sigma, t)
        factor = 1 / (1 - p**(-s))
        factors.append(factor)
    return factors

t = 14.134725
sigmas = np.arange(0.1, 2.05, 0.05)

for sigma in sigmas:
    factors = get_euler_factors(t, sigma)
    vec = [f.real for f in factors]
    print(f'sigma={sigma:.2f}: {vec}')
