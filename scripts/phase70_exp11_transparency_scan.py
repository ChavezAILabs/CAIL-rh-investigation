import numpy as np
import mpmath

def get_F_vector(t, sigma=0.5):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
    factors = []
    for p in primes:
        s = complex(sigma, t)
        factor = 1 / (1 - p**(-s))
        factors.append(factor)
    return [f.real for f in factors]

ns = range(4995, 5006)
for n in ns:
    gamma_n = float(mpmath.zetazero(n).imag)
    vec = get_F_vector(gamma_n)
    print(f'n={n} (gamma={gamma_n}): {vec}')
