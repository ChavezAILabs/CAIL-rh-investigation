import math
import cmath

def get_euler_factors(t, sigma):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    factors = []
    for p in primes:
        s = complex(sigma, t)
        factor = 1 / (1 - p**(-s))
        factors.append(factor)
    return factors

def encode_16d(factors):
    # Encoding strategy: use the real parts of the first 16 factors
    return [f.real for f in factors]

t = 14.134725
sigmas = [2.0, 1.5, 1.2, 1.05, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5]

for sigma in sigmas:
    factors = get_euler_factors(t, sigma)
    vec = encode_16d(factors)
    print(f'sigma={sigma}: {vec}')
