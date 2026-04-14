import numpy as np
import math

def get_F_vector(t, sigma):
    c2 = math.cos(t * math.log(2))
    s2 = math.sin(t * math.log(2))
    s3 = math.sin(t * math.log(3))
    inv_sqrt2 = 1/math.sqrt(2)
    
    u_antisym = np.zeros(16)
    u_antisym[4] = inv_sqrt2
    u_antisym[5] = -inv_sqrt2
    u_antisym[10] = inv_sqrt2
    u_antisym[11] = -inv_sqrt2
    
    f_base = np.zeros(16)
    f_base[0] = c2
    f_base[15] = c2
    f_base[3] = s2
    f_base[12] = s2
    f_base[6] = s3
    f_base[9] = s3
    
    f = f_base + (sigma - 0.5) * u_antisym
    return f

t = 14.134725
sigmas = [0.3, 0.5, 0.8, 1.0, 1.1, 1.5, 2.0]

for sigma in sigmas:
    vec = get_F_vector(t, sigma)
    print(f'sigma={sigma}: {list(vec)}')
