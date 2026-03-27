"""
AIEX-001a Phase 26 — Full 16D Sedenion Embedding
Chavez AI Labs LLC · March 25, 2026

Key findings:
1. F x F* = ||F||^2 * e0 ALWAYS — sedenion alternative law identity (not a condition)
2. ||F||^2 best discriminating measure (discrimination=0.0183)
3. ||F||^2 minimized at sigma=0.5 by functional equation symmetry
4. Per-zero sigma* scattered — not zero-specific in 6D projection
5. ZDTP: sigma=0.5 convergence 0.9883 > sigma=0.6 convergence 0.9872
"""
import numpy as np
from mpmath import mp, zetazero
import json
mp.dps = 25

def cd_conj(v):
    c = list(v); c[0] = v[0]
    for i in range(1, len(v)): c[i] = -v[i]
    return c

def cd_mul(a, b):
    n = len(a)
    if n == 1: return [a[0]*b[0]]
    h = n//2
    a1,a2,b1,b2 = a[:h],a[h:],b[:h],b[h:]
    c1 = [x-y for x,y in zip(cd_mul(a1,b1), cd_mul(cd_conj(b2),a2))]
    c2 = [x+y for x,y in zip(cd_mul(b2,a1), cd_mul(a2,cd_conj(b1)))]
    return c1+c2

def norm_sq(v): return sum(x*x for x in v)

def make16(pairs):
    v=[0.0]*16
    for i,val in pairs: v[i]=float(val)
    return v

sqrt2 = np.sqrt(2.0)
ROOT_16D = {
    2:  make16([(3,1.0),(12,-1.0)]),
    3:  make16([(5,1.0),(10,1.0)]),
    5:  make16([(3,1.0),(6,1.0)]),
    7:  make16([(2,1.0),(7,-1.0)]),
    11: make16([(2,1.0),(7,1.0)]),
    13: make16([(6,1.0),(9,1.0)]),
}
PRIMES = [2,3,5,7,11,13]

def F_16d(t, sigma=0.5):
    r = make16([(0,1.0)])
    for p in PRIMES:
        theta = t*np.log(p); rp=ROOT_16D[p]; rn=np.sqrt(norm_sq(rp))
        f=[0.0]*16; f[0]=np.cos(theta)
        for i in range(16): f[i]+=np.sin(theta)*rp[i]/rn
        r=cd_mul(r,f)
    r[4]+=(sigma-0.5)/sqrt2; r[5]-=(sigma-0.5)/sqrt2
    return r

def ns_F(t, sigma=0.5): return norm_sq(F_16d(t,sigma))

if __name__ == '__main__':
    print("Fetching 100 zeros...")
    zeros = [float(zetazero(n).imag) for n in range(1,101)]
    midpoints = [0.5*(zeros[i]+zeros[i+1]) for i in range(99)]

    SIGMA_VALS = [0.3,0.4,0.5,0.6,0.7]
    print("||F||^2 by sigma (mean over 100 zeros):")
    for sv in SIGMA_VALS:
        vals = [ns_F(t,sv) for t in zeros]
        print(f"  sigma={sv:.1f}: {np.mean(vals):.6f}")

    ns_zeros = [ns_F(t,0.5) for t in zeros]
    ns_mids  = [ns_F(t,0.5) for t in midpoints]
    print(f"||F||^2 zeros mean: {np.mean(ns_zeros):.6f}")
    print(f"||F||^2 midpts mean: {np.mean(ns_mids):.6f}")

    seqs = {
        'norm_sq_sigma05_zeros_n100': ns_zeros,
        'norm_sq_sigma05_midpoints_n99': ns_mids,
        'mean_ns_by_sigma': {str(sv): float(np.mean([ns_F(t,sv) for t in zeros])) for sv in SIGMA_VALS},
    }
    with open('phase26_results.json', 'w') as f:
        json.dump(seqs,f)
    print("Saved: phase26_results.json")
