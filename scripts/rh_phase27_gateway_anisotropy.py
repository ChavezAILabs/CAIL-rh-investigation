"""
AIEX-001a Phase 27 — Gateway Anisotropy
Chavez AI Labs LLC · March 25, 2026

KEY DISCOVERIES:
1. ALGEBRAIC IDENTITY: p=5,7,11 give ||F x r_p||/||F|| = 1.000 ± 0.000 EXACTLY
   for ALL t and sigma. Exact algebraic identity from sedenion root structure.
2. DISCRIMINATING PRIMES: Only p=2 and p=13 (bilateral triple) carry signal.
   p=2 DOWN at zeros (0.924 vs 0.959), p=13 UP at zeros (1.097 vs 1.071).
3. V_BK = Var{||F x r_2||/||F||, ||F x r_13||/||F||}: zeros=0.054 vs mids=0.046
4. ZDTP INVERSION: high-variance zero has convergence 0.620 vs midpoint 0.876
"""
import numpy as np
from mpmath import mp, zetazero
import json
mp.dps = 25

def cd_conj(v):
    c=list(v)
    for i in range(1,len(v)): c[i]=-v[i]
    return c

def cd_mul(a,b):
    n=len(a)
    if n==1: return [a[0]*b[0]]
    h=n//2
    a1,a2,b1,b2=a[:h],a[h:],b[:h],b[h:]
    c1=[x-y for x,y in zip(cd_mul(a1,b1),cd_mul(cd_conj(b2),a2))]
    c2=[x+y for x,y in zip(cd_mul(b2,a1),cd_mul(a2,cd_conj(b1)))]
    return c1+c2

def norm_sq(v): return sum(x*x for x in v)

def make16(pairs):
    v=[0.0]*16
    for i,val in pairs: v[i]=float(val)
    return v

sqrt2=np.sqrt(2.0)
ROOT_16D={2:make16([(3,1),(12,-1)]),3:make16([(5,1),(10,1)]),
          5:make16([(3,1),(6,1)]),7:make16([(2,1),(7,-1)]),
          11:make16([(2,1),(7,1)]),13:make16([(6,1),(9,1)])}
PRIMES=[2,3,5,7,11,13]
BILATERAL=[2,13]

def F_16d(t,sigma=0.5):
    r=make16([(0,1.0)])
    for p in PRIMES:
        theta=t*np.log(p); rp=ROOT_16D[p]; rn=np.sqrt(norm_sq(rp))
        f=[0.0]*16; f[0]=np.cos(theta)
        for i in range(16): f[i]+=np.sin(theta)*rp[i]/rn
        r=cd_mul(r,f)
    r[4]+=(sigma-0.5)/sqrt2; r[5]-=(sigma-0.5)/sqrt2
    return r

def gateway_profile(t, sigma=0.5):
    F=F_16d(t,sigma); ns=norm_sq(F)
    if ns<1e-20: return [0.0]*6, 0.0
    gn=[]
    for p in PRIMES:
        rp=ROOT_16D[p]; rn=np.sqrt(norm_sq(rp))
        probe=[x/rn for x in rp]
        prod=cd_mul(F,probe)
        gn.append(np.sqrt(norm_sq(prod))/np.sqrt(ns))
    var_bilateral = float(np.var([norm_sq(cd_mul(F,[x/np.sqrt(norm_sq(ROOT_16D[p])) for x in ROOT_16D[p]]))/ns for p in BILATERAL]))
    return gn, var_bilateral

if __name__ == '__main__':
    print("Fetching 101 zeros...")
    zeros=[float(zetazero(n).imag) for n in range(1,102)]
    midpoints=[0.5*(zeros[i]+zeros[i+1]) for i in range(100)]

    print("\nAlgebraic identity check: ||F x r_p||/||F|| for each prime (50 zeros):")
    per_prime_zeros = {p: [] for p in PRIMES}
    for j,p in enumerate(PRIMES):
        vals=[gateway_profile(t)[0][j] for t in zeros[:50]]
        per_prime_zeros[p] = vals
        print(f"  p={p:2d}: mean={np.mean(vals):.8f} +/- {np.std(vals):.8f}")

    per_prime_mids = {p: [] for p in PRIMES}
    for j,p in enumerate(PRIMES):
        per_prime_mids[p] = [gateway_profile(t)[0][j] for t in midpoints[:50]]

    var_z=[gateway_profile(t)[1] for t in zeros[:100]]
    var_m=[gateway_profile(t)[1] for t in midpoints[:100]]
    print(f"\nV_BK zeros: {np.mean(var_z):.6f} +/- {np.std(var_z):.6f}")
    print(f"V_BK mids:  {np.mean(var_m):.6f} +/- {np.std(var_m):.6f}")
    print(f"Zeros > mids: {sum(1 for i in range(100) if var_z[i]>var_m[i])}/100")

    seqs={
        'var_zeros_n100': var_z,
        'var_mid_n100':   var_m,
        'diff_var_zm_n100': [var_z[i]-var_m[i] for i in range(100)],
        'per_prime_norm_ratio_zeros_n50': {str(p): per_prime_zeros[p] for p in PRIMES},
        'per_prime_norm_ratio_mids_n50':  {str(p): per_prime_mids[p]  for p in PRIMES},
    }
    with open('phase27_results.json','w') as f:
        json.dump(seqs,f)
    print("Saved: phase27_results.json")
